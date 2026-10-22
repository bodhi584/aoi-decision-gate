"""Replay the production line day by day and compare update policies of the decision gate.

Policies: the first model is kept (static), retrained weekly on all past days, retrained weekly on the last 28 days.
The replay starts after the first half of the records. Every threshold is set on past days only
(at most 1 % of defective boards released on the calibration days).
Usage: python scripts/run_replay.py [data/dataset.csv]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gate.data import load  # noqa: E402
from gate.replay import replay, summary  # noqa: E402

POLICIES = {
    "static": dict(retrain_every=None),
    "weekly_all_past": dict(retrain_every=7),
    "weekly_last_28_days": dict(retrain_every=7, window=28),
}


def main(path="data/dataset.csv"):
    df = load(path)
    start = int(df["day"].quantile(0.5)) + 1
    Path("results").mkdir(exist_ok=True)
    res = {"start_day": start}
    for name, kw in POLICIES.items():
        r = replay(df, start, **kw)
        r.to_csv(f"results/replay_{name}.csv", index=False)
        res[name] = summary(r)
        print(name, res[name], flush=True)
    Path("results/replay.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:])
