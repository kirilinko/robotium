from flask import Flask, render_template

app = Flask(__name__)

# Active le rechargement automatique des templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/connexion")
def sing_in():
    return render_template('sing_in.html')

@app.route("/inscription")
def sing_up():
    return render_template('sing_up.html')

if __name__ == "__main__":
 app.run(debug=True)