# How to work on this project (Team 1)

Each task is a GitHub issue with steps, a deliverable and a due date: see [issues](../../issues), grouped by [milestone](../../milestones) (P2 … Final).

## 1. Set up (once, about 15 minutes)

You need Python 3.11 or newer and Git. No graphics card is needed; Google Colab also works.

```bash
git clone https://github.com/bodhi584/aoi-false-call-classification
cd aoi-false-call-classification
pip install -r requirements.txt pytest jupyter
python scripts/download_data.py      # Siemens AOI data, about 330 MB, checked by checksum
python -m pytest -q                  # all tests should pass
jupyter notebook model_training.ipynb
```

The data are **not** stored in the repository (licence CC BY-NC 3.0). The download script puts them in `data/`.

## 2. Work on your issue

1. Open your issue and read the steps and the *Done when* line.
2. Create a branch with the issue number: `git checkout -b 12-test-plan`
3. Save your files where the issue says (`docs/`, `docs/img/`, `notebooks/`, `tests/`).
4. Push and open a pull request that says `Closes #12`.

```bash
git add docs/test_plan.md
git commit -m "Test plan (#12)"
git push -u origin 12-test-plan
```

No Git? Use **Add file → Upload files** on GitHub, choose *Create a new branch*, and open the pull request there.

## 3. Rules

- English only, short sentences, the terms from the README (binary classification, true defect, false call, recall, specificity).
- Every number comes from a result file in `results/` or a cited source.
- **Keep code simple.** Plain functions, short files, one comment per step, standard scikit-learn and pandas calls only. Every team member must be able to explain every line to the lecturer. How the existing code works: [`docs/code_walkthrough.md`](docs/code_walkthrough.md).
- Tools from the lecture (p. 22): Python, pandas, scikit-learn, matplotlib, Jupyter.
- Questions: comment on the issue.
