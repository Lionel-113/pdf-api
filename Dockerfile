FROM python:3.9

# Installer LibreOffice et dépendances
RUN apt-get update && apt-get install -y libreoffice && \
    pip install --no-cache-dir fastapi uvicorn python-docx

WORKDIR /app
COPY main.py /app/
COPY templates /app/templates/

EXPOSE 8011
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8011"]
