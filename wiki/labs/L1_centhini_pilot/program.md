---
type: lab_program
status: phase1_baseline
manifesto_layer: L1
question: "Can plant→use relations be computationally extracted from the Serat Centhini, measured against a published gold standard, at precision ≥ 0.50?"
last_updated: 2026-05-25
---

# Lab: L1 Centhini Pilot

**Bounded sub-project (SCHEMA G7, not a loop).** Tujuannya membuka **Layer 1**
manifesto (historical text mining) dengan satu teks, satu target ekstraksi, satu
kriteria gagal yang eksplisit. Lab ini berakhir dengan satu synthesis page yang
difile balik ke wiki — bukan loop tak berujung.

> **Mengapa lab ini sekarang.** Per [index.md](../../index.md), L1 = **0 halaman**
> sejak proyek mulai (Mar 2026). Manifesto §V menyebut L1 *"the real frontier —
> inilah yang membedakan JamuKG dari sekadar database mining exercise."* Delapan
> sesi sebelumnya semua L2/L4. Ini langkah pertama ke L1, sengaja kecil dan
> bisa gagal secara terukur.

## Objektif (bounded)

Ekstrak pasangan **(tanaman → kategori-guna / penyakit)** dari teks Serat
Centhini, lalu ukur terhadap gold standard terbit. Bukan "mining semua
manuskrip" (itu loop yang ditolak G6).

## Korpus

| Item | Status | Catatan |
|---|---|---|
| `data/raw/centhini/centhini_latin_vol1_djvu.txt` | **acquired** `[source:archive.org]` | 624 KB, 24,770 baris, 84,945 kata. OCR Tesseract `jv`. Item `serat-centhini-latin-1`. |

**Masalah cakupan korpus (jujur, load-bearing).** Item archive ini = **volume 1
dari 12**. Gold standard Nafayu (lihat bawah) memakai transliterasi **Kamajaya
1985 yang LENGKAP 12-volume / 3500 halaman**. archive `serat-centhini-latin-2..4`
**tidak ada** (metadata kosong `{}` `[script:curl-probe]`). Karakterisasi vol 1:
kosakata medis hadir (`jampi`=13, `usada`=4, `tamba`=3, `loro/lara`=30,
`waras`=11, `wedang`=22) tapi nama tanaman **jarang** (jae=2, kunir=3,
kencur/temu/laos=0) — vol 1 tipis resep herbal.

→ **Konsekuensi metodologis**: uji recall di vol 1 saja akan rendah *secara
struktural* (mayoritas 82 spesies ada di volume lain). Melaporkan recall rendah
dari korpus-mismatch = halu. **Korpus harus dilengkapi (12-vol) ATAU eksperimen
di-scope ke gold-subset spesifik-vol-1 sebelum recall dihitung.**

## Gold standard

`[source:Nafayu2025]` Nafayu et al. (2025), *Bioprospecting medicinal plants of
Centhini*, Ethnobotany Research and Applications 31:1–42. PDF lokal:
`data/raw/centhini/_refs/Nafayu2025.pdf` (10.7 MB, open-access).

- Mereka mengekstrak **37 formula → 82 spesies** lintas 11 kategori-guna Staub.
- Yang **bersih dari teks** = **32 spesies "studied"** (Tabel 1 + diskusi),
  tersimpan terstruktur di
  [`data/processed/centhini_gold_standard_nafayu2025.json`](../../../data/processed/centhini_gold_standard_nafayu2025.json).
- **Caveat**: ~50 sisa spesies (82−32) terkunci di figure (Fig 5/7) sebagai
  gambar, bukan teks. Abstrak bilang "12 disease", footnote Tabel 1 cuma 11
  kategori — inkonsistensi di paper sumber, tidak di-smooth.

## Temuan Phase 0 (selesai sesi 2026-05-25)

1. Korpus vol-1 + gold-standard PDF di-acquire & di-ekstrak.
2. Gold standard 32-spesies di-strukturkan ke JSON dengan provenance + caveat.
3. **Konvergensi historis↔kontemporer** `[script:cross-check]`: **28/32** spesies
   obat Centhini sudah ada di JamuKG (87.5%). Absen: *Boesenbergia rotunda,
   Limonia acidissima, Quercus infectoria, Zingiber montanum* — kemungkinan ada
   di bawah sinonim (deskriptif, sinonim belum di-resolve; **bukan** klaim
   tervalidasi). Petunjuk awal pertanyaan L3 manifesto "apa yang bertahan?".

## Temuan Phase 1 (baseline ekstraksi, sesi 2026-05-25)

Blocker korpus **teratasi**: full 12-volume Centhini di-acquire dari item archive
`seratcenthini` (1,096,457 kata, 6.9 MB) `[source:archive.org]`.

1. **Densitas**: vol-3 paling kaya herbal (jampi=32, plant-terms=61) `[script:density-scan]`.
   `lara/loro/wedang` ubikuitus → noisy, bukan penanda resep yang baik.
