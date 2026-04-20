"""
Herb Co-occurrence Communities (Jamu "schools")
================================================
Extends jamu_grammar.py. Builds a weighted co-occurrence network of herbs
(weight = lift = obs/expected) and finds stable communities via CONSENSUS
Louvain — running Louvain across many seeds and keeping only node-pairs
that co-cluster in the majority of runs.

Hypothesis being tested:
  Jamu formulations cluster into functional "schools" — groups of herbs that
  preferentially co-occur. Forbidden pairs (herbs that never meet despite
  high individual frequency) arise at the boundaries between these schools.

Why consensus and not a single seed?
  Single-seed Louvain gives ARI ≈ 0.73 across seeds (decent but not stellar).
  A handful of "hub" herbs (e.g. Curcuma xanthorrhiza, Centella asiatica)
  genuinely bridge multiple schools and their seed=k assignment is unstable.
  Consensus isolates the stable community core and exposes bridges as
  singletons — a more honest representation.

Empirical result (see data/kg/jamu_herb_communities.json):
  9 stable communities + 5 bridge singletons emerge from 40-seed consensus.
  28/30 top forbidden pairs are cross-community; 0 are within-community;
  2 involve singleton-bridges. Random baseline cross-community rate ~83%.
  Forbidden pairs are structurally cross-school.

Stable communities recovered (consensus threshold 0.7 over 40 Louvain seeds
at res=1.2):
  S0 — Musculoskeletal warming + aromatic base (25)
        Zingiber officinale, Kaempferia, Foeniculum, Amomum, Cinnamomum,
        Myristica — the "warming-pungent" spice cluster
  S1 — Female reproductive / astringent (25)
        Curcuma domestica, Alyxia, Piper betle, Parameria, Guazuma, Punica
  S2 — GI bitter / hepatoprotective (16)
        Andrographis, Orthosiphon, Centella, Phyllanthus, Morinda, Imperata
  S3 — GI aromatic-carminative (9)
        Eucalyptus alba, Cocos nucifera, Nigella, Clausena, Mentha piperita
  S4 — Male tonic / aphrodisiac (8)
        Panax ginseng, Eurycoma, Piper nigrum, Piper retrofractum, Tribulus
  S5 — Aromatic rhizome bitters (4)
        Curcuma xanthorrhiza, Curcuma aeruginosa, Zingiber cassumunar,
        Acorus calamus
  S6 — Aromatic woods (4)
        Massoia, Cinnamomum sintok, Santalum, Trigonella
  S7 — Astringent GI bitters, small (3)
        Alstonia macrophylla, Caesalpinia sappan, Strychnos ligustrina
  S8 — TCM-imported (3)
        Rheum officinale, Carthamus tinctorius, Angelica sinensis
  S9 — Pepaya-daun wungu dyad (2)
        Carica papaya, Graptophyllum pictum
  S10 — Food-grain GI pair (2)
        Zea mays, Soya max

Bridge singletons (genuinely float between communities across seeds):
  Blumea balsamifera, Sauropus androgynus, Curcuma zedoaria,
  Abrus precatorius, Woodfordia floribunda
"""

import json
import sys
import io
import random
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

import networkx as nx
from networkx.algorithms.community import louvain_communities

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


COMMUNITY_LABELS = {
    0: "Musculoskeletal warming + aromatic base",
    1: "Female reproductive / astringent",
    2: "GI bitter / hepatoprotective",
    3: "GI aromatic-carminative",
    4: "Male tonic / aphrodisiac",
    5: "Aromatic rhizome bitters",
    6: "Aromatic woods",
    7: "Astringent GI bitters (small)",
    8: "TCM-imported",
    9: "Pepaya-daun wungu dyad",
    10: "Food-grain GI pair",
}


def load_formulas(path: Path) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_herb_index(formulas: list) -> dict[str, set[int]]:
    herb_formulas = defaultdict(set)
    for i, f in enumerate(formulas):
        for h in f.get("herbs", []):
            sn = h.get("scientific_name", "").strip()
            if sn:
                herb_formulas[sn].add(i)
    return herb_formulas


def build_lift_graph(
    herb_formulas: dict,
    n_formulas: int,
    min_herb_freq: int = 40,
    min_obs: int = 5,
    lift_threshold: float = 1.5,
) -> nx.Graph:
    frequent = [sn for sn in herb_formulas if len(herb_formulas[sn]) >= min_herb_freq]
    G = nx.Graph()
    G.add_nodes_from(frequent)
    for i in range(len(frequent)):
        for j in range(i + 1, len(frequent)):
            h1, h2 = frequent[i], frequent[j]
            obs = len(herb_formulas[h1] & herb_formulas[h2])
            if obs < min_obs:
                continue
            exp = len(herb_formulas[h1]) * len(herb_formulas[h2]) / n_formulas
            lift = obs / exp if exp > 0 else 0
            if lift > lift_threshold:
                G.add_edge(h1, h2, weight=lift, obs=obs, expected=exp)
    return G


