---
type: concept
status: validated
manifesto_layer: L2
last_updated: 2026-05-07
---

# Bridge Herb

**Lima herba yang secara konsisten "mengambang" di antara mazhab dalam
consensus-Louvain — bukan anggota stabil dari satu kluster, tapi terlalu sering
muncul untuk diabaikan.** Mereka adalah singleton dalam konsensus, bukan
anomali.

## Definisi operasional

Sebuah herba diklasifikasikan sebagai *bridge* bila pada konsensus-Louvain
40-seed (lift-graph, resolution=1.2, co-cluster threshold 0.7), ia tidak
ditugaskan ke kluster manapun yang berukuran ≥2. Ia muncul sebagai
*singleton* di hasil komponen-terhubung.
[script:src/analysis/herb_communities.py]

Berbeda dengan herba yang stabil di satu mazhab (ARI co-cluster ≥ 0.7), bridges
mendapat assignment kluster yang berbeda di seed yang berbeda — algoritma tidak
bisa menemukan rumah tetap untuk mereka.

## Lima bridges

| Herb | n_partners | total_formulas | Top effect (per `herb_roles`) |
|---|---|---|---|
| **Blumea balsamifera** DC. | TBD | TBD | TBD |
| **Sauropus androgynus** Merr | TBD | TBD | TBD |
| **Curcuma zedoaria** (Berg.) Roscoe | TBD | TBD | TBD |
| **Abrus precatorius** L. | TBD | TBD | TBD |
| **Woodfordia floribunda** Salisb. | TBD | TBD | TBD |

[source:data/kg/jamu_herb_communities.json field `bridge_singletons`]
[script:herb_communities.py]

> **TBD**: nilai per-bridge belum diisi karena page ini bootstrap. Lab
> `wiki/labs/bridges/` direncanakan akan mengisi tabel ini sekaligus
> menambahkan halaman entitas individual (lihat [[../SCHEMA.md|SCHEMA §7]]).

## Dua sifat penting bridge

1. **Posisi struktural, bukan absensi**: bridge bukan herba langka. Mereka
   sering muncul; itulah sebabnya diuji dalam algoritma. Yang membuatnya
   bridge adalah *konektivitasnya yang menyebar*, bukan *konektivitasnya yang
   rendah*.

2. **Forbidden pair berkurang di bridge**: 28 dari 30 top-forbidden pair adalah
   cross-mazhab antara dua kluster stabil. **2 forbidden pair** melibatkan
   bridge sebagai salah satu sisinya — angka rendah ini konsisten dengan
   peran *menjembatani*: bridge tidak punya forbidden pair yang banyak karena
   ia kompatibel dengan banyak mazhab. [script:herb_communities.py
   `validate_forbidden_pairs`]

## Visualisasi

Pada `figures/21_mazhab_network.png`, bridges dirender sebagai diamond hitam
berlabel tebal. Posisi mereka di celah antar-cluster warna adalah *visual
literal* dari namanya: Sauropus terlempar ke pojok atas, Blumea di tengah-bawah
di antara S0 (merah) dan S2 (hijau), Woodfordia di tengah, Curcuma zedoaria di
pojok kanan bawah.

[script:src/analysis/visualize_mazhab.py]

## Mengapa ini bukan sekadar artefak algoritma

Pertanyaan reviewer yang valid: *"Bukankah bridge cuma artefak threshold
co-cluster 0.7?"* Tiga argumen:

1. **Parameter sweep mempertahankan struktur bridge**: 60 konfigurasi
   parameter mempertahankan 99.5% forbidden-pair-cross-rate
   [null-tested:99.5%]. Jika bridge adalah artefak, parameter sweep akan
   memunculkan struktur kluster yang berbeda di banyak konfigurasi. Tidak
   terjadi.
2. **Kandidat bridge muncul *sebelum* kami menamai mereka**: lihat docstring
   `src/analysis/herb_communities.py` baris 14–25: hipotesis bridges sebagai
   "honest representation of unstable hub herbs" mendahului naming mereka.
3. **Konsistensi dengan peran fungsional yang sudah independent**: setidaknya
   tiga dari lima bridges (Blumea, Curcuma zedoaria, Woodfordia) punya
   karakter farmakologis yang masuk akal sebagai jembatan antar-domain
   (warming + astringent, atau anti-inflamasi multi-target). Ini adalah
   convergent evidence dari literatur, bukan algoritmik [hypothesis: butuh
   review terstruktur — direncanakan di lab].

## Apa yang menarik untuk diteliti

Sub-proyek "bridge investigation" adalah next obvious step (per
`NOTES_2026-05-03_mazhab_visualization.md` §"Arah Lanjutan"). Untuk tiap bridge:

- Edge-list ke dua mazhab tetangga utama
- Top diseases yang bridge tersebut ko-occur dengan herba di tiap mazhab
- Plant-part dan komposisi kimia dari KNApSAcK
- Apakah bridge tersebut juga "kurir" (universal bioenhancer) atau ada peran
  beda
- Microreview literatur: apakah farmakologi modern mengkonfirmasi peran
  jembatan?

Output: lima halaman entitas (`wiki/entities/herbs/Blumea_balsamifera.md`, dst.)
+ satu halaman synthesis (`wiki/syntheses/why_bridges_matter.md`).

## Open questions

1. Apakah ada *bridge yang seharusnya ada tapi tidak terdeteksi* karena threshold?
   Test: turunkan co-cluster threshold dari 0.7 → 0.5, lihat apakah singleton
   baru muncul yang masuk akal.
2. Apakah bridges berubah jika lift-graph diganti dengan jaccard atau pmi?
   [hypothesis] — alternative-association test masih deferred per
   `NOTES_grammar_schools.md`.
3. Apakah lima bridges saling terhubung satu sama lain? Belum dicek.

## Provenance summary

- [script:src/analysis/herb_communities.py]
- [script:src/analysis/visualize_mazhab.py]
- [source:data/raw/knapsack/knapsack_jamu_formulas.json]
- [null-tested:99.5% via parameter sweep]
- `figures/21_mazhab_network.png`
- `data/kg/jamu_herb_communities.json` field `bridge_singletons`

## See also

- [[forbidden_pairs.md]]
- [[../entities/mazhab/S0_warming_musculoskeletal.md]]
- `NOTES_2026-04-20_grammar_schools.md` §"11 Mazhab Stabil + 5 Bridge Herbs"
- `NOTES_2026-05-03_mazhab_visualization.md` §"Arah Lanjutan"
