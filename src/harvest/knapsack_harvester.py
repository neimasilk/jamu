"""
KNApSAcK Jamu Database Harvester
=================================
Harvests jamu formula data from the KNApSAcK Jamu web interface.
Each formula (J-code) contains: company, jamu name, effect, effect group, and ingredient herbs.
"""

import json
import os
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

BASE_URL = "https://www.knapsackfamily.com/jamu/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}
DELAY = 0.5  # seconds between requests — be polite


def fetch_formula(jamu_id: str, session: requests.Session) -> dict | None:
    """
    Fetch a single jamu formula by its J-code.
    Returns parsed formula dict or None if not found.
    """
    url = f"{BASE_URL}haigou.php?hword={jamu_id}"
    try:
        r = session.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            return None
    except requests.RequestException:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", class_="res")
    if not table:
        return None

    rows = table.find_all("tr")
    if len(rows) < 3:
        return None

    formula = {
        "jamu_id": jamu_id,
        "company": "",
        "jamu_name": "",
        "jamu_effect": "",
        "jamu_effect_group": "",
        "herbs": [],
    }

    for row in rows:
        th = row.find("th")
        tds = row.find_all("td")

        if th:
            label = th.get_text(strip=True)

            if label == "Company or Reference" and tds:
                formula["company"] = tds[0].get_text(strip=True)

            elif label == "Jamu Name" and tds:
                formula["jamu_name"] = tds[0].get_text(strip=True)

            elif label == "Jamu Effect" and tds:
                formula["jamu_effect"] = tds[0].get_text(strip=True)

            elif label == "Jamu Effect Group" and tds:
                formula["jamu_effect_group"] = tds[0].get_text(strip=True)

        # Herb ingredient rows: no <th>, multiple <td>
        elif len(tds) >= 5 and not th:
            herb = {
                "herb_name": tds[0].get_text(strip=True),
                "local_name_id": tds[1].get_text(strip=True),
                "local_name_en": tds[2].get_text(strip=True),
                "scientific_name": tds[3].get_text(strip=True),
                "plant_part": tds[4].get_text(strip=True) if len(tds) > 4 else "",
                "percent": tds[6].get_text(strip=True) if len(tds) > 6 else "",
            }
            # Get SID for effect page
            for a in row.find_all("a", href=True):
                href = a["href"]
                if "effect.php" in href and "sid=" in href:
                    herb["effect_sid"] = href.split("sid=")[-1]
            if herb["herb_name"]:  # Skip empty rows
                formula["herbs"].append(herb)

    # Only return if we got meaningful data
    if formula["jamu_name"] or formula["herbs"]:
        return formula
    return None


def fetch_herb_effects(sid: str, session: requests.Session) -> dict | None:
    """Fetch detailed herb effects from effect page."""
    url = f"{BASE_URL}effect.php?sid={sid}"
    try:
        r = session.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            return None
    except requests.RequestException:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    result = {"sid": sid}

    # Try two-column layout first (original format: th/label + td/value)
    for row in soup.find_all("tr"):
        tds = row.find_all("td")
        if len(tds) >= 2:
            label = tds[0].get_text(strip=True)
            value = tds[1].get_text(strip=True)
            if label == "Herb Name":
                result["herb_name"] = value
            elif label == "Herb Name(Indonesia)":
                result["local_name_id"] = value
            elif label == "Herb Name(English/Chinese)":
                result["local_name_en"] = value
            elif label == "Scientific Name":
                result["scientific_name"] = value
            elif label == "Position of Plants":
                result["plant_part"] = value
            elif label == "Effect":
                result["effect"] = value
            elif label == "Comment":
                result["comment"] = value
            elif label == "Reference":
                result["reference"] = value

    # Fallback: single-column positional layout (current format)
    if "herb_name" not in result:
        values = []
        for row in soup.find_all("tr"):
            tds = row.find_all("td")
            if len(tds) == 1:
                values.append(tds[0].get_text(strip=True))

        # Positional mapping: herb_name, local_id, local_en, scientific, part, effect, comment, reference
        field_map = [
            "herb_name", "local_name_id", "local_name_en",
            "scientific_name", "plant_part", "effect", "comment", "reference",
        ]
        for i, field in enumerate(field_map):
            if i < len(values) and values[i] and values[i] != "-":
                result[field] = values[i]

    return result if "herb_name" in result else None


