from flask import Flask, render_template, request
import io
import csv
import jsonify


devmode = True

app = Flask(__name__)





@app.route('/api/csv', methods=['POST'])

def upload_csv():
    file = request.files.get('file')  # Récupère le fichier
    if file and file.filename.endswith('.csv'):
        # Lire le contenu du fichier CSV
        content = file.stream.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        
        # Optionnel : faire un traitement sur les données CSV
        data = []
        for row in csv_reader:
            # Par exemple, ici on fait un traitement basique
            processed_row = [field.upper() for field in row]  # Exemple de traitement (mettre en majuscule)
            data.append(processed_row)

        # Retourner les données traitées
    return jsonify(data)  # Renvoie les données traitées au frontend


    



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)