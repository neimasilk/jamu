"""
Mazhab Network Visualization
=============================
Renders the 11 stable mazhab + 5 bridge singletons identified by
src/analysis/herb_communities.py as a single network figure.

Inputs (already exist):
  data/raw/knapsack/knapsack_jamu_formulas.json  — formulas (rebuild lift graph)
  data/kg/jamu_herb_communities.json             — community assignments + bridges
  data/kg/jamu_grammar.json                      — herb roles + forbidden pairs

Output:
  figures/21_mazhab_network.png        — main figure (full network + forbidden overlay)
  figures/22_mazhab_small_multiples.png — per-mazhab subgraphs

Design choices
--------------
* Reuse exact same lift-graph parameters as herb_communities.py (min_freq=40,
  min_obs=5, lift>1.5) so what is drawn is the *same* graph the consensus
  Louvain ran on. No new analysis, no new parameters.
* Node colour = community id. Bridge singletons get a distinct neutral grey
  with diamond marker and labels (they are the "named" finding).
* Node size ~ sqrt(total formulas) so visual weight tracks salience.
* Edge alpha ~ lift, capped — graph is dense and would otherwise be a hairball.
* Forbidden pairs from jamu_grammar.forbidden_combinations drawn as dashed red
  lines on top of (or alongside) the lift edges. They are not lift edges by
  construction (zero co-occurrence) so adding them as overlays makes the
  cross-mazhab structural claim visible.
"""

import json
import sys
import io
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import networkx as nx

# Reuse the exact lift-graph builder from herb_communities to avoid drift.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from herb_communities import build_herb_index, build_lift_graph, COMMUNITY_LABELS

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# Tab20-derived palette, keeping the 11 colours visually distinguishable.
COMMUNITY_COLORS = {
    0: "#d62728",   # warming musculoskeletal — red
    1: "#9467bd",   # female reproductive — purple
    2: "#2ca02c",   # GI bitter / hepato — green
    3: "#17becf",   # GI aromatic — teal
    4: "#ff7f0e",   # male tonic — orange
    5: "#bcbd22",   # rhizome bitters — olive
    6: "#8c564b",   # aromatic woods — brown
    7: "#7f7f7f",   # astringent GI small — grey
    8: "#e377c2",   # TCM-imported — pink
    9: "#1f77b4",   # pepaya/wungu dyad — blue
    10: "#aec7e8",  # food grain — pale blue
}
BRIDGE_COLOR = "#222222"


def short_name(sn: str, max_len: int = 22) -> str:
    """Genus + species epithet, drop authority. Keep it readable."""
    parts = sn.split()
    if len(parts) >= 2:
        out = f"{parts[0]} {parts[1].rstrip('.,')}"
    else:
        out = sn
    return out if len(out) <= max_len else out[: max_len - 1] + "."


