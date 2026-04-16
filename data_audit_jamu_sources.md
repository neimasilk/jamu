# Data Audit: Digital Sources for Indonesian Traditional Medicine (Jamu) Research

**Date:** 2026-03-17
**Purpose:** Identify accessible digital data sources for a solo researcher studying Indonesian traditional medicine (jamu).

---

## 1. BPOM (Badan POM) Database

### What exists
BPOM maintains a public product registry at **cekbpom.pom.go.id** covering all registered traditional medicines in Indonesia, classified into three tiers:
- **Jamu** (~17,000+ registered products) — efficacy based on empirical/traditional use
- **Obat Herbal Terstandar / OHT** (~78 products) — standardized + preclinical evidence
- **Fitofarmaka** (~21 products) — full clinical trial evidence

### Access details
| Field | Detail |
|-------|--------|
| **URL** | https://cekbpom.pom.go.id/produk-obat-tradisional |
| **Format** | HTML web interface, server-side AJAX (DataTables with `serverSide: true`, POST requests) |
| **Size** | ~17,000+ jamu, ~78 OHT, ~21 fitofarmaka |
| **API** | No public API. Data loads via internal POST endpoint for DataTables |
| **Download** | No bulk download option |
| **Scrapability** | Technically possible (AJAX/POST pagination), but no explicit ToS permission. The POST-based DataTables interface could be reverse-engineered. |
| **Fields available** | Registration number, product name, registrant, dates (submission/issuance/expiration), status, manufacturer, composition, formulation |
| **Cost** | Free to search |
| **Legal status** | Public government data; no explicit open data license. Scraping is a gray area. |
| **Quality** | Authoritative — this is the official regulatory database |

### Assessment
This is the single most complete registry of commercial jamu products in Indonesia. The AJAX/DataTables interface can be scraped programmatically by mimicking POST requests with pagination parameters. However, the data is primarily regulatory (product names, registration numbers, manufacturers) rather than pharmacological (no ingredient details, no plant-disease mappings in the public-facing interface). You would need to cross-reference registration numbers with the actual product labels or other databases for ingredient composition.

---

## 2. RISTOJA (Riset Tumbuhan Obat dan Jamu)

### What exists
RISTOJA is a major government ethnomedicinal research program conducted in three waves: **2012, 2015, and 2017**. It documented traditional healers (hattra/battra), their treatments, and the medicinal plants used across ethnic groups in Indonesia.

Key statistics:
- Identified **4,000+ species** of medicinal plants
- Documented treatments across **54+ ethnic groups** (in Papua alone for 2017)
- Data includes: healer demographics, disease symptoms, plant species, plant parts used, preparation methods, usage methods, local wisdom

### Access details
| Field | Detail |
|-------|--------|
| **Report URL** | https://repository.badankebijakan.kemkes.go.id/id/eprint/4740/ |
| **Report PDF** | https://repository.badankebijakan.kemkes.go.id/id/eprint/4740/1/LaporanNasional_Ristoja2012.pdf (~3MB) |
| **Data portal** | https://labdata.litbang.kemkes.go.id/ (Katalog Data Mikro) |
| **Dashboard** | https://satusehat.kemkes.go.id/data/dashboard/216ccee3-9f18-4261-8da5-e7dcf5ab9cd6 |
| **Raw data access** | **NOT freely downloadable.** Requires formal proposal submission to the Head of NIHRD (Badan Kebijakan Pembangunan Kesehatan), Ministry of Health |
| **Format** | National Reports available as PDF. Raw microdata requires formal request. |
| **Cost** | Free (reports); bureaucratic process (raw data) |
| **Legal status** | Government research data; formal data sharing agreement required for raw data |

### Assessment
This is arguably the most valuable ethnomedicinal dataset for Indonesian traditional medicine. The national reports (PDF) are freely downloadable and contain summary data, tables, and analyses. However, the raw microdata (individual healer records, plant-disease mappings by ethnic group) requires a formal proposal — this is a significant barrier for a solo researcher. The published academic papers that cite RISTOJA data (available on ResearchGate and journal sites) are the most practical way to access processed RISTOJA findings. Dozens of papers have been published using this data, each focusing on specific diseases or regions.

