from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/connexion")
def sing_in():
    return render_template('sing_in.html')

@app.route("/inscription")
def sing_up():
    return render_template('sing_up.html')
