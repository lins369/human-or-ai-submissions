# Initial Q1 comparison - retrospective archive

This commit archives completed local baseline experiments with real archive dates; original execution provenance is retained unchanged.


Study: `results/supervised/a_q1_20261107_v1_study/`. The canonical split is
unchanged: 8,000 train (4,000/class), 2,000 validation (1,000/class). All models
use the same 60,000-feature word unigram/bigram TF-IDF representation.

| Model | Selected setting | Mean inner CV AUROC | Train AUROC | Validation AUROC | Fit seconds |
|---|---|---:|---:|---:|---:|
| Logistic regression | C=10 | 0.935842 | 1.000000 | 0.943436 | 1.78 |
| Multinomial Naive Bayes | alpha=0.1 | 0.886528 | 0.992115 | 0.906051 | 1.69 |
| Calibrated linear SVM | C=1 | 0.936043 | 1.000000 | 0.943876 | 5.84 |

Times include features and SVM calibration, exclude inner tuning. These are
single wall-time measurements on macOS ARM64, one CPU thread. Tuning across
all families took 5.44 seconds; final refits took 9.30 seconds combined. No
GPU was used. Peak process RSS was about 632 MiB (cumulative, not per model).

SVM is the current Q1 candidate, but its lead over LR is only 0.000440. The
exploratory paired bootstrap interval [-0.000713, 0.001660] does not establish
superiority. LR remains a faster alternative. NB's lower score is retained as
a negative result. Team-wide final selection remains open after Q3/Q5. No
Kaggle score has been measured or inferred from validation AUROC.

## Reproduction from repository root

Tested: **Python 3.12.7** with exact versions in `requirements.txt`. Use Python
3.12 for the pinned NumPy 1.26.4 environment; this machine's default Python
3.13 is not the modeling environment. Shared data utilities remain standard-library-only.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r experiments/supervised/requirements.txt
.venv/bin/python -m human_ai.prepare_data
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m unittest experiments.supervised.test_q1 -v
.venv/bin/python -m experiments.supervised.run_q1 --prefix a_q1_reproduction_001
.venv/bin/python -m experiments.supervised.verify_q1 --prefix a_q1_reproduction_001 --output results/supervised/a_q1_reproduction_001_verification.json --refit
```

This machine executed the scripts with `/opt/anaconda3/bin/python`. The original
prefix is `a_q1_20261107_v1`. Use **new** prefixes and outputs for reruns; evidence
is never overwritten. The original selected candidate has already been generated:

```sh
.venv/bin/python -m experiments.supervised.predict --run-id a_q1_20261107_v1_svm --refit-all --output submissions/a_q1_20261107_v1_svm_full10000.csv
.venv/bin/python -m human_ai.check_predictions submissions/a_q1_20261107_v1_svm_full10000.csv --kind submission
```

For a fresh reproduction, substitute its selected run ID and a new output path.
`--refit-all` fits selected settings to all 10,000 supplied labeled rows, without
a new search or holdout estimate. Omit it to predict from a saved 8,000-row model
to a new CSV. Models are ignored `model.joblib` files; regenerate after cloning.
Scripts never upload to Kaggle or consume submission slots.

## Controlled protocol and interpretation

The plan in `q1_plan.json` was fixed before measuring validation scores:

- LR: C in {0.1, 1, 10}; L2, liblinear, tolerance 1e-5, max_iter 2000.
- Multinomial NB: alpha in {0.01, 0.1, 1}; force_alpha=True.
- Linear SVM: C in {0.1, 1, 10}; L2, dual='auto', tolerance 1e-5, max_iter 10000.

All three approaches are tuned with identical three-fold stratified splits
(seed 142), wholly within the 8,000 training IDs. Vocabulary/IDF are refit on
each inner training fold. Within a fold, identical features are reused across
classifiers to save time. All 27 candidate-fold scores and nine CV summaries
are retained. LR's best C is at the grid boundary; no global optimum is claimed.
No adaptive grid expansion followed the held-out comparison.

SVM tuning uses decision-score AUROC; probability calibration follows C selection.
The **entire TF-IDF + SVM pipeline** is inside CalibratedClassifierCV, preventing
calibration-fold vocabulary/IDF leakage. Calibration uses training-only folds
(seed 242), sigmoid, ensemble=False: one final full-training base estimator,
with the sigmoid learned from out-of-fold margins. Model seed is 42.

The common 2,000-row validation set compares the three selected families. It
is therefore a model-selection set, not an untouched estimate after selection.
Paired bootstrap uses 1,000 class-stratified replicates and seed 342. Intervals
condition on fitted models/split, omit training variability and selection
adjustment, and do not establish hidden-domain or hidden-generator performance.
Near-duplicate/source leakage remains unassessed; the existing split audit only
excludes exact whitespace-normalized duplicates. No test/unlabeled/starter data
or leaderboard feedback is used for fitting or selection.

NB is worse here, which does not establish that all NB variants are poor. Its
independence assumptions and correlated unigram/bigram features are possible
explanations, not tested causes. LR/SVM's train AUROC 1.0 versus validation about
0.944 suggests a generalization gap. Q5 will test character features while
holding classifier/settings fixed; this hypothesis has not yet been measured.

## Evidence and integration

- Study bundle: frozen source/plan, versions, Git commit and dirty state, split
  hashes, exact fitting IDs, inner-fold IDs, CV scores, comparison, bootstrap.
- `..._lr`, `..._nb`, `..._svm`: all estimator parameters, metrics, local model,
  and checked `id,label,p_ai` validation predictions.
- `..._svm_full10000`: separate training ID order/settings, training-only
  diagnostics, fit time and local model; **no held-out score**.
- `..._verification.json`: source/fold audits, CSV metric reconstruction,
  reload and fresh-refit checks. All validation probabilities matched exactly.
- `report/sections/q1.tex`: English Q1.1-Q1.4; `output/pdf/q1_results_initial_3models.pdf`: review copy.
- `report/figures/q1_*.png`: comparison and CV-grid figures, regenerated with
  `python -m experiments.supervised.plot_q1 --prefix a_q1_20261107_v1`.
- `docs/lin_q1_handoff.md`: team transfer and honest AI-use notes.

Alex can use `..._svm/validation_predictions.csv` for Q4 independently. If team
selection changes, update Q4 and Q1.4. Gabriel can use the commands/versions
for clean-environment reproduction; that cross-environment check is still pending.

