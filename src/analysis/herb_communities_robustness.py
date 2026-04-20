"""
Robustness Tests for Jamu Herb Community Analysis
===================================================
Two methodological defenses for the forbidden-pair / community findings:

  Test 1: NULL MODEL — degree-preserving bipartite edge swap.
      Tests whether forbidden pairs (herbs with zero co-occurrence despite
      high individual frequency) could arise by chance given observed
      herb frequencies and formula sizes.

      Result: observed 107 forbidden pairs among 1,653 pairs of frequent
      herbs (freq ≥ 100). Null distribution (100 samples, thorough swap
      mixing): mean 7.15, sd 2.63, max 13. Z-score 37.97. p < 0.01
      (empirically; parametric p essentially zero under normal approximation).

      Conclusion: forbidden pairs are a real structural phenomenon, not a
      chance consequence of individual herb rarity or formula-size structure.

  Test 2: PARAMETER SWEEP — does the cross-community property of forbidden
      pairs depend on our specific choices of min_herb_freq, lift_threshold,
      and Louvain resolution?

      Result: across 60 configurations (freq ∈ {30,40,50,60,80}, lift ∈
      {1.3,1.5,1.7,2.0}, resolution ∈ {1.0,1.2,1.4}), forbidden-pair
      cross-community rate: mean 99.5%, min 97%, max 100%. ARI vs canonical
      partition (freq=40, lift=1.5, res=1.2) averages 0.64.

      Conclusion: communities themselves shift modestly with parameters,
      but the forbidden-pair = boundary property is essentially invariant.
      The finding does not depend on arbitrary threshold choices.

Save output to data/kg/jamu_robustness.json for reference.
"""

import json
import sys
import io
import random
import time
from collections import defaultdict, Counter
from itertools import combinations
from math import comb
from pathlib import Path

import networkx as nx
from networkx.algorithms.community import louvain_communities

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# =====================================================================
# Test 1: degree-preserving null model
# =====================================================================

def null_model_test(
    formulas: list,
    forbidden_list: list,
    min_freq_for_forbidden: int = 100,
    n_samples: int = 100,
    swaps_per_edge: int = 5,
    burn_in_multiplier: int = 10,
    seed: int = 42,
) -> dict:
    """Degree-preserving bipartite rewiring (Curveball-style). Swaps edges
    (f1,h1),(f2,h2) → (f1,h2),(f2,h1) when non-duplicating. Converges to
    uniform over bipartite graphs with same row/col degree sequence."""
    random.seed(seed)

    edges = []
    for i, f in enumerate(formulas):
        seen = set()
        for h in f.get("herbs", []):
            sn = h.get("scientific_name", "").strip()
            if sn and sn not in seen:
                edges.append((i, sn))
                seen.add(sn)

    formula_herbs = defaultdict(set)
    herb_formulas = defaultdict(set)
    for fi, h in edges:
        formula_herbs[fi].add(h)
        herb_formulas[h].add(fi)

    frequent = sorted(
        h for h in herb_formulas if len(herb_formulas[h]) >= min_freq_for_forbidden
    )
    all_pairs = list(combinations(frequent, 2))

    def count_forbidden(hf):
        return sum(1 for h1, h2 in all_pairs if len(hf[h1] & hf[h2]) == 0)

    observed = count_forbidden(herb_formulas)

    n_edges = len(edges)
    swap_count = n_edges * swaps_per_edge

    def do_swaps(n):
        accepted = 0
        for _ in range(n):
            i = random.randrange(n_edges)
            j = random.randrange(n_edges)
            if i == j:
                continue
            f1, h1 = edges[i]
            f2, h2 = edges[j]
            if f1 == f2 or h1 == h2:
                continue
            if h2 in formula_herbs[f1] or h1 in formula_herbs[f2]:
                continue
            formula_herbs[f1].remove(h1); formula_herbs[f1].add(h2)
            formula_herbs[f2].remove(h2); formula_herbs[f2].add(h1)
            herb_formulas[h1].remove(f1); herb_formulas[h1].add(f2)
            herb_formulas[h2].remove(f2); herb_formulas[h2].add(f1)
            edges[i] = (f1, h2)
            edges[j] = (f2, h1)
            accepted += 1
        return accepted

    t0 = time.time()
    do_swaps(n_edges * burn_in_multiplier)
    samples = []
    for _ in range(n_samples):
        do_swaps(swap_count)
        samples.append(count_forbidden(herb_formulas))

    mean = sum(samples) / len(samples)
    var = sum((x - mean) ** 2 for x in samples) / max(len(samples) - 1, 1)
    sd = var ** 0.5
    z_score = (observed - mean) / sd if sd > 0 else float("inf")
    p_ge = sum(1 for x in samples if x >= observed) / len(samples)

    return {
        "observed_forbidden_pairs": observed,
        "n_frequent_herbs": len(frequent),
        "n_pairs_tested": len(all_pairs),
        "null_mean": round(mean, 3),
        "null_std": round(sd, 3),
        "null_min": min(samples),
        "null_max": max(samples),
        "null_samples": samples,
        "z_score": round(z_score, 2),
        "p_ge_observed": p_ge,
        "n_samples": n_samples,
        "swaps_per_sample": swap_count,
        "burn_in_swaps": n_edges * burn_in_multiplier,
        "elapsed_sec": round(time.time() - t0, 1),
    }


