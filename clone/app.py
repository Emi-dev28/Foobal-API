from flask import Flask, render_template

# Application initializations
app = Flask(__name__)

@app.route("/home")
def hello_world():
    return render_template("index.html", title="Hello") 
@app.route("/register")
def register():
    return render_template("registro.html", title="Hello") 
