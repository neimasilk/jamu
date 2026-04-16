"""
Network Pharmacology Analysis
==============================
Analyzes multi-target plants, compound-disease pathways,
and plant-plant similarity for the paper.
"""

import json
import sys
import io
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.builder import JamuKG
from src.kg.schema import NodeType, EdgeType


def analyze_multi_target_plants(kg: JamuKG) -> dict:
    """Find plants that treat multiple disease categories."""
    plant_diseases = defaultdict(set)
    plant_compounds = defaultdict(set)

    for u, v, data in kg.graph.edges(data=True):
        u_data = kg.graph.nodes.get(u, {})
        v_data = kg.graph.nodes.get(v, {})

        if data.get("edge_type") == EdgeType.TREATS.value:
            if u_data.get("node_type") == NodeType.PLANT.value:
                latin = u_data.get("latin_name", u)
                disease = v_data.get("name", v)
                category = v_data.get("disease_category", "unknown")
                plant_diseases[latin].add((disease, category))

        if data.get("edge_type") == EdgeType.PRODUCES.value:
            if u_data.get("node_type") == NodeType.PLANT.value:
                latin = u_data.get("latin_name", u)
                compound = v_data.get("name", v)
                plant_compounds[latin].add(compound)

    # Multi-target plants: treat 3+ disease categories
    multi_target = {}
    for plant, disease_set in plant_diseases.items():
        categories = set(cat for _, cat in disease_set if cat not in ("unknown", "pharmacological_effect", "non_medical"))
        if len(categories) >= 3:
            multi_target[plant] = {
                "num_categories": len(categories),
                "categories": sorted(categories),
                "num_diseases": len(disease_set),
                "num_compounds": len(plant_compounds.get(plant, set())),
            }

    return dict(sorted(multi_target.items(), key=lambda x: -x[1]["num_categories"]))


def analyze_compound_promiscuity(kg: JamuKG) -> dict:
    """Find compounds that appear in multiple plants treating different diseases."""
    compound_plants = defaultdict(set)
    compound_activities = defaultdict(set)

    for u, v, data in kg.graph.edges(data=True):
        u_data = kg.graph.nodes.get(u, {})
        v_data = kg.graph.nodes.get(v, {})

        if data.get("edge_type") == EdgeType.PRODUCES.value:
            compound = v_data.get("name", v)
            plant = u_data.get("latin_name", u)
            compound_plants[compound].add(plant)

        if data.get("edge_type") == EdgeType.HAS_ACTIVITY.value:
            compound = u_data.get("name", u)
            activity = v_data.get("name", v)
            compound_activities[compound].add(activity)

    # Promiscuous compounds: in 5+ plants AND 3+ activities
    promiscuous = {}
    for compound, plants in compound_plants.items():
        activities = compound_activities.get(compound, set())
        if len(plants) >= 5 and len(activities) >= 3:
            promiscuous[compound] = {
                "num_plants": len(plants),
                "num_activities": len(activities),
                "plants": sorted(list(plants))[:10],
                "activities": sorted(list(activities))[:10],
            }

    return dict(sorted(promiscuous.items(), key=lambda x: -x[1]["num_plants"]))


def analyze_plant_similarity(kg: JamuKG) -> list:
    """Find plant pairs that share many disease targets (potential substitutes)."""
    plant_diseases = defaultdict(set)

    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") != EdgeType.TREATS.value:
            continue
        u_data = kg.graph.nodes.get(u, {})
        if u_data.get("node_type") == NodeType.PLANT.value:
            plant_diseases[u].add(v)

    # Find pairs with high Jaccard similarity
    plants = list(plant_diseases.keys())
    similar_pairs = []

    for i in range(len(plants)):
        for j in range(i + 1, len(plants)):
            p1, p2 = plants[i], plants[j]
            d1, d2 = plant_diseases[p1], plant_diseases[p2]
            intersection = d1 & d2
            union = d1 | d2

            if len(intersection) >= 5 and len(union) > 0:
                jaccard = len(intersection) / len(union)
                if jaccard >= 0.2:
                    p1_name = kg.graph.nodes[p1].get("latin_name", p1)
                    p2_name = kg.graph.nodes[p2].get("latin_name", p2)
                    similar_pairs.append({
                        "plant1": p1_name,
                        "plant2": p2_name,
                        "shared_diseases": len(intersection),
                        "jaccard": round(jaccard, 3),
                        "union_size": len(union),
                    })

    similar_pairs.sort(key=lambda x: -x["jaccard"])
    return similar_pairs[:50]


