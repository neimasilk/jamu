---
type: entity
class: mazhab
canonical_name: "S0"
label: "Musculoskeletal warming + aromatic base"
manifesto_layer: L2
last_updated: 2026-05-07
---

# Mazhab S0 — Warming Musculoskeletal + Aromatic Base

**Mazhab terbesar (25 herba) di jamu, didominasi rhizoma berkarakter hangat dan
biji aromatik. Pusat gravitasi pengobatan muskuloskeletal-tradisional.**

## Identitas

| Field | Value |
|---|---|
| Community ID | 0 |
| Label | Musculoskeletal warming + aromatic base |
| Size | **25 herba** |
| Stability | Konsensus 40-seed Louvain, ARI 0.72 [null-tested] |
| Color in figure 21 | Merah |

[source:data/kg/jamu_herb_communities.json communities[0]]
[script:herb_communities.py]

## Anggota (urut frekuensi)

Top members per `herb_communities.json`:

1. **Zingiber officinale** Rosc — 1,256 formula → [[../herbs/Zingiber_officinale.md]]
2. Kaempferia galanga L. — kencur
3. Foeniculum vulgare Mill. — adas
4. Zingiber aromaticum Val
5. Amomum cardamomum Willd — kapulaga
6. Cinnamomum burmani Bl — kayu manis
7. Myristica fragrans Houtt. — pala
8. Languas galanga (L.) Stuntz — laos
9. Glycyrrhiza glabra L. — akar manis
10. Caryophyllus aromaticus L. — cengkeh
11. Coriandrum sativum L — ketumbar
12. Piper cubeba L.f. — kemukus
13. Mentha arvensis L
14. Carum copticum (L.) Benth
15. Melaleuca cajuputi Powell — kayu putih
16. Zingiber zerumbet SM
17. Oryza sativa L. — beras
18. Baeckea frutescens L.
19. Usnea misaminensis (Vain) Not.
20. Cyperus rotundus L
21. Helicteres isora L.
22. Cymbopogon nardus L. Rendle — sereh
23. Piperis Albi
24. Equisetum debile Roxb.
25. Zingiber amaricans Bl

[source:data/kg/jamu_herb_communities.json communities[0].members]

## Profil farmasetik

| Atribut | Top 5 |
|---|---|
| Plant parts (% occurrence) | Rhizome **44.0%**, Fruit 27.9%, Bark 5.1%, Seed 5.0%, Root 4.0% |
| Effect distribution | Musculoskeletal **17**, Pain/inflammation 3, Female reproductive 2, Gastrointestinal 2 |
| Role distribution | umum 13, **penyeimbang 7**, menteri 2, kurir 2 |

[source:data/kg/jamu_herb_communities.json] [script:herb_communities.py]

Rhizoma-dominasi (44%) + fruit (27.9%) menandai mazhab ini sebagai kategori
*warming-pungent spice cluster*. Konsisten dengan label "aromatic base" — banyak
herba ini juga muncul di mazhab lain sebagai unsur penyeimbang.

## Validasi konvergen

Mazhab S0 lulus dua axis validasi independen:

1. **Plant-part axis (konvergen)**: 44% rhizome adalah enrichment yang kuat
   dibanding distribusi global (rhizome ~25% across all formulas). Mazhab
   ini punya tanda-tangan farmasetik yang jelas. [script:herb_communities.py
   `herb_part_occurrences`]
2. **Taxonomy axis (divergen — informative)**: anggota S0 tersebar di
   Zingiberaceae, Lamiaceae, Apiaceae, Lauraceae, Myristicaceae, Piperaceae,
   Poaceae, Cupressaceae, dll. Family entropy = tinggi.
   [script:herb_taxonomy.py]
   Divergensi ini adalah bukti positif: mazhab S0 *functional*, bukan
   *lineage-based*. Tradisi memilih herba berdasarkan profil sensorik/farmasetik,
   bukan kekerabatan botanis.

[null-tested:konsensus 40-seed ARI 0.72] — kluster ini stabil di parameter
sweep.

## Kontras dengan mazhab lain

| vs | Hubungan |
|---|---|
| **S1** (Female reproductive / astringent) | Banyak forbidden pair antara S0 (warming) dan S1 (astringent). Visualisasi figure 21 menampilkan jurang ini paling jelas. |
| **S2** (GI bitter / hepatoprotective) | Bertetangga dekat di figure 21 — beberapa herba jembatan (terutama bridge Curcuma zedoaria) menghubungkan ke sini. |
| **S3** (GI aromatic-carminative) | Overlap konseptual dengan S0 (juga aromatic) tetapi target therapeutic berbeda. Ko-eksistensi mungkin via Cocos/Eucalyptus. |
| **S5** (Aromatic rhizome bitters, 4 herba) | Bisa dianggap "anak" S0 yang lebih sempit (hanya rhizome bitters). Curcuma xanthorrhiza ada di S5, bukan S0 — meski botani-nya Zingiberaceae sama dengan banyak anggota S0. |

## Open questions

1. Apakah mazhab ini punya sub-struktur (e.g., spice-cluster vs grain-cluster
   dalam S0)? Belum dianalisis [hypothesis].
2. Apakah role-distribution S0 (13 umum + 7 penyeimbang + 2 menteri + 2 kurir)
   tipikal atau atipikal vs mazhab lain? Cek lintas-mazhab belum dilakukan
   [deferred].
3. Apakah Zingiber officinale (anggota S0 paling sentral) seharusnya
   diklasifikasikan sebagai bridge ke mazhab lain mengingat 362 partner-nya?
   Kompatibilitas tinggi tidak menggugurkan keanggotaannya di S0 secara
   konsensus, tapi pertanyaan tetap menarik.

## Provenance summary

- [source:data/kg/jamu_herb_communities.json communities[0]]
- [script:src/analysis/herb_communities.py] — clustering
- [script:src/analysis/herb_taxonomy.py] — family entropy
- [null-tested:konsensus 40-seed]
- `figures/22_mazhab_small_multiples.png` — internal lift edges (211 edges
  internal di S0)

## See also

- [[../herbs/Zingiber_officinale.md]] (anggota paling sentral)
- [[../../concepts/forbidden_pairs.md]]
- [[../../concepts/bridge_herb.md]]
- `NOTES_2026-04-20_grammar_schools.md` §"11 Mazhab Stabil"
