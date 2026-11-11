"""Plot a likelihood scan from likelihood.txt, nll.txt or deltanll.txt.

Usage: python3 plot_likelihood.py [file] [xmin xmax [ymin ymax]]
The file has two columns: mu and the value of the function.
The plot is saved as a PNG file with the same name, e.g. deltanll.png.
"""
import sys

import matplotlib
matplotlib.use("Agg")  # write files only, no window needed
import matplotlib.pyplot as plt
import numpy as np

filename = sys.argv[1] if len(sys.argv) > 1 else "deltanll.txt"
limits = [float(x) for x in sys.argv[2:6]]
data = np.loadtxt(filename, ndmin=2)
mu, value = data[:, 0], data[:, 1]

fig, ax = plt.subplots()
ax.plot(mu, value, "-")
ax.set_xlabel(r"$\mu$")
ax.set_ylabel(filename.rsplit(".", 1)[0])
if len(limits) >= 2:
    ax.set_xlim(limits[0], limits[1])
    # adjust the y range to the visible points
    visible = (mu >= limits[0]) & (mu <= limits[1]) & np.isfinite(value)
    if len(limits) < 4 and visible.any():
        lo, hi = value[visible].min(), value[visible].max()
        ax.set_ylim(lo - 0.05 * (hi - lo), hi + 0.05 * (hi - lo))
if len(limits) >= 4:
    ax.set_ylim(limits[2], limits[3])
ax.grid(True, alpha=0.3)

output = filename.rsplit(".", 1)[0] + ".png"
fig.savefig(output, dpi=150)
print("saved", output)
