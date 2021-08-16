import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt(
    "build/FB53-Coronafallzahlen.csv",
    delimiter=";",
    names=True,
    encoding="utf-8-sig",
    dtype=None,
    missing_values="-",
)

print("last date Insta:\t", data["Datum"][-1])
forerun = -43
x = np.arange(-forerun)
inzidenz = (
    np.convolve(data["Zuwachs_positiver_Testergebnisse_zum_Vortag"], np.ones(7))[:-6]
    / 5.8825
)

factor = 2
fig, ax = plt.subplots(constrained_layout=True, figsize=(9 / factor, 16 / factor))

ln1 = ax.bar(x, data["aktuell_erkrankte_Personen"][forerun:], label="Aktive Fälle")
ln2 = ax.bar(
    x,
    data["Zuwachs_positiver_Testergebnisse_zum_Vortag"][forerun:],
    color="red",
    label="Neuinfektionen",
)
ax.set_ylabel("Aktive Fälle / Neuinfektionen")
ax.set_ylim(0, np.max(data["aktuell_erkrankte_Personen"][forerun:]) * 1.01)

ax2 = ax.twinx()

ax.set_xlim(-0.7, -forerun - 0.3)
ax.set_xticks(x[::7])
ax.set_xticklabels(data["Datum"][forerun::7], rotation=45, ha="right")

ln3 = ax2.plot(x, inzidenz[forerun:], ".", color="orange", label="7-Tage Inzidenz")
ax2.set_ylabel("7-Tage Inzidenz")
ax2.set_ylim(0, np.max(inzidenz[forerun:]) * 1.01)

fig.legend(loc=(0.03, 0.93), framealpha=1, ncol=3, handletextpad=0.3)
ax.set_title("Covid-19 Zahlen aus Dortmund\n\n")
ax2.grid()

fig.savefig("build/insta_story.png", dpi=500)
