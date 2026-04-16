"""
Jamu Formulation Analysis
=========================
Generates formulation-specific figures (12-20) and the paper summary figure.
Uses KNApSAcK formula data and JamuKG.
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
import seaborn as sns

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def load_formulas(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def plot_top_jamu_herbs(formulas: list, output_path: str, top_n: int = 20):
    """Figure 12: Top herbs used in jamu formulas."""
    herb_freq = Counter()
    for formula in formulas:
        for herb in formula.get("herbs", []):
            name = herb.get("scientific_name", "").strip()
            if name:
                herb_freq[name] += 1

    top = herb_freq.most_common(top_n)
    fig, ax = plt.subplots(figsize=(12, 8))
    names = [f"{h[0]}" for h in reversed(top)]
    counts = [h[1] for h in reversed(top)]
    pcts = [c / len(formulas) * 100 for c in counts]

    bars = ax.barh(range(len(names)), counts, color="#4CAF50", edgecolor="white")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8, style="italic")
    ax.set_xlabel("Number of Formulas")
    ax.set_title(f"Top {top_n} Herbs in Jamu Formulas (n={len(formulas):,})",
                 fontsize=11, fontweight="bold")

    for bar, pct in zip(bars, pcts):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f"{pct:.1f}%", va="center", fontsize=7, color="#666")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_jamu_effect_groups(formulas: list, output_path: str):
    """Figure 13: Effect group distribution."""
    effects = Counter()
    for f in formulas:
        eg = f.get("jamu_effect_group", "").strip()
        if eg and eg != "-":
            effects[eg] += 1

    top = effects.most_common(15)
    fig, ax = plt.subplots(figsize=(12, 6))
    names = [e[0] for e in reversed(top)]
    counts = [e[1] for e in reversed(top)]

    bars = ax.barh(range(len(names)), counts, color="#2196F3", edgecolor="white")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("Number of Formulas")
    ax.set_title("Jamu Effect Group Distribution", fontsize=11, fontweight="bold")

    for bar, c in zip(bars, counts):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
                str(c), va="center", fontsize=8, color="#666")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_herb_cooccurrence(formulas: list, output_path: str, top_n: int = 15):
    """Figure 14: Herb co-occurrence heatmap."""
    herb_freq = Counter()
    for formula in formulas:
        for herb in formula.get("herbs", []):
            name = herb.get("scientific_name", "").strip()
            if name:
                herb_freq[name] += 1

    top_herbs = [h[0] for h in herb_freq.most_common(top_n)]
    cooccur = np.zeros((top_n, top_n), dtype=int)

    for formula in formulas:
        herbs = [h.get("scientific_name", "").strip()
                 for h in formula.get("herbs", []) if h.get("scientific_name")]
        for i, h1 in enumerate(top_herbs):
            if h1 in herbs:
                for j, h2 in enumerate(top_herbs):
                    if h2 in herbs and i != j:
                        cooccur[i][j] += 1

    fig, ax = plt.subplots(figsize=(12, 10))
    # Short names for readability
    short_names = []
    for h in top_herbs:
        parts = h.split()
        if len(parts) >= 2:
            short_names.append(f"{parts[0][0]}. {parts[1]}")
        else:
            short_names.append(h[:15])

    mask = np.triu(np.ones_like(cooccur, dtype=bool), k=0)
    sns.heatmap(cooccur, mask=mask, xticklabels=short_names, yticklabels=short_names,
                annot=True, fmt="d", cmap="YlOrRd", ax=ax,
                annot_kws={"fontsize": 7})
    ax.set_title("Herb Co-occurrence in Jamu Formulas", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_herb_specificity(formulas: list, output_path: str):
    """Figure 15: Herb therapeutic specificity (stacked bar)."""
    herb_effects = defaultdict(Counter)
    for formula in formulas:
        eg = formula.get("jamu_effect_group", "").strip()
        if not eg or eg == "-":
            continue
        for herb in formula.get("herbs", []):
            name = herb.get("scientific_name", "").strip()
            if name:
                herb_effects[name][eg] += 1

    # Get top herbs by total formula count
    herb_totals = {h: sum(c.values()) for h, c in herb_effects.items()}
    top_herbs = sorted(herb_totals, key=herb_totals.get, reverse=True)[:15]

    # Get all effect groups
    all_effects = sorted(set(eg for c in herb_effects.values() for eg in c.keys()))
    colors = plt.cm.Set3(np.linspace(0, 1, len(all_effects)))

    fig, ax = plt.subplots(figsize=(14, 8))
    y = range(len(top_herbs))
    left = np.zeros(len(top_herbs))

    for i, eg in enumerate(all_effects):
        values = [herb_effects[h].get(eg, 0) for h in top_herbs]
        ax.barh(y, values, left=left, color=colors[i], label=eg, edgecolor="white", linewidth=0.3)
        left += values

    short_names = []
    for h in reversed(top_herbs):
        parts = h.split()
        if len(parts) >= 2:
            short_names.append(f"{parts[0][0]}. {parts[1]}")
        else:
            short_names.append(h[:20])

    ax.set_yticks(y)
    ax.set_yticklabels(short_names, fontsize=8, style="italic")
    ax.set_xlabel("Number of Formulas")
    ax.set_title("Herb Therapeutic Specificity by Effect Group", fontsize=11, fontweight="bold")
    ax.legend(fontsize=7, loc="lower right", ncol=2)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_compound_bioactivity(kg_path: str, output_path: str, top_n: int = 20):
    """Figure 16: Compound bioactivity profile."""
    from src.kg.builder import JamuKG
    from src.kg.schema import NodeType, EdgeType

    kg = JamuKG()
    kg.load(kg_path)

    compound_activities = defaultdict(set)
    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") == EdgeType.HAS_ACTIVITY.value:
            u_data = kg.graph.nodes.get(u, {})
            v_data = kg.graph.nodes.get(v, {})
            compound = u_data.get("name", u)
            activity = v_data.get("name", v)
            compound_activities[compound].add(activity)

    top = sorted(compound_activities.items(), key=lambda x: -len(x[1]))[:top_n]

    fig, ax = plt.subplots(figsize=(12, 8))
    names = [c[0] for c in reversed(top)]
    counts = [len(c[1]) for c in reversed(top)]

    bars = ax.barh(range(len(names)), counts, color="#FF9800", edgecolor="white")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Number of Known Bioactivities")
    ax.set_title(f"Top {top_n} Bioactive Compounds in JamuKG", fontsize=11, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_plant_families(formulas: list, output_path: str):
    """Figure 17: Plant family distribution (Zingiberaceae dominance)."""
    zing_prefixes = ["Curcuma", "Zingiber", "Kaempferia", "Alpinia", "Amomum",
                     "Elettaria", "Hedychium", "Boesenbergia", "Languas"]
    piper_prefixes = ["Piper"]
    apiaceae = ["Foeniculum", "Coriandrum", "Apium", "Centella"]

    family_count = Counter()
    for formula in formulas:
        herbs = set()
        for herb in formula.get("herbs", []):
            name = herb.get("scientific_name", "").strip()
            if not name:
                continue
            genus = name.split()[0] if name else ""
            if any(name.startswith(p) for p in zing_prefixes):
                herbs.add("Zingiberaceae")
            elif any(name.startswith(p) for p in piper_prefixes):
                herbs.add("Piperaceae")
            elif any(name.startswith(p) for p in apiaceae):
                herbs.add("Apiaceae")
            else:
                herbs.add("Other")
        for fam in herbs:
            family_count[fam] += 1

    total = len(formulas)
    fig, ax = plt.subplots(figsize=(8, 6))
    families = sorted(family_count.items(), key=lambda x: -x[1])
    names = [f[0] for f in families]
    counts = [f[1] for f in families]
    pcts = [c / total * 100 for c in counts]
    colors = ["#4CAF50", "#FF9800", "#2196F3", "#9E9E9E"]

    bars = ax.bar(names, counts, color=colors[:len(names)], edgecolor="white")
    ax.set_ylabel("Number of Formulas")
    ax.set_title("Plant Family Presence in Jamu Formulas", fontsize=11, fontweight="bold")

    for bar, pct in zip(bars, pcts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                f"{pct:.1f}%", ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def plot_paper_summary(formulas: list, pubmed_path: str, stats_path: str, output_path: str):
    """Figure 00: 4-panel paper summary figure."""
    with open(pubmed_path, "r", encoding="utf-8") as f:
        pubmed = json.load(f)
    with open(stats_path, "r", encoding="utf-8") as f:
        stats = json.load(f)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Panel A: KG overview
    ax = axes[0, 0]
    node_types = stats["nodes_by_type"]
    labels = list(node_types.keys())
    values = list(node_types.values())
    colors = ["#4CAF50", "#F44336", "#2196F3", "#FF9800", "#9C27B0"]
    ax.bar(labels, values, color=colors[:len(labels)], edgecolor="white")
    ax.set_title("A. JamuKG Node Distribution", fontsize=10, fontweight="bold")
    ax.set_ylabel("Count")
    for i, (l, v) in enumerate(zip(labels, values)):
        ax.text(i, v + max(values)*0.01, f"{v:,}", ha="center", fontsize=8)

    # Panel B: Validation gap
    ax = axes[0, 1]
    evidence = Counter(r["evidence_level"] for r in pubmed)
    gap_labels = ["None\n(85.9%)", "Limited\n(10.5%)", "Moderate\n(2.3%)", "Well-studied\n(1.3%)"]
    gap_values = [evidence.get("none", 0), evidence.get("limited", 0),
                  evidence.get("moderate", 0), evidence.get("well_studied", 0)]
    gap_colors = ["#EF5350", "#FFA726", "#66BB6A", "#42A5F5"]
    wedges, texts, autotexts = ax.pie(gap_values, labels=gap_labels, colors=gap_colors,
                                       autopct="", startangle=90,
                                       textprops={"fontsize": 8})
    ax.set_title("B. Validation Gap (5,744 pairs)", fontsize=10, fontweight="bold")

    # Panel C: Top drug discovery candidates
    ax = axes[1, 0]
    plant_unstudied = defaultdict(int)
    for r in pubmed:
        if r["evidence_level"] == "none":
            plant_unstudied[r["plant_name"]] += 1
    top_cands = sorted(plant_unstudied.items(), key=lambda x: -x[1])[:10]
    cand_names = [f"{c[0][:25]}" for c in reversed(top_cands)]
    cand_counts = [c[1] for c in reversed(top_cands)]
    ax.barh(range(len(cand_names)), cand_counts, color="#7E57C2", edgecolor="white")
    ax.set_yticks(range(len(cand_names)))
    ax.set_yticklabels(cand_names, fontsize=7, style="italic")
    ax.set_xlabel("Unstudied Claims")
    ax.set_title("C. Top Drug Discovery Candidates", fontsize=10, fontweight="bold")

    # Panel D: Top herbs in formulas
    ax = axes[1, 1]
    herb_freq = Counter()
    for formula in formulas:
        for herb in formula.get("herbs", []):
            name = herb.get("scientific_name", "").strip()
            if name:
                herb_freq[name] += 1
    top_herbs = herb_freq.most_common(10)
    herb_names = [f"{h[0].split()[0][0]}. {' '.join(h[0].split()[1:])}" if len(h[0].split()) >= 2 else h[0]
                  for h in reversed(top_herbs)]
    herb_counts = [h[1] for h in reversed(top_herbs)]
    ax.barh(range(len(herb_names)), herb_counts, color="#4CAF50", edgecolor="white")
    ax.set_yticks(range(len(herb_names)))
    ax.set_yticklabels(herb_names, fontsize=7, style="italic")
    ax.set_xlabel("Number of Formulas")
    ax.set_title(f"D. Top Herbs in Jamu (n={len(formulas):,})", fontsize=10, fontweight="bold")

    fig.suptitle("JamuKG: Mapping the Validation Gap in Indonesian Traditional Medicine",
                 fontsize=12, fontweight="bold", y=1.01)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def main():
    base_dir = Path(__file__).parent.parent.parent
    fig_dir = base_dir / "figures"
    fig_dir.mkdir(exist_ok=True)

    # Load formulas
    formulas_path = base_dir / "data" / "raw" / "knapsack" / "knapsack_jamu_formulas.json"
    formulas = load_formulas(str(formulas_path))
    print(f"Loaded {len(formulas)} formulas")

    # Find latest KG
    kg_dir = base_dir / "data" / "kg"
    kg_files = sorted(f for f in kg_dir.glob("jamukg_v*_annotated.json"))
    if not kg_files:
        kg_files = sorted(f for f in kg_dir.glob("jamukg_v*.json") if "_stats" not in f.name)
    kg_path = str(kg_files[-1]) if kg_files else None

    # Generate figures
    plot_top_jamu_herbs(formulas, str(fig_dir / "12_top_jamu_herbs.png"))
    plot_jamu_effect_groups(formulas, str(fig_dir / "13_jamu_effect_groups.png"))
    plot_herb_cooccurrence(formulas, str(fig_dir / "14_herb_cooccurrence.png"))
    plot_herb_specificity(formulas, str(fig_dir / "15_herb_therapeutic_specificity.png"))
    plot_plant_families(formulas, str(fig_dir / "17_plant_families.png"))

    if kg_path:
        plot_compound_bioactivity(kg_path, str(fig_dir / "16_compound_bioactivity_profile.png"))

    # Paper summary figure
    pubmed_path = base_dir / "data" / "raw" / "pubmed" / "validation_gap_results.json"
    stats_path = base_dir / "data" / "kg" / "jamukg_latest_stats.json"
    if pubmed_path.exists() and stats_path.exists():
        plot_paper_summary(formulas, str(pubmed_path), str(stats_path),
                          str(fig_dir / "00_paper_summary_figure.png"))

    print(f"\nAll formulation figures saved to {fig_dir}/")


if __name__ == "__main__":
    main()
