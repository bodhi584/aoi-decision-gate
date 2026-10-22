"""Load the Siemens AOI data set (Pfab et al. 2024) and prepare it for the decision gate.

Each row is one solder joint that the AOI machine flagged as defective. The label `class` comes from
the manual inspection station: 0 = false call (the joint is fine), 1 = true defect.
Rows with the same timestamp belong to the same printed circuit board (Pfab et al. 2024, Sec. 2).
"""
from pathlib import Path

import pandas as pd

CATEGORICAL = ["inspection_type", "meta_feat1", "meta_feat2", "meta_feat3", "meta_feat4"]


def load(path: str | Path) -> pd.DataFrame:
    """Read the CSV, add `board` (id per timestamp) and `day` (days since the first record), sort by time."""
    df = pd.read_csv(path)
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    df["ts"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("ts", kind="stable").reset_index(drop=True)
    df["board"] = df["ts"].factorize()[0]
    df["day"] = (df["ts"] - df["ts"].min()).dt.days
    return df


def feature_columns(df: pd.DataFrame) -> list[str]:
    """Categorical columns first, then the inspection measurements."""
    return CATEGORICAL + [c for c in df.columns if c.startswith("inspection_feat")]


def boards(df: pd.DataFrame) -> pd.DataFrame:
    """One row per board: defective if any of its flagged joints is a true defect."""
    return df.groupby("board").agg(day=("day", "first"), defective=("class", "max"), joints=("class", "size"))
