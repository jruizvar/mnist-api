""" Initial set up

      set FLASK_APP=mnist.py

    Execution

      flask run --host 0.0.0.0
"""
from flask import Flask, flash, redirect, render_template, request, url_for
from joblib import load
from skimage import io, util
import numpy as np
import os


app = Flask(__name__)


def model(name):
    img_path = os.path.join("static", "imgs", name)
    im = io.imread(img_path, as_gray=True)
    clf = load(os.path.join("static", "models", "mnist_svm.joblib"))
    X = np.reshape(util.invert(im), (1, im.size))
    prediction = clf.predict(X)
    return prediction[0]


@app.route("/<name>")
def show(name):
    filename = "imgs/" + name
    return render_template(
        "canvas.html",
        name=url_for("static", filename=filename)
    )


@app.route("/<name>/delete", methods=["POST"])
def delete(name):
    filename = os.path.join("static", "imgs", name)
    os.remove(filename)
    return redirect(url_for("index"))


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
            return redirect(request.url)
    imgs = os.listdir(os.path.join("static", "imgs"))
    return render_template(
        "index.html",
        imgs=imgs
    )
