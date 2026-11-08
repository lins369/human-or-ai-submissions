# Supervised comparisons and controlled improvements — Q1, Q5

Owner: Lin (A). **Q1 and the frozen Q5 feature ablation are measured locally.**
Alex owns Q2/Q4; Gabriel owns Q3/Q6 integration.

## Q5 character-feature ablation (November 8)

Study: `a_q5_20261108_v1_study`. This is a separate, prospectively frozen
four-configuration study, not an extension of the Q1 classifier grid. All
models retain SVM C=1, the canonical 8,000/2,000 split, and the Q1 sigmoid
calibration protocol. No C, character range, feature weight, or classifier
search was added after observing Q5 scores.

| Configuration | Actual features | Mean training-only 3-fold AUROC | Validation AUROC | Full fit seconds |
|---|---:|---:|---:|---:|
| W60: original word (1,2) baseline | 60,000 | 0.936043 | 0.943876 | 5.28 |
| C60: character (3,5) | 60,000 | 0.963434 | 0.969550 | 27.43 |
| WC120: word + character | 120,000 | 0.964381 | **0.970006** | 33.66 |
| W120: larger word vocabulary reference | 120,000 | 0.936876 | 0.944597 | 5.47 |

All four training AUROCs are 1.0. Timings are measured in the existing Python
3.12.7/pinned environment, with one CPU thread; they include feature fitting
and calibration, excluding diagnostic CV. Each combination block has unit L2
norm; equal-weight concatenation is normalized again. W60 uses the original
single vectorizer without an extra normalization pass and exactly reproduces
all Q1 validation probabilities (maximum absolute error 0).

The predeclared primary difference WC120 minus W60 is **+0.026130**, with a
1,000-replicate paired stratified bootstrap interval **[+0.020083, +0.031971]**.
WC120 improves raw-margin AUROC over W60 in all three training-only folds.
The W120 difference is +0.000721, interval [-0.000562, +0.001859]; merely
doubling the word feature budget does not reproduce the observed character
gain in this study. This resource reference does not strictly isolate model
capacity. C60 already captures most of the gain: WC120 is only 0.000456 above
C60 on validation, so superiority of the combination over character-only
features has not been established.

At threshold 0.5, WC120 corrects 107 W60 errors and introduces 34 new ones,
reducing total errors from 258 to 185 (accuracy 0.8710 to 0.9075). Descriptive
length bins were fixed from training-only word-count tertiles, at 174 and
240 words. WC120 improves over W60 in all three bins. Changed-error IDs and
probabilities are saved without passage text; passage-level causal hypotheses
still require human review.

The four saved models reproduce their recorded probabilities exactly after
reload. Source/split/fold hashes, CV summaries, calibration and normalization
boundaries, the primary interval, and error-change counts passed verification.
Four Q5 tests and ten shared contract tests passed. This is verification in the
existing environment, not an independent clean-environment reproduction.

Training/evaluation/bootstrap took 146.05 seconds; the detached job including
verification and plotting completed in about 159.26 seconds without interruption.
Atomic per-fold/per-model checkpoints and a process lock permit identical
unfinished studies to resume. The local worker calls no model/API service.
Its log is `tmp/a_q5_20261108_v1.log`; job state is
`tmp/a_q5_20261108_v1_job.json`. These operational files are ignored by Git.

Fresh reproduction, using a NEW prefix:

```sh
.venv/bin/python -m unittest experiments.supervised.test_q5 -v
.venv/bin/python -m experiments.supervised.q5_job --prefix a_q5_reproduction_001
```

Use `--resume` with the same prefix only after an interrupted identical run.
Resume rejects changed training source, plan, environment or split and reuses
completed folds/models. `q5_job` runs training, saved-artifact verification and
plotting sequentially. It does not upload or fit on all 10,000 labels.
For a separate audit, use a new output path:

```sh
.venv/bin/python -m experiments.supervised.verify_q5 --prefix a_q5_20261108_v1 --output results/supervised/a_q5_20261108_v1_additional_verification.json
.venv/bin/python -m experiments.supervised.plot_q5 --prefix a_q5_20261108_v1
```

