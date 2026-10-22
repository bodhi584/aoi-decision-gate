"""Facts about the Siemens AOI data used on the README: size, false-call share, imbalance, drift.

Drift test: a classifier tries to tell the first 30 % of days from the last 30 % using the AOI features only.
AUROC near 0.5 = no drift; near 1.0 = the measurements changed a lot over time.
Usage: python scripts/data_facts.py [data/dataset.csv]
"""
import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_predict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gate.data import boards, load  # noqa: E402
from gate.model import make_classifier, to_X  # noqa: E402


def main(path="data/dataset.csv"):
    df = load(path)
    b = boards(df)
    weekly = b.groupby(b.day // 7).agg(boards=("defective", "size"), defective=("defective", "sum"))
    e, l = df[df.day <= df.day.quantile(0.3)], df[df.day >= df.day.quantile(0.7)]
    s = pd.concat([e.assign(period=0), l.assign(period=1)]).sample(120_000, random_state=0)
    p = cross_val_predict(make_classifier("random_forest"),
                          to_X(s), s.period, cv=3, method="predict_proba")[:, 1]
    facts = {
        "joints": len(df), "boards": len(b), "calendar_days": int(df.day.max()) + 1,
        "days_with_data": int(df.day.nunique()),
        "true_defect_joints": int(df["class"].sum()),
        "defective_boards": int(b.defective.sum()),
        "false_call_share_of_boards_pct": round(100 * (1 - b.defective.mean()), 1),
        "true_defect_share_of_joints_pct": round(100 * df["class"].mean(), 2),
        "joints_per_inspection_type": df.inspection_type.value_counts().sort_index().to_dict(),
        "drift_test_auroc_first_vs_last_30pct_days": round(roc_auc_score(s.period, p), 3),
        "weekly_boards_and_defective_boards": {int(k): [int(v.boards), int(v.defective)] for k, v in weekly.iterrows()},
    }
    Path("results").mkdir(exist_ok=True)
    Path("results/data_facts.json").write_text(json.dumps(facts, indent=2))
    print(json.dumps({k: v for k, v in facts.items() if k != "weekly_boards_and_defective_boards"}, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:])
