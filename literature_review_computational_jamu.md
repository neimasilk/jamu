# Literature Review: Computational & NLP Research on Indonesian Traditional Medicine (Jamu)

**Date:** 2026-03-17
**Purpose:** Identify what has already been done so we do not reinvent the wheel.

---

## 1. Existing NLP / Computational Work Directly on Jamu

### 1.1 The Landmark Review: AI for Jamu Drug Development

**Paper:** "Application of artificial intelligence in the development of Jamu 'traditional Indonesian medicine' as a more effective drug"
**Authors:** Yanuar et al.
**Year:** 2023
**Venue:** Frontiers in Artificial Intelligence, Vol. 6 (doi: 10.3389/frai.2023.1274975)
**URL:** https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2023.1274975/full

**Key findings:**
- Six thousand plant species used empirically by ~40 million Indonesians
- AI can shorten the 10-15 year / US$2.8B drug development pipeline
- Stages: database identification and data mining -> AI technique -> systematic review of proven drugs
- NLP is identified as a key AI tool (sentiment analysis, NER, machine translation, text summarization)
- Drug-target interaction (DTI) prediction using ML/DL is proposed for Jamu formulas

**What we can reuse:** This is the strategic roadmap. Our KG work fits squarely into their "database identification and data mining" stage. The review validates the approach but does NOT actually build an NLP pipeline or KG -- that gap is ours to fill.

---

### 1.2 KNApSAcK Jamu Database & Network Analysis

**Paper:** "Supervised Clustering Based on DPClusO: Prediction of Plant-Disease Relations Using Jamu Formulas of KNApSAcK Database"
**Authors:** Wijaya, Husnawati, Afendi et al.
**Year:** 2014
**Venue:** BioMed Research International (doi: 10.1155/2014/831751)
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC3997850/

**Key findings:**
- Assigned 3,138 Jamu formulas to 116 ICD-10 diseases across 18 disease classes
- Built Jamu network based on ingredient similarity
- Used DPClusO network clustering algorithm
- ~90% successful prediction rate for plant-disease relations

**Related work by Afendi et al.:**
- Efficacy prediction of Jamu formulations by PLS modeling
- Statistical methods: biplot, partial least squares, bootstrapping

**What we can reuse:** The KNApSAcK database itself is a critical existing resource. The 3,138 formulas mapped to ICD-10 codes are directly useful as seed data for our KG. Their network structure (ingredient similarity) is a proven approach we should replicate.

---

### 1.3 Bipartite Graph Optimization for Jamu Formulation

**Paper:** "Bipartite graph search optimization for type II diabetes mellitus Jamu formulation using branch and bound algorithm"
**Authors:** Kusuma, Habibi, Amir, Fadli, Khotimah, Dewanto, Heryanto
**Year:** 2022
**Venue:** Frontiers in Pharmacology, Vol. 13 (doi: 10.3389/fphar.2022.978741)
**URL:** https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2022.978741/full

**Key findings:**
- Models Jamu as plant-protein bipartite graph
- Branch-and-bound with BrFS/DFS/BestFS reduces computation time 40x vs complete search
- Identified 4-plant combination for T2DM: Angelica Sinensis, Citrus aurantium, Glycyrrhiza uralensis, Mangifera indica

**What we can reuse:** The bipartite graph representation (plants <-> proteins/targets) is directly relevant to our KG schema. Their approach demonstrates that graph-based reasoning over Jamu data produces actionable pharmacological predictions.

---

### 1.4 Indonesian Traditional Medicine Ontologies

**Paper:** "Finding Knowledge from Indonesian Traditional Medicine using Semantic Web Rule Language"
**Authors:** Gunawan & Mustofa
**Year:** 2017
**Venue:** International Journal of Electrical and Computer Engineering (IJECE), Vol. 8, No. 5
**URL:** https://ijece.iaescore.com/index.php/IJECE/article/view/8737

**Key findings:**
- Built ontology describing: Jamu products, plants used, plant parts, composition, properties
- Used SWRL rules on top of OWL ontology
- Created RDF knowledge base using Ontology Application Management (OAM) software
- Web interface for querying

**Paper:** "Evaluation of Indonesian Traditional Herbal Medicine Ontology Quality"
**Authors:** Surendro, Yodihartomo, Yulianti
**Year:** 2020
**Venue:** International Journal on Electrical Engineering and Informatics, Vol. 12(1), pp. 72-81
**URL:** https://www.academia.edu/66990877/Evaluation_of_Indonesian_Traditional_Herbal_Medicine_Ontology_Quality

