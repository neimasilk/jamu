# JamuKG — Session Handoff

**Tanggal**: 3 Mei 2026 (last update)
**Status**: KG v08 (ontology-split). Mazhab teridentifikasi, validated, **dan tervisualisasikan** (figures 21+22). Methodology hardened.

> **Pasca-petir (3 Mei 2026)**: komputer kantor kena petir akhir April; recovery dari git utuh — semua artifact v08 (KG, scripts, figures, raw data 66 MB) ter-track dan ter-pulihkan. Tidak ada uncommitted work yang hilang.

---

## Core Findings

1. **85.9% validation gap** — of 5,744 traditional plant-disease claims, 85.9% have ZERO PubMed evidence. Confirmed robust after ontological cleanup (85.0–85.7% across all slicing methods).

2. **Jamu formulation grammar** — four functional herb roles identified from 5,310 formulas:
   - Raja (King): standalone therapeutic agents (Eucalyptus alba, Morinda citrifolia)
   - Menteri (Minister): specialists locked to specific therapeutic areas (Eurycoma longifolia 94% musculoskeletal)
   - Kurir (Courier): universal bioenhancers (Zingiber officinale = hub with 362 partners)
   - Penyeimbang (Harmonizer): broad-spectrum formula glue (Foeniculum vulgare, Amomum cardamomum)

3. **107 forbidden combinations** — herb pairs that never co-occur despite high individual frequency. Cocos nucifera × Piper retrofractum most striking (expected overlap 36, actual 0).

4. **Each therapeutic area has a distinct "base recipe"** — GI needs 2 signature herbs (3.4 mean), respiratory needs 7 (6.2 mean). Complexity correlates with pharmacological complexity.

## KG Evolution

| Version | Nodes | Edges | Plants | Formulations | Session |
|---------|-------|-------|--------|-------------|---------|
| v0.1 | 11,681 | 35,836 | 2,048 | 49 | Mar 17 |
| v0.2 | 13,422 | 43,908 | 2,289 | 1,549 | Mar 30 |
| v0.5 | 15,673 | 55,477 | 2,440 | 3,649 | Mar 30 |
| **v07** | **17,413** | **64,066** | **2,519** | **5,310** | **Apr 16** |

## What Was Accomplished (Apr 16 Session)

### Infrastructure
- KNApSAcK harvest **COMPLETE**: all 5,400 J-codes enumerated → 5,310 valid formulas
- KG v07 rebuilt via `run_full_pipeline.py` (auto-versioning added)
- All 21 figures regenerated with final data
- `paper_findings.json`, supplementary tables S1/S2, `drug_discovery_candidates.csv` all refreshed
- KNApSAcK herb effects harvester **fixed** (positional HTML parsing for changed page structure)
- HerbalDB harvester **built** (`src/harvest/herbaldb_harvester.py`) — site currently down

### Analysis (New)
- **Disease ontology classifier** (`src/analysis/disease_ontology.py`): classified 642 disease/use terms → 636 resolved, 6 ambiguous. Output: `data/kg/disease_ontology.json`
- **Jamu grammar analysis** (`src/analysis/jamu_grammar.py`): herb role classification, forbidden combinations, effect-specific subnetworks. Output: `data/kg/jamu_grammar.json`
- **Formulation analysis figures** (`src/analysis/formulation_analysis.py`): generates figures 12-17, 00

### Manuscript
- `MANUSCRIPT.md`: full paper written (~7,000 words), updated with v07 numbers
- **NOT for immediate submission** — proyek jangka panjang, bukan deliverable semester

### Triage Document
- `TRIAGE.md`: deliberated prioritization of next steps, three tiers

## Key Files

| File | Purpose |
|------|---------|
| `data/kg/jamu_grammar.json` | Herb roles, forbidden combinations, subnetworks |
| `data/kg/disease_ontology.json` | 642 disease terms classified into 9 categories |
| `data/kg/jamukg_v07_annotated.json` | Latest KG with PubMed evidence |
| `data/kg/paper_findings.json` | Key statistics for manuscript |
| `TRIAGE.md` | Prioritized next steps |
| `MANIFESTO_FARMAKOPE_NUSANTARA.md` | Vision document — the "why" |
| `MANUSCRIPT.md` | Full paper draft (not for immediate submission) |
| `src/analysis/jamu_grammar.py` | Jamu formulation grammar analysis |
| `src/analysis/disease_ontology.py` | Disease term ontological classifier |
| `src/analysis/formulation_analysis.py` | Formulation-specific figures |
| `src/harvest/herbaldb_harvester.py` | Ready for when HerbalDB comes back online |

