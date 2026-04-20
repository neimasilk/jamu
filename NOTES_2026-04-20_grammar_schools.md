# Catatan Sesi — Mazhab Komposisi dalam Jamu

**Tanggal**: 20 April 2026
**Konteks**: Memperdalam analisis grammar jamu setelah v07 final dan `jamu_grammar.json` teridentifikasi 107 forbidden combinations. Pertanyaan pemandu dari TRIAGE.md: *mengapa 107 pasang herbal tidak pernah bertemu — inkompatibilitas farmakologis atau sekadar domain terapeutik berbeda?*

---

## Ringkasan Temuan

**Forbidden pair bukan soal farmakologi maupun brand — mereka adalah batas mazhab komposisi, yang dapat diuji lewat ko-okurensi DAN plant-part.**

Analisis ini mengidentifikasi **11 mazhab stabil + 5 bridge herbs** dalam 5,310 formula KNApSAcK via consensus-Louvain community detection (40 seeds, resolution 1.2, co-cluster threshold 0.7) pada graf co-occurrence tertimbang *lift* (obs/expected). Dari 30 top forbidden pair: **28 lintas-mazhab, 0 dalam-mazhab, 2 menyentuh bridge**. Baseline random ~84% lintas.

Temuan paling tajam yang muncul: **Gastrointestinal disorders terpecah menjadi dua mazhab independen** yang berbeda tidak hanya pada herbal tetapi juga pada bentuk sediaan farmasi:
- **S2 (GI pahit/hepatoprotektif)**: 37% Herb + 35% Leaf → tradisi rebusan pahit
- **S3 (GI aromatik/karminatif)**: 65% Oil + 18% Seed → tradisi minyak atsiri

Jensen-Shannon divergence S2↔S3 = **0.545** (tertinggi di antara pasangan GI), menunjukkan kedua mazhab hampir disjoint secara material.

---

## Jalur Investigasi (yang ditempuh dan yang ditolak data)

### 1. Brand/company segregation → DITOLAK

Pertama kali saya curiga forbidden pair artefact: berbeda perusahaan pakai herbal berbeda. Tapi: 34 perusahaan memakai BOTH Cocos nucifera dan Piper retrofractum, namun tetap tidak pernah mencampurnya dalam satu formula. Formulator yang sama secara sadar memilih untuk tidak mencampur.

### 2. Domain-substitution (Cocos ~ Centella sebagai GI alternatif) → DITOLAK

Hipotesis kedua: within-domain forbidden pair (misal Cocos × Centella, keduanya GI) adalah "substitutes" — pilihan pengganti yang tak pernah dipilih bersama. Uji: cosine similarity pada partner-profile.

- Forbidden pair (within- atau cross-domain): cos ≈ 0.28–0.41
- Baseline random pair: cos ≈ 0.70
- Pasangan non-forbidden yang sering co-occur: cos dapat mencapai 0.82

Ternyata forbidden pair bukan substitutes. Mereka **hidup di ekosistem herbal yang benar-benar berbeda** — partnernya pun beda.

### 3. Mazhab/schools di graf co-occurrence → DITERIMA (dengan caveat stabilitas)

Louvain single-seed @res=1.2 menemukan 9 komunitas, tapi mean pairwise ARI antar-seed hanya **0.72** — bagus, tidak sempurna. Beberapa herb genuinely bridge antar-komunitas (Centella asiatica stability Jaccard = 0.25; Curcuma xanthorrhiza = 0.43).

Solusi: **consensus clustering** — jalankan 40 seeds, simpan hanya node-pair yang co-cluster ≥70% dari run. Connected components dari consensus graph = mazhab stabil.

**Hasil final: 11 komunitas stabil + 5 bridge singletons. 28/30 forbidden pair lintas-mazhab, 0 dalam-mazhab, 2 menyentuh bridge.**

### 4. Plant-part sebagai axis kedua → KONVERGEN