**Paper:** "Analysis and Design of Indonesian Traditional Medicine Knowledge System"
**Year:** 2024
**URL:** https://www.e3s-conferences.org/articles/e3sconf/pdf/2024/13/e3sconf_isst2024_03012.pdf

**What we can reuse:** Existing ontology schemas give us a starting vocabulary and relation types. However, these ontologies are described as covering "only a fraction of domain knowledge." Our KG can build on and extend these foundations.

---

### 1.5 HerbalDB: Indonesian Compound Database

**Paper:** "HerbalDB 2.0: Optimization of Construction of Three-Dimensional Chemical Compound Structures to Update Indonesian Medicinal Plant Database"
**Year:** Various (latest version 2.0)
**URL:** https://www.phcogj.com/article/1001

**Key findings:**
- Contains 1,405 Indonesian herbal compounds with 3D structures
- Identified and corrected 170 compounds with structural mismatches
- Serves as the chemical structure backbone for Jamu research

**What we can reuse:** Direct chemical compound data for populating the molecular layer of our KG.

---

### 1.6 RISTOJA: National Ethnobotany Survey

**Full name:** Riset Tumbuhan Obat dan Jamu (Research on Medicinal Plants and Jamu)
**Conducted by:** Health Research and Development Agency (Balitbangkes), Indonesia
**Year:** 2012-2017
**URL:** https://repository.badankebijakan.kemkes.go.id/id/eprint/4740/

**Key findings:**
- Collected 32,014 medicinal plant entries from 405 ethnic groups across 34 provinces
- Contains ethnopharmacological knowledge, traditional medicine formulas, medicinal plant data
- ACCESS RESTRICTION: Data not publicly open; requires formal proposal to NIHRD

**What we can reuse:** If we can obtain access, this is the single richest source of Indonesian ethnobotanical text data. Without access, we need alternative text sources (Jurnal Jamu Indonesia, ethnobotany papers, BPOM registrations).

---

## 2. Knowledge Graphs for Traditional Medicine (Other Traditions)

### 2.1 TCM Databases: The Gold Standard Ecosystem

| Database | Focus | Scale | Key Feature |
|----------|-------|-------|-------------|
| **TCMSP** | TCM pharmacology | Ingredients, targets, diseases | Foundational DB (pre-2014) |
| **SymMap** | Symptom mapping | 1,717 TCM symptoms, 499 herbs, 961 modern symptoms, 19,595 constituents, 4,302 targets, 20,965 targets total | Bridges TCM and modern medicine at phenotypic + molecular levels |
| **BATMAN-TCM** | Target prediction | Herbs, compounds, targets | Intelligent pharmacological research platform |
| **HERB** | Integration | Integrates most other TCM DBs | Meta-database |
| **TCMM** | Modernization | Unified DB | Latest unified effort |

**SymMap reference:** Wu et al. (2019) "SymMap: an integrative database of traditional Chinese medicine enhanced by symptom mapping." Nucleic Acids Research, 47(D1), D1110. doi: 10.1093/nar/gky1021
**URL:** https://academic.oup.com/nar/article/47/D1/D1110/5150228

**Critical assessment:** "A critical assessment of Traditional Chinese Medicine databases as a source for drug discovery" (2024), Frontiers in Pharmacology. doi: 10.3389/fphar.2024.1303693
**URL:** https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2024.1303693/full

**What we can learn:** The TCM ecosystem shows us what "done well" looks like. SymMap's key innovation -- mapping traditional symptom descriptions to modern medical terminology -- is exactly what we need for Jamu. The multi-layered architecture (herbs -> chemicals -> targets -> diseases) is the proven schema.

---

### 2.2 HerbKG: The NLP-First Approach (Most Relevant to Us)

**Paper:** "HerbKG: Constructing a Herbal-Molecular Medicine Knowledge Graph Using a Two-Stage Framework Based on Deep Transfer Learning"
**Authors:** Not specified in search results
**Year:** 2022
**Venue:** Frontiers in Genetics (doi: 10.3389/fgene.2022.799349)
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9091197/

**Key findings:**
- **Two-stage pipeline:** Stage I = NER (using PubTator Central), Stage II = Relation Extraction (custom BERT model)
- Screened PubMed abstracts containing mentions of herbs/chemicals from a pre-defined domain vocabulary
- Processed 500K+ PubMed abstracts
- Result: 53K relations in the KG
- Entities: herbs, chemicals, genes, diseases
- Boosting strategies: fine-tuning BERT on domain resources + generative data augmentation

