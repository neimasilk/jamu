"""
Dr. Duke's Phytochemical & Ethnobotanical Database Loader
=========================================================
Loads and filters Dr. Duke's CC0 database for Indonesian/SE Asian plants.
Extracts: plants, compounds, bioactivities, ethnobotanical uses.
"""

import os
import sys
from pathlib import Path

import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.schema import (
    PlantNode, CompoundNode, DiseaseNode, BioactivityNode,
    KGEdge, EdgeType, EvidenceLevel, SourceDB, make_node_id,
)
from src.kg.builder import JamuKG

# Countries/regions relevant to Indonesian/Nusantara traditional medicine
NUSANTARA_COUNTRIES = [
    "Java", "Sumatra", "Borneo", "Indonesia", "Malaya", "Malaysia",
    "Indochina", "Philippines", "Bali", "Celebes", "Molucca",
]

# Broader SE Asian filter (for compound data — less restrictive)
SE_ASIAN_REGIONS = NUSANTARA_COUNTRIES + [
    "Thailand", "Vietnam", "Burma", "Myanmar", "Cambodia", "Laos",
    "India", "China",  # Include for cross-reference
]


def load_taxonomy(duke_dir: str) -> pd.DataFrame:
    """Load plant taxonomy from FNFTAX.csv."""
    path = os.path.join(duke_dir, "FNFTAX.csv")
    df = pd.read_csv(path, encoding="latin-1")
    df.columns = df.columns.str.strip()
    # Build canonical taxon name
    df["taxon_clean"] = df["TAXON"].str.strip()
    df["genus"] = df["GENUS"].str.strip()
    df["species"] = df["SPECIES"].str.strip()
    df["family"] = df["FAMILY"].str.strip()
    return df


def load_ethnobotany(duke_dir: str) -> pd.DataFrame:
    """Load ethnobotanical uses from ETHNOBOT.csv."""
    path = os.path.join(duke_dir, "ETHNOBOT.csv")
    df = pd.read_csv(path, encoding="latin-1")
    df.columns = df.columns.str.strip()
    df["country_clean"] = df["COUNTRY"].str.strip()
    df["taxon_clean"] = df["TAXON"].str.strip()
    df["activity_clean"] = df["ACTIVITY"].str.strip()
    return df


def load_plant_chemicals(duke_dir: str) -> pd.DataFrame:
    """Load plant-chemical associations from FARMACY_NEW.csv."""
    path = os.path.join(duke_dir, "FARMACY_NEW.csv")
    df = pd.read_csv(path, encoding="latin-1", low_memory=False)
    df.columns = df.columns.str.strip()
    return df


def load_chemical_activities(duke_dir: str) -> pd.DataFrame:
    """Load chemical-activity associations from AGGREGAC.csv."""
    path = os.path.join(duke_dir, "AGGREGAC.csv")
    df = pd.read_csv(path, encoding="latin-1")
    df.columns = df.columns.str.strip()
    return df


def load_chemicals(duke_dir: str) -> pd.DataFrame:
    """Load chemical info from CHEMICALS.csv."""
    path = os.path.join(duke_dir, "CHEMICALS.csv")
    df = pd.read_csv(path, encoding="latin-1")
    df.columns = df.columns.str.strip()
    return df


def load_common_names(duke_dir: str) -> pd.DataFrame:
    """Load common/local names from COMMON_NAMES.csv."""
    path = os.path.join(duke_dir, "COMMON_NAMES.csv")
    df = pd.read_csv(path, encoding="latin-1")
    df.columns = df.columns.str.strip()
    return df


def load_parts(duke_dir: str) -> pd.DataFrame:
    """Load plant part codes from PARTS.csv."""
    path = os.path.join(duke_dir, "PARTS.csv")
    df = pd.read_csv(path, encoding="latin-1")
    df.columns = df.columns.str.strip()
    return df


def filter_nusantara_ethnobotany(ethno_df: pd.DataFrame) -> pd.DataFrame:
    """Filter ethnobotany for Nusantara/Indonesian region."""
    pattern = "|".join(NUSANTARA_COUNTRIES)
    mask = ethno_df["country_clean"].str.contains(pattern, case=False, na=False)
    return ethno_df[mask].copy()


def get_nusantara_plant_set(ethno_nusantara: pd.DataFrame) -> set:
    """Get the set of plant taxon names used in Nusantara."""
    return set(ethno_nusantara["taxon_clean"].dropna().unique())