def harvest_all_formulas(
    start: int = 1,
    end: int = 5400,
    output_dir: str = "data/raw/knapsack",
    checkpoint_every: int = 100,
):
    """
    Harvest all jamu formulas by enumerating J-codes.
    Saves progress incrementally.
    """
    os.makedirs(output_dir, exist_ok=True)
    checkpoint_path = os.path.join(output_dir, "formulas_checkpoint.json")

    # Load existing checkpoint
    formulas = {}
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            formulas = {item["jamu_id"]: item for item in json.load(f)}
        print(f"Loaded {len(formulas)} formulas from checkpoint")

    session = requests.Session()
    new_count = 0
    empty_streak = 0

    pbar = tqdm(range(start, end + 1), desc="Harvesting KNApSAcK")
    for i in pbar:
        jamu_id = f"J{i:05d}"

        # Skip if already harvested
        if jamu_id in formulas:
            continue

        formula = fetch_formula(jamu_id, session)

        if formula:
            formulas[jamu_id] = formula
            new_count += 1
            empty_streak = 0
            pbar.set_postfix(found=len(formulas), new=new_count, last=jamu_id)
        else:
            empty_streak += 1

        # Save checkpoint periodically
        if new_count > 0 and new_count % checkpoint_every == 0:
            save_checkpoint(formulas, checkpoint_path)
            pbar.set_postfix(found=len(formulas), saved="yes")

        time.sleep(DELAY)

    # Final save
    save_checkpoint(formulas, checkpoint_path)

    # Also save as clean output
    clean_path = os.path.join(output_dir, "knapsack_jamu_formulas.json")
    with open(clean_path, "w", encoding="utf-8") as f:
        json.dump(list(formulas.values()), f, ensure_ascii=False, indent=2)

    print(f"\nHarvest complete: {len(formulas)} formulas saved to {clean_path}")
    return list(formulas.values())


def save_checkpoint(formulas: dict, path: str):
    """Save current harvest progress."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(list(formulas.values()), f, ensure_ascii=False, indent=2)


def harvest_herb_effects(
    formulas_path: str,
    output_dir: str = "data/raw/knapsack",
):
    """
    From harvested formulas, extract unique herb SIDs and fetch their effects.
    """
    with open(formulas_path, "r", encoding="utf-8") as f:
        formulas = json.load(f)

    # Collect unique SIDs
    sids = set()
    for formula in formulas:
        for herb in formula.get("herbs", []):
            sid = herb.get("effect_sid", "")
            if sid:
                sids.add(sid)

    print(f"Found {len(sids)} unique herb SIDs to fetch")

    # Check for existing data
    effects_path = os.path.join(output_dir, "knapsack_herb_effects.json")
    existing = {}
    if os.path.exists(effects_path):
        with open(effects_path, "r", encoding="utf-8") as f:
            existing = {item["sid"]: item for item in json.load(f)}

    sids_to_fetch = sids - set(existing.keys())
    print(f"Already have {len(existing)}, need to fetch {len(sids_to_fetch)}")

    session = requests.Session()
    for sid in tqdm(sorted(sids_to_fetch), desc="Fetching herb effects"):
        result = fetch_herb_effects(sid, session)
        if result:
            existing[sid] = result
        time.sleep(DELAY)

    # Save
    with open(effects_path, "w", encoding="utf-8") as f:
        json.dump(list(existing.values()), f, ensure_ascii=False, indent=2)

    print(f"Saved {len(existing)} herb effects to {effects_path}")
    return list(existing.values())


def main():
    """Main entry point — runs full harvest."""
    import argparse

    parser = argparse.ArgumentParser(description="Harvest KNApSAcK Jamu Database")
    parser.add_argument("--start", type=int, default=1, help="Start J-code number")
    parser.add_argument("--end", type=int, default=5400, help="End J-code number")
    parser.add_argument("--quick", action="store_true", help="Quick test: harvest first 50 only")
    parser.add_argument("--effects", action="store_true", help="Also harvest herb effects")
    args = parser.parse_args()

    if args.quick:
        args.end = min(args.end, 50)

    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "knapsack")
    output_dir = os.path.abspath(output_dir)

    formulas = harvest_all_formulas(
        start=args.start,
        end=args.end,
        output_dir=output_dir,
    )

    if args.effects and formulas:
        formulas_path = os.path.join(output_dir, "knapsack_jamu_formulas.json")
        harvest_herb_effects(formulas_path, output_dir)


if __name__ == "__main__":
    main()