**THIS IS THE CLOSEST METHODOLOGICAL TEMPLATE FOR OUR WORK.** The pipeline is:
1. Define domain vocabulary (herb names, chemical names)
2. Screen literature for relevant abstracts
3. Run NER to identify entities
4. Run RE to extract relation triples
5. Populate KG

**What we must adapt:** Their pipeline uses English PubMed. We need to handle Indonesian-language texts. Their NER uses PubTator Central (English-only). We need IndoBERT/NusaBERT-based NER.

---

### 2.3 OpenTCM: GraphRAG + LLM (Cutting Edge, 2025)

**Paper:** "OpenTCM: A GraphRAG-Empowered LLM-based System for Traditional Chinese Medicine Knowledge Retrieval and Diagnosis"
**Authors:** He, Guo et al.
**Year:** 2025
**Venue:** BIGCOM25 (Best Paper Award)
**URL:** https://arxiv.org/abs/2504.20118
**GitHub:** https://github.com/XY1123-TCM/OpenTCM

**Key findings:**
- Extracted 3.73 million ancient Chinese characters from 68 gynecological books
- KG: 48,000+ entities, 152,000+ relationships (3,700+ herbs, 14,000+ diseases, 17,000+ symptoms)
- Used DeepSeek and Kimi LLMs with customized prompts + human expert annotation
- GraphRAG enables training-free LLM framework
- Precision improved from 94.6% to 98.55%

**What we can reuse:** The LLM-based extraction approach is particularly relevant for a solo researcher -- it reduces the need for large annotated training datasets. GraphRAG for downstream querying is the state of the art.

---

### 2.4 TCM Knowledge Graph Construction Methods (Survey)

**Paper:** "A Review of Knowledge Graph in Traditional Chinese Medicine"
**Year:** 2024
**URL:** https://cdn.techscience.cn/files/cmc/2024/online/CMC1022/TSP_CMC_55671/TSP_CMC_55671.pdf

**Key methods documented:**
- **NER:** CRF with character n-grams, Kangxi radicals, POS tags, BMES labels, gazetteer matching; BiLSTM-CRF; BERT-BiLSTM-CRF
- **RE:** Neural dependency parsing (biaffine architecture, BiLSTM encoders, pretrained TCM embeddings)
- **LLM-based:** DeepSeek/Kimi with customized prompts + JSON output + human expert validation

---

### 2.5 GRAYU: Ayurveda Knowledge Graph (2025)

**Paper:** "GRAYU: graph-based database integrating Ayurvedic formulations, medicinal plants, phytochemicals and diseases"
**Year:** 2025
**Venue:** Frontiers in Pharmacology (doi: 10.3389/fphar.2025.1727224)
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12872832/
**Access:** https://caps.ncbs.res.in/GRAYU/

**Key findings:**
- 157,010 nodes, 1,520,687 relationships
- Integrates: 1,039 formulations, 12,743 plants, 129,542 phytochemicals, 13,480 diseases
- Relationship breakdown: 1,370,257 plant-phytochemical, 116,531 plant-disease, 2,389 plant-formulation, 4,087 formulation-disease
- Maps Ayurvedic nosology to modern disease ontologies (ICD/MeSH)
- Interactive graph visualization + advanced search

**What we can reuse:** GRAYU is the closest structural analog to what we want to build for Jamu. Their schema (formulations <-> plants <-> phytochemicals <-> diseases) maps directly. Their approach to nosology mapping (traditional -> modern) is exactly what we need.

---

### 2.6 IMPPAT: Indian Medicinal Plants Database

**Paper:** "IMPPAT 2.0: An Enhanced and Expanded Phytochemical Atlas of Indian Medicinal Plants"
**Year:** 2023
**Venue:** ACS Omega
**URL:** https://pubs.acs.org/doi/10.1021/acsomega.3c00156
**GitHub:** https://github.com/asamallab/IMPPAT2
**Access:** https://cb.imsc.res.in/imppat/

**Key findings:**
- 4,010 Indian medicinal plants, 17,967 phytochemicals, 1,095 therapeutic uses
- Manually curated from 100+ books + 7,000+ research articles
- Includes 2D/3D structures, physicochemical properties, drug-likeness scores, ADMET predictions
- Phytochemical info provided at plant-part level

