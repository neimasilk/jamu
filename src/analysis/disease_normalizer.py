"""
Disease Name Normalizer
========================
Normalizes heterogeneous disease/condition names in JamuKG
to standardized categories with ICD-10 chapter mappings.
"""

import json
import re
import sys
import io
from collections import Counter, defaultdict
from pathlib import Path

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.kg.builder import JamuKG
from src.kg.schema import NodeType, EdgeType

# ICD-10 chapter mapping for common traditional medicine terms
# Maps raw disease names -> (normalized_name, icd10_chapter, category)
DISEASE_MAP = {
    # --- Infectious diseases (A00-B99) ---
    "fever": ("Fever", "A/B", "infectious"),
    "malaria": ("Malaria", "B50-B54", "infectious"),
    "dysentery": ("Dysentery", "A06/A03", "infectious"),
    "gonorrhea": ("Gonorrhea", "A54", "infectious"),
    "syphilis": ("Syphilis", "A50-A53", "infectious"),
    "tuberculosis": ("Tuberculosis", "A15-A19", "infectious"),
    "leprosy": ("Leprosy", "A30", "infectious"),
    "cholera": ("Cholera", "A00", "infectious"),
    "infection": ("Infection", "A/B", "infectious"),
    "amebiasis": ("Amebiasis", "A06", "infectious"),
    "worms": ("Helminthiasis", "B65-B83", "infectious"),
    "vermifuge": ("Anthelmintic use", "B65-B83", "pharmacological_effect"),
    "fungus": ("Fungal infection", "B35-B49", "infectious"),
    "ringworm": ("Ringworm", "B35", "infectious"),

    # --- Neoplasms (C00-D48) ---
    "tumor": ("Tumor", "C/D", "neoplasm"),
    "cancer": ("Cancer", "C00-C97", "neoplasm"),

    # --- Blood (D50-D89) ---
    "anemia": ("Anemia", "D50-D64", "blood"),

    # --- Endocrine/metabolic (E00-E90) ---
    "diabetes": ("Diabetes", "E10-E14", "endocrine"),
    "goiter": ("Goiter", "E01-E05", "endocrine"),
    "obesity": ("Obesity", "E66", "endocrine"),

    # --- Mental/behavioral (F00-F99) ---
    "insomnia": ("Insomnia", "F51", "mental"),
    "anxiety": ("Anxiety", "F41", "mental"),
    "aphrodisiac": ("Aphrodisiac use", "F52", "pharmacological_effect"),
    "anaphrodisiac": ("Anaphrodisiac use", "F52", "pharmacological_effect"),

    # --- Nervous system (G00-G99) ---
    "epilepsy": ("Epilepsy", "G40", "nervous"),
    "paralysis": ("Paralysis", "G80-G83", "nervous"),
    "neuralgia": ("Neuralgia", "G50-G59", "nervous"),
    "convulsion": ("Convulsion", "G40/R56", "nervous"),

    # --- Eye (H00-H59) ---
    "conjunctivitis": ("Conjunctivitis", "H10", "eye"),
    "blindness": ("Vision disorders", "H53-H54", "eye"),
    "cataract": ("Cataract", "H25-H26", "eye"),
    "ophthalmia": ("Eye inflammation", "H10-H13", "eye"),

    # --- Ear (H60-H95) ---
    "earache": ("Earache", "H92", "ear"),
    "deafness": ("Hearing loss", "H90-H91", "ear"),

    # --- Circulatory (I00-I99) ---
    "hypertension": ("Hypertension", "I10-I15", "circulatory"),
    "hemorrhage": ("Hemorrhage", "I60-I62/R58", "circulatory"),
    "heart": ("Heart disease", "I00-I52", "circulatory"),
    "angina": ("Angina", "I20", "circulatory"),
    "stroke": ("Stroke", "I60-I69", "circulatory"),
    "hemorrhoid": ("Hemorrhoids", "I84", "circulatory"),
    "varicose": ("Varicose veins", "I83", "circulatory"),
    "edema": ("Edema", "R60", "circulatory"),
    "anasarca": ("Edema (generalized)", "R60", "circulatory"),

    # --- Respiratory (J00-J99) ---
    "cough": ("Cough", "R05/J00-J99", "respiratory"),
    "asthma": ("Asthma", "J45", "respiratory"),
    "bronchitis": ("Bronchitis", "J20-J21", "respiratory"),
    "cold": ("Common cold", "J00", "respiratory"),
    "pneumonia": ("Pneumonia", "J12-J18", "respiratory"),
    "catarrh": ("Upper respiratory inflammation", "J00-J06", "respiratory"),

    # --- Digestive (K00-K93) ---
    "diarrhea": ("Diarrhea", "K52/A09", "digestive"),
    "constipation": ("Constipation", "K59.0", "digestive"),
    "dyspepsia": ("Dyspepsia", "K30", "digestive"),
    "colic": ("Colic", "R10", "digestive"),
    "gastritis": ("Gastritis", "K29", "digestive"),
    "hepatitis": ("Hepatitis", "K75/B15-B19", "digestive"),
    "jaundice": ("Jaundice", "R17", "digestive"),
    "nausea": ("Nausea", "R11", "digestive"),
    "vomiting": ("Vomiting", "R11", "digestive"),
    "stomatitis": ("Stomatitis", "K12", "digestive"),

    # --- Skin (L00-L99) ---
    "dermatosis": ("Dermatosis", "L00-L99", "skin"),
    "eczema": ("Eczema", "L20-L30", "skin"),
    "psoriasis": ("Psoriasis", "L40", "skin"),
    "boil": ("Boil/Furuncle", "L02", "skin"),
    "abscess": ("Abscess", "L02", "skin"),
    "itch": ("Pruritus", "L29", "skin"),
    "scabies": ("Scabies", "B86", "skin"),
    "acne": ("Acne", "L70", "skin"),
    "ulcer": ("Skin ulcer", "L97-L98", "skin"),
    "burn": ("Burn", "T20-T32", "skin"),
    "alopecia": ("Alopecia", "L63-L65", "skin"),
    "wound": ("Wound", "T14", "skin"),
    "sore": ("Sore/Ulcer", "L00-L99", "skin"),

    # --- Musculoskeletal (M00-M99) ---
    "rheumatism": ("Rheumatism", "M79", "musculoskeletal"),
    "arthritis": ("Arthritis", "M05-M14", "musculoskeletal"),
    "gout": ("Gout", "M10", "musculoskeletal"),
    "lumbago": ("Low back pain", "M54.5", "musculoskeletal"),
    "sprain": ("Sprain", "S13-S93", "musculoskeletal"),

    # --- Genitourinary (N00-N99) ---
    "kidney": ("Kidney disease", "N00-N29", "genitourinary"),
    "calculus": ("Urinary calculus", "N20-N23", "genitourinary"),
    "amenorrhea": ("Amenorrhea", "N91", "genitourinary"),
    "dysmenorrhea": ("Dysmenorrhea", "N94.4-N94.6", "genitourinary"),
    "leucorrhea": ("Leucorrhea", "N76", "genitourinary"),
    "urethritis": ("Urethritis", "N34", "genitourinary"),

    # --- Pregnancy (O00-O99) ---
    "parturition": ("Childbirth support", "O80-O84", "pregnancy"),
    "abortion": ("Abortifacient use", "O03-O06", "pharmacological_effect"),
    "abortifacient": ("Abortifacient use", "O03-O06", "pharmacological_effect"),
    "abortive": ("Abortifacient use", "O03-O06", "pharmacological_effect"),
    "afterbirth": ("Postpartum care", "O73", "pregnancy"),
    "galactagogue": ("Galactagogue use", "O92", "pharmacological_effect"),

    # --- Symptoms (R00-R99) ---
    "swelling": ("Swelling/Inflammation", "R22/R60", "symptom"),
    "pain": ("Pain", "R52", "symptom"),
    "headache": ("Headache", "R51", "symptom"),
    "vertigo": ("Vertigo", "R42", "symptom"),
    "hiccup": ("Hiccup", "R06.6", "symptom"),
    "thirst": ("Polydipsia", "R63.1", "symptom"),
    "fatigue": ("Fatigue", "R53", "symptom"),

    # --- Injury/poisoning (S/T) ---
    "snakebite": ("Snakebite", "T63.0", "injury"),
    "bite": ("Animal bite", "T63", "injury"),
    "sting": ("Insect sting", "T63", "injury"),
    "fracture": ("Fracture", "S/T", "injury"),

    # --- Additional diseases ---
    "appendicitis": ("Appendicitis", "K35-K37", "digestive"),
    "arrhythmia": ("Arrhythmia", "I49", "circulatory"),
    "beriberi": ("Beriberi", "E51", "endocrine"),
    "beri-beri": ("Beriberi", "E51", "endocrine"),
    "chickenpox": ("Chickenpox", "B01", "infectious"),
    "cholecystitis": ("Cholecystitis", "K81", "digestive"),
    "cirrhosis": ("Liver cirrhosis", "K74", "digestive"),
    "colitis": ("Colitis", "K50-K52", "digestive"),
    "conjunctivitis": ("Conjunctivitis", "H10", "eye"),
    "dropsy": ("Edema/Dropsy", "R60", "circulatory"),
    "elephantiasis": ("Elephantiasis", "B74", "infectious"),
    "enteritis": ("Enteritis", "K50-K52", "digestive"),
    "erysipelas": ("Erysipelas", "A46", "infectious"),
    "filariasis": ("Filariasis", "B74", "infectious"),
    "gangrene": ("Gangrene", "R02", "circulatory"),
    "gastroenteritis": ("Gastroenteritis", "K52", "digestive"),
    "hernia": ("Hernia", "K40-K46", "digestive"),
    "herpes": ("Herpes", "B00", "infectious"),
    "hydrocele": ("Hydrocele", "N43", "genitourinary"),
    "impetigo": ("Impetigo", "L01", "skin"),
    "laryngitis": ("Laryngitis", "J04", "respiratory"),
    "measles": ("Measles", "B05", "infectious"),
    "meningitis": ("Meningitis", "G00-G03", "nervous"),
    "mumps": ("Mumps", "B26", "infectious"),
    "nephritis": ("Nephritis", "N00-N08", "genitourinary"),
    "neuritis": ("Neuritis", "G50-G59", "nervous"),
    "orchitis": ("Orchitis", "N45", "genitourinary"),
    "otitis": ("Otitis", "H65-H67", "ear"),
    "peritonitis": ("Peritonitis", "K65", "digestive"),
    "pharyngitis": ("Pharyngitis", "J02", "respiratory"),
    "pleurisy": ("Pleurisy", "R09.1", "respiratory"),
    "prostatitis": ("Prostatitis", "N41", "genitourinary"),
    "rabies": ("Rabies", "A82", "infectious"),
    "rickets": ("Rickets", "E55", "endocrine"),
    "scurvy": ("Scurvy", "E54", "endocrine"),
    "septicemia": ("Septicemia", "A41", "infectious"),
    "smallpox": ("Smallpox", "B03", "infectious"),
    "tetanus": ("Tetanus", "A35", "infectious"),
    "thrush": ("Oral thrush", "B37", "infectious"),
    "tonsillitis": ("Tonsillitis", "J03", "respiratory"),
    "typhoid": ("Typhoid", "A01", "infectious"),
    "urticaria": ("Urticaria", "L50", "skin"),
    "varicella": ("Chickenpox", "B01", "infectious"),
    "wart": ("Wart", "B07", "skin"),
    "whooping": ("Whooping cough", "A37", "respiratory"),
    "yaws": ("Yaws", "A66", "infectious"),
    "prolapse": ("Prolapse", "N81", "genitourinary"),
    "hemorrhoids": ("Hemorrhoids", "I84", "circulatory"),
    "piles": ("Hemorrhoids", "I84", "circulatory"),
    "spleen": ("Spleen disorders", "D73", "blood"),
    "liver": ("Liver disease", "K70-K77", "digestive"),
    "bladder": ("Bladder disease", "N30-N32", "genitourinary"),
    "cataract": ("Cataract", "H25-H26", "eye"),
    "glaucoma": ("Glaucoma", "H40", "eye"),
    "pleurisy": ("Pleurisy", "R09.1", "respiratory"),
    "bronchosis": ("Bronchial disease", "J40-J47", "respiratory"),
    "cardiopathy": ("Heart disease", "I00-I52", "circulatory"),
    "adenopathy": ("Lymphadenopathy", "R59", "symptom"),
    "ascites": ("Ascites", "R18", "digestive"),
    "cachexia": ("Cachexia", "R64", "symptom"),
    "chlorosis": ("Chlorosis/Anemia", "D50", "blood"),
    "condyloma": ("Condyloma", "A63", "infectious"),
    "contusion": ("Bruise", "T14", "injury"),
    "bruise": ("Bruise", "T14", "injury"),
    "blister": ("Blister", "T14", "skin"),
    "carbuncle": ("Carbuncle", "L02", "skin"),
    "callus": ("Callus", "L84", "skin"),
    "corn": ("Corn", "L84", "skin"),
    "chill": ("Chills/Rigor", "R68.83", "symptom"),
    "chills": ("Chills/Rigor", "R68.83", "symptom"),
    "congestion": ("Congestion", "R09", "symptom"),

    # --- Body parts (map to associated disorders) ---
    "abdomen": ("Abdominal complaints", "R10", "symptom"),
    "ankle": ("Ankle complaints", "M25", "musculoskeletal"),
    "bones": ("Bone disorders", "M80-M89", "musculoskeletal"),
    "bowel": ("Bowel disorders", "K55-K63", "digestive"),
    "brain": ("Brain disorders", "G00-G99", "nervous"),
    "breast": ("Breast disorders", "N60-N64", "genitourinary"),
    "chest": ("Chest complaints", "R07", "symptom"),
    "skin": ("Skin conditions", "L00-L99", "skin"),
    "eye": ("Eye disorders", "H00-H59", "eye"),

    # --- Pharmacological effects (not diseases) ---
    "diuretic": ("Diuretic use", None, "pharmacological_effect"),
    "purgative": ("Purgative use", None, "pharmacological_effect"),
    "laxative": ("Laxative use", None, "pharmacological_effect"),
    "emetic": ("Emetic use", None, "pharmacological_effect"),
    "antiemetic": ("Antiemetic use", None, "pharmacological_effect"),
    "tonic": ("Tonic use", None, "pharmacological_effect"),
    "sedative": ("Sedative use", None, "pharmacological_effect"),
    "stimulant": ("Stimulant use", None, "pharmacological_effect"),
    "anodyne": ("Analgesic use", None, "pharmacological_effect"),
    "antidote": ("Antidote use", None, "pharmacological_effect"),
    "alterative": ("Alterative use", None, "pharmacological_effect"),
    "antiseptic": ("Antiseptic use", None, "pharmacological_effect"),
    "antispasmodic": ("Antispasmodic use", None, "pharmacological_effect"),
    "aperient": ("Mild laxative use", None, "pharmacological_effect"),
    "astringent": ("Astringent use", None, "pharmacological_effect"),
    "carminative": ("Carminative use", None, "pharmacological_effect"),
    "cathartic": ("Cathartic use", None, "pharmacological_effect"),
    "choleretic": ("Choleretic use", None, "pharmacological_effect"),
    "cicatrizant": ("Wound healing use", None, "pharmacological_effect"),
    "contraceptive": ("Contraceptive use", None, "pharmacological_effect"),
    "cordial": ("Cordial/Tonic use", None, "pharmacological_effect"),
    "demulcent": ("Demulcent use", None, "pharmacological_effect"),
    "depurative": ("Depurative use", None, "pharmacological_effect"),
    "digestive": ("Digestive aid", None, "pharmacological_effect"),
    "emmenagogue": ("Emmenagogue use", None, "pharmacological_effect"),
    "emollient": ("Emollient use", None, "pharmacological_effect"),
    "expectorant": ("Expectorant use", None, "pharmacological_effect"),
    "febrifuge": ("Antipyretic use", None, "pharmacological_effect"),
    "hemostatic": ("Hemostatic use", None, "pharmacological_effect"),
    "hepatoprotective": ("Hepatoprotective use", None, "pharmacological_effect"),
    "narcotic": ("Narcotic use", None, "pharmacological_effect"),
    "nervine": ("Nervine use", None, "pharmacological_effect"),
    "pectoral": ("Pectoral use", None, "pharmacological_effect"),
    "refrigerant": ("Cooling agent use", None, "pharmacological_effect"),
    "resolvent": ("Resolvent use", None, "pharmacological_effect"),
    "rubefacient": ("Rubefacient use", None, "pharmacological_effect"),
    "stomachic": ("Stomachic use", None, "pharmacological_effect"),
    "styptic": ("Styptic use", None, "pharmacological_effect"),
    "sudorific": ("Diaphoretic use", None, "pharmacological_effect"),
    "suppurative": ("Suppurative use", None, "pharmacological_effect"),
    "vulnerary": ("Vulnerary/Wound healing", None, "pharmacological_effect"),
    "antiphlogistic": ("Anti-inflammatory use", None, "pharmacological_effect"),
    "anorectic": ("Appetite suppressant", None, "pharmacological_effect"),
    "cardioactive": ("Cardioactive use", None, "pharmacological_effect"),
    "collyrium": ("Eye wash use", None, "pharmacological_effect"),
    "cataplasm": ("Poultice use", None, "pharmacological_effect"),

    # --- Non-medical ---
    "piscicide": ("Fish poison", None, "non_medical"),
    "insecticide": ("Insecticide", None, "non_medical"),
    "acaricide": ("Acaricide", None, "non_medical"),
    "cosmetic": ("Cosmetic use", None, "non_medical"),
    "spice": ("Spice/Condiment", None, "non_medical"),
    "arrow-poison": ("Arrow poison", None, "non_medical"),
    "birdlime": ("Birdlime", None, "non_medical"),
    "canicide": ("Canicide", None, "non_medical"),
    "chewstick": ("Dental hygiene", None, "non_medical"),
    "dye": ("Dye", None, "non_medical"),
    "fiber": ("Fiber/Material", None, "non_medical"),
    "fumitory": ("Fumigation", None, "non_medical"),
    "incense": ("Incense", None, "non_medical"),
    "preservative": ("Preservative", None, "non_medical"),
    "soap": ("Soap/Cleaning", None, "non_medical"),
    "timber": ("Timber", None, "non_medical"),
    "artemicide": ("Artemicide", None, "non_medical"),
    "ascaricide": ("Ascaricide", None, "non_medical"),
    "centipede": ("Centipede treatment", None, "non_medical"),
}


