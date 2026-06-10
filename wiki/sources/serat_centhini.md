---
type: source
location: data/raw/centhini/full12/
size_mb: 6.9
n_records: 12
license: Public domain (text ~1814; Latin transliteration of historical manuscript). Internet Archive item seratcenthini.
last_harvested: 2026-05-25
last_updated: 2026-06-10
manifesto_layer: L1
---

# Serat Centhini (Latin transliteration, full 12 volumes)

**Teks historis Jawa pertama yang masuk JamuKG — pembuka Layer 1 manifesto.**

## What it is

Serat Centhini (*Suluk Tambangraras*) adalah ensiklopedia tembang Jawa awal
abad ke-19 (atas inisiatif Kanjeng Gusti Pangeran Adipati Anom Amêngkunagara III,
Surakarta), 12 volume / ~3500 halaman, memuat kawruh dari spiritualitas hingga
pengobatan. Korpus yang kita pakai = **12 volume penuh** transliterasi aksara
Latin dari item Internet Archive `seratcenthini` →
`data/raw/centhini/full12/centhini01..12.txt`, **1,096,457 kata / 6.9 MB**.

> **Riwayat akuisisi (jujur).** Sesi 25 Mei semula hanya mengamankan **vol-1**
> (item `serat-centhini-latin-1`, 0.6 MB) karena vol 2–4 archive kosong; vol-1
> tipis herbal → blocker recall. Blocker **teratasi di Phase 1**: full 12-vol
> ditemukan di item `seratcenthini` dan di-commit. File vol-1 lama
> (`centhini_latin_vol1_djvu.txt`) masih ada sebagai artefak historis; korpus
> kerja sekarang = `full12/`.

## How we use it

Korpus uji untuk lab [[wiki/labs/L1_centhini_pilot/program.md|L1 Centhini Pilot]]:
ekstraksi pasangan (tanaman → guna) untuk membangun *Historical Pharmacological
Knowledge Graph* (HPKG, Manifesto §V). Dibandingkan terhadap gold standard
`[source:Nafayu2025]` di
[`data/processed/centhini_gold_standard_nafayu2025.json`](../../data/processed/centhini_gold_standard_nafayu2025.json).

## Quality and caveats

- **OCR moderat**: satu-satunya huruf non-ASCII di korpus = **ĕ (e-pepet,
  U+0115)**; di-fold ke `e` saat matching (`[script:centhini_extract.py]`).
  Ejaan Solo lama + sebagian garbel tetap ada.
- **Bahasa Jawa sastra**, bukan Indonesia. Nama tanaman vernakular (kunir, jae),
  bukan Latin — jembatan Jawa→Latin = tantangan inti ("Kegelapan Bahasa" D2).
- **Densitas herbal tidak rata**: vol-3 paling kaya resep (`jampi` terbanyak);
  `lara/loro/wedang` ubikuitus → noisy, bukan penanda resep yang baik.
- Gold standard Nafayu memakai edisi Kamajaya 1985 yang juga lengkap 12-vol →
  cakupan korpus kini **cocok** dengan gold (blocker recall vol-1 sudah hilang).

## Coverage in the wiki

- [[wiki/labs/L1_centhini_pilot/program.md|L1 Centhini Pilot]] — lab yang memakainya
- Recall dictionary-match: **26/32** gold species ter-named (23/32 hi-conf;
  18/32 hi-conf+konteks medis) `[script:centhini_extract.py]`.
- Cross-temporal: 28/32 spesies obat Centhini (gold) sudah ada di JamuKG
  kontemporer `[script:centhini_extract.py]` — sinyal awal kontinuitas (L3).

## See also

- [data_audit_jamu_sources.md](../../data_audit_jamu_sources.md) §5 — peta sumber teks historis
- [MANIFESTO_FARMAKOPE_NUSANTARA.md](../../MANIFESTO_FARMAKOPE_NUSANTARA.md) §V (L1), §VI (D1–D4 kegelapan)