**What we can reuse:** The curation methodology (books + papers -> structured DB) and the inclusion of computed properties (drug-likeness, ADMET) as an enrichment layer. Their GitHub repo may have reusable data processing scripts.

---

### 2.7 African Traditional Medicine

**Paper:** "Conceptual graph-based knowledge representation for supporting reasoning in African traditional medicine"
**Authors:** Kamsu-Foguem, Diallo et al.
**Year:** 2013
**Venue:** Engineering Applications of Artificial Intelligence
**URL:** https://www.sciencedirect.com/science/article/abs/pii/S0952197612003120

**Paper:** "Toward a Knowledge-Based System for African Traditional Herbal Medicine: A Design Science Research Approach"
**Year:** 2022
**Venue:** PMC (doi: various)
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8959699/

**Key findings:**
- Hybrid knowledge model: ML + ontology-based techniques
- Conceptual graphs for reasoning
- Challenges similar to ours: oral traditions, multilingual, sparse digital records

---

## 3. Indonesian NLP Model Landscape

### 3.1 IndoBERT

**Paper:** "IndoLEM and IndoBERT: A Benchmark Dataset and Pre-trained Language Model for Indonesian NLP"
**Authors:** Koto, Rahimi, Lau, Baldwin
**Year:** 2020
**Venue:** COLING 2020
**URL:** https://aclanthology.org/2020.coling-main.66/
**HuggingFace:** https://huggingface.co/indolem/indobert-base-uncased

**Key findings:**
- Trained on 220M+ words, 2.4M steps (180 epochs)
- Final perplexity: 3.97
- State-of-the-art on IndoLEM benchmark (morpho-syntax, semantics, discourse)

### 3.2 NusaBERT

**Paper:** "NusaBERT: Teaching IndoBERT to be Multilingual and Multicultural"
**Authors:** Wongso, Setiawan et al.
**Year:** 2024
**Venue:** arXiv (2403.01817)
**URL:** https://arxiv.org/html/2403.01817v1
**GitHub:** https://github.com/LazarusNLP/NusaBERT

**Key findings:**
- Extends IndoBERT with vocabulary expansion + diverse multilingual corpus
- Pre-training corpus: 13 languages (CulturaX, Wikipedia, KoPI-NLLB)
- State-of-the-art for multilingual Indonesian local language tasks
- **Includes Javanese** in training data

### 3.3 Indonesian NER Models

**HuggingFace:** https://huggingface.co/cahya/bert-base-indonesian-NER
- 3 fine-tuned variants available
- General-domain NER (person, location, organization), NOT biomedical

**Paper:** "Named entity recognition in the medical domain for Indonesian language health consultation services using bidirectional-lstm-crf algorithm"
**Year:** 2024
**Venue:** ScienceDirect (Procedia Computer Science)
**URL:** https://www.sciencedirect.com/science/article/pii/S1877050924031521

**Key findings:**
- BiLSTM-CRF on medical consultation data
- Accuracy: 0.9968
- Entities: anatomical entities, proteins, genes (in Indonesian text)

### 3.4 Cendol: Instruction-Tuned LLM for Indonesian Languages

**Paper:** "Cendol: Open Instruction-tuned Generative Large Language Models for Indonesian Languages"
**Year:** 2024
**URL:** https://arxiv.org/html/2404.06138v1

**Key findings:**
- Decoder-only and encoder-decoder architectures
- Large-scale instruction-tuning dataset for Indonesian + local languages
- Covers multiple Indonesian regional languages

### 3.5 Javanese Language Support

- **NusaBERT** includes Javanese
- **IndoJavE**: Pre-trained models for Indonesian-Javanese-English code-mixed text
- **NusaX corpus**: Parallel sentiment data across 10 local languages including Javanese
- **LoraxBench** (2025): Benchmark covering 20 Indonesian languages, 6 tasks
- **wav2vec2**: Multilingual speech recognition for Indonesian + Javanese + Sundanese

### 3.6 CRITICAL GAP: No Biomedical Indonesian BERT

**Finding:** There is NO published domain-specific biomedical/pharmacological Indonesian language model. The gap between:
- General Indonesian NER (cahya/bert-base-indonesian-NER) and
- English biomedical NER (BioBERT, PubMedBERT)

...has not been bridged. This is a significant opportunity and challenge for our work.

