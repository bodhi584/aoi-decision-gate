# Cases

Each case is a **published** simulation model with **published expert results**. We first reproduce the expert results; only then is the case used to test the assistant.

| Folder | Case | Owner | Status |
|---|---|---|---|
| [`A1_smt2020/`](A1_smt2020/) | Semiconductor fab (SMT2020), large company | Melisa Subasi | first reproduction: 28 / 28 values within tolerance |
| [`A2_sme/`](A2_sme/) | Sheet-metal job shop, SME | Yu Han | first reproduction: identical to the published 30 replications |
| Case 3 | Pallet warehouse with reach trucks (logistics). Source: Saengphueng (2026), *Code and Data for: Task Interleaving in Warehouse Operations*, Zenodo, DOI 10.5281/zenodo.21469786 | Meron Hagos | candidate · first check: all 360 published KPI means reproduced · to be confirmed by P2 (3 Nov) |
| Case 4 | Press line, manual vs robotic (metal forming), **held-out test case**. Source: Gołda, Kampa and Paprocka (2016), *Proc. FedCSIS*, DOI 10.15439/2016F307 | Alejandro Rivas | candidate · to be confirmed by P2 (3 Nov) |
| reserve | Operator-paced assembly line. Source: Seppanen (2005), *Proc. Winter Simulation Conference*, 1343–1349, DOI 10.1109/WSC.2005.1574396 | — | reserve case if a candidate fails |

**Selection criteria for a case:** the model files are public (or can be rebuilt exactly from the paper), the expert results are published with their spread, and the model can be run headless with open-source software.

Code and data for Cases 3 and 4 are added once the cases are confirmed. For the held-out Case 4, the test questions stay out of this repository until the final evaluation.
