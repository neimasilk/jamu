---
type: meta
description: Chronological log of wiki + project activity. Append-only.
last_updated: 2026-05-07
---

# Wiki Log

Append-only chronological record. Format: `## [YYYY-MM-DD] <kind> | <title>`
where `<kind>` is `ingest`, `query`, `lint`, `analysis`, `manuscript`,
`recovery`, `wiki-bootstrap`. Recent first.

Quick listing: `grep "^## \[" wiki/log.md | tail -10`

## [2026-05-08] handoff | HANDOFF refreshed for clean restart

User akan restart komputer. HANDOFF.md di-refresh dengan:
- Top blockquote "⚡ RESTART READY" — snapshot git state, env state, dan
  instruksi resume.
- Section baru "May 7 (Sore) Session Summary — Wiki Adoption" yang merangkum
  bootstrap wiki dengan tujuh kearifan lokal.
- Resume Prompt updated mention CLAUDE.md auto-load + wiki/SCHEMA.md.
- Last commits di handoff: c2638a5 (wiki), 1649a74 (handoff fresh-clone),
  3813ef4 (pipeline), a922fa2 (mazhab viz).

Working tree clean, in sync dengan origin/main. Aman restart.

## [2026-05-07] analysis | Pipeline integration + figures regen (pagi, sesi paralel di mesin lain)

Sesi yang dijalankan oleh user dari mesin lain pagi tadi (commit `3813ef4`).
Menutup task (f) dari handoff post-petir:

- `run_full_pipeline.py` sekarang end-to-end: step1 sync → step2 rebuild →
  step3 annotate → step4 ontology-split → step5 viz (3 modules) → step6 stats
- `src/kg/builder.py`: tambah `edges="links"` di save/load (kompat networkx 3.4+)
- `src/analysis/network_pharmacology.py`: auto-detect KG terbaru (sebelumnya
  hardcoded ke v02)
- Figures **00, 01–17 regenerated dari v08** (jamukg_v08_annotated.json).
  Figures 18–20 belum punya generator script di `src/`, tracked sebagai known
  issue. Figures 21–22 (mazhab, dari sesi 3 Mei) tidak disentuh.
- Goal HKI dideklarasikan: Hak Cipta atas Program Komputer + Basis Data via
  DJKI. Reproduktibilitas pipeline jadi prerequisite untuk pendaftaran.

Notes: `NOTES_2026-05-07_pipeline_integration.md`. Commit `3813ef4`.

Implication untuk wiki: source page `knapsack.md` masih akurat, tapi belum
ada source pages untuk duke/pubmed/farmakope yang sekarang juga ter-konsumsi
end-to-end oleh pipeline. Tambah saat ingest berikutnya.

## [2026-05-07] wiki-bootstrap | Adopted Karpathy LLM Wiki pattern (sore)

- Created `CLAUDE.md` (root pointer)
- Created `wiki/SCHEMA.md` (keystone — schema with kearifan lokal)
- Created `wiki/README.md`, `wiki/index.md`, `wiki/log.md` (this file)
- Bootstrap concept pages: `validation_gap`, `forbidden_pairs`, `bridge_herb`
- Bootstrap entity pages: `Zingiber_officinale`, `mazhab/S0_warming_musculoskeletal`
- Bootstrap source page: `knapsack`
- Cloned `karpathy/autoresearch` into `inbox/autoresearch/` for reference; the
  loop pattern is **not** adopted (see SCHEMA G6); only the `program.md` /
  `results.tsv` discipline is kept for future bounded labs (G7)

Decision summary:
- Wiki augments, does not replace, canonical docs (MANUSCRIPT, MANIFESTO,
  HANDOFF, TRIAGE, PAPER_DRAFT, NOTES_*)
- Mandatory claim-provenance tags on quantitative claims
- Bilingual rule explicit (ID narrative, EN technical)
- Lint advisory only, never auto-fix
- Manifesto layer asymmetry visible in index.md, treated as honest signal

