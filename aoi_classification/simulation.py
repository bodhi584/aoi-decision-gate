"""Day-by-day simulation of the production line on the recorded days (walk-forward evaluation).

The recorded days are played back in time order. On each day every flagged board is classified by a model trained
only on earlier days, as it would be in operation. The classifier is retrained every `retrain_every` days
(None = never: the model from the first training window is kept).

Positive class = true defect. Per day we count how many false calls were correctly classified as false call
(these boards would skip manual inspection) and how many true defects were missed (classified as false call).
"""
import pandas as pd

from .model import FalseCallClassifier


def simulate(df: pd.DataFrame, start_day: int, retrain_every: int | None = 7, window: int | None = None,
             max_miss: float = 0.01, calib_days: int = 14, seed: int = 0,
             model: str = "random_forest") -> pd.DataFrame:
    """Simulate the days from `start_day` on; return one row per simulated day.

    window: train only on the last `window` days (None = all past days).
    max_miss: share of true defects that may be classified as false call on the calibration days (0.01 = recall 99 %).
    """
    rows, clf, trained_on = [], None, None
    for day in sorted(d for d in df["day"].unique() if d >= start_day):
        if clf is None or (retrain_every is not None and day - trained_on >= retrain_every):
            past = df[df["day"] < day]
            if window is not None:
                past = past[past["day"] >= day - window]
            try:
                clf = FalseCallClassifier(max_miss=max_miss, calib_days=calib_days, seed=seed, model=model).fit(past)
                trained_on = day
            except ValueError:
                if clf is None:
                    raise
                trained_on = day  # too few true defects in the window: keep the current classifier until the next update
        b = clf.classify(df[df["day"] == day])
        rows.append({
            "day": day,
            "boards": len(b),
            "false_call_boards": int((b.defective == 0).sum()),
            "defective_boards": int(b.defective.sum()),
            "false_calls_identified": int(((b.defective == 0) & b.predicted_false_call).sum()),
            "missed_defects": int(((b.defective == 1) & b.predicted_false_call).sum()),
            "threshold": clf.threshold,
            "trained_on_day": trained_on,
        })
    return pd.DataFrame(rows)


def summary(r: pd.DataFrame) -> dict:
    """KPIs over all simulated days (positive class = true defect)."""
    fc, dfct = int(r.false_call_boards.sum()), int(r.defective_boards.sum())
    ident, missed = int(r.false_calls_identified.sum()), int(r.missed_defects.sum())
    return {
        "days": len(r),
        "boards": int(r.boards.sum()),
        "false_call_boards": fc,
        "defective_boards": dfct,
        "recall_pct": round(100 * (dfct - missed) / dfct, 2) if dfct else None,
        "specificity_pct": round(100 * ident / fc, 1) if fc else None,
        "missed_defects": missed,
        "manual_inspections_saved": ident,
    }
