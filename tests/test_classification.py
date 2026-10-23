"""Unit tests on a small synthetic data set (the real data are not stored in the repository)."""
import numpy as np
import pandas as pd
import pytest

from aoi_classification import FalseCallClassifier, simulate, summary, threshold_for
from aoi_classification.data import CATEGORICAL, boards


def synthetic(days=40, boards_per_day=30, seed=0):
    rng = np.random.default_rng(seed)
    rows, t0 = [], pd.Timestamp("2026-01-01", tz="UTC")
    for d in range(days):
        for b in range(boards_per_day):
            ts = t0 + pd.Timedelta(days=d, minutes=b)
            bad = rng.random() < 0.1
            for j in range(rng.integers(1, 4)):
                y = int(bad and j == 0)
                rows.append({"timestamp": str(ts), "class": y, "inspection_type": int(rng.integers(0, 2)),
                             "meta_feat1": 0, "meta_feat2": 1, "meta_feat3": 0, "meta_feat4": 3,
                             "inspection_feat1": rng.normal(5.0 if y else 0.0), "inspection_feat2": rng.normal()})
    df = pd.DataFrame(rows)
    df["ts"] = pd.to_datetime(df.timestamp)
    df["board"] = df["ts"].factorize()[0]
    df["day"] = (df.ts - df.ts.min()).dt.days
    return df


def test_board_is_defective_if_any_joint_is():
    df = synthetic(days=2)
    b = boards(df)
    expected = df.groupby("board")["class"].max()
    assert (b.defective == expected).all()


def test_threshold_releases_at_most_the_allowed_defects():
    scores = np.array([0.1, 0.2, 0.3, 0.9, 0.95, 0.99])
    defective = np.array([0, 0, 0, 1, 1, 1])
    thr = threshold_for(scores, defective, max_miss=0.0)
    assert ((scores < thr) & (defective == 1)).sum() == 0
    assert ((scores < thr) & (defective == 0)).sum() == 3


def test_classifier_finds_some_false_calls_and_keeps_defects():
    df = synthetic()
    clf = FalseCallClassifier(max_miss=0.0, calib_days=7).fit(df[df.day < 30])
    b = clf.classify(df[df.day >= 30])
    assert b.predicted_false_call[b.defective == 0].mean() > 0.3
    assert b.predicted_false_call[b.defective == 1].mean() < 0.2


def test_simulation_uses_only_past_days():
    df = synthetic()
    r = simulate(df, start_day=25, retrain_every=5, calib_days=7)
    assert (r.trained_on_day <= r.day).all()
    assert r.day.min() == 25
    s = summary(r)
    assert s["boards"] == r.boards.sum()


def test_classifier_needs_defects_in_both_parts():
    df = synthetic()
    df["class"] = 0
    with pytest.raises(ValueError):
        FalseCallClassifier().fit(df)


def test_categorical_columns_exist():
    df = synthetic(days=1)
    assert all(c in df for c in CATEGORICAL)


@pytest.mark.parametrize("model", ["logistic_regression", "random_forest", "neural_network"])
def test_each_model_trains_and_decides(model):
    df = synthetic()
    b = FalseCallClassifier(model=model, max_miss=0.0, calib_days=7).fit(df[df.day < 30]).classify(df[df.day >= 30])
    assert set(b.columns) >= {"score", "defective", "predicted_false_call"}
    assert b.predicted_false_call[b.defective == 0].mean() > 0.1


def test_summary_kpis():
    r = pd.DataFrame({"day": [1, 2], "boards": [10, 10], "false_call_boards": [9, 8], "defective_boards": [1, 2],
                      "false_calls_identified": [3, 2], "missed_defects": [0, 1], "threshold": [0.1, 0.1],
                      "trained_on_day": [0, 0]})
    s = summary(r)
    assert s["recall_pct"] == round(100 * 2 / 3, 2)      # 3 true defects, 1 missed
    assert s["specificity_pct"] == round(100 * 5 / 17, 1)  # 17 false calls, 5 identified
    assert s["manual_inspections_saved"] == 5
