import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt(
    "build/FB53-Coronafallzahlen-Altersinzidenzen.csv",
    delimiter=";",
    names=True,
    encoding="utf-8-sig",
    dtype=None,
)

spalten = data.dtype.names

plt.figure(constrained_layout=True)
plt.title("Inzidenz nach Altersgruppen")

for i in range(7):
    mask = data[spalten[0]] == data[spalten[0]][i]
    plt.plot(
        data[spalten[1]][mask],
        data[spalten[-1]][mask],
        "-",
        label=data[spalten[0]][i],
        linewidth=0.5,
    )

plt.legend()
plt.xticks(
    data[spalten[1]][mask][::-4][::-1], data[spalten[1]][mask][::-4][::-1], rotation=90
)
plt.xlim(-1, data[spalten[1]][mask].size)
plt.ylim(0, np.max(data[spalten[-1]]) * 1.01)

plt.xlabel("Kalenderwoche")
plt.ylabel("7-Tage Inzidenz")

plt.savefig("build/altersinzidenz.pdf")
