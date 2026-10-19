# Feasibility test (16 Oct 2026)

A first small test to check that the approach works at all, before the planned experiments (P4). It is **not** one of the planned experiments: the question set was not yet split into development and test, and only two cases were used.

| | |
|---|---|
| AI model | Qwen 2.5, 7 billion parameters, instruction-tuned (open source), run locally with Ollama on a free Colab GPU |
| Cases | pallet warehouse (Case 3 candidate) and operator-paced assembly line (reserve case) |
| Questions | 40 (20 per case), each with a fixed correct answer and tolerance |
| Setups | A: AI + simulation, no checks · B: the same rules written as instructions in the prompt · C: AI + Planner Copilot (code checks) |
| Repetitions | each question answered once per setup (temperature 0) |

## Result (40 questions per setup)

| Setup | Correct | Cautious | Confidently wrong |
|---|---|---|---|
| A · AI + simulation, no checks | 20 (50 %) | 4 (10 %) | 16 (40 %) |
| B · rules as prompt instructions | 26 (65 %) | 8 (20 %) | 6 (15 %) |
| C · AI + Planner Copilot | **38 (95 %)** | 1 (2.5 %) | **1 (2.5 %)** |

## What it shows, and what it does not
- The direction is clear: code checks reduced confidently wrong answers from 16 to 1; writing the same rules into the prompt helped, but much less (6).
- 40 questions on two cases with one model are too few for a firm conclusion: the 95 % confidence interval for 38/40 correct is about 83–99 %. The planned experiments use all four cases, about 150 questions and several AI models.
- These results informed the targets in the [README](../README.md#3-goals-three-measurable-targets) (90 % correct, ≤ 2 % confidently wrong).
