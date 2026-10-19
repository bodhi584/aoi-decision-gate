# Case 1 · SMT2020 semiconductor fab (large company)

**Owner:** Melisa Subasi

**Source and expert reference**
- Testbed: Kopp, D., Hassoun, M., Kalir, A. and Mönch, L. (2020). SMT2020 — A semiconductor manufacturing testbed. *IEEE Transactions on Semiconductor Manufacturing* 33(4), 522–531.
- Expert results: Tassel, P. et al. (2023). Semiconductor fab scheduling with self-supervised and reinforcement learning. *Proc. Winter Simulation Conference*. Table 1 (mean and sd over 100 seeds) is stored in `paper_table1.json`.
- Simulator: open-source implementation of Tassel et al., https://github.com/ingambe/RL4SemiconductorFabSched (MIT licence), pinned to commit `89467c6` by `setup.sh`.

**Scenarios:** two fabs (HVLM = high volume / low mix, LVHM = low volume / high mix) × two dispatching rules (FIFO, critical ratio). KPIs: cycle time and on-time share per lot class (regular, hot, super-hot), and the benchmark cost score.

## Run it
```bash
bash setup.sh                                                         # Python 3.9 venv + simulator (once)
.venv/bin/python run_static.py --dataset HVLM --rule fifo --days 30 --seed 0 --out test.json   # quick test, minutes
A1_CACHE_ONLY=1 python reproduce.py 6                                  # compare the stored 6-seed results with Table 1
```
A full 180-day run takes about 30–45 min on two CPU cores. The KPI summaries of our runs (4 scenarios × seeds 0–5) are in `precomputed/`, so `reproduce.py` can check them without re-running the simulator. `run_scenario.py` adds breakdown what-ifs (`--mtbf_factor`, `--mttr_factor`).

Known pitfalls: Python 3.9 only (numpy 1.22.4, cloudpickle 2.1.0); `wandb` is replaced by a stub in `stubs/`; the cost score is a benchmark score, not euros.

## First reproduction (17 Oct 2026)
See [`reproduction.md`](reproduction.md): **28 of 28 published values within tolerance** (6 seeds per scenario).
