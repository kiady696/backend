from flask import Flask, render_template

devmode = True

app = Flask(__name__)



@app.route('/')
def homepage():
    return 'Projet Famoki'


if __name__ == '__main__':
    app.run(port=5000,debug=devmode)