---

## 3. Farmakope Herbal Indonesia (Indonesian Herbal Pharmacopoeia)

### What exists
Official pharmacopoeia published by the Ministry of Health standardizing herbal raw materials (simplisia) and extracts.

Available editions:
- **Edition I** (2008): Initial monographs
- **Edition II** (2017): 253 monographs (213 revised from Ed. I + 40 new plants), 561 pages, ISBN 978-602-416-329-7
- **Supplement I to Edition II** (2022): 110 additional monographs (55 new plant species)

### Access details
| Field | Detail |
|-------|--------|
| **Download page (Ed II)** | https://farmalkes.kemkes.go.id/en/unduh/farmakope-herbal-indonesia-edisi-ii/ |
| **Download page (Ed I)** | https://farmalkes.kemkes.go.id/en/unduh/farmakope-herbal-indonesia-edisi-i/ |
| **Supplement I PDF (direct)** | https://farmalkes.kemkes.go.id/wp-content/uploads/2023/05/Buku-Suplemen-I-FHI-Edisi-II.pdf |
| **Alt mirror** | https://repository.kemkes.go.id/book/392 |
| **Academia.edu** | PDFs of Edition I also available on Academia.edu |
| **Format** | PDF |
| **Size** | Ed II: 561 pages; Supplement I: 110 monographs |
| **Cost** | Free download from official government site |
| **Legal status** | Official government publication, freely distributed |

### Assessment
Excellent structured reference data. Each monograph contains: Latin name, local names, botanical description, chemical constituents, pharmacological properties, quality standards (identity tests, purity, chemical content). The PDFs are text-based (not scanned images), making them amenable to text extraction/parsing. However, converting 363+ monographs from PDF to structured data would require significant NLP/parsing effort. This is a high-priority source for building a plant-compound-property knowledge base.

---

## 4. Academic Datasets

### 4a. Kaggle

| Dataset | URL | Content | Size | Format |
|---------|-----|---------|------|--------|
| **Dataset Tanaman Herbal** | https://www.kaggle.com/datasets/anefiamutiaraatha/dataset-tanaman-herbal | Likely plant images (3.6 GB suggests image data) | ~3.6 GB | ZIP |
| **Tokopedia Product and Review** | https://www.kaggle.com/datasets/musabiam/tokopedia-product-and-review-dataset | General Tokopedia products/reviews (not jamu-specific) | Varies | CSV |
| **Tokopedia Product Reviews** | https://www.kaggle.com/datasets/farhan999/tokopedia-product-reviews | Product reviews from Tokopedia | Varies | CSV |
| **Tokopedia Reviews - Food & Drink** | https://www.kaggle.com/datasets/kulitekno/tokopedia-product-review-category-food-and-drink | Food/drink category (may include herbal drinks) | Varies | CSV |

**No dedicated jamu text/formulation dataset found on Kaggle.**

### 4b. HuggingFace
**No Indonesian medicinal plant or jamu dataset found.** Only general Indonesian NLP datasets exist on the platform.

### 4c. Zenodo
**No dedicated jamu dataset found.** One market analysis report on Indonesian herbal medicine market exists but is not a research dataset.

### 4d. GitHub

| Dataset | URL | Content | Size |
|---------|-----|---------|------|
| **IndoHerb** | https://github.com/Salmanim20/indo_medicinal_plant | 100 species, 10,000 images (100/species), 128x128px. Image-only — no text data on medicinal properties. Validated by biology professor. | ~image dataset |
| **Sastra Jawa** | https://github.com/nsulistiyawan/sastra-jawa | Effort to digitalize Javanese language content | Small |

### 4e. Mendeley Data

