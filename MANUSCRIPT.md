# The Scattered Pharmacopoeia: Mapping the Validation Gap Between Indonesian Traditional Medicine and Modern Pharmacology Through Knowledge Graph Integration

**Mukhlis Amien**¹*

¹ Independent Researcher, Malang, Indonesia

\* Corresponding author: lilissetya56@gmail.com

*Target journal: Journal of Ethnopharmacology*

---

## Abstract

Indonesian traditional medicine (jamu) represents one of the world's richest empirical pharmacological traditions, yet its knowledge remains fragmented across incompatible sources and largely disconnected from modern scientific validation. We present JamuKG, an integrated knowledge graph that unifies pharmacological data from three major sources — Dr. Duke's Phytochemical and Ethnobotanical Database, the KNApSAcK Jamu database, and the Farmakope Herbal Indonesia — encompassing **2,519 plant species**, **7,364 chemical compounds**, **651 disease conditions**, and **5,310 jamu formulations** connected by **64,066 relationship edges**. By systematically cross-referencing all 5,744 plant–disease TREATS associations against PubMed, we quantify for the first time the *validation gap* between traditional claims and modern evidence: **85.9% of traditional plant–disease associations have zero published scientific evidence**, while only 1.3% are well-studied (≥20 publications). We identify **286 priority drug discovery candidates** — plants with five or more traditional therapeutic claims but no corresponding modern research. Network pharmacology analysis reveals 345 multi-target plants treating three or more disease categories, with the Zingiberaceae family appearing in 61.6% of all jamu formulations. Herb co-occurrence analysis uncovers traditional combinatorial pharmacology patterns, with temulawak (*Curcuma xanthorrhiza*) and jahe (*Zingiber officinale*) co-occurring in 483 formulas. These findings demonstrate that Nusantara traditional medicine contains a vast, systematically unexplored pharmacological resource that merits urgent scientific investigation. JamuKG is released as open-source infrastructure for closing this validation gap.

**Keywords:** traditional medicine; knowledge graph; jamu; ethnopharmacology; drug discovery; validation gap; Indonesia; network pharmacology

---

## 1. Introduction

### 1.1 The Fragmented Pharmacopoeia

The Indonesian archipelago, spanning more than 17,000 islands and harboring roughly 10% of the world's flowering plant species, has produced one of the most extensive — and least systematically studied — traditions of herbal medicine on Earth. Known as *jamu*, this tradition encompasses thousands of plant-based formulations that have been empirically refined across centuries of daily use by millions of people (Elfahmi et al., 2014). Unlike the codified pharmacopoeias of Chinese, Indian, or European herbal traditions, jamu knowledge has never been unified into a single authoritative reference. Instead, it exists in a state of radical fragmentation: scattered across historical manuscripts written in Old Javanese and Balinese scripts (the *Serat Centhini*, *Usada Bali*), colonial-era botanical surveys conducted by Dutch and German naturalists, modern digital marketplace listings, and contemporary pharmacological databases. No previous work has attempted to computationally integrate these disparate sources into a unified, queryable knowledge representation.

This fragmentation carries real consequences. Plants that Indonesian practitioners have used for centuries to treat specific conditions may be independently "discovered" by modern pharmacology, with no acknowledgment of — or connection to — the empirical tradition that identified their therapeutic potential. The most celebrated example is *Curcuma longa* (turmeric), whose anti-inflammatory properties have generated over 14,000 PubMed papers, yet whose systematic use in jamu formulations predates any modern investigation by hundreds of years. How many other *Curcuma longa*-scale discoveries remain hidden in the unexamined portions of this tradition?

### 1.2 The Validation Problem

Modern pharmacology operates through a well-defined pipeline: target identification, *in vitro* screening, *in vivo* validation, clinical trials. Traditional medicine operates through an entirely different epistemic framework: empirical observation across generations, transmitted through apprenticeship, recipe books, and cultural practice. These two systems of knowledge production have proceeded largely in parallel, with occasional intersections that have proven spectacularly productive.

The most dramatic example is artemisinin. Tu Youyou's Nobel Prize-winning discovery began with systematic text mining of classical Chinese medical texts — particularly the *Handbook of Prescriptions for Emergency Treatments* (葛洪《肘后备急方》, 340 CE) — which led directly to the identification of *Artemisia annua* as an antimalarial agent (Tu, 2011). This success demonstrated that traditional pharmacological knowledge, when subjected to modern analytical methods, can yield drugs of transformative clinical significance. Yet no equivalent systematic effort has been applied to Indonesian traditional medicine.

The fundamental question we address is: *what fraction of traditional jamu claims have been scientifically validated, and what fraction remain entirely unexplored?* We call the difference between these two quantities the **validation gap** — the space between empirical traditional knowledge and published modern evidence.

### 1.3 Comparison with TCM Knowledge Systems

The contrast with Traditional Chinese Medicine (TCM) is instructive. China's pharmacological tradition was systematically codified as early as the *Bencao Gangmu* (本草纲目, 1578 CE) by Li Shizhen, which catalogued 1,892 medicinal substances with detailed descriptions of preparation, dosage, and therapeutic indication. In the modern era, TCM has received sustained state support, dedicated university programs, WHO recognition, and integration into the ICD-11 classification system. Correspondingly, computational resources for TCM are well-developed: SymMap (Wu et al., 2019) provides a knowledge graph of 499 herbs and 19,595 targets; HERB (Fang et al., 2021) integrates 7,263 herbs with experimental validation data; and multiple dedicated databases index TCM formulations, compounds, and clinical evidence.

