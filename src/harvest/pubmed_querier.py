"""
PubMed Cross-Reference for JamuKG
===================================
For each plant-disease TREATS edge in the KG, queries PubMed
to determine evidence level. This produces the Validation Gap Map —
the core finding of the paper.
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import requests as req
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.builder import JamuKG
from src.kg.schema import NodeType, EdgeType, EvidenceLevel

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def get_plant_disease_pairs(kg: JamuKG) -> list[dict]:
    """Extract all unique plant-disease TREATS pairs from the KG."""
    pairs = []
    seen = set()

    for u, v, data in kg.graph.edges(data=True):
        if data.get("edge_type") != EdgeType.TREATS.value:
            continue

        u_data = kg.graph.nodes[u]
        v_data = kg.graph.nodes[v]

        # Only plant -> disease edges
        if u_data.get("node_type") != NodeType.PLANT.value:
            continue
        if v_data.get("node_type") != NodeType.DISEASE.value:
            continue

        plant_name = u_data.get("latin_name", "")
        disease_name = v_data.get("name", "")

        if not plant_name or not disease_name:
            continue

        key = (plant_name, disease_name)
        if key in seen:
            continue
        seen.add(key)

        pairs.append({
            "plant_id": u,
            "disease_id": v,
            "plant_name": plant_name,
            "disease_name": disease_name,
            "source_dbs": data.get("source_dbs", []),
        })

    return pairs


def query_pubmed_count(plant_latin: str, disease_term: str) -> dict:
    """
    Query PubMed for papers about a plant-disease association.
    Uses NCBI eutils REST API directly (more reliable than BioPython).
    """
    query = f'"{plant_latin}" AND "{disease_term}"'

    try:
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 5,
        }
        r = req.get(EUTILS_BASE, params=params, timeout=15)
        data = r.json()
        result = data.get("esearchresult", {})

        count = int(result.get("count", 0))
        pmids = result.get("idlist", [])

        return {
            "query": query,
            "count": count,
            "pmids": pmids[:5],
        }
    except Exception as e:
        return {
            "query": query,
            "count": -1,
            "error": str(e),
            "pmids": [],
        }


def classify_evidence(count: int) -> str:
    """Classify evidence level based on PubMed hit count."""
    if count <= 0:
        return EvidenceLevel.NONE.value
    elif count <= 5:
        return EvidenceLevel.LIMITED.value
    elif count <= 20:
        return EvidenceLevel.MODERATE.value
    else:
        return EvidenceLevel.WELL_STUDIED.value


def run_validation_gap_analysis(
    kg_path: str,
    output_dir: str,
    max_queries: int = 0,
    delay: float = 0.35,
):
    """
    Run the full validation gap analysis.
    Queries PubMed for each plant-disease pair in the KG.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load KG
    print("Loading JamuKG...")
    kg = JamuKG()
    kg.load(kg_path)

    # Get plant-disease pairs
    pairs = get_plant_disease_pairs(kg)
    print(f"Found {len(pairs)} unique plant-disease pairs")

    if max_queries > 0:
        pairs = pairs[:max_queries]
        print(f"Limiting to {max_queries} queries")

    # Load checkpoint
    checkpoint_path = os.path.join(output_dir, "pubmed_checkpoint.json")
    results = {}
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            results = {r["key"]: r for r in json.load(f)}
        print(f"Loaded {len(results)} cached results")

    # Query PubMed
    new_queries = 0
    for pair in tqdm(pairs, desc="Querying PubMed"):
        key = f"{pair['plant_name']}||{pair['disease_name']}"

        if key in results:
            continue

        pubmed = query_pubmed_count(pair["plant_name"], pair["disease_name"])

        result = {
            "key": key,
            "plant_id": pair["plant_id"],
            "disease_id": pair["disease_id"],
            "plant_name": pair["plant_name"],
            "disease_name": pair["disease_name"],
            "pubmed_count": pubmed["count"],
            "pubmed_pmids": pubmed["pmids"],
            "evidence_level": classify_evidence(pubmed["count"]),
            "source_dbs": pair["source_dbs"],
        }
        results[key] = result
        new_queries += 1

        # Checkpoint every 100 queries
        if new_queries % 100 == 0:
            save_results(results, checkpoint_path)

        # Rate limit: NCBI allows 3/sec without key, 10/sec with key
        time.sleep(delay)

    # Final save
    save_results(results, checkpoint_path)

    # Save clean output
    output_path = os.path.join(output_dir, "validation_gap_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(list(results.values()), f, ensure_ascii=False, indent=2)

    # Generate summary
    summary = generate_summary(list(results.values()))
    summary_path = os.path.join(output_dir, "validation_gap_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print_summary(summary)

    return list(results.values())


def save_results(results: dict, path: str):
    """Save checkpoint."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(list(results.values()), f, ensure_ascii=False, indent=2)


def generate_summary(results: list[dict]) -> dict:
    """Generate validation gap summary statistics."""
    total = len(results)
    evidence_dist = Counter(r["evidence_level"] for r in results)

    # Top plants with most studied associations
    plant_studied = defaultdict(int)
    plant_unstudied = defaultdict(int)
    for r in results:
        if r["evidence_level"] != EvidenceLevel.NONE.value:
            plant_studied[r["plant_name"]] += 1
        else:
            plant_unstudied[r["plant_name"]] += 1

    # Top diseases by evidence gap
    disease_gap = defaultdict(lambda: {"studied": 0, "unstudied": 0})
    for r in results:
        d = r["disease_name"]
        if r["evidence_level"] != EvidenceLevel.NONE.value:
            disease_gap[d]["studied"] += 1
        else:
            disease_gap[d]["unstudied"] += 1

    # Most promising gaps: high traditional consensus (many plants) + zero papers
    promising_gaps = []
    for r in results:
        if r["evidence_level"] == EvidenceLevel.NONE.value:
            promising_gaps.append(r)

    # Top well-studied pairs (for validation)
    well_studied = [r for r in results if r["evidence_level"] == EvidenceLevel.WELL_STUDIED.value]
    well_studied.sort(key=lambda x: x["pubmed_count"], reverse=True)

    return {
        "total_pairs": total,
        "evidence_distribution": dict(evidence_dist),
        "pct_no_evidence": round(evidence_dist.get(EvidenceLevel.NONE.value, 0) / max(total, 1) * 100, 1),
        "pct_well_studied": round(evidence_dist.get(EvidenceLevel.WELL_STUDIED.value, 0) / max(total, 1) * 100, 1),
        "top_studied_plants": dict(Counter(plant_studied).most_common(20)),
        "top_unstudied_plants": dict(Counter(plant_unstudied).most_common(20)),
        "top_well_studied_pairs": [
            {"plant": r["plant_name"], "disease": r["disease_name"], "pubmed_count": r["pubmed_count"]}
            for r in well_studied[:20]
        ],
        "disease_gap_summary": {
            d: v for d, v in sorted(disease_gap.items(), key=lambda x: -x[1]["unstudied"])[:30]
        },
    }


def print_summary(summary: dict):
    """Print human-readable summary."""
    print("\n" + "=" * 70)
    print("VALIDATION GAP ANALYSIS — SUMMARY")
    print("=" * 70)
    print(f"Total plant-disease pairs analyzed: {summary['total_pairs']:,}")
    print(f"\nEvidence distribution:")
    for level, count in sorted(summary["evidence_distribution"].items()):
        pct = count / max(summary["total_pairs"], 1) * 100
        bar = "#" * int(pct / 2)
        print(f"  {level:15s}: {count:>5,} ({pct:5.1f}%) {bar}")

    print(f"\n>>> {summary['pct_no_evidence']}% of traditional claims have ZERO PubMed evidence <<<")
    print(f">>> {summary['pct_well_studied']}% are well-studied (20+ papers) <<<")

    print(f"\nTop well-studied plant-disease pairs:")
    for pair in summary.get("top_well_studied_pairs", [])[:10]:
        print(f"  {pair['plant']:35s} -> {pair['disease']:20s} ({pair['pubmed_count']} papers)")

    print(f"\nTop plants with most UNSTUDIED claims:")
    for plant, count in list(summary.get("top_unstudied_plants", {}).items())[:10]:
        print(f"  {plant:45s}: {count} unstudied claims")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="PubMed Validation Gap Analysis")
    parser.add_argument("--kg", default="data/kg/jamukg_v01.json", help="Path to KG JSON")
    parser.add_argument("--max", type=int, default=0, help="Max queries (0=all)")
    parser.add_argument("--delay", type=float, default=0.35, help="Delay between queries")
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent.parent
    kg_path = base_dir / args.kg
    output_dir = base_dir / "data" / "raw" / "pubmed"

    run_validation_gap_analysis(
        str(kg_path),
        str(output_dir),
        max_queries=args.max,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