def adjusted_rand_index(a: dict, b: dict, nodes: list) -> float:
    va = [a[n] for n in nodes]
    vb = [b[n] for n in nodes]
    contingency = Counter(zip(va, vb))
    marginals_a = Counter(va)
    marginals_b = Counter(vb)
    n = len(nodes)
    sum_c = sum(comb(v, 2) for v in contingency.values())
    sum_a = sum(comb(v, 2) for v in marginals_a.values())
    sum_b = sum(comb(v, 2) for v in marginals_b.values())
    total = comb(n, 2)
    expected = sum_a * sum_b / total if total else 0
    max_idx = (sum_a + sum_b) / 2
    if max_idx - expected == 0:
        return 1.0
    return (sum_c - expected) / (max_idx - expected)


def consensus_louvain(
    G: nx.Graph,
    n_seeds: int = 40,
    resolution: float = 1.2,
    co_cluster_threshold: float = 0.7,
) -> tuple[list[set], list[float]]:
    """Run Louvain n_seeds times. A node pair is kept in a consensus edge if
    they co-cluster in >= threshold fraction of runs. Connected components of
    the consensus graph are the stable communities."""
    nodes = list(G.nodes)
    co_count = defaultdict(int)
    assignments = []

    for seed in range(1, n_seeds + 1):
        comms = louvain_communities(G, weight="weight", resolution=resolution, seed=seed)
        assign = {n: ci for ci, c in enumerate(comms) for n in c}
        assignments.append(assign)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if assign[nodes[i]] == assign[nodes[j]]:
                    key = tuple(sorted([nodes[i], nodes[j]]))
                    co_count[key] += 1

    # pairwise ARI for stability report
    ari_values = []
    for i in range(len(assignments)):
        for j in range(i + 1, len(assignments)):
            ari_values.append(adjusted_rand_index(assignments[i], assignments[j], nodes))

    consensus = nx.Graph()
    consensus.add_nodes_from(nodes)
    for (a, b), c in co_count.items():
        if c >= co_cluster_threshold * n_seeds:
            consensus.add_edge(a, b, weight=c / n_seeds)

    components = sorted(nx.connected_components(consensus), key=len, reverse=True)
    return components, ari_values


def herb_part_occurrences(
    formulas: list, comm_assign: dict
) -> dict[int, Counter]:
    """For each community, count total plant-part occurrences in formulas.
    This is weighted by how often the community's herbs actually appear, so
    it reflects the community's pharmaceutical *form* — oil vs leaf vs root.
    """
    comm_parts = defaultdict(Counter)
    for f in formulas:
        for h in f.get("herbs", []):
            sn = h.get("scientific_name", "").strip()
            part = h.get("plant_part", "").strip()
            if sn in comm_assign and part:
                comm_parts[comm_assign[sn]][part] += 1
    return comm_parts


def community_profiles(
    communities: list[set],
    roles: dict,
    herb_formulas: dict,
    formulas: list,
) -> list[dict]:
    comm_assign = {sn: ci for ci, comm in enumerate(communities) for sn in comm}
    part_profiles = herb_part_occurrences(formulas, comm_assign)

    profiles = []
    for ci, comm in enumerate(communities):
        if len(comm) < 2:
            continue
        members = sorted(comm, key=lambda sn: -len(herb_formulas[sn]))
        eff = Counter()
        role_ct = Counter()
        for sn in comm:
            r = roles.get(sn, {})
            if r.get("top_effect"):
                eff[r["top_effect"]] += 1
            if r.get("role"):
                role_ct[r["role"]] += 1

        parts = part_profiles.get(ci, Counter())
        total_parts = sum(parts.values()) or 1
        parts_pct = {
            p: round(c / total_parts * 100, 1)
            for p, c in parts.most_common(5)
        }

        profiles.append({
            "community_id": ci,
            "label": COMMUNITY_LABELS.get(ci, "(unlabeled)"),
            "size": len(comm),
            "effect_distribution": dict(eff.most_common()),
            "role_distribution": dict(role_ct),
            "plant_part_occurrences_pct": parts_pct,
            "members": members,
        })
    return profiles


