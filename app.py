
from flask import Flask, render_template, request, jsonify
import os
import xgboost as xgb
import uuid
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import uuid
from sklearn.preprocessing import LabelEncoder
from lime.lime_tabular import LimeTabularExplainer
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import base64
from io import BytesIO

devmode = True

app = Flask(__name__)
app.secret_key = 'user01'
app.config['UPLOAD_FOLDER'] = './uploads'


# Répertoire où les fichiers seront sauvegardés temporairement
UPLOAD_FOLDER = 'uploads'

# Crée le dossier uploads si il n'existe pas déjà
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/api/csv', methods=['POST'])
def upload1_csv():
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
                list_col = list(df.columns)
                print("Affichage des colonnes : " , list_col)
            # Retourner un message de succès avec un aperçu des données
                #afficher : nom du fichier, nom des colonnes,  target
                return jsonify({"filename": name_csv, "data_preview": df.head().to_json(),"colonnes": list_col}), 200
            except Exception as e:
                return jsonify({"error": f"Error processing CSV: {str(e)}"}), 500
        else:
            return jsonify({"error": "Invalid file format, only CSV files are allowed"}), 400



        
         

        















    


@app.route('/api/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    idFile = uuid()
    filename = f"./uploads/{idFile}.csv"
    file.save(filename)
    columns = pd.read_csv(filename).columns
    return {"idFile": idFile, "columns": columns}

@app.route('/api/train_model', methods=['POST'])
def train_model():
    # Lecture des paramètres envoyés via la requête JSON
    model_choice = request.json.get('model', 'xgboost')
    idFile = request.json.get('idFile', '')
    yColumn = request.json.get('yColumn', '')

    # Charger le fichier CSV
    df = pd.read_csv(f"./uploads/{idFile}")
    X = df.drop(columns=[yColumn])
    y = df[yColumn]

    # Encodage des labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Séparation en train et test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialisation du modèle selon le choix
    if model_choice == 'random_forest':
        model = RandomForestClassifier(random_state=42)
    elif model_choice == 'xgboost':
        model = xgb.XGBClassifier( eval_metric='mlogloss')
    #use_label_encoder=False,
    # Liste des nombres d'estimateurs à tester
    n_estimators_range = range(10, 510, 10)

    # Listes pour stocker les résultats
    train_accuracies = []
    test_accuracies = []

    # Boucle pour tester différents nombres d'estimateurs
    for n_estimators in n_estimators_range:
        model.set_params(n_estimators=n_estimators)
        model.fit(X_train, y_train)

        # Prédictions et calcul des accuracies
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        train_accuracy = accuracy_score(y_train, y_train_pred)
        test_accuracy = accuracy_score(y_test, y_test_pred)

        train_accuracies.append(train_accuracy)
        test_accuracies.append(test_accuracy)

    # Trouver l'accuracy maximale
    max_accuracy = max(test_accuracies)
    best_n_estimators = n_estimators_range[np.argmax(test_accuracies)]

    # Générer un graphique des accuracies
    fig, ax = plt.subplots()
    ax.plot(n_estimators_range, train_accuracies, label='Train Accuracy', color='blue')
    ax.plot(n_estimators_range, test_accuracies, label='Test Accuracy', color='red')
    ax.set_title('Accuracy vs N Estimators')
    ax.set_xlabel('Number of Estimators')
    ax.set_ylabel('Accuracy')
    ax.legend()

    # Sauvegarder le graphique en base64
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)

    # Préparer la réponse JSON avec le graphique
    response = {
        'model_choice': model_choice,
        'n_estimators_range': list(n_estimators_range),
        'train_accuracies': train_accuracies,
        'test_accuracies': test_accuracies,
        'max_accuracy': max_accuracy,
        'best_n_estimators': best_n_estimators,
        'accuracy_plot': img_b64  # Le graphique en base64
    }

    # Retourner les résultats sous forme de JSON
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)