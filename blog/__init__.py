from flask import Flask, render_template, abort, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