Setelah komunitas terdefinisi, saya tabulasi distribusi plant-part per komunitas (diweighted by occurrence count). Hasilnya sangat cohesive — tiap mazhab punya "fingerprint material" sendiri. Ini validasi independen: komunitas bukan sekadar statistical clusters, mereka adalah **tradisi farmasetika** yang membedakan teknik preparasi.

---

## 11 Mazhab Stabil + 5 Bridge Herbs

File sumber: `data/kg/jamu_herb_communities.json`

| ID | Label | n | Plant parts dominan | Anggota kunci |
|----|-------|----|---------------------|---------------|
| S0 | Musculoskeletal warming + aromatic base | 25 | Rhizome 44%, Fruit 28% | Zingiber officinale, Kaempferia, Foeniculum, Amomum, Cinnamomum, Myristica |
| S1 | Female reproductive / astringent | 25 | Rhizome 33%, Leaf 30%, Bark 15% | Curcuma domestica, Alyxia, Piper betle, Parameria, Guazuma, Parkia |
| S2 | GI bitter / hepatoprotective | 16 | **Herb 37%, Leaf 35%** | Andrographis, Orthosiphon, Centella, Phyllanthus, Morinda, Imperata |
| S3 | GI aromatic-carminative | 9 | **Oil 65%, Seed 18%** | Eucalyptus alba, Cocos nucifera, Nigella, Clausena, Mentha piperita |
| S4 | Male tonic / aphrodisiac | 8 | Fruit 62%, Root 32% | Panax ginseng, Eurycoma, Piper nigrum/retrofractum, Tribulus |
| S5 | Aromatic rhizome bitters | 4 | **Rhizome 100%** | Curcuma xanthorrhiza, Curcuma aeruginosa, Zingiber cassumunar, Acorus |
| S6 | Aromatic woods | 4 | Bark 55%, Seed 21%, Wood 10% | Massoia, Cinnamomum sintok, Santalum, Trigonella |
| S7 | Astringent GI bitters (kecil) | 3 | **Wood 60%, Bark 38%** | Alstonia macrophylla, Caesalpinia sappan, Strychnos ligustrina |
| S8 | **TCM-imported** | 3 | **Root 78%, Flower 22%** | Rheum officinale, Carthamus tinctorius, Angelica sinensis |
| S9 | Pepaya–daun wungu dyad | 2 | Leaf 93% | Carica papaya, Graptophyllum pictum |
| S10 | Food-grain GI pair | 2 | Flour 50%, Seed 40% | Zea mays, Soya max |

**Bridge singletons** (genuinely float across communities between seeds):
Woodfordia floribunda, Blumea balsamifera, Sauropus androgynus, Curcuma zedoaria, Abrus precatorius

---

## Beberapa Wawasan

### Gastrointestinal punya DUA tradisi independen, juga di bentuk material

- **S2 (GI bitter/hepatoprotective)** — Andrographis, Phyllanthus, Morinda, Orthosiphon, Centella. Dominan Herb/Leaf. Mewakili tradisi *liver tonic* dengan ekstrak air/rebusan dari daun-dan-ranting (pahit, hepatoprotektif, alkaloid/flavonoid).
- **S3 (GI aromatic-carminative)** — Eucalyptus alba, Cocos nucifera, Nigella, Clausena, Mentha piperita, Andropogon citratus. Dominan Oil/Seed. Mewakili tradisi *minyak atsiri* karminatif (angin-perut, dispepsia, kolik).

Forbidden pair Cocos × Phyllanthus (cos=0.76, ekspektasi overlap 15.9, aktual 0) kini dapat dijelaskan: keduanya memang untuk GI, tapi dari **pendekatan farmasetika yang berbeda** — tidak dirancang untuk saling mendukung.

### Peran fungsional divalidasi (meski ada caveat)

Crossing-rate per role sesuai prediksi Jun-Chen-Zuo-Shi analog:
- Menteri: 26% (spesialis, setia jalur)
- Raja: 30%
- Kurir: 47%
- Penyeimbang: 50%

