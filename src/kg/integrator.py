"""
JamuKG Integrator
=================
Merges data from all harvested sources into a unified JamuKG.
Sources: Dr. Duke's, KNApSAcK, Farmakope Herbal Indonesia.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.schema import (
    PlantNode, CompoundNode, DiseaseNode, FormulationNode,
    BioactivityNode, KGEdge, EdgeType, EvidenceLevel, SourceDB,
    make_node_id,
)
from src.kg.builder import JamuKG


# --- Name normalization helpers ---

# Common Indonesian plant name -> Latin name mappings
# Built from Farmakope + KNApSAcK data
INDO_TO_LATIN = {
    "kunyit": "Curcuma longa",
    "jahe": "Zingiber officinale",
    "kencur": "Kaempferia galanga",
    "temulawak": "Curcuma xanthorrhiza",
    "lengkuas": "Alpinia galanga",
    "lempuyang": "Zingiber zerumbet",
    "temu kunci": "Boesenbergia rotunda",
    "temu ireng": "Curcuma aeruginosa",
    "kunir putih": "Kaempferia rotunda",
    "cengkeh": "Syzygium aromaticum",
    "kayu manis": "Cinnamomum verum",
    "sirih": "Piper betle",
    "kumis kucing": "Orthosiphon aristatus",
    "sambiloto": "Andrographis paniculata",
    "mengkudu": "Morinda citrifolia",
    "pegagan": "Centella asiatica",
    "meniran": "Phyllanthus niruri",
    "lidah buaya": "Aloe vera",
    "jambu biji": "Psidium guajava",
    "daun salam": "Syzygium polyanthum",
    "pasak bumi": "Eurycoma longifolia",
    "pare": "Momordica charantia",
    "manggis": "Garcinia mangostana",
    "mimba": "Azadirachta indica",
    "jinten hitam": "Nigella sativa",
    "jeruk purut": "Citrus hystrix",
    "asam jawa": "Tamarindus indica",
    "bawang merah": "Allium cepa",
    "bawang putih": "Allium sativum",
    "cabe rawit": "Capsicum frutescens",
    "belimbing manis": "Averrhoa carambola",
    "belimbing wuluh": "Averrhoa bilimbi",
    "pandan": "Pandanus amaryllifolius",
    "pepaya": "Carica papaya",
    "stevia": "Stevia rebaudiana",
    "alang-alang": "Imperata cylindrica",
}


def normalize_latin_name(name: str) -> str:
    """Normalize a Latin binomial to consistent format."""
    # Remove author names (anything after the second word)
    parts = name.strip().split()
    if len(parts) >= 2:
        genus = parts[0].capitalize()
        species = parts[1].lower()
        return f"{genus} {species}"
    return name.strip()


def load_duke_kg(path: str) -> JamuKG:
    """Load the Duke-derived KG."""
    kg = JamuKG()
    kg.load(path)
    return kg


def load_knapsack_data(formulas_path: str, effects_path: str = None) -> dict:
    """Load KNApSAcK harvested data."""
    with open(formulas_path, "r", encoding="utf-8") as f:
        formulas = json.load(f)

    effects = {}
    if effects_path and os.path.exists(effects_path):
        with open(effects_path, "r", encoding="utf-8") as f:
            effects_list = json.load(f)
            effects = {e["sid"]: e for e in effects_list if "sid" in e}

    return {"formulas": formulas, "effects": effects}


def load_farmakope_data(path: str) -> list[dict]:
    """Load Farmakope parsed monographs."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def integrate_knapsack(kg: JamuKG, knapsack_data: dict):
    """Add KNApSAcK data to the KG."""
    source = SourceDB.KNAPSACK.value
    formulas = knapsack_data["formulas"]
    effects = knapsack_data["effects"]

    print(f"Integrating {len(formulas)} KNApSAcK formulas...")

    for formula in formulas:
        jamu_id = formula["jamu_id"]
        jamu_name = formula.get("jamu_name", "")
        if not jamu_name:
            continue

        # Add formulation node
        form_id = make_node_id(f"knapsack_{jamu_id}")
        form_node = FormulationNode(
            node_id=form_id,
            name=jamu_name,
            source_db=source,
            description=formula.get("jamu_effect", ""),
            sources=[source],
        )
        kg.add_formulation(form_node)

        # Add disease from effect group
        effect_group = formula.get("jamu_effect_group", "")
        if effect_group and effect_group != "-":
            disease_id = make_node_id(effect_group)
            disease = DiseaseNode(
                node_id=disease_id,
                name=effect_group,
                sources=[source],
            )
            kg.add_disease(disease)
            kg.add_edge(KGEdge(
                source_id=form_id,
                target_id=disease_id,
                edge_type=EdgeType.TREATS,
                source_db=source,
            ))

        # Add herbs and CONTAINS edges
        for herb in formula.get("herbs", []):
            sci_name = herb.get("scientific_name", "")
            local_name = herb.get("local_name_id", "")

            if sci_name:
                latin = normalize_latin_name(sci_name)
                plant_id = make_node_id(latin)
                plant = PlantNode(
                    node_id=plant_id,
                    latin_name=latin,
                    local_names={"indonesia": local_name} if local_name else {},
                    sources=[source],
                )
                kg.add_plant(plant)

                # CONTAINS edge: formulation -> plant
                kg.add_edge(KGEdge(
                    source_id=form_id,
                    target_id=plant_id,
                    edge_type=EdgeType.CONTAINS,
                    source_db=source,
                ))

                # If we have effect data for this herb, add TREATS edges
                sid = herb.get("effect_sid", "")
                if sid and sid in effects:
                    effect_text = effects[sid].get("effect", "")
                    if effect_text and effect_text != "-":
                        # Parse effect text into individual uses
                        # Effects are comma/semicolon separated
                        uses = [u.strip() for u in effect_text.replace(";", ",").split(",") if u.strip()]
                        for use in uses[:10]:  # Limit to avoid noise
                            use_id = make_node_id(use)
                            disease = DiseaseNode(
                                node_id=use_id,
                                name=use,
                                sources=[source],
                            )
                            kg.add_disease(disease)
                            kg.add_edge(KGEdge(
                                source_id=plant_id,
                                target_id=use_id,
                                edge_type=EdgeType.TREATS,
                                source_db=source,
                                evidence_text=effect_text[:200],
                            ))


