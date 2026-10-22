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


def system_figure():
    """Input -> System -> Output of the project."""
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
    fig, ax = plt.subplots(figsize=(11, 3.2))
    ax.set_xlim(0, 11); ax.set_ylim(0, 3.2); ax.axis("off")
    def box(x, y, w, h, fc, head, body, hc="#1F3A5F"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec="none"))
        ax.text(x + 0.15, y + h - 0.3, head, fontsize=11, fontweight="bold", color=hc, va="top")
        ax.text(x + 0.15, y + h - 0.75, body, fontsize=9, color="#14213D", va="top", linespacing=1.5)
    def arr(x1, y1, x2, y2, c=BLUE):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, color=c, lw=1.8))
    ax.text(0.1, 3.05, "INPUT", fontsize=9, color=BLUE, fontweight="bold")
    box(0.1, 0.4, 3.0, 2.5, "#E9EDF3", "AOI alarm", "AOI machine flags a solder joint\n(camera + fixed limits)\n\nabout 70 AOI measurements,\ncomponent type, error code")
    arr(3.15, 1.65, 3.75, 1.65)
    ax.text(3.8, 3.05, "SYSTEM (OURS)", fontsize=9, color=BLUE, fontweight="bold")
    box(3.8, 0.4, 3.4, 2.5, "#DCE7F5", "Binary classification", "supervised machine learning,\ntrained on past manual-inspection\nresults\n\nlogistic regression · random forest ·\nneural network (scikit-learn)")
    arr(7.25, 1.9, 7.85, 2.3, "#1D6B3A"); arr(7.25, 1.4, 7.85, 1.0, "#A12A2A")
    ax.text(7.9, 3.05, "OUTPUT: is the AOI alarm real?", fontsize=9, color=BLUE, fontweight="bold")
    box(7.9, 1.75, 3.0, 1.15, "#E3F2E8", "False call", "→ skip manual inspection", "#1D6B3A")
    box(7.9, 0.4, 3.0, 1.15, "#FBE5E5", "True defect", "→ manual inspection, repair", "#A12A2A")
    ax.text(0.1, 0.05, "Today every AOI alarm goes to manual inspection; in the Siemens data about 98 % of the flagged boards are false calls.",
            fontsize=9, color="#555F6D")
    fig.tight_layout()
    fig.savefig("docs/img/system.png", dpi=200)


def main():
    system_figure()
    base = json.loads(Path("results/baseline.json").read_text())
    rep = json.loads(Path("results/replay.json").read_text())
    models = list(NAMES)
    Path("docs/img").mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 3.6))
    k = "released_false_calls_pct_at_99pct_caught"
    bars(ax, [NAMES[m] for m in models], [[base[m]["random_split"][k] for m in models],
                                         [base[m]["time_split"][k] for m in models]],
         [GREY, BLUE], ["Random split (as often in papers)", "Time order (as on the real line)"])
    ax.set_ylabel("False calls correctly identified (%)\nwhile 99 % of defects are caught", fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Baseline: the same models look much better with a random split", fontsize=10)
    fig.tight_layout()
    fig.savefig("docs/img/baseline.png", dpi=200)

    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    pol = [("train_once", "Train once", GREY), ("retrain_weekly", "Retrain every week", BLUE)]
    bars(axs[0], [NAMES[m] for m in models], [[rep[m][p]["false_calls_released_pct"] for m in models] for p, _, _ in pol],
         [c for _, _, c in pol], [l for _, l, _ in pol])
    axs[0].set_title("False calls correctly identified\n(manual inspections saved, higher is better)", fontsize=10)
    axs[0].set_ylabel("%")
    axs[0].legend(frameon=False, fontsize=8)
    bars(axs[1], [NAMES[m] for m in models], [[rep[m][p]["defects_released_pct"] for m in models] for p, _, _ in pol],
         [c for _, _, c in pol], [l for _, l, _ in pol], fmt="{:.2f} %")
    axs[1].axhline(1, color=RED, ls="--", lw=1)
    axs[1].text(-0.45, 1.06, "target ≤ 1 %", color=RED, fontsize=8, ha="left", va="bottom")
    axs[1].set_title("Defective boards missed\n(lower is better)", fontsize=10)
    axs[1].set_ylabel("%")
    fig.suptitle(f"Day-by-day simulation of the line: {rep['logistic_regression']['train_once']['days']} production days, "
                 f"{rep['logistic_regression']['train_once']['boards']:,} flagged boards", fontsize=10)
    fig.tight_layout()
    fig.savefig("docs/img/results.png", dpi=200)


if __name__ == "__main__":
    main()
