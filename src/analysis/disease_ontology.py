"""
Disease Ontology Classifier
============================
Classifies the 642 heterogeneous disease/use terms from Dr. Duke's database
into proper ontological categories:

- clinical_disease: actual diseases (Diabetes, Malaria, Asthma)
- symptom: symptoms/signs (Fever, Headache, Cough)
- pharmacological_action: drug-like actions (Diuretic, Emetic, Laxative)
- therapeutic_use: medical uses that aren't disease names (Wound healing, Antidote)
- cosmetic: cosmetic/beauty uses (Cosmetic, Hair-Tonic, Deodorant)
- biocidal: killing agents (Piscicide, Insecticide, Herbicide)
- non_medical: clearly non-medical uses (Dye, Spice, Incense, Arrow-poison)
- body_part: just a body part, not a condition (Abdomen, Chest, Eye)
- ambiguous: needs manual review

This is foundational work. Every downstream analysis depends on this classification.
"""

import json
import re
from collections import Counter
from pathlib import Path


# === CLASSIFICATION RULES ===
# Order matters: first match wins.

# Pattern-based rules (regex on term)
PATTERN_RULES = [
    # Biocidal agents — things that kill
    (r"(?i)(piscicide|insecticide|larvicide|herbicide|fungicide|acaricide"
     r"|canicide|felicide|vermicide|rodenticide|artemicide|termiticide"
     r"|molluscicide|nematicide)", "biocidal"),

    # Clearly non-medical
    (r"(?i)^(arrow[- ]?poison|homocide|homicide|intoxicant|fish ?bait"
     r"|birdlime|dugout|funereal|incense|chewstick|masticatory"
     r"|spice|dye|ornamental|timber|fiber|paper|soap|sponge"
     r"|candlenut|ligature|liniment|cataplasm)$", "non_medical"),

    # Cosmetic uses
    (r"(?i)(cosmetic|hair[- ]?(tonic|oil|wash|black)|deodorant|deodorant"
     r"|depilatory|dentifrice|freckle|blemish|gray hair|grey hair"
     r"|perfum|mouthwash|gargle)$", "cosmetic"),

    # Pharmacological actions (drug effects, not diseases)
    (r"(?i)^(diuretic|emetic|antiemetic|laxative|cathartic|purgative"
     r"|aperient|carminative|astringent|demulcent|emollient"
     r"|diaphoretic|expectorant|febrifuge|anodyne|stimulant"
     r"|depressant|CNS stimulant|sedative|tonic|alterative"
     r"|choleretic|cardiotonic|cardioactive|counterirritant"
     r"|antiphlogistic|antispasmodic|hemostat|cicatrizant"
     r"|detoxicant|deobstruent|hydragogue|litholytic"
     r"|antiseptic|depurative|rubefacient|vermifuge"
     r"|lactagogue|lactogogue|lactafuge|lactifuge"
     r"|emmenagogue|abortifacient|contraceptive"
     r"|anorectic|aphrodisiac|anaphrodisiac"
     r"|vulnerary|sudorific|sialagogue|stomachic)\\??$", "pharmacological_action"),

    # Veterinary uses
    (r"(?i)\(veterinary\)|\(vet\)", "pharmacological_action"),

    # Antidote subtypes
    (r"(?i)^antidote", "therapeutic_use"),

    # Bite/sting treatments
    (r"(?i)^(bite|sting|jellyfish|centipede|scorpion|bee|bugbite"
     r"|lizardbite|millipede)", "therapeutic_use"),

    # Body parts used as conditions (vague terms)
    (r"(?i)^(abdomen|ankle|bladder|bones|bowel|brain|breast|chest"
     r"|ear|eye|feet|gallbladder|gall|groin|gum|glands|heart"
     r"|intestine|jaw|joint|kidney|knee|leg|lip|liver|loin|lung"
     r"|mouth|nerve|nerves|nose|skin|spleen|stomach|throat"
     r"|tongue|uterus|vagina|vein|womb)$", "body_part"),

    # Symptoms (things you feel/observe, not disease entities)
    (r"(?i)^(fever|cough|headache|ache|pain|swelling|inflammation"
     r"|bleeding|hemorrhage|itch|cramp|cramps|convulsion|fits"
     r"|dizziness|giddiness|vertigo|hiccup|hoarseness|fatigue"
     r"|lassitude|malaise|nausea|insomnia|delirium|dullness"
     r"|edema|dropsy|anasarca|epistaxis|hematemesis|hemoptysis"
     r"|hematuria|hematochezia|metrorrhagia|menorrhagia"
     r"|incontinence|enuresis|flatulence|gas|indigestion"
     r"|heartburn|constipation|halitosis|dandruff|baldness"
     r"|alopecia|chills|burning[- ]feet|heavy legs"
     r"|loose teeth|chafing|blister|callus|corn|bruise"
     r"|contusion|black[- ]eye|lameness|inappetence)\\??$", "symptom"),

    # Ache subtypes
    (r"(?i)^ache\(", "symptom"),

    # Fever subtypes
    (r"(?i)^fever\(", "symptom"),
]