20/30 forbidden pair melibatkan Menteri. Caveat: `kurir` hanya n=3 herb dalam klasifikasi, jadi angka 47% berbasis sampel kecil — perlu kalibrasi ulang jika min_freq diturunkan.

### Kantong TCM di dalam jamu (S8)

Rheum officinale (大黄), Carthamus tinctorius (红花), Angelica sinensis (当归). 78% Root + 22% Flower. Membentuk pulau sendiri yang **tidak merger ke mazhab manapun bahkan pada resolution rendah**. Ini bukan noise — ini sinyal tradisi formulasi impor yang persist sebagai "genre terpisah" dalam katalog digital jamu. Mendukung narasi Manifesto bahwa jamu memiliki lapisan-lapisan pengaruh; TCM masih dapat dideteksi secara struktural.

### Penyeimbang bukan klik melainkan glue — vindikasi Jun-Chen-Zuo-Shi

Analisis single-seed Louvain sempat memunculkan C3 yang hampir seluruhnya penyeimbang (12/16), menggoda interpretasi "penyeimbang sub-community." Tapi di consensus clustering, klik ini **terurai**: penyeimbang tersebar ke mazhab-mazhab yang mereka layani. Foeniculum bergabung ke S0 (musculoskeletal/base), Alyxia ke S1 (female reproductive), dst. Ini **konsisten dengan pemahaman original**: penyeimbang memang general-purpose glue yang melekat pada specialist herb yang mereka dukung paling sering — bukan sub-community independen.

### Hub herbs yang mengambang (bridges)

5 herb genuine-nya bridge: Curcuma zedoaria, Blumea balsamifera, Abrus precatorius, Sauropus androgynus, Woodfordia floribunda. Mereka tidak konsisten dalam satu mazhab — perlu investigasi apakah mereka punya banyak "mode pemakaian" berbeda atau hanya koneksi lemah ke semua.

### S5 — klaster farmasetik-murni

Curcuma xanthorrhiza, Curcuma aeruginosa, Zingiber cassumunar, Acorus calamus. **100% Rhizome**. Ini klaster yang terdefinisi bukan oleh efek (tersebar ke 2 effect groups) melainkan oleh teknik preparasi — semua adalah rimpang yang diparut/diperas. Mungkin menjadi lajur persiapan pabrik yang sama (same processing line).

### Axis ketiga — botanical family — TIDAK menjelaskan mazhab

Setelah konfirmasi konvergensi co-occurrence dan plant-part, axis ketiga diuji: apakah mazhab juga cohere secara taxonomic? Jawabannya tegas: **tidak**. 8 dari 11 mazhab mengandung ≥3 family berbeda. Family-entropy per komunitas berkisar 0.81–1.00 (makin mendekati 1 = makin tersebar).

Contoh paling tajam:

| Family | Anggota jamu | Mazhab yang ditempati |
|--------|--------------|------------------------|
| Zingiberaceae (17 sp) | 6 Zingiber, 4 Curcuma, 2 Kaempferia, dll | **S0, S1, S3, S5, bridge** (5 lokasi) |
| Piperaceae (5 sp) | Piper retrofractum/nigrum, betle, cubeba | **S0, S1, S4** (3 lokasi) |
| Apiaceae (7 sp) | Foeniculum, Centella, Apium, Angelica, dll | **S0, S2, S4, S8** (4 lokasi) |
| Myrtaceae (7 sp) | Eucalyptus, Eugenia, Melaleuca, Psidium | **S0, S1, S2, S3** (4 lokasi) |
| Asteraceae (6 sp) | Carthamus, Sonchus, Gynura, Blumea, dll | **S1, S2, S8, bridge** (4 lokasi) |

