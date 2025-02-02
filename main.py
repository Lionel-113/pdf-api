from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from docx import Document
import os

app = FastAPI()

TEMPLATES_DIR = "templates"
OUTPUT_DOCX = "output.docx"
OUTPUT_PDF = "output.pdf"

@app.get("/list-templates/")
async def list_templates():
    """Liste les modèles disponibles"""
    files = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".docx")]
    return {"templates": files}

@app.post("/generate-pdf/")
async def generate_pdf(modele: str, data: dict):
    """Génère un PDF à partir d'un modèle DOCX choisi."""
    
    template_path = os.path.join(TEMPLATES_DIR, modele)

    # Vérifier si le modèle existe
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Modèle introuvable")

    # Charger le modèle DOCX
    doc = Document(template_path)

    # Remplacer les balises dynamiques (ex: {{nom}}, {{date}})
    for para in doc.paragraphs:
        for key, value in data.items():
            para.text = para.text.replace(f"{{{{{key}}}}}", str(value))

    # Sauvegarde du document modifié
    doc.save(OUTPUT_DOCX)

    # Convertir en PDF avec LibreOffice
    os.system(f'libreoffice --headless --convert-to pdf "{OUTPUT_DOCX}" --outdir .')

    # Vérifier que le PDF a été généré
    if not os.path.exists(OUTPUT_PDF):
        raise HTTPException(status_code=500, detail="Erreur lors de la conversion en PDF")

    # Retourner le fichier PDF généré
    return FileResponse(OUTPUT_PDF, media_type="application/pdf", filename="document.pdf")
