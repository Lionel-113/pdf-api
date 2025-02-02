# pdf-api
Build du container :

    docker build -t pdf-api .

Lancer le container pour utiliser les templates inclus dans le container :

    docker run -p 8011:8011 pdf-api

Lancer le container pour utiliser les templates inclus dans le dossier templates local (chargement dynamique des templates) :

    docker run -p 8011:8011 -v .\templates:/app/templates pdf-api

Authentification des requetes par un token.  
Le token est généré à chaque buid et doit etre recupéré dans le container dans le fichier /app/config.json


Liste les templates disponibles :

    curl -X GET "http://localhost:8011/list-templates/"   
    -H "Authorization: Bearer 52549071480d42c42e7e1e09759df3509ef4b69e272b0ffce407dfd7a23faea0"


Requete pour convertir un modele docx en lui passant en parametre les variables.  
Les variables doivent etre au format {{ma_variable}} dans le modèle docx

    curl -X 'POST' \
      'http://localhost:8011/generate-pdf/?modele=fiche.docx' \
      -H "Authorization: Bearer 52549071480d42c42e7e1e09759df3509ef4b69e272b0ffce407dfd7a23faea0" \
      -H 'Content-Type: application/json' \
      -d '{"nom_user": " Dupont", "prenom_user": "Maurice", "brand_computer": "DELL", "model_computer": "Inspiron 5530"}' \
      --output fiche.pdf