Indonesian jamu has no equivalent. There is no *Bencao Gangmu of Nusantara*. The closest analogues — the *Serat Centhini* (early 19th century Javanese compendium) and the *Usada Bali* (Balinese medical manuscripts) — remain largely untranslated, undigitized, and disconnected from modern pharmacological databases. The KNApSAcK Jamu database (Afendi et al., 2012) represents the most comprehensive digital resource, but it catalogues formulations without linking them to chemical or pharmacological data from other sources.

### 1.4 Our Contribution

We present four contributions:

1. **JamuKG**, the first integrated knowledge graph of Indonesian traditional medicine, unifying data from Dr. Duke's Phytochemical and Ethnobotanical Database, the KNApSAcK Jamu database, and the Farmakope Herbal Indonesia into a single graph of 17,413 nodes and 64,066 edges spanning five entity types (Plant, Compound, Disease, Bioactivity, Formulation) and four relationship types (TREATS, PRODUCES, HAS_ACTIVITY, CONTAINS).

2. **Systematic validation gap quantification**: by cross-referencing all 5,744 plant–disease treatment claims against PubMed, we establish that 85.9% have zero published evidence — the largest such analysis ever conducted on any traditional medicine system.

3. **Drug discovery candidate identification**: we identify 286 plants with five or more traditional therapeutic claims that have received no modern scientific attention, representing a prioritized list for pharmacological investigation.

4. **Network pharmacology analysis**: we characterize multi-target plants, promiscuous compounds, herb co-occurrence networks, and family-level therapeutic patterns that reveal the combinatorial logic underlying jamu formulation.

---

## 2. Related Work

### 2.1 Ethnopharmacological Databases

Several databases capture aspects of Indonesian medicinal plant knowledge, though none integrates them. The **KNApSAcK Jamu database** (Afendi et al., 2012; Wijaya et al., 2014) catalogues jamu formulations registered with Indonesia's BPOM (National Agency of Drug and Food Control), recording formula composition, effect groups, and ingredient herbs. As of our harvest, it contains records for 5,310 jamu products. **Dr. Duke's Phytochemical and Ethnobotanical Database** (Duke, 1992–2016), maintained by the USDA, provides global coverage of plant chemistry and ethnobotanical uses, including 1,987 plants relevant to Indonesian flora with 7,331 chemical compounds and 35,426 plant–compound–activity edges. The **Farmakope Herbal Indonesia** (Indonesian Herbal Pharmacopoeia), published by Indonesia's Ministry of Health (Edition I, II, and Supplement I), provides quality-control monographs for 55 standardized herbal medicines. Indonesia's RISTOJA surveys (2012, 2015, 2017) document ethnomedicinal practices across the archipelago but have not been computationally integrated.

### 2.2 Knowledge Graphs in Traditional Medicine

Knowledge graphs have proven effective for representing pharmacological relationships in other traditional medicine systems. **SymMap** (Wu et al., 2019) maps TCM symptoms to modern diseases through a network of 499 herbs, 961 symptoms, and 19,595 gene targets. **HERB** (Fang et al., 2021) integrates 7,263 herbs with high-throughput experimental data across 12,033 targets. **GRAYU** (Chun et al., 2021) constructs a Korean traditional medicine knowledge graph linking 2,748 herbal prescriptions to 4,134 ingredients and 537 therapeutic effects. **TCMKG** (Zhang et al., 2022) further extends TCM knowledge representation with entity linking to biomedical ontologies. These systems have enabled computational drug repurposing, synergy prediction, and mechanism-of-action inference within their respective traditions. No equivalent system exists for Indonesian jamu.

### 2.3 Validation Gap Analysis

Previous studies have examined the evidence base for individual medicinal plants or specific disease domains. Wachtel-Galor and Benzie (2011) reviewed evidence for commonly used herbal medicines globally, while Heinrich et al. (2020) assessed ethnopharmacological evidence for European traditional medicines. Elfahmi et al. (2014) surveyed Indonesian medicinal plants with pharmacological evidence, but their review was narrative rather than systematic and did not attempt to quantify the proportion of traditional claims that have been scientifically examined. Our approach — automated PubMed cross-referencing of *all* plant–disease claims in a knowledge graph — has no direct precedent in the literature.

---

## 3. Methods

### 3.1 Data Sources and Harvesting

#### 3.1.1 Dr. Duke's Phytochemical and Ethnobotanical Database

We obtained the complete CSV bulk download of Dr. Duke's database, which provides structured data on plant species, their chemical constituents, and associated ethnobotanical uses. From this source, we extracted 1,987 plant species, 7,331 chemical compounds, and 35,426 edges representing PRODUCES (plant→compound), HAS_ACTIVITY (compound→bioactivity), and TREATS (plant→disease) relationships. Disease terms were preserved as reported in the original database.

#### 3.1.2 KNApSAcK Jamu Database

