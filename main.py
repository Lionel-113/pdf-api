from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from docx import Document
import os
import json

app = FastAPI()

TEMPLATES_DIR = "templates"
CONFIG_FILE = "config.json"
OUTPUT_DOCX = "output.docx"
OUTPUT_PDF = "output.pdf"

# Charger le token API depuis config.json
if not os.path.exists(CONFIG_FILE):
    raise RuntimeError("Le fichier de configuration 'config.json' est introuvable")

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

API_TOKEN = config.get("api_token")
if not API_TOKEN:
    raise RuntimeError("Token API non défini dans 'config.json'")

def check_token(auth_header: str):
    """Vérifie que le token fourni est valide via le header Authorization."""
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant ou mal formaté")
    
    token = auth_header.split(" ")[1]  # Extraire le token après "Bearer"
    
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Token invalide")

@app.get("/list-templates/")
async def list_templates(authorization: str = Header(None)):
    """Liste les modèles disponibles avec authentification via header"""
    check_token(authorization)
    files = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".docx")]
    return {"templates": files}

@app.post("/generate-pdf/")
async def generate_pdf(modele: str, data: dict, authorization: str = Header(None)):
    """Génère un PDF à partir d'un modèle DOCX choisi avec authentification via header"""
    check_token(authorization)

    template_path = os.path.join(TEMPLATES_DIR, modele)
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Modèle introuvable")

    doc = Document(template_path)
    for para in doc.paragraphs:
        for key, value in data.items():
            para.text = para.text.replace(f"{{{{{key}}}}}", str(value))

    doc.save(OUTPUT_DOCX)

    os.system(f'libreoffice --headless --convert-to pdf "{OUTPUT_DOCX}" --outdir .')

    if not os.path.exists(OUTPUT_PDF):
        raise HTTPException(status_code=500, detail="Erreur lors de la conversion en PDF")

    return FileResponse(OUTPUT_PDF, media_type="application/pdf", filename="document.pdf")
