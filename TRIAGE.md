# JamuKG — Triage
**16 April 2026** (deliberation) | **20 April 2026** (progress update di bawah)

Catatan deliberasi setelah audit mendalam terhadap data yang sudah ada.

---

## Progress Update — 20 April 2026

Tiga sesi di tanggal 20 April 2026 menyelesaikan sebagian besar Tier 1 + Tier 2. Detail lengkap di `NOTES_2026-04-20_grammar_schools.md` dan `NOTES_2026-04-20_ontology_applied.md`.

### ✅ Selesai
- **Ontology cleanup + apply to KG** (Tier 1). v08 KG tercipta: 8,931 TREATS lama → 6,923 TREATS (clinical+symptom) + 1,387 HAS_USE + 407 ETHNOBOTANICAL_USE + 214 APPLIED_TO. 6 ambiguous terms resolved.
- **Deeper grammar analysis** (Tier 2). 11 mazhab stabil + 5 bridge herbs via consensus-Louvain, divalidasi oleh dua axis independen (plant-part, taxonomy).
- **Forbidden combinations investigation** (Tier 2). 107 forbidden pairs lulus uji signifikansi (Z=37.97 vs null degree-preserving) dan parameter sweep (99.5% cross-mazhab di 60 konfigurasi).
- **Methodological robustness suite**. Null model + parameter sweep tersimpan sebagai skrip reusable (`src/analysis/herb_communities_robustness.py`).

### Hasil mengejutkan (jujur)

Angka validation gap **hanya bergerak dari 85.9% → 85.6%** setelah ontology cleanup — jauh di bawah hipotesis awal triage (88.5%). Gap ternyata **struktural** di semua kategori (82–87%), bukan artefak label. Cleanup tetap bernilai karena:
1. Meningkatkan precision klaim (3,740 clinical vs 5,744 mixed)
2. Re-ranking drug discovery candidates: 8/30 plants keluar dari top-30 karena ranked tinggi akibat non-clinical uses
3. Membongkar blind spot: 3,183 KNApSAcK formulation edges tidak pernah diquery PubMed

Angka 88.5% yang dihipotesiskan di TRIAGE asli (via restriksi ke istilah spesifik) **tidak tercapai** dengan pendekatan ontology-split. Jalur perbaikan PubMed-query-quality (mengganti "Skin" → "skin AND disease" dll.) masih belum dieksplorasi.

### Belum dikerjakan (Tier 2/3)
- Synergy prediction (co-occurrence + bioenhancement mechanism)
- Visualisasi jaringan mazhab
- HerbalDB harvest (server masih down)
- Historical text mining (Layer 1 Manifesto)
- Marketplace mining
- ICD-10 mapping improvement
- Formulation-level PubMed validation (aggregate from constituent plants)
- Piperaceae / TCM island / bridge herb case studies (scoped)
- PubMed-query-quality improvement (mengaddress 88.5% hypothesis dari TRIAGE asli)

---

## Apa yang Ditemukan dari Audit

### 1. Validation Gap Mungkin Lebih Besar dari 85.9%

Angka 85.9% menggunakan semua 5,744 pasangan plant-disease — termasuk pasangan dengan istilah penyakit yang samar seperti "Skin", "Wound", "Cancer" yang menghasilkan ribuan false positive di PubMed (contoh: "Pithecellobium scutiferum" AND "Skin" = 1,896 hit — hampir pasti noise).

Ketika dibatasi pada istilah penyakit yang **spesifik** (620 dari 642 istilah), hasilnya:
- **88.5% tanpa bukti** (naik dari 85.9%)
- **Hanya 0.8% well-studied** (turun dari 1.3%)

**Implikasi:** Angka 85.9% kita bukan exaggeration — justru **konservatif**. Gap sebenarnya mungkin lebih besar. Ini memperkuat temuan, tapi juga berarti kita harus memperbaiki metode query PubMed.

### 2. 241 Pasangan Bukan Tentang Penyakit Sama Sekali

Dari Dr. Duke's database, ada istilah seperti "Piscicide" (racun ikan, 62 pasangan), "Arrow-poison" (18), "Cosmetic" (28), "Spice" (14), "Homicide" (1). Ini **bukan klaim terapeutik** — ini penggunaan etnobotani. Mereka seharusnya tidak ada di edge TREATS.

Ini bukan bug kecil. Ini masalah ontologis: apa yang kita sebut "penyakit" dalam KG sebenarnya adalah campuran dari:
- **Penyakit klinis** (Diabetes, Malaria, Dysentery)
- **Gejala** (Fever, Headache, Cough)
- **Penggunaan farmakologis** (Diuretic, Vermifuge, Emmenagogue)
- **Penggunaan non-medis** (Piscicide, Dye, Spice)
- **Penggunaan kosmetik** (Cosmetic, Hair-Tonic)

Sebuah KG yang serius harus membedakan ini.

### 3. Ada "Grammar" dalam Komposisi Jamu

Temuan paling menarik dari audit:

**a) Distribusi bimodal.** Formula jamu terbagi jelas: formula 1-herbal (815 produk, biasanya standalone) dan formula 4-5 herbal (puncak distribusi, 1,974 produk). Ini bukan acak — ini dua "mode" pembuatan jamu yang berbeda.

