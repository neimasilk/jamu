"""
JamuKG Visualization
====================
Generates interactive and static visualizations of the knowledge graph.
"""

import json
import os
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import networkx as nx

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.builder import JamuKG
from src.kg.schema import NodeType, EdgeType

# Color scheme for node types
NODE_COLORS = {
    NodeType.PLANT.value: "#4CAF50",        # Green
    NodeType.COMPOUND.value: "#2196F3",      # Blue
    NodeType.DISEASE.value: "#F44336",       # Red
    NodeType.BIOACTIVITY.value: "#FF9800",   # Orange
    NodeType.FORMULATION.value: "#9C27B0",   # Purple
}

NODE_LABELS = {
    NodeType.PLANT.value: "Plant",
    NodeType.COMPOUND.value: "Compound",
    NodeType.DISEASE.value: "Disease",
    NodeType.BIOACTIVITY.value: "Bioactivity",
    NodeType.FORMULATION.value: "Formulation",
}


def plot_kg_overview(kg: JamuKG, output_path: str):
    """Bar chart of node and edge type distributions."""
    stats = kg.stats()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Node distribution
    node_types = stats["nodes_by_type"]
    labels = [NODE_LABELS.get(k, k) for k in node_types.keys()]
    values = list(node_types.values())
    colors = [NODE_COLORS.get(k, "#999") for k in node_types.keys()]

    bars = axes[0].barh(labels, values, color=colors)
    axes[0].set_xlabel("Count")
    axes[0].set_title(f"JamuKG Nodes (n={stats['total_nodes']:,})")
    for bar, val in zip(bars, values):
        axes[0].text(bar.get_width() + 50, bar.get_y() + bar.get_height() / 2,
                     f"{val:,}", va="center", fontsize=9)

    # Edge distribution
    edge_types = stats["edges_by_type"]
    e_labels = list(edge_types.keys())
    e_values = list(edge_types.values())

    bars2 = axes[1].barh(e_labels, e_values, color="#607D8B")
    axes[1].set_xlabel("Count")
    axes[1].set_title(f"JamuKG Edges (n={stats['total_edges']:,})")
    for bar, val in zip(bars2, e_values):
        axes[1].text(bar.get_width() + 50, bar.get_y() + bar.get_height() / 2,
                     f"{val:,}", va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_top_plants(kg: JamuKG, output_path: str, top_n: int = 25):
    """Top plants by number of disease associations."""
    plant_diseases = Counter()
    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.TREATS.value:
            u_data = kg.graph.nodes[u]
            if u_data.get("node_type") == NodeType.PLANT.value:
                name = u_data.get("latin_name", u)
                if name:
                    plant_diseases[name] += 1

    top = plant_diseases.most_common(top_n)
    # Filter out empty names
    top = [(name, count) for name, count in top if name.strip()][:top_n]

    fig, ax = plt.subplots(figsize=(10, 8))
    names = [t[0] for t in reversed(top)]
    counts = [t[1] for t in reversed(top)]

    ax.barh(names, counts, color="#4CAF50")
    ax.set_xlabel("Number of Disease Associations (Traditional Claims)")
    ax.set_title(f"Top {len(top)} Nusantara Medicinal Plants by Traditional Use Breadth")

    for i, (name, count) in enumerate(zip(names, counts)):
        ax.text(count + 0.3, i, str(count), va="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_top_diseases(kg: JamuKG, output_path: str, top_n: int = 25):
    """Top diseases by number of plant treatments."""
    disease_plants = Counter()
    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.TREATS.value:
            v_data = kg.graph.nodes[v]
            if v_data.get("node_type") == NodeType.DISEASE.value:
                name = v_data.get("name", v)
                disease_plants[name] += 1

    top = disease_plants.most_common(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))
    names = [t[0] for t in reversed(top)]
    counts = [t[1] for t in reversed(top)]

    ax.barh(names, counts, color="#F44336")
    ax.set_xlabel("Number of Plants Used as Treatment")
    ax.set_title(f"Top {top_n} Conditions in Nusantara Traditional Medicine")

    for i, count in enumerate(counts):
        ax.text(count + 0.5, i, str(count), va="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_top_compounds(kg: JamuKG, output_path: str, top_n: int = 25):
    """Top compounds by number of bioactivities."""
    compound_acts = Counter()
    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.HAS_ACTIVITY.value:
            name = kg.graph.nodes[u].get("name", u)
            compound_acts[name] += 1

    top = compound_acts.most_common(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))
    names = [t[0] for t in reversed(top)]
    counts = [t[1] for t in reversed(top)]

    ax.barh(names, counts, color="#2196F3")
    ax.set_xlabel("Number of Known Bioactivities")
    ax.set_title(f"Top {top_n} Bioactive Compounds in Nusantara Plants")

    for i, count in enumerate(counts):
        ax.text(count + 0.3, i, str(count), va="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_validation_gap(pubmed_results_path: str, output_path: str):
    """Pie/bar chart of validation gap distribution."""
    if not os.path.exists(pubmed_results_path):
        print(f"PubMed results not found at {pubmed_results_path}")
        return

    with open(pubmed_results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    evidence_dist = Counter(r["evidence_level"] for r in results)

    labels_map = {
        "none": "No Evidence",
        "limited": "Limited (1-5)",
        "moderate": "Moderate (6-20)",
        "well_studied": "Well-Studied (20+)",
    }
    colors_map = {
        "none": "#BDBDBD",
        "limited": "#FFE082",
        "moderate": "#81C784",
        "well_studied": "#4CAF50",
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Pie chart
    labels = [labels_map.get(k, k) for k in evidence_dist.keys()]
    sizes = list(evidence_dist.values())
    colors = [colors_map.get(k, "#999") for k in evidence_dist.keys()]

    wedges, texts, autotexts = axes[0].pie(
        sizes, labels=labels, colors=colors, autopct="%1.1f%%",
        startangle=90, textprops={"fontsize": 9}
    )
    axes[0].set_title(f"Validation Gap Distribution\n(n={sum(sizes):,} plant-disease pairs)")

    # Bar chart by disease
    from collections import defaultdict
    disease_evidence = defaultdict(lambda: {"studied": 0, "unstudied": 0})
    for r in results:
        d = r["disease_name"]
        if r["evidence_level"] != "none":
            disease_evidence[d]["studied"] += 1
        else:
            disease_evidence[d]["unstudied"] += 1

    # Top 15 diseases by total claims
    top_diseases = sorted(disease_evidence.items(),
                         key=lambda x: x[1]["studied"] + x[1]["unstudied"],
                         reverse=True)[:15]

    d_names = [t[0] for t in reversed(top_diseases)]
    d_studied = [t[1]["studied"] for t in reversed(top_diseases)]
    d_unstudied = [t[1]["unstudied"] for t in reversed(top_diseases)]

    y_pos = range(len(d_names))
    axes[1].barh(y_pos, d_studied, color="#4CAF50", label="Has PubMed Evidence")
    axes[1].barh(y_pos, d_unstudied, left=d_studied, color="#BDBDBD", label="No Evidence")
    axes[1].set_yticks(y_pos)
    axes[1].set_yticklabels(d_names, fontsize=8)
    axes[1].set_xlabel("Number of Plant-Disease Claims")
    axes[1].set_title("Validation Gap by Disease")
    axes[1].legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def generate_subgraph_html(kg: JamuKG, center_plant: str, output_path: str, depth: int = 2):
    """Generate interactive HTML visualization of a plant's neighborhood."""
    try:
        from pyvis.network import Network
    except ImportError:
        print("pyvis not installed, skipping HTML visualization")
        return

    # BFS from center plant
    if center_plant not in kg.graph:
        print(f"Plant {center_plant} not found in KG")
        return

    subgraph_nodes = set()
    frontier = {center_plant}
    for _ in range(depth):
        next_frontier = set()
        for node in frontier:
            subgraph_nodes.add(node)
            for neighbor in kg.graph.successors(node):
                next_frontier.add(neighbor)
            for neighbor in kg.graph.predecessors(node):
                next_frontier.add(neighbor)
        frontier = next_frontier - subgraph_nodes
    subgraph_nodes.update(frontier)

    # Limit to manageable size
    if len(subgraph_nodes) > 200:
        subgraph_nodes = set(list(subgraph_nodes)[:200])

    sub = kg.graph.subgraph(subgraph_nodes)

    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="#333333")
    net.barnes_hut(gravity=-3000, spring_length=150)

    for node in sub.nodes():
        data = kg.graph.nodes[node]
        ntype = data.get("node_type", "")
        color = NODE_COLORS.get(ntype, "#999")
        label = data.get("name", data.get("latin_name", node))
        if len(label) > 30:
            label = label[:27] + "..."
        size = 15 if node != center_plant else 30
        net.add_node(node, label=label, color=color, size=size,
                     title=f"{NODE_LABELS.get(ntype, ntype)}: {data.get('name', data.get('latin_name', node))}")

    for u, v, data in sub.edges(data=True):
        etype = data.get("edge_type", "")
        net.add_edge(u, v, title=etype, label=etype, font={"size": 8})

    net.save_graph(output_path)
    print(f"Saved interactive graph: {output_path}")


def plot_validation_heatmap(pubmed_results_path: str, output_path: str, top_plants: int = 30, top_diseases: int = 20):
    """Heatmap of plant x disease evidence levels — key paper figure."""
    if not os.path.exists(pubmed_results_path):
        print(f"PubMed results not found at {pubmed_results_path}")
        return

    with open(pubmed_results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    import numpy as np

    # Count plant and disease occurrences to find top ones
    plant_count = Counter(r["plant_name"] for r in results)
    disease_count = Counter(r["disease_name"] for r in results)

    top_p = [p for p, _ in plant_count.most_common(top_plants)]
    top_d = [d for d, _ in disease_count.most_common(top_diseases)]

    # Build matrix: 0=no data, 1=no evidence, 2=limited, 3=moderate, 4=well_studied
    evidence_to_num = {"none": 1, "limited": 2, "moderate": 3, "well_studied": 4}
    matrix = np.zeros((len(top_p), len(top_d)))

    for r in results:
        if r["plant_name"] in top_p and r["disease_name"] in top_d:
            pi = top_p.index(r["plant_name"])
            di = top_d.index(r["disease_name"])
            matrix[pi, di] = evidence_to_num.get(r["evidence_level"], 0)

    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["#FFFFFF", "#EF5350", "#FFE082", "#81C784", "#2E7D32"])

    fig, ax = plt.subplots(figsize=(16, 12))
    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=4)

    ax.set_xticks(range(len(top_d)))
    ax.set_xticklabels(top_d, rotation=45, ha="right", fontsize=7)
    ax.set_yticks(range(len(top_p)))
    ax.set_yticklabels([f"  {p}" for p in top_p], fontsize=7, style="italic")
    ax.set_title("Validation Gap Heatmap: Traditional Plant-Disease Claims vs. PubMed Evidence",
                 fontsize=11, fontweight="bold", pad=15)

    # Legend
    legend_labels = ["No claim", "No evidence (gap!)", "Limited (1-5)", "Moderate (6-20)", "Well-studied (20+)"]
    legend_colors = ["#FFFFFF", "#EF5350", "#FFE082", "#81C784", "#2E7D32"]
    patches = [mpatches.Patch(color=c, label=l) for c, l in zip(legend_colors, legend_labels)]
    ax.legend(handles=patches, loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_drug_discovery_candidates(pubmed_results_path: str, output_path: str, top_n: int = 30):
    """Bar chart of top drug discovery candidates: high traditional consensus + zero PubMed evidence."""
    if not os.path.exists(pubmed_results_path):
        return

    with open(pubmed_results_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    # Find plants with zero-evidence claims
    from collections import defaultdict
    plant_gaps = defaultdict(list)
    for r in results:
        if r["evidence_level"] == "none":
            plant_gaps[r["plant_name"]].append(r["disease_name"])

    # Rank by number of unstudied claims
    ranked = sorted(plant_gaps.items(), key=lambda x: len(x[1]), reverse=True)[:top_n]

    fig, ax = plt.subplots(figsize=(12, 10))
    names = [f"{r[0]}" for r in reversed(ranked)]
    counts = [len(r[1]) for r in reversed(ranked)]

    bars = ax.barh(names, counts, color="#EF5350", edgecolor="#B71C1C", linewidth=0.5)
    ax.set_xlabel("Number of Unstudied Traditional Claims (PubMed count = 0)")
    ax.set_title("Top Drug Discovery Candidates\nPlants with Most Unstudied Traditional Disease Associations",
                 fontsize=11, fontweight="bold")

    for bar, val in zip(bars, counts):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=8)

    # Add annotation
    ax.text(0.98, 0.02,
            "These plants have traditional claims\nbacked by empirical use across generations\nbut ZERO modern scientific validation.",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
            fontstyle="italic", color="#666666",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF9C4", alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_source_overlap(kg: JamuKG, output_path: str):
    """Venn-style bar chart showing multi-source consensus for plants."""
    from collections import defaultdict

    source_plants = defaultdict(set)
    for n, data in kg.graph.nodes(data=True):
        if data.get("node_type") != NodeType.PLANT.value:
            continue
        sources = data.get("sources", [])
        if isinstance(sources, list):
            for s in sources:
                source_plants[s].add(n)

    # Count overlaps
    all_sources = sorted(source_plants.keys())
    single_source = {}
    for s in all_sources:
        only_this = source_plants[s].copy()
        for other_s in all_sources:
            if other_s != s:
                only_this -= source_plants[other_s]
        single_source[s] = len(only_this)

    multi = set()
    for s in all_sources:
        for other_s in all_sources:
            if s != other_s:
                multi.update(source_plants[s] & source_plants[other_s])

    fig, ax = plt.subplots(figsize=(10, 5))

    x = range(len(all_sources) + 1)
    labels = [s.replace("_", "\n") for s in all_sources] + ["Multi-source\nconsensus"]
    values = [len(source_plants[s]) for s in all_sources] + [len(multi)]
    colors = ["#42A5F5", "#66BB6A", "#FFA726", "#EF5350"][:len(all_sources)] + ["#AB47BC"]

    bars = ax.bar(x, values, color=colors, edgecolor="white", linewidth=1.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Number of Plant Species")
    ax.set_title("Plant Coverage by Data Source", fontsize=11, fontweight="bold")

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                f"{val:,}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def main():
    base_dir = Path(__file__).parent.parent.parent

    # Find latest KG version
    kg_dir = base_dir / "data" / "kg"
    kg_files = sorted(kg_dir.glob("jamukg_v*.json"))
    kg_files = [f for f in kg_files if "_stats" not in f.name]
    kg_path = kg_files[-1] if kg_files else kg_dir / "jamukg_v01.json"
    print(f"Using KG: {kg_path.name}")

    fig_dir = base_dir / "figures"
    fig_dir.mkdir(exist_ok=True)

    print("Loading JamuKG...")
    kg = JamuKG()
    kg.load(str(kg_path))

    print("Generating figures...")
    plot_kg_overview(kg, str(fig_dir / "01_kg_overview.png"))
    plot_top_plants(kg, str(fig_dir / "02_top_plants.png"))
    plot_top_diseases(kg, str(fig_dir / "03_top_diseases.png"))
    plot_top_compounds(kg, str(fig_dir / "04_top_compounds.png"))
    plot_source_overlap(kg, str(fig_dir / "06_source_overlap.png"))

    # Validation gap (if available)
    pubmed_path = base_dir / "data" / "raw" / "pubmed" / "validation_gap_results.json"
    if pubmed_path.exists():
        plot_validation_gap(str(pubmed_path), str(fig_dir / "05_validation_gap.png"))
        plot_validation_heatmap(str(pubmed_path), str(fig_dir / "07_validation_heatmap.png"))
        plot_drug_discovery_candidates(str(pubmed_path), str(fig_dir / "08_drug_discovery_candidates.png"))

    # Interactive subgraph for key plants
    for plant_id in ["curcuma_longa", "zingiber_officinale", "piper_betle"]:
        if plant_id in kg.graph:
            generate_subgraph_html(
                kg, plant_id,
                str(fig_dir / f"interactive_{plant_id}.html"),
                depth=1,
            )

    print(f"\nAll figures saved to {fig_dir}/")


if __name__ == "__main__":
    main()