# Exact-match classifications for remaining high-frequency terms
EXACT_CLASSIFICATIONS = {
    # Clinical diseases
    "Abscess": "clinical_disease",
    "Acne": "clinical_disease",
    "Adenopathy": "clinical_disease",
    "Aftosa": "clinical_disease",
    "Ague": "clinical_disease",
    "Amebiasis": "clinical_disease",
    "Amenorrhea": "clinical_disease",
    "Anemia": "clinical_disease",
    "Angina": "clinical_disease",
    "Angina?": "clinical_disease",
    "Appendicitis": "clinical_disease",
    "Arrhythmia": "clinical_disease",
    "Arthritis": "clinical_disease",
    "Arthritis?": "clinical_disease",
    "Ascites": "clinical_disease",
    "Asthma": "clinical_disease",
    "Athlete's-Foot": "clinical_disease",
    "Beri-Beri": "clinical_disease",
    "Beriberi": "clinical_disease",
    "Boil": "clinical_disease",
    "Bronchitis": "clinical_disease",
    "Bronchosis": "clinical_disease",
    "Buboes": "clinical_disease",
    "Burn": "clinical_disease",
    "Burns": "clinical_disease",
    "Cachexia": "clinical_disease",
    "Cancer": "clinical_disease",
    "Cancer(Nose)": "clinical_disease",
    "Cancer(Stomach)": "clinical_disease",
    "Cancer(Uterus)": "clinical_disease",
    "Carbuncle": "clinical_disease",
    "Cardiopathy": "clinical_disease",
    "Cataract": "clinical_disease",
    "Catarrh": "clinical_disease",
    "Cephalgia": "clinical_disease",
    "Cerebrosis": "clinical_disease",
    "Chancre": "clinical_disease",
    "Chickenpox": "clinical_disease",
    "Chickenpox?": "clinical_disease",
    "Cholecystitis": "clinical_disease",
    "Cholecystosis": "clinical_disease",
    "Cholera": "clinical_disease",
    "Chlorosis": "clinical_disease",
    "Cirrhosis": "clinical_disease",
    "Cold": "symptom",
    "Cold(Head)": "symptom",
    "Colic": "symptom",
    "Colitis": "clinical_disease",
    "Condyloma": "clinical_disease",
    "Congestion": "symptom",
    "Conjunctivitis": "clinical_disease",
    "Cystitis": "clinical_disease",
    "Cystitis?": "clinical_disease",
    "Dengue": "clinical_disease",
    "Dengue?": "clinical_disease",
    "Dermatosis": "clinical_disease",
    "Diabetes": "clinical_disease",
    "Diarrhea": "clinical_disease",
    "Diphtheria": "clinical_disease",
    "Dislocation": "therapeutic_use",
    "Dysentery": "clinical_disease",
    "Dysmenorrhea": "clinical_disease",
    "Dyspepsia": "clinical_disease",
    "Dyspnea": "symptom",
    "Dysuria": "symptom",
    "Earache": "symptom",
    "Eczema": "clinical_disease",
    "Enteritis": "clinical_disease",
    "Enteromegaly": "clinical_disease",
    "Enterorrhagia": "symptom",
    "Enterosis": "clinical_disease",
    "Epilepsy": "clinical_disease",
    "Eruption": "symptom",
    "Erysipelas": "clinical_disease",
    "Evil eye": "non_medical",
    "Fistula": "clinical_disease",
    "Food poisoning": "clinical_disease",
    "Fracture": "therapeutic_use",
    "Frambesia": "clinical_disease",
    "Framboesia": "clinical_disease",
    "Furuncle": "clinical_disease",
    "Gangrene": "clinical_disease",
    "Gastralgia": "symptom",
    "Gastritis": "clinical_disease",
    "Gastrointestinal": "body_part",
    "Gastromegaly": "clinical_disease",
    "Gastrosis": "clinical_disease",
    "Gingivitis": "clinical_disease",
    "Gingivosis": "clinical_disease",
    "Glossitis": "clinical_disease",
    "Goiter": "clinical_disease",
    "Gonorrhea": "clinical_disease",
    "Gout": "clinical_disease",
    "Gravel": "clinical_disease",
    "Hemorrhoid": "clinical_disease",
    "Hepatitis": "clinical_disease",
    "Hepatomegaly": "clinical_disease",
    "Hepatosis": "clinical_disease",
    "Herpes": "clinical_disease",
    "Herpes zoster": "clinical_disease",
    "Hydrophobia": "clinical_disease",
    "Hysteria": "clinical_disease",
    "Icterus": "clinical_disease",
    "Impetigo": "clinical_disease",
    "Impotence": "clinical_disease",
    "Impotency": "clinical_disease",
    "Infection": "clinical_disease",
    "Infertility": "clinical_disease",
    "Insanity": "clinical_disease",
    "Internal": "ambiguous",
    "Jaundice": "clinical_disease",
    "Labor": "therapeutic_use",
    "Leprosy": "clinical_disease",
    "Leucoderma": "clinical_disease",
    "Leucorrhea": "clinical_disease",
    "Leukorrhea": "clinical_disease",
    "Lumbago": "clinical_disease",
    "Lunacy": "clinical_disease",
    "Malaria": "clinical_disease",
    "Mange": "clinical_disease",
    "Mastalgia": "symptom",
    "Mastitis": "clinical_disease",
    "Measles": "clinical_disease",
    "Medicine": "ambiguous",
    "Medicine (Vet)": "ambiguous",
    "Memory": "ambiguous",
    "Migraine": "clinical_disease",
    "Miscarriage": "therapeutic_use",
    "Morphinism": "clinical_disease",
    "Morphinism (Opiumism)": "clinical_disease",
    "Mumps": "clinical_disease",
    "Myalgia": "symptom",
    "Ophthalmia": "clinical_disease",
    "Orchitis": "clinical_disease",
    "Otitis": "clinical_disease",
    "Otosis": "clinical_disease",
    "Paralysis": "clinical_disease",
    "Parturition": "therapeutic_use",
    "Piles": "clinical_disease",
    "Pimple": "clinical_disease",
    "Pleurisy": "clinical_disease",
    "Pneumonia": "clinical_disease",
    "Poison": "therapeutic_use",
    "Prolapse": "clinical_disease",
    "Rheumatism": "clinical_disease",
    "Ringworm": "clinical_disease",
    "Scabies": "clinical_disease",
    "Scurvy": "clinical_disease",
    "Smallpox": "clinical_disease",
    "Sore": "symptom",
    "Splenomegaly": "clinical_disease",
    "Sprue": "clinical_disease",
    "Sty": "clinical_disease",
    "Syphilis": "clinical_disease",
    "Tetanus": "clinical_disease",
    "Thrush": "clinical_disease",
    "Tuberculosis": "clinical_disease",
    "Tumor": "clinical_disease",
    "Typhoid": "clinical_disease",
    "Typhus": "clinical_disease",
    "Ulcer": "clinical_disease",
    "Urethritis": "clinical_disease",
    "Urticaria": "clinical_disease",
    "Wart": "clinical_disease",
    "Wound": "therapeutic_use",
    "Yaws": "clinical_disease",

    # More specific
    "Afterbirth": "therapeutic_use",
    "Aphthae": "clinical_disease",
    "Aphthaee": "clinical_disease",
    "Aphthagenic": "clinical_disease",
    "Blennorhea": "clinical_disease",
    "Circumscission": "therapeutic_use",
    "Collyrium": "pharmacological_action",
    "Debility": "symptom",
    "Depression": "clinical_disease",
    "Dhobi Itch": "clinical_disease",
    "Est": "non_medical",
    "Fumitory": "non_medical",
    "Fumitory (Opium substitute)": "non_medical",
    "Illness": "symptom",
    "Longevity": "non_medical",
    "Panacea": "pharmacological_action",
    "Sore": "symptom",
    "Thinness": "symptom",
    "Weakness": "symptom",
    "Worms": "clinical_disease",

    # --- Resolved ambiguous terms (≥2 pairs) ---
    # Conditions/diseases
    "Puerperium": "therapeutic_use",
    "Sore(Throat)": "symptom",
    "Sorethroat?": "symptom",
    "Bilious": "symptom",
    "Scurf": "clinical_disease",
    "Pertussis": "clinical_disease",
    "Pinworms": "clinical_disease",
    "Prickly heat": "clinical_disease",
    "Tumor(Breast)": "clinical_disease",
    "Tumor(Abdomen)": "clinical_disease",
    "Tumor(Belly)": "clinical_disease",
    "Tumor(Gum)": "clinical_disease",
    "Tumor(Hand)": "clinical_disease",
    "Tumor(Neck)": "clinical_disease",
    "Tumor(Scrotum)": "clinical_disease",
    "Tumor(Stomach)": "clinical_disease",
    "Tumor(Uterus)": "clinical_disease",
    "Venereal": "clinical_disease",
    "Sciatica": "clinical_disease",
    "Shingles": "clinical_disease",
    "Phthisis": "clinical_disease",
    "Tapeworm": "clinical_disease",
    "Gallstones": "clinical_disease",
    "Gallstone": "clinical_disease",
    "Obesity": "clinical_disease",
    "Pustule": "clinical_disease",
    "Pustules": "clinical_disease",
    "Scrofula": "clinical_disease",
    "Rickets": "clinical_disease",
    "Varices": "clinical_disease",
    "Varicosity": "clinical_disease",
    "Tinea": "clinical_disease",
    "Pinkeye": "clinical_disease",
    "Pocks": "clinical_disease",
    "Pox": "clinical_disease",
    "Polyps": "clinical_disease",
    "Polyp(Abdomen)": "clinical_disease",
    "Polyp(Nose)": "clinical_disease",
    "Polyp(Stomach)": "clinical_disease",
    "Rhagades": "clinical_disease",
    "Rhematism": "clinical_disease",  # typo for Rheumatism
    "Saccharomycose": "clinical_disease",
    "Sclerosis(Spleen)": "clinical_disease",
    "Whitlow": "clinical_disease",
    "Felon": "clinical_disease",
    "Stroke": "clinical_disease",
    "Dyschezia": "symptom",
    "Vaginamegaly": "clinical_disease",
    "Uteromegaly": "clinical_disease",
    "Gasatromegaly": "clinical_disease",

    # Symptoms
    "Sprain": "symptom",
    "Numbness": "symptom",
    "Spasm": "symptom",
    "Gripes": "symptom",
    "Pyuria": "symptom",
    "Syncope": "symptom",
    "Drunkenness": "symptom",
    "Nervousness": "symptom",
    "Palpitation": "symptom",
    "Palpitations": "symptom",
    "Shortwindedness": "symptom",
    "Stitch": "symptom",
    "Tenesmus": "symptom",
    "Tremors": "symptom",
    "Nightsweats": "symptom",
    "Thirst": "symptom",
    "Weariness": "symptom",
    "Inertia": "symptom",
    "Hematachezia": "symptom",
    "Hematoptysis": "symptom",
    "Rash": "symptom",
    "Pain(Chest)": "symptom",
    "Tinnitus?": "symptom",
    "Hangover": "symptom",
    "Sunstroke": "symptom",

    # Therapeutic uses
    "Pregnancy": "therapeutic_use",
    "Post-Natal": "therapeutic_use",
    "Gynecology": "therapeutic_use",
    "Urogenital": "therapeutic_use",
    "Scald": "therapeutic_use",
    "Splinter": "therapeutic_use",
    "Cut": "therapeutic_use",
    "Thorn": "therapeutic_use",
    "Odontectomy": "therapeutic_use",
    "Dentition": "therapeutic_use",
    "Preventitive": "therapeutic_use",
    "Preventitive(Fever)": "therapeutic_use",
    "Preventitive(Measless)": "therapeutic_use",
    "Yaws (Preventive)": "therapeutic_use",
    "Dislocation": "therapeutic_use",

    # Pharmacological actions
    "Abortive": "pharmacological_action",
    "Abortive?": "pharmacological_action",
    "Poultice": "pharmacological_action",
    "Apertif": "pharmacological_action",
    "Apertif(Veterinary)": "pharmacological_action",
    "Digestive": "pharmacological_action",
    "Digestion": "pharmacological_action",
    "Refrigerant": "pharmacological_action",
    "Resolvent": "pharmacological_action",
    "Cordial": "pharmacological_action",
    "Pectoral": "pharmacological_action",
    "Nervine": "pharmacological_action",
    "Stupefacient": "pharmacological_action",
    "Uterotonic": "pharmacological_action",
    "Vesicant": "pharmacological_action",
    "Salve": "pharmacological_action",
    "Sterilizant": "pharmacological_action",
    "Sternutatory": "pharmacological_action",
    "Mucus-Mover": "pharmacological_action",
    "Convulsion(Pediatric)": "symptom",
    "Anaphrodisiac (Female)": "pharmacological_action",
    "Aphrodisiac(Chinese)": "pharmacological_action",
    "Aphrodisiac(Female)": "pharmacological_action",
    "Tonic (for pubic girls)": "pharmacological_action",
    "Narcotic (Pollen)": "pharmacological_action",

    # Cosmetic
    "Shampoo": "cosmetic",
    "Perfume": "cosmetic",
    "Perfumery": "cosmetic",
    "Toothblack": "cosmetic",
    "Hairblack": "cosmetic",
    "Freckles": "cosmetic",
    "Eye drop": "pharmacological_action",
    "Eyesight": "symptom",
    "Vision": "symptom",
    "Hair": "cosmetic",

    # Non-medical
    "Poison(Arrow)": "non_medical",
    "Tea": "non_medical",
    "Internal": "ambiguous",
    "Medicine": "ambiguous",
    "Medicine (Vet)": "ambiguous",
    "Memory": "pharmacological_action",
    "Deafness": "clinical_disease",
    "Ichthyosarcotoxism": "non_medical",
    "Ichthyosarcotoxin": "non_medical",
    "Opium substitute": "non_medical",
    "Philter": "non_medical",
    "Philtre": "non_medical",
    "Witchcraft": "non_medical",
    "Tattoo": "non_medical",
    "Paste": "non_medical",
    "Oilseed": "non_medical",
    "Vegetable": "non_medical",
    "Sweetener": "non_medical",
    "Tenderizer": "non_medical",
    "Watervine": "non_medical",
    "Water vine": "non_medical",
    "Water": "non_medical",
    "Suriculture": "non_medical",
    "Synergist": "pharmacological_action",

    # Body parts
    "Stone": "clinical_disease",
    "Bladder stone": "clinical_disease",
    "Kidney stones": "clinical_disease",
    "Kidneystone?": "clinical_disease",
    "Cornea": "body_part",
    "Neck": "body_part",
    "Waist": "body_part",
    "Wrist": "body_part",
    "Rib": "body_part",
    "Teeth": "body_part",
    "Female": "body_part",
    "Opacity": "symptom",

    # Repellents — biocidal-adjacent
    "Repellant(Insect)": "biocidal",
    "Repellant(Rat)": "biocidal",
    "Repellant(Tiger)": "biocidal",
    "Leech-repellant": "biocidal",
    "Waspsting": "therapeutic_use",
    "Poison (Fatality)": "non_medical",
    "Poison(Crab)": "therapeutic_use",

    # Skin conditions
    "Cracked feet": "symptom",
    "Cracked lips": "symptom",
    "Cracked skin": "symptom",
    "Dermatitigenic": "clinical_disease",
    "Maculitis": "clinical_disease",
    "Urticant": "non_medical",
    "Urtication": "therapeutic_use",
    "Internulcer": "clinical_disease",
    "Intestinal-Ailments": "clinical_disease",
    "Intoxication": "symptom",
    "Metroxenia": "clinical_disease",
    "Mucositis": "clinical_disease",
}


