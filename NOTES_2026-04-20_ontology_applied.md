# Catatan Sesi — Ontology Applied to KG (v08)

**Tanggal**: 20 April 2026
**Konteks**: Menyelesaikan TRIAGE Tier 1 item yang tercatat tapi belum dikerjakan: **apply disease ontology to KG**. Tujuan: memisahkan TREATS edges (klaim klinis) dari HAS_USE (penggunaan farmakologis/etnobotanical) supaya claim utama manuskrip ("85.9% validation gap") lebih presisi dan defensible.

---

## Hasil Utama (Honest)

**Yang bekerja sesuai harapan**:
1. Ontologi applied. 8,931 TREATS edges dipisah: 77.5% tetap TREATS (clinical + symptom), 15.5% → HAS_USE (pharm.action + therapeutic.use), 4.6% → ETHNOBOTANICAL_USE (non_medical + biocidal + cosmetic), 2.4% → APPLIED_TO (body_part). Nol edge unmapped.
2. 6 istilah ambiguous terselesaikan dengan review medical-knowledge: **Ozoena**, **Syphilis(3)**, **Typhus (Typhoid)** → clinical_disease. **Internal**, **Medicine**, **Medicine (Vet)** → non_medical. Tercatat eksplisit di `apply_disease_ontology.py` supaya bisa di-kritik/di-review ulang.
3. v08 KG tercipta di `data/kg/jamukg_v08_annotated.json`. Edge lama dipertahankan dengan field `original_edge_type='treats'` + field baru `ontology_category` dan refined `edge_type`.

**Yang tidak sesuai harapan (finding jujur)**:

Angka validation gap *tidak banyak bergeser* setelah cleanup — hanya dari **85.89% → 85.56%** untuk subset TREATS clinical. Gap serupa terlihat di semua kategori:

| Kategori | n | No evidence | Well-studied |
|---|---|---|---|
| TREATS (clinical+symptom) | 3,740 | 85.6% | 1.3% |
| HAS_USE (pharm.action+therapeutic.use) | 1,387 | 87.0% | 1.2% |
| ETHNOBOTANICAL_USE | 407 | 87.5% | 2.2% |
| APPLIED_TO (body_part) | 214 | 81.8% | 1.4% |

Saya sempat mengharapkan angka yang lebih dramatis (naik ke 90%+ atau turun ke 80%) — realita: gap-nya **struktural**. PubMed under-cover tradisi etnobotani apa pun label yang kita beri. Cleanup tidak "discover" gap baru, ia hanya **mempresisikan klaim yang sudah ada**.

---

## Yang Ontologi Cleanup SEBETULNYA Menyelesaikan

Meskipun headline number tidak bergerak, cleanup punya tiga dampak konkret:

### 1. Precision klaim manuskrip

Sebelum: "85.9% of 5,744 traditional plant-disease claims..."
Setelah: "85.6% of 3,740 **clinical** plant-condition claims (TREATS-cleaned), with additional breakdown: 1,387 HAS_USE (pharmacological actions + therapeutic uses, 87% unstudied), 407 ETHNOBOTANICAL_USE (non-medical, cosmetic, biocidal, 87.5% unstudied), 214 APPLIED_TO (body-part targeting, 82% unstudied)."

Reviewer yang teliti tidak bisa lagi menuduh: "Angka 85.9% anda mencampur Arrow-poison dan Cosmetic dengan penyakit klinis."

### 2. Drug discovery candidate list — re-ranking signifikan

Top-30 kandidat DDC lama diurutkan dengan `unstudied_claims` yang mencampur semua kategori. Re-rank dengan `unstudied_clinical_claims` only:
- 22/30 overlap dengan daftar lama
- **8 plants drop out**: Blumea balsamifera, Chloranthus officinalis, Crinum asiaticum, Fagraea racemosa, Hedyotis capitellata, Myristica fragrans, Phyllanthus urinaria, Tinospora tuberculata. Mereka ranked tinggi karena banyak etnobotanical/pharm.action claims, bukan karena klaim klinis.
- **8 plants masuk baru**: Brucea javanica, Caesalpinia sp., Cocos nucifera, Cordyline fruticosa, Gmelina villosa, Michelia champaca, Parkia javanica, Pogostemon heyneanus.

