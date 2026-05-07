# Catatan Sesi — Pipeline Integration & Figures Regeneration (v08)

**Tanggal**: 7 Mei 2026
**Mode**: otomatis (user busy; akan review kemudian)
**Tujuan**: tutup item infrastruktur (f) dari handoff — `run_full_pipeline.py` predates v08, sehingga rerun pipeline akan kehilangan ontology split. Sekaligus regenerasi figures 00–17 dengan data v08.

Konteks tambahan: user mendeklarasikan tujuan **HKI** (Hak Kekayaan Intelektual / DJKI Hak Cipta atas Program Komputer + Basis Data) di awal sesi. Reproduktibilitas pipeline jadi load-bearing untuk pendaftaran software, bukan sekadar nice-to-have.

---

## Ringkasan Perubahan

| File | Perubahan | Alasan |
|---|---|---|
| `run_full_pipeline.py` | Tambah `step4_apply_ontology(version)`; renumber visualize→step5, stats→step6; step5 sekarang call tiga modul figure (visualize + network_pharmacology + formulation_analysis) bukan satu | Pipeline harus produce v08-style output end-to-end; figures 00–17 harus regen otomatis |
| `src/kg/builder.py` | `JamuKG.save/load` pakai `edges="links"` eksplisit; load tolerant terhadap kedua konvensi | NetworkX 3.6+ default key berubah dari `links` → `edges`; existing artifact pakai `links`; tanpa fix, load v08 fail dengan `KeyError: 'edges'` |
| `src/analysis/network_pharmacology.py` | `main()` auto-detect KG terbaru via glob+sort, bukan hardcoded `jamukg_v02_*` | Hardcode lama bikin script crash setelah v02 obsolete |
| `figures/00–17` (kecuali 18, 19, 20) | Regenerated dari v08 KG | Sebelumnya stale dari v07 |

**Tidak diubah**:
- `MANUSCRIPT.md` — sesuai prinsip "no MANUSCRIPT edit tanpa konteks deliberasi dulu"
- `figures/21+22` (mazhab) — sudah final dari sesi 3 Mei
- `figures/18, 19, 20` — tidak ada generator script di `src/`; dibiarkan as-is dengan timestamp lama (perlu dilacak siapa generator-nya di sesi lain)
- `data/kg/jamukg_v07*` dan `v08_annotated.json` — historis, tidak disentuh

---

## Verifikasi

1. **Syntax check** `run_full_pipeline.py`: ✓ `python -c "import ast; ast.parse(...)"`
2. **Functional check** step4 logic: jalankan `build_node_to_category` + `apply_split` di-memory pada `jamukg_v07_annotated.json`. Hasil identik dengan `data/kg/v08_ontology_split_report.json` yang sudah ada:
   - 651 disease nodes mapped, 0 unmapped
   - 8,931 → 6,923 TREATS + 1,387 HAS_USE + 407 ETHNOBOTANICAL_USE + 214 APPLIED_TO ✓
3. **Figure regeneration** end-to-end:
   - `python -m src.analysis.visualize` → 01-08 + 3 interactive HTML
   - `python -m src.analysis.network_pharmacology` → 09-11
   - `python -m src.analysis.formulation_analysis` → 12-17, 00
   - Total 17 PNG di `figures/` dengan timestamp 2026-05-07, semua dari `jamukg_v08_annotated.json`

Tidak rerun full pipeline (step1-6) karena step1-3 butuh raw data harvest yang tidak relevan untuk validasi infrastruktur ini. Step4 (ontology) dan step5 (figures) sudah divalidasi terpisah; struktur step1-3 tidak diubah.

---

## Side-Findings (Honest)

### 1. Dependency hygiene
Env user tidak punya `seaborn` (dan beberapa lainnya dari `requirements.txt`) — kemungkinan recovery pasca-petir belum lengkap. Saya install: `seaborn`, `pyvis`, `biopython`, `tqdm`, `pyyaml`, `beautifulsoup4`, `pdfplumber`. Setelah install, semua script jalan.

Untuk HKI: requirements.txt sudah benar, tapi user perlu `pip install -r requirements.txt` di env yang clean. Tidak ada problem desain.

### 2. NetworkX version drift
NetworkX 3.4 mengubah default `node_link_data/graph` edges-key dari `"links"` ke `"edges"`. Existing artifact KG pakai `"links"`. Tanpa fix di `builder.py`, load v08 crash. Sekarang save dan load eksplisit pakai `"links"` untuk backward-compat dengan `apply_disease_ontology.py` (yang baca JSON langsung tanpa networkx).

