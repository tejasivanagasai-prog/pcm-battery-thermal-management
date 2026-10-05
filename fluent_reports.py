"""Read ANSYS Fluent report-definition output files (*.out) and plot time histories.

A Fluent report file looks like this:

    "battery-temp-rfile"
    "Time Step" "battery-temp" "flow-time"
    ("Time Step" "battery-temp" "flow-time")
    1 300.84 60
    2 301.63 120
    ...

Usage:
    python scripts/fluent_reports.py data/fluent_reports/*.out \
        --out figures/time_histories_raw.png
"""
from __future__ import annotations

import argparse
import re
import shlex
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def read_report(path: str | Path) -> pd.DataFrame:
    """Parse one Fluent .out report file into a DataFrame (one column per quantity)."""
    columns: list[str] | None = None
    rows: list[list[float]] = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("("):  # header in parentheses: ("Time Step" "a" "b")
            columns = shlex.split(line.strip("()"))
            continue
        if line.startswith('"'):  # file title or plain header line
            if columns is None and len(shlex.split(line)) > 1:
                columns = shlex.split(line)
            continue
        if re.match(r"^[-+0-9.]", line):
            rows.append([float(v) for v in line.split()])
    if columns is None or not rows:
        raise ValueError(f"No header or data found in {path}")
    return pd.DataFrame(rows, columns=columns[: len(rows[0])])


def plot_reports(paths: list[str], x: str, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    for p in paths:
        df = read_report(p)
        if x not in df.columns:
            raise KeyError(f"{p}: column '{x}' not found, available: {list(df.columns)}")
        ys = [c for c in df.columns if c not in (x, "Time Step")]
        for y in ys:
            ax.plot(df[x], df[y], marker="o", ms=3, label=f"{Path(p).stem}: {y}")
    ax.set_xlabel(x)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, facecolor="white")
    print(f"Saved {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", help="Fluent .out report files")
    parser.add_argument("--x", default="flow-time", help="column for the x-axis")
    parser.add_argument("--out", type=Path, default=Path("figures/time_histories_raw.png"))
    args = parser.parse_args()
    plot_reports(args.files, args.x, args.out)


if __name__ == "__main__":
    main()
