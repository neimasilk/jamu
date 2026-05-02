# Catatan Sesi — Visualisasi Jaringan Mazhab

**Tanggal**: 3 Mei 2026
**Status**: figure 21 + 22 dihasilkan, siap masuk paper

Sesi pendek pasca-recovery (komputer kantor kena petir; semua artifact v08 ter-recover utuh dari git). Tujuan: zoom out dari narrow exploration tiga sesi April (grammar → robustness → ontology) dengan deliverable konkret yang sudah lama "deferred" — visualisasi jaringan mazhab.

## Yang Dihasilkan

| File | Isi |
|---|---|
| `src/analysis/visualize_mazhab.py` | Skrip viz; reuse `build_lift_graph` dari `herb_communities.py` agar grafik yang ditampilkan adalah *grafik yang sama* yang dianalisis Louvain |
| `figures/21_mazhab_network.png` | Full network 106 herb × 1,136 lift edges + 30 forbidden pair overlay |
| `figures/22_mazhab_small_multiples.png` | 9 subnetwork per-mazhab (S0–S8; S9 dan S10 dilewati karena ukuran 2) |

## Apa yang Figure Tunjukkan

**Figure 21 (overview)**:
- 11 mazhab terlihat jelas sebagai cluster warna terpisah di layout spring
- 5 bridge singleton (diamond hitam, label tebal): Sauropus, Curcuma zedoaria, Blumea, Woodfordia, Abrus — masing-masing terletak di celah antar-cluster, bukan di interior salah satu
- 30 forbidden pair (garis putus merah) dominan **memotong** antar-mazhab, bukan di dalam — visualisasi langsung dari klaim Z=37.97 di robustness suite
- S0 (warming musculoskeletal, merah) di pusat — wajar, karena ini cluster terbesar dan banyak herb-nya juga muncul di formula multi-domain

**Figure 22 (per-mazhab detail)**:
- S0 (25 herbs, 211 internal edges): hub Zingiber officinale, Foeniculum, Kaempferia — densitas tinggi
- S1 (25, 149): Curcuma domestica, Alyxia, Piper betle dominan; struktur lebih sparse dari S0
- S2 (16, 69): Andrographis–Centella–Phyllanthus–Orthosiphon — sumbu hepatoprotektif jelas
- S3 (9, 18): Eucalyptus alba sebagai hub sentral GI-aromatic
- S4 (8, 21): Eurycoma + tiga Piper (nigrum, retrofractum) + Tribulus — male tonic
- S5–S8: cluster kecil (3–4 herb) yang masih punya struktur internal
- Visual ini mendukung klaim "mazhab functional, bukan lineage-based": dalam S0, herba dari Zingiberaceae, Lamiaceae, Apiaceae, Lauraceae bercampur

## Keputusan Metodologis

1. **Reuse builder dari herb_communities.py**, bukan rebuild parameter sendiri — agar yang divisualisasikan literally adalah graf yang dianalisis. Kalau parameter beda (misal lift>1.0 atau min_freq=20) figure jadi propaganda ketimbang ilustrasi data.
2. **Forbidden pair overlay opsional**, tetap ditampilkan karena ini visualisasi paling persuasif dari hasil null-model: pembaca tidak perlu paham Z-score untuk melihat bahwa garis merah tidak pernah masuk ke dalam satu kluster warna.
3. **Layout spring seeded (seed=7)** — reproducible. Bukan layout terbaik secara visual tapi stabil dan tidak menyembunyikan hubungan.
4. **Tidak ada normalisasi posisi atau "perbaikan layout manual"** — kalau ada bridge yang terlempar agak jauh (Sauropus, Curcuma zedoaria), itu memang sinyal bahwa algoritma layout tidak dapat memberinya tempat alami. Itulah definisi bridge.

## Yang Tidak Dilakukan (Sengaja)

- **Tidak menambah analisis baru** (sesuai prinsip handoff: "no new analysis tanpa robustness test"). Ini murni visualisasi data yang sudah lulus validasi.
- **Tidak edit MANUSCRIPT.md** (sesuai prinsip handoff: "no MANUSCRIPT edit tanpa konteks deliberasi dulu"). Figure ditambahkan ke `figures/` siap-pakai; integrasi ke paper bisa dilakukan di sesi berikutnya dengan deliberasi terpisah.
- **Tidak generate versi interaktif** (pyvis atau plotly). Figure statis cukup untuk paper. Interaktif mungkin worth it kalau ada deliverable web/dashboard, bukan sekarang.
- **Tidak optimize layout via bobot custom** untuk readability. Mempertahankan default spring biar honest.

## Arah Lanjutan (untuk sesi berikutnya)

Setelah lima opsi handoff (a–f), prioritas relative berdasarkan apa yang sekarang sudah possible:

1. **Bridge herb investigation** — sekarang figure menunjukkan posisi mereka; tinggal probe edge-list spesifik tiap bridge ke dua/tiga mazhab tetangga, lihat efek dominan, lalu tulis micro-narrative tiap bridge (Sauropus → laktasi+GI-bitter; Curcuma zedoaria → warming+female-reproductive; etc.). 5 herb × 1–2 paragraph = 1 short section paper.
2. **Synergy prediction** — masih perlu dataset bioenhancement (PubMed query manual), bisa start dengan pairs lift-tinggi di S0 (warming) dan S1 (reproductive).
3. **PubMed query-quality improvement** — masih untouched, tapi modul kerjanya besar (perlu PubMed API budget + rebuild evidence layer).
4. **Regenerasi figures dengan v08 + integrate ontology ke run_full_pipeline.py** — pekerjaan infrastruktur, perlu satu sesi tersendiri.

Tidak diburu. Santai dalam waktu, serius dalam metodologi.
