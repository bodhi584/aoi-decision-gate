"""Day-by-day simulation of the line: three models, two update policies.

Models: logistic regression (baseline), random forest, neural network. Policies: train once, or retrain every week
on all past days. The simulation starts after the first half of the recorded days; every threshold is set on past
days only (recall 99 % on the calibration days).
Writes results/simulation.json (KPIs) and results/simulation_<model>_<policy>.csv (one row per day).
Usage: python scripts/run_simulation.py [data/dataset.csv]   (about 10 minutes)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aoi_classification.data import load  # noqa: E402
from aoi_classification.simulation import simulate, summary  # noqa: E402

from aoi_classification.model import MODELS  # noqa: E402

POLICIES = {
    "train_once": dict(retrain_every=None),
    "retrain_weekly": dict(retrain_every=7),
}


def main(path="data/dataset.csv"):
    df = load(path)
    start = int(df["day"].quantile(0.5)) + 1
    Path("results").mkdir(exist_ok=True)
    res = {"start_day": start}
    for model in MODELS:
        res[model] = {}
        for name, kw in POLICIES.items():
            r = simulate(df, start, model=model, **kw)
            r.to_csv(f"results/simulation_{model}_{name}.csv", index=False)
            res[model][name] = summary(r)
            print(model, name, res[model][name], flush=True)
    Path("results/simulation.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:])
