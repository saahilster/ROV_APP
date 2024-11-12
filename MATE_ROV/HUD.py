from flask import Flask, render_template

HUDweb = Flask(__name__)

@HUDweb.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    HUDweb.run()