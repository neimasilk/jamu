"""
Run this in a SEPARATE terminal to continue the KNApSAcK harvest:
    python run_knapsack_harvest.py

It will automatically resume from the last checkpoint.
After completion, rebuild the KG with:
    python run_rebuild_kg.py
"""
from src.harvest.knapsack_harvester import harvest_all_formulas, harvest_herb_effects
import os

output_dir = os.path.join("data", "raw", "knapsack")
formulas = harvest_all_formulas(start=1, end=5400, output_dir=output_dir, checkpoint_every=50)

formulas_path = os.path.join(output_dir, "knapsack_jamu_formulas.json")
if os.path.exists(formulas_path):
    harvest_herb_effects(formulas_path, output_dir)

print("\nDone! Now run: python run_rebuild_kg.py")