2. **Recall baseline** (leksikon seed kasar, regex word-boundary, tanpa tuning)
   `[script:dict-match]`: **21/32** gold species ter-named; **19/32** dalam
   konteks medis ketat (dekat jampi/usada/tamba/ginodhog/pipis).
   `data/processed/centhini_phase1_recall.json`.
3. **Presisi (eyeball 34 konteks, BUKAN sampel berlabel formal)**: term
   high-confidence (dlingo, laos, kunci, kunir, adas, kawis, kelor, jae, tumbar,
   brambang, turi, klapa, jambe, mrica, krokot) mendarat di resep jampi/usada
   nyata — perkiraan presisi **~>0.8**. Term `ambig` (jati="sejati", kudu="harus",
   pari="pari-mitra", asem) = false positive homonim (memvalidasi flag conf).
   `data/processed/centhini_phase1_contexts.txt`.
4. **KEY — tata-bahasa resep**: teks formulaik
   `jampi/usada <penyakit> … <bahan> … <verba-olah (pinipis/ginodhog/inguyup/binorèh)>`.
   Relasi tanaman→penyakit eksplisit (cth: *jampi amĕjahi cacing*=vermifuge → laos,
   dlingo, bangle; *jampi kuping tuli* → oyot kelor; *jampi lara netra* → adas).
   **Relation Extraction feasible** — mirror historis dari jamu-grammar KNApSAcK (L2).

> **Status falsifikasi (jujur)**: Manifesto §X (presisi<0.50) **belum diuji formal**
> — butuh sampel acak berlabel tangan. Tapi sinyal preliminary **kuat di sisi
> feasible**, bukan "teks terlalu ambigu". Belum ada klaim `status:validated` (G2).

## Kriteria sukses & falsifikasi

- **Falsifikasi (Manifesto §X)**: NER/RE menghasilkan **presisi < 0.50** →
  teks terlalu ambigu, L1-on-Centhini ditunda & dilaporkan jujur.
- **Benchmark recall**: fraksi dari gold species (subset yang sesuai cakupan
  korpus) yang berhasil ditemukan extractor.
- **G2**: tidak ada klaim `status:validated` tanpa salah satu di atas.

## Rencana metode (dictionary-first, G7 simplicity)

1. Bangun leksikon **Jawa-vernakular → Latin** (jembatani "Kegelapan Bahasa" D2):
   seed dari nama lokal di KG (34 mapping) + gold species + kamus tembung Jawa
   nama tanaman (kunir→*Curcuma*, jae→*Zingiber*, dst). Normalisasi diakritik
   OCR (ê, è).
2. Dictionary match di teks (baseline). Naik ke NER/RE **hanya jika** dictionary
   jelas kurang — bukan default.
3. Ekstrak ko-okurensi (tanaman ↔ istilah penyakit Jawa: loro, lara, tamba) dalam
   jendela bait.
4. Ukur presisi (sampel hand-checked) + recall (vs gold).

## Failure modes (jujur, di-antisipasi)

- OCR noisy: tembang/verse, ejaan Solo lama, diakritik.
- Bahasa Jawa sastra ≠ Indonesia; nama tanaman arkais tak ada di kamus modern.
- Relasi tanaman↔penyakit tersebar lintas bait, bukan satu kalimat → RE sulit.
- Korpus vol-1 incomplete (lihat atas) → recall bias ke bawah.

## Decision points / tugas sesi berikutnya

1. ~~**[blocker]** Amankan korpus 12-volume penuh~~ → **SELESAI** (item archive
   `seratcenthini`, `data/raw/centhini/full12/`).
2. **Perbaiki leksikon** (recall sebenarnya > 21/32 — beberapa "absen" hanya
   salah nama):
   - Tambah nama Jawa yang ditemukan di teks: `bĕngle`→*Zingiber montanum*,
     `puyang`→*Zingiber zerumbet*, `mungsi`→*Nigella sativa* (ketiganya muncul di
     resep tapi leksikon seed pakai nama salah/modern).
   - **Drop/context-gate term `ambig`** (jati, kudu, pari, asem) — homonim,
     false-positive. Atau wajibkan ko-okurensi dengan verba-olah.
   - Cari nama Jawa untuk yang masih nol (cengkeh? "gomak"/lain; bawang putih).
3. **Presisi formal**: ambil sampel acak ~50 match, label tangan
   (medicinal / non-medicinal), hitung presisi → uji falsifikasi §X resmi.
4. **Relation Extraction**: parse pola `jampi/usada <penyakit> … <bahan> …
   <verba-olah>` → ekstrak triple (tanaman, penyakit, metode). Mulai dari vol-3.
5. Cross-map 11 kategori Staub ↔ `disease_ontology.json`; cocokkan penyakit Jawa
   (watuk=cough, kuping tuli=deafness, lara netra/lamur=eye, padharan=GI) ke ontologi.

## Terminasi (G7)

Lab selesai ketika: (a) extractor diukur vs gold (lulus/falsifikasi), dan (b)
satu synthesis page (`wiki/syntheses/centhini_extraction_pilot.md`) difile balik.
Tidak ada loop otomatis.
