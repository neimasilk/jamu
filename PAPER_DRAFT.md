# JamuKG: A Knowledge Graph for Mapping the Validation Gap in Indonesian Traditional Medicine

## Working Title
**"The Scattered Pharmacopoeia: Mapping the Validation Gap Between Indonesian Traditional Medicine and Modern Pharmacology Through Knowledge Graph Integration"**

*Target journal: Journal of Ethnopharmacology or Information Fusion*

---

## Abstract (Draft)

Indonesian traditional medicine (jamu) represents one of the world's richest empirical pharmacological traditions, yet its knowledge remains fragmented across incompatible sources and largely disconnected from modern scientific validation. We present JamuKG, an integrated knowledge graph that unifies pharmacological data from three major sources — Dr. Duke's Phytochemical and Ethnobotanical Database, the KNApSAcK Jamu database (3,599 formulas), and the Indonesian Herbal Pharmacopoeia — encompassing **2,437 plant species**, **7,364 chemical compounds**, **651 disease conditions**, and **3,599 jamu formulations** connected by **55,222 relationship edges**. By systematically cross-referencing all 5,744 plant-disease TREATS associations against PubMed, we quantify for the first time the *validation gap* between traditional claims and modern evidence: **85.9% of traditional plant-disease associations have zero published scientific evidence**, while only 1.3% are well-studied (20+ publications). We identify **286 priority drug discovery candidates** — plants with 5+ traditional therapeutic claims but no corresponding modern research. Network pharmacology analysis reveals 345 multi-target plants treating 3+ disease categories, with the Zingiberaceae family appearing in 65.9% of all jamu formulations. Herb co-occurrence analysis uncovers traditional combinatorial pharmacology patterns, with temulawak (*Curcuma xanthorrhiza*) and jahe (*Zingiber officinale*) co-occurring in 365 formulas. These findings demonstrate that Nusantara traditional medicine contains a vast, systematically unexplored pharmacological resource that merits urgent scientific investigation. JamuKG is released as open-source infrastructure for closing this validation gap.

---

## 1. Introduction

### 1.1 The Fragmented Pharmacopoeia
- Indonesia has one of the richest traditional medicine systems (jamu)
- Knowledge is scattered across 4 media: historical manuscripts, colonial records, digital marketplaces, modern literature
- No systematic integration exists

### 1.2 The Validation Problem
- Modern pharmacology "discovers" what traditional practitioners already knew
- But there is no systematic mapping of what has been validated and what hasn't
- The validation gap = the space between empirical traditional knowledge and modern scientific evidence

### 1.3 Comparison with TCM
- China's Traditional Chinese Medicine has been systematically codified (Bencao Gangmu, 1578)
- TCM has full state support, university programs, ICD-11 integration
- Indonesian jamu has no equivalent — no "Bencao Gangmu of Nusantara"
- Artemisinin example: text mining of classical TCM texts → Nobel Prize

### 1.4 Our Contribution
- JamuKG: first integrated knowledge graph of Indonesian traditional medicine
- Systematic quantification of the validation gap using PubMed cross-referencing
- Identification of priority drug discovery candidates
- Open-source infrastructure for future research

---

## 2. Related Work

### 2.1 Ethnopharmacological Databases
- KNApSAcK Jamu (Afendi et al., 2012) — formulas and herbs
- Dr. Duke's Phytochemical Database — global plant chemistry
- RISTOJA (2012, 2015, 2017) — Indonesian ethnomedicinal survey
- Farmakope Herbal Indonesia (Ed. I, II, Supplement I)

### 2.2 Knowledge Graphs in Pharmacology
- SymMap (Wu et al., 2019) — TCM knowledge graph
- HERB (Fang et al., 2021) — herb-target-disease KG
- GRAYU (Chun et al., 2021) — Korean medicine KG
- Gap: no equivalent for Indonesian traditional medicine

