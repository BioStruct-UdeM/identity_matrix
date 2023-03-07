import re, sys
import base64
from io import BytesIO
from pathlib import Path
from datetime import datetime

import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable


def generate_matrix(input_filename, selected_cmap):
    data = []
    all_species = []

    with open("uploads/" + input_filename, "r") as f:
        lines = f.readlines()[6:]
        for line in lines:
            # species = re.findall(re.compile("[a-zA-Z]*_[a-zA-Z]*"), line)[0].replace(
            #     "_", " "
            # )
            species = re.findall(re.compile(": \S*\s*"), line)[0].split(" ")[1]
            all_species.append(species)

            data_line = re.findall(re.compile("\d+\.\d+"), line)
            data_line_float = []
            for percent in data_line:
                data_line_float.append(round(float(percent), 1))
            data.append(data_line_float)
    data_array = np.array(data)

    fig = Figure(figsize=[8, 8], dpi=None, frameon=False)
    Figure.set_layout_engine(fig, layout="tight")

    ax = fig.subplots()
    ident_matrix = ax.imshow(data_array, cmap=selected_cmap, vmin=0, vmax=100)
    ax.set_title("Percent Identity Matrix")
    ax.set_xticks(
        np.arange(len(all_species)), labels=all_species, rotation=45, ha="right"
    )
    ax.set_yticks(np.arange(len(all_species)), labels=all_species)
    for i in range(len(all_species)):
        for j in range(len(all_species)):
            text = ax.text(j, i, data_array[i, j], ha="center", va="center", color="w")

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    Figure.colorbar(fig, mappable=ident_matrix, cax=cax)

    pngImage = BytesIO()
    fig.savefig(pngImage, format="png")
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode("utf8")

    try:
        input_filename.split(".")[1]
        filename = input_filename.split(".")[0]
    except IndexError:
        filename = input_filename

    title = "Percentage Identity Matrix plot"
    author = "Normand Cyr"
    creation_date = datetime.now()
    for file_extension in ["png", "pdf", "svg"]:
        if file_extension == "png":
            metadata = {
                "Title": title,
                "Author": author,
                "Creation time": str(creation_date),
                "Software": "Python Matplotlib",
            }
        elif file_extension == "pdf":
            metadata = {
                "Title": title,
                "Author": author,
                "CreationDate": creation_date,
            }
        elif file_extension == "svg":
            metadata = {
                "Title": title,
                "Creator": author,
                "Date": creation_date,
            }
        else:
            metadata = {
                "Title": title,
            }
        Figure.savefig(
            fig,
            fname=Path(f"./app/static/results/{filename}.{file_extension}"),
            dpi=300,
            format=file_extension,
            bbox_inches="tight",
            transparent=True,
            metadata=metadata,
        )

    return pngImageB64String, filename


if __name__ == "__main__":
    generate_matrix(sys.argv[1])