## [2026-05-03] analysis | Visualised 11 mazhab + 5 bridges as network figures

Post-recovery session. Generated `figures/21_mazhab_network.png` (full network,
106 herbs, 1136 lift edges, 30 forbidden pair overlay) and
`figures/22_mazhab_small_multiples.png` (per-mazhab subnetworks S0–S8).
`src/analysis/visualize_mazhab.py` reuses `build_lift_graph` from
`herb_communities.py` so the rendered graph is the same one Louvain analyzed
(no parameter drift).

Notes: `NOTES_2026-05-03_mazhab_visualization.md`. Commit `a922fa2`.

## [2026-05-03] recovery | Office computer struck by lightning; project recovered from git

All v08 artifacts intact — KG (16.4 MB), scripts in `src/analysis/`, raw data
(66 MB), figures, manuscript. Only ephemeral state lost (venv, IDE config,
inbox/ which holds the autoresearch repo separately). No uncommitted work
lost.

## [2026-04-20] analysis | Three sessions: grammar mazhab → robustness suite → ontology applied

Session 1 — Grammar depth:
- Found 11 stable "mazhab" via consensus-Louvain (40 seeds, ARI 0.72)
- Identified 5 bridge singletons: Blumea, Curcuma zedoaria, Sauropus, Abrus,
  Woodfordia
- Validated by plant-part axis (convergent) and taxonomy axis (divergent —
  jamu grammar is functional, not lineage-based)
- Notes: `NOTES_2026-04-20_grammar_schools.md`

Session 2 — Robustness suite (folded into the same notes file):
- Null model degree-preserving for forbidden pairs: Z=37.97, p ≪ 0.01
- Parameter sweep: 99.5% cross-mazhab rate across 60 configurations
- Script: `src/analysis/herb_communities_robustness.py`
- Output: `data/kg/jamu_robustness.json`

Session 3 — Ontology applied:
- Disease ontology cleanup (642 terms → 636 classified, 6 ambiguous resolved)
- Applied to KG: split TREATS into 4 edge types (TREATS clinical 6,923 +
  HAS_USE 1,387 + ETHNOBOTANICAL_USE 407 + APPLIED_TO 214)
- Produced KG v08 (`data/kg/jamukg_v08_annotated.json`)
- Re-ranked DDC: 8/30 plants replaced
- Updated MANUSCRIPT.md with v08 numbers
- Notes: `NOTES_2026-04-20_ontology_applied.md`
- Commit: `a611aa0`

Key honest finding: validation gap moved only 85.9% → 85.56% (way below
hypothesised 88.5% in original TRIAGE). Gap is structural across all 4
categories (82–87%), not a label artifact.

## [2026-04-16] analysis | KNApSAcK harvest complete; jamu grammar analysis

- KNApSAcK harvest: all 5,400 J-codes → 5,310 valid formulas
- KG v07 rebuilt via `run_full_pipeline.py` (auto-versioning added)
- All 21 figures (00–20) regenerated
- New analysis: jamu grammar classification (raja/menteri/kurir/penyeimbang),
  107 forbidden combinations, effect-specific subnetworks
- New analysis: disease ontology classifier (`src/analysis/disease_ontology.py`)
- HerbalDB harvester built (`src/harvest/herbaldb_harvester.py`) — site down
- Manuscript draft (~7,000 words) written; not for immediate submission

Decision: this is a long-term masterpiece project. Pace is deliberate.

## [2026-03-30] analysis | KG v0.5 built; KNApSAcK formulas integrated

KG grew from 13,422 → 15,673 nodes; 1,549 → 3,649 formulations. PubMed
annotation expanded.

## [2026-03-17] init | Initial KG v0.1

11,681 nodes, 35,836 edges, 2,048 plants, 49 formulations. Initial commit.

---

**Format reminder.** New entries go to the top, under a fresh `## [date] kind |
title` header. Body is plain prose with bullet points. Reference commits, file
paths, and other wiki pages by [[wikilink]] when useful.
