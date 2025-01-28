from flask import Flask, render_template

devmode = True

app = Flask(__name__)



@app.route('/')
def homepage():
    return 'Projet Famoki'

@app.route('/login')
def page_de_connexion():
    return '/loginRouteVue'


if __name__ == '__main__':
    app.run(port=5000,debug=devmode)