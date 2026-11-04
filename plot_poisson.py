"""Plot the histogram from hist.txt or histpoi.txt.

Usage: python3 plot_poisson.py [hist.txt|histpoi.txt]
The plot is saved as a PNG file with the same name, e.g. histpoi.png.
"""
import sys

import matplotlib
matplotlib.use("Agg")  # write files only, no window needed
import matplotlib.pyplot as plt
import numpy as np

filename = sys.argv[1] if len(sys.argv) > 1 else "histpoi.txt"
data = np.loadtxt(filename, ndmin=2)
k, counts = data[:, 0], data[:, 1]

fig, ax = plt.subplots()
ax.bar(k, counts, width=1, alpha=0.5, label="data")
if data.shape[1] > 2:
    prediction = data[:, 2]
    ax.errorbar(k, prediction, yerr=np.sqrt(prediction), fmt="o", color="C1",
                label=r"Poisson $N\,P(k,\mu)$")
ax.set_xlabel("k")
ax.set_ylabel("entries")
ax.legend()

output = filename.rsplit(".", 1)[0] + ".png"
fig.savefig(output, dpi=150)
print("saved", output)
