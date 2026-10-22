"""Replay simulation of the production line.

The recorded days are played back in time order. On each day the gate decides every flagged board using only a
model trained on earlier days, exactly as it would on the real line. The gate is retrained every `retrain_every`
days (None = never, i.e. the model from the first training window is kept).
"""
import pandas as pd

from .model import Gate


def replay(df: pd.DataFrame, start_day: int, retrain_every: int | None = 7, window: int | None = None,
           max_miss: float = 0.01, calib_days: int = 14, seed: int = 0) -> pd.DataFrame:
    """Return one row per replayed day with released / inspected board counts.

    window: train only on the last `window` days (None = all past days).
    """
    rows, gate, trained_on = [], None, None
    for day in sorted(d for d in df["day"].unique() if d >= start_day):
        if gate is None or (retrain_every is not None and day - trained_on >= retrain_every):
            past = df[df["day"] < day]
            if window is not None:
                past = past[past["day"] >= day - window]
            try:
                gate, trained_on = Gate(max_miss=max_miss, calib_days=calib_days, seed=seed).fit(past), day
            except ValueError:
                if gate is None:
                    raise
                trained_on = day  # too few defects in the window: keep the current gate until the next update
        b = gate.decide(df[df["day"] == day])
        rows.append({
            "day": day,
            "boards": len(b),
            "false_call_boards": int((b.defective == 0).sum()),
            "defective_boards": int(b.defective.sum()),
            "released_false_calls": int(((b.defective == 0) & b.release).sum()),
            "released_defects": int(((b.defective == 1) & b.release).sum()),
            "threshold": gate.threshold,
            "trained_on_day": trained_on,
        })
    return pd.DataFrame(rows)


def summary(r: pd.DataFrame) -> dict:
    fc, dfct = r.false_call_boards.sum(), r.defective_boards.sum()
    return {
        "days": len(r),
        "boards": int(r.boards.sum()),
        "false_call_boards": int(fc),
        "defective_boards": int(dfct),
        "false_calls_released_pct": round(100 * r.released_false_calls.sum() / fc, 1),
        "defects_released": int(r.released_defects.sum()),
        "defects_released_pct": round(100 * r.released_defects.sum() / dfct, 2) if dfct else 0.0,
        "manual_inspections_saved": int(r.released_false_calls.sum()),
    }
