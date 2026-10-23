"""Binary classification of AOI alarms: true defect (1) or false call (0).

Steps (see docs/code_walkthrough.md):
1. Each flagged solder joint gets a score between 0 and 1 from a classifier (higher = more likely a true defect).
2. A board's score is the highest score of its flagged joints.
3. A board is classified as false call (it skips manual inspection) if its score is below the threshold.
4. The threshold is set on the last days of the training data so that at most 1 % of the true defects are missed
   (recall 99 %).

Three standard classifiers from scikit-learn (lecture p. 12, 17, 22):
- logistic regression: the simple baseline
- random forest: many decision trees that vote
- neural network: one hidden layer with 10 neurons
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

from .data import CATEGORICAL, feature_columns

# The about 70 AOI measurements are the columns inspection_feat1, inspection_feat2, ...
MEASUREMENTS = make_column_selector(pattern="^inspection_feat")

MODELS = ["logistic_regression", "random_forest", "neural_network"]
DEFAULT_MODEL = "random_forest"


def make_classifier(name=DEFAULT_MODEL, seed=0):
    """Return an untrained scikit-learn model: data preparation + classifier."""
    if name == "logistic_regression":
        # Categories become 0/1 columns, measurements are scaled to mean 0 and standard deviation 1.
        prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
                                  ("num", StandardScaler(), MEASUREMENTS)])
        clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    elif name == "random_forest":
        # Trees need no scaling; categories become numbers.
        prep = ColumnTransformer([("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
                                   CATEGORICAL),
                                  ("num", "passthrough", MEASUREMENTS)])
        clf = RandomForestClassifier(n_estimators=100, min_samples_leaf=5, class_weight="balanced_subsample",
                                     n_jobs=-1, random_state=seed)
    elif name == "neural_network":
        # Same preparation as logistic regression; one hidden layer with 10 neurons.
        prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
                                  ("num", StandardScaler(), MEASUREMENTS)])
        clf = MLPClassifier(hidden_layer_sizes=(10,), early_stopping=True, max_iter=200, random_state=seed)
    else:
        raise ValueError(f"unknown model {name}; choose from {MODELS}")
    return make_pipeline(prep, clf)


def to_X(df):
    """The input columns of the classifier; category codes are treated as text, not as numbers."""
    X = df[feature_columns(df)].copy()
    for c in CATEGORICAL:
        X[c] = X[c].astype(str)
    return X


def board_scores(df, joint_scores):
    """One row per board: score = highest joint score on the board; defective = 1 if any joint is a true defect."""
    s = pd.DataFrame({"board": df["board"].values, "score": joint_scores, "y": df["class"].values})
    return s.groupby("board").agg(score=("score", "max"), defective=("y", "max"))


def threshold_for(scores, defective, max_miss):
    """Highest threshold that misses at most `max_miss` of the true defects (false call if score < threshold)."""
    defect_scores = np.sort(scores[defective == 1])
    if len(defect_scores) == 0:
        return 0.0
    k = int(np.floor(max_miss * len(defect_scores)))  # number of true defects we may miss
    return float(defect_scores[k])


class FalseCallClassifier:
    """Classifier + threshold. Use fit() on past days, then classify() on a new day."""

    def __init__(self, max_miss=0.01, calib_days=14, seed=0, model=DEFAULT_MODEL):
        self.max_miss = max_miss      # 0.01 = at most 1 % of true defects missed (recall 99 %)
        self.calib_days = calib_days  # last days of the training data, used only to set the threshold
        self.seed = seed
        self.model = model

    def fit(self, df):
        """Train on all but the last `calib_days` days; set the threshold on those last days."""
        last = df["day"].max()
        train = df[df["day"] <= last - self.calib_days]
        calib = df[df["day"] > last - self.calib_days]
        if train["class"].sum() == 0 or calib["class"].sum() == 0:
            raise ValueError("training data need true defects both before and inside the calibration days")
        self.clf = make_classifier(self.model, self.seed).fit(to_X(train), train["class"])
        b = board_scores(calib, self.clf.predict_proba(to_X(calib))[:, 1])
        self.threshold = threshold_for(b["score"].values, b["defective"].values, self.max_miss)
        return self

    def classify(self, df):
        """One row per board: predicted_false_call = True (skip manual inspection) or False (true defect)."""
        b = board_scores(df, self.clf.predict_proba(to_X(df))[:, 1])
        b["predicted_false_call"] = b["score"] < self.threshold
        return b