# =====================================================================
# Test 2: community parameter sweep
# =====================================================================

def adjusted_rand_index(a1: dict, a2: dict, nodes: list) -> float:
    va = [a1[n] for n in nodes]
    vb = [a2[n] for n in nodes]
    cont = Counter(zip(va, vb))
    ma = Counter(va)
    mb = Counter(vb)
    n = len(nodes)
    sc = sum(comb(v, 2) for v in cont.values())
    sa = sum(comb(v, 2) for v in ma.values())
    sb = sum(comb(v, 2) for v in mb.values())
    tot = comb(n, 2)
    if tot == 0:
        return 1.0
    expected = sa * sb / tot
    mx = (sa + sb) / 2
    if mx == expected:
        return 1.0
    return (sc - expected) / (mx - expected)


def parameter_sweep(
    formulas: list,
    forbidden_list: list,
    canonical_assign: dict,
    min_freqs: list = (30, 40, 50, 60, 80),
    lift_thresholds: list = (1.3, 1.5, 1.7, 2.0),
    resolutions: list = (1.0, 1.2, 1.4),
    min_obs: int = 5,
    seed: int = 1,
) -> list:
    herb_formulas = defaultdict(set)
    for i, f in enumerate(formulas):
        for h in f.get("herbs", []):
            sn = h.get("scientific_name", "").strip()
            if sn:
                herb_formulas[sn].add(i)
    N = len(formulas)

    def build_graph(min_freq, lift_threshold):
        freq_herbs = [sn for sn in herb_formulas if len(herb_formulas[sn]) >= min_freq]
        G = nx.Graph()
        G.add_nodes_from(freq_herbs)
        for i in range(len(freq_herbs)):
            for j in range(i + 1, len(freq_herbs)):
                h1, h2 = freq_herbs[i], freq_herbs[j]
                obs = len(herb_formulas[h1] & herb_formulas[h2])
                if obs < min_obs:
                    continue
                exp = len(herb_formulas[h1]) * len(herb_formulas[h2]) / N
                lift = obs / exp if exp > 0 else 0
                if lift > lift_threshold:
                    G.add_edge(h1, h2, weight=lift)
        return G

    results = []
    for freq in min_freqs:
        for lift in lift_thresholds:
            for res in resolutions:
                G = build_graph(freq, lift)
                if G.number_of_nodes() < 10:
                    continue
                comms = louvain_communities(
                    G, weight="weight", resolution=res, seed=seed
                )
                assign = {n: ci for ci, c in enumerate(comms) for n in c}

                common = [n for n in canonical_assign if n in assign]
                ari = (
                    adjusted_rand_index(canonical_assign, assign, common)
                    if common else 0.0
                )

                cross = within = missing = 0
                for pair in forbidden_list:
                    c1 = assign.get(pair["herb1"])
                    c2 = assign.get(pair["herb2"])
                    if c1 is None or c2 is None:
                        missing += 1
                    elif c1 == c2:
                        within += 1
                    else:
                        cross += 1

                total = cross + within
                cross_rate = cross / total if total else 0.0
                results.append({
                    "min_freq": freq,
                    "lift_threshold": lift,
                    "resolution": res,
                    "nodes": G.number_of_nodes(),
                    "edges": G.number_of_edges(),
                    "n_communities": len(comms),
                    "largest_community": max((len(c) for c in comms), default=0),
                    "ari_vs_canonical": round(ari, 3),
                    "forbidden_cross": cross,
                    "forbidden_within": within,
                    "forbidden_missing": missing,
                    "cross_rate": round(cross_rate, 3),
                })
    return results


