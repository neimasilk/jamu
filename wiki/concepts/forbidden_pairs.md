---
type: concept
status: validated
manifesto_layer: L2
last_updated: 2026-05-07
---

# Forbidden Pairs

**107 pasangan herba yang tidak pernah co-occur dalam 5,310 formula KNApSAcK
meskipun masing-masing herba sering muncul.** Ini adalah temuan struktural di
permukaan grammar jamu, bukan kebetulan statistik.

## Definisi operasional

Pair `(h1, h2)` dikategorikan forbidden bila:
- Frekuensi h1 ≥ ambang (e.g., ≥40 formula) DAN frekuensi h2 ≥ ambang
- Expected co-occurrence di bawah independensi ≥ 5
- Observed co-occurrence = 0
[script:src/analysis/jamu_grammar.py]

Tiga puluh pair teratas (paling tinggi expected-vs-observed kontras) tersimpan
di `data/kg/jamu_grammar.json` field `forbidden_combinations`.

## Robustness — angka kunci

| Test | Result | Source |
|---|---|---|
| Null model (degree-preserving rewiring) | **Z = 37.97**, p ≪ 0.01 | [null-tested:Z=37.97] [script:herb_communities_robustness.py] |
| Parameter sweep (60 configurations) | **99.5%** of forbidden pairs cross-mazhab; **0%** within-mazhab | [null-tested:parameter-robust-99.5%] |
| Random baseline cross-rate | 83% | Same script |

Gap antara 99.5% (forbidden) dan 83% (random) adalah signifikan: forbidden
pairs **sangat berlebihan** terletak di antar-mazhab dibanding ekspektasi.

## Pasangan paling mencolok

Top-3 dari `data/kg/jamu_grammar.json`:

| h1 | h2 | freq1 | freq2 | expected overlap | observed |
|---|---|---|---|---|---|
| Cocos nucifera L. | Piper retrofractum Vahl. | 277 | 696 | 36.3 | **0** |
| (lainnya — load `data/kg/jamu_grammar.json` `forbidden_combinations` array) | | | | | |

[source:knapsack] [script:jamu_grammar.py]

## Visualisasi

`figures/21_mazhab_network.png` menampilkan 30 forbidden pairs sebagai garis
merah putus. Visual menegaskan klaim Z=37.97 secara intuitif: garis merah selalu
**memotong** antar-cluster warna mazhab, tidak intra. Bridge herbs (lihat
[[bridge_herb.md]]) yang berada di antara cluster adalah satu-satunya
"jembatan" yang dijinkan; pair forbidden adalah jurang yang tidak dijembatani.

## Interpretasi (terbuka)

Mengapa pair-pair ini forbidden?

- **Hipotesis A: incompatibility farmakologis** — substansi h1 dan h2 saling
  meniadakan atau mengganggu (e.g., warming vs cooling). Belum diuji
  [hypothesis].
- **Hipotesis B: substitusi di domain yang sama** — dua herba mengisi peran
  yang sama dalam formula yang berbeda; tradisi jamu cenderung memilih satu,
  bukan keduanya. Konsisten dengan klaim "mazhab functional, not lineage"
  (lihat [[../entities/mazhab/S0_warming_musculoskeletal.md|S0]]). Belum diuji
  langsung [hypothesis].
- **Hipotesis C: provenance regional** — pair berasal dari tradisi geografis
  yang berbeda (e.g., Jawa vs Bali) dan tidak pernah bertemu. Butuh metadata
  geografis di KNApSAcK yang belum ter-extract [hypothesis].

Tidak ada upaya membatasi ke satu hipotesis sebelum data tambahan. Lihat
`NOTES_2026-04-20_grammar_schools.md` §"Jalur Investigasi" untuk hipotesis yang
sudah ditolak.

## Apa yang TIDAK kami klaim

- ~~Forbidden pair menunjukkan kontraindikasi medis modern~~ — terlalu jauh.
  Forbidden hanya menunjukkan absensi statistik. [contradicted-by:N/A — kami
  memang tidak mengklaim ini, dicantumkan untuk eksplisit]
- ~~Setiap forbidden pair pasti punya alasan farmakologis~~ — bisa jadi
  artefak corpus. Itu sebabnya kami uji null model dan parameter sweep dulu.

## Open questions

1. Bootstrap-formula robustness: drop 20% formula, rebuild graph, apakah top-30
   forbidden pairs stabil? Disarankan di NOTES_grammar_schools.md tapi belum
   dijalankan [deferred].
2. Apakah forbidden pair memiliki tanda tangan plant-part yang berbeda? (e.g.,
   semua forbidden Cocos×X melibatkan minyak, semua Piper×X melibatkan biji)
3. Apakah forbidden pair konsisten kalau corpus-nya bukan KNApSAcK saja
   (e.g., HerbalDB ketika online)?

## Provenance summary

- [script:src/analysis/jamu_grammar.py] — pair extraction
- [script:src/analysis/herb_communities_robustness.py] — null model + sweep
- [source:data/raw/knapsack/knapsack_jamu_formulas.json] (5,310 formulas)
- [null-tested:Z=37.97]
- [null-tested:99.5% cross-mazhab across 60 configs]
- `figures/21_mazhab_network.png` — visualisasi

## See also

- [[bridge_herb.md]] — herba yang menjembatani mazhab; *bukan* forbidden pair
- [[../entities/mazhab/S0_warming_musculoskeletal.md]]
- [[validation_gap.md]] — perspektif berbeda (evidensi, bukan struktur)
- `NOTES_2026-04-20_grammar_schools.md` §"Uji Metodologis"
