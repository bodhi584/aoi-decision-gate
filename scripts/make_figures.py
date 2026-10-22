"""Figures for the README and slides, made from the result files only.

Usage: python scripts/make_figures.py   (after run_baseline.py and run_replay.py)
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

NAMES = {"logistic_regression": "Logistic regression\n(baseline)", "random_forest": "Random forest",
         "neural_network": "Neural network\n(1 hidden layer)"}
GREY, BLUE, RED = "#9AA5B1", "#2F6DB5", "#C0392B"


def bars(ax, groups, series, colors, labels, fmt="{:.1f} %"):
    x = np.arange(len(groups))
    w = 0.8 / len(series)
    for i, (vals, c, lab) in enumerate(zip(series, colors, labels)):
        b = ax.bar(x + (i - (len(series) - 1) / 2) * w, vals, w, color=c, label=lab)
        ax.bar_label(b, [fmt.format(v) for v in vals], fontsize=8, padding=2)
    ax.set_xticks(x, groups, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)


def main():
    base = json.loads(Path("results/baseline.json").read_text())
    rep = json.loads(Path("results/replay.json").read_text())
    models = list(NAMES)
    Path("docs/img").mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 3.6))
    k = "released_false_calls_pct_at_99pct_caught"
    bars(ax, [NAMES[m] for m in models], [[base[m]["random_split"][k] for m in models],
                                         [base[m]["time_split"][k] for m in models]],
         [GREY, BLUE], ["Random split (as often in papers)", "Time order (as on the real line)"])
    ax.set_ylabel("False-call boards released (%)\nwhile 99 % of defects are caught", fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Baseline: the same models look much better with a random split", fontsize=10)
    fig.tight_layout()
    fig.savefig("docs/img/baseline.png", dpi=200)

    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    pol = [("train_once", "Train once", GREY), ("retrain_weekly", "Retrain every week", BLUE)]
    bars(axs[0], [NAMES[m] for m in models], [[rep[m][p]["false_calls_released_pct"] for m in models] for p, _, _ in pol],
         [c for _, _, c in pol], [l for _, l, _ in pol])
    axs[0].set_title("False-call boards released\n(manual inspections saved, higher is better)", fontsize=10)
    axs[0].set_ylabel("%")
    axs[0].legend(frameon=False, fontsize=8)
    bars(axs[1], [NAMES[m] for m in models], [[rep[m][p]["defects_released_pct"] for m in models] for p, _, _ in pol],
         [c for _, _, c in pol], [l for _, l, _ in pol], fmt="{:.2f} %")
    axs[1].axhline(1, color=RED, ls="--", lw=1)
    axs[1].text(-0.45, 1.06, "target ≤ 1 %", color=RED, fontsize=8, ha="left", va="bottom")
    axs[1].set_title("Defective boards released\n(lower is better)", fontsize=10)
    axs[1].set_ylabel("%")
    fig.suptitle(f"Day-by-day simulation of the line: {rep['logistic_regression']['train_once']['days']} production days, "
                 f"{rep['logistic_regression']['train_once']['boards']:,} flagged boards", fontsize=10)
    fig.tight_layout()
    fig.savefig("docs/img/results.png", dpi=200)


if __name__ == "__main__":
    main()
