""" Initial set up

      set FLASK_APP=mnist.py

    Execution

      flask run --host 0.0.0.0
"""

from flask import Flask, render_template, url_for
import os


app = Flask(__name__)


@app.route("/<name>")
def show(name):
    filename = "imgs/" + name
    return render_template(
        "canvas.html",
        name=url_for("static", filename=filename)
    )


@app.route("/")
def index():
    imgs = os.listdir(r"static\imgs")
    return render_template(
        "index.html",
        imgs=imgs
    )