def normalize_disease_name(raw_name: str) -> tuple:
    """
    Normalize a disease name.
    Returns (normalized_name, icd10_code, category).
    """
    clean = raw_name.strip().rstrip("?").lower()

    # Direct lookup
    if clean in DISEASE_MAP:
        return DISEASE_MAP[clean]

    # Handle Ache(X) pattern
    ache_match = re.match(r"ache\((\w+)\)", clean)
    if ache_match:
        body_part = ache_match.group(1).capitalize()
        if body_part == "Head":
            return ("Headache", "R51", "symptom")
        elif body_part == "Tooth":
            return ("Toothache", "K08.8", "digestive")
        elif body_part == "Stomach":
            return ("Stomachache", "R10", "digestive")
        elif body_part == "Back":
            return ("Back pain", "M54", "musculoskeletal")
        elif body_part == "Ear":
            return ("Earache", "H92", "ear")
        elif body_part == "Chest":
            return ("Chest pain", "R07", "symptom")
        else:
            return (f"{body_part} pain", "R52", "symptom")

    # Handle Antidote(X) pattern
    antidote_match = re.match(r"antidote\((.+)\)", clean)
    if antidote_match:
        return ("Antidote use", None, "pharmacological_effect")

    # Handle KNApSAcK effect groups (already good)
    knapsack_groups = {
        "musculoskeletal and connective tissue disorders": ("Musculoskeletal disorders", "M00-M99", "musculoskeletal"),
        "gastrointestinal disorders": ("Gastrointestinal disorders", "K00-K93", "digestive"),
        "female reproductive organ problems": ("Gynecological disorders", "N70-N98", "genitourinary"),
        "disorders of appetite": ("Appetite disorders", "R63", "symptom"),
        "pain/inflammation": ("Pain/Inflammation", "R52/M79", "symptom"),
    }
    if clean in knapsack_groups:
        return knapsack_groups[clean]

    # Partial matching
    for key, value in DISEASE_MAP.items():
        if key in clean or clean in key:
            return value

    # Default: keep original, categorize as unknown
    return (raw_name.strip().rstrip("?"), None, "unknown")