def main():
    base = Path(__file__).resolve().parent.parent.parent
    formulas_path = base / "data" / "raw" / "knapsack" / "knapsack_jamu_formulas.json"
    grammar_path = base / "data" / "kg" / "jamu_grammar.json"
    comms_path = base / "data" / "kg" / "jamu_herb_communities.json"
    output_path = base / "data" / "kg" / "jamu_robustness.json"

    formulas = json.load(open(formulas_path, "r", encoding="utf-8"))
    grammar = json.load(open(grammar_path, "r", encoding="utf-8"))
    forbidden_list = grammar["forbidden_combinations"]
    canonical = json.load(open(comms_path, "r", encoding="utf-8"))
    canonical_assign = canonical["community_assignments"]

    print("=" * 70)
    print("Test 1: Degree-preserving null model for forbidden pairs")
    print("=" * 70)
    null_result = null_model_test(
        formulas, forbidden_list, min_freq_for_forbidden=100, n_samples=100
    )
    print(f"  Observed forbidden pairs: {null_result['observed_forbidden_pairs']} "
          f"(among {null_result['n_pairs_tested']} pairs of "
          f"{null_result['n_frequent_herbs']} frequent herbs)")
    print(f"  Null mean: {null_result['null_mean']} "
          f"(sd {null_result['null_std']}, "
          f"range [{null_result['null_min']}, {null_result['null_max']}])")
    print(f"  Z-score: {null_result['z_score']}")
    print(f"  Empirical p(null >= observed): {null_result['p_ge_observed']}")

    print()
    print("=" * 70)
    print("Test 2: Parameter sweep for community detection")
    print("=" * 70)
    sweep = parameter_sweep(formulas, forbidden_list, canonical_assign)
    rates = [r["cross_rate"] for r in sweep]
    aris = [r["ari_vs_canonical"] for r in sweep]
    print(f"  Configurations tested: {len(sweep)}")
    print(f"  Forbidden-pair cross-community rate: "
          f"mean={sum(rates)/len(rates)*100:.1f}%, "
          f"min={min(rates)*100:.0f}%, max={max(rates)*100:.0f}%")
    print(f"  ARI vs canonical: "
          f"mean={sum(aris)/len(aris):.3f}, "
          f"min={min(aris):.3f}, max={max(aris):.3f}")
    n_100 = sum(1 for r in rates if r >= 0.99)
    print(f"  Configs with cross-rate ≥99%: {n_100}/{len(sweep)}")

    output = {
        "null_model_test": null_result,
        "parameter_sweep": {
            "configurations": sweep,
            "summary": {
                "n_configs": len(sweep),
                "cross_rate_mean": round(sum(rates) / len(rates), 3),
                "cross_rate_min": min(rates),
                "cross_rate_max": max(rates),
                "ari_mean": round(sum(aris) / len(aris), 3),
                "ari_min": min(aris),
                "ari_max": max(aris),
                "n_configs_cross_rate_above_99pct": n_100,
            },
        },
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved → {output_path}")


if __name__ == "__main__":
    main()
