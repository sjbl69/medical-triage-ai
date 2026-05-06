from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI(
    title="Medical Triage API",
    version="1.0"
)

# =========================
# REQUEST
# =========================
class Request(BaseModel):
    symptom: str

# =========================
# RULE-BASED TRIAGE
# =========================
def triage(symptom: str):

    s = symptom.lower()

    if any(x in s for x in [
        "poitrine",
        "respirer",
        "saignement",
        "avc",
        "convulsion"
    ]):
        return (
            "URGENCE",
            "Appelez immédiatement les secours."
        )

    if any(x in s for x in [
        "fièvre",
        "douleur",
        "infection"
    ]):
        return (
            "ATTENTION",
            "Consultez rapidement un professionnel de santé."
        )

    return (
        "NON_URGENCE",
        "Reposez-vous et surveillez les symptômes."
    )

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "status": "API running"
    }

# =========================
# TEST
# =========================
@app.get("/test")
def test():
    return {
        "message": "API functional"
    }

# =========================
# GENERATE
# =========================
@app.post("/generate")
def generate(req: Request):

    start = time.time()

    triage_level, message = triage(req.symptom)

    latency = round(time.time() - start, 3)

    return {
        "triage": triage_level,
        "symptom": req.symptom,
        "message": message,
        "latency": latency
    }