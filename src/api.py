from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Medical Triage API",
    description="API de triage médical (POC IA + règles de sécurité)",
    version="1.0"
)

class PromptRequest(BaseModel):
    prompt: Optional[str] = ""

@app.get("/")
def root():
    return {
        "status": "API running"
    }

@app.get("/test")
def test():
    return {
        "message": "test ok"
    }

@app.post("/generate")
def generate(request: PromptRequest):

    text = request.prompt.lower()

    if "poitrine" in text:
        response = "⚠️ URGENCE : Appelez immédiatement les secours."

    elif "respirer" in text:
        response = "⚠️ Difficulté respiratoire détectée. Appelez les urgences."

    elif "saignement" in text:
        response = "⚠️ Saignement important. Contactez les secours."

    elif "fièvre" in text:
        response = "Surveillez la température et reposez-vous."

    else:
        response = "Consultez un professionnel de santé si les symptômes persistent."

    return {
        "prompt": request.prompt,
        "response": response
    }