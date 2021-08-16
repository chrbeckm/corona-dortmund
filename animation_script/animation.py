import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

data = np.genfromtxt(
    "build/FB53-Coronafallzahlen.csv",
    delimiter=";",
    names=True,
    encoding="utf-8-sig",
    dtype=None,
    missing_values="-",
)

inzidenz = (
    np.convolve(data["Zuwachs_positiver_Testergebnisse_zum_Vortag"], np.ones(7))[:-6]
    / 5.8825
)

x = np.arange(len(inzidenz))
forerun = 43

fig, ax = plt.subplots(constrained_layout=True, figsize=(4.5, 8))

ln1 = ax.bar(x, data["aktuell_erkrankte_Personen"], label="Aktive Fälle")
ln2 = ax.bar(
    x,
    data["Zuwachs_positiver_Testergebnisse_zum_Vortag"],
    color="red",
    label="pos. Fälle",
)
ax.set_ylabel("Aktive Fälle / pos. Fälle")
ax.set_ylim(0, np.max(data["aktuell_erkrankte_Personen"]) * 1.01)

ax2 = ax.twinx()

ax.set_xticks(x[::-7][::-1])
ax.set_xticklabels(data["Datum"][::-7][::-1], rotation=45, ha="right")

ln3 = ax2.plot(x, inzidenz, ".", color="orange", label="7-Tage Inzidenz")
ax2.set_ylabel("7-Tage Inzidenz")
ax2.set_ylim(0, np.max(inzidenz) * 1.01)

fig.legend(loc=(0.03, 0.94), framealpha=1, ncol=3, handletextpad=0.3)
ax.set_title("Covid-19 Zahlen aus Dortmund\n\n")
ax2.grid()


def init():
    ax.set_xlim(0, forerun)
    return ln1


def animate(i):
    ax.set_xlim(i, i + forerun)
    return ln1


anim = FuncAnimation(fig, animate, init_func=init, frames=x[:-forerun])

anim.save("build/animation/dortmund_animation.mp4", writer=PillowWriter(fps=10))