def draw_main_figure(
    G: nx.Graph,
    comm_assign: dict,
    bridges: set,
    roles: dict,
    forbidden: list,
    out_path: Path,
):
    pos = nx.spring_layout(G, k=0.45, iterations=200, seed=7, weight="weight")

    # Node visuals --------------------------------------------------------
    sizes = []
    colors = []
    edgecolors = []
    for n in G.nodes():
        formulas = roles.get(n, {}).get("total_formulas", 30)
        sizes.append(60 + 8 * (formulas ** 0.5))
        if n in bridges:
            colors.append(BRIDGE_COLOR)
            edgecolors.append("white")
        else:
            colors.append(COMMUNITY_COLORS.get(comm_assign.get(n, -1), "#cccccc"))
            edgecolors.append("white")

    # Edge visuals --------------------------------------------------------
    weights = [d["weight"] for _, _, d in G.edges(data=True)]
    wmax = max(weights) if weights else 1.0
    edge_alphas = [min(0.55, 0.08 + 0.5 * (w / wmax)) for w in weights]
    edge_widths = [0.4 + 1.5 * (w / wmax) for w in weights]

    fig, ax = plt.subplots(figsize=(15, 12))

    # 1) lift edges (background)
    for (u, v, d), a, w in zip(G.edges(data=True), edge_alphas, edge_widths):
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color="#666666",
            alpha=a,
            linewidth=w,
            zorder=1,
        )

    # 2) forbidden pairs overlay (only those whose both ends are present)
    forb_drawn = 0
    for pair in forbidden:
        h1, h2 = pair["herb1"], pair["herb2"]
        if h1 in pos and h2 in pos:
            ax.plot(
                [pos[h1][0], pos[h2][0]],
                [pos[h1][1], pos[h2][1]],
                color="#d62728",
                linestyle="--",
                linewidth=1.0,
                alpha=0.85,
                zorder=2,
            )
            forb_drawn += 1

    # 3) bridge singletons get a distinct diamond marker drawn on top
    bridge_xy = [(pos[n][0], pos[n][1], n) for n in G.nodes() if n in bridges]
    nonbridge_idx = [i for i, n in enumerate(G.nodes()) if n not in bridges]
    bridge_idx = [i for i, n in enumerate(G.nodes()) if n in bridges]

    nodes_list = list(G.nodes())
    # non-bridges as circles
    ax.scatter(
        [pos[nodes_list[i]][0] for i in nonbridge_idx],
        [pos[nodes_list[i]][1] for i in nonbridge_idx],
        s=[sizes[i] for i in nonbridge_idx],
        c=[colors[i] for i in nonbridge_idx],
        edgecolors="white",
        linewidths=0.8,
        zorder=3,
    )
    # bridges as diamonds, larger
    ax.scatter(
        [pos[nodes_list[i]][0] for i in bridge_idx],
        [pos[nodes_list[i]][1] for i in bridge_idx],
        s=[max(180, sizes[i] * 1.8) for i in bridge_idx],
        c=BRIDGE_COLOR,
        marker="D",
        edgecolors="white",
        linewidths=1.2,
        zorder=4,
    )

    # 4) labels — bridges always; otherwise top-N by formula count per community
    label_set = set(bridges)
    by_comm = defaultdict(list)
    for n in G.nodes():
        if n not in bridges:
            by_comm[comm_assign.get(n, -1)].append(
                (roles.get(n, {}).get("total_formulas", 0), n)
            )
    for ci, items in by_comm.items():
        items.sort(reverse=True)
        for _, n in items[:3]:  # top-3 per community
            label_set.add(n)

    for n in label_set:
        x, y = pos[n]
        weight = "bold" if n in bridges else "normal"
        col = BRIDGE_COLOR if n in bridges else "black"
        ax.text(
            x,
            y + 0.025,
            short_name(n),
            fontsize=7.5,
            ha="center",
            va="bottom",
            color=col,
            fontweight=weight,
            zorder=5,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7),
        )

    # 5) legend
    handles = []
    for ci in sorted(COMMUNITY_LABELS.keys()):
        handles.append(
            mpatches.Patch(
                color=COMMUNITY_COLORS[ci],
                label=f"S{ci} — {COMMUNITY_LABELS[ci]}",
            )
        )
    handles.append(
        Line2D(
            [0], [0],
            marker="D", color="w",
            markerfacecolor=BRIDGE_COLOR, markeredgecolor="white",
            markersize=10, label="Bridge singleton",
        )
    )
    handles.append(
        Line2D([0], [0], color="#d62728", linestyle="--", label="Forbidden pair"),
    )
    handles.append(
        Line2D([0], [0], color="#666666", alpha=0.5, linewidth=2, label="Lift > 1.5 co-occurrence"),
    )
    leg = ax.legend(
        handles=handles,
        loc="lower left",
        fontsize=8.5,
        frameon=True,
        framealpha=0.92,
        title="Mazhab (consensus-Louvain, 40 seeds, ARI 0.72)",
        title_fontsize=9,
    )
    leg.get_frame().set_edgecolor("#888888")

    ax.set_axis_off()
    ax.set_title(
        f"Jamu mazhab — {G.number_of_nodes()} herbs, {G.number_of_edges()} lift edges, "
        f"{forb_drawn} forbidden pairs (KG v08)",
        fontsize=12,
        pad=12,
    )

    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {out_path} ({forb_drawn} forbidden pairs drawn)")


