# pdf-api
Build du container :

    docker build -t pdf-api .

Lancer le container pour utiliser les templates inclus dans le container :

    docker run -p 8011:8011 pdf-api

Lancer le container pour utiliser les templates inclus dans le dossier templates local (chargement dynamique des templates) :

    docker run -p 8011:8011 -v .\templates:/app/templates pdf-api

Liste les templates disponibles :

curl -X GET 'http://localhost:8011/list-templates/'


Requete pour convertir un modele docx en lui passant en parametre les variables
LEs variables doivent etre au format {{ma_variable}} dans le modèle docx

curl -X 'POST' \
  'http://localhost:8011/generate-pdf/?modele=fiche.docx' \
  -H 'Content-Type: application/json' \
  -d '{"nom_user": " Dupont", "prenom_user": "Maurice", "brand_computer": "DELL", "model_computer": "Inspiron 5530"}' \
  --output facture.pdf