| Dataset | URL | Content | License |
|---------|-----|---------|---------|
| **Herbal consumption during COVID-19** | https://data.mendeley.com/datasets/c6z323wky2/4 | Survey data on herbal consumption patterns (types of herbs, frequency, demographics, motivations) | CC BY 4.0 |
| **Indonesian Herb Leaf Dataset 3500** | https://data.mendeley.com/datasets/s82j8dh4rr/1 | 3500 images, 10 species, 350 images each | Varies |

### Assessment
The academic dataset landscape for Indonesian jamu is **sparse for structured text data**. Most datasets are image-based (for computer vision/plant identification), not text-based knowledge about formulations, ingredients, or therapeutic uses. The Mendeley COVID herbal consumption dataset is the most useful structured text dataset found, but it covers consumption patterns, not formulations. **There is a clear gap** for a structured jamu knowledge dataset — this represents an opportunity.

---

## 5. Digital Libraries for Historical Texts

### 5a. Leiden University Digital Collections

| Field | Detail |
|-------|--------|
| **URL** | https://digitalcollections.universiteitleiden.nl/manuscriptsarchivesletters |
| **Content** | 1,200+ manuscripts and letters, including Southeast Asian/Indonesian materials |
| **Format** | Scanned digital images (folio-by-folio) |
| **Access** | Free, public, no login required for viewing |
| **Relevance** | Holds Javanese and Malay manuscripts, potentially including medical texts. No specific search filter for "medicine" or "herbal" but can browse Southeast Asian collections |
| **Note** | Currently migrating to new system. The full Southeast Asian collection includes 18,000+ manuscripts total (not all digitized). |

### 5b. Perpusnas / Khastara

| Field | Detail |
|-------|--------|
| **URL** | https://khastara.perpusnas.go.id/ |
| **Content** | 8,324 titles total: 837 ancient manuscripts, 144 rare translated monographs, 1,548 maps, 5,716 graphic materials, 79 rare serials |
| **Format** | Digital repository (images and metadata) |
| **Access** | Free; contact layanan_koleksi@mail.perpusnas.go.id for assistance |
| **Scripts** | Arabic, Javanese, Old Sundanese, Jawi, Pegon, Batak, Balinese, Bugis, and others |
| **Topics** | Includes medicine among many subjects |
| **Award** | Won 2024 UNESCO-Jikji Memory of the World Prize for preservation work |
| **Quality concern** | The web interface appeared to show 0 collections when fetched, suggesting possible technical issues or ongoing maintenance |

### 5c. Sastra.org (Javanese Literature Digital Archive)

| Field | Detail |
|-------|--------|
| **URL** | https://www.sastra.org/ |
| **Content** | Thousands of Javanese literary titles, digitized from late 18th–early 20th century manuscripts |
| **Format** | Digital text (transcribed) and digital images |
| **Access** | Free, searchable |
| **Medical content** | Includes **Primbon** texts under "Bahasa dan Budaya > Pawukon dan Primbon" category. At least one Primbon (Warsadiningrat, c. 1892) is listed. |
| **Maintained by** | Yayasan Sastra Lestari (since 1997) |

### 5d. Serat Centhini

| Field | Detail |
|-------|--------|
| **URL** | https://archive.org/details/seratcenthini |
| **Content** | Complete 12-volume Serat Centhini with OCR text |
| **Format** | PDF with OCR/full text extraction available |
| **Alt source** | Latin script version: https://archive.org/details/serat-centhini-latin-1 |
| **Access** | Free on Internet Archive |
| **Relevance** | Contains extensive passages on Javanese herbal medicine, healing practices, plant knowledge |

### 5e. Serat Primbon Jampi Jawi

- Physical manuscript at **Reksopustoko Mangkunegaran Library**, Surakarta (collection no. M 33)
- A published book "Usada Jawi: Pengobatan Tradisional Jawa" by Suyami & Titi Mumfangati is available on Google Play Books
- Academic article on DOAJ: "Pengobatan Tradisional Jawa dalam Manuskrip Serat Primbon Jampi Jawi"
- No freely available full digital transcription found

