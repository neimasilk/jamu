---
type: meta
description: Content-oriented catalog of all wiki pages
last_updated: 2026-05-07
---

# Wiki Index

Catalog of all pages in this wiki, organized by type. The wiki is bootstrapped,
not exhaustive — see [SCHEMA.md §7](SCHEMA.md#7-roadmap) for what is deferred.

## Concepts (`wiki/concepts/`)

| Page | One-line summary | Manifesto |
|---|---|---|
| [validation_gap](concepts/validation_gap.md) | 85.56% of clinical TREATS claims have zero PubMed evidence — structural, not artifact | L4 |
| [forbidden_pairs](concepts/forbidden_pairs.md) | 107 herb pairs that never co-occur despite high individual frequency; Z=37.97 vs null model | L2 |
| [bridge_herb](concepts/bridge_herb.md) | 5 herbs that float between mazhab in consensus-Louvain; structurally important singletons | L2 |

**Deferred**: consensus_louvain, ontology_split, jamu_grammar_roles (raja/menteri/kurir/penyeimbang), DDC_priority

## Entities (`wiki/entities/`)

### Herbs (`wiki/entities/herbs/`)

| Page | Role | Mazhab | n_partners |
|---|---|---|---|
| [Zingiber officinale Rosc](entities/herbs/Zingiber_officinale.md) | kurir (universal bioenhancer) | S0 (warming musculoskeletal) | 362 |

**Deferred**: Curcuma xanthorrhiza, Eucalyptus alba, Morinda citrifolia, Eurycoma longifolia, Cocos nucifera, the 4 other bridge herbs (Curcuma zedoaria, Sauropus, Abrus, Woodfordia)

### Mazhab (`wiki/entities/mazhab/`)

| Page | Label | Size |
|---|---|---|
| [S0 — Warming musculoskeletal + aromatic base](entities/mazhab/S0_warming_musculoskeletal.md) | red cluster | 25 |

**Deferred**: S1–S10. Each gets a page when the work demands.

### Disease categories (`wiki/entities/diseases/`)

**Deferred**: 9 categories from disease ontology classifier.

## Sources (`wiki/sources/`)

| Page | Records | Size |
|---|---|---|
| [knapsack](sources/knapsack.md) | 5,310 formulas | 17 MB |
| [serat_centhini](sources/serat_centhini.md) | 1 vol (of 12) | 0.6 MB | L1 |

**Deferred**: duke_ethnobotany (40 MB), pubmed_evidence (3.7 MB), farmakope_indonesia (5.6 MB)

## Syntheses (`wiki/syntheses/`)

Pages that emerged from non-trivial queries and were filed back per
[SCHEMA §4.2](SCHEMA.md#42-query-when-user-asks-a-question).

**Deferred**: v07_to_v08_transition, why_85.56_pct_is_structural,
bridge_position_diagnosis. None yet — wiki is fresh.

## Labs (`wiki/labs/`)

Bounded sub-project workspaces (see [SCHEMA G7](SCHEMA.md#g7-sub-project-labs-are-bounded-not-loops)).

| Lab | Status | Layer |
|---|---|---|
| [L1_centhini_pilot](labs/L1_centhini_pilot/program.md) | phase1_baseline (21/32 recall; recipe-grammar found) | L1 |

**Deferred**: `labs/bridges/` — the 5 bridge herbs have a figure
(`figures/21_mazhab_network.png`) but no narrative pages yet.

## Meta files

- [README.md](README.md) — entry point
- [SCHEMA.md](SCHEMA.md) — maintenance contract (keystone)
- [log.md](log.md) — chronological log

## Cross-cutting view: Manifesto layer coverage

| Layer | Pages in wiki | Notes |
|---|---|---|
| L1 (Historical text mining) | labs/L1_centhini_pilot, sources/serat_centhini | **Frontier — opened 2026-05-25.** Phase 1 baseline: full 12-vol corpus + gold standard secured; dictionary recall 21/32; recipe-grammar (`jampi <ailment> … <ingredients> … <prep>`) found → RE feasible. Precision not yet formally tested; no validated claim. |
| L2 (Contemporary digital, KNApSAcK) | concepts/forbidden_pairs, concepts/bridge_herb, entities/herbs/Zingiber_officinale, entities/mazhab/S0, sources/knapsack | Well-developed |
| L3 (Cross-temporal alignment) | 0 | Needs L1 first |
| L4 (Validation bridge, PubMed) | concepts/validation_gap | Well-developed in canonical docs (`MANUSCRIPT.md`); only one wiki concept-page so far |
| cross | SCHEMA.md, README.md | Methodological |

The asymmetry is **honest, not a bug** — it reflects where the project actually
stands.
