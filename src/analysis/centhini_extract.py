"""
Serat Centhini L1 Extraction — reproducible baseline
====================================================
Layer-1 (historical text mining) pilot extractor for the Serat Centhini.

This script is the *reproducible* replacement for the ad-hoc Phase-1 commands
that were run interactively in the 2026-05-25 session and never committed (the
abstract provenance tags `[script:dict-match]`, `[script:density-scan]`,
`[script:cross-check]` in the lab program referred to no real file). SCHEMA §3.3
requires `[script:<file.py>]`; running this file regenerates the Phase-1
artifacts deterministically from the public-domain corpus.

What it does (three passes, all deterministic, no network):

  1. density_scan()  — per-volume medical-marker + plant-term density. Reproduces
                       the "vol-3 is the herbal-dense volume" finding.
  2. dictionary_match() — Javanese-vernacular -> Latin dictionary recall against
                       the Nafayu (2025) gold standard. Writes recall.json +
                       contexts.txt. Reports BOTH the optimistic surface recall
                       (any match) AND the honest high-confidence recall (drops
                       the 3 flagged homonyms jati/pari/asem).
  3. cross_check()   — how many of the 32 gold species already live in JamuKG
                       (historical<->contemporary convergence, an L3 signal).

Matching rules (explicit, so anyone can reproduce):
  - Normalization: lowercase + fold OCR e-breve (U+0115/U+0114) -> 'e'. These are
    the ONLY non-ASCII letters present in the corpus; the fold is length
    preserving so match offsets map straight back onto the original text for
    context display. Add to FOLD_MAP if a new corpus introduces other diacritics.
  - A term matches on a whole-word boundary (`\bterm\b`) in the normalized text.
  - Per species, overlapping match intervals are merged so a single textual
    mention is never double-counted.
  - A match is "in medical context" (med_ctx) when it falls within MED_WINDOW
    characters of a recipe marker (jampi/usada/tamba/ginodhog/pipis).

Honesty notes (the point of committing this):
  - The hand-run Phase-1 numbers were internally inconsistent (the symptom this
    file fixes): some species were counted with diacritic folding, some without,
    and some terms used prefix instead of word-boundary matching. This file folds
    and bounds uniformly. Consequence: the reproducible recall is HIGHER than the
    2026-05-25 hand pass — 26/32 surface (was 21/32) — because uniform e-breve
    folding recovers five real mentions the hand pass missed (lempuyang ->
    Z. zerumbet, cengkeh -> Syzygium, kecipir -> Psophocarpus, kemukus ->
    P. cubeba, jinten cemeng -> Nigella). The hand 21/32 is kept visible in the
    lab program.md G4 table; this is an improvement, not a contradiction smoothed.
  - NO `status:validated` claim is produced here. Precision is still an eyeball
    estimate; the formal labeled-sample precision test (Manifesto §X) is the
    next step and is NOT run by this script (G2).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = ROOT / "data" / "raw" / "centhini" / "full12"
LEXICON_PATH = ROOT / "data" / "processed" / "centhini_javanese_lexicon_seed.json"
GOLD_PATH = ROOT / "data" / "processed" / "centhini_gold_standard_nafayu2025.json"
KG_PATH = ROOT / "data" / "kg" / "jamukg_v08_annotated.json"
RECALL_OUT = ROOT / "data" / "processed" / "centhini_phase1_recall.json"
CONTEXTS_OUT = ROOT / "data" / "processed" / "centhini_phase1_contexts.txt"

# === MATCHING PARAMETERS ===

# Recipe markers. A plant mention near one of these is taken to be in a
# medicinal context (a jampi/usada recipe) rather than incidental prose.
MEDICAL_MARKERS = ["jampi", "usada", "tamba", "ginodhog", "pipis"]
MED_WINDOW = 90  # characters either side of a match to scan for a marker

# Folding map for OCR diacritics actually present in the corpus. Length
# preserving on purpose (see module docstring). e-breve -> e.
FOLD_MAP = {0x0115: "e", 0x0114: "e"}

# Homonym terms the lexicon flags conf="ambig": "jati" (=true/genuine),
# "pari" (=companion, in pari-mitra), "asem" (=sour). They inflate the surface
# recall with false positives, so the honest headline excludes them.
AMBIG_CONF = "ambig"


def normalize(text):
    """Lowercase + fold e-breve. Length preserving -> offsets map to original."""
    return text.translate(FOLD_MAP).lower()


def load_corpus():
    """Return [(volume_label, original_text), ...] in volume order."""
    vols = []
    for path in sorted(CORPUS_DIR.glob("*.txt")):
        vols.append((path.stem, path.read_text(encoding="utf-8")))
    if not vols:
        sys.exit(f"No corpus files in {CORPUS_DIR}")
    return vols


def merge_intervals(spans):
    """Merge overlapping (start, end) spans; return non-overlapping count + list."""
    if not spans:
        return []
    spans = sorted(spans)
    merged = [spans[0]]
    for start, end in spans[1:]:
        if start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def find_marker_positions(norm_text):
    positions = []
    for marker in MEDICAL_MARKERS:
        for m in re.finditer(r"\b" + re.escape(normalize(marker)), norm_text):
            positions.append(m.start())
    positions.sort()
    return positions


def near_marker(pos, marker_positions):
    """True if pos is within MED_WINDOW of any marker (binary search)."""
    import bisect

    i = bisect.bisect_left(marker_positions, pos - MED_WINDOW)
    return i < len(marker_positions) and marker_positions[i] <= pos + MED_WINDOW


# === PASS 1: DENSITY SCAN ===

def density_scan(vols, lexicon):
    """Per-volume recipe-marker and plant-term density. Prints a small table."""
    plant_terms = sorted({t for entry in lexicon.values() for t in entry["terms"]})
    rows = []
    for label, text in vols:
        norm = normalize(text)
        jampi = len(re.findall(r"\bjampi", norm))
        plant_hits = sum(len(re.findall(r"\b" + re.escape(normalize(t)) + r"\b", norm))
                         for t in plant_terms)
        rows.append((label, jampi, plant_hits))
    densest = max(rows, key=lambda r: r[1] + r[2])
    print("Density scan (per volume):")
    print(f"  {'volume':14} {'jampi':>6} {'plant-term hits':>16}")
    for label, jampi, plant in rows:
        mark = "  <- densest" if (label, jampi, plant) == densest else ""
        print(f"  {label:14} {jampi:6} {plant:16}{mark}")
    return {label: {"jampi": j, "plant_term_hits": p} for label, j, p in rows}


# === PASS 2: DICTIONARY-MATCH RECALL ===

def dictionary_match(vols, lexicon):
    """Recall pass over the whole corpus. Returns (recall_dict, contexts_list)."""
    # One normalized stream so cross-volume offsets are global and unique.
    originals, norms, offsets, cursor = [], [], [], 0
    for _, text in vols:
        originals.append(text)
        norms.append(normalize(text))
        offsets.append(cursor)
        cursor += len(text) + 1  # +1 for the join separator
    full_original = "\n".join(originals)
    full_norm = "\n".join(norms)
    marker_positions = find_marker_positions(full_norm)

    recall = {}
    contexts = []
    for species, entry in lexicon.items():
        spans = []
        for term in entry["terms"]:
            pat = r"\b" + re.escape(normalize(term)) + r"\b"
            for m in re.finditer(pat, full_norm):
                spans.append((m.start(), m.end()))
        merged = merge_intervals(spans)
        med_spans = [(s, e) for s, e in merged if near_marker(s, marker_positions)]
        recall[species] = {
            "total": len(merged),
            "med_ctx": len(med_spans),
            "conf": entry["conf"],
            "hi_conf": entry["conf"] not in (AMBIG_CONF, "low"),
        }
        # Up to two medical-context snippets per species for precision eyeball.
        for s, e in med_spans[:2]:
            snippet = full_original[max(0, s - 100): e + 100]
            snippet = re.sub(r"\s+", " ", snippet).strip()
            contexts.append((species, full_original[s:e], snippet))
    return recall, contexts


def summarize(recall):
    """Compute headline recall fractions, surface vs honest high-confidence."""
    n = len(recall)
    named = [s for s, r in recall.items() if r["total"] > 0]
    med = [s for s, r in recall.items() if r["med_ctx"] > 0]
    hi_named = [s for s in named if recall[s]["hi_conf"]]
    hi_med = [s for s in med if recall[s]["hi_conf"]]
    return {
        "n_gold_species": n,
        "surface_named_recall": f"{len(named)}/{n}",
        "hi_conf_named_recall": f"{len(hi_named)}/{n}",
        "med_context_recall": f"{len(med)}/{n}",
        "hi_conf_med_context_recall": f"{len(hi_med)}/{n}",
        "ambig_homonyms_excluded": sorted(
            s for s in named if not recall[s]["hi_conf"]),
    }


# === PASS 3: CROSS-CHECK GOLD vs JamuKG ===

def cross_check(gold):
    """How many gold species already exist in JamuKG (L3 convergence signal)."""
    kg = json.loads(KG_PATH.read_text(encoding="utf-8"))
    latins = [n.get("latin_name", "").lower()
              for n in kg["nodes"] if n.get("node_type") == "plant"]
    latins = [l for l in latins if l]
    present, absent = [], []
    for species in gold:
        s = species.lower()
        # Genus+species match, ignoring trailing authority strings in the KG.
        hit = any(l == s or l.startswith(s + " ") or l.startswith(s)
                  or (" " + s + " ") in (" " + l + " ") for l in latins)
        (present if hit else absent).append(species)
    return present, absent


# === OUTPUT ===

def write_recall(recall, summary):
    payload = {
        "_meta": {
            "description": "Phase-1 dictionary-match recall of 32 Nafayu (2025) "
                           "gold species against the full 12-volume Serat Centhini.",
            "script": "src/analysis/centhini_extract.py",
            "corpus": "data/raw/centhini/full12/ (1,096,457 words, public domain)",
            "lexicon": "data/processed/centhini_javanese_lexicon_seed.json (hand-curated input)",
            "gold_standard": "data/processed/centhini_gold_standard_nafayu2025.json",
            "matching": "lowercase + e-breve fold; \\bterm\\b; merged intervals; "
                        f"med_ctx = within {MED_WINDOW} chars of "
                        f"{'/'.join(MEDICAL_MARKERS)}",
            "supersedes": "Ad-hoc 2026-05-25 hand counts (surface 21/32, med 19/32). "
                          "Uniform diacritic folding + word-boundary matching here "
                          "RAISES surface recall to 26/32 by recovering five real "
                          "OCR-diacritic mentions the hand pass missed; per-species "
                          "totals also differ. Deltas + rationale in "
                          "wiki/labs/L1_centhini_pilot/program.md (G4 table).",
            "status": "baseline — NOT status:validated (G2); formal precision test pending.",
        },
        "_summary": summary,
        "species": recall,
    }
    RECALL_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                          encoding="utf-8")


def write_contexts(contexts):
    lines = ["# Phase 1 dictionary-match contexts (strict medical window). "
             "For precision eyeball.",
             "# Regenerated by src/analysis/centhini_extract.py", ""]
    for species, term, snippet in contexts:
        lines.append(f"[{species} | {term}]")
        lines.append(f"  ...{snippet}...")
        lines.append("")
    CONTEXTS_OUT.write_text("\n".join(lines), encoding="utf-8")


def main():
    vols = load_corpus()
    total_words = sum(len(text.split()) for _, text in vols)
    print(f"Corpus: {len(vols)} volumes, {total_words:,} words\n")

    lexicon = json.loads(LEXICON_PATH.read_text(encoding="utf-8"))
    gold = json.loads(GOLD_PATH.read_text(encoding="utf-8"))["studied_species"]

    density_scan(vols, lexicon)
    print()

    recall, contexts = dictionary_match(vols, lexicon)
    summary = summarize(recall)
    write_recall(recall, summary)
    write_contexts(contexts)

    print("Recall (vs 32 gold species):")
    print(f"  surface named   : {summary['surface_named_recall']}")
    print(f"  high-confidence : {summary['hi_conf_named_recall']}  "
          f"(drops homonyms {', '.join(summary['ambig_homonyms_excluded'])})")
    print(f"  in medical ctx  : {summary['med_context_recall']}")
    print(f"  hi-conf med ctx : {summary['hi_conf_med_context_recall']}")
    print(f"  -> {RECALL_OUT.relative_to(ROOT)}")
    print(f"  -> {CONTEXTS_OUT.relative_to(ROOT)}\n")

    present, absent = cross_check(gold)
    print(f"Cross-check vs JamuKG v08: {len(present)}/{len(gold)} gold species present")
    print(f"  absent (likely synonyms / lost herbs): {', '.join(absent)}")


if __name__ == "__main__":
    main()
