from flask import Flask, render_template

# Application initializations
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")