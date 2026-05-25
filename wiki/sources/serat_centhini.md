---
type: source
location: data/raw/centhini/centhini_latin_vol1_djvu.txt
size_mb: 0.6
n_records: 1
license: Public domain (text ~1814; Latin transliteration of historical manuscript). Internet Archive item serat-centhini-latin-1.
last_harvested: 2026-05-25
manifesto_layer: L1
---

# Serat Centhini (Latin transliteration, vol 1)

**Teks historis Jawa pertama yang masuk JamuKG — pembuka Layer 1 manifesto.**

## What it is

Serat Centhini (*Suluk Tambangraras*) adalah ensiklopedia tembang Jawa awal
abad ke-19 (atas inisiatif Kanjeng Gusti Pangeran Adipati Anom Amêngkunagara III,
Surakarta), 12 volume / ~3500 halaman, memuat kawruh dari spiritualitas hingga
pengobatan. Item yang kita unduh = **volume 1** transliterasi aksara Latin di
Internet Archive (`serat-centhini-latin-1`), OCR Tesseract bahasa Jawa (`jv`),
624 KB teks.

## How we use it

Korpus uji untuk lab [[wiki/labs/L1_centhini_pilot/program.md|L1 Centhini Pilot]]:
ekstraksi pasangan (tanaman → guna) untuk membangun *Historical Pharmacological
Knowledge Graph* (HPKG, Manifesto §V). Dibandingkan terhadap gold standard
`[source:Nafayu2025]` di
[`data/processed/centhini_gold_standard_nafayu2025.json`](../../data/processed/centhini_gold_standard_nafayu2025.json).

## Quality and caveats

- **Hanya 1 dari 12 volume.** Gold standard Nafayu memakai edisi Kamajaya 1985
  yang **lengkap**; 82 spesies mereka tersebar di seluruh 12 volume. Recall di
  vol 1 saja bias ke bawah — lihat program.md "Masalah cakupan korpus".
- **OCR moderat**: diakritik (ê pepet, è), ejaan Solo lama, sebagian garbel.
  Butuh normalisasi sebelum dictionary match.
- **Bahasa Jawa sastra**, bukan Indonesia. Nama tanaman vernakular (kunir, jae),
  bukan Latin — jembatan Jawa→Latin = tantangan inti ("Kegelapan Bahasa" D2).
- vol 1 sampling: kosakata medis hadir (jampi/usada/tamba/loro/waras) tapi
  resep herbal jarang.

## Coverage in the wiki

- [[wiki/labs/L1_centhini_pilot/program.md|L1 Centhini Pilot]] — lab yang memakainya
- Cross-temporal: 28/32 spesies obat Centhini (gold) sudah ada di JamuKG
  kontemporer `[script:cross-check]` — sinyal awal kontinuitas (L3).

## See also

- [data_audit_jamu_sources.md](../../data_audit_jamu_sources.md) §5 — peta sumber teks historis
- [MANIFESTO_FARMAKOPE_NUSANTARA.md](../../MANIFESTO_FARMAKOPE_NUSANTARA.md) §V (L1), §VI (D1–D4 kegelapan)
