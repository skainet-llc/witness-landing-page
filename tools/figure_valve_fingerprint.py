#!/usr/bin/env python3
"""Feature fingerprint of one valve stroke as a radar chart (stylised).

    python3 tools/figure_valve_fingerprint.py <fontdir> <out.svg>

Six features per stroke on six axes: the learned normal range as a band and
one deviating stroke on top, legend below. Illustrative shapes, not measurements; the axes
carry no numbers on purpose. Same size and palette as the use-case figures.
"""
import os
import sys

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

DARK = "#262626"
RED = "#E83B3B"
PANEL = "#F2F2F2"
TEXT = "#3C3B3B"
GREY = "#9A9A9A"
LINE = "#D9D9D9"

MM = 1 / 25.4
W, H = 87, 62  # mm; same width as the other use-case figures

FEATURES = ["duration", "start-up\npeak current", "energy",
            "end-position\npeak", "current\nprofile", "power\nfactor"]
NORMAL_LO = [0.50, 0.52, 0.50, 0.48, 0.52, 0.50]
NORMAL_HI = [0.68, 0.70, 0.68, 0.66, 0.70, 0.68]
STROKE = [0.90, 0.66, 0.86, 0.97, 0.63, 0.57]
DEVIATES = [0, 2, 3]


def setup_fonts(fontdir):
    family = "sans-serif"
    for name in ("Regular", "SemiBold", "Bold"):
        path = os.path.join(fontdir, "Biryani-%s.ttf" % name)
        if os.path.exists(path):
            font_manager.fontManager.addfont(path)
            family = "Biryani"
    plt.rcParams.update({"font.family": family, "font.size": 6.6,
                         "text.color": TEXT, "svg.fonttype": "path",
                         "svg.hashsalt": "witness"})


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    setup_fonts(sys.argv[1])
    n = len(FEATURES)
    ang = np.pi / 2 - 2 * np.pi * np.arange(n) / n  # clockwise from the top

    def pts(r):
        r = np.broadcast_to(np.asarray(r, dtype=float), (n,))
        return np.column_stack([r * np.cos(ang), r * np.sin(ang)])

    fig = plt.figure(figsize=(W * MM, H * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    top, bottom = 1.42, -1.86  # room for the legend row below the radar
    half_w = (top - bottom) / 2 * W / H
    ax.set_xlim(-half_w, half_w)
    ax.set_ylim(bottom, top)
    ax.set_aspect("equal")
    ax.axis("off")

    for r in (0.25, 0.5, 0.75, 1.0):
        ax.add_patch(Polygon(pts(r), closed=True, fill=False, ec=LINE,
                             lw=0.5))
    for x, y in pts(1.0):
        ax.plot([0, x], [0, y], color=LINE, lw=0.5)

    # learned normal range as a band
    band = np.vstack([pts(NORMAL_HI), pts(NORMAL_HI)[:1],
                      pts(NORMAL_LO)[:1], pts(NORMAL_LO)[::-1]])
    ax.add_patch(Polygon(band, closed=True, fc=DARK, alpha=0.16, lw=0))
    mid = (np.array(NORMAL_LO) + np.array(NORMAL_HI)) / 2
    ax.add_patch(Polygon(pts(mid), closed=True, fill=False, ec=DARK, lw=1.1))

    # one deviating stroke
    s = pts(STROKE)
    ax.add_patch(Polygon(s, closed=True, fc=RED, alpha=0.10, lw=0))
    ax.add_patch(Polygon(s, closed=True, fill=False, ec=RED, lw=1.0,
                         ls=(0, (3, 1.6))))
    ax.scatter(s[:, 0], s[:, 1], s=7, c=[RED if i in DEVIATES else DARK
                                         for i in range(n)], lw=0, zorder=4)

    for i, ((x, y), name) in enumerate(zip(pts(1.13), FEATURES)):
        ha = "center" if abs(x) < 0.1 else ("left" if x > 0 else "right")
        va = "bottom" if y > 0.9 else ("top" if y < -0.9 else "center")
        ax.text(x, y, name, ha=ha, va=va, linespacing=1.15,
                color=RED if i in DEVIATES else TEXT)

    # legend row below the radar
    ly = -1.66
    lx = -2.02
    ax.add_patch(Polygon([[lx, ly - 0.07], [lx + 0.3, ly - 0.07],
                          [lx + 0.3, ly + 0.07], [lx, ly + 0.07]],
                         closed=True, fc=DARK, alpha=0.16, lw=0))
    ax.plot([lx, lx + 0.3], [ly, ly], color=DARK, lw=1.1)
    ax.text(lx + 0.38, ly, "learned normal", va="center")
    lx = -0.42
    ax.plot([lx, lx + 0.3], [ly, ly], color=RED, lw=1.0, ls=(0, (3, 1.6)))
    ax.text(lx + 0.38, ly, "this stroke", va="center")
    lx = 0.92
    ax.scatter([lx + 0.06], [ly], s=7, c=RED, lw=0)
    ax.text(lx + 0.2, ly, "outside normal", va="center", color=RED)

    fig.savefig(sys.argv[2], format="svg", metadata={"Date": None})


if __name__ == "__main__":
    main()
