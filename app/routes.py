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


@app.route("/pim", methods=["GET"])
@app.route("/pim.html", methods=["GET"])
def pim():
    individual_cmaps = {}
    for cmap in colour_maps.cmap_list:
        single_cmap_B64 = colour_maps.plot_single_color_gradient(cmap)
        individual_cmaps[cmap] = single_cmap_B64
    return render_template(
        "pim.html",
        title="Percent Identity Matrix Generator",
        cmap_list=colour_maps.cmap_list,
        individual_cmaps=individual_cmaps,
    )


@app.route("/pim", methods=["POST"])
def upload_pim_file():
    uploaded_file = request.files["text_data_file"]
    selected_cmap = request.form["selected_cmap"]
    if uploaded_file:
        mimetype = uploaded_file.content_type
        if mimetype == "text/plain":
            complete_filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(
                os.path.join(app.config["UPLOAD_PATH"], complete_filename)
            )
            pngImageB64String, filename = im.generate_matrix(
                complete_filename, selected_cmap
            )
            return render_template(
                "pim_result.html",
                title="Resulting Percent Identity Matrix",
                png_image=pngImageB64String,
                filename=filename,
                selected_cmap=selected_cmap,
            )
        else:
            abort(400)
    else:
        return redirect(url_for("index"))


@app.route("/colour_maps", methods=["GET"])
def show_colour_maps():
    colour_map_B64 = colour_maps.plot_color_gradients()
    cmap_list = colour_maps.cmap_list
    return render_template("colour_maps.html", cmap=colour_map_B64, cmap_list=cmap_list)


@app.route("/test", methods=["GET"])
def test():
    return render_template("test.html")
