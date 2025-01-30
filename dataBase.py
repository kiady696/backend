from flask_session import Session
from flask_bcrypt import Bcrypt 
from functools import wraps
from flask.globals import session
import os
import json
import random

class DataBase():
    def __init__(self,app):
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_TYPE"] = "filesystem"
        Session(app)
        self.__bcrypt = Bcrypt(app)
        self.app = app
        if "DATABASE_FOLDER" not in app.config: app.config["DATABASE_FOLDER"] = '.'
        self.savePath = os.path.join(app.config["DATABASE_FOLDER"],"db.json")
        if os.path.exists(self.savePath):
            with open(self.savePath, 'r') as openfile:
                self.database = json.load(openfile)
        else:
            self.database = {'users':{},'models':{}}
            self.addNewUser("admin","admin")
            self.__save()
    
    def login_required(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if self.isLogged():
                return f(*args, **kwargs)
            return {},401
        return decorated_function
    
    def isLogged(self):
        return session.get('name') in self.database['users']
    
    def usernameAlreadyExist(self,name):
        return name in self.database['users']

    def isValidUser(self,name,password):
        if name in self.database['users']:
            if self.__bcrypt.check_password_hash(self.database['users'][name]['password'], password+self.database['users'][name]['salt']):
                session['name'] = name
                return True
        return False
    
    def addNewUser(self,name,password):
        salt = ''.join(chr(random.randint(48,123)) for _ in range(16))
        password = self.__bcrypt.generate_password_hash(password+salt).decode('utf-8') 
        self.database['users'][name] = {"password":password,"models":[],"datasets":[],'salt':salt}
        self.__save()
        if(session.accessed):session['name'] = name

    def getCurrentUsername(self):
        return session.get('name')

    def logout(self):
        del session['name']

    def predictionCounterIncrement(self,token):
        self.database['models'][token]['predictionCount']+=1
        self.__save()

    def deleteUser(self,name):
        del self.database['users'][name]
        self.__save()
    
    def addModel(self,token):
        self.database['users'][session['name']]['models'].append(token)
        self.database['models'][token] = {'owner':session['name'],'predictionCount':0}
        self.__save()
    
    def getListModel(self):
        return {k:v['predictionCount'] for k,v in self.database['models'].items() if v['owner']==session['name'] }
    
    def removeModel(self,token):
        if self.database['models'][token]['owner'] == session.get('name'):
            del self.database['models'][token]
            self.database['users'][session.get('name')]['models'].remove(token)
            return True
        return False

    def addDatasets(self,dataset):
        self.database['users'][session['name']]['datasets'].append(dataset)
        self.__save()
    
    def getListDatasets(self):
        return self.database['users'][session['name']]['datasets']
    
    def __save(self):
        with open(self.savePath, "w") as outfile:
            outfile.write(json.dumps(self.database, indent=4))
