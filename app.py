from flask import Flask, render_template
from flask import Flask, request, session, jsonify
import xgboost as xgb
import uuid
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import uuid
from sklearn.preprocessing import LabelEncoder


devmode = True

app = Flask(__name__)
app.secret_key = 'user01'
app.config['UPLOAD_FOLDER'] = './uploads'



@app.route('/')
def homepage():
    return 'Projet Famoki'

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
    idFile = "TEST"
    yColumn = "variety"
    print(model_choice,idFile,yColumn)

    df = pd.read_csv(f"./uploads/{idFile}.csv")
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


if __name__ == '__main__':
    app.run(port=5000,debug=devmode)