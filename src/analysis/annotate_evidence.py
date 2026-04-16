"""
Evidence Annotator
==================
Annotates KG edges with PubMed evidence levels from validation gap results.
This is what transforms the KG from a traditional knowledge graph into
a scientifically cross-referenced resource.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.builder import JamuKG
from src.kg.schema import NodeType, EdgeType, EvidenceLevel


def annotate_kg_with_evidence(kg: JamuKG, pubmed_results_path: str) -> dict:
    """
    Annotate TREATS edges in the KG with PubMed evidence levels.
    Returns summary statistics.
    """
    with open(pubmed_results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    # Build lookup: (plant_name, disease_name) -> result
    lookup = {}
    for r in results:
        key = (r["plant_name"], r["disease_name"])
        lookup[key] = r

    annotated = 0
    not_found = 0

    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") != EdgeType.TREATS.value:
            continue

        u_data = kg.graph.nodes[u]
        v_data = kg.graph.nodes[v]

        if u_data.get("node_type") != NodeType.PLANT.value:
            continue
        if v_data.get("node_type") != NodeType.DISEASE.value:
            continue

        plant_name = u_data.get("latin_name", "")
        disease_name = v_data.get("name", "")

        key = (plant_name, disease_name)
        if key in lookup:
            r = lookup[key]
            data["evidence_level"] = r["evidence_level"]
            data["pubmed_count"] = r["pubmed_count"]
            data["pubmed_ids"] = r.get("pubmed_pmids", [])
            annotated += 1
        else:
            not_found += 1

    # Count evidence distribution
    evidence_dist = {}
    for _, _, data in kg.graph.edges(data=True):
        el = data.get("evidence_level", "none")
        evidence_dist[el] = evidence_dist.get(el, 0) + 1

    summary = {
        "annotated_edges": annotated,
        "not_found": not_found,
        "evidence_distribution": evidence_dist,
    }

    print(f"Annotated {annotated:,} TREATS edges with PubMed evidence")
    print(f"  Not found in PubMed results: {not_found:,}")
    print(f"  Evidence distribution: {evidence_dist}")

    return summary


def main():
    base_dir = Path(__file__).parent.parent.parent

    # Find latest KG
    kg_dir = base_dir / "data" / "kg"
    kg_files = sorted(f for f in kg_dir.glob("jamukg_v*.json") if "_stats" not in f.name)
    kg_path = kg_files[-1] if kg_files else kg_dir / "jamukg_v01.json"

    pubmed_path = base_dir / "data" / "raw" / "pubmed" / "validation_gap_results.json"
    if not pubmed_path.exists():
        print("Error: PubMed results not found. Run validation gap analysis first.")
        return

    print(f"Loading KG: {kg_path.name}")
    kg = JamuKG()
    kg.load(str(kg_path))

    summary = annotate_kg_with_evidence(kg, str(pubmed_path))

    # Save annotated KG
    version = kg_path.stem.split("_")[-1]  # e.g. "v01"
    output_path = kg_dir / f"jamukg_{version}_annotated.json"
    kg.save(str(output_path))
    print(f"Saved annotated KG to {output_path}")

    # Update stats
    stats = kg.stats()
    stats_path = kg_dir / f"jamukg_{version}_annotated_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    main()
