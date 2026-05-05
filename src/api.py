from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import torch
import time
import re
import os
import json

# =========================
# INIT APP
# =========================
app = FastAPI(
    title="Medical Triage API",
    version="1.0",
    description="API de triage médical (POC IA + règles de sécurité)"
)

# =========================
# DEVICE
# =========================
device = 0 if torch.cuda.is_available() else -1

# =========================
# 🔍 DEBUG MODEL FILES (désactivé en CI)
# =========================
if os.getenv("CI") != "true":
    print("FILES IN MODEL:", os.listdir("/app/models/final_model"))
    with open("/app/models/final_model/config.json") as f:
        print("CONFIG LOADED:", json.load(f))

# =========================
# LOAD MODEL (désactivé en CI)
# =========================
if os.getenv("CI") == "true":
    pipe = None
else:
    pipe = pipeline(
        "text-generation",
        model="/app/models/final_model",
        tokenizer="/app/models/final_model",
        device=device
    )

# =========================
# REQUEST SCHEMA
# =========================
class Request(BaseModel):
    symptom: str

# =========================
# CLEAN MODEL OUTPUT
# =========================
def clean_response(text: str) -> str:
    if "Doctor:" in text:
        text = text.split("Doctor:")[-1]

    text = re.sub(r"(Patient:|Doctor:).*", "", text)

    return text.strip()

# =========================
# RULE-BASED SAFETY (AMÉLIORÉ)
# =========================
def rule_based_triage(symptom: str):
    s = symptom.lower()

    if any(x in s for x in [
        "douleur thoracique",
        "poitrine",
        "difficulté à respirer",
        "respirer",
        "essoufflement",
        "perte de connaissance",
        "inconscient",
        "saignement abondant",
        "overdose",
        "convulsion",
        "crise cardiaque",
        "avc"
    ]):
        return "URGENCE", "⚠️ Appelez immédiatement les secours."

    if any(x in s for x in [
        "fièvre élevée",
        "forte fièvre",
        "infection",
        "douleur intense",
        "vomissements persistants",
        "médicament",
        "traitement"
    ]):
        return "ATTENTION", "⚠️ Consultez un professionnel de santé rapidement."

    if any(x in s for x in [
        "rhume",
        "toux légère",
        "mal de gorge",
        "fatigue",
        "nez qui coule"
    ]):
        return "NON_URGENCE", "Reposez-vous et surveillez les symptômes."

    return "CONSULTATION", "Consultez un professionnel de santé."

# =========================
# MAIN ENDPOINT
# =========================
@app.post("/generate")
def generate(req: Request):
    start = time.time()

    triage_rule, message_rule = rule_based_triage(req.symptom)

    prompt = f"Patient: J'ai {req.symptom}\nDoctor:"

    # 👉 gestion CI (sans modèle)
    if pipe is None:
        model_response = "Service indisponible en CI"
    else:
        result = pipe(
            prompt,
            max_new_tokens=40,
            do_sample=False
        )[0]["generated_text"]

        model_response = clean_response(result)

    # priorité sécurité
    if triage_rule in ["URGENCE", "ATTENTION"]:
        final_message = message_rule
    else:
        if (
            len(model_response) < 10
            or "patient" in model_response.lower()
            or "doctor" in model_response.lower()
        ):
            final_message = message_rule
        else:
            final_message = model_response

    latency = time.time() - start

    return {
        "triage": triage_rule,
        "symptom": req.symptom,
        "message": final_message,
        "latency": round(latency, 3)
    }

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {"status": "API running"}

# =========================
# TEST
# =========================
@app.get("/test")
def test():
    return {
        "example": {
            "symptom": "douleur à la poitrine"
        }
    }