def classify_term(term: str) -> str:
    """Classify a single disease/use term."""
    term_clean = term.strip()

    # 1. Check exact match first
    if term_clean in EXACT_CLASSIFICATIONS:
        return EXACT_CLASSIFICATIONS[term_clean]

    # 2. Check pattern rules
    for pattern, category in PATTERN_RULES:
        if re.search(pattern, term_clean):
            return category

    # 3. Heuristics for remaining terms
    # Terms ending in -osis, -itis, -emia, -asis are likely diseases
    if re.search(r"(?i)(osis|itis|emia|asis|emia|algia|rrhea|rrhagia)$", term_clean):
        return "clinical_disease"

    # Terms ending in -icide are biocidal
    if re.search(r"(?i)cide$", term_clean):
        return "biocidal"

    # Terms ending in -fugal, -fuge are pharmacological
    if re.search(r"(?i)(fuge|fugal|gogue|lytic|retic|tic)$", term_clean):
        return "pharmacological_action"

    # Terms with ? suffix
    if term_clean.endswith("?"):
        return classify_term(term_clean[:-1])

    # Default: ambiguous — needs manual review
    return "ambiguous"


def classify_all_terms(terms: list[str]) -> dict:
    """Classify all disease terms and return classification map."""
    result = {}
    for term in terms:
        result[term] = classify_term(term)
    return result