def plot_disease_category_distribution(kg: JamuKG, output_path: str):
    """Pie chart of disease categories in the KG."""
    categories = Counter()
    for n, data in kg.graph.nodes(data=True):
        if data.get("node_type") == NodeType.DISEASE.value:
            cat = data.get("disease_category", "unknown")
            categories[cat] += 1

    # Group small categories
    threshold = 5
    main_cats = {k: v for k, v in categories.items() if v >= threshold}
    other = sum(v for k, v in categories.items() if v < threshold)
    if other > 0:
        main_cats["other"] = other

    fig, ax = plt.subplots(figsize=(10, 7))
    labels = list(main_cats.keys())
    sizes = list(main_cats.values())

    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.1f%%",
        startangle=90, textprops={"fontsize": 8}, pctdistance=0.85
    )
    ax.set_title("Disease Category Distribution in JamuKG\n(after normalization)", fontsize=11, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_validation_by_category(kg: JamuKG, pubmed_path: str, output_path: str):
    """Bar chart showing validation gap BY disease category."""
    with open(pubmed_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    # Build disease -> category lookup from KG
    disease_cat = {}
    for n, data in kg.graph.nodes(data=True):
        if data.get("node_type") == NodeType.DISEASE.value:
            disease_cat[data.get("name", n)] = data.get("disease_category", "unknown")

    # Group PubMed results by category
    cat_evidence = defaultdict(lambda: {"studied": 0, "unstudied": 0})
    for r in results:
        cat = disease_cat.get(r["disease_name"], "unknown")
        if cat in ("pharmacological_effect", "non_medical"):
            continue
        if r["evidence_level"] != "none":
            cat_evidence[cat]["studied"] += 1
        else:
            cat_evidence[cat]["unstudied"] += 1

    # Sort by total
    sorted_cats = sorted(cat_evidence.items(), key=lambda x: x[1]["studied"] + x[1]["unstudied"], reverse=True)
    sorted_cats = [(k, v) for k, v in sorted_cats if v["studied"] + v["unstudied"] >= 10]

    fig, ax = plt.subplots(figsize=(12, 6))
    cats = [c[0] for c in reversed(sorted_cats)]
    studied = [c[1]["studied"] for c in reversed(sorted_cats)]
    unstudied = [c[1]["unstudied"] for c in reversed(sorted_cats)]

    y = range(len(cats))
    ax.barh(y, studied, color="#4CAF50", label="Has PubMed evidence")
    ax.barh(y, unstudied, left=studied, color="#EF5350", label="No evidence (validation gap)")
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=9)
    ax.set_xlabel("Number of Plant-Disease Claims")
    ax.set_title("Validation Gap by Disease Category", fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)

    # Add gap percentages
    for i, (cat, data) in enumerate(reversed(sorted_cats)):
        total = data["studied"] + data["unstudied"]
        gap_pct = data["unstudied"] / total * 100
        ax.text(total + 2, i, f"{gap_pct:.0f}% gap", va="center", fontsize=8, color="#666")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_multi_target_plants(multi_target: dict, output_path: str, top_n: int = 20):
    """Bar chart of top multi-target plants."""
    top = list(multi_target.items())[:top_n]

    fig, ax = plt.subplots(figsize=(12, 8))
    names = [f"{p} ({v['num_compounds']} cpd)" for p, v in reversed(top)]
    num_cats = [v["num_categories"] for _, v in reversed(top)]
    num_diseases = [v["num_diseases"] for _, v in reversed(top)]

    y = range(len(names))
    bars = ax.barh(y, num_cats, color="#7E57C2", edgecolor="white")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8, style="italic")
    ax.set_xlabel("Number of Disease Categories Treated")
    ax.set_title("Multi-Target Medicinal Plants\n(treating multiple disease categories)", fontsize=11, fontweight="bold")

    for bar, nc, nd in zip(bars, num_cats, num_diseases):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f"{nc} cat, {nd} diseases", va="center", fontsize=7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def main():
    base_dir = Path(__file__).parent.parent.parent
    kg_dir = base_dir / "data" / "kg"
    fig_dir = base_dir / "figures"

    # Load normalized KG
    kg = JamuKG()
    kg_path = kg_dir / "jamukg_v02_normalized.json"
    if not kg_path.exists():
        kg_path = kg_dir / "jamukg_v02_annotated.json"
    kg.load(str(kg_path))
    print(f"Loaded: {kg_path.name}")

    # 1. Multi-target plants
    print("\n=== Multi-Target Plants ===")
    multi_target = analyze_multi_target_plants(kg)
    print(f"Found {len(multi_target)} multi-target plants (3+ disease categories)")
    for plant, data in list(multi_target.items())[:15]:
        print(f"  {plant:40s}: {data['num_categories']} categories, {data['num_diseases']} diseases, {data['num_compounds']} compounds")
        print(f"    Categories: {', '.join(data['categories'])}")

    # 2. Promiscuous compounds
    print("\n=== Promiscuous Compounds ===")
    promiscuous = analyze_compound_promiscuity(kg)
    print(f"Found {len(promiscuous)} promiscuous compounds (5+ plants, 3+ activities)")
    for compound, data in list(promiscuous.items())[:15]:
        print(f"  {compound:35s}: {data['num_plants']} plants, {data['num_activities']} activities")

    # 3. Similar plant pairs
    print("\n=== Similar Plant Pairs (potential substitutes) ===")
    similar = analyze_plant_similarity(kg)
    print(f"Found {len(similar)} similar plant pairs (Jaccard >= 0.2, shared >= 5)")
    for pair in similar[:15]:
        print(f"  {pair['plant1']:30s} <-> {pair['plant2']:30s} J={pair['jaccard']:.3f} ({pair['shared_diseases']} shared)")

    # 4. Plots
    plot_disease_category_distribution(kg, str(fig_dir / "09_disease_categories.png"))
    plot_multi_target_plants(multi_target, str(fig_dir / "10_multi_target_plants.png"))

    pubmed_path = base_dir / "data" / "raw" / "pubmed" / "validation_gap_results.json"
    if pubmed_path.exists():
        plot_validation_by_category(kg, str(pubmed_path), str(fig_dir / "11_validation_by_category.png"))

    # Save results
    results = {
        "multi_target_plants": {k: v for k, v in list(multi_target.items())[:50]},
        "promiscuous_compounds": {k: v for k, v in list(promiscuous.items())[:50]},
        "similar_plant_pairs": similar[:50],
    }
    with open(kg_dir / "network_pharmacology_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to {kg_dir / 'network_pharmacology_results.json'}")
    print(f"Figures saved to {fig_dir}/")


if __name__ == "__main__":
    main()
