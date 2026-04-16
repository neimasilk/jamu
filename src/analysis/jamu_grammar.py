"""
Jamu Formulation Grammar Analysis
===================================
Investigating the compositional logic of jamu formulations.

Hypothesis: Jamu formulations follow an implicit "grammar" analogous
to TCM's Jun-Chen-Zuo-Shi (君臣佐使) system:
  - Jun (君 King): primary therapeutic herb
  - Chen (臣 Minister): supporting/enhancing herb
  - Zuo (佐 Assistant): moderating side effects or adding secondary effects
  - Shi (使 Guide/Courier): bioavailability enhancer or harmonizer

We test this by examining:
  1. Role classification based on solo vs. combination patterns
  2. Hub structure in the co-occurrence network
  3. Forbidden combinations (herbs that NEVER co-occur)
  4. Effect-specific subnetworks
"""

import json
import sys
import io
from collections import Counter, defaultdict
from pathlib import Path
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def load_formulas(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_herb_names(formula: dict) -> list[str]:
    """Get clean herb scientific names from a formula."""
    return [h.get("scientific_name", "").strip()
            for h in formula.get("herbs", [])
            if h.get("scientific_name", "").strip()]


def classify_herb_roles(formulas: list, min_freq: int = 20) -> dict:
    """
    Classify herbs into functional roles based on their behavior patterns.

    Metrics used:
    - solo_ratio: how often herb appears alone (high = standalone agent)
    - specificity: concentration in one effect group (high = specialist)
    - mean_position: average position in formula ingredient lists
    - partner_diversity: how many different herbs it combines with
    """
    herb_solo = Counter()
    herb_multi = Counter()
    herb_total = Counter()
    herb_effects = defaultdict(Counter)
    herb_partners = defaultdict(set)
    herb_positions = defaultdict(list)

    for f in formulas:
        herbs = extract_herb_names(f)
        eg = f.get("jamu_effect_group", "").strip()

        if len(herbs) == 1:
            herb_solo[herbs[0]] += 1
        for i, h in enumerate(herbs):
            herb_total[h] += 1
            if len(herbs) > 1:
                herb_multi[h] += 1
                herb_positions[h].append(i / max(len(herbs) - 1, 1))
                for other in herbs:
                    if other != h:
                        herb_partners[h].add(other)
            if eg and eg != "-":
                herb_effects[h][eg] += 1

    # Classify
    roles = {}
    for herb, total in herb_total.items():
        if total < min_freq:
            continue

        solo = herb_solo.get(herb, 0)
        solo_ratio = solo / total

        # Specificity: max fraction in any one effect group
        effects = herb_effects.get(herb, Counter())
        effect_total = sum(effects.values())
        specificity = max(effects.values()) / max(effect_total, 1) if effects else 0

        # Partner diversity
        n_partners = len(herb_partners.get(herb, set()))

        # Mean position in ingredient list
        positions = herb_positions.get(herb, [])
        mean_pos = sum(positions) / len(positions) if positions else 0.5

        # Role classification
        if solo_ratio > 0.15:
            role = "raja"  # King: often used standalone → primary therapeutic agent
        elif specificity > 0.6 and n_partners < 200:
            role = "menteri"  # Minister: specialist in specific effect group
        elif n_partners > 300 and solo_ratio < 0.02:
            role = "kurir"  # Courier: appears in many combinations, rarely alone
        elif solo_ratio < 0.02 and specificity < 0.4:
            role = "penyeimbang"  # Harmonizer: broad-spectrum supporting role
        else:
            role = "umum"  # General: no strong pattern

        roles[herb] = {
            "role": role,
            "total_formulas": total,
            "solo_count": solo,
            "solo_ratio": round(solo_ratio, 3),
            "specificity": round(specificity, 3),
            "top_effect": effects.most_common(1)[0][0] if effects else "",
            "n_partners": n_partners,
            "mean_position": round(mean_pos, 3),
        }

    return roles


def find_forbidden_combinations(formulas: list, min_freq: int = 100) -> list:
    """
    Find herb pairs that appear frequently individually but NEVER together.
    These may represent traditional knowledge of negative interactions.
    """
    herb_sets = defaultdict(set)
    for i, f in enumerate(formulas):
        for h in extract_herb_names(f):
            herb_sets[h].add(i)

    # Only consider frequent herbs
    frequent = {h for h, s in herb_sets.items() if len(s) >= min_freq}

    forbidden = []
    for h1, h2 in combinations(sorted(frequent), 2):
        overlap = len(herb_sets[h1] & herb_sets[h2])
        if overlap == 0:
            forbidden.append({
                "herb1": h1,
                "herb2": h2,
                "freq1": len(herb_sets[h1]),
                "freq2": len(herb_sets[h2]),
                "expected_overlap": len(herb_sets[h1]) * len(herb_sets[h2]) / len(formulas),
            })

    forbidden.sort(key=lambda x: -x["expected_overlap"])
    return forbidden


def analyze_effect_subnetworks(formulas: list) -> dict:
    """
    For each effect group, what is the characteristic herb combination?
    Are there "signature" herbs for each therapeutic area?
    """
    subnetworks = {}

    for eg_name in ["Gastrointestinal disorders",
                    "Musculoskeletal and connective tissue disorders",
                    "Female reproductive organ problems",
                    "Pain/inflammation",
                    "Respiratory disease",
                    "Wounds and skin infections",
                    "Urinary related problems",
                    "Disorders of appetite"]:
        eg_formulas = [f for f in formulas
                       if f.get("jamu_effect_group", "").strip() == eg_name]
        if len(eg_formulas) < 10:
            continue

        herb_freq = Counter()
        pair_freq = Counter()
        for f in eg_formulas:
            herbs = extract_herb_names(f)
            for h in herbs:
                herb_freq[h] += 1
            for h1, h2 in combinations(sorted(set(herbs)), 2):
                pair_freq[(h1, h2)] += 1

        # Signature herbs: appear in >20% of formulas for this effect
        threshold = len(eg_formulas) * 0.20
        signature = [(h, c, c/len(eg_formulas)*100)
                     for h, c in herb_freq.most_common(20)
                     if c >= threshold]

        # Characteristic pairs
        char_pairs = [(p, c) for p, c in pair_freq.most_common(10)]

        subnetworks[eg_name] = {
            "n_formulas": len(eg_formulas),
            "mean_herbs": sum(len(extract_herb_names(f)) for f in eg_formulas) / len(eg_formulas),
            "signature_herbs": [{"herb": h, "count": c, "pct": round(p, 1)}
                               for h, c, p in signature],
            "top_pairs": [{"pair": list(p), "count": c} for p, c in char_pairs],
        }

    return subnetworks


def main():
    base_dir = Path(__file__).parent.parent.parent
    formulas_path = base_dir / "data" / "raw" / "knapsack" / "knapsack_jamu_formulas.json"
    formulas = load_formulas(str(formulas_path))
    print(f"Loaded {len(formulas)} formulas")
    print()

    # 1. Herb role classification
    print("=" * 70)
    print("KLASIFIKASI PERAN HERBAL (Jun-Chen-Zuo-Shi Nusantara)")
    print("=" * 70)

    roles = classify_herb_roles(formulas, min_freq=50)

    role_groups = defaultdict(list)
    for herb, data in roles.items():
        role_groups[data["role"]].append((herb, data))

    role_descriptions = {
        "raja": "RAJA (King) — Agen terapeutik utama, sering digunakan sendiri",
        "menteri": "MENTERI (Minister) — Spesialis di area terapeutik tertentu",
        "kurir": "KURIR (Courier) — Bioenhancer/harmonizer, tidak pernah sendiri",
        "penyeimbang": "PENYEIMBANG (Harmonizer) — Pendukung spektrum luas",
        "umum": "UMUM (General) — Tidak ada pola dominan",
    }

    for role_name in ["raja", "menteri", "kurir", "penyeimbang", "umum"]:
        herbs = role_groups.get(role_name, [])
        herbs.sort(key=lambda x: -x[1]["total_formulas"])
        print(f"\n--- {role_descriptions[role_name]} ({len(herbs)} herbs) ---")
        for herb, data in herbs[:8]:
            parts = herb.split()
            short = f"{parts[0]} {parts[1]}" if len(parts) >= 2 else herb[:25]
            print(f"  {short:30s} | {data['total_formulas']:5d}x | "
                  f"solo {data['solo_ratio']*100:4.1f}% | "
                  f"spec {data['specificity']*100:4.0f}% → {data['top_effect'][:25]:25s} | "
                  f"{data['n_partners']:3d} partners")

    # 2. Forbidden combinations
    print()
    print("=" * 70)
    print("KOMBINASI TERLARANG (herbs yang TIDAK PERNAH muncul bersama)")
    print("=" * 70)

    forbidden = find_forbidden_combinations(formulas, min_freq=100)
    if forbidden:
        print(f"\nFound {len(forbidden)} forbidden pairs among herbs with freq ≥ 100:")
        for pair in forbidden[:15]:
            parts1 = pair["herb1"].split()
            parts2 = pair["herb2"].split()
            s1 = f"{parts1[0]} {parts1[1]}" if len(parts1) >= 2 else pair["herb1"]
            s2 = f"{parts2[0]} {parts2[1]}" if len(parts2) >= 2 else pair["herb2"]
            print(f"  {s1:30s} × {s2:30s} | "
                  f"freq {pair['freq1']:4d} + {pair['freq2']:4d} | "
                  f"expected overlap: {pair['expected_overlap']:.1f}")
    else:
        print("  No forbidden pairs found (all frequent herbs co-occur at least once)")

    # 3. Effect-specific subnetworks
    print()
    print("=" * 70)
    print("SIGNATURE HERBS PER AREA TERAPEUTIK")
    print("=" * 70)

    subnetworks = analyze_effect_subnetworks(formulas)
    for eg_name, data in subnetworks.items():
        print(f"\n--- {eg_name} ({data['n_formulas']} formulas, "
              f"mean {data['mean_herbs']:.1f} herbs) ---")
        print("  Signature herbs (>20% of formulas):")
        for sh in data["signature_herbs"]:
            parts = sh["herb"].split()
            short = f"{parts[0]} {parts[1]}" if len(parts) >= 2 else sh["herb"][:25]
            print(f"    {short:30s}: {sh['pct']:5.1f}% ({sh['count']} formulas)")
        if data["top_pairs"]:
            print("  Top pairs:")
            for tp in data["top_pairs"][:3]:
                p1, p2 = tp["pair"]
                s1 = p1.split()[0] + " " + p1.split()[1] if len(p1.split()) >= 2 else p1
                s2 = p2.split()[0] + " " + p2.split()[1] if len(p2.split()) >= 2 else p2
                print(f"    {s1:25s} + {s2:25s}: {tp['count']}")

    # Save results
    output = {
        "herb_roles": {h: d for h, d in roles.items()},
        "forbidden_combinations": forbidden[:30],
        "effect_subnetworks": subnetworks,
    }
    output_path = base_dir / "data" / "kg" / "jamu_grammar.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()
