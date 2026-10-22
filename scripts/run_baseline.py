"""Baseline: how well can each classifier (logistic regression, random forest, neural network) separate false calls from true defects, and how much does the split matter?

Train on the first 70 % of the records (time order) and test on the rest, versus a random 70/30 split of boards.
Reports joint-level AUROC and, on the test boards, the share of false-call boards that could be released
while still sending 100 / 99 / 95 % of the defective boards to manual inspection. These operating points are read
from the test set itself, so they are an upper bound; the replay simulation (run_replay.py) sets thresholds on past data only.
Usage: python scripts/run_baseline.py [data/dataset.csv]
"""
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aoi_classification.data import load  # noqa: E402
from aoi_classification.model import MODELS, board_scores, make_classifier, threshold_for, to_X  # noqa: E402


def evaluate(train, test, model):
    clf = make_classifier(model).fit(to_X(train), train["class"])
    p = clf.predict_proba(to_X(test))[:, 1]
    b = board_scores(test, p)
    out = {"joint_auroc": round(roc_auc_score(test["class"], p), 3), "test_boards": len(b),
           "test_defective_boards": int(b.defective.sum())}
    for keep in (1.0, 0.99, 0.95):
        thr = threshold_for(b.score.values, b.defective.values, 1 - keep)
        out[f"released_false_calls_pct_at_{int(keep * 100)}pct_caught"] = round(
            100 * ((b.defective == 0) & (b.score < thr)).sum() / (b.defective == 0).sum(), 1)
    return out


def main(path="data/dataset.csv"):
    df = load(path)
    cut = df["day"].quantile(0.7)
    ub = df["board"].unique()
    tb = set(np.random.RandomState(0).choice(ub, int(0.7 * len(ub)), replace=False))
    m = df["board"].isin(tb)
    res = {}
    for model in MODELS:
        res[model] = {"time_split": evaluate(df[df.day <= cut], df[df.day > cut], model),
                      "random_split": evaluate(df[m], df[~m], model)}
        print(model, json.dumps(res[model]), flush=True)
    Path("results").mkdir(exist_ok=True)
    Path("results/baseline.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:])
