"""
JamuKG Full Pipeline
====================
Run after KNApSAcK harvest and PubMed validation gap complete.
Steps:
  1. Sync KNApSAcK checkpoint -> clean file
  2. Rebuild integrated KG (auto-versioned)
  3. Annotate KG with PubMed evidence
  4. Apply disease ontology (split TREATS into TREATS / HAS_USE /
     ETHNOBOTANICAL_USE / APPLIED_TO)
  5. Generate all visualizations
  6. Print final statistics
"""

import json
import os
import sys
import io
import shutil
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE_DIR = Path(__file__).parent


def get_next_version() -> str:
    """Auto-detect next KG version number."""
    kg_dir = BASE_DIR / "data" / "kg"
    existing = sorted(kg_dir.glob("jamukg_v*.json"))
    versions = []
    for f in existing:
        name = f.stem
        if "_stats" in name or "_annotated" in name or "_normalized" in name or "_final" in name:
            continue
        # Extract version number: jamukg_v06 -> 6
        parts = name.replace("jamukg_v", "")
        try:
            versions.append(int(parts))
        except ValueError:
            pass
    next_v = max(versions) + 1 if versions else 1
    return f"v{next_v:02d}"


def step1_sync_knapsack():
    """Sync KNApSAcK checkpoint to clean file."""
    print("\n" + "=" * 60)
    print("STEP 1: Syncing KNApSAcK checkpoint")
    print("=" * 60)

    ckpt_path = BASE_DIR / "data" / "raw" / "knapsack" / "formulas_checkpoint.json"
    clean_path = BASE_DIR / "data" / "raw" / "knapsack" / "knapsack_jamu_formulas.json"

    if not ckpt_path.exists():
        print("  No checkpoint found, skipping")
        return

    with open(ckpt_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(clean_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  Synced {len(data)} formulas from checkpoint")


def step2_rebuild_kg():
    """Rebuild integrated KG."""
    version = get_next_version()
    print("\n" + "=" * 60)
    print(f"STEP 2: Rebuilding integrated KG ({version})")
    print("=" * 60)

    from src.kg.integrator import build_integrated_kg
    kg = build_integrated_kg()

    stats = kg.stats()
    print(f"\n  Total nodes: {stats['total_nodes']:,}")
    print(f"  Total edges: {stats['total_edges']:,}")

    output_path = BASE_DIR / "data" / "kg" / f"jamukg_{version}.json"
    kg.save(str(output_path))
    print(f"  Saved to {output_path}")

    stats_path = BASE_DIR / "data" / "kg" / f"jamukg_{version}_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    # Also update latest stats
    latest_stats_path = BASE_DIR / "data" / "kg" / "jamukg_latest_stats.json"
    with open(latest_stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    return kg, version


def step3_annotate_evidence(kg, version="v02"):
    """Annotate KG with PubMed evidence."""
    print("\n" + "=" * 60)
    print("STEP 3: Annotating KG with PubMed evidence")
    print("=" * 60)

    pubmed_path = BASE_DIR / "data" / "raw" / "pubmed" / "validation_gap_results.json"
    if not pubmed_path.exists():
        print("  PubMed results not found, skipping")
        return kg

    from src.analysis.annotate_evidence import annotate_kg_with_evidence
    annotate_kg_with_evidence(kg, str(pubmed_path))

    output_path = BASE_DIR / "data" / "kg" / f"jamukg_{version}_annotated.json"
    kg.save(str(output_path))
    print(f"  Saved annotated KG to {output_path}")

    stats = kg.stats()
    stats_path = BASE_DIR / "data" / "kg" / f"jamukg_{version}_annotated_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    # Also update latest stats
    latest_stats_path = BASE_DIR / "data" / "kg" / "jamukg_latest_stats.json"
    with open(latest_stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    return kg


def step4_apply_ontology(version: str):
    """Apply disease ontology: split TREATS into refined edge types.

    Reads `jamukg_{version}_annotated.json`, rewrites it in place with
    ontology-aware edge types, and writes a split-report sibling.

    The annotated KG produced by step 3 contains `treats` edges that mix
    clinical disease, symptom, pharmacological action, ethnobotanical use,
    and body-part targets. This step splits them according to
    `data/kg/disease_ontology.json` (with 6 hand-resolved ambiguous terms
    documented in `src/analysis/apply_disease_ontology.py`).
    """
    print("\n" + "=" * 60)
    print("STEP 4: Applying disease ontology (split TREATS)")
    print("=" * 60)

    annotated_path = BASE_DIR / "data" / "kg" / f"jamukg_{version}_annotated.json"
    ontology_path = BASE_DIR / "data" / "kg" / "disease_ontology.json"

    if not annotated_path.exists():
        print(f"  Annotated KG not found at {annotated_path}, skipping")
        return
    if not ontology_path.exists():
        print(f"  Ontology not found at {ontology_path}, skipping")
        return

    from src.analysis.apply_disease_ontology import (
        build_node_to_category,
        apply_split,
        compute_validation_gap,
        AMBIGUOUS_RESOLUTION,
    )

    with open(annotated_path, "r", encoding="utf-8") as f:
        kg_dict = json.load(f)
    with open(ontology_path, "r", encoding="utf-8") as f:
        ontology = json.load(f)

    node2cat = build_node_to_category(kg_dict, ontology)
    new_kg, stats = apply_split(kg_dict, node2cat)

    print(f"  Disease nodes mapped: {len(node2cat)}")
    print(f"  Edge split (from {stats['treats_before']} treats edges):")
    print(f"    treats             : {stats['treats_after']}")
    print(f"    has_use            : {stats['has_use']}")
    print(f"    ethnobotanical_use : {stats['ethnobotanical_use']}")
    print(f"    applied_to         : {stats['applied_to']}")
    if stats["unmapped"]:
        print(f"    unmapped           : {stats['unmapped']}  (warning)")

    # Overwrite annotated file in place; from this run forward,
    # `_annotated.json` includes ontology split.
    with open(annotated_path, "w", encoding="utf-8") as f:
        json.dump(new_kg, f, ensure_ascii=False)
    print(f"  Updated {annotated_path.name} with ontology split")

    # Validation gap per refined edge type (Dr. Duke subset)
    gap_report = {}
    for et in ["treats", "has_use", "ethnobotanical_use", "applied_to"]:
        g = compute_validation_gap(new_kg, et, restrict_source_db="dr_duke")
        gap_report[et] = g
    knaps_gap = compute_validation_gap(new_kg, "treats", restrict_source_db="knapsack_jamu")

    report = {
        "version": version,
        "method": "apply disease_ontology.json to TREATS edges; 6 ambiguous resolved",
        "ambiguous_resolution": AMBIGUOUS_RESOLUTION,
        "edge_split_stats": {
            "treats_before": stats["treats_before"],
            "treats_after": stats["treats_after"],
            "has_use": stats["has_use"],
            "ethnobotanical_use": stats["ethnobotanical_use"],
            "applied_to": stats["applied_to"],
            "unmapped": stats["unmapped"],
        },
        "validation_gap_dr_duke": gap_report,
        "validation_gap_knapsack_formulations": knaps_gap,
    }
    report_path = BASE_DIR / "data" / "kg" / f"{version}_ontology_split_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Wrote split report: {report_path.name}")


def step5_visualize():
    """Generate all visualizations.

    Calls three figure-producing modules in sequence:
      - visualize.py            -> figures 01-08 + interactive subgraphs
      - network_pharmacology.py -> figures 09-11
      - formulation_analysis.py -> figures 12-17 + 00 (paper summary)
    Each is wrapped so a failure in one does not abort later groups,
    but errors are still surfaced to the console.
    """
    print("\n" + "=" * 60)
    print("STEP 5: Generating visualizations")
    print("=" * 60)

    for module_path, label in [
        ("src.analysis.visualize", "core figures (01-08)"),
        ("src.analysis.network_pharmacology", "network pharmacology (09-11)"),
        ("src.analysis.formulation_analysis", "formulation figures (12-17, 00)"),
    ]:
        print(f"\n--- {label} ---")
        try:
            mod = __import__(module_path, fromlist=["main"])
            mod.main()
        except Exception as e:
            print(f"  WARNING: {label} failed: {type(e).__name__}: {e}")


def step6_final_stats():
    """Print final statistics."""
    print("\n" + "=" * 60)
    print("STEP 6: Final Statistics")
    print("=" * 60)

    from src.analysis.statistics import analyze_kg

    # Find latest KG
    kg_dir = BASE_DIR / "data" / "kg"
    kg_files = sorted(f for f in kg_dir.glob("jamukg_v*_annotated.json"))
    if not kg_files:
        kg_files = sorted(f for f in kg_dir.glob("jamukg_v*.json") if "_stats" not in f.name)

    if kg_files:
        analyze_kg(str(kg_files[-1]))

    # Print validation gap summary
    summary_path = BASE_DIR / "data" / "raw" / "pubmed" / "validation_gap_summary.json"
    if summary_path.exists():
        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)
        print(f"\n{'=' * 60}")
        print("VALIDATION GAP SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total pairs: {summary.get('total_pairs', '?'):,}")
        print(f"No evidence: {summary.get('pct_no_evidence', '?')}%")
        print(f"Well studied: {summary.get('pct_well_studied', '?')}%")


if __name__ == "__main__":
    step1_sync_knapsack()
    kg, version = step2_rebuild_kg()
    kg = step3_annotate_evidence(kg, version)
    step4_apply_ontology(version)
    step5_visualize()
    step6_final_stats()
    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETE — JamuKG {version}")
    print("=" * 60)