def integrate_farmakope(kg: JamuKG, monographs: list[dict]):
    """Add Farmakope data to the KG."""
    source = SourceDB.FARMAKOPE.value

    print(f"Integrating {len(monographs)} Farmakope monographs...")

    for mono in monographs:
        sci_name = mono.get("scientific_name", "")
        indo_name = mono.get("indonesian_name", "")
        chem_identity = mono.get("chemical_identity", "")
        family = mono.get("family", "")
        plant_part = mono.get("plant_part", "")

        if not sci_name and not indo_name:
            continue

        # Resolve plant
        if sci_name:
            latin = normalize_latin_name(sci_name)
        elif indo_name:
            # Try to map from Indonesian name
            indo_lower = indo_name.lower().replace("daun ", "").replace("akar ", "").replace(
                "rimpang ", "").replace("buah ", "").replace("biji ", "").replace(
                "bunga ", "").replace("herba ", "").replace("kulit buah ", "").replace(
                "pulpa ", "").replace("kayu ", "").replace("umbi lapis ", "").strip()
            latin = INDO_TO_LATIN.get(indo_lower, "")
            if not latin:
                latin = indo_name  # Use Indonesian name as fallback

        if not latin:
            continue

        plant_id = make_node_id(latin if " " in latin else indo_name)
        local_names = {}
        if indo_name:
            # Clean the Indonesian name (remove part prefix)
            clean_indo = indo_name
            for prefix in ["Daun ", "Akar ", "Rimpang ", "Buah ", "Biji ",
                          "Bunga ", "Herba ", "Kulit Buah ", "Pulpa ", "Kayu ",
                          "Umbi Lapis "]:
                if clean_indo.startswith(prefix):
                    clean_indo = clean_indo[len(prefix):]
                    break
            local_names["indonesia"] = clean_indo

        plant = PlantNode(
            node_id=plant_id,
            latin_name=normalize_latin_name(sci_name) if sci_name else "",
            family=family,
            local_names=local_names,
            sources=[source],
        )
        kg.add_plant(plant)

        # Add chemical identity compound
        if chem_identity:
            # May contain multiple compounds separated by ; or ,
            for chem_name in chem_identity.replace(";", ",").split(","):
                chem_name = chem_name.strip()
                if not chem_name or len(chem_name) < 2:
                    continue
                chem_id = make_node_id(chem_name)
                compound = CompoundNode(
                    node_id=chem_id,
                    name=chem_name,
                    sources=[source],
                )
                kg.add_compound(compound)
                kg.add_edge(KGEdge(
                    source_id=plant_id,
                    target_id=chem_id,
                    edge_type=EdgeType.PRODUCES,
                    source_db=source,
                ))


