import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt(
    "build/FB53-Coronafallzahlen-Stadtbezirke.csv",
    delimiter=";",
    names=True,
    encoding="cp1252",#utf-8-sig",
    dtype=None,
    missing_values="-",
)

maximal = 0
maxdiff = 0
daten = dict()
for name in data.dtype.names:
    if name == data.dtype.names[1]:
        None
    elif name == data.dtype.names[0]:
        daten[name] = data[name][data["Bezeichnung"] == "Positivfälle"]
    else:
        daten[name + "-Positiv"] = np.array(
            data[name][data["Bezeichnung"] == "Positivfälle"]
        )
        daten[name + "-PositivPro.1M"] = np.array(
            data[name][
                data["Bezeichnung"]
                == "Positivfälle pro 100.000 Einwohner*innen im jeweiligen Stadtbezirk"
            ]
        )
        if maximal < np.max(daten[name + "-PositivPro.1M"]):
            maximal = np.max(daten[name + "-PositivPro.1M"])
        if maxdiff < np.max(np.diff(daten[name + "-PositivPro.1M"])):
            maxdiff = np.max(np.diff(daten[name + "-PositivPro.1M"]))

daten["Gesamt-Positiv"][0:3] *= 1000
print("last date Bezirke:\t", daten[data.dtype.names[0]][-1])

factor = 2
plt.figure(constrained_layout=True, figsize=(9 / factor, 16 / factor))
plt.text(
    len(daten[data.dtype.names[0]]),
    0.8 * maximal,
    s="Kumulative\npositive Fälle\npro 100k in den\nDortmunder\nStadtbezirken",
)
for name in daten.keys():
    if name.split("-")[-1] == "PositivPro.1M" and name.split("-")[0] != "Ohne_Angaben":
        if name.split("-")[0] in ["Huckarde", "Mengede", "Gesamt"]:
            plt.plot(daten[name], "--", label=name.split("-")[0], linewidth=2)
        else:
            plt.plot(daten[name], label=name.split("-")[0], linewidth=1)
plt.xticks(np.arange(len(daten[name])), daten[data.dtype.names[0]], rotation=90)
plt.legend(loc=(1.01, 0))
plt.xlim(-0.1, len(daten[data.dtype.names[0]]) - 0.9)
plt.ylim(0, 1.01 * maximal)
plt.grid()
plt.savefig("build/bezirke_insta.pdf")

plt.figure(constrained_layout=True)
plt.title("Kumulative positive Fälle pro 100k in den Dortmunder Stadtbezirken")
for name in daten.keys():
    if name.split("-")[-1] == "PositivPro.1M" and name.split("-")[0] != "Ohne_Angaben":
        if name.split("-")[0] in ["Huckarde", "Mengede", "Gesamt"]:
            plt.plot(daten[name], "--", label=name.split("-")[0], linewidth=2)
        else:
            plt.plot(daten[name], label=name.split("-")[0], linewidth=1)
plt.xticks(np.arange(len(daten[name])), daten[data.dtype.names[0]], rotation=45)
plt.legend(loc=(1.01, 0))
plt.xlim(-0.1, len(daten[data.dtype.names[0]]) - 0.9)
plt.ylim(0, 1.01 * maximal)
plt.grid()
plt.savefig("build/bezirke.pdf")


plt.figure(constrained_layout=True, figsize=(9 / factor, 16 / factor))
plt.text(
    len(daten[data.dtype.names[0]]) - 0.5,
    0.8 * maxdiff,
    s="Differenz\nder kumulativen\npositiven Fälle\npro 100k in den\nDortmunder\nStadtbezirken\nzum Vormonat",
)
for name in daten.keys():
    if name.split("-")[-1] == "PositivPro.1M" and name.split("-")[0] != "Ohne_Angaben":
        if name.split("-")[0] in ["Huckarde", "Mengede", "Gesamt"]:
            plt.plot(np.diff(daten[name]), "--", label=name.split("-")[0], linewidth=2)
        else:
            plt.plot(np.diff(daten[name]), label=name.split("-")[0], linewidth=1)
plt.xticks(np.arange(len(daten[name][1:])), daten[data.dtype.names[0]][1:], rotation=90)
plt.legend(loc=(1.01, 0))
plt.xlim(-0.1, len(daten[data.dtype.names[0]]) - 1.9)
plt.ylim(0, 1.01 * maxdiff)
plt.grid()
plt.savefig("build/bezirke_insta_differenz.pdf")