Evidence includes `q5_plan.json`, `cv_progress.json`, `cv_results.csv`,
`comparison.csv`, `bootstrap.json`, `baseline_gate.json`, `changed_errors.csv`,
`error_change_summary.json`, and `length_subgroups.csv` in the study directory;
each model has its own config/metrics/predictions/checksum receipt. The figure
is `report/figures/q5_a_q5_20261108_v1_comparison.png`.

WC120 is the leading Q5 development candidate; C60 is a lower-dimensional
alternative. Final team selection remains open. If selected, Alex should use
`results/supervised/a_q5_20261108_v1_wc120/validation_predictions.csv` for Q4.
No new full-data checkpoint, test prediction file, or Kaggle upload was created.
The earlier word-only submission is unchanged.

The validation set already informed Q1 development. All intervals condition
on this split and fitted models, omit training variability and selection
adjustment, and do not establish hidden-domain/test-set gains. Character
features could also encode source shortcuts; near-duplicate/source leakage
remains unassessed. Report prose continues to be maintained in Overleaf.

## Expanded Q1 (current, November 8)

Study: `a_q1_expanded_20261108_v2_study`. Seven classifier families plus a
representation control, **64 distinct settings / 192 candidate-fold fits**.
All parameter choices use three training-only folds, a coarse search and one
predeclared refinement. The original 8,000/2,000 split and original v1 evidence
are unchanged. Settings are best among those actually tested, not global optima.

| Model | Representation | Best tested settings | Validation AUROC | Fit seconds |
|---|---|---|---:|---:|
| Logistic regression | TF-IDF | C=33.33333333333333 | 0.943699 | 1.98 |
| Multinomial NB | TF-IDF | alpha=0.3 | 0.905623 | 1.75 |
| Calibrated linear SVM | TF-IDF | C=1 | **0.943876** | 6.08 |
| Decision tree | TF-IDF | depth=15; min leaf=20 | 0.812888 | 2.76 |
| Random forest | TF-IDF | 400 trees; unlimited depth; max_features=0.02; min leaf=1 | 0.936392 | 35.37 |
| Histogram gradient boosting | SVD-128 | 300 rounds; rate=0.1; 15 leaves; L2=0 | 0.939490 | 5.43 |
| Neural network / MLP | SVD-128 + scaling | hidden=(128,); alpha=0.0001; rate=0.003 | 0.939616 | 4.76 |
| LR representation control | SVD-128 + scaling | C=0.3 | 0.922601 | 4.18 |

TF-IDF settings are unchanged from v1. SVD (128 components, 7 power iterations,
seed 42) and StandardScaler are fitted only on each applicable training fold.
The scaled SVD LR control and MLP share a representation; boosted trees use
the same SVD components without scaling. Comparisons with sparse models also
change representation, so they do not isolate the classifier alone.

All timings include full feature fitting and any calibration, not parameter
search. The expanded search took 223.10 s; search plus eight final fits and
evaluation took 297.47 s before bootstrap/secondary-seed checks. Peak process
RSS was about 965 MiB (cumulative high-water mark, not isolated model memory).
All runs used one CPU thread; no GPU or external weights were needed.

Word-only SVM remains the Q1 candidate; the separate Q5 candidate is above.
Its lead over retuned LR is just 0.000177,
paired conditional bootstrap interval [-0.000468, 0.000794]. LR is a faster
alternative, and the difference is unresolved. All intervals omit training
variation and model-selection correction. The original validation set was
already inspected in v1: this extension is a development comparison, not an
untouched final estimate. No expanded choice used Kaggle feedback.

