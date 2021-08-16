import numpy as np
import matplotlib.pyplot as plt


def tickse():
    plt.xticks(data["Datum"][::-14][::-1], data["Datum"][::-14][::-1], rotation=90)


data = np.genfromtxt(
    "build/FB53-Coronafallzahlen.csv",
    delimiter=";",
    names=True,
    encoding="utf-8-sig",
    dtype=None,
    missing_values="-",
)

spalten = data.dtype.names

dortmund = 6.03609
rki = 5.88250
n_positive_tests = (
    np.convolve(data["Zuwachs_positiver_Testergebnisse_zum_Vortag"], np.ones(7))[:-6]
    / rki
)

plt.figure(constrained_layout=True)
plt.bar(
    data["Datum"],
    data["Zuwachs_positiver_Testergebnisse_zum_Vortag"],
    label="Neuinfektionen",
)

plt.plot(
    data["Datum"], n_positive_tests, "k.", markersize=3, label="7-Tage Inzidenz",
)

plt.plot([-1, data["Datum"].size], [35, 35], "-g", linewidth=0.5)
plt.plot([-1, data["Datum"].size], [50, 50], "-y", linewidth=0.5)
plt.plot([-1, data["Datum"].size], [100, 100], "-r", linewidth=0.5)

plt.title(
    "Neuinfektionen pro Tag mit 7-Tage-Inzidenz, \n Stadt Dortmund: "
    + r"$\num{588250}$ Einwohnerïnnen"
)
plt.legend(loc="upper left")
tickse()
plt.xlim(-1, data["Datum"].size)
plt.savefig("build/faelle-pro-tag.pdf")


plt.figure(constrained_layout=True)
plt.plot(
    data["Datum"], n_positive_tests, "k.", markersize=3, label="7-Tage Inzidenz",
)

plt.plot([-1, data["Datum"].size], [35, 35], "-g", linewidth=0.5)
plt.plot([-1, data["Datum"].size], [50, 50], "-y", linewidth=0.5)
plt.plot([-1, data["Datum"].size], [100, 100], "-r", linewidth=0.5)

plt.title("7-Tage-Inzidenz, \n Stadt Dortmund: " + r"$\num{588250}$ Einwohnerïnnen")
plt.legend(loc="upper left")
tickse()
plt.xlim(-1, data["Datum"].size)
plt.ylim(0, np.max(n_positive_tests) * 1.05)
plt.savefig("build/inzidenz.pdf")


plt.figure(constrained_layout=True)
plt.title("Gesamtzahl an Fällen")
plt.bar(
    data["Datum"], data["positive_Testergebnisse_insgesamt"], label="positive Tests",
)
plt.bar(data["Datum"], data["genesene_Personen_gesamt"], label="Genesene")
plt.bar(
    data["Datum"],
    50 * data["ursächlich_an_COVID19_Verstorbene"],
    label=r"Verstorbene $\cdot\:50$",
)
plt.bar(
    data["Datum"],
    50 * data["aufgrund_anderer_Ursachen_Verstorbene"],
    label=r"an anderer Ursache Verstorbene $\cdot\:50$",
)
plt.legend()
tickse()
plt.xlim(-1, data["Datum"].size)
plt.ylim(0, np.max(data["positive_Testergebnisse_insgesamt"]) * 1.05)
plt.savefig("build/insgesamt.pdf")


plt.figure(constrained_layout=True)
plt.title("Aktuelle Fälle pro Tag")
plt.bar(data["Datum"], data["aktuell_erkrankte_Personen"], label="erkrankt")
plt.bar(
    data["Datum"],
    data["darunter_aktuell_stationär_behandelte_Personen"],
    label="stationär",
)
plt.bar(
    data["Datum"],
    data["darunter_aktuell_intensivmedizinisch_behandelte_Personen"],
    label="intensiv",
)
plt.bar(
    data["Datum"], data["darunter_aktuell_beatmete_Personen"], label="beatmet",
)
plt.legend()
tickse()
plt.xlim(-1, data["Datum"].size)
plt.ylim(0, np.max(data["aktuell_erkrankte_Personen"]) * 1.05)
plt.savefig("build/aktuell.pdf")


fig, ax = plt.subplots(constrained_layout=True)
plt.title("Aktive Fälle pro Tag vs 7-Tage Inzidenz")

ax.bar(data["Datum"], data["aktuell_erkrankte_Personen"], label="aktiv")
ax.set_ylabel("Aktive Fälle")
ax.set_ylim(0, np.max(data["aktuell_erkrankte_Personen"]) * 1.05)

ax2 = ax.twinx()
ax2.plot(
    data["Datum"], n_positive_tests, "r.", label=r"7-Tage Inzidenz", markersize=1,
)
ax2.set_ylabel("7-Tage Inzidenz")
ax2.set_ylim(0, np.max(n_positive_tests) * 1.05)

ax.set_xlim(-1, data["Datum"].size)
ax.set_xticks(data["Datum"][::-14][::-1])
ax.set_xticklabels(data["Datum"][::-14][::-1], rotation=90)

plt.legend(loc="upper left")
plt.savefig("build/aktuellVSinzidenz.pdf")
