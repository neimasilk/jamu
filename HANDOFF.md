# JamuKG — Session Handoff

**Tanggal**: 8 Mei 2026 (last update — restart-ready)
**Status**: KG v08 (ontology-split). Mazhab teridentifikasi, validated, tervisualisasikan. **Pipeline ter-integrate end-to-end**: `run_full_pipeline.py` sekarang produce v08-style output otomatis (rebuild → annotate → ontology-split → 3 figure modules). **Wiki paradigm adopted (Karpathy LLM Wiki)** — `CLAUDE.md` + `wiki/SCHEMA.md`. Methodology hardened.

> ## ⚡ RESTART READY (8 Mei 2026)
>
> Komputer akan di-restart. Snapshot sebelum mati:
> - **Git**: working tree clean. Last commit `c2638a5` "Adopt Karpathy LLM Wiki paradigm with kearifan lokal" sudah dipush ke `origin/main`. Branch `main` in sync (no ahead/behind).
> - **Tidak ada uncommitted work**. Aman restart.
> - **Setelah restart**: `cd C:/Users/amien/Documents/jamu && git status` harus print "nothing to commit, working tree clean". Kalau env Python hilang, `pip install -r requirements.txt` (lihat blockquote "Fresh clone" di bawah untuk daftar deps yang sebelumnya ter-install).
> - **Untuk Claude Code di sesi berikutnya**: `CLAUDE.md` di root sudah auto-pointer ke `wiki/SCHEMA.md` + HANDOFF.md (file ini) + `wiki/log.md` (last 5–10 entries via `grep "^## \[" wiki/log.md | tail -10`). Lanjutkan dari arah lanjutan yang dijelaskan di Resume Prompt paling bawah.

> **Pasca-petir (3 Mei 2026)**: komputer kantor kena petir akhir April; recovery dari git utuh — semua artifact v08 (KG, scripts, figures, raw data 66 MB) ter-track dan ter-pulihkan. Tidak ada uncommitted work yang hilang.

> **Mei 7 2026 (pagi)**: pipeline integration + figures regen (sesi otomatis, user busy). Detail: `NOTES_2026-05-07_pipeline_integration.md`. **Goal HKI** dideklarasikan — Hak Cipta atas Program Komputer + Basis Data via DJKI. Reproduktibilitas pipeline jadi prerequisite untuk pendaftaran.

> **Mei 7 2026 (sore) — wiki adoption**: project sekarang dioperasikan sebagai LLM-maintained wiki à la Karpathy. Read `CLAUDE.md` → `wiki/SCHEMA.md` di awal sesi. Wiki augments (tidak menggantikan) canonical docs. Autoresearch loop **tidak** diadopsi (lihat SCHEMA G6). Bootstrap content: SCHEMA, README, index, log; concepts (validation_gap, forbidden_pairs, bridge_herb); entities (Zingiber officinale, mazhab S0); source page knapsack. Halaman lain ditambah saat ingest berikutnya.

> **Fresh clone (7 Mei 2026)**: user baru re-clone repo dari `github.com/neimasilk/jamu.git`. Dataset lengkap dari git (no LFS, 126 tracked files, 158 MB total). Python deps di env sebelum restart: `seaborn, pyvis, biopython, tqdm, pyyaml, beautifulsoup4, pdfplumber, networkx, matplotlib, pandas, requests, pdfplumber, openai`. Setelah restart komputer, kalau env Python masih ada → tidak perlu install lagi; kalau env baru → `pip install -r requirements.txt`.

> **Git state akhir sesi 8 Mei 2026 (restart point)**:
> - Last 4 commit (terbaru di atas):
>   - `c2638a5` Adopt Karpathy LLM Wiki paradigm with kearifan lokal (7 Mei sore)
>   - `1649a74` Add fresh-clone + git-state notes to HANDOFF for clean restart (7 Mei pagi)
>   - `3813ef4` Integrate ontology step into pipeline; regen figures from v08 (7 Mei pagi)
>   - `a922fa2` Visualize 11 mazhab + 5 bridges as network figures (3 Mei sore)
> - Working tree: clean. Origin: in sync.

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

