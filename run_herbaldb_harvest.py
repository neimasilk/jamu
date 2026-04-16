"""
Run this to harvest HerbalDB data:
    python run_herbaldb_harvest.py

It will automatically resume from the last checkpoint.
After completion, rebuild the KG with:
    python run_full_pipeline.py
"""
from src.harvest.herbaldb_harvester import harvest_all
import os

output_dir = os.path.join("data", "raw", "herbaldb")
harvest_all(output_dir=output_dir)

print("\nDone! Now run: python run_full_pipeline.py")
