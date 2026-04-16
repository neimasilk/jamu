"""
JamuKG Builder
==============
Constructs and manages the JamuKG knowledge graph using NetworkX.
"""

import json
from pathlib import Path
from typing import Optional

import networkx as nx

from .schema import (
    NodeType, EdgeType, EvidenceLevel, SourceDB,
    PlantNode, CompoundNode, DiseaseNode, FormulationNode,
    BioactivityNode, KGEdge, make_node_id,
)


class JamuKG:
    """The Jamu Knowledge Graph."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self._node_registry = {}  # node_id -> node dataclass

    # --- Add Nodes ---

    def add_plant(self, plant: PlantNode) -> str:
        """Add a plant node. Merges if already exists."""
        if plant.node_id in self._node_registry:
            existing = self._node_registry[plant.node_id]
            # Merge local names
            existing.local_names.update(plant.local_names)
            # Merge sources
            for s in plant.sources:
                if s not in existing.sources:
                    existing.sources.append(s)
            self.graph.nodes[plant.node_id].update(self._node_to_dict(existing))
        else:
            self._node_registry[plant.node_id] = plant
            self.graph.add_node(plant.node_id, **self._node_to_dict(plant))
        return plant.node_id

    def add_compound(self, compound: CompoundNode) -> str:
        if compound.node_id in self._node_registry:
            existing = self._node_registry[compound.node_id]
            for s in compound.sources:
                if s not in existing.sources:
                    existing.sources.append(s)
            self.graph.nodes[compound.node_id].update(self._node_to_dict(existing))
        else:
            self._node_registry[compound.node_id] = compound
            self.graph.add_node(compound.node_id, **self._node_to_dict(compound))
        return compound.node_id

    def add_disease(self, disease: DiseaseNode) -> str:
        if disease.node_id in self._node_registry:
            existing = self._node_registry[disease.node_id]
            if disease.icd10_code and not existing.icd10_code:
                existing.icd10_code = disease.icd10_code
                existing.icd10_class = disease.icd10_class
            for s in disease.sources:
                if s not in existing.sources:
                    existing.sources.append(s)
            self.graph.nodes[disease.node_id].update(self._node_to_dict(existing))
        else:
            self._node_registry[disease.node_id] = disease
            self.graph.add_node(disease.node_id, **self._node_to_dict(disease))
        return disease.node_id

    def add_formulation(self, formulation: FormulationNode) -> str:
        if formulation.node_id not in self._node_registry:
            self._node_registry[formulation.node_id] = formulation
            self.graph.add_node(formulation.node_id, **self._node_to_dict(formulation))
        return formulation.node_id

    def add_bioactivity(self, bioactivity: BioactivityNode) -> str:
        if bioactivity.node_id in self._node_registry:
            existing = self._node_registry[bioactivity.node_id]
            for s in bioactivity.sources:
                if s not in existing.sources:
                    existing.sources.append(s)
            self.graph.nodes[bioactivity.node_id].update(self._node_to_dict(existing))
        else:
            self._node_registry[bioactivity.node_id] = bioactivity
            self.graph.add_node(bioactivity.node_id, **self._node_to_dict(bioactivity))
        return bioactivity.node_id

    # --- Add Edges ---

    def add_edge(self, edge: KGEdge):
        """Add an edge. If edge already exists, merge evidence."""
        key = (edge.source_id, edge.target_id, edge.edge_type.value)

        if self.graph.has_edge(edge.source_id, edge.target_id):
            existing = self.graph[edge.source_id][edge.target_id]
            if existing.get("edge_type") == edge.edge_type.value:
                # Merge evidence
                for pmid in edge.pubmed_ids:
                    if pmid not in existing.get("pubmed_ids", []):
                        existing.setdefault("pubmed_ids", []).append(pmid)
                # Update evidence level if stronger
                if self._evidence_rank(edge.evidence_level) > self._evidence_rank(
                    EvidenceLevel(existing.get("evidence_level", "none"))
                ):
                    existing["evidence_level"] = edge.evidence_level.value
                # Add source
                if edge.source_db and edge.source_db not in existing.get("source_dbs", []):
                    existing.setdefault("source_dbs", []).append(edge.source_db)
                return

        self.graph.add_edge(
            edge.source_id,
            edge.target_id,
            edge_type=edge.edge_type.value,
            evidence_level=edge.evidence_level.value,
            confidence=edge.confidence,
            source_dbs=[edge.source_db] if edge.source_db else [],
            pubmed_ids=edge.pubmed_ids,
            evidence_text=edge.evidence_text,
        )

    # --- Query ---

    def get_plants(self) -> list:
        return [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == NodeType.PLANT.value]

    def get_compounds(self) -> list:
        return [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == NodeType.COMPOUND.value]

    def get_diseases(self) -> list:
        return [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == NodeType.DISEASE.value]

    def get_formulations(self) -> list:
        return [n for n, d in self.graph.nodes(data=True) if d.get("node_type") == NodeType.FORMULATION.value]

    def get_plant_diseases(self, plant_id: str) -> list:
        """Get all diseases a plant is claimed to treat."""
        result = []
        for _, target, data in self.graph.out_edges(plant_id, data=True):
            if data.get("edge_type") == EdgeType.TREATS.value:
                result.append((target, data))
        return result

    def get_plant_compounds(self, plant_id: str) -> list:
        """Get all compounds a plant produces."""
        result = []
        for _, target, data in self.graph.out_edges(plant_id, data=True):
            if data.get("edge_type") == EdgeType.PRODUCES.value:
                result.append((target, data))
        return result

    # --- Statistics ---

    def stats(self) -> dict:
        """Return basic KG statistics."""
        nodes_by_type = {}
        for _, data in self.graph.nodes(data=True):
            nt = data.get("node_type", "unknown")
            nodes_by_type[nt] = nodes_by_type.get(nt, 0) + 1

        edges_by_type = {}
        for _, _, data in self.graph.edges(data=True):
            et = data.get("edge_type", "unknown")
            edges_by_type[et] = edges_by_type.get(et, 0) + 1

        evidence_dist = {}
        for _, _, data in self.graph.edges(data=True):
            el = data.get("evidence_level", "none")
            evidence_dist[el] = evidence_dist.get(el, 0) + 1

        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "nodes_by_type": nodes_by_type,
            "edges_by_type": edges_by_type,
            "evidence_distribution": evidence_dist,
            "connected_components": nx.number_weakly_connected_components(self.graph),
        }

    # --- I/O ---

    def save(self, path: str):
        """Save KG to JSON (node-link format)."""
        data = nx.node_link_data(self.graph)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, path: str):
        """Load KG from JSON."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.graph = nx.node_link_graph(data)

    # --- Internal ---

    @staticmethod
    def _node_to_dict(node) -> dict:
        """Convert a node dataclass to a dict for NetworkX storage."""
        d = {}
        for k, v in node.__dict__.items():
            if k == "node_id":
                continue
            if isinstance(v, list):
                d[k] = [x.value if hasattr(x, "value") else x for x in v]
            elif hasattr(v, "value"):
                d[k] = v.value
            else:
                d[k] = v
        d["node_type"] = node.node_type.value
        return d

    @staticmethod
    def _evidence_rank(level: EvidenceLevel) -> int:
        return {
            EvidenceLevel.NONE: 0,
            EvidenceLevel.LIMITED: 1,
            EvidenceLevel.MODERATE: 2,
            EvidenceLevel.WELL_STUDIED: 3,
            EvidenceLevel.CONTRADICTED: -1,
        }.get(level, 0)
