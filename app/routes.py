import os

from flask import (
    render_template,
    request,
    abort,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename

from config import Config
from app import app, im, colour_maps
from app.forms import SubmissionForm


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.errorhandler(400)
def too_large(e):
    return "Invalid MIME type", 400


@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html", title="Scientific web apps")


@app.route("/pim", methods=["GET", "POST"])
@app.route("/pim.html", methods=["GET", "POST"])
def pim():
    form = SubmissionForm()
    cmaps = []
    for cmap_name in colour_maps.cmap_list:
        cmap = colour_maps.plot_single_color_gradient(cmap_name)
        cmaps.append(cmap)

    if form.validate_on_submit():
        selected_cmap = form.colour_map.data

        mimetype = form.file.data.content_type
        if mimetype == "text/plain":
            filename = secure_filename(form.file.data.filename)
            form.file.data.save("uploads/" + filename)
            pngImageB64String, filename = im.generate_matrix(filename, selected_cmap)

            return render_template(
                "pim_result.html",
                title="Resulting Percent Identity Matrix",
                png_image=pngImageB64String,
                filename=filename,
                selected_cmap=selected_cmap,
            )

        else:
            abort(400)

    return render_template(
        "pim.html",
        title="Percent Identity Matrix Generator",
        form=form,
        cmaps=cmaps,
    )


@app.route("/colour_maps", methods=["GET"])
def show_colour_maps():
    colour_map_B64 = colour_maps.plot_color_gradients()
    cmap_list = colour_maps.cmap_list
    return render_template("colour_maps.html", cmap=colour_map_B64, cmap_list=cmap_list)


@app.route("/test", methods=["GET"])
def test():
    return render_template("test.html")
