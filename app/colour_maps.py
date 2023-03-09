"""
Generation of individual Matplotlib colour maps
Copyright (C) <2023>  <Normand Cyr>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import base64
from io import BytesIO

import numpy as np
import matplotlib as mpl
from matplotlib.figure import Figure

cmap_list = [
    "Greys",
    "Purples",
    "Blues",
    "Greens",
    "Oranges",
    "Reds",
    "YlOrBr",
    "YlOrRd",
    "OrRd",
    "PuRd",
    "RdPu",
    "BuPu",
    "GnBu",
    "PuBu",
    "YlGnBu",
    "PuBuGn",
    "BuGn",
    "YlGn",
]


gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients():
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig = Figure(figsize=[6.4, figh], dpi=None, frameon=False)
    axs = fig.subplots(nrows=nrows + 1)
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh, left=0.2, right=0.99)
    axs[0].set_title("Colormap", fontsize=14)

    for ax, name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect="auto", cmap=mpl.colormaps[name])
        ax.text(
            -0.01,
            0.5,
            name,
            va="center",
            ha="right",
            fontsize=10,
            transform=ax.transAxes,
        )

    for ax in axs:
        ax.set_axis_off()

    colour_map_B64 = save_B64_cmap(fig)

    return colour_map_B64


def plot_single_color_gradient(cmap_name):
    fig = Figure(figsize=[4, 0.25], dpi=None, frameon=False)
    ax = fig.subplots(1, 1)
    fig.subplots_adjust(top=1 - 0.125, bottom=0.125, left=0, right=1)
    ax.imshow(gradient, aspect="auto", cmap=mpl.colormaps[cmap_name])
    ax.set_axis_off()

    return fig


def save_B64_cmap(fig):
    pngImage = BytesIO()
    fig.savefig(pngImage, format="png")
    colour_map_B64 = "data:image/png;base64,"
    colour_map_B64 += base64.b64encode(pngImage.getvalue()).decode("utf8")

    return colour_map_B64


def save_cmap(cmap_name):
    fig = Figure(figsize=[4, 0.25], dpi=None, frameon=False)
    ax = fig.subplots(1, 1)
    fig.subplots_adjust(top=1 - 0.125, bottom=0.125, left=0, right=1)

    try:
        ax.imshow(gradient, aspect="auto", cmap=mpl.colormaps[cmap_name])
        ax.set_axis_off()
        fig.savefig(f"app/static/{cmap_name}.png", format="png")
        return "Colour map saved to disk."
    except KeyError:
        return "Not a known colour map name. See https://matplotlib.org/stable/tutorials/colors/colormaps.html."