## May 7 Session Summary

Sesi otomatis (user busy → review later). Zoom-out dari orbit mazhab, tutup hutang infrastruktur untuk persiapan HKI:

- `run_full_pipeline.py` — ditambahi `step4_apply_ontology` antara annotate dan visualize; renumbered visualize→step5, stats→step6; step5 sekarang panggil tiga modul figure (visualize + network_pharmacology + formulation_analysis) bukan satu. **Pipeline sekarang produce v08-style output end-to-end dari satu perintah** `python run_full_pipeline.py`.
- `src/kg/builder.py` — `JamuKG.save/load` pakai `edges="links"` eksplisit; load tolerant terhadap kedua konvensi. Fix untuk networkx 3.4+ yang ubah default key dari `"links"` → `"edges"`. Tanpa fix, load v08 crash dengan `KeyError: 'edges'`.
- `src/analysis/network_pharmacology.py` — `main()` auto-detect KG terbaru, bukan hardcoded `jamukg_v02_*`.
- `figures/00, 01–17` (kecuali 18–20) — regenerated dari v08 KG. Timestamp 2026-05-07.
- `NOTES_2026-05-07_pipeline_integration.md` — keputusan metodologis + side-findings.

**Verifikasi**: split logic on v07 → identik dengan existing v08 report (8,931 → 6,923 + 1,387 + 407 + 214, 0 unmapped). Semua tiga figure-modul jalan end-to-end pada v08.

**Side-finding (honest)**: env user pasca-petir tidak punya `seaborn` + 6 deps lain dari `requirements.txt`; install ulang sudah dilakukan. Bukan problem desain — recovery env-nya yang belum lengkap. Untuk HKI, user perlu `pip install -r requirements.txt` di env clean.

**Figures 18–20 belum regen**: tidak ada generator script di `src/`; mereka dihasilkan ad-hoc. Perlu dilacak generatornya di sesi terpisah.

## May 7 (Sore) Session Summary — Wiki Adoption