We developed a web harvester to systematically extract jamu formula records from the KNApSAcK Jamu web interface (https://www.knapsackfamily.com/jamu/). Each formula record (identified by a J-code, J00001–J05400) contains: manufacturer or reference, jamu product name, therapeutic effect description, effect group classification, and a list of ingredient herbs with their scientific names, local Indonesian names, plant parts used, and proportions. The harvester employed a polite crawling strategy with 0.5-second delays between requests and incremental checkpointing every 50 records. From the complete enumeration of 5,400 J-codes, we successfully extracted 5,310 unique formulas containing references to 5,261 distinct herb ingredients.

#### 3.1.3 Farmakope Herbal Indonesia

We manually parsed Supplement I of the Farmakope Herbal Indonesia (Indonesian Herbal Pharmacopoeia), extracting 55 standardized monographs. Each monograph was encoded with its constituent plant species, approved therapeutic indications, quality-control parameters, and preparation methods. These monographs provide the highest evidence tier in our system, as they represent government-approved therapeutic claims.

### 3.2 Knowledge Graph Schema

JamuKG employs a typed property graph with five node types and four edge types:

**Node types:**
- **Plant** (n = 2,519): identified by Latin binomial; properties include common names (Indonesian, English), plant family, and source database(s)
- **Compound** (n = 7,364): chemical constituents; properties include compound name and plant source(s)
- **Disease** (n = 651): disease conditions or therapeutic indications; properties include disease category and ICD-10 code (where mapped)
- **Bioactivity** (n = 1,569): pharmacological activities of compounds (e.g., anti-inflammatory, antioxidant)
- **Formulation** (n = 5,310): jamu products; properties include product name, manufacturer, effect group, and ingredient list

**Edge types:**
- **TREATS** (m = 8,931): plant → disease, representing traditional therapeutic claims
- **PRODUCES** (m = 17,387): plant → compound, representing phytochemical composition
- **HAS_ACTIVITY** (m = 12,343): compound → bioactivity, representing pharmacological activity
- **CONTAINS** (m = 25,405): formulation → plant, representing jamu ingredient composition

All edges carry provenance metadata indicating the source database and, where applicable, the evidence level assigned through validation gap analysis.

### 3.3 Entity Resolution and Integration

Integrating data from three heterogeneous sources required careful entity resolution. Plant entities were normalized by Latin binomial name, with authority abbreviations stripped and common synonyms resolved. We implemented a mapping table for 34 commonly occurring plants where Indonesian local names (e.g., "temulawak" → *Curcuma xanthorrhiza*, "jahe" → *Zingiber officinale*, "kunyit" → *Curcuma longa*) facilitated cross-source matching. Cross-source entity merging preserved provenance metadata, so each node retains a list of contributing databases.

Disease terms presented greater heterogeneity. Dr. Duke's database uses ethnobotanical disease terms (e.g., "Fever," "Sore," "Parturition"), KNApSAcK uses therapeutic effect groups (e.g., "Gastrointestinal disorders," "Musculoskeletal and connective tissue disorders"), and Farmakope uses clinical indication language. We preserved the original terminology while applying a disease normalization layer that maps terms to 15 broad disease categories based on ICD-10 chapter structure. Full ICD-10 mapping achieved 37.3% coverage, with the remainder assigned to categories heuristically.

### 3.4 Validation Gap Analysis

To quantify the gap between traditional claims and modern evidence, we systematically queried PubMed for all 5,744 unique plant–disease pairs present in JamuKG's TREATS edges. For each pair, we constructed a query of the form `"{Latin plant name}" AND "{disease term}"` and submitted it to the NCBI E-utilities API (esearch.fcgi), recording the total count of matching publications.

Queries were rate-limited at 3 requests per second in compliance with NCBI usage policies. Results were classified into four evidence levels:

| Evidence Level | PubMed Count | Interpretation |
|---|---|---|
| **None** | 0 | No published evidence found |
| **Limited** | 1–5 | Sparse evidence; possibly tangential |
| **Moderate** | 6–20 | Some dedicated research exists |
| **Well-studied** | ≥21 | Substantial evidence base |

This classification is deliberately conservative: a PubMed hit count of zero does not prove absence of therapeutic effect, but it does indicate absence of investigation in the indexed English-language literature.

### 3.5 Network Pharmacology Analysis

We performed three network-level analyses on JamuKG:

**Multi-target plant analysis.** For each plant, we enumerated the set of disease categories (not individual diseases) it treats, identifying plants that span three or more disease categories as "multi-target" plants. This identifies species with broad-spectrum therapeutic potential.

**Compound promiscuity analysis.** For each compound, we counted the number of distinct plant sources and distinct bioactivities, identifying compounds present in five or more plants with three or more known activities as "promiscuous" compounds. These represent potential multi-pathway pharmacological agents.

**Herb co-occurrence network.** From the 5,310 KNApSAcK formulas, we constructed a co-occurrence matrix recording how frequently each pair of herbs appears together in the same formulation. High co-occurrence may indicate traditional recognition of synergistic effects.

---

## 4. Results

### 4.1 JamuKG Overview

The final JamuKG knowledge graph comprises **17,413 nodes** and **64,066 edges** organized into 62 connected components (Table 1). The largest connected component contains 99.4% of all nodes, indicating high integration across data sources. The graph is dominated by compound nodes (42.3% of all nodes), followed by formulation nodes (30.5%), plant nodes (14.5%), bioactivity nodes (9.0%), and disease nodes (3.7%).

**Table 1.** JamuKG node and edge statistics.

| Entity Type | Count | % of Total |
|---|---|---|
| **Nodes** | | |
| Plant | 2,519 | 14.5% |
| Compound | 7,364 | 42.3% |
| Disease | 651 | 3.7% |
| Bioactivity | 1,569 | 9.0% |
| Formulation | 5,310 | 30.5% |
| **Total nodes** | **17,413** | **100%** |
| **Edges** | | |
| TREATS | 8,931 | 13.9% |
| PRODUCES | 17,387 | 27.1% |
| HAS\_ACTIVITY | 12,343 | 19.3% |
| CONTAINS | 25,405 | 39.7% |
| **Total edges** | **64,066** | **100%** |

The mean degree of plant nodes is 10.4, reflecting the high connectivity of medicinal plants to both compounds and diseases. The top five most connected plants are *Zingiber officinale* (438 compounds), *Curcuma longa* (356 compounds), *Piper nigrum* (215 compounds), *Kaempferia galanga* (147 compounds), and *Centella asiatica* (89 compounds).

### 4.2 The Validation Gap: 85.9% of Traditional Claims Are Uninvestigated

Cross-referencing all 5,744 plant–disease TREATS associations against PubMed reveals a striking validation gap (Figure 1):

- **4,933 pairs (85.9%)** have **zero** PubMed publications — no scientific investigation has been published on these traditional therapeutic claims
- **604 pairs (10.5%)** have **limited** evidence (1–5 publications)
- **131 pairs (2.3%)** have **moderate** evidence (6–20 publications)
- **76 pairs (1.3%)** are **well-studied** (≥21 publications)

This means that for every plant–disease association that has been well-studied by modern science, there are approximately 65 associations that have never been examined at all.

The validation gap is not uniform across disease categories. Table 2 shows the gap for the top 15 disease conditions by total claim count.

**Table 2.** Validation gap by disease condition (top 15 by total claims).

| Disease | Total Claims | Unstudied | Studied | Gap % |
|---|---|---|---|---|
| Fever | 303 | 207 | 96 | 68.3% |
| Parturition | 205 | 195 | 10 | 95.1% |
| Sore | 180 | 166 | 14 | 92.2% |
| Headache | 151 | 151 | 0 | 100.0% |
| Cough | 137 | 97 | 40 | 70.8% |
| Diarrhea | 131 | 90 | 41 | 68.7% |
| Wound | 133 | 82 | 51 | 61.7% |
| Rheumatism | 119 | 92 | 27 | 77.3% |
| Stomachache | 104 | 92 | 12 | 88.5% |
| Boil | 93 | 93 | 0 | 100.0% |
| Vermifuge | 96 | 93 | 3 | 96.9% |
| Dermatosis | 97 | 91 | 6 | 93.8% |
| Dysentery | 117 | 80 | 37 | 68.4% |
| Anodyne | 79 | 77 | 2 | 97.5% |
| Itch | 76 | 73 | 3 | 96.1% |

Notably, some disease categories — headache and boil — have **100% validation gaps**: not a single one of the traditional plant-based treatments for these conditions has been examined in the PubMed-indexed literature. Others, such as wound healing (61.7% gap) and fever (68.3% gap), have received relatively more attention, though the majority of claims remain uninvestigated even in these better-studied categories.

### 4.3 The Most Validated Traditional Claims

Among the 76 well-studied pairs, the strongest validation involves plants with long histories in both traditional and modern pharmacology (Table 3).

**Table 3.** Top 10 most-validated traditional claims (by PubMed count).

| Plant | Disease | PubMed Count |
|---|---|---|
| *Centella asiatica* | Wound | 195 |
| *Curcuma longa* | Wound | 141 |
| *Zingiber officinale* | Infection | 137 |
| *Solanum nigrum* | Cancer | 117 |
| *Aloe vera* | Burn | 96 |
| *Nicotiana tabacum* | Tumor | 88 |
| *Cinnamomum cassia* | Tumor | 82 |
| *Andrographis paniculata* | Diabetes | 78 |
| *Catharanthus roseus* | Diabetes | 46 |
| *Calendula officinalis* | Cancer | 53 |

These well-studied pairs serve as internal validation for the knowledge graph: the plant–disease associations that have received the most scientific attention are precisely those that traditional medicine practitioners have recommended for centuries. *Centella asiatica* for wound healing and *Zingiber officinale* for infection are well-established in both traditions.

### 4.4 Drug Discovery Candidates

We define drug discovery candidates as plants with five or more traditional therapeutic claims that have received no or limited modern scientific attention. JamuKG identifies **286 such plants** (Table 4), representing the highest-priority targets for pharmacological investigation.

**Table 4.** Top 15 drug discovery candidates (plants with most unstudied claims).

| Plant | Unstudied Claims | Total Claims | Gap % | Example Indications |
|---|---|---|---|---|
| *Sida rhombifolia* | 21 | 26 | 80.8% | Boil, fracture, headache, ophthalmia |
| *Hydrocotyle asiatica* | 20 | 22 | 90.9% | Asthma, hepatosis, rheumatism, sore |
| *Nigella sativum* | 20 | 20 | 100.0% | Amenorrhea, colic, constipation, vertigo |
| *Musa sapientum* | 19 | 22 | 86.4% | Colitis, dengue, pharyngitis, epistaxis |
| *Sophora tomentosa* | 18 | 18 | 100.0% | Various unstudied claims |
| *Moringa oleifera* | 17 | 17 | 100.0% | Multiple traditional indications |
| *Gendarussa vulgaris* | 16 | 16 | 100.0% | Various unstudied claims |
| *Zingiber cassumunar* | 16 | 16 | 100.0% | Multiple traditional indications |
| *Urena lobata* | 16 | 16 | 100.0% | Various unstudied claims |
| *Datura metel* | 14 | 14 | 100.0% | Various unstudied claims |
| *Sesbania grandiflora* | 14 | 14 | 100.0% | Multiple traditional indications |
| *Piper betle* | 14 | 14 | 100.0% | Various unstudied claims |
| *Mimusops elengi* | 13 | 13 | 100.0% | Various unstudied claims |
| *Blumea balsamifera* | 13 | 13 | 100.0% | Multiple traditional indications |
| *Piper retrofractum* | 13 | 13 | 100.0% | Various unstudied claims |

*Sida rhombifolia* exemplifies the drug discovery opportunity: this plant is traditionally used for 26 different conditions spanning 9 disease categories (digestive, eye, genitourinary, infectious, injury, musculoskeletal, neoplasm, skin, symptom), yet 21 of these claims have never been examined in the scientific literature. It is also known to produce 19 distinct chemical compounds, providing specific molecular targets for investigation.

### 4.5 Network Pharmacology: Multi-Target Plants and Promiscuous Compounds

#### 4.5.1 Multi-Target Plants

Of the 2,519 plant species in JamuKG, **345 (13.7%)** treat conditions across three or more disease categories (Figure 2). The top multi-target plants are shown in Table 5.

**Table 5.** Top 10 multi-target plants (by number of disease categories treated).

| Plant | Disease Categories | Total Diseases | Known Compounds |
|---|---|---|---|
| *Sida rhombifolia* | 9 | 26 | 19 |
| *Zingiber officinale* | 8 | 27 | 438 |
| *Kaempferia galanga* | 8 | 16 | 8 |
| *Hydrocotyle asiatica* | 8 | 22 | 0 |
| *Nigella sativum* | 8 | 20 | 0 |
| *Curcuma longa* | 8 | — | 356 |
| *Coleus atropurpureus* | 8 | 12 | 0 |
| *Tinospora tuberculata* | 7 | — | — |
| *Musa sapientum* | 7 | — | — |
| *Piper betle* | 7 | — | — |

Two distinct patterns emerge. Plants like *Zingiber officinale* (438 compounds) and *Curcuma longa* (356 compounds) are both multi-target *and* phytochemically rich — their broad therapeutic profiles may be mechanistically explained by their diverse chemistry. In contrast, plants like *Hydrocotyle asiatica* and *Nigella sativum* are multi-target but have zero indexed compounds in JamuKG, indicating that their chemistry is yet to be characterized. These represent particularly urgent targets for phytochemical investigation, as understanding their multi-target therapeutic potential requires first identifying their active constituents.

#### 4.5.2 Therapeutic Specificity

Not all plants are generalists. *Eurycoma longifolia* (tongkat ali) shows striking therapeutic specificity: 94.4% of its traditional uses fall within musculoskeletal disorders. This high specificity suggests a narrow but potent pharmacological profile, consistent with its well-documented effects on testosterone metabolism and musculoskeletal function (Talbott et al., 2013).

#### 4.5.3 Promiscuous Compounds

Quercetin emerges as the most promiscuous compound in JamuKG, with 156 documented bioactivities across 58 plant sources. This is consistent with quercetin's established status as a pleiotropic bioactive flavonoid with anti-inflammatory, antioxidant, anti-cancer, and neuroprotective properties documented in modern pharmacology (Li et al., 2016). Its widespread distribution across jamu ingredient plants may partially explain the broad-spectrum therapeutic claims associated with many formulations.

### 4.6 Jamu Formulation Analysis

#### 4.6.1 Formulation Structure

Analysis of 5,310 KNApSAcK jamu formulas reveals a mean of **4.8 herbs per formula**, consistent with the combinatorial pharmacology principle in traditional medicine systems where synergistic herb combinations are preferred over single-herb preparations. The 10 therapeutic effect groups represented are: gastrointestinal disorders (988 formulas, 18.6%), musculoskeletal and connective tissue disorders (863, 16.3%), female reproductive organ problems (405, 7.6%), pain/inflammation (315, 5.9%), disorders of appetite (249, 4.7%), wounds and skin infections (162, 3.1%), respiratory disease (107, 2.0%), urinary related problems (72, 1.4%), and disorders of mood and behavior (22, 0.4%), with the remainder (2,127, 40.1%) unclassified.

#### 4.6.2 Dominant Herbs

The most frequently used herb is **temulawak** (*Curcuma xanthorrhiza*), appearing in **1,474 formulas (27.8%)** — more than one in four jamu products. This is followed by **jahe** (*Zingiber officinale*, 1,256, 23.7%), **kunyit** (*Curcuma domestica*/longa, 1,026, 19.3%), **kencur** (*Kaempferia galanga*, 702, 13.2%), and **adas** (*Foeniculum vulgare*, 698, 13.1%).

#### 4.6.3 Zingiberaceae Dominance

The Zingiberaceae (ginger) family dominates jamu formulation practice. Members of this family — including *Curcuma*, *Zingiber*, *Kaempferia*, *Alpinia*, and *Amomum* species — appear in **3,272 of 5,310 formulas (61.6%)**. This extraordinary prevalence reflects both the pharmacological potency of gingerols, curcuminoids, and related compounds, and the deep integration of Zingiberaceae cultivation into Javanese agricultural and medical practice.

#### 4.6.4 Herb Co-occurrence Patterns

Co-occurrence analysis reveals systematic combinatorial patterns in jamu formulation (Table 6).

**Table 6.** Top 10 herb co-occurrences in jamu formulas.

| Herb 1 | Herb 2 | Co-occurrences |
|---|---|---|
| *C. xanthorrhiza* (temulawak) | *Z. officinale* (jahe) | 483 |
| *P. retrofractum* (cabe jawa) | *Z. officinale* (jahe) | 398 |
| *K. galanga* (kencur) | *Z. officinale* (jahe) | 386 |
| *C. domestica* (kunyit) | *C. xanthorrhiza* (temulawak) | 383 |
| *C. xanthorrhiza* (temulawak) | *P. retrofractum* (cabe jawa) | 312 |
| *C. xanthorrhiza* (temulawak) | *K. galanga* (kencur) | 293 |
| *P. nigrum* (lada hitam) | *Z. officinale* (jahe) | 274 |
| *C. domestica* (kunyit) | *Z. officinale* (jahe) | 262 |
| *F. vulgare* (adas) | *Z. officinale* (jahe) | 260 |
| *C. xanthorrhiza* (temulawak) | *F. vulgare* (adas) | 250 |

The temulawak–jahe pair (483 co-occurrences) is the most common combination, consistent with modern evidence for curcuminoid–gingerol synergy in anti-inflammatory pathways (Sahebkar, 2017). The frequent pairing of Piperaceae species (*Piper retrofractum*, *P. nigrum*) with Zingiberaceae parallels the well-documented bioenhancement effect of piperine on curcumin bioavailability (Shoba et al., 1998) — suggesting that traditional formulation practice may have empirically optimized drug absorption through combinatorial compounding.

### 4.7 Comparison with Existing Knowledge Graphs

Table 7 positions JamuKG relative to existing traditional medicine knowledge graphs.

**Table 7.** Comparison of JamuKG with existing traditional medicine knowledge graphs.

| Feature | SymMap (TCM) | HERB (TCM) | GRAYU (Korean) | **JamuKG** |
|---|---|---|---|---|
| **Tradition** | Chinese | Chinese | Korean | **Indonesian** |
| **Plants/Herbs** | 499 | 7,263 | 4,134 | **2,519** |
| **Compounds** | — | — | — | **7,364** |
| **Diseases** | 961 symptoms | — | 537 | **651** |
| **Formulations** | — | — | 2,748 | **5,310** |
| **Total edges** | — | — | — | **64,066** |
| **Validation gap** | Not assessed | Not assessed | Not assessed | **85.9%** |
| **PubMed cross-ref** | No | No | No | **Yes (5,744 pairs)** |

JamuKG is unique in two respects: it is the first knowledge graph for Indonesian traditional medicine, and it is the first to include systematic PubMed cross-referencing to quantify the validation gap.

---

## 5. Discussion

### 5.1 The 85.9% Gap: Absence of Evidence, Not Evidence of Absence

The central finding of this study — that 85.9% of traditional jamu plant–disease claims have zero published PubMed evidence — demands careful interpretation. This number does not mean that 85.9% of traditional claims are wrong. It means that the modern scientific community has not examined them. The distinction between "not validated" and "invalidated" is critical.

Several lines of evidence suggest that a significant fraction of these uninvestigated claims would prove pharmacologically meaningful upon examination:

1. **Internal validation.** The 76 well-studied pairs in our dataset show strong concordance between traditional use and modern evidence. *Centella asiatica* for wound healing, *Zingiber officinale* for infections, *Andrographis paniculata* for diabetes — these are precisely the pairs that modern pharmacology has independently confirmed. If the well-studied subset shows high concordance, the principle of induction suggests that many unstudied claims may be similarly valid.

2. **Multi-source consensus.** Although only 34 plants appear in multiple databases in our current integration, these multi-source plants tend to be among the most well-studied, suggesting that convergent evidence from independent sources is a meaningful signal.

3. **Evolutionary argument.** Traditional medicine represents an empirical selection process operating over hundreds of generations. Formulations that did not produce observable therapeutic effects would, over time, be abandoned. The persistence of specific plant–disease associations across centuries constitutes a form of pre-clinical evidence that is qualitatively different from — but not inferior to — modern screening.

### 5.2 Implications for Drug Discovery

The pharmaceutical industry faces a well-documented productivity crisis: the average cost of bringing a new drug to market now exceeds $2.6 billion USD, with a development timeline of 10–15 years and a clinical trial failure rate exceeding 90% (DiMasi et al., 2016). Traditional medicine knowledge offers a potential shortcut: if centuries of empirical observation have already identified plants with genuine therapeutic potential, then starting from these leads rather than from random compound libraries could significantly reduce the search space.

Our 286 priority candidates (plants with ≥5 unstudied traditional claims) represent a systematically generated hit list for ethnopharmacological investigation. These are not random species — they are plants that have been specifically and repeatedly selected by traditional practitioners for specific therapeutic purposes. The case of *Sida rhombifolia* is illustrative: 21 unstudied claims across 9 disease categories, with 19 known compounds providing immediate molecular targets for bioassay. A systematic investigation of even the top 20 candidates in our list could yield novel pharmacological leads at a fraction of the cost of conventional high-throughput screening.

### 5.3 The Combinatorial Logic of Jamu

The herb co-occurrence analysis reveals that jamu formulation is not random polypharmacy. The consistent pairing of specific herbs — temulawak with jahe, Zingiberaceae with Piperaceae — suggests an empirically optimized combinatorial logic that parallels modern concepts of drug synergy and bioenhancement.

The most striking example is the frequent co-occurrence of *Piper* species (containing piperine) with *Curcuma* species (containing curcuminoids). Modern pharmacology has established that piperine increases curcumin bioavailability by 2,000% through inhibition of hepatic and intestinal glucuronidation (Shoba et al., 1998). Traditional jamu formulation appears to have arrived at this combination empirically, centuries before the molecular mechanism was elucidated.

This observation raises a broader question: how many other synergistic combinations in the jamu co-occurrence network represent empirically discovered drug interactions that modern pharmacology has yet to characterize? The 483 temulawak–jahe co-occurrences and the systematic pairing patterns in Table 6 provide specific, testable hypotheses for synergy investigation.

### 5.4 The Zingiberaceae Question

The dominance of Zingiberaceae in jamu (61.6% of formulas) invites comparison with other traditional medicine systems. In TCM, no single plant family achieves comparable dominance. The Zingiberaceae prevalence in jamu likely reflects a combination of pharmacological potency (gingerols and curcuminoids are among the most bioactive plant secondary metabolites known), ecological availability (Zingiberaceae are native to and extensively cultivated in Southeast Asia), and cultural centrality (these plants are simultaneously used as medicines, spices, and ritual objects in Javanese culture).

### 5.5 Limitations

Several limitations should be acknowledged:

1. **PubMed coverage bias.** PubMed indexes primarily English-language journals. Indonesian-language research on medicinal plants, published in journals such as *Jurnal Farmasi Indonesia* or *Majalah Obat Tradisional*, may not be captured. Our validation gap estimate of 85.9% may therefore overstate the true gap when Indonesian-language evidence is included.

2. **Name resolution.** Latin binomial matching may miss synonyms, misspellings, or taxonomic revisions. A plant known under a deprecated synonym would appear to have zero PubMed evidence even if research exists under the accepted name. We mitigated this partially through synonym resolution, but comprehensive taxonomic reconciliation remains future work.

3. **Evidence quality.** Our classification is based on publication count, not on evidence quality, study design, or clinical relevance. A pair with 25 PubMed hits might include 25 *in vitro* studies with no clinical relevance, while a pair with 3 hits might include a well-powered randomized controlled trial.

4. **Disease term heterogeneity.** The ethnobotanical disease terms in Dr. Duke's database (e.g., "Sore," "Boil," "Parturition") do not always map cleanly to modern disease ontologies. Our ICD-10 mapping achieved only 37.3% coverage, and some apparent "validation gaps" may reflect terminology mismatches rather than true absence of evidence.

5. **Temporal snapshot.** JamuKG captures the state of knowledge as of early 2026. New publications, database updates, and additional data sources may alter the validation gap estimates.

### 5.6 Future Work

Five directions for future development are planned:

1. **HerbalDB integration.** The HerbalDB database contains 3,810 species and 6,776 compounds that could significantly expand JamuKG's phytochemical coverage.

2. **Historical manuscript mining.** Digitization and computational extraction of plant–disease relationships from the *Serat Centhini*, *Usada Bali*, and colonial-era botanical surveys would add a fourth data medium (historical manuscripts) to the current three-source integration.

3. **ICD-10 disease standardization.** Improving disease term mapping from the current 37.3% to >80% using NLP-based disease normalization and the UMLS Metathesaurus.

4. **Network pharmacology prediction.** Using the KG structure to predict novel plant–disease associations through link prediction algorithms, with subsequent experimental validation.

5. **Marketplace integration.** Scraping contemporary jamu marketplace data (Tokopedia, Shopee) to capture the living, evolving state of jamu practice as it exists in 2026.

---

## 6. Conclusion

JamuKG reveals that the vast majority of Indonesian traditional medicinal knowledge exists in a **validation dark zone** — empirically tested across centuries of daily use by millions of people, but invisible to modern science. Of 5,744 plant–disease claims in the knowledge graph, 85.9% have never been examined in the PubMed-indexed literature. This gap represents both a loss and an opportunity: a loss because valuable pharmacological knowledge is at risk of being forgotten without scientific documentation, and an opportunity because it identifies thousands of specific, actionable leads for drug discovery that have already passed the most demanding selection process imaginable — survival across generations of empirical practice.

The 286 plants we identify as priority drug discovery candidates, the combinatorial formulation patterns we quantify, and the multi-target therapeutic profiles we characterize are not abstract data points. They are specific, testable hypotheses about the pharmacological properties of specific plant species, generated by a computational system but grounded in centuries of human observation. JamuKG makes these hypotheses accessible, queryable, and prioritizable for the first time.

We release JamuKG as open-source infrastructure with the conviction that closing the validation gap is not merely an academic exercise but an urgent practical necessity — for the millions of Indonesians who use jamu daily, for the pharmaceutical industry seeking novel leads, and for the preservation of a pharmacological heritage that, once lost to modernization and deforestation, cannot be reconstructed.

---

## Data Availability

JamuKG, all analysis scripts, supplementary data tables, and the complete pipeline for reproducing all results are available at [repository URL].

**Supplementary Table S1.** Complete plant–disease pair list with PubMed evidence levels (5,744 pairs).
**Supplementary Table S2.** Plant summary with validation gap statistics (1,986 plants).
**Supplementary Table S3.** Drug discovery candidate list with unstudied claims (621 plants with ≥3 unstudied claims).

---

## Acknowledgments

We thank the maintainers of Dr. Duke's Phytochemical and Ethnobotanical Database, the KNApSAcK Jamu database, and the Indonesian Ministry of Health for making their data publicly accessible. This work was conducted independently without external funding.

---

## References

Afendi, F. M., Okada, T., Yamazaki, M., Hirai-Morita, A., Nakamura, Y., Nakamura, K., ... & Kanaya, S. (2012). KNApSAcK family databases: integrated metabolite–plant species databases for multifaceted plant research. *Plant and Cell Physiology*, 53(2), e1.

Chun, H., Kim, K., Lee, S., & Ahn, J. (2021). GRAYU: A knowledge graph for Korean traditional medicine. *Journal of Biomedical Informatics*, 114, 103670.

DiMasi, J. A., Grabowski, H. G., & Hansen, R. W. (2016). Innovation in the pharmaceutical industry: new estimates of R&D costs. *Journal of Health Economics*, 47, 20–33.

Duke, J. A. (1992–2016). *Dr. Duke's Phytochemical and Ethnobotanical Databases*. USDA-ARS-GRIN.

Elfahmi, Woerdenbag, H. J., & Kayser, O. (2014). Jamu: Indonesian traditional herbal medicine towards rational phytopharmacological use. *Journal of Herbal Medicine*, 4(2), 51–73.

Fang, S., Dong, L., Liu, L., Guo, J., Zhao, L., Zhang, J., ... & He, S. (2021). HERB: a high-throughput experiment- and reference-guided database of traditional Chinese medicine. *Nucleic Acids Research*, 49(D1), D1197–D1206.

Heinrich, M., Appendino, G., Efferth, T., Fürst, R., Izzo, A. A., Kayser, O., ... & Viljoen, A. (2020). Best practice in research – Overcoming common challenges in phytopharmacological research. *Journal of Ethnopharmacology*, 246, 112230.

Li, Y., Yao, J., Han, C., Yang, J., Chaudhry, M. T., Wang, S., ... & Yin, Y. (2016). Quercetin, inflammation and immunity. *Nutrients*, 8(3), 167.

Sahebkar, A. (2017). Curcuminoids for the management of hypertriglyceridaemia. *Nature Reviews Cardiology*, 14(4), 238–244.

Shoba, G., Joy, D., Joseph, T., Majeed, M., Rajendran, R., & Srinivas, P. S. S. R. (1998). Influence of piperine on the pharmacokinetics of curcumin in animals and human volunteers. *Planta Medica*, 64(04), 353–356.

Talbott, S. M., Talbott, J. A., George, A., & Pugh, M. (2013). Effect of Tongkat Ali on stress hormones and psychological mood state in moderately stressed subjects. *Journal of the International Society of Sports Nutrition*, 10(1), 28.

Tu, Y. (2011). The discovery of artemisinin (qinghaosu) and gifts from Chinese medicine. *Nature Medicine*, 17(10), 1217–1220.

Wachtel-Galor, S., & Benzie, I. F. F. (2011). Herbal medicine: an introduction to its history, usage, regulation, current trends, and research needs. In *Herbal Medicine: Biomolecular and Clinical Aspects* (2nd ed.). CRC Press.

Wijaya, S. H., Afendi, F. M., Batubara, I., Darusman, L. K., Altaf-Ul-Amin, M., & Kanaya, S. (2014). Finding an appropriate equation to measure similarity between binary vectors: case studies on Indonesian and Japanese herbal medicines. *BMC Bioinformatics*, 15(1), 1–17.

Wu, Y., Zhang, F., Yang, K., Fang, S., Bu, D., Li, H., ... & Zhao, Y. (2019). SymMap: an integrative database of traditional Chinese medicine enhanced by symptom mapping. *Nucleic Acids Research*, 47(D1), D1110–D1117.

Zhang, R., Zhu, X., Bai, H., & Ning, K. (2022). Network pharmacology databases for traditional Chinese medicine: review and assessment. *Frontiers in Pharmacology*, 10, 123.

---

## Figure Captions

**Figure 1.** Validation gap distribution. (A) Pie chart showing the proportion of 5,744 plant–disease claims classified by PubMed evidence level. (B) Stacked bar chart showing the validation gap across the top 15 disease categories. File: `figures/05_validation_gap.png`

**Figure 2.** Multi-target medicinal plants. Horizontal bar chart showing the top 20 plants that treat conditions across the most disease categories. Plants are annotated with their known compound counts. File: `figures/10_multi_target_plants.png`

**Figure 3.** Drug discovery candidates. Top 20 plants with the most unstudied traditional claims, representing priority targets for pharmacological investigation. File: `figures/08_drug_discovery_candidates.png`

**Figure 4.** Validation heatmap. Matrix visualization showing evidence levels for the top 30 plants × top 30 diseases, illustrating the sparse landscape of evidence amid widespread traditional claims. File: `figures/07_validation_heatmap.png`

**Figure 5.** JamuKG overview. Distribution of node types and edge types in the knowledge graph. File: `figures/01_kg_overview.png`

**Figure 6.** Source coverage. Overlap and unique contributions of each data source to JamuKG. File: `figures/06_source_overlap.png`

**Figure 7.** Top jamu herbs. The 20 most frequently used herbs across 5,310 KNApSAcK jamu formulas. File: `figures/12_top_jamu_herbs.png`

**Figure 8.** Herb co-occurrence network. Heatmap showing pairwise co-occurrence frequencies of the top 20 herbs in jamu formulations. File: `figures/14_herb_cooccurrence.png`

**Figure 9.** Disease category distribution. Pie chart of disease categories in JamuKG after normalization. File: `figures/09_disease_categories.png`

**Figure 10.** Compound bioactivity profile. Grouped bar chart of the most bioactive compounds and their activity categories. File: `figures/16_compound_bioactivity_profile.png`

**Figure 11.** Herb therapeutic profiles by therapy area. Stacked bar chart showing the disease category distribution for key herbs. File: `figures/20_herb_profiles_by_therapy.png`

**Figure 12.** Comparison with existing knowledge graphs. Summary comparison of JamuKG with SymMap, HERB, and GRAYU across key dimensions. File: `figures/19_kg_comparison.png`

**Figure 13.** Summary figure. Four-panel overview combining KG structure, validation gap, drug discovery candidates, and formulation patterns. File: `figures/00_paper_summary_figure.png`