**Possible approach:** Fine-tune IndoBERT or NusaBERT on Indonesian biomedical/pharmacological text, or use multilingual BioBERT + Indonesian-specific fine-tuning.

---

## 4. Text Mining for Ethnopharmacology

### 4.1 Plant-Specific NLP Corpora

**Paper:** "Plant phenotype relationship corpus for biomedical relationships between plants and phenotypes"
**Year:** 2022
**Venue:** Scientific Data (Nature)
**URL:** https://www.nature.com/articles/s41597-022-01350-1

**Key findings:**
- 600 PubMed abstracts, 5,668 plant entities, 11,282 phenotype entities, 9,709 relationships
- Annotation: BRAT tool, mention-level + relation-level
- Plant NER: dictionary-based using NCBI Taxonomy (151,250 concepts, 315,173 terms)

**Paper:** "A corpus for plant-chemical relationships in the biomedical domain"
**Year:** 2016
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC5029005/

**Paper:** "A corpus of plant-disease relations in the biomedical domain"
**Year:** 2019
**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC6713337/

**What we can reuse:** These three corpora (plant-phenotype, plant-chemical, plant-disease) provide annotated training data for relation extraction models. Even though they are in English, they can bootstrap our RE model before domain adaptation.

### 4.2 Standard Pipeline Components

Based on the literature, the standard ethnopharmacology text mining pipeline is:

```
1. Corpus Assembly
   - PubMed/literature screening by keyword
   - Domain vocabulary for filtering

2. Named Entity Recognition
   - Dictionary-based: NCBI Taxonomy, ChemSpot, domain gazetteers
   - ML-based: BioBERT/PubMedBERT fine-tuned on domain corpus
   - Entity types: Plant, Chemical, Gene/Protein, Disease, Symptom

3. Relation Extraction
   - BERT-based classification of entity pairs
   - Relation types: plant-CONTAINS-chemical, chemical-TARGETS-gene, plant-TREATS-disease
   - Ensemble methods (SARE) achieve best results

4. Knowledge Graph Population
   - Triple format: [head, relation, tail]
   - Graph database (Neo4j) or RDF store

5. Downstream Applications
   - Network pharmacology analysis
   - Drug-target interaction prediction
   - Formula optimization
```

### 4.3 Key Tools

| Tool | Purpose | URL |
|------|---------|-----|
| **DeepKE** | NER + RE toolkit, supports low-resource/few-shot | https://github.com/zjunlp/DeepKE |
| **PubTator Central** | Biomedical NER (English) | NCBI |
| **BRAT** | Annotation tool | brat.nlplab.org |
| **BioBERT** | Biomedical language model | https://github.com/dmis-lab/biobert |
| **PubMedBERT** | Domain-specific pre-training | Microsoft |
| **ChemSpot** | Chemical NER | humboldt-university |
| **Cytoscape** | Network visualization | cytoscape.org |

---

## 5. Drug Discovery from Traditional Medicine via Computation

### 5.1 Network Pharmacology

Network pharmacology (NP) is the dominant computational paradigm, integrating:
- Systems biology + omics + computational methods
- Multi-target drug interaction analysis
- "Multi-component, multi-target, multi-pathway" fits traditional medicine perfectly

**Key resources:** DrugBank, TCMSP, PharmGKB, STRING, AutoDock

**Reference:** "Network pharmacology: towards the artificial intelligence-based precision traditional Chinese medicine" (2024), Briefings in Bioinformatics. doi: 10.1093/bib/bbad518
**URL:** https://academic.oup.com/bib/article/25/1/bbad518/7513596

### 5.2 Success Stories Beyond Artemisinin

| Compound | Source | Traditional Use | Modern Application |
|----------|--------|----------------|-------------------|
| Artemisinin | Artemisia annua (sweet wormwood) | Chinese fever remedy | Antimalarial (Nobel Prize 2015) |
| Galanthamine | Galanthus nivalis | Turkish/Bulgarian neurological use | Alzheimer's treatment |
| Capsaicin | Capsicum spp. | Aztec/Indian cough/bronchitis remedy | Pain management |
| Berberine | Coptis chinensis | TCM digestive remedy | Anti-diabetic, anti-inflammatory |
| Triptolide | Tripterygium wilfordii | TCM autoimmune | Anticancer, immunosuppressive |
| Celastrol | Tripterygium wilfordii | TCM anti-inflammatory | Anti-obesity, anti-diabetes |
| Curcumin | Curcuma longa | Ayurvedic/Jamu anti-inflammatory | Broad: anti-cancer, neuroprotective |
| Morphine | Papaver somniferum | Opium (pain) | Analgesic |