Piperaceae adalah contoh terbersih: tiga Piper species yang berbeda-beda masuk ke tiga mazhab yang berbeda sesuai fungsi. Piper retrofractum (cabe jawa) + Piper nigrum (merica) → tonik pria (S4). Piper betle (daun sirih) → reproduksi perempuan (S1). Piper cubeba (kemukus) → warming base (S0).

**Implikasi untuk narasi paper**: jamu grammar adalah **functional, bukan taxonomic**. Formulator tradisional berpikir dalam "apa yang dilakukan herb ini" dan "bagaimana mempersiapkannya" — bukan "herb ini famili apa". Kontras dengan Bencao Gangmu (本草纲目) yang mengorganisasikan sebagian berdasarkan taksonomi (水部, 草部, 木部, 鳞部 dst). Jamu tidak pernah memiliki kodifikasi taksonomik terpusat — dan strukturnya mencerminkan itu.

---

## Uji Metodologis (Robustness Defense)

Klaim utama sesi ini rentan pada satu pertanyaan reviewer: *"Bagaimana kalian tahu forbidden pair dan mazhab itu nyata, bukan artefak pilihan ambang batas?"* Dua uji metodologis di bawah ini menjawabnya secara sistematis. Detail hasil di `data/kg/jamu_robustness.json`. Skrip reusable: `src/analysis/herb_communities_robustness.py`.

### Uji 1 — Null model degree-preserving untuk forbidden pair

**Null hypothesis**: forbidden pair (107 pasang dengan co-occurrence = 0) hanya refleksi dari distribusi frekuensi herbal + ukuran formula, tanpa struktur mazhab.

**Metode**: Curveball-style bipartite edge swap. Incidence matrix formula × herbal di-rewiring dengan menjaga row sums (ukuran formula) dan column sums (frekuensi herbal). 100 sampel independen setelah burn-in 254K swaps (5× jumlah edge per sampel).

**Hasil**:

| Metrik | Observed | Null (100 samples) |
|---|---|---|
| Forbidden pairs (freq ≥ 100) | **107** | mean 7.15, sd 2.63 |
| Range | — | [2, 13] |
| Z-score | — | **37.97** |
| Empirical p(null ≥ observed) | — | 0.0 (tidak pernah mendekati) |

**Kesimpulan**: Forbidden pair ~15× lebih banyak daripada yang diharapkan oleh chance saja. Struktur yang mendorong pasangan herbal tertentu tidak pernah bertemu **bukan artefak frequency** — ia adalah fenomena strukturali riil yang memerlukan penjelasan.

### Uji 2 — Parameter sweep untuk komunitas

**Null hypothesis**: rate "forbidden pair = cross-community" (28/30 ≈ 93%) hanyalah artefak dari pilihan konkret `min_herb_freq=40`, `lift_threshold=1.5`, `resolution=1.2`.

**Metode**: Grid sweep 60 konfigurasi:
- `min_herb_freq` ∈ {30, 40, 50, 60, 80}
- `lift_threshold` ∈ {1.3, 1.5, 1.7, 2.0}
- Louvain `resolution` ∈ {1.0, 1.2, 1.4}

Untuk tiap konfigurasi: bangun graf, jalankan Louvain (seed=1), hitung forbidden-pair cross-rate dan ARI vs partisi kanonikal consensus.

**Hasil**:

| Metrik | Mean | Min | Max |
|---|---|---|---|
| Forbidden-pair cross-rate | **99.5%** | 97% | 100% |
| ARI vs kanonikal | 0.64 | 0.41 | 0.81 |
| Konfigurasi ≥99% cross-rate | **51/60** | | |

**Kesimpulan**: Struktur komunitas itu sendiri bergeser moderat dengan parameter (ARI 0.41–0.81), tetapi sifat "forbidden pair terletak di boundary" adalah **invariant**. Tidak ada satu konfigurasi pun yang jatuh di bawah 97%. Klaim ini tidak bergantung pada pilihan threshold yang arbitrer.

### Implikasi gabungan

Gabungan kedua uji ini memberi landasan yang cukup kokoh untuk klaim utama:

