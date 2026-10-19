# Cases

Each case is a **published** simulation model with **published expert results**. We first reproduce the expert results; only then is the case used to test the assistant.

| Folder | Case | Owner | Status |
|---|---|---|---|
| [`A1_smt2020/`](A1_smt2020/) | Semiconductor fab (SMT2020), large company | Melisa Subasi | first reproduction: 28 / 28 values within tolerance |
| [`A2_sme/`](A2_sme/) | Sheet-metal job shop, SME | Yu Han | first reproduction: identical to the published 30 replications |
| — | Case 3, new industry | Meron Hagos | to be chosen by P2 (3 Nov) |
| — | Case 4, new industry, held-out test case | Alejandro Rivas | to be chosen by P2 (3 Nov) |

**Selection criteria for a case:** the model files are public (or can be rebuilt exactly from the paper), the expert results are published with their spread, and the model can be run headless with open-source software.