**Reference:** "Molecular Understanding and Modern Application of Traditional Medicines: Triumphs and Trials" (2007), Cell.
**URL:** https://www.cell.com/fulltext/S0092-8674(07)01084-7

*Cell* journal ranked celastrol, triptolide, artemisinin, capsaicin and curcumin as the top five natural drugs developable into modern compounds.

### 5.3 Computational Drug Discovery Pipeline for Traditional Medicine

```
Traditional Knowledge -> Text Mining/KG -> Network Pharmacology -> Molecular Docking -> In vitro -> Clinical
                         ^^^^^^^^^^^^^^
                         (OUR CONTRIBUTION)
```

---

## 6. Gap Analysis: What Has NOT Been Done

| Gap | Description | Opportunity for Us |
|-----|-------------|-------------------|
| **No Jamu KG** | No published knowledge graph specifically for Jamu exists | Build the first one |
| **No Indonesian biomedical NER** | No NER model for Indonesian pharmacological/botanical text | Fine-tune IndoBERT/NusaBERT |
| **No Indonesian RE for ethnopharm** | No relation extraction for Indonesian ethnopharmacological text | Adapt HerbKG pipeline |
| **RISTOJA is locked** | Richest ethnobotanical dataset is not publicly accessible | Use alternative sources or apply for access |
| **No LLM-based extraction for Jamu** | OpenTCM approach not applied to Indonesian medicine | Apply GPT/LLM extraction to Jamu literature |
| **Ontologies are shallow** | Existing Jamu ontologies cover "only a fraction" of domain knowledge | Extend with comprehensive KG |
| **No Javanese/local language NER** | Traditional knowledge exists in local languages, no NER exists | Potential future extension |

---

## 7. Recommended Architecture (Based on Literature)

Drawing from all findings, the optimal approach for a solo researcher:

### Phase 1: Data Assembly
- Harvest KNApSAcK Jamu data (3,138 formulas, publicly available)
- Harvest HerbalDB compounds (1,405 compounds)
- Scrape Jurnal Jamu Indonesia and Indonesian ethnobotany papers
- Collect BPOM (Indonesian FDA) herbal registration data

### Phase 2: Entity Extraction
- **For English literature:** Use PubTator Central + BioBERT/PubMedBERT (proven by HerbKG)
- **For Indonesian literature:** Fine-tune NusaBERT on small annotated dataset (use DeepKE for few-shot NER)
- **For both:** Use LLM-based extraction (GPT-4/Claude with structured prompts, validated by OpenTCM approach)

### Phase 3: Relation Extraction
- BERT-based RE for English texts
- LLM-based RE with JSON output for Indonesian texts (following OpenTCM methodology)
- Human expert validation on sample

### Phase 4: Knowledge Graph Construction
- Schema following GRAYU/SymMap architecture:
  - Formulation <-> Plant <-> Chemical <-> Target/Gene <-> Disease
  - Add: Ethnicity, Region, Traditional Use, Plant Part
- Neo4j or similar graph database
- Map traditional disease names to ICD-10 (following KNApSAcK precedent)

### Phase 5: Applications
- Network pharmacology analysis via Cytoscape
- GraphRAG for LLM-powered querying (following OpenTCM)
- Formula optimization (following Kusuma et al. bipartite graph approach)

---

## 8. Key Repositories and Tools to Bookmark

| Resource | URL | Relevance |
|----------|-----|-----------|
| KNApSAcK Family DB | http://www.knapsackfamily.com/ | Jamu formula data |
| HerbalDB | (see Pharmacognosy Journal) | Indonesian compound structures |
| GRAYU (Ayurveda) | https://caps.ncbs.res.in/GRAYU/ | Schema reference |
| IMPPAT 2.0 | https://cb.imsc.res.in/imppat/ | Methodology reference |
| SymMap | http://www.symmap.org/ | TCM symptom mapping reference |
| DeepKE | https://github.com/zjunlp/DeepKE | NER/RE toolkit |
| OpenTCM | https://github.com/XY1123-TCM/OpenTCM | GraphRAG reference |
| NusaBERT | https://github.com/LazarusNLP/NusaBERT | Indonesian multilingual model |
| IndoBERT | https://huggingface.co/indolem/indobert-base-uncased | Indonesian base model |
| cahya/Indonesian-NER | https://huggingface.co/cahya/bert-base-indonesian-NER | Indonesian NER baseline |
| BioBERT | https://github.com/dmis-lab/biobert | Biomedical NER baseline |
| PPR Corpus | Nature Scientific Data (2022) | Plant-phenotype training data |
| IMPPAT2 GitHub | https://github.com/asamallab/IMPPAT2 | Reusable scripts |

