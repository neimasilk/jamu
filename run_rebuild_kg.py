"""
Rebuild the integrated JamuKG after new data is harvested.
    python run_rebuild_kg.py
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from src.kg.integrator import main
main()
