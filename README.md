# Planner Copilot

**A local AI assistant for production planning simulations.**
Case Study *Intelligent Systems in Production* (MDM-M-2), Technische Hochschule Deggendorf (THD), winter semester 2026/27 · Team 1

| | |
|---|---|
| Team | Yu Han (team lead) · Melisa Subasi · Meron Hagos · Alejandro Rivas |
| Status | **P1 – proposal** (20 Oct 2026). Milestone plan and log: [`PROGRESS.md`](PROGRESS.md) · tasks: [Issues](../../issues) · deadlines: [Milestones](../../milestones) |
| Proposal | [`docs/proposal.md`](docs/proposal.md) · slides: [`docs/P1_proposal_presentation.pdf`](docs/P1_proposal_presentation.pdf) |

## The problem

When a factory has a busy week, missing workers or a broken machine, it needs a simulation to plan well. A validated discrete-event simulation (DES) model can answer questions such as *"20 % more orders next week: do we need a fourth worker?"*, but today mostly a simulation expert can run it correctly: which inputs are inside the validated range, how many runs are needed, how to compare two scenarios.

## Our approach

Planner Copilot is an assistant that runs **existing, validated** simulation models on behalf of a planner and **checks its own steps with code**:

```
planner's question ──► input check ──► local language model ──► code checks ──► simulation model ──► answer + confidence interval
                       (units, missing data)   (chooses the scenario)   (scope, valid range,     (published,       or a reasoned refusal
                                                                          replications)            validated)
```

- The language model runs **locally** (open-source model), so company data stays in-house.
- Every number comes from the simulation, never from the language model.
- Code checks enforce standard simulation practice: questions outside the model's scope are refused, inputs outside the validated range are flagged, and results come with replications and a 95 % confidence interval.

## How we will evaluate it

We use **published simulation cases with known expert results** from about four industries and compare three setups on the same test questions: the expert result, *AI + simulation*, and *AI + Planner Copilot + simulation*. Targets: ≥ 90 % of answers within tolerance of the expert result, ≤ 2 % confidently wrong answers, ≥ 90 % correct refusals.

## Repository structure

| Folder | Content | Status |
|---|---|---|
| [`docs/`](docs/) | Proposal, presentations, final report | proposal and P1 slides ✅ |
| [`cases/`](cases/) | One folder per published case: model setup, reproduction of the expert results | Case 1 and Case 2 chosen, first reproductions done |
| `lit/` | Literature review | due P2 (3 Nov) |
| `engine/` | Code checks around the language model | from P3 (24 Nov) |
| `agent/` | Assistant workflow and model selection | from P3 (24 Nov) |
| `eval/` | Test questions, grading, experiment results | from P3–P4 |
| `ui/` | Chat front end and charts | from P3 |

## Reproduce what is here

Everything uses public data and open-source software; no paid service is needed.

- **Case 1, semiconductor fab (SMT2020):** [`cases/A1_smt2020/`](cases/A1_smt2020/)
- **Case 2, sheet-metal job shop (SME):** [`cases/A2_sme/`](cases/A2_sme/)

## Licence

Code: MIT (see [`LICENSE`](LICENSE)). Simulation models and data belong to their authors and are used under their licences (cited in each case folder).