---

## Sources

- [Application of AI in Jamu Development (Frontiers, 2023)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2023.1274975/full)
- [Supervised Clustering for Jamu Plant-Disease Prediction (PMC, 2014)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3997850/)
- [Bipartite Graph Jamu Formulation Optimization (Frontiers, 2022)](https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2022.978741/full)
- [Indonesian Traditional Medicine Ontology via SWRL (IJECE, 2017)](https://ijece.iaescore.com/index.php/IJECE/article/view/8737)
- [Indonesian Herbal Medicine Ontology Quality Evaluation (2020)](https://www.academia.edu/66990877/Evaluation_of_Indonesian_Traditional_Herbal_Medicine_Ontology_Quality)
- [SymMap: TCM Symptom Mapping Database (NAR, 2019)](https://academic.oup.com/nar/article/47/D1/D1110/5150228)
- [Critical Assessment of TCM Databases (Frontiers, 2024)](https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2024.1303693/full)
- [HerbKG: Two-Stage KG Construction (Frontiers Genetics, 2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9091197/)
- [OpenTCM: GraphRAG + LLM for TCM (arXiv, 2025)](https://arxiv.org/abs/2504.20118)
- [TCM Knowledge Graph Review (2024)](https://cdn.techscience.cn/files/cmc/2024/online/CMC1022/TSP_CMC_55671/TSP_CMC_55671.pdf)
- [GRAYU: Ayurveda Graph Database (Frontiers Pharmacology, 2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12872832/)
- [IMPPAT 2.0: Indian Medicinal Plants Atlas (ACS Omega, 2023)](https://pubs.acs.org/doi/10.1021/acsomega.3c00156)
- [African Traditional Medicine Knowledge System (PMC, 2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8959699/)
- [IndoLEM and IndoBERT (COLING, 2020)](https://aclanthology.org/2020.coling-main.66/)
- [NusaBERT (arXiv, 2024)](https://arxiv.org/html/2403.01817v1)
- [Indonesian Medical NER with BiLSTM-CRF (ScienceDirect, 2024)](https://www.sciencedirect.com/science/article/pii/S1877050924031521)
- [Cendol: Indonesian LLMs (arXiv, 2024)](https://arxiv.org/html/2404.06138v1)
- [LoraxBench: 20 Indonesian Languages Benchmark (2025)](https://arxiv.org/html/2508.12459)
- [Plant Phenotype Relationship Corpus (Nature Scientific Data, 2022)](https://www.nature.com/articles/s41597-022-01350-1)
- [Plant-Chemical Corpus (PMC, 2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5029005/)
- [Plant-Disease Corpus (PMC, 2019)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6713337/)
- [DeepKE Toolkit (EMNLP 2022)](https://github.com/zjunlp/DeepKE)
- [Network Pharmacology + AI for TCM (Briefings Bioinformatics, 2024)](https://academic.oup.com/bib/article/25/1/bbad518/7513596)
- [Molecular Understanding of Traditional Medicines (Cell, 2007)](https://www.cell.com/fulltext/S0092-8674(07)01084-7)
- [HerbalDB 2.0 (Pharmacognosy Journal)](https://www.phcogj.com/article/1001)
- [RISTOJA Database (Indonesian Government Repository)](https://repository.badankebijakan.kemkes.go.id/id/eprint/4740/)
- [LLM-based TCM KG Construction (Springer, 2025)](https://link.springer.com/article/10.1007/s12539-025-00735-1)
- [Indonesian NER on HuggingFace](https://huggingface.co/cahya/bert-base-indonesian-NER)
- [BioBERT (Bioinformatics, 2020)](https://github.com/dmis-lab/biobert)
- [TCM Knowledge Graph GitHub](https://github.com/AI-HPC-Research-Team/TCM_knowledge_graph)
- [NusaBERT GitHub](https://github.com/LazarusNLP/NusaBERT)
- [IMPPAT2 GitHub](https://github.com/asamallab/IMPPAT2)
