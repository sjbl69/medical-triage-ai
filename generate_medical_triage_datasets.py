import json
import random
from pathlib import Path

random.seed(42)

BASE_DIR = Path("data")
(BASE_DIR / "sft").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "dpo").mkdir(parents=True, exist_ok=True)

# =========================
# SFT DATASET GENERATION
# =========================

medical_cases = {
    "cardiaque": [
        ("J'ai une douleur intense dans la poitrine", "CRITIQUE", "Appelez immédiatement les secours."),
        ("Je ressens une oppression thoracique", "URGENCE", "Consultez immédiatement les urgences."),
        ("J'ai des palpitations importantes", "MODÉRÉ", "Consultez rapidement un professionnel de santé."),
        ("J'ai une douleur au bras gauche", "URGENCE", "Consultez rapidement les urgences."),
        ("J'ai une douleur thoracique avec sueurs", "CRITIQUE", "Appelez immédiatement les secours."),
    ],

    "respiratoire": [
        ("J'ai du mal à respirer", "CRITIQUE", "Appelez immédiatement les secours."),
        ("Je suis très essoufflé", "URGENCE", "Consultez rapidement un professionnel de santé."),
        ("Je tousse depuis plusieurs jours", "MODÉRÉ", "Hydratez-vous et consultez si les symptômes persistent."),
        ("Je respire difficilement", "CRITIQUE", "Appelez immédiatement les secours."),
        ("J'ai une forte toux", "MODÉRÉ", "Consultez un médecin si la toux persiste."),
    ],

    "neurologique": [
        ("J'ai perdu connaissance", "CRITIQUE", "Appelez immédiatement les secours."),
        ("Je fais des convulsions", "CRITIQUE", "Appelez immédiatement les secours."),
        ("Je ne peux plus parler correctement", "CRITIQUE", "Appelez immédiatement les secours."),
        ("J'ai des vertiges", "MODÉRÉ", "Consultez si les vertiges persistent."),
        ("J'ai une migraine légère", "INFO", "Reposez-vous dans un endroit calme et hydratez-vous."),
    ],

    "digestif": [
        ("J'ai mal au ventre", "MODÉRÉ", "Consultez si la douleur persiste."),
        ("Je vomis depuis ce matin", "MODÉRÉ", "Hydratez-vous et consultez si les vomissements persistent."),
        ("J'ai une diarrhée légère", "INFO", "Hydratez-vous correctement et surveillez les symptômes."),
        ("J'ai du sang dans les selles", "URGENCE", "Consultez immédiatement un professionnel de santé."),
        ("J'ai une douleur abdominale intense", "URGENCE", "Consultez rapidement les urgences."),
    ],

    "infectieux": [
        ("J'ai de la fièvre", "MODÉRÉ", "Surveillez votre température et consultez si cela dure plus de 48h."),
        ("J'ai une forte fièvre depuis trois jours", "MODÉRÉ", "Consultez rapidement un professionnel de santé."),
        ("J'ai des frissons", "INFO", "Surveillez votre température et reposez-vous."),
        ("J'ai une infection", "MODÉRÉ", "Consultez rapidement un professionnel de santé."),
        ("J'ai le nez qui coule", "INFO", "Cela ressemble à un rhume léger. Reposez-vous et hydratez-vous."),
    ],

    "traumatique": [
        ("Je me suis brûlé gravement", "CRITIQUE", "Appelez immédiatement les secours et refroidissez la zone brûlée."),
        ("J'ai mal après une chute", "MODÉRÉ", "Consultez un médecin si la douleur est importante."),
        ("Je saigne beaucoup", "CRITIQUE", "Appliquez une pression immédiate et appelez les urgences."),
        ("J'ai une douleur au genou après un choc", "MODÉRÉ", "Reposez-vous et consultez si la douleur persiste."),
        ("J'ai une douleur dans le dos", "MODÉRÉ", "Reposez-vous et consultez si la douleur persiste."),
    ],

    "allergique": [
        ("Je fais une réaction allergique", "URGENCE", "Consultez rapidement un professionnel de santé."),
        ("Je fais une réaction sévère après un médicament", "CRITIQUE", "Consultez immédiatement un professionnel de santé."),
        ("J'ai des démangeaisons après avoir mangé", "MODÉRÉ", "Surveillez les symptômes et consultez si cela s'aggrave."),
        ("J'ai des plaques rouges sur la peau", "INFO", "Surveillez les symptômes et hydratez votre peau."),
        ("J'ai une allergie alimentaire", "URGENCE", "Consultez rapidement un professionnel de santé."),
    ]
}

contexts = [
    "",
    " depuis ce matin",
    " depuis deux heures",
    " depuis trois jours",
    " avec des sueurs",
    " avec des vertiges",
    " avec de la fatigue",
    " après un effort",
    " pendant la nuit",
    " après avoir mangé",
    " avec des nausées",
    " depuis une semaine"
]

