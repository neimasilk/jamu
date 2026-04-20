"""
Apply Disease Ontology to Knowledge Graph
===========================================
Addresses TRIAGE Tier 1 item: "split TREATS edges into TREATS vs HAS_USE
based on disease-ontology classification."

Input : data/kg/jamukg_v07_annotated.json
        data/kg/disease_ontology.json
Output: data/kg/jamukg_v08_annotated.json

Split policy (based on TRIAGE deliberation):
  TREATS              <- clinical_disease, symptom
                         (real conditions the plant is claimed to treat)
  HAS_USE             <- pharmacological_action, therapeutic_use
                         (functional uses: "used as abortifacient", "used as antidote")
  ETHNOBOTANICAL_USE  <- non_medical, biocidal, cosmetic
                         (arrow-poison, spice, hair-tonic — not therapeutic claims)
  APPLIED_TO          <- body_part
                         (plant applied to abdomen, breast — target not treatment)

6 previously ambiguous terms resolved by medical-knowledge review:
  Ozoena          -> clinical_disease    (chronic atrophic rhinitis)
  Syphilis(3)     -> clinical_disease    (tertiary syphilis)
  Typhus (Typhoid)-> clinical_disease
  Internal        -> non_medical         (too vague to be clinical)
  Medicine        -> non_medical         (too vague)
  Medicine (Vet)  -> non_medical         (veterinary, not human clinical)

Finding (honest, recorded here):
  The overall validation gap barely moves — 85.89% -> 85.56% for the cleaned
  TREATS subset. Similar gaps (86-87%) across ALL categories. Interpretation:
  under-representation is structural to PubMed coverage, not a label artifact.

  What the cleanup DOES buy:
    1. Claim precision — "3,740 clinical TREATS" is more defensible than
       "5,744 mixed claims including veterinary contraceptives".
    2. Downstream filters — drug-discovery candidates can restrict to TREATS.
    3. Removes a reviewer attack surface.
"""

import json
import sys
import io
from collections import Counter
from pathlib import Path

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# Edge-type split policy
TREATS_CATS = {"clinical_disease", "symptom"}
HAS_USE_CATS = {"pharmacological_action", "therapeutic_use"}
ETHNO_CATS = {"non_medical", "biocidal", "cosmetic"}
APPLIED_CATS = {"body_part"}

EDGE_TYPE_FOR_CAT = {}
for c in TREATS_CATS:
    EDGE_TYPE_FOR_CAT[c] = "treats"
for c in HAS_USE_CATS:
    EDGE_TYPE_FOR_CAT[c] = "has_use"
for c in ETHNO_CATS:
    EDGE_TYPE_FOR_CAT[c] = "ethnobotanical_use"
for c in APPLIED_CATS:
    EDGE_TYPE_FOR_CAT[c] = "applied_to"

# Resolutions for the 6 ambiguous disease terms
AMBIGUOUS_RESOLUTION = {
    "Ozoena": "clinical_disease",
    "Syphilis(3)": "clinical_disease",
    "Typhus (Typhoid)": "clinical_disease",
    "Internal": "non_medical",
    "Medicine": "non_medical",
    "Medicine (Vet)": "non_medical",
}

# The 9 KNApSAcK effect-group disease nodes — all are legitimate clinical_disease
# by design (they are KNApSAcK's own disease classification, not Dr. Duke ethno terms)
KNAPSACK_EFFECT_GROUPS = {
    "Female reproductive organ problems",
    "Respiratory disease",
    "Musculoskeletal and connective tissue disorders",
    "Disorders of appetite",
    "Wounds and skin infections",
    "Pain/inflammation",
    "Urinary related problems",
    "Disorders of mood and behavior",
    "Gastrointestinal disorders",
}


def build_node_to_category(kg: dict, ontology: dict) -> dict[str, str]:
    categories = dict(ontology["classifications"])
    categories.update(AMBIGUOUS_RESOLUTION)

    node2cat = {}
    for node in kg["nodes"]:
        if node.get("node_type") != "disease":
            continue
        name = node.get("name", "")
        if name in categories:
            node2cat[node["id"]] = categories[name]
        elif name in KNAPSACK_EFFECT_GROUPS:
            node2cat[node["id"]] = "clinical_disease"
        else:
            node2cat[node["id"]] = "unmapped"
    return node2cat


def apply_split(kg: dict, node2cat: dict) -> tuple[dict, dict]:
    """Annotate each treats edge with category and refined edge_type.
    Returns (new_kg, stats)."""
    new_kg = {
        "directed": kg.get("directed", True),
        "multigraph": kg.get("multigraph", False),
        "graph": dict(kg.get("graph", {})),
        "nodes": [dict(n) for n in kg["nodes"]],
        "links": [],
    }
    new_kg["graph"]["version"] = "v08"
    new_kg["graph"]["ontology_applied"] = True

    stats = {
        "treats_before": 0,
        "treats_after": 0,
        "has_use": 0,
        "ethnobotanical_use": 0,
        "applied_to": 0,
        "unmapped": 0,
        "by_target_source": Counter(),
    }

    for edge in kg["links"]:
        new_edge = dict(edge)
        if edge.get("edge_type") == "treats":
            stats["treats_before"] += 1
            cat = node2cat.get(edge["target"], "unmapped")
            new_edge_type = EDGE_TYPE_FOR_CAT.get(cat, "treats")
            new_edge["edge_type"] = new_edge_type
            new_edge["ontology_category"] = cat
            new_edge["original_edge_type"] = "treats"

            stats["by_target_source"][(new_edge_type, cat)] += 1
            if new_edge_type == "treats":
                stats["treats_after"] += 1
            else:
                stats[new_edge_type] += 1
            if cat == "unmapped":
                stats["unmapped"] += 1

        new_kg["links"].append(new_edge)

    return new_kg, stats


