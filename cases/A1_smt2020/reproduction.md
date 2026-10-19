# Case 1 · reproduction of Tassel et al. (2023), Table 1

180 simulated days after the simulator's one-year warm-up, four scenarios, seeds 0–5 (6 replications each; the paper uses 100).
Pass rule: our mean lies within the wider of ±5 %, ±2 published sd, or ±2 percentage points for on-time shares.

**Result: 28 of 28 values within tolerance.**

| Scenario | Regular lots, cycle time (days) ours / paper | Hot lots, cycle time (days) ours / paper | Cost score ours / paper |
|---|---|---|---|
| HVLM, FIFO | 71.78 / 72.57 | 26.92 / 26.91 | 37,914 / 38,014 |
| HVLM, critical ratio | 70.43 / 70.80 | 26.90 / 26.94 | 39,609 / 39,813 |
| LVHM, FIFO | 53.96 / 52.38 | 23.85 / 23.80 | 101,810 / 102,171 |
| LVHM, critical ratio | 52.18 / 52.25 | 23.73 / 23.71 | 106,867 / 108,856 |

Run `A1_CACHE_ONLY=1 python reproduce.py 6` to print all 28 values next to the paper.

**Caveats**
- 6 seeds instead of 100: the means match; our spread estimate is still rough.
- Super-hot on-time share rests on only 9–10 lots per run, so it passes only through the wide published spread.
- LVHM FIFO regular cycle time is 3.0 % above the paper (inside the 5 % tolerance); the other cycle times are within 1.1 %.
