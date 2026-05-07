---
type: entity
class: herb
canonical_name: "Zingiber officinale Rosc"
manifesto_layer: L2
last_updated: 2026-05-07
---

# Zingiber officinale Rosc

**Hub kurir paling sentral dalam jamu — muncul di 1,256 dari 5,310 formula
KNApSAcK, ko-occur dengan 362 herba lain. Anggota mazhab S0 (warming
musculoskeletal).** [source:knapsack] [script:jamu_grammar.py]

## Identitas

- **Scientific name**: *Zingiber officinale* Rosc
- **Family**: Zingiberaceae
- **Common names (ID)**: jahe; jahe gajah, jahe merah (varietas)
- **Plant part dominant**: rhizome

## Posisi di JamuKG

| Atribut | Nilai | Source |
|---|---|---|
| Mazhab | S0 — warming musculoskeletal + aromatic base | [script:herb_communities.py] |
| Role classification | **kurir** (universal bioenhancer) | [script:jamu_grammar.py] |
| Total formulas | **1,256 / 5,310** = 23.7% | [source:knapsack] |
| Solo count / ratio | 13 / 0.01 — hampir tidak pernah berdiri sendiri | [script:jamu_grammar.py] |
| Number of partners | **362** unique co-occurring herbs | [script:jamu_grammar.py] |
| Mean position in formula | 0.987 — selalu di akhir, konsisten dengan peran kurir | [script:jamu_grammar.py] |
| Specificity | 0.519 — moderat, bukan domain-specialist | [script:jamu_grammar.py] |
| Top effect | Musculoskeletal and connective tissue disorders | [script:jamu_grammar.py] |

[source:data/kg/jamu_grammar.json `herb_roles["Zingiber officinale Rosc"]`]

## Mengapa "kurir"

Klasifikasi "kurir" diberikan kepada herba yang:
- Muncul di banyak formula (high frequency)
- Ko-occur dengan banyak partner berbeda (high n_partners)
- Tidak terikat ke satu domain efek (specificity moderat)
- Posisi di formula relatif konsisten (di sini: akhir; mean_position 0.987)

Zingiber officinale adalah eksemplar paling jelas: 362 partner adalah dua kali
lipat partner kurir-kurir lain. [[../../concepts/jamu_grammar_roles.md|Jamu
grammar roles]] (deferred page) menjelaskan empat peran lengkapnya.

Kurir di tradisi formula klasik Tiongkok disebut *zuo* (使) atau *envoy* — herba
yang mengantar khasiat herba utama ke target. Klasifikasi kami berbasis grafik
ko-occurrence empiris, bukan importasi taksonomi tradisional, namun
konvergensinya sugestif [hypothesis: konvergensi dengan TCM zuo belum
diuji secara terstruktur].

## Hubungan cross-mazhab

- **Forbidden pairs**: Zingiber officinale tidak muncul dalam 30 top-forbidden
  pairs di `data/kg/jamu_grammar.json` — konsisten dengan peran kurir
  (kompatibel dengan banyak mazhab).
- **Signature pair tertinggi**: dengan Curcuma xanthorrhiza (32 formula
  bersama, GI domain) [script:jamu_grammar.py `effect_subnetworks` GI top_pairs]
- **Kemungkinan synergy candidate**: lift-tinggi + literature bioenhancement
  (gingerol meningkatkan bioavailabilitas senyawa lain) [hypothesis] — belum
  dieksplorasi dalam sintesis terstruktur

## Validation gap perspective

Sebagai kurir di banyak formula, klaim "Zingiber officinale TREATS X" ada di
banyak pasangan plant-disease. Berapa persen dari klaim-klaim ini punya bukti
PubMed? Belum di-stratify secara per-herb di KG v08. Pertanyaan terbuka untuk
sesi berikutnya — tambahkan kolom `gap_per_herb` ke `paper_findings.json`?

## Open questions

1. Apakah tiga varietas (jahe gajah, jahe merah, jahe putih) terpisah dalam
   data sumber atau dileburkan? KNApSAcK menggunakan satu species name, tapi
   farmakologi varietas berbeda. [hypothesis: butuh cek metadata sumber]
2. Apakah Zingiber officinale berperan sebagai bridge antara *forms*
   farmasetik (oil vs powder) selain antara mazhab? Plant-part di S0 didominasi
   rhizome (44%); apakah rhizome Zingiber masuk ke formula non-rhizome-dominant?
3. Bagaimana posisi mean (0.987) dipertahankan secara budaya — apakah resep
   yang menyimpang dari konvensi ini lebih sedikit muncul, atau ditolak?

## Provenance summary

- [source:data/raw/knapsack/knapsack_jamu_formulas.json] — 1,256 formula
- [script:src/analysis/jamu_grammar.py] — role classification
- [script:src/analysis/herb_communities.py] — mazhab assignment S0
- [source:data/kg/jamu_grammar.json] — angka di atas

## See also

- [[../mazhab/S0_warming_musculoskeletal.md]]
- [[../../concepts/forbidden_pairs.md]]
- [[../../concepts/bridge_herb.md]] — Zingiber officinale BUKAN bridge (ia kurir,
  yang berbeda); halaman bridge dijelaskan untuk perbedaannya
