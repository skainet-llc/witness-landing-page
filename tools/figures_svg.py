#!/usr/bin/env python3
"""Render a WITNESS use-case repo's tools/figures.py as SVG instead of PDF.

    python3 tools/figures_svg.py <path/to/figures.py> <outdir> [args ...]

Runs the given figures.py unchanged (its own CLI: outdir first, then e.g.
--travel throw) but redirects every Figure.savefig("*.pdf") to "*.svg".
Text is converted to paths, so the SVGs need no font at view time.
"""
import os
import runpy
import sys

import matplotlib

matplotlib.use("svg")
import matplotlib.figure  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["svg.fonttype"] = "path"
plt.rcParams["svg.hashsalt"] = "witness"  # deterministic ids

_orig = matplotlib.figure.Figure.savefig


def _savefig(self, fname, *args, **kwargs):
    if isinstance(fname, str) and fname.endswith(".pdf"):
        fname = fname[:-4] + ".svg"
        kwargs.setdefault("metadata", {"Date": None})
        kwargs["format"] = "svg"
    return _orig(self, fname, *args, **kwargs)


matplotlib.figure.Figure.savefig = _savefig


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    script = os.path.abspath(sys.argv[1])
    sys.argv = [script] + sys.argv[2:]
    # figures.py calls matplotlib.use("pdf"); harmless, savefig picks the
    # format from the patched file name.
    runpy.run_path(script, run_name="__main__")


if __name__ == "__main__":
    main()