### 2.3 Validation Gap Analysis
- Previous work on individual plants (curcumin, ginger, etc.)
- No systematic mapping across an entire pharmacopoeia
- Our approach: automated PubMed cross-referencing of all claims

---

## 3. Methods

### 3.1 Data Sources and Harvesting
- **Dr. Duke's Phytochemical Database**: CSV bulk download, 1,987 plants, 7,331 compounds, 35,426 edges
- **KNApSAcK Jamu**: Web harvesting of ~5,400 jamu formulas (J-codes), ~5,261 herb ingredients
- **Farmakope Herbal Indonesia**: PDF parsing of Supplement I (55 monographs)

### 3.2 Knowledge Graph Schema
- Node types: Plant, Compound, Disease, Bioactivity, Formulation
- Edge types: TREATS, PRODUCES, HAS_ACTIVITY, CONTAINS
- Evidence levels: none, limited, moderate, well_studied
- Source provenance tracking

### 3.3 Entity Resolution and Integration
- Latin binomial normalization
- Indonesian-to-Latin name mapping (34 common plants)
- Cross-source entity merging with provenance preservation

### 3.4 Validation Gap Analysis
- Extract all Plant → Disease (TREATS) edges
- For each pair: query PubMed eutils API with "{Latin name}" AND "{disease term}"
- Classify by hit count: 0 = none, 1-5 = limited, 6-20 = moderate, 20+ = well_studied
- Rate-limited at 3 queries/second (NCBI policy)

---

## 4. Results

### 4.1 JamuKG Overview
- [Figure 1: KG overview — node/edge distributions]
- Total: 11,681 nodes, 35,836 edges, 62 connected components
- Dominated by compounds (7,364) and plants (2,048)

### 4.2 The Validation Gap
- [Figure 2: Validation gap pie chart + disease breakdown]
- **85.2% of plant-disease claims have ZERO PubMed evidence**
- Only 2.6% are well-studied (20+ papers)
- The gap is consistent across disease categories

### 4.3 Drug Discovery Candidates
- [Figure 3: Top candidates bar chart]
- 74 plants with 5+ unstudied claims
- Top: *Sida rhombifolia* (21), *Hydrocotyle asiatica* (20), *Nigella sativum* (20)
- These represent the highest-priority targets for pharmacological validation

### 4.4 Validation Heatmap
- [Figure 4: Plant × disease heatmap colored by evidence level]
- Shows the sparse landscape of evidence amid a sea of traditional claims
- Well-studied "islands": *Curcuma longa*, *Centella asiatica*, *Zingiber officinale*

### 4.5 Multi-Source Consensus
- [Figure 6: Source overlap chart]
- 34/2,437 plants appear in multiple databases
- Most plants documented in only one source — highlighting fragmentation

### 4.6 Formulation Analysis
- [Figure 12: Top jamu herbs, Figure 13: Effect groups, Figure 14: Co-occurrence]
- 3,599 KNApSAcK formulas analyzed, mean 4.9 herbs per formula
- Temulawak (*C. xanthorrhiza*) in 30.3% of ALL formulas
- Top co-occurrence: temulawak + jahe in 365 formulas
- Zingiberaceae family appears in 65.9% of all formulas

### 4.7 Network Pharmacology
- [Figure 10: Multi-target plants, Figure 11: Validation by category]
- 345 plants treat 3+ disease categories
- *Sida rhombifolia*: 9 disease categories, 19 known compounds
- Quercetin: most promiscuous compound (156 activities, 58 plant sources)
- *Eurycoma longifolia*: 94.4% specificity for musculoskeletal disorders

### 4.8 Drug Discovery Prioritization
- 621 plants with 3+ unstudied claims exported as candidate list
- *Nigella sativum*: 20 unstudied claims, 100% gap (zero studied)
- *Sophora tomentosa*: 18 unstudied claims, 100% gap

---

## 5. Discussion