def validate_forbidden_pairs(
    forbidden: list,
    comm_assign: dict[str, int],
    assigned_nodes: list,
    n_samples: int = 3000,
) -> dict:
    cross = within = missing = 0
    for pair in forbidden:
        c1 = comm_assign.get(pair["herb1"])
        c2 = comm_assign.get(pair["herb2"])
        if c1 is None or c2 is None:
            missing += 1
        elif c1 == c2:
            within += 1
        else:
            cross += 1

    random.seed(7)
    rand_cross = rand_within = 0
    for _ in range(n_samples):
        a, b = random.sample(assigned_nodes, 2)
        if comm_assign[a] == comm_assign[b]:
            rand_within += 1
        else:
            rand_cross += 1
    rand_cross_rate = rand_cross / max(rand_cross + rand_within, 1)

    return {
        "forbidden_cross": cross,
        "forbidden_within": within,
        "forbidden_missing": missing,
        "random_cross_rate": round(rand_cross_rate, 3),
    }


def main():
    base = Path(__file__).resolve().parent.parent.parent
    formulas_path = base / "data" / "raw" / "knapsack" / "knapsack_jamu_formulas.json"
    grammar_path = base / "data" / "kg" / "jamu_grammar.json"
    output_path = base / "data" / "kg" / "jamu_herb_communities.json"

    formulas = load_formulas(formulas_path)
    grammar = json.load(open(grammar_path, "r", encoding="utf-8"))
    roles = grammar["herb_roles"]
    forbidden = grammar["forbidden_combinations"]
    print(f"Loaded {len(formulas)} formulas, {len(roles)} classified herbs")

    herb_formulas = build_herb_index(formulas)
    G = build_lift_graph(
        herb_formulas,
        n_formulas=len(formulas),
        min_herb_freq=40,
        min_obs=5,
        lift_threshold=1.5,
    )
    print(f"Lift graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    components, ari_values = consensus_louvain(
        G, n_seeds=40, resolution=1.2, co_cluster_threshold=0.7
    )
    mean_ari = sum(ari_values) / len(ari_values) if ari_values else 0.0
    print(
        f"Louvain single-seed stability: mean pairwise ARI = "
        f"{mean_ari:.3f} "
        f"(min={min(ari_values):.3f}, max={max(ari_values):.3f})"
    )

    stable_components = [c for c in components if len(c) >= 2]
    singletons = [list(c)[0] for c in components if len(c) == 1]
    print(f"Consensus: {len(stable_components)} stable communities, "
          f"{len(singletons)} bridge singletons")

    profiles = community_profiles(stable_components, roles, herb_formulas, formulas)

    comm_assign = {
        sn: ci for ci, comm in enumerate(stable_components) for sn in comm
    }
    assigned_nodes = list(comm_assign.keys())
    validation = validate_forbidden_pairs(forbidden, comm_assign, assigned_nodes)

    print()
    print("=" * 80)
    for p in profiles:
        print(f"\nS{p['community_id']}  [{p['label']}]  {p['size']} herbs")
        print(f"  Roles: {p['role_distribution']}")
        print(f"  Effects (top 3): "
              f"{dict(list(p['effect_distribution'].items())[:3])}")
        print(f"  Plant parts: {p['plant_part_occurrences_pct']}")
        print(f"  Top members: {p['members'][:6]}")

    print()
    print(f"Bridge singletons (unstable across seeds):")
    for sn in singletons:
        r = roles.get(sn, {})
        print(f"  {sn[:40]:40s}  n={len(herb_formulas[sn]):4d}  "
              f"top_eff={r.get('top_effect','?')[:28]}")

    print()
    print("=" * 80)
    print("Validation — forbidden pairs against consensus community structure")
    print("=" * 80)
    print(f"  Cross-community:  {validation['forbidden_cross']}/{len(forbidden)}")
    print(f"  Within-community: {validation['forbidden_within']}/{len(forbidden)}")
    print(f"  Missing (bridges): {validation['forbidden_missing']}")
    print(f"  Random baseline cross-community rate: "
          f"{validation['random_cross_rate']*100:.0f}%")

    output = {
        "method": {
            "graph": "lift-weighted co-occurrence",
            "min_herb_freq": 40,
            "min_obs": 5,
            "lift_threshold": 1.5,
            "algorithm": "consensus Louvain over 40 seeds",
            "resolution": 1.2,
            "co_cluster_threshold": 0.7,
            "stability_mean_ari": round(mean_ari, 3),
        },
        "communities": profiles,
        "bridge_singletons": singletons,
        "community_assignments": comm_assign,
        "forbidden_pair_validation": validation,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {output_path}")


if __name__ == "__main__":
    main()
