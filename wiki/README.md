---
type: meta
last_updated: 2026-05-07
---

# JamuKG Wiki

LLM-maintained knowledge wiki for the JamuKG research project. Adapted from
[Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
with kearifan lokal — see [SCHEMA.md](SCHEMA.md) for the maintenance contract.

## Pembagian kerja

- **User**: kurasi sumber, ajukan pertanyaan, deliberasi, lihat hasil. Open
  Obsidian (atau editor markdown apapun) dan jelajahi wiki seperti baca buku.
- **Claude**: tulis halaman, update cross-reference, flag kontradiksi, jalankan
  lint per sesi, file synthesis dari query. Tidak menulis MANUSCRIPT.md tanpa
  deliberasi (lihat `CLAUDE.md` G1).

## Cara navigasi

Mulai dari salah satu:

1. **[index.md](index.md)** — katalog semua halaman, dikelompokkan per
   kategori. Cara cepat menemukan halaman tertentu.
2. **[log.md](log.md)** — kronologi sesi. Apa yang terakhir dikerjakan.
3. **`grep -r "keyword" wiki/`** — full-text search.

## Hubungan dengan dokumen kanonik

Wiki ini **menambah**, tidak menggantikan, dokumen-dokumen di root proyek:

| Dokumen kanonik | Posisi vs wiki |
|---|---|
| [`MANIFESTO_FARMAKOPE_NUSANTARA.md`](../MANIFESTO_FARMAKOPE_NUSANTARA.md) | Visi 4-layer. Wiki men-tag tiap halaman dengan `manifesto_layer`. |
| [`HANDOFF.md`](../HANDOFF.md) | State terkini. Dibaca di awal tiap sesi. |
| [`MANUSCRIPT.md`](../MANUSCRIPT.md) | Draft paper. Tidak diedit tanpa deliberasi. |
| [`TRIAGE.md`](../TRIAGE.md) | Deliberasi prioritas. Wiki me-link, tidak duplicate. |
| [`PAPER_DRAFT.md`](../PAPER_DRAFT.md) | Versi pendek, terpisah. |
| `NOTES_*.md` | Laporan per-sesi. [log.md](log.md) merangkum kronologi-nya. |
| [`data_audit_jamu_sources.md`](../data_audit_jamu_sources.md) | Audit data sources. Wiki source-page me-link. |
| [`literature_review_computational_jamu.md`](../literature_review_computational_jamu.md) | Tinjauan literatur. Tidak dipindah. |

## Struktur folder

```
wiki/
  README.md         ← anda di sini
  SCHEMA.md         ← keystone — kontrak maintenance
  index.md          ← katalog content-oriented
  log.md            ← kronologi append-only
  concepts/         ← ide & metode (validation_gap, forbidden_pairs, …)
  entities/         ← named individuals (herbs, mazhab, diseases)
    herbs/
    mazhab/
  sources/          ← raw data sources (knapsack, duke, pubmed, …)
  syntheses/        ← jawaban panjang dari query yang naik kelas jadi halaman
  labs/             ← (future) bounded sub-project workspaces
```

## Status saat ini (May 2026)

Wiki masih **bootstrapped, tidak exhaustive**. Karpathy: *"wiki grows with
use, ingest one source at a time"*. Lihat [SCHEMA.md §7 Roadmap](SCHEMA.md#7-roadmap)
untuk apa yang akan ditambah.