### 5.1 The 85% Gap
- Most traditional knowledge has never been scientifically tested
- This is NOT evidence of absence — it's absence of evidence
- Implications for drug discovery: massive untapped resource

### 5.2 Why This Matters for Drug Discovery
- Empirical selection over hundreds of generations = natural pre-screening
- Modern drug discovery: $2.6B per drug, 10-15 year timeline
- Traditional knowledge as "pre-clinical evidence" that costs nothing to generate

### 5.3 Validated Claims as Ground Truth
- The ~3% well-studied pairs serve as validation for the KG
- Curcuma longa → anti-inflammatory: confirmed by >100 papers
- This gives confidence that the unstudied claims are worth investigating

### 5.4 Limitations
- PubMed coverage is English-biased; Indonesian-language papers may be missed
- Latin name matching may miss synonyms
- Evidence level based on hit count, not quality assessment
- Disease terms are heterogeneous (need ICD-10 mapping)

### 5.5 Future Work
- HerbalDB integration (3,810 species, 6,776 compounds)
- Historical manuscript mining (Serat Centhini, Usada Bali)
- Marketplace scraping (Tokopedia jamu listings)
- Network pharmacology analysis (multi-target pathways)
- ICD-10 disease normalization

---

## 6. Conclusion

JamuKG reveals that the vast majority of Indonesian traditional medicinal knowledge exists in a "validation dark zone" — empirically tested across centuries but invisible to modern science. This gap represents both a loss and an opportunity: a loss because valuable knowledge is being forgotten without scientific documentation, and an opportunity because it identifies thousands of pharmacological leads that have already passed the most brutal selection process — survival across generations. We release JamuKG as open-source infrastructure for closing this gap.

---

## Key Figures (16 total)

| # | Title | Type | File |
|---|-------|------|------|
| 1 | KG Overview | Bar chart | `figures/01_kg_overview.png` |
| 2 | Top Medicinal Plants | Horizontal bar | `figures/02_top_plants.png` |
| 3 | Top Diseases | Horizontal bar | `figures/03_top_diseases.png` |
| 4 | Top Bioactive Compounds | Horizontal bar | `figures/04_top_compounds.png` |
| 5 | Validation Gap Distribution | Pie + stacked bar | `figures/05_validation_gap.png` |
| 6 | Source Coverage | Bar chart | `figures/06_source_overlap.png` |
| 7 | Validation Heatmap | Heatmap matrix | `figures/07_validation_heatmap.png` |
| 8 | Drug Discovery Candidates | Horizontal bar | `figures/08_drug_discovery_candidates.png` |
| 9 | Disease Categories | Pie chart | `figures/09_disease_categories.png` |
| 10 | Multi-Target Plants | Horizontal bar | `figures/10_multi_target_plants.png` |
| 11 | Validation by Category | Stacked bar | `figures/11_validation_by_category.png` |
| 12 | Top Jamu Herbs | Horizontal bar | `figures/12_top_jamu_herbs.png` |
| 13 | Jamu Effect Groups | Horizontal bar | `figures/13_jamu_effect_groups.png` |
| 14 | Herb Co-occurrence | Heatmap | `figures/14_herb_cooccurrence.png` |
| 15 | Herb Therapeutic Specificity | Stacked bar | `figures/15_herb_therapeutic_specificity.png` |
| 16 | Compound Bioactivity Profile | Grouped bar | `figures/16_compound_bioactivity_profile.png` |

---

## Key Numbers for Abstract (KG v0.2)

- **2,289** plant species
- **7,364** chemical compounds
- **651** disease conditions
- **1,549** jamu formulations
- **6,673** treatment claims
- **43,908** relationship edges
- **~85.7%** validation gap (zero PubMed evidence)
- **88** priority drug discovery candidates (5+ unstudied claims)
- **26** multi-source consensus plants
- **3** integrated data sources (Dr. Duke's, KNApSAcK Jamu, Farmakope Herbal Indonesia)
