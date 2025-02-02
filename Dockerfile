FROM python:3.9

# Installer LibreOffice et dépendances
RUN apt-get update && apt-get install -y libreoffice && \
    pip install --no-cache-dir fastapi uvicorn python-docx

WORKDIR /app
COPY main.py /app/
COPY templates /app/templates/

# Générer un token API aléatoire et l’enregistrer dans config.json
RUN python3 -c "import secrets, json; json.dump({'api_token': secrets.token_hex(32)}, open('/app/config.json', 'w'))" && \
    echo 'TOKEN GÉNÉRÉ :' $(jq -r '.api_token' /app/config.json)

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