def draw_small_multiples(
    G: nx.Graph,
    comm_assign: dict,
    bridges: set,
    roles: dict,
    out_path: Path,
):
    """One subplot per stable mazhab (size>=3). Shows internal lift-edges and
    the herbs themselves with full short-names. Helps a reader see the
    *internal grammar* of each school separately from the macro view."""
    by_comm = defaultdict(list)
    for n in G.nodes():
        if n in bridges:
            continue
        by_comm[comm_assign.get(n, -1)].append(n)

    plot_comms = sorted(
        [ci for ci, members in by_comm.items() if len(members) >= 3],
        key=lambda ci: -len(by_comm[ci]),
    )
    n_plots = len(plot_comms)
    cols = 3
    rows = (n_plots + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(15, 4.5 * rows))
    axes = axes.flatten()

    for ax, ci in zip(axes, plot_comms):
        members = by_comm[ci]
        sub = G.subgraph(members).copy()
        if sub.number_of_edges() == 0:
            sub_pos = nx.circular_layout(sub)
        else:
            sub_pos = nx.spring_layout(
                sub, k=0.7, iterations=120, seed=11, weight="weight"
            )

        # edges
        if sub.number_of_edges() > 0:
            ws = [d["weight"] for _, _, d in sub.edges(data=True)]
            wmax = max(ws)
            for (u, v, d) in sub.edges(data=True):
                ax.plot(
                    [sub_pos[u][0], sub_pos[v][0]],
                    [sub_pos[u][1], sub_pos[v][1]],
                    color="#666",
                    alpha=min(0.7, 0.15 + 0.55 * (d["weight"] / wmax)),
                    linewidth=0.6 + 1.6 * (d["weight"] / wmax),
                )

        # nodes
        sizes = [80 + 6 * (roles.get(node, {}).get("total_formulas", 30) ** 0.5)
                 for node in sub.nodes()]
        ax.scatter(
            [sub_pos[node][0] for node in sub.nodes()],
            [sub_pos[node][1] for node in sub.nodes()],
            s=sizes,
            c=COMMUNITY_COLORS.get(ci, "#cccccc"),
            edgecolors="white",
            linewidths=0.8,
            zorder=3,
        )
        for node in sub.nodes():
            x, y = sub_pos[node]
            ax.text(
                x, y + 0.05, short_name(node, 26),
                fontsize=7, ha="center", va="bottom",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75),
                zorder=5,
            )
        ax.set_title(f"S{ci} — {COMMUNITY_LABELS[ci]} ({len(members)} herbs, "
                     f"{sub.number_of_edges()} internal edges)", fontsize=10)
        ax.set_axis_off()

    for ax in axes[n_plots:]:
        ax.set_axis_off()

    plt.suptitle("Mazhab subnetworks — internal lift-edge structure",
                 fontsize=12, y=1.0)
    plt.tight_layout()
    plt.savefig(out_path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {out_path} ({n_plots} mazhab subplots)")


def main():
    base = Path(__file__).resolve().parent.parent.parent
    formulas_path = base / "data" / "raw" / "knapsack" / "knapsack_jamu_formulas.json"
    grammar_path = base / "data" / "kg" / "jamu_grammar.json"
    comm_path = base / "data" / "kg" / "jamu_herb_communities.json"
    figures_dir = base / "figures"
    figures_dir.mkdir(exist_ok=True)

    formulas = json.load(open(formulas_path, "r", encoding="utf-8"))
    grammar = json.load(open(grammar_path, "r", encoding="utf-8"))
    comm_data = json.load(open(comm_path, "r", encoding="utf-8"))
    print(f"Loaded {len(formulas)} formulas, "
          f"{len(grammar['herb_roles'])} roles, "
          f"{len(comm_data['communities'])} communities, "
          f"{len(comm_data['bridge_singletons'])} bridge singletons")

    herb_formulas = build_herb_index(formulas)
    G = build_lift_graph(
        herb_formulas,
        n_formulas=len(formulas),
        min_herb_freq=40,
        min_obs=5,
        lift_threshold=1.5,
    )
    print(f"Lift graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    comm_assign = comm_data["community_assignments"]
    bridges = set(comm_data["bridge_singletons"])

    # Add bridge singletons as nodes (they were dropped from clusters but live
    # in the lift graph as long as they have any edges; ensure presence).
    for b in bridges:
        if b not in G:
            G.add_node(b)

    draw_main_figure(
        G,
        comm_assign,
        bridges,
        grammar["herb_roles"],
        grammar["forbidden_combinations"],
        figures_dir / "21_mazhab_network.png",
    )
    draw_small_multiples(
        G,
        comm_assign,
        bridges,
        grammar["herb_roles"],
        figures_dir / "22_mazhab_small_multiples.png",
    )


if __name__ == "__main__":
    main()
