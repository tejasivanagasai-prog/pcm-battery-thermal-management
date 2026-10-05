"""Plot the end-of-run comparison of the four battery arrangements.

Reads data/results_summary.csv and writes figures/summary_metrics.png.

Usage:
    python scripts/plot_summary.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "results_summary.csv"
OUT = ROOT / "figures" / "summary_metrics.png"

# PCM melting window from the material definition (solidus / liquidus)
SOLIDUS_K, LIQUIDUS_K = 311.0, 316.0


def main() -> None:
    df = pd.read_csv(DATA)
    labels = [f"Design {d}" for d in df["design"]]
    best = df["peak_battery_temp_K"].idxmin()
    colors = ["#2a9d8f" if i == best else "#9aa5b1" for i in range(len(df))]

    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))

    ax = axes[0]
    ax.bar(labels, df["peak_battery_temp_K"], color=colors)
    ax.axhspan(SOLIDUS_K, LIQUIDUS_K, color="#f4a261", alpha=0.15,
               label="PCM melting range")
    ax.set_ylim(312.5, 316.5)
    ax.set_ylabel("Peak cell temperature [K]")
    ax.set_title("Peak temperature (lower is better)")
    ax.legend(loc="upper left", fontsize=8)

    ax = axes[1]
    ax.bar(labels, df["battery_temp_spread_K"], color=colors)
    ax.set_ylabel("Max - min cell temperature [K]")
    ax.set_title("Non-uniformity (lower is better)")

    ax = axes[2]
    ax.bar(labels, df["mean_liquid_fraction"], color=colors)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Mean PCM liquid fraction [-]")
    ax.set_title("PCM melted (lower = more reserve)")

    for ax, fmt in zip(axes, ["{:.1f}", "{:.1f}", "{:.3f}"]):
        ax.grid(axis="y", alpha=0.3)
        ax.set_axisbelow(True)
        for patch in ax.patches:
            h = patch.get_height()
            ax.annotate(fmt.format(h),
                        (patch.get_x() + patch.get_width() / 2, h),
                        ha="center", va="bottom", fontsize=8)

    fig.suptitle("Four arrangements of 12 Li-ion cells in PCM, t = 1800 s", fontsize=12)
    fig.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=150, facecolor="white")
    print(f"Saved {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
