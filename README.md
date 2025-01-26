# Installation
## 1 Cloner ce dépôt dans un dossier de votre choix dans votre ordinateur : 
``` 
git clone git@github.com:kiady696/backend.git
```
## 2 A la racine du projet ``` je/sais/pas/backend/ ```,  Créer votre environnement virtuel python : 
   - Si vous utilisez anaconda
   ```
      conda create -n <nom_de_votre_environnement>
   ```
   - Si vous utilisez python sans anaconda
   ```
      python3 -m <nom_de_votre_environnement>
   ```
## 3 Activer l'environnement virtuel : 
   - Si vous utilisez anaconda
   ```
      conda activate <nom_de_votre_environnement>
   ```
   - Si vous utilisez python sans anaconda
   ```
      .<nom_de_votre_environnement>/Scripts/activate
   ```
## 4 Installer les dépendances (ça va installer tout ce qu'il y a dans requirements.txt, même setuptools) 
```
   pip install 
```

# Lancement du serveur de développement
## 5 Lancer le serveur Flask en mode debug : 
```
   flask run --debug
```

Et voilà 
