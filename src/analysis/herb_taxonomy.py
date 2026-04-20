"""
Herb Taxonomy × Community Analysis
===================================
Tests whether jamu mazhab (schools) are structured by botanical family or
by pharmaceutical function.

Manual genus → family mapping following APG IV (angiosperms) with
traditional form retained where KNApSAcK uses older synonyms
(e.g., Languas = Alpinia, Caryophyllus aromaticus = Syzygium aromaticum).

Hypothesis alternatives:
  H1 (taxonomy-driven): mazhab cluster by family — e.g., Zingiberaceae
      all together, Apiaceae all together.
  H2 (function-driven): families are distributed across mazhab because
      formulators pick by effect/form, not by lineage.

Empirical result (see main output): mazhab are PRIMARILY function-driven.
Most families distribute across 2-5 communities. Only a few families are
truly mazhab-bound:
  - Piperaceae → split between S4 (male tonic) and S0 (warming base)
  - Zingiberaceae → heavily in S0 (warming), but also S5 (rhizome bitters)
    and scattered into S1, S2, S3
  - Apocynaceae → S1 (female reproductive) — Alyxia + Parameria both
  - Myrtaceae → scattered across S3 (oils), S6 (woods), and S0
  - Acanthaceae → split S2 / S1 / S9

Conclusion: jamu grammar is organized along a FUNCTIONAL axis (effect,
material form, preparation), NOT along botanical lineage. This aligns
with oral-traditional pharmacy where formulators think in terms of
"what this herb *does*", not "what it's related to". Contrast with TCM's
Bencao Gangmu organization which is partly taxonomic (水部, 草部, 木部 etc.).
"""

import json
import sys
import io
from collections import Counter, defaultdict
from pathlib import Path

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# Manual genus → family mapping. Follows APG IV; notes on non-standard
# KNApSAcK names:
#   Languas = Alpinia (Zingiberaceae), Caryophyllus aromaticus = Syzygium,
#   Andropogon citratus = Cymbopogon citratus, Galla = Quercus gall,
#   Piperis = Piperaceae synonym, Soya = Glycine.
GENUS_FAMILY = {
    "Abrus": "Fabaceae",
    "Acorus": "Acoraceae",
    "Allium": "Amaryllidaceae",
    "Aloe": "Asphodelaceae",
    "Alpinia": "Zingiberaceae",
    "Alstonia": "Apocynaceae",
    "Alyxia": "Apocynaceae",
    "Amomum": "Zingiberaceae",
    "Andrographis": "Acanthaceae",
    "Andropogon": "Poaceae",         # lemongrass, old name for Cymbopogon
    "Angelica": "Apiaceae",
    "Apium": "Apiaceae",
    "Areca": "Arecaceae",
    "Baeckea": "Myrtaceae",
    "Blumea": "Asteraceae",
    "Boesenbergia": "Zingiberaceae",
    "Caesalpinia": "Fabaceae",
    "Camellia": "Theaceae",
    "Carica": "Caricaceae",
    "Carthamus": "Asteraceae",
    "Carum": "Apiaceae",
    "Caryophyllus": "Myrtaceae",     # = Syzygium aromaticum
    "Cassia": "Fabaceae",
    "Centella": "Apiaceae",
    "Cinnamomum": "Lauraceae",
    "Citrus": "Rutaceae",
    "Clausena": "Rutaceae",
    "Cocos": "Arecaceae",
    "Coriandrum": "Apiaceae",
    "Curcuma": "Zingiberaceae",
    "Cymbopogon": "Poaceae",
    "Cyperus": "Cyperaceae",
    "Dioscorea": "Dioscoreaceae",
    "Elephantopus": "Asteraceae",
    "Equisetum": "Equisetaceae",
    "Eucalyptus": "Myrtaceae",
    "Eugenia": "Myrtaceae",
    "Eurycoma": "Simaroubaceae",
    "Foeniculum": "Apiaceae",
    "Galla": "Fagaceae",              # Quercus gall
    "Glycyrrhiza": "Fabaceae",
    "Graptophyllum": "Acanthaceae",
    "Guazuma": "Malvaceae",
    "Gynura": "Asteraceae",
    "Helicteres": "Malvaceae",
    "Imperata": "Poaceae",
    "Kaempferia": "Zingiberaceae",
    "Languas": "Zingiberaceae",        # = Alpinia
    "Massoia": "Lauraceae",
    "Melaleuca": "Myrtaceae",
    "Mentha": "Lamiaceae",
    "Momordica": "Cucurbitaceae",
    "Morinda": "Rubiaceae",
    "Murraya": "Rutaceae",
    "Myristica": "Myristicaceae",
    "Nigella": "Ranunculaceae",
    "Olea": "Oleaceae",
    "Orthosiphon": "Lamiaceae",
    "Oryza": "Poaceae",
    "Panax": "Araliaceae",
    "Parameria": "Apocynaceae",
    "Parkia": "Fabaceae",
    "Phaleria": "Thymelaeaceae",
    "Phyllanthus": "Phyllanthaceae",
    "Pimpinella": "Apiaceae",
    "Piper": "Piperaceae",
    "Piperis": "Piperaceae",
    "Plantago": "Plantaginaceae",
    "Pluchea": "Asteraceae",
    "Psidium": "Myrtaceae",
    "Punica": "Lythraceae",
    "Quercus": "Fagaceae",
    "Rheum": "Polygonaceae",
    "Santalum": "Santalaceae",
    "Sauropus": "Phyllanthaceae",
    "Sericocalyx": "Acanthaceae",
    "Sonchus": "Asteraceae",
    "Soya": "Fabaceae",               # = Glycine max
    "Strychnos": "Loganiaceae",
    "Syzygium": "Myrtaceae",
    "Talinum": "Talinaceae",
    "Tamarindus": "Fabaceae",
    "Terminalia": "Combretaceae",
    "Theae": "Theaceae",
    "Tinospora": "Menispermaceae",
    "Tribulus": "Zygophyllaceae",
    "Trigonella": "Fabaceae",
    "Usnea": "Parmeliaceae",          # lichen
    "Woodfordia": "Lythraceae",
    "Zea": "Poaceae",
    "Zingiber": "Zingiberaceae",
}


