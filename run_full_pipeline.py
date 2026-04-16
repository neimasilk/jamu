"""
JamuKG Full Pipeline
====================
Run after KNApSAcK harvest and PubMed validation gap complete.
Steps:
  1. Sync KNApSAcK checkpoint -> clean file
  2. Rebuild integrated KG (auto-versioned)
  3. Annotate KG with PubMed evidence
  4. Generate all visualizations
  5. Print final statistics
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


def step4_visualize():
    """Generate all visualizations."""
    print("\n" + "=" * 60)
    print("STEP 4: Generating visualizations")
    print("=" * 60)

    from src.analysis.visualize import main as viz_main
    viz_main()


def step5_final_stats():
    """Print final statistics."""
    print("\n" + "=" * 60)
    print("STEP 5: Final Statistics")
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
    step4_visualize()
    step5_final_stats()
    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETE — JamuKG {version}")
    print("=" * 60)
