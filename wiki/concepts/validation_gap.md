---
type: concept
status: validated
manifesto_layer: L4
last_updated: 2026-05-07
---

# Validation Gap

**Sebagian besar klaim plant-disease tradisional di KG kita tidak punya bukti
PubMed.** Pada KG v08 angkanya **85.56% [null-tested:robust across 4 ontology
categories]** — gap yang struktural, bukan artefak.

## Definisi operasional

"Validation gap" = persentase edge plant-disease (tipe TREATS-clinical) yang
tidak mendapat satu pun PubMed PMID saat dicari via query terstandarisasi.

- Numerator: edge tanpa evidensi PMID
- Denominator: total edge tipe TREATS-clinical pada KG v08
  ([source:knapsack] + [source:duke_csv] + [source:farmakope_pdf], setelah
  ontology-split)
- Query method: lihat [[../sources/pubmed_evidence.md]] (deferred page)

## Numbers

| Edge type | n | Gap | Source |
|---|---|---|---|
| TREATS clinical | 3,740 | **85.56%** [script:annotate_evidence.py] | KG v08 |
| HAS_USE | 1,387 | 87.0% [script:annotate_evidence.py] | KG v08 |
| ETHNOBOTANICAL_USE | 407 | 87.5% [script:annotate_evidence.py] | KG v08 |
| APPLIED_TO | 214 | 81.8% [script:annotate_evidence.py] | KG v08 |

Pre-v08 (mixed, before ontology split): 85.9% of 5,744 mixed claims
[script:annotate_evidence.py, run on v07].

## Mengapa angka ini *struktural*, bukan artefak

Tiga argumen konvergen:

1. **Slicing-robust**. Membersihkan ontology (memisahkan klinis dari
   non-klinis) menggeser angka hanya 0.34 poin (85.9 → 85.56), bukan turun
   ke 75% atau lebih [null-tested:konsisten 82–87% di empat kategori].
2. **Kategori-konsisten**. Empat tipe edge yang berbeda secara konseptual
   (klinis, kegunaan umum, etnobotani, aplikasi non-medis) semuanya menghasilkan
   gap di rentang 82–87%. Kalau gap adalah artefak labeling, kategori-kategori
   ini seharusnya divergen [null-tested:cross-category consistency].
3. **Evidensi blind-spot terdokumentasi**. 3,183 KNApSAcK formulation edges
   tidak pernah di-query ke PubMed sama sekali — visibilitas rendah, bukan
   karena PubMed sepi, melainkan karena kita belum memerintahkan query untuk
   itu [hypothesis: kalau query ditingkatkan kualitasnya, gap mungkin turun
   beberapa poin].

## Yang tidak terjadi (jujur)

Hipotesis awal di TRIAGE pra-Apr-20 adalah: ~~kalau query dibatasi ke istilah
spesifik, gap turun ke 88.5%~~. Hipotesis ini **tidak terkonfirmasi** —
ontology-split menggeser dasar perhitungan tapi tidak membuat gap ekstrem.
[contradicted-by:NOTES_2026-04-20_ontology_applied.md]

Strikethrough disengaja per [[../SCHEMA.md|SCHEMA G4]]: jangan menghaluskan
kontradiksi. Gap antara hipotesis dan realita itulah pelajaran-nya — query
quality (bukan ontology fidelity) yang mungkin jadi lever sebenarnya.

## Implikasi

- **Untuk paper**: klaim utama sah dan robust. MANUSCRIPT.md sudah memuat
  angka v08 [manuscript:§4 + Table 4 re-ranked]. Tidak perlu re-tooling.
- **Untuk drug discovery candidates**: re-ranking v08 mengeluarkan 8/30 plants
  yang sebelumnya naik karena kontaminasi non-clinical use. Lihat
  `data/kg/drug_discovery_candidates_v08.json`.
- **Untuk arah riset selanjutnya**: bukan "menutup gap" yang penting, melainkan
  *menjelaskan struktur* gap. Layer 1 (historical text mining per Manifesto)
  bisa jadi sumber evidensi independen, bukan PubMed. Itu jalur yang berbeda.

## Open questions

1. Apakah perbaikan PubMed query (mengganti `"Skin"` → `"skin AND disease"` dll.)
   menggeser gap secara signifikan? **Hipotesis**, belum diuji
   [hypothesis:pubmed-query-quality].
2. Berapa banyak gap yang sebenarnya tertutup oleh literatur Indonesian
   (jurnal lokal yang tidak ter-index PubMed)? **Hipotesis**, butuh L1 sources.
3. Apakah ada pola: gap di mazhab S0 (warming) vs S2 (GI bitter) berbeda?
   Belum di-stratify per-mazhab.

## Provenance summary

- [script:src/analysis/annotate_evidence.py] — gap calculation
- [script:src/analysis/apply_disease_ontology.py] — ontology split (v07→v08)
- [source:data/raw/pubmed/] — evidence layer
- [manuscript:§4] — published version of these numbers
- [null-tested:cross-category consistency, 82–87%]

## See also

- [[bridge_herb.md]]
- [[forbidden_pairs.md]]
- `MANIFESTO_FARMAKOPE_NUSANTARA.md` Layer 4
- `NOTES_2026-04-20_ontology_applied.md`