def build_duke_kg(duke_dir: str) -> JamuKG:
    """
    Build a JamuKG from Dr. Duke's database.

    Strategy:
    1. Load ethnobotany, filter to Nusantara plants
    2. For those plants, load their chemical constituents
    3. For those chemicals, load their bioactivities
    4. Build the KG
    """
    kg = JamuKG()
    source = SourceDB.DUKE.value

    print("Loading Dr. Duke's database...")
    taxonomy = load_taxonomy(duke_dir)
    ethno = load_ethnobotany(duke_dir)
    farmacy = load_plant_chemicals(duke_dir)
    chem_act = load_chemical_activities(duke_dir)
    chemicals = load_chemicals(duke_dir)
    parts = load_parts(duke_dir)
    common_names = load_common_names(duke_dir)

    # Build parts lookup
    parts_lookup = dict(zip(parts["PPCO"].str.strip(), parts["PPNA"].str.strip()))

    # Build FNFNUM -> taxon lookup
    fnf_to_taxon = dict(zip(taxonomy["FNFNUM"], taxonomy["taxon_clean"]))
    fnf_to_family = dict(zip(taxonomy["FNFNUM"], taxonomy["family"]))

    # Step 1: Filter ethnobotany to Nusantara
    ethno_nusantara = filter_nusantara_ethnobotany(ethno)
    nusantara_plants = get_nusantara_plant_set(ethno_nusantara)
    print(f"  Nusantara ethnobotany entries: {len(ethno_nusantara)}")
    print(f"  Unique Nusantara plants: {len(nusantara_plants)}")

    # Step 2: Add plant nodes
    taxon_to_family = dict(zip(taxonomy["taxon_clean"], taxonomy["family"]))
    for plant_name in nusantara_plants:
        family = taxon_to_family.get(plant_name, "")
        node = PlantNode(
            node_id=make_node_id(plant_name),
            latin_name=plant_name,
            family=family if pd.notna(family) else "",
            sources=[source],
        )
        kg.add_plant(node)

    # Step 3: Add ethnobotanical uses (plant -> treats -> activity/disease)
    for _, row in ethno_nusantara.iterrows():
        plant_name = row["taxon_clean"]
        activity = row["activity_clean"]
        if pd.isna(plant_name) or pd.isna(activity):
            continue

        plant_id = make_node_id(plant_name)

        # Add disease/activity node
        disease_id = make_node_id(activity)
        disease = DiseaseNode(
            node_id=disease_id,
            name=activity,
            sources=[source],
        )
        kg.add_disease(disease)

        # Add TREATS edge
        edge = KGEdge(
            source_id=plant_id,
            target_id=disease_id,
            edge_type=EdgeType.TREATS,
            source_db=source,
            confidence=0.7,  # Ethnobotanical claim, not clinically validated
        )
        kg.add_edge(edge)

    # Step 4: Add plant-chemical associations
    # Filter farmacy to Nusantara plants (via FNFNUM)
    nusantara_fnfnums = set(
        taxonomy[taxonomy["taxon_clean"].isin(nusantara_plants)]["FNFNUM"]
    )
    farmacy_nusantara = farmacy[farmacy["FNFNUM"].isin(nusantara_fnfnums)]
    print(f"  Plant-chemical entries for Nusantara plants: {len(farmacy_nusantara)}")

    chem_set = set()
    for _, row in farmacy_nusantara.iterrows():
        fnfnum = row["FNFNUM"]
        chem_name = str(row.get("CHEM", "")).strip()
        if not chem_name or chem_name == "nan":
            continue

        plant_name = fnf_to_taxon.get(fnfnum, "")
        if not plant_name:
            continue

        plant_id = make_node_id(plant_name)
        chem_id = make_node_id(chem_name)

        # Add compound node
        if chem_id not in chem_set:
            cas = str(row.get("CHEMID", "")).strip()
            compound = CompoundNode(
                node_id=chem_id,
                name=chem_name,
                cas_number=cas if cas != "nan" else "",
                sources=[source],
            )
            kg.add_compound(compound)
            chem_set.add(chem_id)

        # Add PRODUCES edge
        edge = KGEdge(
            source_id=plant_id,
            target_id=chem_id,
            edge_type=EdgeType.PRODUCES,
            source_db=source,
        )
        kg.add_edge(edge)

    # Step 5: Add chemical -> bioactivity associations
    nusantara_chems = set(farmacy_nusantara["CHEM"].dropna().str.strip().unique())
    chem_act_filtered = chem_act[chem_act["CHEM"].str.strip().isin(nusantara_chems)]
    print(f"  Chemical-activity entries: {len(chem_act_filtered)}")

    for _, row in chem_act_filtered.iterrows():
        chem_name = str(row["CHEM"]).strip()
        activity = str(row["ACTIVITY"]).strip()
        if not chem_name or not activity or activity == "nan":
            continue

        chem_id = make_node_id(chem_name)
        act_id = make_node_id(activity)

        # Add bioactivity node
        bioact = BioactivityNode(
            node_id=act_id,
            name=activity,
            sources=[source],
        )
        kg.add_bioactivity(bioact)

        # Add HAS_ACTIVITY edge
        edge = KGEdge(
            source_id=chem_id,
            target_id=act_id,
            edge_type=EdgeType.HAS_ACTIVITY,
            source_db=source,
        )
        kg.add_edge(edge)

    return kg


def main():
    """Main entry point."""
    duke_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "duke_csv")
    duke_dir = os.path.abspath(duke_dir)

    if not os.path.exists(duke_dir):
        print(f"Error: Duke CSV directory not found at {duke_dir}")
        print("Please download Duke-Source-CSV.zip first.")
        return

    kg = build_duke_kg(duke_dir)

    # Print stats
    stats = kg.stats()
    print("\n=== JamuKG from Dr. Duke's ===")
    print(f"Total nodes: {stats['total_nodes']}")
    print(f"Total edges: {stats['total_edges']}")
    print("Nodes by type:")
    for ntype, count in sorted(stats["nodes_by_type"].items()):
        print(f"  {ntype}: {count}")
    print("Edges by type:")
    for etype, count in sorted(stats["edges_by_type"].items()):
        print(f"  {etype}: {count}")

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "entities", "duke_kg.json")
    output_path = os.path.abspath(output_path)
    kg.save(output_path)
    print(f"\nSaved to {output_path}")

    return kg


if __name__ == "__main__":
    main()
