"""
JamuKG Statistics & Analysis
=============================
Generates statistics and basic analysis of the JamuKG.
"""

import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.builder import JamuKG
from src.kg.schema import NodeType, EdgeType


def analyze_kg(kg_path: str):
    """Run comprehensive analysis on the KG."""
    kg = JamuKG()
    kg.load(kg_path)

    stats = kg.stats()

    print("=" * 70)
    print(f"JamuKG Analysis")
    print("=" * 70)
    print(f"Total nodes: {stats['total_nodes']:,}")
    print(f"Total edges: {stats['total_edges']:,}")
    print(f"Connected components: {stats['connected_components']:,}")

    # Node breakdown
    print(f"\n--- Nodes by Type ---")
    for ntype, count in sorted(stats["nodes_by_type"].items(), key=lambda x: -x[1]):
        print(f"  {ntype:20s}: {count:>6,}")

    # Edge breakdown
    print(f"\n--- Edges by Type ---")
    for etype, count in sorted(stats["edges_by_type"].items(), key=lambda x: -x[1]):
        print(f"  {etype:20s}: {count:>6,}")

    # Top plants by number of compounds
    print(f"\n--- Top 20 Plants by Number of Compounds ---")
    plant_compounds = Counter()
    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.PRODUCES.value:
            plant_name = kg.graph.nodes[u].get("latin_name", u)
            plant_compounds[plant_name] += 1

    for plant, count in plant_compounds.most_common(20):
        print(f"  {plant:45s}: {count:>4} compounds")

    # Top plants by number of disease associations
    print(f"\n--- Top 20 Plants by Disease Associations ---")
    plant_diseases = Counter()
    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.TREATS.value:
            node_type = kg.graph.nodes[u].get("node_type", "")
            if node_type == NodeType.PLANT.value:
                plant_name = kg.graph.nodes[u].get("latin_name", u)
                plant_diseases[plant_name] += 1

    for plant, count in plant_diseases.most_common(20):
        print(f"  {plant:45s}: {count:>4} diseases")

    # Top diseases by number of plant treatments
    print(f"\n--- Top 20 Diseases by Number of Plant Treatments ---")
    disease_plants = Counter()
    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.TREATS.value:
            disease_name = kg.graph.nodes[v].get("name", v)
            disease_plants[disease_name] += 1

    for disease, count in disease_plants.most_common(20):
        print(f"  {disease:45s}: {count:>4} plants")

    # Top compounds by bioactivity count
    print(f"\n--- Top 20 Compounds by Bioactivities ---")
    compound_activities = Counter()
    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.HAS_ACTIVITY.value:
            chem_name = kg.graph.nodes[u].get("name", u)
            compound_activities[chem_name] += 1

    for chem, count in compound_activities.most_common(20):
        print(f"  {chem:45s}: {count:>4} activities")

    # Source coverage
    print(f"\n--- Source Coverage ---")
    source_nodes = Counter()
    for n, data in kg.graph.nodes(data=True):
        sources = data.get("sources", [])
        if isinstance(sources, list):
            for s in sources:
                source_nodes[s] += 1

    for source, count in source_nodes.most_common():
        print(f"  {source:30s}: {count:>6,} nodes")

    # Plants with data from multiple sources
    multi_source = 0
    for n, data in kg.graph.nodes(data=True):
        if data.get("node_type") == NodeType.PLANT.value:
            sources = data.get("sources", [])
            if isinstance(sources, list) and len(sources) > 1:
                multi_source += 1

    total_plants = stats["nodes_by_type"].get(NodeType.PLANT.value, 0)
    print(f"\n  Plants in multiple sources: {multi_source}/{total_plants}")

    return stats


def main():
    base_dir = Path(__file__).parent.parent.parent
    kg_path = base_dir / "data" / "kg" / "jamukg_v01.json"

    if not kg_path.exists():
        print(f"Error: KG not found at {kg_path}")
        return

    analyze_kg(str(kg_path))


if __name__ == "__main__":
    main()
