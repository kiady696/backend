from flask import Flask, render_template, request, jsonify
import io
import csv
import pandas as pd
import os


devmode = True

app = Flask(__name__)


# Répertoire où les fichiers seront sauvegardés temporairement
UPLOAD_FOLDER = 'uploads'

# Crée le dossier uploads si il n'existe pas déjà
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/api/csv', methods=['POST'])
def upload_csv():
        file = request.files.get('file')  # Récupère le fichier

        if file and file.filename.endswith('.csv'): #Vérification si le fichier est bien un CSV

            name_csv = file.filename # Get name csv

        # Sauvegarder le fichier temporairement
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

        # Charger le fichier CSV dans un DataFrame Pandas
            try:
                df = pd.read_csv(file_path)
            # Optionnel: tu peux ici faire des opérations sur le DataFrame
                print(df.head())  # Affiche les 5 premières lignes du DataFrame
            
            # Retourner un message de succès avec un aperçu des données
                #afficher : nom du fichier, nom des colonnes,  target
                return jsonify({"filename": name_csv, "data_preview": df.head().to_json()}), 200
            except Exception as e:
                return jsonify({"error": f"Error processing CSV: {str(e)}"}), 500
        else:
            return jsonify({"error": "Invalid file format, only CSV files are allowed"}), 400



        
         

        















    



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)