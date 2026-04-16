"""
HerbalDB Harvester
===================
Harvests plant and compound data from HerbalDB (herbaldb.farmasi.ui.ac.id/v3/).
HerbalDB is maintained by Faculty of Pharmacy, Universitas Indonesia.

Expected data: ~3,810 plant species, ~6,776 compounds with 3D structures.

Usage:
    python -m src.harvest.herbaldb_harvester
    python -m src.harvest.herbaldb_harvester --quick  # Test with first 50
"""

import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

BASE_URL = "http://herbaldb.farmasi.ui.ac.id/v3/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}
DELAY = 0.5  # seconds between requests
TIMEOUT = 30


def test_connection() -> bool:
    """Test if HerbalDB is accessible."""
    try:
        r = requests.get(BASE_URL, headers=HEADERS, timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False


def discover_endpoints(session: requests.Session) -> dict:
    """
    Discover available pages and API endpoints on HerbalDB.
    Returns dict of discovered URLs and their types.
    """
    endpoints = {}
    try:
        r = session.get(BASE_URL, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return endpoints

        soup = BeautifulSoup(r.text, "html.parser")

        # Find all links
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if href and not href.startswith(("#", "javascript:", "mailto:")):
                full_url = urljoin(BASE_URL, href)
                if "herbaldb" in full_url:
                    endpoints[full_url] = text

        # Check common API paths
        for path in ["api/", "api/plants", "api/compounds", "search", "browse",
                      "plant/list", "compound/list", "species/", "plants/"]:
            url = urljoin(BASE_URL, path)
            try:
                r = session.get(url, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    content_type = r.headers.get("Content-Type", "")
                    endpoints[url] = f"API ({content_type[:30]})"
            except requests.RequestException:
                pass
            time.sleep(0.3)

    except requests.RequestException as e:
        print(f"  Discovery failed: {e}")

    return endpoints


def harvest_plant_list(session: requests.Session) -> list[dict]:
    """
    Harvest the list of all plants from HerbalDB.
    Tries multiple strategies: API endpoints, paginated list, search.
    """
    plants = []

    # Strategy 1: Try paginated browse/list page
    for page in range(1, 200):  # Max 200 pages
        url = f"{BASE_URL}plant/list?page={page}"
        try:
            r = session.get(url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code != 200:
                # Try alternative URL patterns
                for alt in [f"{BASE_URL}plants?page={page}",
                            f"{BASE_URL}browse/plants?page={page}",
                            f"{BASE_URL}species?page={page}"]:
                    r = session.get(alt, headers=HEADERS, timeout=TIMEOUT)
                    if r.status_code == 200:
                        break
                else:
                    break

            soup = BeautifulSoup(r.text, "html.parser")
            # Look for plant entries in tables or lists
            entries = extract_plant_entries(soup)
            if not entries:
                break

            plants.extend(entries)
            time.sleep(DELAY)

        except requests.RequestException:
            break

    return plants


def extract_plant_entries(soup: BeautifulSoup) -> list[dict]:
    """Extract plant entries from a page."""
    entries = []

    # Try table format
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip header
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                entry = {"raw_cells": [c.get_text(strip=True) for c in cells]}
                # Look for links to detail pages
                for a in row.find_all("a", href=True):
                    entry["detail_url"] = urljoin(BASE_URL, a["href"])
                    entry["name"] = a.get_text(strip=True)
                if entry.get("name"):
                    entries.append(entry)

    # Try card/div format
    if not entries:
        for card in soup.find_all(["div", "li"], class_=lambda c: c and any(
                x in (c if isinstance(c, str) else " ".join(c))
                for x in ["plant", "species", "item", "card", "result"])):
            a = card.find("a", href=True)
            if a:
                entries.append({
                    "name": a.get_text(strip=True),
                    "detail_url": urljoin(BASE_URL, a["href"]),
                })

    return entries


def fetch_plant_detail(url: str, session: requests.Session) -> dict | None:
    """Fetch detailed plant data from a detail page."""
    try:
        r = session.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return None
    except requests.RequestException:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    plant = {"source_url": url}

    # Extract structured data from tables
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True).lower()
                value = cells[1].get_text(strip=True)

                if any(k in key for k in ["scientific", "latin", "species", "binomial"]):
                    plant["scientific_name"] = value
                elif any(k in key for k in ["family", "familia"]):
                    plant["family"] = value
                elif any(k in key for k in ["local", "common", "indonesia", "vernacular"]):
                    plant["local_name"] = value
                elif any(k in key for k in ["synonym"]):
                    plant["synonyms"] = value
                elif any(k in key for k in ["part", "bagian"]):
                    plant["plant_parts"] = value
                elif any(k in key for k in ["use", "khasiat", "indication", "effect"]):
                    plant["traditional_uses"] = value
                elif any(k in key for k in ["compound", "senyawa", "chemical"]):
                    plant["compounds"] = value

    # Extract compound links
    compounds = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if any(x in href for x in ["compound", "molecule", "chem"]):
            compounds.append({
                "name": text,
                "url": urljoin(BASE_URL, href),
            })
    if compounds:
        plant["compound_links"] = compounds

    # Look for headings with plant name
    for h in soup.find_all(["h1", "h2", "h3"]):
        text = h.get_text(strip=True)
        if text and not plant.get("scientific_name"):
            # Check if it looks like a Latin name (italicized or capitalized genus)
            em = h.find(["em", "i"])
            if em:
                plant["scientific_name"] = em.get_text(strip=True)

    return plant if plant.get("scientific_name") else None


def fetch_compound_detail(url: str, session: requests.Session) -> dict | None:
    """Fetch detailed compound data from a detail page."""
    try:
        r = session.get(url, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return None
    except requests.RequestException:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    compound = {"source_url": url}

    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True).lower()
                value = cells[1].get_text(strip=True)

                if any(k in key for k in ["name", "nama"]):
                    compound["name"] = value
                elif any(k in key for k in ["formula", "molecular"]):
                    compound["molecular_formula"] = value
                elif any(k in key for k in ["weight", "berat"]):
                    compound["molecular_weight"] = value
                elif any(k in key for k in ["cas"]):
                    compound["cas_number"] = value
                elif any(k in key for k in ["smiles"]):
                    compound["smiles"] = value
                elif any(k in key for k in ["inchi"]):
                    compound["inchi"] = value
                elif any(k in key for k in ["activity", "bioactiv", "aktiv"]):
                    compound["bioactivity"] = value

    return compound if compound.get("name") else None


def save_checkpoint(data: list, path: str):
    """Save harvest progress."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def harvest_all(output_dir: str = "data/raw/herbaldb", max_plants: int = 0):
    """
    Main harvest function. Discovers endpoints and harvests all data.

    Args:
        output_dir: Directory to save harvested data
        max_plants: Maximum plants to harvest (0 = all)
    """
    os.makedirs(output_dir, exist_ok=True)
    checkpoint_path = os.path.join(output_dir, "herbaldb_checkpoint.json")

    # Load existing checkpoint
    existing = []
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"Loaded {len(existing)} plants from checkpoint")

    # Test connection
    print(f"Testing connection to {BASE_URL}...")
    if not test_connection():
        print("ERROR: HerbalDB is not accessible. The server may be down.")
        print("Try again later. Existing checkpoint preserved.")
        return existing

    session = requests.Session()

    # Discover endpoints
    print("Discovering endpoints...")
    endpoints = discover_endpoints(session)
    print(f"Found {len(endpoints)} endpoints:")
    for url, desc in list(endpoints.items())[:20]:
        print(f"  {url}: {desc}")

    # Save endpoint map for debugging
    with open(os.path.join(output_dir, "endpoints.json"), "w", encoding="utf-8") as f:
        json.dump(endpoints, f, ensure_ascii=False, indent=2)

    # Harvest plant list
    print("\nHarvesting plant list...")
    plant_list = harvest_plant_list(session)
    print(f"Found {len(plant_list)} plants in listing")

    if not plant_list:
        print("No plants found via listing. Check endpoints.json for manual exploration.")
        return existing

    # Harvest plant details
    existing_urls = {p.get("source_url") for p in existing}
    plants_to_fetch = [p for p in plant_list if p.get("detail_url") not in existing_urls]

    if max_plants > 0:
        plants_to_fetch = plants_to_fetch[:max_plants]

    print(f"Fetching details for {len(plants_to_fetch)} new plants...")
    new_count = 0
    for p in tqdm(plants_to_fetch, desc="Fetching plant details"):
        detail = fetch_plant_detail(p["detail_url"], session)
        if detail:
            existing.append(detail)
            new_count += 1

            if new_count % 50 == 0:
                save_checkpoint(existing, checkpoint_path)

        time.sleep(DELAY)

    # Final save
    save_checkpoint(existing, checkpoint_path)

    # Save clean output
    clean_path = os.path.join(output_dir, "herbaldb_plants.json")
    with open(clean_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"\nHarvest complete: {len(existing)} plants saved to {clean_path}")
    return existing


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Harvest HerbalDB (UI)")
    parser.add_argument("--quick", action="store_true", help="Quick test: first 50 plants")
    parser.add_argument("--discover", action="store_true", help="Only discover endpoints")
    args = parser.parse_args()

    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "herbaldb")
    output_dir = os.path.abspath(output_dir)

    if args.discover:
        session = requests.Session()
        if not test_connection():
            print("HerbalDB is not accessible.")
            return
        endpoints = discover_endpoints(session)
        for url, desc in endpoints.items():
            print(f"  {url}: {desc}")
        return

    max_plants = 50 if args.quick else 0
    harvest_all(output_dir, max_plants=max_plants)


if __name__ == "__main__":
    main()
