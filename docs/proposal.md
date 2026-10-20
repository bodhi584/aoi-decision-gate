# One-page proposal (P1, 20 Oct 2026)

**Course:** MDM2 – Case Study: Intelligent Systems in Production
**Team:** Team 1 · Yu Han · Melisa Subasi · Meron Hagos · Alejandro Rivas
**Project title:** Planner Copilot: A Local AI Assistant for Production Planning Simulations
**Industrial application:** production planning when orders suddenly increase, workers are missing or machines break down, for small and large factories without an in-house simulation expert
**Keywords:** AI assistant, simulation, production planning, decision support

## Roles and cases
Each member owns one case (a published factory simulation model with known expert results):
- Case 1, semiconductor fab (SMT2020): Melisa Subasi; also test questions, final report
- Case 2, sheet-metal job shop (SME): Yu Han (team lead); also code checks (guardrail engine)
- Case 3, new industry, still to be chosen: Meron Hagos; also user interface, literature review
- Case 4, another new industry (test case), still to be chosen: Alejandro Rivas; also experiments

## 1) Problem statement and measurable outcomes
When a factory has a busy week, missing workers or a broken machine, it needs a simulation to plan well. Today mostly only a simulation expert can run it correctly. We plan to build Planner Copilot: an AI assistant that runs existing simulation models and checks its own steps with code. Goals, to be tested on published expert cases: at least 90 % of answers within an agreed tolerance of the expert result; at most 2 % confidently wrong answers; at least 90 % correct refusals when a question cannot be answered.

## 2) Motivation and industrial relevance
Small companies get answers without hiring a simulation expert, and large companies save expert time. Company data stays in-house. Reliable AI help for production planning is needed now.

## 3) Related work snapshot
Schmitt et al. (2026): AI can adapt existing simulation models, but needs cloud AI and expert checks. Kambhampati et al. (2024): the AI suggests, code verifies. Our gap: a local AI with code checks instead of expert checks, compared with published expert results.

## 4) Method and feasibility
We plan to use published simulation cases (public data) from about 4 industries and rebuild them. For each case we plan to write test questions with correct answers. We plan to build the assistant with open-source tools and compare three setups: expert, AI + simulation, and AI + Planner Copilot + simulation. Expected results: software, test questions, report and demo. Details will be refined as the project progresses.

## 5) Milestones and timeline
| | Date | Deliverable |
|---|---|---|
| P1 | 20 Oct | proposal, team, GitHub |
| P2 | 3 Nov | literature report, method outline, baseline simulation |
| P3 | 24 Nov | cases rebuilt, first version of the assistant |
| P4 | 8 Dec | first experiments |
| P5 | 22 Dec | demo, experiments and analysis, report draft |
| Final | 12 Jan | final presentation, report, demo video |

## 6) Risks and ethics
Only public data will be used, so no privacy issue; all sources are cited. Main risk: rebuilding the cases takes longer than planned (fallback: fewer cases).

## References
- Kambhampati, S. et al. (2024). Position: LLMs can't plan, but can help planning in LLM-Modulo frameworks. *Proc. 41st ICML*, PMLR 235.
- Schmitt, T. et al. (2026). LLM-driven discrete-event simulation: a generative AI framework for automated model generation, adaptation, and evaluation in manufacturing. *Journal of Manufacturing Systems* 85, 642–661.