Setelah diskusi tentang [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) dan [karpathy/autoresearch](https://github.com/karpathy/autoresearch), user minta adopsi paradigma wiki — bukan loop autoresearch. Hasil:

- `CLAUDE.md` (root) — auto-loaded oleh Claude Code; pointer ke `wiki/SCHEMA.md` + HANDOFF + log.md, plus tiga guardrails.
- `wiki/SCHEMA.md` — keystone (templates, frontmatter, claim-provenance tags, bilingual rule, ingest/query/lint workflow, tujuh guardrails). Tujuh kearifan lokal: provenance tags wajib (anti-Goodhart), manifesto layer tag, bilingual rule, wiki augments tidak menggantikan canonical docs, lint advisory only, **autoresearch loop ditolak eksplisit (G6)**, sub-project labs bounded saja (G7).
- `wiki/{README, index, log}` — entry, katalog, kronologi (di-seed dari sesi Mar 17 → 7 Mei).
- Bootstrap halaman: 3 concept (validation_gap, forbidden_pairs, bridge_herb), 2 entity (Zingiber officinale, mazhab S0), 1 source (knapsack). Halaman lain ditambah saat ingest berikutnya per SCHEMA §7.
- `inbox/autoresearch/` — clone repo Karpathy untuk referensi (sudah di .gitignore karena punya git-repo terpisah).
- `.gitignore` — tambah `.env` + `.env.*` (secrets).

**Tabrakan dengan sesi 7 Mei pagi**: HANDOFF.md di-edit kedua sesi; resolved integratif via rebase. TRIAGE.md auto-merge sukses. File lain tidak overlap.

**Yang sengaja TIDAK dilakukan**: tidak edit MANUSCRIPT.md, tidak refactor canonical docs ke wiki/, tidak generate halaman exhaustive (compounding-from-use principle), tidak adopt autoresearch loop (G6).

## Resume Prompt (one paragraph, for a clean session)

Lanjutkan JamuKG — proyek masterpiece jangka panjang tentang integrasi farmakopeia Nusantara (lihat MANIFESTO_FARMAKOPE_NUSANTARA.md untuk visi). **Auto-load oleh Claude Code**: `CLAUDE.md` di root → ikut perintahnya untuk baca `wiki/SCHEMA.md` (keystone wiki schema), HANDOFF.md (file ini), dan `wiki/log.md` last 5–10 entries. Wiki paradigm adopted (Karpathy LLM Wiki) dengan tujuh kearifan lokal di SCHEMA §6; autoresearch loop **ditolak** (G6). Konteks tambahan kalau perlu: TRIAGE.md, dua NOTES_2026-04-20_*.md, NOTES_2026-05-03_mazhab_visualization.md, NOTES_2026-05-07_pipeline_integration.md. State saat ini: KG v08 dengan ontology-split edges (6,923 TREATS clinical + 1,387 HAS_USE + 407 ETHNOBOTANICAL_USE + 214 APPLIED_TO); 11 mazhab + 5 bridge herbs (consensus-Louvain, plant-part konvergen, taxonomy divergen → jamu grammar functional bukan lineage-based); forbidden pairs lulus null model Z=37.97 dan parameter sweep 99.5% cross-mazhab; MANUSCRIPT.md updated v08 (85.56% dari 3,740 clinical TREATS, 165 priority DDC); **figures 21+22** mazhab network + small multiples; **figures 00–17 regenerated dari v08 (7 Mei 2026)**; **`run_full_pipeline.py` sekarang end-to-end reproducible** dengan ontology step terintegrasi (step1 sync → step2 rebuild → step3 annotate → step4 ontology-split → step5 viz × 3 modul → step6 stats); **wiki/ ter-bootstrap** dengan SCHEMA + 9 halaman seed (concepts, entities, sources, log). **Tujuan HKI**: user ingin satu Hak Cipta DJKI atas Program Komputer + Basis Data dari proyek ini; reproduktibilitas pipeline sudah memenuhi technical bar untuk pendaftaran. Arah lanjutan yang belum dikerjakan: (a) **bridge herb investigation** (Blumea, Curcuma zedoaria, Abrus, Sauropus, Woodfordia) — figure 21 sudah menunjukkan posisi mereka; concept page `wiki/concepts/bridge_herb.md` sudah ada dengan TBD table — kandidat lab pertama; (b) **synergy prediction** dari pairs high-lift + bioenhancement literature; (c) **case study Piperaceae** atau **TCM-island (S8)** sebagai short paper; (d) **PubMed query-quality improvement** (hipotesis 88.5% spesifik-term, masih belum dieksplorasi); (e) **HKI registration prep** — dokumen deskripsi sistem, screenshot pipeline jalan, source archive. Skrip reusable di `src/analysis/`: herb_communities.py, herb_taxonomy.py, herb_communities_robustness.py, apply_disease_ontology.py, visualize_mazhab.py, jamu_grammar.py. Prinsip user: **santai dalam waktu, serius dalam metodologi** — peneliti boleh salah/gagal/pivot asal tidak bohong. Jangan buru-buru submit paper. Tiga guardrails yang jangan diulang (juga di `CLAUDE.md` dan `wiki/SCHEMA.md` §G1–G3): (i) edit MANUSCRIPT.md tanpa konteks deliberasi dulu, (ii) menambah analisis baru tanpa robustness test, (iii) narrow exploration selama 3+ sesi — sesekali zoom out dan audit apa yang dihindari. Sesi 7 Mei sudah break dari mazhab orbit (sesi infrastruktur + wiki), jadi sesi berikutnya boleh kembali ke analytical work.
