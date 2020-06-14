""" Initial set up for local tests

      set FLASK_APP=application.py

    Execution

      flask run --host 0.0.0.0
"""
from flask import (
        Flask, flash, redirect, render_template,
        request, send_from_directory, url_for
        )
from joblib import load
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np
import os


application = Flask(__name__)


def prepimage(im):
    im_gray = np.squeeze(im[:, :, [-1]])
    im_tiny = resize(im_gray, (28, 28))
    im_flat = np.reshape(im_tiny, (1, -1))
    return im_flat


def model(name):
    img_path = os.path.join("static", "imgs", name)
    im = plt.imread(img_path)
    X = prepimage(im)
    clf = load(os.path.join("static", "models", "mnist_svm.joblib"))
    prediction = clf.predict(X)[0]
    return prediction


@application.route("/<name>")
def show(name):
    filename = "imgs/" + name
    prediction = model(name)
    return render_template(
        "canvas.html",
        name=url_for("static", filename=filename),
        prediction=prediction
    )


@application.route("/<name>/delete", methods=["POST"])
def delete(name):
    filename = os.path.join("static", "imgs", name)
    os.remove(filename)
    return redirect(url_for("index"))


@application.route("/", methods=["GET", "POST"])
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


@application.route('/favicon.ico')
def favicon():
    return send_from_directory(
            os.path.join(application.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    application.run()
