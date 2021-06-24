import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt(
    "build/FB53-Coronafallzahlen-Virusvarianten.csv",
    delimiter=";",
    names=True,
    encoding="utf-8-sig",
    dtype=None,
)

spalten = data.dtype.names
colors = ["blue", "orange", "green", "red", "purple"]

fig, ax = plt.subplots(constrained_layout=True)
plt.title("Virusvarianten")

minimal = np.zeros(data[spalten[1]][data[spalten[0]] == data[spalten[0]][0]].size)
for i in range(0, 2):
    mask = data[spalten[0]] == data[spalten[0]][i]
    ax.bar(
        data[spalten[1]][mask],
        data[spalten[-1]][mask],
        color=colors[i],
        label=data[spalten[0]][i],
        bottom=minimal,
        width=.9,
        alpha=1
    )
    minimal += data[spalten[-1]][mask]
ax.legend(loc="upper left")
ax.set_ylim(0, np.max(minimal) * 1.05)

ax2 = ax.twinx()
minimal = np.zeros(data[spalten[1]][data[spalten[0]] == data[spalten[0]][2]].size)
for i in range(2, 5):
    mask = data[spalten[0]] == data[spalten[0]][i]
    ax2.bar(
        data[spalten[1]][mask],
        data[spalten[-1]][mask],
        color=colors[i],
        label=data[spalten[0]][i],
        bottom=minimal,
        width=.5,
        alpha=1
    )
    minimal += data[spalten[-1]][mask]
ax2.legend(loc="center left")
ax2.set_ylim(0, np.max(minimal) * 1.05)
ax2.set_ylabel(r"$\beta$" + "\n" + r"$\gamma$" + "\n" + r"$\delta$", rotation=0)

ax.set_xlabel("Kalenderwoche")
ax.set_xlim(0, data[spalten[1]][mask].size)
ax.set_xticks(data[spalten[1]][mask][::-2][::-1])
ax.set_xticklabels(data[spalten[1]][mask][::-2][::-1], rotation=90)

plt.savefig("build/virusvarianten.pdf")
