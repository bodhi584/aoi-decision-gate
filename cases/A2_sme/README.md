# Case 2 · SME sheet-metal job shop (JaamSim)

**Owner:** Yu Han

**Source and expert reference**
Jurczyk-Bunkowska, M. (2026). *JaamSim models, order portfolios, and replication results for capacity planning in an SME manufacturing system.* Zenodo, DOI [10.5281/zenodo.23229885](https://doi.org/10.5281/zenodo.23229885), licence CC BY 4.0.
A real job shop: 69 orders, 3 shared workers, 4 machines (sheet laser, tube laser, punching machine, bending machine). The authors publish the model files and their 30-replication results, which are our expert reference (`expert_values.json`).

**Scenarios:** normal week (`norm`) and a week with 20 % more orders (`over20`). KPIs: overtime after the Friday shift end, orders unfinished on Friday, machine utilisation.

## Run it
1. `bash setup.sh` builds the open-source JaamSim simulator headless (Java 17+, a few minutes, once).
2. Download the model files into `model/` (list and MD5 checksums in [`model/README.md`](model/README.md)); the notebook does this and checks the MD5.
3. `bash run.sh M3 norm` and `bash run.sh M3 over20` run the published scenarios (30 replications each, a few seconds).
4. [`reproduce.ipynb`](reproduce.ipynb) prints our values next to the published ones.

## First reproduction (14 Oct 2026)
All 30 replications are **identical** to the authors' published results (difference 0 in every replication):

| Scenario | Overtime after Friday shift end (h) | Unfinished orders | Bottleneck |
|---|---|---|---|
| normal week | 3.31 (sd 0.42) | 4.4 | sheet laser (32 % busy) |
| +20 % orders | 11.54 (sd 0.59) | 15.2 | sheet laser (36 % busy) |

Full output: [`reproduce_output.txt`](reproduce_output.txt). It also contains a 4-worker variant, which is our own run and not a published scenario.
