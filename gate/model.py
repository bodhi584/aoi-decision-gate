"""The decision gate: a classifier on AOI measurements plus a release threshold.

A board is released (skips manual inspection) only if every flagged joint on it scores below the threshold.
The threshold is chosen on past data so that at most `max_miss` of the defective boards would have been released.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from .data import CATEGORICAL, feature_columns


def make_classifier(seed: int = 0) -> HistGradientBoostingClassifier:
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.05, class_weight="balanced", random_state=seed,
        categorical_features="from_dtype",
    )


def to_X(df: pd.DataFrame) -> pd.DataFrame:
    X = df[feature_columns(df)].copy()
    for c in CATEGORICAL:
        X[c] = X[c].astype("category")
    return X


def board_scores(df: pd.DataFrame, joint_scores: np.ndarray) -> pd.DataFrame:
    """Board score = highest joint score on that board."""
    s = pd.DataFrame({"board": df["board"].values, "score": joint_scores, "y": df["class"].values})
    return s.groupby("board").agg(score=("score", "max"), defective=("y", "max"))


def threshold_for(scores: np.ndarray, defective: np.ndarray, max_miss: float) -> float:
    """Largest threshold that releases at most `max_miss` of the defective boards (release if score < threshold)."""
    d = np.sort(scores[defective == 1])
    if len(d) == 0:
        return 0.0
    k = int(np.floor(max_miss * len(d)))  # number of defective boards we may release
    return float(d[k])


@dataclass
class Gate:
    max_miss: float = 0.01
    calib_days: int = 14
    seed: int = 0

    def fit(self, df: pd.DataFrame) -> "Gate":
        """Train on all but the last `calib_days` days and set the threshold on those held-back days.

        The threshold is only valid for the model it was set on, so that model is the one used for decisions.
        """
        last = df["day"].max()
        fit_part, cal_part = df[df["day"] <= last - self.calib_days], df[df["day"] > last - self.calib_days]
        if cal_part["class"].sum() == 0 or fit_part["class"].sum() == 0:
            raise ValueError("training window needs true defects both before and inside the calibration days")
        self.clf = make_classifier(self.seed).fit(to_X(fit_part), fit_part["class"])
        b = board_scores(cal_part, self.clf.predict_proba(to_X(cal_part))[:, 1])
        self.threshold = threshold_for(b["score"].values, b["defective"].values, self.max_miss)
        return self

    def decide(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return one row per board with `release` (True = skip manual inspection)."""
        b = board_scores(df, self.clf.predict_proba(to_X(df))[:, 1])
        b["release"] = b["score"] < self.threshold
        return b
