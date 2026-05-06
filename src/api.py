from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Medical Triage AI",
    version="1.0"
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "Medical Triage AI API running"}

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