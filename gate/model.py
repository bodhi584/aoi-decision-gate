"""The decision gate: a classifier on AOI measurements plus a release threshold.

A board is released (skips manual inspection) only if every flagged joint on it scores below the threshold.
The threshold is chosen on past data so that at most `max_miss` of the defective boards would have been released.

Three standard classifiers from scikit-learn, as in the lecture and its example project:
- logistic regression: the simple baseline
- random forest: many decision trees that vote
- neural network: a small multilayer perceptron with one hidden layer (lecture p. 12, 17)
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from .data import CATEGORICAL, feature_columns

MODELS = ["logistic_regression", "random_forest", "neural_network"]
DEFAULT_MODEL = "random_forest"


def _prep(scale: bool) -> ColumnTransformer:
    """Categories as numbers (trees) or one-hot columns (regression, network); measurements scaled if needed."""
    cat = (OneHotEncoder(handle_unknown="ignore") if scale
           else OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))
    num = StandardScaler() if scale else "passthrough"
    return ColumnTransformer([("cat", cat, CATEGORICAL),
                              ("num", num, lambda X: [c for c in X.columns if c not in CATEGORICAL])])


def make_classifier(name: str = DEFAULT_MODEL, seed: int = 0):
    if name == "logistic_regression":
        return make_pipeline(_prep(True), LogisticRegression(max_iter=1000, class_weight="balanced"))
    if name == "random_forest":
        return make_pipeline(_prep(False), RandomForestClassifier(
            n_estimators=100, min_samples_leaf=5, class_weight="balanced_subsample", n_jobs=-1, random_state=seed))
    if name == "neural_network":
        return make_pipeline(_prep(True), MLPClassifier(
            hidden_layer_sizes=(10,), early_stopping=True, max_iter=200, random_state=seed))
    raise ValueError(f"unknown model {name!r}; choose from {MODELS}")


def to_X(df: pd.DataFrame) -> pd.DataFrame:
    X = df[feature_columns(df)].copy()
    for c in CATEGORICAL:
        X[c] = X[c].astype(str)
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
    model: str = DEFAULT_MODEL

    def fit(self, df: pd.DataFrame) -> "Gate":
        """Train on all but the last `calib_days` days and set the threshold on those held-back days.

        The threshold is only valid for the model it was set on, so that model is the one used for decisions.
        """
        last = df["day"].max()
        fit_part, cal_part = df[df["day"] <= last - self.calib_days], df[df["day"] > last - self.calib_days]
        if cal_part["class"].sum() == 0 or fit_part["class"].sum() == 0:
            raise ValueError("training window needs true defects both before and inside the calibration days")
        self.clf = make_classifier(self.model, self.seed).fit(to_X(fit_part), fit_part["class"])
        b = board_scores(cal_part, self.clf.predict_proba(to_X(cal_part))[:, 1])
        self.threshold = threshold_for(b["score"].values, b["defective"].values, self.max_miss)
        return self

    def decide(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return one row per board with `release` (True = skip manual inspection)."""
        b = board_scores(df, self.clf.predict_proba(to_X(df))[:, 1])
        b["release"] = b["score"] < self.threshold
        return b