def herb_to_family(scientific_name: str) -> str:
    genus = scientific_name.split()[0] if scientific_name else ""
    return GENUS_FAMILY.get(genus, "UNKNOWN")


def normalized_entropy(counts: Counter) -> float:
    """Shannon entropy divided by log(n_categories) → ranges 0..1.
    0 = concentrated in one category, 1 = uniformly spread."""
    import math
    total = sum(counts.values())
    if total == 0 or len(counts) <= 1:
        return 0.0
    h = -sum(v / total * math.log(v / total) for v in counts.values() if v > 0)
    return h / math.log(len(counts))


def main():
    base = Path(__file__).resolve().parent.parent.parent
    comms = json.load(open(base / "data" / "kg" / "jamu_herb_communities.json",
                           encoding="utf-8"))
    assign = comms["community_assignments"]
    singletons = comms.get("bridge_singletons", [])
    labels = {p["community_id"]: p["label"] for p in comms["communities"]}

    # Coverage check
    all_herbs = set(assign) | set(singletons)
    unmapped = [h for h in all_herbs if herb_to_family(h) == "UNKNOWN"]
    print(f"Herbs: {len(all_herbs)}, unmapped genera: {len(unmapped)}")
    if unmapped:
        print("  Unmapped:", unmapped[:10])

    # Family distribution per community
    comm_family = defaultdict(Counter)
    for h, ci in assign.items():
        comm_family[ci][herb_to_family(h)] += 1

    # Reverse: family → communities it appears in
    family_to_comms = defaultdict(Counter)
    for h, ci in assign.items():
        family_to_comms[herb_to_family(h)][ci] += 1

    print("\n" + "=" * 90)
    print("FAMILY DISTRIBUTION WITHIN EACH COMMUNITY")
    print("=" * 90)
    for ci in sorted(comm_family):
        fams = comm_family[ci]
        total = sum(fams.values())
        ent = normalized_entropy(fams)
        top = ", ".join(f"{f}:{c}" for f, c in fams.most_common(5))
        print(f"\nS{ci} [{labels.get(ci,'?')[:38]:38s}] n={total:2d} "
              f"entropy={ent:.2f}")
        print(f"  {top}")

    print("\n" + "=" * 90)
    print("COMMUNITY DISTRIBUTION PER FAMILY (is this family mazhab-bound?)")
    print("=" * 90)
    print("Lower entropy = more concentrated in one mazhab")
    rows = []
    for fam, cc in family_to_comms.items():
        total = sum(cc.values())
        ent = normalized_entropy(cc)
        rows.append((fam, total, ent, cc))
    rows.sort(key=lambda r: (-r[1], r[2]))
    for fam, total, ent, cc in rows:
        if total < 2:
            continue
        dist = ", ".join(f"S{ci}:{c}" for ci, c in sorted(cc.items()))
        print(f"{fam:20s} n={total:2d} entropy={ent:.2f}  → {dist}")

    print("\n" + "=" * 90)
    print("Summary: how family-bound are the mazhab?")
    print("=" * 90)
    # For each community, compute entropy of its family distribution
    # Low entropy = community dominated by few families
    print("\nCommunity family-entropy (high = taxonomically diverse, low = single-family):")
    for ci in sorted(comm_family):
        ent = normalized_entropy(comm_family[ci])
        n = sum(comm_family[ci].values())
        print(f"  S{ci}  {labels.get(ci,'?')[:40]:40s}  n={n:2d}  entropy={ent:.2f}")

    # Multi-family vs single-family communities
    multi_family = sum(1 for ci in comm_family if len(comm_family[ci]) >= 3)
    print(f"\nCommunities with ≥3 distinct families: {multi_family}/{len(comm_family)}")

    # Singletons: what family?
    print(f"\nBridge singletons and their families:")
    for sn in singletons:
        print(f"  {sn[:40]:40s}  {herb_to_family(sn)}")

    # Save output
    output = {
        "genus_family_map": GENUS_FAMILY,
        "community_family_distribution": {
            f"S{ci}": dict(comm_family[ci]) for ci in sorted(comm_family)
        },
        "family_community_distribution": {
            fam: {f"S{ci}": c for ci, c in cc.items()}
            for fam, cc in family_to_comms.items()
        },
        "community_family_entropy": {
            f"S{ci}": round(normalized_entropy(comm_family[ci]), 3)
            for ci in sorted(comm_family)
        },
    }
    out_path = base / "data" / "kg" / "jamu_herb_taxonomy.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
