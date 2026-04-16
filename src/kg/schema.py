"""
JamuKG Schema Definitions
=========================
Node and edge type definitions for the Jamu Knowledge Graph.
Follows GRAYU/SymMap architecture adapted for Indonesian traditional medicine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --- Node Types ---

class NodeType(str, Enum):
    FORMULATION = "formulation"
    PLANT = "plant"
    PLANT_PART = "plant_part"
    COMPOUND = "compound"
    DISEASE = "disease"
    BIOACTIVITY = "bioactivity"
    ETHNIC_GROUP = "ethnic_group"


class EdgeType(str, Enum):
    CONTAINS = "contains"           # formulation -> plant
    HAS_PART = "has_part"           # plant -> plant_part
    PRODUCES = "produces"           # plant -> compound
    HAS_ACTIVITY = "has_activity"   # compound -> bioactivity
    TREATS = "treats"               # formulation/plant -> disease
    USED_BY = "used_by"             # formulation -> ethnic_group
    MAPS_TO_ICD10 = "maps_to_icd10"


class EvidenceLevel(str, Enum):
    NONE = "none"              # 0 PubMed hits
    LIMITED = "limited"        # 1-5 hits
    MODERATE = "moderate"      # 6-20 hits
    WELL_STUDIED = "well_studied"  # 20+ hits
    CONTRADICTED = "contradicted"  # Evidence against claim


class SourceDB(str, Enum):
    KNAPSACK = "knapsack_jamu"
    DUKE = "dr_duke"
    FARMAKOPE = "farmakope_herbal_indonesia"
    HERBALDB = "herbaldb_ui"
    PUBMED = "pubmed"
    RISTOJA = "ristoja"
    REVIEW_PAPER = "review_paper"


# --- Node Data Classes ---

@dataclass
class PlantNode:
    """A plant species in the knowledge graph."""
    node_id: str                           # Canonical: latin_binomial lowercase, e.g. "curcuma_longa"
    latin_name: str                        # e.g. "Curcuma longa L."
    family: str = ""                       # e.g. "Zingiberaceae"
    local_names: dict = field(default_factory=dict)  # {"indonesia": "kunyit", "jawa": "kunir", ...}
    sources: list = field(default_factory=list)       # [SourceDB.KNAPSACK, SourceDB.DUKE, ...]

    @property
    def node_type(self) -> NodeType:
        return NodeType.PLANT


@dataclass
class CompoundNode:
    """A chemical compound."""
    node_id: str                    # Lowercase normalized, e.g. "curcumin"
    name: str                       # Display name
    cas_number: str = ""            # CAS registry number if available
    formula: str = ""               # Molecular formula
    sources: list = field(default_factory=list)

    @property
    def node_type(self) -> NodeType:
        return NodeType.COMPOUND


@dataclass
class DiseaseNode:
    """A disease or health condition."""
    node_id: str                    # Normalized name, e.g. "diabetes_mellitus"
    name: str                       # Display name
    icd10_code: str = ""            # ICD-10 code if mapped
    icd10_class: str = ""           # ICD-10 disease class
    sources: list = field(default_factory=list)

    @property
    def node_type(self) -> NodeType:
        return NodeType.DISEASE


@dataclass
class FormulationNode:
    """A jamu formulation/product."""
    node_id: str                    # Unique ID from source
    name: str                       # Formula name
    source_db: str = ""             # Which database it came from
    description: str = ""
    sources: list = field(default_factory=list)

    @property
    def node_type(self) -> NodeType:
        return NodeType.FORMULATION


@dataclass
class BioactivityNode:
    """A biological activity."""
    node_id: str                    # e.g. "anti_inflammatory"
    name: str                       # e.g. "Anti-inflammatory"
    sources: list = field(default_factory=list)

    @property
    def node_type(self) -> NodeType:
        return NodeType.BIOACTIVITY


# --- Edge Data Class ---

@dataclass
class KGEdge:
    """An edge in the knowledge graph."""
    source_id: str
    target_id: str
    edge_type: EdgeType
    evidence_level: EvidenceLevel = EvidenceLevel.NONE
    confidence: float = 1.0         # 0-1 confidence score
    source_db: str = ""             # Provenance
    pubmed_ids: list = field(default_factory=list)  # Supporting PMIDs
    evidence_text: str = ""         # Original text evidence


def make_node_id(name: str) -> str:
    """Create a canonical node ID from a name string."""
    return (
        name.lower()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
        .replace("'", "")
    )