### 5f. Usada Bali (Lontar Medical Manuscripts)

| Field | Detail |
|-------|--------|
| **Physical collection** | Museum Gedong Kirtya, Singaraja, Bali — 1,750 original lontars + 7,211 copied lontar titles |
| **Usada types** | Usada Buduh, Usada Rare, Usada Tuju, and others |
| **Digital access** | ~130 lontars accessible online (unclear which portal) |
| **No comprehensive digital portal found** for Usada texts specifically |

### 5g. British Library Javanese Manuscripts

| Field | Detail |
|-------|--------|
| **URL** | Via British Library Digitised Manuscripts site; also on Wikimedia Commons |
| **Content** | 75 Javanese manuscripts from Yogyakarta (taken 1812), ~30,000 digital images |
| **Medical content** | Includes **6 volumes of Primbon** and at least one healing text (MSS Jav 85 "Layang sembayang lan tetamba" — prayers and healing) |
| **Access** | Free on British Library website and Wikimedia Commons |
| **Wikimedia** | https://commons.wikimedia.org/wiki/Category:British_Library_manuscripts_from_Yogyakarta_Digitisation_Project |

### Assessment
Historical texts are **scattered across multiple institutions** with varying levels of digitization. The Serat Centhini on Internet Archive is the single most accessible large historical text with medical content. The British Library's digitized Primbon manuscripts are freely available. Sastra.org has searchable Javanese texts including some Primbon. For Balinese Usada, digital access remains very limited. Extracting structured data from any of these requires expertise in Old Javanese/Balinese scripts and languages.

---

## 6. PubMed/Scholar Coverage

### Estimated paper counts
Based on search patterns (exact counts require direct PubMed queries):
- **"Indonesian medicinal plants"**: Likely 1,000–2,000+ papers on PubMed
- **"jamu"** (in title/abstract): Several hundred papers
- Related terms ("ethnobotany Indonesia", "ethnopharmacology Indonesia"): Additional hundreds

### Key review papers identified

| Paper | Focus | Year | Source |
|-------|-------|------|--------|
| Anti-cancer potential of Indonesian herbal plants (systematic review, PRISMA) | Cancer / in vitro | 2023 | PMC 37608914 |
| Indonesian medicinal plants for sexual dysfunction (systematic review) | Sexual dysfunction | 2025 | ScienceDirect |
| Anti-inflammatory plants for COPD treatment (systematic review) | COPD | 2025 | PMC 12025578 |
| Ethnopharmacology of wound healing plants in Indonesia (scoping review, 94 articles, 238 species) | Wound healing | 2025 | JAPS |
| Indonesian medicinal plants for metabolic syndrome | Metabolic syndrome | 2020 | PMC 7218133 |
| Tenggerese medicinal plants phytochemistry (41 species) | Regional ethnobotany | 2022 | MDPI Molecules |
| Flavonoids from Indonesian plants for diabetes | Diabetes | 2025 | Naunyn-Schmiedeberg's |
| Indonesian medicinal plants for breast cancer (74 plants, 38 families) | Breast cancer | 2025 | Asia-Pacific J Cancer Prevention |

### Assessment
There is substantial and growing academic literature. The systematic reviews are particularly valuable because they aggregate plant-disease-compound relationships from multiple primary studies. Mining these review papers for structured data (plant species, active compounds, target diseases, mechanisms) would be a highly productive approach.

---

## 7. Existing Knowledge Bases

### 7a. KNApSAcK Jamu Database

| Field | Detail |
|-------|--------|
| **URL** | https://www.knapsackfamily.com/jamu/top.php |
| **Content** | **5,310 Jamu formulas** with ingredient plants, linked to diseases |
| **Search** | Bidirectional: Herb → Jamu, Jamu → Herb |
| **Maintained by** | Nara Institute of Science and Technology (NAIST), Japan |
| **Access** | Free web search; unclear bulk download options |
| **Browser requirement** | Legacy (Firefox or IE only noted) |
| **Key research** | Used to map 3,138 Jamu formulas to 116 diseases (ICD classification, 18 disease classes) with ~90% prediction accuracy |
| **Quality** | High — academically validated, used in multiple publications |

