import re, sys

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def generate_matrix(filename):
    data = []
    all_species = []

    with open(filename, "r") as f:
        lines = f.readlines()[6:]
        for line in lines:
            # species = re.findall(re.compile("[a-zA-Z]*_[a-zA-Z]*"), line)[0].replace(
            #     "_", " "
            # )
            species = re.findall(re.compile(": \S*\s*"), line)[0].split(" ")[1]
            all_species.append(species)
            print(species)

            data_line = re.findall(re.compile("\d+\.\d+"), line)
            data_line_float = []
            for percent in data_line:
                data_line_float.append(round(float(percent), 1))
            data.append(data_line_float)
            print(data_line_float)

    print(data)
    data_array = np.array(data)
    print(data_array)

    plt.rcParams["figure.figsize"] = [8, 8]

    fig, ax = plt.subplots()
    im = ax.imshow(data_array, cmap="PuBu", vmin=0, vmax=100)

    ax.set_xticks(np.arange(len(all_species)), labels=all_species)
    ax.set_yticks(np.arange(len(all_species)), labels=all_species)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for i in range(len(all_species)):
        for j in range(len(all_species)):
            text = ax.text(
                j,
                i,
                data_array[i, j],
                ha="center",
                va="center",
                color="w",
            )

    ax.set_title("Identity matrix")

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.2)
    plt.colorbar(im, cax=cax)
    fig.tight_layout()
    plt.savefig("identity_matrix.pdf", bbox_inches="tight", transparent=True)
    plt.show()


def main():
    return "youpidou"


if __name__ == "__main__":
    print("Doing")
    generate_matrix(sys.argv[1])
