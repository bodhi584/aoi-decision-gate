# Progress

Last update: 20 Oct 2026

## Milestones

Each milestone follows the course requirements for the Software & Simulation track.

| Milestone | Date | Course requirement | What we deliver | Status |
|---|---|---|---|---|
| **P1** | 20 Oct | Proposal + tech stack + MVP | Proposal ([`docs/proposal.md`](docs/proposal.md)), slides with tech stack and MVP ([`docs/P1_proposal_presentation.pdf`](docs/P1_proposal_presentation.pdf)), [README](README.md) | ✅ done |
| **P2** | 3 Nov | Core code + baseline simulation; test plan + report | Code checks and workflow (core of Planner Copilot); all four cases running as baseline simulations; test plan; literature report and method | 🔄 in progress |
| **P3** | 24 Nov | Feature progress; unit/CI status; issues board | First version of the assistant on all cases; unit tests run automatically on every change (CI); tasks tracked as issues | ⏳ planned |
| **P4** | 8 Dec | Feature progress; unit/CI status; issues board | First experiments (three setups); test status and issues updated | ⏳ planned |
| **P5** | 22 Dec | Demo video + run instructions; packaging status | Demo video, step-by-step run instructions, installable package | ⏳ planned |
| **Final** | 12 Jan | Final presentation, report | Final presentation, final report, full evaluation including the held-out case | ⏳ planned |

## Timeline

![Project schedule](docs/img/gantt.png)

Tasks and owners are tracked as [issues](../../issues), grouped by [milestone](../../milestones).

## Cases

| Case | Industry | Source | Owner | Status |
|---|---|---|---|---|
| 1 | Semiconductor fab (large company) | SMT2020 testbed (Kopp et al. 2020); expert results from Tassel et al. 2023 | Melisa Subasi | chosen · first reproduction: 28 of 28 published values within tolerance |
| 2 | Sheet-metal job shop (SME) | JaamSim model and 30-replication results, Jurczyk-Bunkowska 2026 (Zenodo) | Yu Han | chosen · reproduction identical to the published replications |
| 3 | Pallet warehouse with reach trucks (logistics) | Saengphueng 2026 (Zenodo) | Meron Hagos | candidate · first check: 360 of 360 published values reproduced |
| 4 | Press line, manual vs robotic (held-out test) | Gołda, Kampa and Paprocka 2016 (FedCSIS) | Alejandro Rivas | candidate · to be confirmed |

Case 4 is the held-out test case: its test questions are written separately and kept out of this repository until the final evaluation.

## Log

- **20 Oct 2026** · Proposal submitted (P1). Repository published.
- **16 Oct 2026** · Candidates for Cases 3 and 4 found (warehouse, press line); Case 3 first check: the published 60 scenarios × 6 KPIs reproduced exactly.
- **16–17 Oct 2026** · Case 1: open-source SMT2020 simulator set up; four published scenarios (HVLM / LVHM × FIFO / critical ratio) run with 6 seeds each; all 28 values of Tassel et al. (2023, Table 1) within tolerance. See [`cases/A1_smt2020/`](cases/A1_smt2020/).
- **14 Oct 2026** · Case 2: published JaamSim model run headless; 30 replications identical to the authors' published results (overtime 3.31 h normal week, 11.54 h with 20 % more orders). See [`cases/A2_sme/`](cases/A2_sme/).