**This is the single most important structured dataset for jamu formulation-to-disease mapping.**

### 7b. NAPRALERT

| Field | Detail |
|-------|--------|
| **URL** | https://pharmacognosy.pharmacy.uic.edu/napralert/ |
| **Content** | 200,000+ published studies on natural products |
| **Access** | Free with limitations (organism, pharmacology, compound, author queries); fee-based for extensive searches (charged per citation) |
| **Maintained by** | University of Illinois at Chicago |
| **Indonesian coverage** | Not Indonesia-specific, but includes Indonesian plants |
| **Quality** | Gold standard for natural products literature |

### 7c. Dr. Duke's Phytochemical and Ethnobotanical Databases

| Field | Detail |
|-------|--------|
| **URL (web)** | https://phytochem.nal.usda.gov/ |
| **URL (bulk download)** | https://catalog.data.gov/dataset/dr-dukes-phytochemical-and-ethnobotanical-databases-0849e |
| **CSV download** | Duke-Source-CSV.zip (direct: https://ndownloader.figshare.com/files/43363335) |
| **Data dictionary** | DrDukesDatabaseDataDictionary-prelim.csv also available |
| **Content** | ~49,788 records across 6 entity types: Biological Activity, Chemical, Plant, Syndrome, Ethnobotanical Activity, Ethnobotanical Plant |
| **License** | **Creative Commons CCZero** (public domain) |
| **Cost** | Free |
| **Export** | Web: spreadsheet downloads. Bulk: full CSV dump |
| **Indonesian coverage** | Global database; includes Indonesian plants but not Indonesia-focused |

**This is the most accessible bulk-downloadable phytochemical dataset.** CC0 license means unrestricted use.

### 7d. HerbalDB (University of Indonesia)

| Field | Detail |
|-------|--------|
| **URL** | http://herbaldb.farmasi.ui.ac.id/v3/ |
| **Content** | 3,810 species, 6,776 compounds with 3D structures |
| **Focus** | Indonesian medicinal plant compounds specifically |
| **Format** | Web database (MySQL backend) |
| **Access** | Free web access |
| **Use case** | Virtual screening, drug discovery |
| **Quality** | Academic — developed by Faculty of Pharmacy, Universitas Indonesia |

### 7e. Digital Flora of Indonesia

| Field | Detail |
|-------|--------|
| **URL** | https://www.indonesiaplants.org/ |
| **Content** | 23,203 vascular plant species checklist (BRIN data suggests 30,466 total species) |
| **Data fields** | Scientific names, authors, protolog, publication year, synonyms, distribution by island |
| **Access** | Free |
| **Maintained by** | Tumbuhan Asli Nusantara Foundation (voluntary) |
| **Limitation** | Taxonomic checklist only — no medicinal use data |
| **Download** | No bulk download apparent |

### 7f. Jamupedia

| Field | Detail |
|-------|--------|
| **URL** | https://en.jamupedia.com/ |
| **Content** | Informational website about jamu traditions, fitofarmaka products, general jamu knowledge |
| **Format** | HTML articles |
| **Structured data** | No — this is editorial content, not a database |

### Assessment
**KNApSAcK Jamu** and **Dr. Duke's database** are the two highest-priority knowledge bases. KNApSAcK has the only large-scale structured jamu formulation dataset (5,310 formulas). Duke's is the only bulk-downloadable phytochemical database with a CC0 license. HerbalDB is uniquely Indonesia-focused for compound data.

---

## 8. Marketplace Data Alternatives

### The problem
Scraping Tokopedia/Shopee directly violates their Terms of Service and is legally risky.

### Alternatives found

| Source | URL | Content | Cost | Notes |
|--------|-----|---------|------|-------|
| **Bright Data - Tokopedia dataset** | https://brightdata.com/products/datasets/tokopedia | Product listings, pricing, reviews, seller info | $250/100K records | Commercial data broker; legal for research use |
| **Bright Data - Shopee dataset** | https://brightdata.com/products/datasets/shopee | Similar fields | $250/100K records | Same |
| **Bright Data - Tokopedia sample** | https://github.com/luminati-io/Tokopedia-dataset-samples | 1,001 product sample | Free | GitHub sample dataset |
| **Bright Data - Shopee sample** | https://github.com/luminati-io/Shopee-dataset-samples | 1,000+ product sample | Free | GitHub sample dataset |
| **Kaggle - Tokopedia Product Reviews** | https://www.kaggle.com/datasets/farhan999/tokopedia-product-reviews | General product reviews | Free | Not jamu-specific |
| **Kaggle - Tokopedia Food & Drink Reviews** | https://www.kaggle.com/datasets/kulitekno/tokopedia-product-review-category-food-and-drink | Food/drink category reviews | Free | May include herbal drinks |

### Assessment
For a solo researcher on a budget, the **free GitHub samples** from Bright Data and **Kaggle review datasets** are the starting points. None are jamu-specific — you would need to filter by category/keywords. The Bright Data commercial datasets ($250/100K) are an option if you need scale, but for initial research, the free samples plus Kaggle datasets may suffice. A more practical approach might be to use BPOM's registered product list as a product catalog rather than marketplace data.

---

## Summary: Priority Data Sources for a Solo Researcher

### Tier 1 — Immediately actionable, free, high value

| Source | Why | Action |
|--------|-----|--------|
| **KNApSAcK Jamu DB** | 5,310 jamu formulas with plant-disease mappings | Systematically query and save results from web interface |
| **Dr. Duke's CSV dump** | ~50K records, phytochemical data, CC0 license | Download Duke-Source-CSV.zip immediately |
| **Farmakope Herbal Indonesia PDFs** | 363+ standardized plant monographs | Download all editions; parse PDFs for structured extraction |
| **RISTOJA National Reports (PDF)** | Summary ethnomedicinal data across Indonesia | Download from repository.badankebijakan.kemkes.go.id |
| **Serat Centhini (Internet Archive)** | 12-volume historical text with herbal knowledge, OCR available | Download and text-mine for plant/medicine references |
| **HerbalDB UI** | 3,810 species, 6,776 compounds — Indonesia-specific | Query systematically |
| **Systematic review papers** | Aggregated plant-disease-compound data | Download key reviews and extract tables |

### Tier 2 — Requires more effort but valuable

| Source | Why | Barrier |
|--------|-----|---------|
| **BPOM cekbpom.pom.go.id** | 17,000+ registered products | Requires scraping AJAX interface |
| **British Library Javanese MSS** | Primbon healing texts, freely available images | Requires Old Javanese reading ability |
| **Sastra.org** | Searchable Javanese texts including Primbon | Requires Javanese language skills |
| **NAPRALERT** | 200K+ studies | Free access is limited; institutional access helps |
| **Digital Flora of Indonesia** | 23,000+ species taxonomy | No medicinal use data; useful for name standardization |

### Tier 3 — Restricted or expensive

| Source | Why | Barrier |
|--------|-----|---------|
| **RISTOJA raw microdata** | The most detailed ethnomedicinal dataset for Indonesia | Requires formal proposal to Kemenkes |
| **Bright Data marketplace datasets** | Product/review data from Tokopedia/Shopee | $250/100K records |
| **Usada Bali lontars** | Traditional Balinese medical knowledge | Mostly not digitized; physical access required |

### Key gap identified
There is **no existing open, structured, machine-readable dataset** that maps Indonesian jamu formulations to their plant ingredients, active compounds, and target diseases in a single downloadable file. The closest is KNApSAcK Jamu (web-only, 5,310 formulas) and the various PDF pharmacopoeia. Building such a unified dataset by combining these sources would be a novel and valuable research contribution.
