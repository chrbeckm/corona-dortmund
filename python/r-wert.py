import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt(
    "build/FB53-Coronafallzahlen-R-Wert.csv",
    delimiter=";",
    names=True,
    encoding="utf-8-sig",
    dtype=None,
    missing_values="NA",
)

spalten = data.dtype.names

fig, ax = plt.subplots(constrained_layout=True)
plt.title("R-Wert vs 7-Tage Inzidenz")

ax.plot(data[spalten[0]], data[spalten[1]], label="R-Wert", color="blue", linewidth=1)
ax.set_ylabel("R-Wert", color="blue")
ax.set_ylim(0, np.max(data[spalten[1]]) * 1.05)

ax2 = ax.twinx()
ax2.plot(
    data[spalten[0]],
    data[spalten[2]],
    "-",
    label="7-Tage Inzidenz",
    color="red",
    linewidth=1,
)
ax2.set_ylabel("7-Tage Inzidenz", color="red")
ax2.set_ylim(0, np.max(data[spalten[2]][4:]) * 1.05)

ax.set_xlim(-1, data[spalten[0]].size)
ax.set_xticks(data[spalten[0]][::-14][::-1])
ax.set_xticklabels(data[spalten[0]][::-14][::-1], rotation=90)

plt.savefig("build/r-wert.pdf")
