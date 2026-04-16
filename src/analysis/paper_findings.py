"""
Paper Findings Generator
========================
Generates key statistics and findings for the paper manuscript.
Run after PubMed validation gap analysis completes.
"""

import json
import sys
import io
from collections import Counter, defaultdict
from pathlib import Path

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.builder import JamuKG
from src.kg.schema import NodeType, EdgeType


def generate_paper_findings(kg_path: str, pubmed_path: str, output_path: str):
    """Generate all key findings for the paper."""

    # Load KG
    kg = JamuKG()
    kg.load(kg_path)
    stats = kg.stats()

    # Load PubMed results
    with open(pubmed_path, "r", encoding="utf-8") as f:
        pubmed_results = json.load(f)

    findings = {}

    # === FINDING 1: KG Scale ===
    findings["kg_scale"] = {
        "total_nodes": stats["total_nodes"],
        "total_edges": stats["total_edges"],
        "plants": stats["nodes_by_type"].get("plant", 0),
        "compounds": stats["nodes_by_type"].get("compound", 0),
        "diseases": stats["nodes_by_type"].get("disease", 0),
        "bioactivities": stats["nodes_by_type"].get("bioactivity", 0),
        "formulations": stats["nodes_by_type"].get("formulation", 0),
        "connected_components": stats["connected_components"],
    }

    # === FINDING 2: Validation Gap ===
    evidence_dist = Counter(r["evidence_level"] for r in pubmed_results)
    total_pairs = len(pubmed_results)
    pct_none = evidence_dist.get("none", 0) / max(total_pairs, 1) * 100
    pct_well = evidence_dist.get("well_studied", 0) / max(total_pairs, 1) * 100

    findings["validation_gap"] = {
        "total_pairs_analyzed": total_pairs,
        "evidence_distribution": dict(evidence_dist),
        "pct_no_evidence": round(pct_none, 1),
        "pct_limited": round(evidence_dist.get("limited", 0) / max(total_pairs, 1) * 100, 1),
        "pct_moderate": round(evidence_dist.get("moderate", 0) / max(total_pairs, 1) * 100, 1),
        "pct_well_studied": round(pct_well, 1),
    }

    # === FINDING 3: Drug Discovery Candidates ===
    # Plants with most unstudied claims
    plant_unstudied = defaultdict(list)
    plant_studied = defaultdict(list)
    for r in pubmed_results:
        if r["evidence_level"] == "none":
            plant_unstudied[r["plant_name"]].append(r["disease_name"])
        else:
            plant_studied[r["plant_name"]].append({
                "disease": r["disease_name"],
                "pubmed_count": r["pubmed_count"],
                "level": r["evidence_level"],
            })

    top_candidates = sorted(plant_unstudied.items(), key=lambda x: len(x[1]), reverse=True)[:30]
    findings["drug_discovery_candidates"] = [
        {"plant": plant, "unstudied_claims": len(diseases), "diseases": diseases[:10]}
        for plant, diseases in top_candidates
    ]

    # === FINDING 4: Most Validated Traditional Claims ===
    well_studied = [r for r in pubmed_results if r["evidence_level"] == "well_studied"]
    well_studied.sort(key=lambda x: x["pubmed_count"], reverse=True)
    findings["most_validated_claims"] = [
        {
            "plant": r["plant_name"],
            "disease": r["disease_name"],
            "pubmed_count": r["pubmed_count"],
        }
        for r in well_studied[:30]
    ]

    # === FINDING 5: Multi-Source Consensus Plants ===
    multi_source_plants = []
    for n, data in kg.graph.nodes(data=True):
        if data.get("node_type") != NodeType.PLANT.value:
            continue
        sources = data.get("sources", [])
        if isinstance(sources, list) and len(sources) > 1:
            multi_source_plants.append({
                "plant": data.get("latin_name", n),
                "sources": sources,
                "num_sources": len(sources),
            })
    multi_source_plants.sort(key=lambda x: x["num_sources"], reverse=True)
    findings["multi_source_plants"] = {
        "count": len(multi_source_plants),
        "total_plants": stats["nodes_by_type"].get("plant", 0),
        "top_plants": multi_source_plants[:20],
    }

    # === FINDING 6: Disease Gap Analysis ===
    disease_gap = defaultdict(lambda: {"total": 0, "unstudied": 0, "studied": 0, "well_studied": 0})
    for r in pubmed_results:
        d = r["disease_name"]
        disease_gap[d]["total"] += 1
        if r["evidence_level"] == "none":
            disease_gap[d]["unstudied"] += 1
        elif r["evidence_level"] == "well_studied":
            disease_gap[d]["well_studied"] += 1
        else:
            disease_gap[d]["studied"] += 1

    # Diseases with most unstudied claims (drug discovery opportunity areas)
    diseases_by_gap = sorted(disease_gap.items(), key=lambda x: x[1]["unstudied"], reverse=True)
    findings["disease_gap_analysis"] = [
        {"disease": d, **v} for d, v in diseases_by_gap[:30]
    ]

    # === FINDING 7: Key Statistics for Paper Abstract ===
    findings["abstract_stats"] = {
        "total_plants": stats["nodes_by_type"].get("plant", 0),
        "total_compounds": stats["nodes_by_type"].get("compound", 0),
        "total_diseases": stats["nodes_by_type"].get("disease", 0),
        "total_treat_edges": stats["edges_by_type"].get("treats", 0),
        "total_produce_edges": stats["edges_by_type"].get("produces", 0),
        "validation_gap_pct": round(pct_none, 1),
        "total_pairs_queried": total_pairs,
        "drug_candidates_count": len([p for p in plant_unstudied if len(plant_unstudied[p]) >= 5]),
    }

    # Save
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)

    # Print
    print("\n" + "=" * 70)
    print("PAPER FINDINGS SUMMARY")
    print("=" * 70)

    print(f"\n--- KG Scale ---")
    for k, v in findings["kg_scale"].items():
        print(f"  {k}: {v:,}")

    print(f"\n--- Validation Gap (Core Finding) ---")
    print(f"  Total plant-disease pairs: {total_pairs:,}")
    print(f"  No evidence: {findings['validation_gap']['pct_no_evidence']}%")
    print(f"  Limited: {findings['validation_gap']['pct_limited']}%")
    print(f"  Moderate: {findings['validation_gap']['pct_moderate']}%")
    print(f"  Well-studied: {findings['validation_gap']['pct_well_studied']}%")

    print(f"\n--- Top 10 Drug Discovery Candidates ---")
    for c in findings["drug_discovery_candidates"][:10]:
        print(f"  {c['plant']:40s}: {c['unstudied_claims']} unstudied claims")

    print(f"\n--- Top 10 Most Validated Traditional Claims ---")
    for c in findings["most_validated_claims"][:10]:
        print(f"  {c['plant']:35s} -> {c['disease']:25s} ({c['pubmed_count']} papers)")

    print(f"\n--- Multi-Source Consensus ---")
    print(f"  Plants in multiple databases: {findings['multi_source_plants']['count']}/{findings['multi_source_plants']['total_plants']}")

    print(f"\n--- Abstract-Ready Numbers ---")
    a = findings["abstract_stats"]
    print(f"  JamuKG integrates {a['total_plants']:,} plants, {a['total_compounds']:,} compounds,")
    print(f"  {a['total_diseases']:,} diseases with {a['total_treat_edges']:,} traditional treatment claims.")
    print(f"  Cross-referencing with PubMed reveals that {a['validation_gap_pct']}% of")
    print(f"  {a['total_pairs_queried']:,} plant-disease associations have ZERO published evidence,")
    print(f"  identifying {a['drug_candidates_count']} plants with 5+ unstudied claims")
    print(f"  as priority drug discovery candidates.")

    return findings


def main():
    base_dir = Path(__file__).parent.parent.parent

    # Find latest KG
    kg_dir = base_dir / "data" / "kg"
    kg_files = sorted(f for f in kg_dir.glob("jamukg_v*.json") if "_stats" not in f.name and "_annotated" not in f.name)
    kg_path = kg_files[-1] if kg_files else kg_dir / "jamukg_v01.json"

    pubmed_path = base_dir / "data" / "raw" / "pubmed" / "validation_gap_results.json"
    output_path = base_dir / "data" / "kg" / "paper_findings.json"

    if not pubmed_path.exists():
        print("Error: Run PubMed validation gap analysis first.")
        return

    generate_paper_findings(str(kg_path), str(pubmed_path), str(output_path))


if __name__ == "__main__":
    main()
