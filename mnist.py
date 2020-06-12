""" Initial set up

      set FLASK_APP=mnist.py

    Execution

      flask run --host 0.0.0.0
"""
from flask import (
        Flask, flash, redirect, render_template, request,
        send_from_directory, url_for
        )
import os


app = Flask(__name__)


@app.route("/model")
def model():
    return "previsao do modelo"


@app.route("/<name>")
def show(name):
    filename = "imgs/" + name
    return render_template(
        "canvas.html",
        name=url_for("static", filename=filename)
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save(os.path.join("static", "imgs", filename))
            return redirect(url_for("uploaded_file", filename=filename))
    imgs = os.listdir(r"static\imgs")
    return render_template(
        "index.html",
        imgs=imgs
    )


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(
            os.path.join("static", "imgs"), filename
            )