## Project Philosophy

This is a **long-term masterpiece project** — like Michelangelo, not a semester paper mill. See `MANIFESTO_FARMAKOPE_NUSANTARA.md` for the full vision. The manifesto describes 4 layers:

| Layer | Status | Depth |
|-------|--------|-------|
| L4: Validation Bridge (PubMed) | **DONE** | Solid |
| L2: Contemporary Digital (KNApSAcK) | **DONE** | 5,310 formulas integrated |
| L1: Historical Text Mining | **NOT STARTED** | The real frontier |
| L3: Cross-Temporal Alignment | **NOT STARTED** | Needs L1 |

## What to Continue Next

Per `TRIAGE.md`, three tiers:

### Tier 1 — Foundation (DONE as of 2026-04-20)
- [x] Disease ontology cleanup (636/642 classified)
- [x] Resolve 6 remaining ambiguous terms (Apr 20 session 3: Ozoena/Syphilis3/Typhus→clinical; Internal/Medicine/MedicineVet→non_medical)
- [x] Apply ontology to KG: split TREATS into TREATS vs HAS_USE vs ETHNOBOTANICAL_USE vs APPLIED_TO — produces v08 KG

### Tier 2 — Discovery (substantial progress Apr 20)
- [x] Herb role classification (Raja/Menteri/Kurir/Penyeimbang)
- [x] Forbidden combinations (107 pairs found)
- [x] Effect-specific signature herbs
- [x] **Deeper grammar analysis** (Apr 20 session 1): found 11 stable "mazhab" (schools) via consensus-Louvain, each cohere in co-occurrence + plant-part but NOT in taxonomy → jamu grammar is functional-material, not lineage-based
- [x] **Forbidden combinations investigation** (Apr 20 session 1): structurally cross-mazhab. Null model Z=37.97. Parameter-robust (99.5% cross-rate across 60 configs)
- [x] **Methodological robustness suite** (Apr 20 session 2): null model + parameter sweep
- [ ] **Synergy prediction**: pairs with high co-occurrence + known bioenhancement mechanisms (not started)
- [ ] Visualize jamu grammar as network figures (not started)
- [ ] Piperaceae / TCM-island / bridge-herb case studies (scoped in NOTES)

### Tier 3 — Expansion
- [ ] HerbalDB harvest (server down, harvester ready)
- [ ] Historical text mining (Serat Centhini, Usada Bali)
- [ ] Marketplace mining (Tokopedia)
- [ ] Improve ICD-10 mapping (37.3% → target 80%+)
- [ ] Formulation-level PubMed validation (visibility of current 3,183-edge blind spot)

## April 20 Session Summary

Three sessions (grammar depth → methodological robustness → ontology applied).

**Key additions to the project**:
- `data/kg/jamu_herb_communities.json` — 11 stable mazhab + 5 bridges (consensus-Louvain, 40 seeds)
- `data/kg/jamu_herb_taxonomy.json` — family × mazhab entropy analysis (family entropy 0.81–1.00, i.e., cross-taxonomic)
- `data/kg/jamu_robustness.json` — null model Z=37.97, 60-config param sweep mean 99.5% cross-rate
- `data/kg/jamukg_v08_annotated.json` — ontology-split KG (8,931 treats → 6,923 TREATS + 1,387 HAS_USE + 407 ETHNOBOTANICAL_USE + 214 APPLIED_TO)
- `data/kg/drug_discovery_candidates_v08.json` — re-ranked by clinical-only unstudied claims (8/30 plants replaced)
- `NOTES_2026-04-20_grammar_schools.md` — mazhab findings + methodological defense
- `NOTES_2026-04-20_ontology_applied.md` — v08 build + honest note: gap barely moves but DDC list improves

**Updated headline numbers (propagated to MANUSCRIPT.md in session 3)**:
- Validation gap: **85.56%** of **3,740** clinical TREATS claims (was 85.9% of 5,744 mixed)
- Also: 87.0% of 1,387 HAS_USE, 87.5% of 407 ETHNOBOTANICAL_USE, 81.8% of 214 APPLIED_TO
- Gap is structural across all categories — not a label artifact
- Jamu grammar: **11 mazhab + 5 bridges**; 107 forbidden pairs Z=37.97 vs null
- Piperaceae splits into 3 mazhab by function; Zingiberaceae spans 5; no taxonomic coherence
- DDC count: **165 plants** with ≥5 unstudied *clinical* claims (was 286 pooled)