Contoh kontaminasi:
- **Sida rhombifolia**: was rank #1 dengan 21 claims. Sebenarnya 7 clinical + 14 non-clinical. Turun ke rank #3 dengan 16 clinical.
- **Blumea balsamifera**: keluar dari top-30. Kebanyakan claims-nya adalah pharm.action/therapeutic.use, bukan penyakit.

List terkoreksi: `data/kg/drug_discovery_candidates_v08.json`.

### 3. Visibilitas blind spot: KNApSAcK formulation claims

Sampingan dari analisis ini: **3,183 KNApSAcK formulation→effect_group edges memiliki 100% zero PubMed evidence**. Penyebabnya: PubMed harvester hanya query (plant, disease) dari Dr. Duke; formulasi jamu (J00001 "Enolimit", dst) tidak diquery karena tidak ada representasinya di literatur biomedis.

Ini bukan bug — memang secara desain. Tapi layak ditandai sebagai limitation eksplisit di manuskrip. Masa depan: validasi level-formulasi bisa dilakukan dengan *aggregating* evidence dari tanaman-tanaman penyusunnya (e.g., formula J00001 yang punya plants X,Y,Z untuk musculoskeletal "mewarisi" bukti PubMed dari X,Y,Z untuk musculoskeletal).

---

## File Baru Sesi Ini

- `src/analysis/apply_disease_ontology.py` — pipeline reproducible v07 → v08
- `data/kg/jamukg_v08_annotated.json` — KG dengan refined edge types (8,931 TREATS lama dipisah)
- `data/kg/v08_ontology_split_report.json` — statistik split + validation gap per kategori
- `data/kg/drug_discovery_candidates_v08.json` — DDC list re-ranked dengan clinical-only filter
- `NOTES_2026-04-20_ontology_applied.md` — dokumen ini

## Rekomendasi untuk Update Manuskrip (Belum Dilakukan)

1. **Abstract**: ganti "85.9% of 5,744 plant-disease claims" dengan "85.6% of 3,740 clinical plant-condition claims (after ontological cleanup)". Tambahkan 1 kalimat breakdown per kategori.
2. **Methods**: tambahkan subsection "Disease ontology classification and edge splitting" yang menjelaskan 9 kategori + resolusi 6 ambiguous.
3. **Results drug discovery**: ganti top-30 dengan v08 list. Sebutkan bahwa 8 plants dari daftar lama ranked tinggi karena non-clinical uses.
4. **Limitations**: tambah "Formulation-level validation is not performed; the 3,183 KNApSAcK formulation claims are annotated as unstudied by default."

Saya **tidak** menyentuh MANUSCRIPT.md karena prinsipnya "masterpiece, no rush." Rekomendasi di atas bisa dilakukan kapan pun.

## Honest Self-Assessment

Saya sempat berharap ontology cleanup akan menjadi temuan dramatis (e.g., gap naik jadi 90%+). Realita: 85.89% → 85.56%. Itu hasil yang **jujur membosankan** — dan justru signifikan untuk alasan lain: gap-nya bukan artefak label, melainkan struktural. Saya tulis hasilnya tanpa mendramatisir.

Yang lebih impactful dari cleanup: DDC re-ranking, claim precision, dan visibilitas KNApSAcK blind spot. Ketiganya concrete improvements untuk manuskrip masa depan.

Yang belum dilakukan dengan sengaja:
- Tidak menyentuh MANUSCRIPT.md (perlu review manual sebelum edit)
- Tidak query PubMed untuk KNApSAcK formulations (proyek berbeda — butuh design yang terpisah)
- Tidak test apakah grammar-mazhab findings sesi sebelumnya berubah dengan v08 (kemungkinan tidak, karena grammar pakai `jamu_effect_group` bukan TREATS edges — tapi cek eksplisit untuk sesi berikutnya)
