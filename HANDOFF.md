# JamuKG — Session Handoff

**Tanggal**: 16 April 2026
**Status**: KG v07 final, disease ontology clean, jamu grammar discovered

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

### Tier 1 — Foundation (mostly done)
- [x] Disease ontology cleanup (636/642 classified)
- [ ] Resolve 6 remaining ambiguous terms (minor)
- [ ] Apply ontology to KG: split TREATS into TREATS vs HAS_USE edges

### Tier 2 — Discovery (the interesting stuff)
- [x] Herb role classification (Raja/Menteri/Kurir/Penyeimbang)
- [x] Forbidden combinations (107 pairs found)
- [x] Effect-specific signature herbs
- [ ] **Deeper grammar analysis**: are there compositional *rules*? (e.g., "every muskuloskeletal formula must contain ≥1 Zingiberaceae + ≥1 Piperaceae")
- [ ] **Forbidden combinations investigation**: why do some pairs never co-occur? Pharmacological incompatibility or just different therapeutic domains?
- [ ] **Synergy prediction**: pairs with high co-occurrence + known bioenhancement mechanisms
- [ ] Visualize jamu grammar as network figures

### Tier 3 — Expansion
- [ ] HerbalDB harvest (server down, harvester ready)
- [ ] Historical text mining (Serat Centhini, Usada Bali)
- [ ] Marketplace mining (Tokopedia)
- [ ] Improve ICD-10 mapping (37.3% → target 80%+)

## Resume Prompt

```
Lanjutkan proyek JamuKG dalam mode santai — ini masterpiece jangka
panjang, bukan sprint. Baca HANDOFF.md dan TRIAGE.md. KG v07 sudah
final (17,413 nodes, 64,066 edges). Disease ontology bersih (636/642).
Temuan baru: grammar jamu teridentifikasi — 4 peran herbal
(Raja/Menteri/Kurir/Penyeimbang), 107 forbidden combinations,
signature herbs per area terapeutik. Lihat jamu_grammar.json. Arah
selanjutnya: dalami grammar analysis (aturan komposisi, investigasi
forbidden pairs, prediksi sinergi), atau eksplorasi apa pun yang
menarik dari data. Jangan buru-buru submit paper — baca MANIFESTO
dulu untuk konteks. Kerjakan dengan pelan dan matang.
```