**Git state (end of 2026-04-20)**: commit `a611aa0` on main, pushed to origin. Working tree clean.

**Files that were NOT updated despite v08 data** (deferred honestly, not regressions):
- `figures/` 00–20 — generated from v07 data; need rerun with v08 split for paper revision (figures 21–22 baru, dari v08)
- `PAPER_DRAFT.md` — separate, shorter draft; not updated in this sweep (MANUSCRIPT.md is primary)
- `data/kg/paper_findings.json` validation_gap + drug_discovery_candidates sections — kept unchanged; new v08 section added alongside
- `run_full_pipeline.py` — predates v08; does not call `apply_disease_ontology.py` yet
- Bootstrap-formula robustness + alternative-association-measure tests — noted as future work in NOTES

## May 3 Session Summary

Sesi pendek pasca-recovery. Satu deliverable konkret (visualisasi mazhab):

- `src/analysis/visualize_mazhab.py` — reuse `build_lift_graph` dari `herb_communities.py` (no parameter drift)
- `figures/21_mazhab_network.png` — 106 herbs × 1,136 lift edges, 11 mazhab color-coded, 5 bridges sebagai diamonds berlabel, 30 forbidden pairs sebagai dashed red overlay
- `figures/22_mazhab_small_multiples.png` — 9 subnetwork per-mazhab (S0–S8) dengan internal edges
- `NOTES_2026-05-03_mazhab_visualization.md` — keputusan metodologis + arah lanjutan

Visual mengkonfirmasi klaim sebelumnya secara intuitif: forbidden pairs (merah putus) memotong antar-mazhab, tidak intra-mazhab. Bridge herbs berada di celah antar-cluster. Re-ranked arah lanjutan favoring bridge herb investigation karena posisi mereka sekarang visible.

## Resume Prompt (one paragraph, for a clean session)

Lanjutkan JamuKG — proyek masterpiece jangka panjang tentang integrasi farmakopeia Nusantara (lihat MANIFESTO_FARMAKOPE_NUSANTARA.md untuk visi). Baca dulu HANDOFF.md (status ini), TRIAGE.md (deliberasi + progress), dua NOTES_2026-04-20_*.md (tiga sesi April: grammar mazhab, robustness suite, ontology applied), dan NOTES_2026-05-03_mazhab_visualization.md (sesi pasca-petir, visualisasi). State saat ini: KG v08 sudah dibangun dengan ontology-split edges (6,923 TREATS clinical + 1,387 HAS_USE + 407 ETHNOBOTANICAL_USE + 214 APPLIED_TO), 11 mazhab stabil + 5 bridge herbs teridentifikasi via consensus-Louvain dan divalidasi oleh plant-part (konvergen) + taxonomy (divergen secara informatif — jamu grammar functional, bukan lineage-based), forbidden pairs lulus null model (Z=37.97) dan parameter sweep (99.5% cross-mazhab di 60 konfigurasi), MANUSCRIPT.md sudah diperbarui dengan angka v08 (85.56% dari 3,740 clinical TREATS; 165 priority DDC; Table 4 re-ranked), dan **figures/21+22 baru menampilkan jaringan mazhab** (overview + per-mazhab small multiples) dengan forbidden pair overlay. Arah lanjutan yang paling menarik belum dijalankan: (a) **bridge herb investigation** (5 herba bridge: Blumea, Curcuma zedoaria, Abrus, Sauropus, Woodfordia) — sekarang prioritas teratas karena posisi mereka sudah visible di figure 21, (b) **synergy prediction** dari pairs high-lift dikombinasikan dengan literatur bioenhancement, (c) **case study Piperaceae** atau **TCM-island (S8)** sebagai kandidat short paper, (d) **PubMed query-quality improvement** untuk mengaddress hipotesis 88.5% spesifik-term yang belum tercapai, atau (e) **regenerasi figures 00–20** dengan data v08 + update run_full_pipeline.py agar ontology step ter-integrate. Skrip reusable di `src/analysis/`: herb_communities.py, herb_taxonomy.py, herb_communities_robustness.py, apply_disease_ontology.py, visualize_mazhab.py. Prinsip user: **santai dalam waktu, serius dalam metodologi** — peneliti boleh salah/gagal/pivot asal tidak bohong. Jangan buru-buru submit paper. Tiga hal yang jangan diulang: (i) edit MANUSCRIPT.md tanpa konteks deliberasi dulu, (ii) menambah analisis baru tanpa robustness test, (iii) narrow exploration selama 3+ sesi — sesekali zoom out dan audit apa yang dihindari.
