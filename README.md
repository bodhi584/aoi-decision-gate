# Planner Copilot

**A local AI assistant for production planning simulations**

Case Study *Intelligent Systems in Production* · Technische Hochschule Deggendorf (THD) · Team 1 · guided by Dr. Hamidreza Heidari
Yu Han · Melisa Subasi · Meron Hagos · Alejandro Rivas

📄 Proposal slides: [`docs/P1_proposal_presentation.pdf`](docs/P1_proposal_presentation.pdf) · one-page proposal: [`docs/proposal.md`](docs/proposal.md) · progress: [`PROGRESS.md`](PROGRESS.md)

This page is our proposal in long form. Every section answers **what** we do and **why**. Each reason is backed by a source (paper and page), by our own results (linked file), or is marked as **our own setting** with the reasoning behind it. Terms are explained in the [glossary](#glossary); sources are listed under [references](#references).

---

## 1. The problem
**Good production planning needs simulation, and experts.**

- A busy week, missing workers or a broken machine: a simulation shows what will happen before it does.
- Today mostly only a simulation expert can run it correctly, and small companies often have none.
- An AI chatbot alone cannot plan production, and nobody can check its answer without an expert.

**Key motivations:** small companies get answers without a simulation expert · large companies save expert time · company data stays in-house · reliable AI help for planning is needed now.

> **Why simulation and not a spreadsheet?** Workers, machines and orders interact: when two machines need the same worker, one of them waits. A spreadsheet adds up average times and misses this waiting. Example from our Case 2: a spreadsheet estimate gives no overtime for a normal week, while the published simulation shows 3.3 hours of overtime and about 4 unfinished orders.
>
> **Why is an expert needed to run it?** Changing a validated model correctly takes expert knowledge. One simulation run is not an answer: five runs of the same model can give average delays from 1.8 to 10.4 minutes (Law 2023, p. 1488), so the expert decides how many runs are needed and reports a confidence interval. A model is also valid only for the conditions it was tested for (Sargent 2015, p. 1729), so the expert knows which questions it may answer.
>
> **Why can't an AI chatbot do it alone?** A language model produces plausible text, not calculated results. Language models cannot plan reliably on their own, and cannot reliably check their own plans (Kambhampati et al. 2024). Without an expert, nobody notices when the answer is wrong.

## 2. Project scope
**Aim:** test whether a local AI assistant with code checks can answer planning questions at the level of published expert simulations.

| Includes | Out of scope (current phase) |
|---|---|
| About 4 published simulation cases | A company's own production data and models |
| Test questions with correct answers | Commercial simulation tools |
| A local AI assistant with code checks | Use in a real factory |
| Comparison of three setups | |

> **Why published cases?** They come with expert results that were peer-reviewed or published with the model files. That gives us an objective reference to grade against, and anyone can repeat our tests with public data.
>
> **Why "at the level of published experts" and not "better than experts"?** The assistant does not replace the simulation method; it replaces the person who operates the model. Reaching the expert's result is the success criterion.
>
> **Why are company data, commercial tools and real factories out of scope?** Company data needs a validated company model and data agreements; commercial tools (e.g. Plant Simulation) need licences and cannot be shared openly; a real-factory trial needs time and safety approval beyond one semester. We keep them as future work.

## 3. Goals: three measurable targets

| Target | Measure | Meaning |
|---|---|---|
| **≥ 90 %** | Close to the expert | For questions with an answer, the AI's answer is close to the expert's answer. |
| **≤ 2 %** | Confidently wrong | The AI gives a wrong answer and sounds sure. This is the most dangerous error. |
| **≥ 90 %** | Correct refusals | When a question cannot be answered, the AI says so instead of guessing. |

> **Why these three measures?** They cover the three things that can happen to a planner: a useful answer, a dangerous answer, or an honest "I can't answer that". Accuracy alone would hide the dangerous answers.
>
> **Why is "confidently wrong" the most important?** A plant manager acts on a confident number, for example by hiring or cancelling overtime. A cautious answer costs time; a confidently wrong one costs money. Simulation validation treats the same error the same way: accepting an invalid model as valid is the *model user's risk*, which "must be kept small" (Sargent, Goldsman and Yaacoub 2016, p. 171). A confidently wrong answer is that error at the level of a single question, so its limit is the strictest (≤ 2 %).
>
> **What does "close to the expert" mean?** Within the wider of ±5 % or ±2 standard deviations of the published result. Comparable studies accept 5–10 % deviation from the reference model (Schmitt et al. 2026, p. 648), and simulation validation requires the accepted accuracy to be fixed before testing (Sargent 2015, p. 1730). We fix ours now, before any experiment.
>
> **Why should the AI refuse at all?** A language model tends to answer every question, even when it should not. The research literature on this problem states that models should "ideally abstain", i.e. refuse, when they cannot answer reliably (Wen et al. 2025, p. 529). A simulation model can answer only what it models (e.g. it has no costs in euros), so refusing those questions is part of a correct answer.
>
> **Why 90 % and 2 %, and not other numbers?** These values are **our own setting**; we found no published benchmark for this task to copy them from. We fixed them before any experiment, as validation practice requires (Sargent 2015, p. 1730), so they cannot be adjusted to fit our results. 100 % is not realistic: some published values rest on very few events (for example a handful of rush orders per run), so their spread is wide even for the expert. Whether 90 % is reached is part of the result.

## 4. Our idea
**An AI assistant that runs the simulation, and checks itself.**

![Question in plain language → Local AI assistant → Code checks every step → Existing simulation model → Answer with uncertainty](docs/img/idea.png)

The answer always comes from the simulation, never from the AI itself, and it shows how certain the result is.

> **Why an existing, validated model instead of letting the AI build one?** A recent study let large AI models build and adapt factory simulations: adapting a valid model was more reliable than generating a new one, and even then human checkpoints were required (Schmitt et al. 2026, pp. 646, 655). Validation is the expensive expert work; we reuse it.
>
> **Why code checks and not just instructions in the prompt?** Small AI models do not correct themselves reliably: in one study, self-reflection gave a small model no improvement at all (Shinn et al. 2023, Table 4), and a 7-billion-parameter model that gets 71.8 % of simple single tool calls right scores only 13.5 % on the basic multi-step category of the same benchmark (Patil et al. 2025, Table 1). A rule in the prompt is one more thing the model must remember; a rule in code is applied every time. This follows the principle "the AI suggests, external code verifies" (Kambhampati et al. 2024).
>
> **Which checks?** The standard rules of simulation practice, applied to every question: refuse questions outside the model's purpose; warn when an input is outside the validated range (Sargent 2015, p. 1729); use several independent runs and report a 95 % confidence interval (Law 2023, pp. 1488–1489); compare two scenarios run by run (Law 2023, p. 1498) on the same random numbers, which makes the difference more precise (Goldsman et al. 2005, p. 183).
>
> **Why "answer with uncertainty"?** Because one run is not an answer (see section 1). The planner sees a range, for example "3.7 h overtime (3.4–4.0 h, 30 runs)", and can judge the risk.
>
> **Why a local AI?** Data protection is the most named obstacle for companies that already use AI in Germany: in a 2026 survey of 603 German companies (20+ employees), 66 % of AI users named data-protection requirements and 45 % the worry that company data could "fall into the wrong hands" (Bitkom 2026). A model that runs on the company's own computer keeps production data in-house. It also makes our results repeatable: the same model version gives the same behaviour.

## 5. Technology stack

| Process | Tool | Purpose | Why this tool |
|---|---|---|---|
| Simulation | JaamSim, Python | A computer model of a factory: shows what happens if orders, workers or machines change | The published cases are built in these tools; both are free, open source and run without a screen, so we can run thousands of scenarios automatically |
| AI model | Open-source LLM (Ollama) | The AI that understands plain-language questions; runs on our own computer | Open models can run locally (data stays in-house); Ollama runs many different models the same way, so we can compare several |
| Code checks | Python, MCP server | Checks every AI step and refuses unclear questions | MCP (Model Context Protocol) is an open standard for connecting AI models to tools; any model can use the same checked tools |
| Interface | Gradio | A simple web page to ask questions and see charts | A web page in a few lines of Python, no separate front-end project |
| Compute | Google Colab GPU | A cloud computer with a graphics card to run the AI | Free; it stands in for the company PC with a graphics card in the final setting. Only public data is used there |
| Code sharing | GitHub | A shared place to store and track our code | Version history, review of each change, and this page for the lecturer |

*Tools may change as the project progresses.*

## 6. Plan: four steps

1. **Find cases**: about 4 published simulation cases from different industries, using public data only.
2. **Rebuild and ask**: rebuild each case and write test questions with the correct answers.
3. **Build the assistant**: a local AI assistant with code checks, built with open-source tools.
4. **Compare**: three setups: expert, AI + simulation, and AI + Planner Copilot + simulation.

> **Why about 4 cases from different industries?** One case could be solved by tuning to it. Several industries (semiconductors, metalworking, warehousing, metal forming) show whether the approach carries over. The number 4 is **our feasibility choice**: each case needs a reproduction, a case description and about 20 test questions, which is about one case per team member in one semester.
>
> **Why rebuild (reproduce) each case first?** If our run of the model does not match the published results, any later difference could be our mistake rather than the AI's. Reproduction comes first; only then is a case used for testing.
>
> **Why one held-out test case?** We tune the code checks on the other cases. If we tested only there, the result would be too optimistic, as in machine learning when a model is tested on its training data. The held-out case is run once at the end, with frozen rules, and its questions are written separately.
>
> **Why three setups?** *Expert* is the reference (the published result). *AI + simulation* shows what an AI does with the model but without our checks. *AI + Planner Copilot + simulation* adds the checks. The difference between the last two is the effect of our work; the same questions are used for all three.

### Method: Design Science Research
We follow the six steps of Design Science Research (Peffers et al. 2007): problem → objectives → design and development → demonstration → evaluation → communication.

> **Why this method?** Our result is a working system (an artifact), not a survey or a theory. Design Science Research is the standard method for building and evaluating such artifacts against a real problem (Hevner et al. 2004). Its process asks us to define measurable objectives before building (section 3) and to evaluate the system against them, going back to design where the evaluation shows a problem (Peffers et al. 2007, pp. 55–56).

### Cases
A case is one published factory simulation model with known expert results. Details: [`cases/`](cases/).

| Case | Industry | Source | Owner | Status |
|---|---|---|---|---|
| 1 | Semiconductor fab | SMT2020 (Kopp et al. 2020); expert results Tassel et al. 2023 | Melisa Subasi | first reproduction: 28 of 28 values within tolerance |
| 2 | Sheet-metal job shop (SME) | Jurczyk-Bunkowska 2026 (Zenodo) | Yu Han | first reproduction: identical to the published results |
| 3 | Pallet warehouse | Saengphueng 2026 (Zenodo) | Meron Hagos | candidate |
| 4 | Press line, held-out test case | Gołda, Kampa and Paprocka 2016 | Alejandro Rivas | candidate |

> **Why these cases?** Each one meets our case criteria: the model is public or can be rebuilt exactly from the paper, expert results are published with their spread, and it runs with free software. Together they cover a large company (Case 1) and small companies (Case 2), and the factors planners ask about: workers, machines, breakdowns, dispatching rules and order volume.

## 7. Team: who does what

| Yu Han | Melisa Subasi | Meron Hagos | Alejandro Rivas |
|---|---|---|---|
| **Team lead** | **Questions & report** | **Interface & literature** | **Experiments** |
| Case 2 | Case 1 | Case 3 | Case 4 |
| Code checks (guardrail engine) | Test questions | User interface | Experiments |
| | Final report editor | Literature review | GitHub & demo |

> **Why does everyone own one case?** Each case needs someone who knows its model in detail. It also spreads the work evenly.
>
> **Why does the owner of the held-out case run the experiments, not the code checks?** The person who writes the checks must not see the held-out test questions; otherwise the final test would not be fair.

## 8. Timeline

| Date | Milestone | Status |
|---|---|---|
| 20 Oct | Proposal, team, GitHub | ✅ |
| 3 Nov | Literature report, method outline, baseline simulation | 🔄 |
| 24 Nov | Cases rebuilt, first version of the assistant | ⏳ |
| 8 Dec | First experiments | ⏳ |
| 22 Dec | Demo, experiments and analysis, report draft | ⏳ |
| 12 Jan | Final presentation, report, demo video | ⏳ |

![Project schedule](docs/img/gantt.png)

> **Why this order?** The dates follow the course milestones. Cases must be reproduced before they can be used for testing, and the checks must be finished before the experiments; so reproduction and building overlap in November, and experiments start only in December.

## 9. Expected outcomes

| | |
|---|---|
| **Test questions** | Questions with correct answers for about 4 published cases. |
| **Planner Copilot** | A working open-source assistant that runs the simulations. |
| **Comparison** | Measured results for three setups against our targets. |
| **Report and demo** | Final report, demo video and this GitHub repository. |

> **Why publish the test questions and the software?** So that others can repeat the comparison with other AI models; the comparison is only meaningful if the questions and grading are open.

## 10. Bill of materials

| Component | Specification | Cost |
|---|---|---|
| GPU access (Google Colab) | Cloud GPU for the local AI | Free tier, to be confirmed |
| Simulation cases and data | Published, public | Free |
| Software | Open source | Free |

> **Why no budget?** Everything we use is open source or public, which is also what makes the work repeatable for anyone. The only open point is how much free GPU time we will get.

## 11. Risks and ethics
- **Ethics:** only public data, so no privacy issue. All sources are cited.
- **Main risk:** rebuilding the cases may take longer than planned. Fallback: fewer cases (a reserve case is already identified, see [`cases/`](cases/)).

> **Why is this the main risk?** A case is only usable after its published results are reproduced, and published models often lack details. Two cases are already reproduced, which lowers this risk.

---

## Glossary
| Term | Meaning |
|---|---|
| AI model / LLM | Large language model: an AI that reads and writes text, e.g. understands a planner's question |
| Local AI | The AI model runs on the company's own computer, not on an internet service |
| DES | Discrete-event simulation: a computer model that steps through events (an order arrives, a machine breaks) to predict waiting times, output and overtime |
| Validated model | A simulation model whose results were checked against the real system for stated conditions |
| Replication / run | One simulation of the same scenario with different random numbers; several runs are averaged |
| Confidence interval (95 %) | The range in which the true average lies with 95 % confidence, computed from several runs |
| Code checks / guardrails | Program rules that check every AI step before the simulation runs |
| MCP | Model Context Protocol: an open standard for how AI models call tools |
| SME | Small or medium-sized enterprise |
| Held-out test case | A case kept aside and used only once, for the final test |

## References
- Goldsman, D., Kim, S.-H. and Nelson, B. L. (2005). Statistical selection of the best system. *Proc. Winter Simulation Conference*, 178–187.
- Hevner, A. R., March, S. T., Park, J. and Ram, S. (2004). Design science in information systems research. *MIS Quarterly* 28(1), 75–105.
- Kambhampati, S. et al. (2024). Position: LLMs can't plan, but can help planning in LLM-Modulo frameworks. *Proc. 41st ICML*, PMLR 235.
- Law, A. M. (2023). Design and analysis of simulation experiments using three simple statistical formulas. *Proc. Winter Simulation Conference*, 1487–1499.
- Patil, S. G. et al. (2025). The Berkeley Function Calling Leaderboard (BFCL): from tool use to agentic evaluation of large language models. *Proc. 42nd ICML*, PMLR 267.
- Peffers, K., Tuunanen, T., Rothenberger, M. A. and Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems* 24(3), 45–77.
- Sargent, R. G. (2015). An introductory tutorial on verification and validation of simulation models. *Proc. Winter Simulation Conference*, 1729–1740.
- Schmitt, T. et al. (2026). LLM-driven discrete-event simulation: a generative AI framework for automated model generation, adaptation, and evaluation in manufacturing. *Journal of Manufacturing Systems* 85, 642–661.
- Shinn, N. et al. (2023). Reflexion: language agents with verbal reinforcement learning. *Advances in Neural Information Processing Systems 36*.
- Sargent, R. G., Goldsman, D. M. and Yaacoub, T. (2016). A tutorial on the operational validation of simulation models. *Proc. Winter Simulation Conference*, 163–177.
- Wen, B. et al. (2025). Know your limits: a survey of abstention in large language models. *Transactions of the Association for Computational Linguistics* 13, 529–556.
- Bitkom (2026). *Erstmals nutzt Mehrheit der Unternehmen KI* [press release, 14 Sep 2026; survey of 603 companies with 20+ employees]. https://www.bitkom.org/Presse/Presseinformation/Erstmals-nutzt-Mehrheit-Unternehmen-KI
- Case sources: see [`cases/`](cases/).

---

## Repository structure

| Folder | Content |
|---|---|
| [`docs/`](docs/) | Proposal, presentations, final report |
| [`cases/`](cases/) | One folder per case: model setup and reproduction of the published expert results |
| `lit/`, `engine/`, `agent/`, `ui/`, `eval/` | Added at the milestones above |

Code: MIT licence ([`LICENSE`](LICENSE)). Simulation models and data belong to their authors and are used under their licences, cited in each case folder.
