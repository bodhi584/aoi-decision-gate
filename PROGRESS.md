# Progress

Last update: 23 Oct 2026

## Milestones

Each milestone follows the course requirements for the Software & Simulation track.

| Milestone | Date | Course requirement | What we deliver | Status |
|---|---|---|---|---|
| **P1** | 20 Oct · revised 23 Oct | Proposal + tech stack + MVP | Revised one-page proposal ([`docs/proposal.pdf`](docs/proposal.pdf)), slides ([`docs/slides_revised_topic.pdf`](docs/slides_revised_topic.pdf)), [README](README.md), data set, baseline and first replay simulation running | ✅ done |
| **P2** | 3 Nov | Core code + baseline sim; test plan + report | Decision gate and replay simulation as core code; baseline results for all update policies; test plan; literature report | 🔄 in progress |
| **P3** | 24 Nov | Feature progress; unit/CI status; issues board | Neural network model; drift detection; unit tests run on every push (CI); tasks as issues | ⏳ planned |
| **P4** | 8 Dec | Feature progress; unit/CI status; issues board | Full evaluation with production KPIs; error analysis by inspection type, component and period | ⏳ planned |
| **P5** | 22 Dec | Demo video + run instructions; packaging status | Replay demo (day-by-day decisions and saved inspections), demo video, run instructions, package | ⏳ planned |
| **Final** | 12 Jan | Final presentation, report | Final presentation and report | ⏳ planned |

## Timeline

![Project schedule](docs/img/gantt.png)

Tasks and owners are tracked as [issues](../../issues), grouped by [milestone](../../milestones).

## Tech stack

Python · pandas · scikit-learn (gradient-boosted trees) · PyTorch (neural network, from P3) · pytest and GitHub Actions (tests on every push) · matplotlib (figures)

## Log

- **23 Oct 2026** · Revised topic submitted: AI decision gate for false-call reduction after AOI (Siemens data). Repository renamed and rewritten for the new topic. Baseline and first replay simulation running; unit tests and CI set up.
- **22 Oct 2026** · Siemens AOI data set (Pfab et al. 2024) downloaded and checked: 440,274 flagged joints, 39,742 boards, strong drift over time. First baseline: time-ordered evaluation is much harder than a random split.
- **21 Oct 2026** · Siemens and NVIDIA announce an AI second check of AOI results in Erlangen (about 40 % fewer false calls targeted), confirming the problem is current.
- **20 Oct 2026** · P1: the first topic (Planner Copilot, an AI assistant for production-planning simulations) was judged too broad and not focused on one production problem. Decision: narrow to one concrete problem from the lecture examples (p. 18, Siemens quality control).
