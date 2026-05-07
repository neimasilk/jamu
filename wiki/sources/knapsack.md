---
type: source
location: data/raw/knapsack/knapsack_jamu_formulas.json
size_mb: 8.4
n_records: 5310
license: KNApSAcK family databases — academic use; check source for commercial
last_harvested: 2026-04-16
manifesto_layer: L2
---

# KNApSAcK Jamu Formulations

**Sumber data utama untuk struktur formula jamu di proyek ini.** 5,310 formula
yang valid (dari 5,400 J-codes yang di-enumerate), masing-masing menyebut
beberapa herba dengan plant-part dan posisi.

## Apa itu

KNApSAcK ([http://www.knapsackfamily.com/](http://www.knapsackfamily.com/))
adalah keluarga database metabolomics dan etnobotani yang dimaintain oleh NAIST
(Jepang). Salah satu sub-database-nya adalah katalog formula jamu Indonesia
yang ter-tag dengan ID "J-code" (J0001, J0002, ...). Tiap J-code adalah satu
formula tradisional dengan komposisi herbal eksplisit.

## Struktur record

Tiap formula di `knapsack_jamu_formulas.json` adalah dict dengan field utama:

```json
{
  "id": "J0123",
  "name": "...",
  "indication": "Disorder name as labeled",
  "herbs": [
    {"scientific_name": "Zingiber officinale Rosc",
     "plant_part": "Rhizome",
     "position": 0.987,
     ...},
    ...
  ]
}
```

Posisi (`position`) adalah ordinal dalam daftar bahan, dinormalisasi 0–1.
Plant-part menggunakan kosakata KNApSAcK (Rhizome, Fruit, Bark, dst.).

## Bagaimana kami menggunakannya

Skrip pembaca: `src/harvest/knapsack_harvester.py` (fixed Apr 16 untuk struktur
HTML baru). Output: `data/raw/knapsack/knapsack_jamu_formulas.json`.

Skrip downstream:
- `src/kg/builder.py` — bangun KG, edge type APPLIED_TO/HAS_USE/etc.
  [script:src/kg/builder.py]
- `src/analysis/jamu_grammar.py` — herb roles + forbidden pairs
- `src/analysis/herb_communities.py` — mazhab via consensus-Louvain
- `src/analysis/herb_taxonomy.py` — family entropy per mazhab
- `src/analysis/visualize_mazhab.py` — figure 21 + 22

Setiap analisis utama di proyek ini mengonsumsi file ini sebagai *primary
source of truth* untuk struktur formula. Cleaning/tokenisasi nama herba
tertaut langsung ke KNApSAcK conventions; species-name mismatch dengan
sumber lain (Duke, PubMed) ditangani di `src/extract/entities/` [deferred page].

## Caveat dan kualitas

| Issue | Status | Implikasi |
|---|---|---|
| Indication labels tidak terstandarisasi (campuran istilah klinis, etnobotani, dan kategori non-medis) | **Resolved** lewat `src/analysis/disease_ontology.py` (642 → 636 classified) | KG v08 ontology-split addresses this |
| Beberapa formula adalah produk komersial, bukan "tradisional klasik" | Belum di-flag eksplisit | Mungkin tidak relevan untuk klaim utama, tapi perlu disclosed di paper |
| Posisi formula tidak selalu mencerminkan dosis | Diketahui | Position digunakan sebagai proxy peran (kurir biasanya akhir), bukan dosage |
| Plant-part vocabulary tidak sepenuhnya kongruen dengan literatur farmakognosi modern | Diketahui | Mempengaruhi matching ke Duke ethnobotany |
| Geographical metadata (Java/Bali/Sumatra) tidak ekstraktabel dari record | Diketahui | Tidak bisa stratify mazhab per geography |

[source:knapsack] [script:harvester]

## Coverage di wiki

Halaman wiki yang derive dari sumber ini:
- [[../concepts/forbidden_pairs.md]] — pair extraction
- [[../concepts/bridge_herb.md]] — community membership
- [[../concepts/validation_gap.md]] — denominator base
- [[../entities/herbs/Zingiber_officinale.md]] — herb-level statistik
- [[../entities/mazhab/S0_warming_musculoskeletal.md]] — community profile

## Status maintenance

- **Last harvested**: 2026-04-16. Harvest komplit (semua 5,400 J-code
  di-enumerate). Tidak ada rencana re-harvest kecuali KNApSAcK menambah formula
  baru.
- **Verifikasi integritas**: SHA-256 belum dicatat — TODO untuk lint
  berikutnya. [hypothesis: nilai tidak akan banyak — file di-track di git, jadi
  integrity dijamin git]

## See also

- [[../concepts/validation_gap.md]] — peran formula sebagai denominator
- `data_audit_jamu_sources.md` (root) — audit sumber yang lebih luas
- `src/harvest/knapsack_harvester.py`
