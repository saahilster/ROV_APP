from flask import Flask, render_template

HUDweb = Flask(__name__)
ControlApp = Flask(__name__ )

@HUDweb.route("/")
def home():
    return render_template("index.html")

@ControlApp.route("/C")
def homeTwo():
    return render_template("index.html")