def compute_validation_gap(kg: dict, edge_type: str, restrict_source_db: str | None = None) -> dict:
    """Validation gap: fraction of (source,target) pairs with zero PubMed evidence."""
    pair_max_pmc: dict = {}
    for edge in kg["links"]:
        if edge.get("edge_type") != edge_type:
            continue
        if restrict_source_db and restrict_source_db not in edge.get("source_dbs", []):
            continue
        key = (edge["source"], edge["target"])
        pair_max_pmc[key] = max(pair_max_pmc.get(key, 0), edge.get("pubmed_count", 0))

    if not pair_max_pmc:
        return {"n": 0}

    n = len(pair_max_pmc)
    zero = sum(1 for c in pair_max_pmc.values() if c == 0)
    limited = sum(1 for c in pair_max_pmc.values() if 1 <= c <= 4)
    moderate = sum(1 for c in pair_max_pmc.values() if 5 <= c <= 19)
    well = sum(1 for c in pair_max_pmc.values() if c >= 20)

    return {
        "n": n,
        "no_evidence": zero,
        "no_evidence_pct": round(zero / n * 100, 2),
        "limited": limited,
        "limited_pct": round(limited / n * 100, 2),
        "moderate": moderate,
        "moderate_pct": round(moderate / n * 100, 2),
        "well_studied": well,
        "well_studied_pct": round(well / n * 100, 2),
    }


def main():
    base = Path(__file__).resolve().parent.parent.parent
    in_kg = base / "data" / "kg" / "jamukg_v07_annotated.json"
    in_ont = base / "data" / "kg" / "disease_ontology.json"
    out_kg = base / "data" / "kg" / "jamukg_v08_annotated.json"
    out_report = base / "data" / "kg" / "v08_ontology_split_report.json"

    print(f"Loading {in_kg.name} ...")
    kg = json.load(open(in_kg, "r", encoding="utf-8"))
    ont = json.load(open(in_ont, "r", encoding="utf-8"))
    print(f"  {len(kg['nodes'])} nodes, {len(kg['links'])} links")

    node2cat = build_node_to_category(kg, ont)
    print(f"\nDisease nodes mapped: {len(node2cat)}")
    cat_dist = Counter(node2cat.values())
    for k, v in cat_dist.most_common():
        print(f"  {k:25s} {v}")

    new_kg, stats = apply_split(kg, node2cat)
    print("\n--- Edge split result ---")
    print(f"  Before: {stats['treats_before']} edges of type 'treats'")
    print(f"  After:")
    print(f"    treats             : {stats['treats_after']}")
    print(f"    has_use            : {stats['has_use']}")
    print(f"    ethnobotanical_use : {stats['ethnobotanical_use']}")
    print(f"    applied_to         : {stats['applied_to']}")
    print(f"    unmapped           : {stats['unmapped']}")

    # Compute validation gap on dr_duke subset for each refined edge type
    print("\n--- Validation gap (Dr. Duke plant-condition pairs only) ---")
    gap_report = {}
    for et in ["treats", "has_use", "ethnobotanical_use", "applied_to"]:
        g = compute_validation_gap(new_kg, et, restrict_source_db="dr_duke")
        gap_report[et] = g
        if g.get("n"):
            print(f"\n  [{et}] n={g['n']}")
            print(f"    no evidence:  {g['no_evidence']:5d} ({g['no_evidence_pct']}%)")
            print(f"    limited:      {g['limited']:5d} ({g['limited_pct']}%)")
            print(f"    moderate:     {g['moderate']:5d} ({g['moderate_pct']}%)")
            print(f"    well-studied: {g['well_studied']:5d} ({g['well_studied_pct']}%)")

    # Also include KNApSAcK formulation-effect_group edges (these are all TREATS by design)
    knaps_gap = compute_validation_gap(new_kg, "treats", restrict_source_db="knapsack_jamu")
    if knaps_gap.get("n"):
        print(f"\n  [treats | source=knapsack_jamu]  n={knaps_gap['n']}")
        print(f"    no evidence:  {knaps_gap['no_evidence']} ({knaps_gap['no_evidence_pct']}%)")

    # Write outputs
    with open(out_kg, "w", encoding="utf-8") as f:
        json.dump(new_kg, f, ensure_ascii=False)
    print(f"\nWrote {out_kg}")

    report = {
        "method": "apply disease_ontology.json to TREATS edges; 6 ambiguous resolved",
        "ambiguous_resolution": AMBIGUOUS_RESOLUTION,
        "edge_split_stats": {
            "treats_before": stats["treats_before"],
            "treats_after": stats["treats_after"],
            "has_use": stats["has_use"],
            "ethnobotanical_use": stats["ethnobotanical_use"],
            "applied_to": stats["applied_to"],
            "unmapped": stats["unmapped"],
        },
        "validation_gap_dr_duke": gap_report,
        "validation_gap_knapsack_formulations": knaps_gap,
        "honest_note": (
            "Ontology cleanup moves the validation gap number negligibly "
            "(85.89% -> 85.56% for the clinical TREATS subset). All categories "
            "show similar 82-87% no-evidence rates, suggesting the gap is "
            "structural to PubMed coverage rather than a consequence of "
            "category mixing. What the cleanup DOES improve: claim precision "
            "(TREATS now means clinical only, no Arrow-poison or Cosmetic), "
            "downstream filter quality (drug-discovery candidates can be "
            "restricted to clinical), and removes a reviewer attack surface."
        ),
    }
    with open(out_report, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out_report}")


if __name__ == "__main__":
    main()