def normalize_all_diseases(kg: JamuKG) -> dict:
    """Normalize all disease names in the KG and return statistics."""
    categories = Counter()
    icd10_mapped = 0
    total = 0
    normalized_map = {}

    for n, data in kg.graph.nodes(data=True):
        if data.get("node_type") != NodeType.DISEASE.value:
            continue

        raw_name = data.get("name", n)
        normalized, icd10, category = normalize_disease_name(raw_name)

        total += 1
        categories[category] += 1
        if icd10:
            icd10_mapped += 1

        normalized_map[n] = {
            "raw": raw_name,
            "normalized": normalized,
            "icd10": icd10 or "",
            "category": category,
        }

        # Update node in graph
        data["normalized_name"] = normalized
        if icd10:
            data["icd10_code"] = icd10
        data["disease_category"] = category

    return {
        "total_diseases": total,
        "icd10_mapped": icd10_mapped,
        "icd10_pct": round(icd10_mapped / max(total, 1) * 100, 1),
        "categories": dict(categories.most_common()),
        "normalized_map": normalized_map,
    }


def main():
    base_dir = Path(__file__).parent.parent.parent
    kg_dir = base_dir / "data" / "kg"

    kg = JamuKG()
    kg.load(str(kg_dir / "jamukg_v02_annotated.json"))

    print("Normalizing disease names...")
    result = normalize_all_diseases(kg)

    print(f"\nTotal diseases: {result['total_diseases']}")
    print(f"ICD-10 mapped: {result['icd10_mapped']} ({result['icd10_pct']}%)")
    print(f"\nCategories:")
    for cat, count in result["categories"].items():
        print(f"  {cat:25s}: {count:>4}")

    # Save normalized KG
    kg.save(str(kg_dir / "jamukg_v02_normalized.json"))
    print(f"\nSaved normalized KG")

    # Save mapping
    map_path = kg_dir / "disease_normalization_map.json"
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Saved mapping to {map_path}")

    return result


if __name__ == "__main__":
    main()
