
from flask import Flask, render_template, request, jsonify
import os
import xgboost as xgb
import uuid
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import uuid
from sklearn.preprocessing import LabelEncoder
from dataBase import DataBase

devmode = True

app = Flask(__name__)
app.secret_key = 'user01'
app.config['UPLOAD_FOLDER'] = './uploads'

# Instanciation de l'objet dbe issue de la classe DataBase
db = DataBase(app)


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



        
         

        















    


# @app.route('/api/upload', methods=['POST'])
# def upload_csv():
#     file = request.files['file']
#     idFile = uuid()
#     filename = f"./uploads/{idFile}.csv"
#     file.save(filename)
#     columns = pd.read_csv(filename).columns
#     return {"idFile": idFile, "columns": columns}

@app.route('/api/train_model', methods=['POST'])
def train_model():
    """"model_choice = request.json['model']
    idFile = request.json['idFile']
    yColumn = request.json['yColumn']
    print(model_choice,idFile,yColumn)
    
    df = pd.read_csv(f"./uploads/{idFile}.csv")
    print(df)
    X = df.drop(columns=[yColumn])
    y = df[yColumn]
    
    if model_choice == 'random_forest':
        model = RandomForestClassifier()
        model.fit(X, y)
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
    elif model_choice == 'xgboost':
        model = xgb.XGBClassifier()
        model.fit(X, y)
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)"""
    model_choice = "xgboost"  
    #idFile = "TEST"
    idFile = request.json['file/name']
    yColumn = "variety"
    print(model_choice,idFile,yColumn)

    df = pd.read_csv(f"./uploads/{idFile}")
    print(df)
    X = df.drop(columns=[yColumn])
    y = df[yColumn]
    label_encoder=LabelEncoder()
    y=label_encoder.fit_transform(y)

    if model_choice == 'random_forest':
        model = RandomForestClassifier()
        model.fit(X, y)
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
    elif model_choice == 'xgboost':
        model = xgb.XGBClassifier()
        model.fit(X, y)
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        print(accuracy) 
        return jsonify(accuracy)


@app.route('/')
def homepage():
    return 'Projet Famoki'


@app.route('/api/login')
def page_de_connexion():
    
    # Vérification données envoyées par le front 
    
    # Comparaison des identifiants reçus depuis le front avec chaque users enregistrés
    
    # Génération du token
    
    # retourner un json avec un "{[ Ok : boolean , Message : "message", token : token]}"
    return '/loginRouteVue'


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)