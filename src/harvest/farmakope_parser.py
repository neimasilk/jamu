"""
Farmakope Herbal Indonesia PDF Parser
======================================
Extracts structured monograph data from Farmakope Herbal Indonesia PDFs.
Each monograph contains: plant name (Indonesian + Latin), plant part,
chemical identity compounds, and quality parameters.
"""

import json
import os
import re
import sys
from pathlib import Path

import pdfplumber
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def extract_all_text(pdf_path: str) -> list[dict]:
    """Extract text from all pages of the PDF."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({"page_num": i + 1, "text": text})
    return pages


def find_monograph_pages(pages: list[dict]) -> list[dict]:
    """
    Identify monograph boundaries.
    Monographs start with an ALL CAPS Indonesian plant name header
    (e.g., "DAUN ALAMANDA") which may appear mid-page.
    """
    part_prefixes = [
        "DAUN", "AKAR", "RIMPANG", "BUAH", "BIJI", "BUNGA",
        "KULIT BUAH", "HERBA", "UMBI LAPIS", "PULPA", "KAYU",
    ]

    # Build a list of (page_num, line_index, header_text) for all monograph starts
    mono_starts = []
    for page_data in pages:
        text = page_data["text"]
        page_num = page_data["page_num"]
        if page_num < 30:
            continue

        lines = text.strip().split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not re.match(r"^[A-Z\s-]+$", stripped) or len(stripped) < 6:
                continue
            for prefix in part_prefixes:
                if stripped.startswith(prefix + " ") or stripped.endswith(" " + prefix):
                    # Verify: next line should be a Latin pharmacopoeia name
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if re.match(r"^[A-Z][a-z]", next_line):
                            mono_starts.append((page_num, i, stripped))
                    break

    # Now extract text for each monograph
    # Strategy: for each monograph start, collect text from that point
    # until the next monograph start
    monographs = []
    all_page_texts = {p["page_num"]: p["text"] for p in pages}
    max_page = max(all_page_texts.keys())

    for idx, (start_page, start_line, header) in enumerate(mono_starts):
        # Determine end boundary
        if idx + 1 < len(mono_starts):
            end_page = mono_starts[idx + 1][0]
            end_line = mono_starts[idx + 1][1]
        else:
            end_page = min(start_page + 8, max_page)
            end_line = 9999

        # Collect text
        text_parts = []
        mono_pages = []
        for pg in range(start_page, end_page + 1):
            if pg not in all_page_texts:
                continue
            page_text = all_page_texts[pg]
            page_lines = page_text.strip().split("\n")

            if pg == start_page:
                # Start from the header line
                text_parts.append("\n".join(page_lines[start_line:]))
            elif pg == end_page and pg == mono_starts[idx + 1][0] if idx + 1 < len(mono_starts) else False:
                # End before the next monograph header
                text_parts.append("\n".join(page_lines[:end_line]))
            else:
                text_parts.append(page_text)
            mono_pages.append(pg)

        monographs.append({
            "start_page": start_page,
            "pages": mono_pages,
            "header": header,
            "text": "\n\n".join(text_parts),
        })

    return monographs


def parse_monograph_text(text: str) -> dict:
    """
    Parse a monograph text block into structured data.
    Extracts: Indonesian name, Latin name, scientific name, family, plant part,
    chemical identity, and other details.
    """
    result = {
        "indonesian_name": "",
        "latin_pharmacopoeia_name": "",
        "scientific_name": "",
        "family": "",
        "plant_part": "",
        "chemical_identity": "",
        "min_content": "",
        "description": "",
        "raw_text": text[:3000],  # Keep first 3000 chars for reference
    }

    lines = text.strip().split("\n")

    # Extract Indonesian name (usually in ALL CAPS near the top)
    for line in lines[:5]:
        stripped = line.strip()
        # Skip page numbers
        if stripped.startswith("-") and stripped.endswith("-"):
            continue
        if re.match(r"^[A-Z\s]+$", stripped) and len(stripped) > 3:
            result["indonesian_name"] = stripped.title()
            break

    # Extract Latin pharmacopoeia name (e.g., "Allamandae Catharticae Folium")
    latin_parts = [
        "Folium", "Folia", "Radix", "Rhizoma", "Cortex", "Fructus",
        "Semen", "Herba", "Flos", "Flores", "Bulbus", "Lignum",
        "Pulpa", "Caulis",
    ]
    for line in lines[:10]:
        stripped = line.strip()
        for part in latin_parts:
            if part in stripped and re.match(r"^[A-Z][a-z]", stripped):
                result["latin_pharmacopoeia_name"] = stripped
                # Extract plant part from Latin name
                result["plant_part"] = part
                break

    # Extract scientific name and family
    # Pattern: "... adalah [part] [Scientific name Author], suku [Family], ..."
    sci_pattern = re.compile(
        r"adalah\s+\w+\s+([A-Z][a-z]+\s+[a-z]+(?:\s+(?:\([^)]+\)\s*)?[A-Z][a-z.]*)?)\s*[.,]?\s*suku\s+([A-Za-z]+)",
    )
    sci_match = sci_pattern.search(text[:1000])
    if sci_match:
        result["scientific_name"] = sci_match.group(1).strip().rstrip(",.")
        result["family"] = sci_match.group(2).strip()
    else:
        # Alternative pattern without "suku"
        sci_pattern2 = re.compile(
            r"adalah\s+\w+\s+([A-Z][a-z]+\s+[a-z]+(?:\s+\([^)]+\))?\s+[A-Z][a-z.]*)"
        )
        sci_match2 = sci_pattern2.search(text[:1000])
        if sci_match2:
            result["scientific_name"] = sci_match2.group(1).strip().rstrip(",.")

    # Extract chemical identity compound
    # Pattern: "Senyawa identitas [Compound Name]"
    chem_pattern = re.compile(r"Senyawa identitas\s+(.+?)(?:\n|Struktur)", re.DOTALL)
    chem_match = chem_pattern.search(text)
    if chem_match:
        result["chemical_identity"] = chem_match.group(1).strip()

    # Extract minimum content requirement
    # Pattern: "mengandung [compound] tidak kurang dari X%"
    content_pattern = re.compile(
        r"mengandung\s+(.+?)\s+tidak kurang dari\s+([\d,]+%?)"
    )
    content_match = content_pattern.search(text[:1000])
    if content_match:
        result["min_content"] = f"{content_match.group(1).strip()}: >= {content_match.group(2).strip()}"

    # Extract first paragraph as description
    desc_start = text.find("adalah ")
    if desc_start >= 0:
        desc_end = text.find("\n\n", desc_start)
        if desc_end < 0:
            desc_end = desc_start + 500
        desc = text[desc_start:desc_end].replace("\n", " ").strip()
        result["description"] = desc[:500]

    return result


def parse_farmakope_pdf(pdf_path: str) -> list[dict]:
    """Main function: parse a Farmakope PDF into structured monographs."""
    print(f"Extracting text from {pdf_path}...")
    pages = extract_all_text(pdf_path)
    print(f"  {len(pages)} pages extracted")

    print("Finding monograph boundaries...")
    monographs = find_monograph_pages(pages)
    print(f"  {len(monographs)} monographs found")

    print("Parsing monographs...")
    results = []
    for mono in tqdm(monographs, desc="Parsing"):
        parsed = parse_monograph_text(mono["text"])
        parsed["pages"] = mono["pages"]
        parsed["start_page"] = mono["start_page"]
        results.append(parsed)

    return results


def main():
    """Parse all Farmakope PDFs in the data directory."""
    pdf_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "farmakope_pdf")
    pdf_dir = os.path.abspath(pdf_dir)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "entities")
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    all_monographs = []

    for fname in sorted(os.listdir(pdf_dir)):
        if not fname.endswith(".pdf"):
            continue
        pdf_path = os.path.join(pdf_dir, fname)
        print(f"\n=== Processing: {fname} ===")
        monographs = parse_farmakope_pdf(pdf_path)
        all_monographs.extend(monographs)

        # Print summary
        for m in monographs:
            sci = m.get("scientific_name", "?")
            indo = m.get("indonesian_name", "?")
            chem = m.get("chemical_identity", "?")
            print(f"  {indo:30s} | {sci:35s} | Chem: {chem[:40]}")

    # Save
    output_path = os.path.join(output_dir, "farmakope_monographs.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_monographs, f, ensure_ascii=False, indent=2)

    print(f"\n=== Total: {len(all_monographs)} monographs saved to {output_path} ===")
    return all_monographs


if __name__ == "__main__":
    main()