MLP uses ReLU/Adam, at most 500 epochs, internal 10% stratified stopping data,
patience 20, tolerance 1e-4; stopping monitors accuracy. Feature transforms use
all fitting rows, while gradient updates use 90%; its training diagnostic
includes the internal stopping rows. Selected primary MLP stopped after 27
epochs. Seeds 42/7/142 yield validation AUROCs 0.939616/0.936834/0.940165;
seed 42 remains primary, without selecting the best seed. No candidate fit
had a convergence warning. One physical-core detection warning was recorded;
threadpool limits remained one. The original logger also emits a NumPy
deprecation warning when recording scalar iteration counts; pinned versions
completed correctly and all eight refits reproduced predictions exactly.

For new reproduction, using the Python 3.12 environment described below:

```sh
.venv/bin/python -m unittest experiments.supervised.test_expanded_q1 -v
.venv/bin/python -m experiments.supervised.expanded_q1 --prefix a_q1_expanded_reproduction_001
.venv/bin/python -m experiments.supervised.verify_expanded_q1 --prefix a_q1_expanded_reproduction_001 --output results/supervised/a_q1_expanded_reproduction_001_verification.json --refit
.venv/bin/python -m experiments.supervised.export_expanded_q1 --prefix a_q1_expanded_reproduction_001 --output submissions/a_q1_expanded_reproduction_001.csv
```

Original expanded candidate (already generated, so do not overwrite):
`submissions/a_q1_expanded_20261108_v2_svm_full10000.csv`. Its selected settings
were refit on all 10,000 supplied labels and its 3,000 test probabilities pass
the CSV checker and saved-model reload check. It was not uploaded to Kaggle.

Reports are written separately in Overleaf. Report prose, TeX sources, build
entrypoints and PDFs are not part of this code PR. The actual grids and
refinements remain in the study's JSON/CSV evidence. To regenerate only the
experiment figures:

```sh
.venv/bin/python -m experiments.supervised.plot_expanded_q1 --prefix a_q1_expanded_20261108_v2
```

Use the expanded study's `cv_results.json` / `cv_results.csv` for every exact
parameter combination, `cv_progress.json` for all fold scores and stopping
iterations, `chosen_parameters.json` for selections, `bootstrap.json` for
uncertainty, and `mlp_secondary_seeds.json` for stability. Each of the eight
run directories contains parameters, source/split provenance, metrics and
canonical 2,000-row validation predictions. The audit confirms all eight fresh
refits match saved probabilities exactly in this environment. Cross-machine
or clean-environment reproduction remains pending.

The single tree is a clear negative result here. The forest improves greatly
over it, but costs 35.37 s without beating SVM. Boosting/MLP beat the SVD LR
control while trailing sparse LR/SVM nominally; nonlinear modeling helps this
representation, while information discarded by compression is a plausible
limitation. These results do not establish that other tree, ensemble, or neural
representations would fail. Forest tree count and boosting rounds remain at
the largest values tested, so further resource/performance trade-offs are open.

## Initial v1 results and protocol (historical record)

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
0.944 suggests a generalization gap. Character features were still an unmeasured
hypothesis at this Q1 stage; the separate Q5 study above now tests them while
holding classifier/settings fixed.

## Evidence and integration

- Study bundle: frozen source/plan, versions, Git commit and dirty state, split
  hashes, exact fitting IDs, inner-fold IDs, CV scores, comparison, bootstrap.
- `..._lr`, `..._nb`, `..._svm`: all estimator parameters, metrics, local model,
  and checked `id,label,p_ai` validation predictions.
- `..._svm_full10000`: separate training ID order/settings, training-only
  diagnostics, fit time and local model; **no held-out score**.
- `..._verification.json`: source/fold audits, CSV metric reconstruction,
  reload and fresh-refit checks. All validation probabilities matched exactly.
- Report writing is handled separately in Overleaf, using the recorded code/results.
- `report/figures/q1_*.png`: comparison and CV-grid figures, regenerated with
  `python -m experiments.supervised.plot_q1 --prefix a_q1_20261107_v1`.
- `docs/lin_q1_handoff.md`: team transfer and honest AI-use notes.

Alex can use `..._svm/validation_predictions.csv` for Q4 independently. If team
selection changes, update Q4 and Q1.4. Gabriel can use the commands/versions
for clean-environment reproduction; that cross-environment check is still pending.