def print_classification_summary(classifications: dict, pair_counts: dict = None):
    """Print summary of classification results."""
    from collections import Counter

    cat_counts = Counter(classifications.values())
    total_terms = len(classifications)
    total_pairs = sum(pair_counts.values()) if pair_counts else 0

    print(f"\n{'='*60}")
    print(f"DISEASE ONTOLOGY CLASSIFICATION")
    print(f"{'='*60}")
    print(f"Total terms: {total_terms}")
    if pair_counts:
        print(f"Total pairs: {total_pairs}")
    print()

    for cat in ["clinical_disease", "symptom", "pharmacological_action",
                "therapeutic_use", "cosmetic", "biocidal", "non_medical",
                "body_part", "ambiguous"]:
        terms_in_cat = [t for t, c in classifications.items() if c == cat]
        n_terms = len(terms_in_cat)
        if pair_counts:
            n_pairs = sum(pair_counts.get(t, 0) for t in terms_in_cat)
            print(f"  {cat:25s}: {n_terms:4d} terms, {n_pairs:5d} pairs")
        else:
            print(f"  {cat:25s}: {n_terms:4d} terms")

    # Show ambiguous terms for manual review
    ambiguous = [(t, pair_counts.get(t, 0) if pair_counts else 0)
                 for t, c in classifications.items() if c == "ambiguous"]
    ambiguous.sort(key=lambda x: -x[1])
    if ambiguous:
        print(f"\n--- AMBIGUOUS (needs manual review) ---")
        for term, count in ambiguous:
            print(f"  {term:40s} ({count:3d} pairs)")


