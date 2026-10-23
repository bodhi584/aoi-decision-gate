# How the code works (for everyone in the team)

The core is three short files in `aoi_classification/`: `data.py`, `model.py`, `simulation.py` (about 190 lines together).
Everything else in `scripts/` only calls these files and saves results.

## The six steps

| Step | What happens | Where |
|---|---|---|
| 1. Load | Read the Siemens CSV. One row = one solder joint flagged by the AOI machine. `class` is the manual-inspection result: 0 = false call, 1 = true defect. Rows with the same timestamp are one board; `day` counts days from the first record. | `data.py` → `load()` |
| 2. Prepare | Input columns: 5 categorical fields (inspection type and 4 anonymised fields such as component type and AOI error code) and about 70 AOI measurements. Logistic regression and the neural network get categories as 0/1 columns and scaled measurements; the random forest gets categories as numbers and raw measurements. | `model.py` → `make_classifier()`, `to_X()` |
| 3. Train | The classifier learns from past days which joints were true defects. It gives every joint a score between 0 and 1. | `model.py` → `FalseCallClassifier.fit()` |
| 4. Board score | A board's score is the highest score of its flagged joints (one bad joint makes the board defective). | `model.py` → `board_scores()` |
| 5. Threshold | On the last 14 days of the training data we choose the threshold so that at most 1 % of the true defects score below it (recall 99 %). Below the threshold = false call. | `model.py` → `threshold_for()` |
| 6. Simulate | The recorded days are played back in time order. Each day is classified by a model trained only on earlier days. We count false calls correctly classified (= manual inspections saved) and true defects missed. | `simulation.py` → `simulate()`, `summary()` |

Run it step by step: `model_training.ipynb`.

## Questions the lecturer may ask

**What is the input, the system and the output?**
Input: one AOI alarm (a flagged board with about 70 measurements per flagged solder joint). System: binary classification with supervised machine learning, trained on past manual-inspection results. Output: true defect (goes to manual inspection) or false call (skips manual inspection).

**Why "supervised"?**
Every training example has a known answer (the label from the manual inspection station). The model learns from these labelled examples.

**Why binary classification?**
There are exactly two classes in the data: 0 = false call, 1 = true defect.

**Why three models?**
Logistic regression is the simplest baseline. Random forest is a standard method for table data. The neural network (one hidden layer, 10 neurons) is the method from the lecture (p. 12, 17). We compare them on the same task.

**What are recall and specificity?**
Positive class = true defect. Recall = share of true defects that we classify as true defect (target ≥ 99 %). Specificity = share of false calls that we classify as false call (target ≥ 20 %); each one is a manual inspection saved.

**Why is recall so strict (99 %)?**
A missed true defect leaves the factory. Saving inspection time must not lower quality.

**Why do you test in time order and not with a random split?**
In a factory the model is always trained on the past and used on the future. A random split mixes future and past and looks much better than reality: specificity 14–18 % with a random split, but only 1.8–6.4 % in time order (results/baseline.json).

**Why is the threshold set on separate days and not on the training data?**
On its own training data a model looks better than it really is. The last 14 days are kept out of training so the threshold is set on data the model has not seen.

**Why is the board score the maximum of its joints?**
A board is defective if any one of its joints is defective. So the board is as risky as its riskiest joint.

**Why `class_weight="balanced"`?**
Only about 1 % of flagged joints are true defects. Without weighting, the model would learn to say "false call" almost always.

**Why scale the measurements for logistic regression and the neural network but not for the random forest?**
Logistic regression and neural networks learn weights and work best when all inputs have a similar range. Decision trees only compare a value with a split point, so scaling does not change them.

**Why retrain every week?**
The production line changes over time (materials, settings, products). We compare "train once" with "retrain every week" in the simulation.

**Is the data real? Can we share it?**
Real production data from a Siemens SMT line in Bavaria (Pfab et al. 2024, *Data in Brief* 53, 110110), licence CC BY-NC 3.0. It is not stored in our repository; `scripts/download_data.py` downloads it and checks the checksum.

**Where does every number come from?**
From the files in `results/`, written by the scripts in `scripts/`. Anyone can reproduce them with the commands in README section *Run it*.