**b) Herbal yang TIDAK PERNAH muncul sendiri.** Piper retrofractum (cabe jawa) muncul di 696 formula tapi *tidak pernah* sebagai bahan tunggal. Begitu juga Piper nigrum (441), Alyxia reinwardtii (466), dan Amomum cardamomum (417). Herbal ini bukan obat — mereka adalah **komponen pendukung** yang hanya bekerja dalam kombinasi.

**c) Zingiber officinale sebagai "universal base".** Hampir setiap herbal pendukung memiliki jahe sebagai partner utamanya. Jahe berfungsi sebagai *base note* dalam komposisi jamu — mirip peran kaldu ayam dalam masakan Prancis, atau peran Jun (君, raja) dalam TCM. Ini memperkuat hipotesis bahwa jamu memiliki sistem komposisi yang analog dengan Jun-Chen-Zuo-Shi (君臣佐使) TCM.

**d) Kompleksitas terapeutik tidak acak.** Gangguan gastrointestinal: rata-rata 3.4 herbal. Gangguan respirasi: rata-rata 6.2 herbal. Tradisi jamu tampaknya sudah "tahu" secara empiris bahwa penyakit yang berbeda membutuhkan tingkat kompleksitas farmakologis yang berbeda.

---

## Triage: Tiga Tier

### TIER 1 — Fondasi (Kanvas Harus Benar Dulu)

**Ontologi penyakit yang bersih.**

Sekarang node "Disease" di KG kita adalah campuran kacau dari penyakit, gejala, penggunaan farmakologis, dan penggunaan non-medis. Ini mengotori setiap analisis yang dibangun di atasnya.

Yang perlu dilakukan:
- Klasifikasi ulang 642 istilah penyakit ke dalam kategori: `clinical_disease`, `symptom`, `pharmacological_use`, `non_medical_use`, `cosmetic`
- Pisahkan edge TREATS menjadi TREATS (untuk penyakit/gejala aktual) dan HAS_USE (untuk penggunaan non-medis)
- Re-run validation gap hanya untuk klaim terapeutik yang sebenarnya

Ini pekerjaan membosankan tapi kritis. Tanpa ini, angka 85.9% kita bisa dipertanyakan oleh reviewer mana pun.

**Mengapa ini duluan:** Setiap analisis — drug discovery candidates, network pharmacology, manuscript — dibangun di atas ontologi ini. Jika fondasinya kotor, semuanya kotor.

### TIER 2 — Penemuan (Yang Membuat Proyek Ini Bermakna)

**Grammar Jamu: Sistem Jun-Chen-Zuo-Shi Nusantara.**

Data sudah menunjukkan pola yang jelas: ada herbal yang selalu muncul sendiri (Pandanus conoideus: 89% solo), ada yang tidak pernah muncul sendiri (Piper retrofractum: 0% solo, 696 formula), dan ada yang menjadi "base" universal (Zingiber officinale).

Hipotesis yang bisa diuji:
1. Apakah herbal jamu bisa diklasifikasi ke dalam peran-peran fungsional (seperti Jun-Chen-Zuo-Shi)?
2. Apakah kombinasi tertentu menghasilkan efek yang berbeda secara sistematis? (temulawak+jahe untuk muskuloskeletal, tapi temulawak+adas untuk gastrointestinal?)
3. Apakah "kompleksitas resep" (jumlah herbal) berkorelasi dengan "kompleksitas penyakit"?
4. Apakah ada *forbidden combinations* — herbal yang TIDAK PERNAH muncul bersama?

Ini adalah temuan yang unik untuk KG kita — tidak ada paper yang pernah menganalisis ini secara komputasional dari 5,310 formula.

**Mengapa ini tier 2, bukan tier 1:** Analisis ini tetap bisa dilakukan dengan data kotor, tapi hasilnya akan lebih tajam setelah ontologi dibersihkan.

### TIER 3 — Ekspansi (Ketika Fondasi Kokoh)

**a) HerbalDB** — 3,810 spesies, 6,776 senyawa dengan struktur 3D. Ini akan menambah dimensi kimia yang sekarang hanya datang dari Duke. Server sedang down; harvester sudah siap.

**b) Historical text mining** — Layer 1 manifesto. Ini membutuhkan akses ke digitalisasi manuskrip (Serat Centhini, Usada Bali) dan NER/RE yang di-fine-tune untuk bahasa Jawa Kuno. Proyek besar, tapi *inilah* yang membedakan JamuKG dari sekadar "database mining exercise".

**c) Marketplace mining** — Layer 2 manifesto. Tokopedia, Shopee listing jamu. Corpus hidup yang berubah setiap hari.

**Mengapa ini tier 3:** Data baru tanpa fondasi yang bersih hanya menambah noise. Lebih baik memiliki KG kecil yang bersih daripada KG besar yang kotor.

---

## Yang TIDAK Perlu Dilakukan Sekarang

- ~~Submit paper~~ — Ini bukan deliverable semester. Manuscript sudah ada sebagai dokumentasi, bukan target.
- ~~Format LaTeX~~ — Prematur.
- ~~Expand ke 4 sumber data sekaligus~~ — Kedalaman > keluasan.
- ~~ICD-10 mapping mekanis~~ — Lebih penting memperbaiki ontologi dulu daripada memetakan ke sistem klasifikasi yang mungkin tidak cocok untuk pengetahuan tradisional.

---

## Langkah Pertama: Bersihkan Ontologi

Mulai dari yang membosankan tapi benar. Seperti Michelangelo yang menghabiskan berbulan-bulan menyiapkan plester sebelum mulai melukis.