def main():
    base_dir = Path(__file__).parent.parent.parent

    # Load PubMed results to get all disease terms with counts
    pubmed_path = base_dir / "data" / "raw" / "pubmed" / "validation_gap_results.json"
    with open(pubmed_path, "r", encoding="utf-8") as f:
        pubmed = json.load(f)

    # Count pairs per disease term
    pair_counts = Counter(r["disease_name"] for r in pubmed)
    all_terms = sorted(pair_counts.keys())

    # Classify
    classifications = classify_all_terms(all_terms)

    # Print summary
    print_classification_summary(classifications, pair_counts)

    # Save
    output_path = base_dir / "data" / "kg" / "disease_ontology.json"
    output = {
        "total_terms": len(classifications),
        "classifications": classifications,
        "category_counts": dict(Counter(classifications.values())),
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {output_path}")

    # Calculate corrected validation gap
    print(f"\n{'='*60}")
    print("CORRECTED VALIDATION GAP")
    print(f"{'='*60}")

    # Only count clinical_disease + symptom as legitimate TREATS
    medical_categories = {"clinical_disease", "symptom"}
    medical_pairs = [r for r in pubmed if classifications.get(r["disease_name"]) in medical_categories]
    medical_none = sum(1 for r in medical_pairs if r["evidence_level"] == "none")
    medical_well = sum(1 for r in medical_pairs if r["evidence_level"] == "well_studied")

    print(f"Medical pairs only: {len(medical_pairs)}/{len(pubmed)}")
    print(f"No evidence: {medical_none}/{len(medical_pairs)} = {medical_none/max(len(medical_pairs),1)*100:.1f}%")
    print(f"Well-studied: {medical_well}/{len(medical_pairs)} = {medical_well/max(len(medical_pairs),1)*100:.1f}%")

    # Including therapeutic uses (wound, fracture, parturition)
    therapeutic_categories = {"clinical_disease", "symptom", "therapeutic_use"}
    therapeutic_pairs = [r for r in pubmed if classifications.get(r["disease_name"]) in therapeutic_categories]
    therapeutic_none = sum(1 for r in therapeutic_pairs if r["evidence_level"] == "none")
    therapeutic_well = sum(1 for r in therapeutic_pairs if r["evidence_level"] == "well_studied")

    print(f"\nMedical + therapeutic uses: {len(therapeutic_pairs)}/{len(pubmed)}")
    print(f"No evidence: {therapeutic_none}/{len(therapeutic_pairs)} = {therapeutic_none/max(len(therapeutic_pairs),1)*100:.1f}%")
    print(f"Well-studied: {therapeutic_well}/{len(therapeutic_pairs)} = {therapeutic_well/max(len(therapeutic_pairs),1)*100:.1f}%")


if __name__ == "__main__":
    main()