1. **Forbidden pair adalah fenomena struktural signifikan** (Z=37.97, p ≪ 0.01 vs null yang tepat).
2. **Forbidden pair terletak di batas mazhab secara invariant terhadap pilihan parameter** (cross-rate ≥97% di semua 60 konfigurasi yang diuji).
3. Oleh karena itu, **narasi "mazhab komposisi jamu"** kokoh secara metodologis.

Yang masih belum diuji:
- **Bootstrap formula** (drop-20% → rebuild → cluster). Expected tidak mengubah banyak berdasarkan parameter sweep, tapi perlu eksplisit.
- **Alternative association measure** (PMI, chi-square residual, Jaccard). Expected memberi komunitas serupa berdasarkan konsensus-ARI yang sudah robust.
- **Community label validity**: 11 label manual di `herb_communities.py` dibuat subjektif — perlu verifikasi independen (e.g., dua annotator).

---

## Arah Lanjutan (Re-Ranked Setelah Sesi Ini)

1. **Bridge herb investigation.** Untuk 5 bridge (Curcuma zedoaria, Blumea, Abrus, Sauropus, Woodfordia), deskripsikan pola pemakaiannya — apakah mereka "connector herbs" yang dipakai ketika formulator ingin menjembatani mazhab? Cek: dalam formula mana bridge muncul bersama anggota-anggota dari 2+ mazhab berbeda?
2. **TCM island (S8) deep-dive.** Berapa formula mengandung anggota S8? Perusahaan mana? Apakah formula-formula ini punya ciri nama/pack yang khas (misal "Cap Tiga Naga", "Jamu Tenaga Pria Tionghoa")? Ini berpotensi jadi short paper sendiri: "Digital traces of TCM integration in Indonesian jamu corpus."
3. **Piperaceae case study sebagai illustration.** Piper retrofractum + nigrum (S4) vs Piper betle (S1) vs Piper cubeba (S0): bagaimana *formula*-nya berbeda? Uji: apakah chemistry (piperamide content, essential oil profile) sesuai dengan penempatan mazhab?
4. **Visualisasi jaringan** — force-directed layout, node colored by community, edge thickness by lift, node shape by family. Triangulasi tiga axis sekaligus dalam satu gambar.
5. **Historical text check** — apakah kombinasi mazhab S3 konsisten dengan istilah tradisional untuk *angin*, *mual*, *perut kembung*? Analisis kata pada `jamu_name`.
6. **Cross-check Manifesto Layer 1**: jika Serat Centhini digitalized, apakah struktur mazhab teramati konsisten? (Long-term; butuh L1 harvest.)

---

## File yang Dihasilkan Sesi Ini

- `src/analysis/herb_communities.py` — consensus clustering, ARI stability, plant-part integration
- `src/analysis/herb_taxonomy.py` — genus→family mapping + entropy analysis mazhab × family
- `src/analysis/herb_communities_robustness.py` — null model + parameter sweep
- `data/kg/jamu_herb_communities.json` — 11 komunitas + 5 bridges
- `data/kg/jamu_herb_taxonomy.json` — family distribution per komunitas + entropy
- `data/kg/jamu_robustness.json` — null test (Z=37.97) + 60-config parameter sweep
- `NOTES_2026-04-20_grammar_schools.md` — dokumen ini

## Yang Tidak Dilakukan (dengan sengaja)

- Tidak menyentuh `MANUSCRIPT.md` atau `PAPER_DRAFT.md`. Temuan ini menarik tapi masih butuh validasi taxonomi dan visualisasi sebelum pantas masuk manuskrip.
- Tidak membangun visualisasi — pola sudah jelas secara numerik; figure belakangan ketika akan ditulis ke paper.
- Tidak memperbarui `jamu_grammar.json` karena sudah final di v07. Komunitas hidup di file terpisah.
- Tidak mengejar sintesis dengan PubMed evidence. Untuk sesi lain.
