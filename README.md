# Planner Copilot

**A local AI assistant for production planning simulations**

Case Study *Intelligent Systems in Production* · Technische Hochschule Deggendorf (THD) · Team 1 · guided by Dr. Hamidreza Heidari
Yu Han · Melisa Subasi · Meron Hagos · Alejandro Rivas

📄 Proposal slides: [`docs/P1_proposal_presentation.pdf`](docs/P1_proposal_presentation.pdf) · one-page proposal: [`docs/proposal.md`](docs/proposal.md) · progress: [`PROGRESS.md`](PROGRESS.md)

---

## The problem
**Good production planning needs simulation, and experts.**

- A busy week, missing workers or a broken machine: a simulation shows what will happen before it does.
- Today mostly only a simulation expert can run it correctly, and small companies often have none.
- An AI chatbot alone cannot plan production, and nobody can check its answer without an expert.

**Key motivations:** small companies get answers without a simulation expert · large companies save expert time · company data stays in-house · reliable AI help for planning is needed now.

## Project scope
**Aim:** test whether a local AI assistant with code checks can answer planning questions at the level of published expert simulations.

| Includes | Out of scope (current phase) |
|---|---|
| About 4 published simulation cases | A company's own production data and models |
| Test questions with correct answers | Commercial simulation tools |
| A local AI assistant with code checks | Use in a real factory |
| Comparison of three setups | |

## Goals: three measurable targets

| Target | Measure | Meaning |
|---|---|---|
| **≥ 90 %** | Close to the expert | For questions with an answer, the AI's answer is close to the expert's answer. |
| **≤ 2 %** | Confidently wrong | The AI gives a wrong answer and sounds sure. This is the most dangerous error. |
| **≥ 90 %** | Correct refusals | When a question cannot be answered, the AI says so instead of guessing. |

## Our idea
**An AI assistant that runs the simulation, and checks itself.**

![Question in plain language → Local AI assistant → Code checks every step → Existing simulation model → Answer with uncertainty](docs/img/idea.png)

The answer always comes from the simulation, never from the AI itself, and it shows how certain the result is.

## Technology stack

| Process | Tool | Purpose |
|---|---|---|
| Simulation | JaamSim, Python | A computer model of a factory: shows what happens if orders, workers or machines change |
| AI model | Open-source LLM (Ollama) | The AI that understands plain-language questions; runs on our own computer |
| Code checks | Python, MCP server | Checks every AI step and refuses unclear questions |
| Interface | Gradio | A simple web page to ask questions and see charts |
| Compute | Google Colab GPU | A cloud computer with a graphics card to run the AI |
| Code sharing | GitHub | A shared place to store and track our code |

*Tools may change as the project progresses.*

## Plan: four steps

1. **Find cases**: about 4 published simulation cases from different industries, using public data only.
2. **Rebuild and ask**: rebuild each case and write test questions with the correct answers.
3. **Build the assistant**: a local AI assistant with code checks, built with open-source tools.
4. **Compare**: three setups: expert, AI + simulation, and AI + Planner Copilot + simulation.

### Cases
A case is one published factory simulation model with known expert results. Details: [`cases/`](cases/).

| Case | Industry | Source | Owner | Status |
|---|---|---|---|---|
| 1 | Semiconductor fab | SMT2020 (Kopp et al. 2020); expert results Tassel et al. 2023 | Melisa Subasi | first reproduction: 28 of 28 values within tolerance |
| 2 | Sheet-metal job shop (SME) | Jurczyk-Bunkowska 2026 (Zenodo) | Yu Han | first reproduction: identical to the published results |
| 3 | Pallet warehouse | Saengphueng 2026 (Zenodo) | Meron Hagos | candidate |
| 4 | Press line, held-out test case | Gołda, Kampa and Paprocka 2016 | Alejandro Rivas | candidate |

## Team: who does what

| Yu Han | Melisa Subasi | Meron Hagos | Alejandro Rivas |
|---|---|---|---|
| **Team lead** | **Questions & report** | **Interface & literature** | **Experiments** |
| Case 2 | Case 1 | Case 3 | Case 4 |
| Code checks (guardrail engine) | Test questions | User interface | Experiments |
| | Final report editor | Literature review | GitHub & demo |

## Timeline

| Date | Milestone | Status |
|---|---|---|
| 20 Oct | Proposal, team, GitHub | ✅ |
| 3 Nov | Literature report, method outline, baseline simulation | 🔄 |
| 24 Nov | Cases rebuilt, first version of the assistant | ⏳ |
| 8 Dec | First experiments | ⏳ |
| 22 Dec | Demo, experiments and analysis, report draft | ⏳ |
| 12 Jan | Final presentation, report, demo video | ⏳ |

![Project schedule](docs/img/gantt.png)

## Expected outcomes

| | |
|---|---|
| **Test questions** | Questions with correct answers for about 4 published cases. |
| **Planner Copilot** | A working open-source assistant that runs the simulations. |
| **Comparison** | Measured results for three setups against our targets. |
| **Report and demo** | Final report, demo video and this GitHub repository. |

## Bill of materials

| Component | Specification | Cost |
|---|---|---|
| GPU access (Google Colab) | Cloud GPU for the local AI | Free tier, to be confirmed |
| Simulation cases and data | Published, public | Free |
| Software | Open source | Free |

## Risks and ethics
- **Ethics:** only public data, so no privacy issue. All sources are cited.
- **Main risk:** rebuilding the cases may take longer than planned. Fallback: fewer cases.

---

## Repository structure

| Folder | Content |
|---|---|
| [`docs/`](docs/) | Proposal, presentations, final report |
| [`cases/`](cases/) | One folder per case: model setup and reproduction of the published expert results |
| `lit/`, `engine/`, `agent/`, `ui/`, `eval/` | Added at the milestones above |

Code: MIT licence ([`LICENSE`](LICENSE)). Simulation models and data belong to their authors and are used under their licences, cited in each case folder.