def build_integrated_kg() -> JamuKG:
    """Build the unified JamuKG from all sources."""
    base_dir = Path(__file__).parent.parent.parent
    processed = base_dir / "data" / "processed" / "entities"
    raw = base_dir / "data" / "raw"

    # Start with Duke KG as base (largest source)
    duke_path = processed / "duke_kg.json"
    if duke_path.exists():
        print("Loading Dr. Duke's KG as base...")
        kg = load_duke_kg(str(duke_path))
        stats = kg.stats()
        print(f"  Base: {stats['total_nodes']} nodes, {stats['total_edges']} edges")
    else:
        print("Warning: Duke KG not found, starting empty")
        kg = JamuKG()

    # Add KNApSAcK data
    knapsack_formulas = raw / "knapsack" / "knapsack_jamu_formulas.json"
    knapsack_effects = raw / "knapsack" / "knapsack_herb_effects.json"
    if knapsack_formulas.exists():
        knapsack_data = load_knapsack_data(
            str(knapsack_formulas),
            str(knapsack_effects) if knapsack_effects.exists() else None,
        )
        integrate_knapsack(kg, knapsack_data)
    else:
        print("Warning: KNApSAcK data not found")

    # Add Farmakope data
    farmakope_path = processed / "farmakope_monographs.json"
    if farmakope_path.exists():
        monographs = load_farmakope_data(str(farmakope_path))
        integrate_farmakope(kg, monographs)
    else:
        print("Warning: Farmakope data not found")

    return kg


def main():
    """Build and save the integrated JamuKG."""
    kg = build_integrated_kg()

    # Print stats
    stats = kg.stats()
    print("\n" + "=" * 60)
    print("JamuKG v0.1 — Integrated Knowledge Graph")
    print("=" * 60)
    print(f"Total nodes: {stats['total_nodes']:,}")
    print(f"Total edges: {stats['total_edges']:,}")
    print(f"Connected components: {stats['connected_components']:,}")
    print("\nNodes by type:")
    for ntype, count in sorted(stats["nodes_by_type"].items(), key=lambda x: -x[1]):
        print(f"  {ntype:20s}: {count:>6,}")
    print("\nEdges by type:")
    for etype, count in sorted(stats["edges_by_type"].items(), key=lambda x: -x[1]):
        print(f"  {etype:20s}: {count:>6,}")

    # Save — auto-detect version
    base_dir = Path(__file__).parent.parent.parent
    kg_dir = base_dir / "data" / "kg"

    # Find next version number
    import re
    existing = sorted(kg_dir.glob("jamukg_v*.json"))
    version = "v02"
    for p in existing:
        m = re.match(r"jamukg_(v\d+)\.json$", p.name)
        if m:
            num = int(m.group(1)[1:]) + 1
            version = f"v{num:02d}"

    output_path = kg_dir / f"jamukg_{version}.json"
    kg.save(str(output_path))
    print(f"\nSaved to {output_path}")

    # Also save statistics
    stats_path = kg_dir / f"jamukg_{version}_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    return kg


if __name__ == "__main__":
    main()