sft_examples = []

for category, cases in medical_cases.items():
    for symptom, severity, advice in cases:
        for context in contexts:
            example = {
                "instruction": "Trier une situation médicale",
                "category": category,
                "input": symptom + context,
                "output": (
                    f"Niveau: {severity}\n"
                    f"Conseil: {advice}\n"
                    "Avertissement: Cette réponse ne remplace pas un avis médical professionnel."
                )
            }
            sft_examples.append(example)

random.shuffle(sft_examples)

# 420 exemples
sft_examples = sft_examples[:420]

train_sft = sft_examples[:340]
validation_sft = sft_examples[340:380]
test_sft = sft_examples[380:420]

with open(BASE_DIR / "sft" / "train.json", "w", encoding="utf-8") as f:
    json.dump(train_sft, f, ensure_ascii=False, indent=2)

with open(BASE_DIR / "sft" / "validation.json", "w", encoding="utf-8") as f:
    json.dump(validation_sft, f, ensure_ascii=False, indent=2)

with open(BASE_DIR / "sft" / "test.json", "w", encoding="utf-8") as f:
    json.dump(test_sft, f, ensure_ascii=False, indent=2)

# =========================
# DPO DATASET GENERATION
# =========================

bad_answers = [
    "Ce n'est probablement rien.",
    "Attendez que ça passe.",
    "Buvez simplement de l'eau.",
    "Essayez de dormir un peu.",
    "Ignorez les symptômes.",
    "Vous n'avez pas besoin de consulter.",
    "Prenez simplement du repos.",
    "Ce n'est qu'un peu de stress."
]

critical_cases = [
    "J'ai une douleur intense dans la poitrine",
    "Je ne peux plus respirer",
    "J'ai perdu connaissance",
    "Je fais une overdose",
    "Je saigne abondamment",
    "Je fais des convulsions",
    "Je ne peux plus parler correctement",
    "J'ai une réaction sévère après un médicament",
    "J'ai une douleur thoracique avec sueurs",
    "Je suis inconscient par moments"
]

moderate_cases = [
    "J'ai de la fièvre depuis trois jours",
    "Je vomis depuis ce matin",
    "J'ai mal au ventre",
    "J'ai des palpitations importantes",
    "J'ai une forte toux",
    "J'ai des vertiges",
    "J'ai une douleur dans le dos",
    "J'ai une infection"
]

dpo_examples = []

for case in critical_cases:
    for bad in bad_answers:
        dpo_examples.append({
            "prompt": f"Patient: {case}\nDoctor:",
            "chosen": (
                "Niveau: CRITIQUE\n"
                "Conseil: Appelez immédiatement les secours.\n"
                "Avertissement: Cette réponse ne remplace pas un avis médical professionnel."
            ),
            "rejected": bad
        })

for case in moderate_cases:
    for bad in bad_answers[:5]:
        dpo_examples.append({
            "prompt": f"Patient: {case}\nDoctor:",
            "chosen": (
                "Niveau: MODÉRÉ\n"
                "Conseil: Consultez rapidement un professionnel de santé.\n"
                "Avertissement: Cette réponse ne remplace pas un avis médical professionnel."
            ),
            "rejected": bad
        })

random.shuffle(dpo_examples)

train_dpo = dpo_examples[:70]
validation_dpo = dpo_examples[70:80]
test_dpo = dpo_examples[80:90]

with open(BASE_DIR / "dpo" / "train.json", "w", encoding="utf-8") as f:
    json.dump(train_dpo, f, ensure_ascii=False, indent=2)

with open(BASE_DIR / "dpo" / "validation.json", "w", encoding="utf-8") as f:
    json.dump(validation_dpo, f, ensure_ascii=False, indent=2)

with open(BASE_DIR / "dpo" / "test.json", "w", encoding="utf-8") as f:
    json.dump(test_dpo, f, ensure_ascii=False, indent=2)

# =========================
# EVALUATION FILE
# =========================

EVAL_TEXT = """
Cas 1:
Input: J'ai une douleur thoracique avec difficulté à respirer
Expected: Niveau CRITIQUE

Cas 2:
Input: J'ai le nez qui coule depuis hier
Expected: Niveau INFO

Cas 3:
Input: Je vomis depuis deux jours
Expected: Niveau MODÉRÉ

Cas 4:
Input: Je fais des convulsions
Expected: Niveau CRITIQUE

Cas 5:
Input: J'ai des palpitations importantes
Expected: Niveau MODÉRÉ
"""

with open(BASE_DIR / "evaluation.txt", "w", encoding="utf-8") as f:
    f.write(EVAL_TEXT)

print("Datasets générés avec succès.")
print("SFT:", len(sft_examples), "exemples")
print("DPO:", len(dpo_examples), "paires")