Implikasi reproduktibilitas: konvensi `"links"` di-pin di `builder.py`. Jika seseorang upgrade networkx ke versi yang nanti deprecate `edges=` arg, perlu attention. Tapi untuk sekarang, stable.

### 3. Path hardcoding di `network_pharmacology.py`
Old code: `kg_path = kg_dir / "jamukg_v02_normalized.json"` — pre-v07 era. Sekarang auto-detect via glob+sort, konsisten dengan `visualize.py` dan `formulation_analysis.py`.

### 4. Figures 18, 19, 20
Tidak ada generator di `src/`. Mereka dihasilkan ad-hoc (mungkin di notebook) dan disimpan ke `figures/`. Untuk HKI / reproduktibilitas, sebaiknya dilacak siapa generator-nya dan di-port ke `src/analysis/` di sesi terpisah. Bukan blocker sekarang karena filenya ada (sekedar stale).

---

## Pipeline Sekarang (After This Session)

```
python run_full_pipeline.py
  step1: sync KNApSAcK checkpoint
  step2: rebuild KG -> jamukg_vXX.json (auto-versioned)
  step3: annotate evidence -> jamukg_vXX_annotated.json
  step4: apply ontology -> overwrite jamukg_vXX_annotated.json + write report
  step5: visualize (3 modules: figs 01-17 + 00)
  step6: final stats
```

Dari sini, "annotated" SELALU berarti "PubMed-evidence + ontology-split". Tidak perlu file `_v0X` dan `_v0(X+1)_annotated` terpisah seperti dulu (v07 → v08).

---

## Yang Tidak Dilakukan (Deliberately)

1. **Tidak rerun step1-3** (rebuild KG dari raw): butuh KNApSAcK API dan PubMed query yang bisa berjam-jam dan butuh budget. v08_annotated yang ada sudah valid; cukup memvalidasi step4-5 yang baru.
2. **Tidak update MANUSCRIPT.md** dengan figure-figure baru: prinsip handoff melarang edit tanpa deliberasi. Figure baru identik visual dengan yang lama (v08 sudah dipakai sebelumnya), jadi tidak ada delta klaim.
3. **Tidak generate figures 18, 19, 20**: tidak ada generator. Track issue terpisah.
4. **Tidak refactor visualize.py untuk drop seaborn**: di luar scope; dependency sudah terinstall.
5. **Tidak buat `requirements-pinned.txt` atau `pip freeze` snapshot**: berguna untuk HKI tapi sebaiknya dilakukan setelah env benar-benar stable.

---

## Arah Lanjutan (Untuk Sesi Berikutnya)

Sekarang opsi (d) mazhab viz [done 3 Mei] dan (f) pipeline integration [done hari ini] sudah selesai. Yang tersisa di handoff:

1. **(c) Bridge herb investigation** — masih relevan; sekarang figure 21 menunjukkan posisi mereka. 1 sesi pendek bisa selesai jadi 1 short section.
2. **(a) Synergy prediction** — perlu PubMed query untuk bioenhancement literature; effort menengah.
3. **(b) Piperaceae / TCM-island case study** — bagus untuk short paper; data sudah cukup, tinggal narasi.
4. **(e) PubMed query-quality improvement** — masih hutang metodologis lama; high-effort, high-reward.
5. **HKI registration prep** — bundling JamuKG sebagai Hak Cipta software + database. Setelah pipeline integration ini, technical bar terpenuhi. Yang perlu disiapkan: dokumen deskripsi sistem (1-2 halaman), screenshot pipeline jalan, sample output, lampiran source code archive.

Catatan untuk meta: setelah sesi ini, orbit "pipeline & infrastructure" sudah closed. Sesi berikutnya boleh kembali ke analytical work (bridge herbs, synergy, dll.) tanpa khawatir prinsip "3+ sesi narrow exploration" — karena sesi ini break dari mazhab orbit.

---

## File yang Dihasilkan / Dimodifikasi Sesi Ini

- `run_full_pipeline.py` — added step4 (ontology), renumbered, expanded step5
- `src/kg/builder.py` — networkx-version-tolerant save/load
- `src/analysis/network_pharmacology.py` — auto-detect latest KG
- `figures/00, 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17` — regenerated
- `figures/interactive_*.html` — regenerated
- `data/kg/network_pharmacology_results.json` — regenerated dari v08
- `NOTES_2026-05-07_pipeline_integration.md` — dokumen ini

Tidak ada `data/kg/v0X_ontology_split_report.json` baru karena tidak rerun pipeline; existing `v08_ontology_split_report.json` masih valid (count tervalidasi identik).
