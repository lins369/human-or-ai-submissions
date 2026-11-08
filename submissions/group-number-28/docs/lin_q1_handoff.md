# Lin Q1 handoff

## Q5 update (November 8)

The prospectively frozen four-condition Q5 study is complete locally:
`a_q5_20261108_v1_study`. SVM C=1, the canonical split and calibration protocol
are unchanged. No adaptive parameter search followed the scores.

- W60 baseline: 0.943876; C60 characters: 0.969550; WC120 combination: 0.970006;
  W120 larger word vocabulary: 0.944597. All four train AUROCs are 1.0.
- Primary WC120 minus W60: +0.026130, conditional paired interval
  [+0.020083, +0.031971]; all three training-only CV folds agree in direction.
  W60 exactly reproduces Q1 probabilities. WC120 is only 0.000456 above C60;
  the combination has not been established as superior to character-only.
- At threshold 0.5, 107 old errors are corrected and 34 new errors appear;
  total validation errors fall from 258 to 185. Length-bin results and changed
  IDs/probabilities are recorded; causal failure explanations await review.
- WC120 is the leading Q5 development candidate; final team selection is open.
  If adopted, Alex's Q4 input becomes
  `results/supervised/a_q5_20261108_v1_wc120/validation_predictions.csv`.
  The old Q1 held-out file below remains valid for that historical model.
- Four Q5 tests and ten shared tests passed. Reloaded predictions exactly match
  for all four models, and the primary bootstrap interval was independently
  reconstructed from saved probabilities. Clean-environment/cross-machine
  reproduction by Gabriel remains pending.
- The detached local job completed training, verification and plotting in
  about 159.26 seconds without interruption. Checkpoints can resume identical
  unfinished steps; no external model/API service was used for training.
- No all-10,000-label Q5 fit, test predictions, or Kaggle upload occurred. The
  existing word-only submission must not be described as a character candidate.
- These are development-validation results, not private/public Kaggle scores.
  Conditional intervals omit training variation and selection adjustment;
  source shortcuts and near-duplicate leakage remain unassessed.
- Codex assisted with Q5 design, implementation, execution, automated checks,
  interpretation and plotting. Lin's personal verification is not claimed;
  review the code/results and update the AI-use disclosure with actual checks.

## Current expanded study (November 8)

Q1 now covers LR, NB, SVM, decision trees, random forests, gradient boosting,
and an MLP neural network, plus an SVD LR representation control. The search
completed 64 configurations and 192 candidate-fold fits. Parameters were
selected using training-only coarse search and one predeclared refinement.
Full settings and results are in `experiments/supervised/README.md` and
`a_q1_expanded_20261108_v2_study`.

- SVM C=1 remains the provisional candidate: validation AUROC 0.943876.
  Retuned LR uses C=33.33333333333333 and achieves 0.943699.
- Decision tree: 0.812888; random forest: 0.936392; boosting: 0.939490;
  MLP: 0.939616.
- The first five models use sparse TF-IDF. Boosting uses SVD-128; MLP uses
  SVD-128 plus scaling. The scaled SVD LR control achieves 0.922601, so all
  differences cannot be attributed to the classifier alone.
- MLP seeds 7/142 achieve 0.936834/0.940165. The preselected seed 42 remains
  the primary result; the best seed was not selected after evaluation.
- Alex's current Q4 input is
  `results/supervised/a_q1_expanded_20261108_v2_svm/validation_predictions.csv`.
  SVM settings are unchanged; these predictions are byte-identical to v1.
- All eight models were refit in fresh instances and exactly reproduced their
  saved validation probabilities. Three additional representation/search/leakage
  tests passed, with zero model convergence warnings. Gabriel's independent
  clean-environment and cross-machine reproduction remains pending.
- Current full-data candidate:
  `submissions/a_q1_expanded_20261108_v2_svm_full10000.csv`.
  Its SHA-256 matches the initial candidate because the selected SVM is
  unchanged. A duplicate upload would consume a Kaggle slot without new evidence.
- Report writing is handled separately in Overleaf. Local report prose, TeX
  sources, build entrypoints and PDFs are excluded from this code PR. Exact
  search details remain in the study's JSON/CSV files for later writing.
- "Best" means best among tested settings, not globally optimal. Validation
  had already been inspected in v1; this is a development comparison. Bootstrap
  intervals are not selection-adjusted. No Kaggle scores informed selection,
  and Q5 was not part of this Q1 study. The later Q5 results are recorded above.
- AI also assisted with the added models, search, representation control, seed
  stability and updated report. Lin should review the disclosure below against
  Lin's actual verification; no personal team-member checks are claimed.

## Initial three-model study (historical record)

Q1.1-Q1.4 have measured experiments to support later Overleaf writing. Ownership is Lin:
Q1/Q5; Alex: Q2/Q4; Gabriel: Q3/Q6. This work did not perform Q5 or change raw
data, the canonical split, or teammates' experiment/report files.

### Results and handoff

- Initial SVM C=1: validation AUROC 0.943876; training AUROC 1.0; validation
  accuracy at threshold 0.5 is 0.871.
- LR C=10: 0.943436. Its 0.000440 gap to SVM has a paired interval crossing
  zero, so clear superiority is not established.
- NB alpha=0.1: 0.906051. This negative result uses the same features/split;
  it does not establish that every NB variant performs poorly.
- These scores use the fixed 8,000/2,000 split, not Kaggle public/private data.
- Alex's initial Q4 input is
  `results/supervised/a_q1_20261107_v1_svm/validation_predictions.csv`:
  2,000 rows, `id,label,p_ai`. Align by ID and state the error-analysis threshold.
  Update Q4 if team-wide selection changes; Q2 may retain its own fixed baseline.
- `..._svm_full10000/` includes the former validation labels and cannot provide
  an honest Q4 held-out evaluation.
- Gabriel's commands and exact dependencies are in
  `experiments/supervised/README.md`; tested Python is 3.12.7. Ten shared
  contract tests and four initial modeling tests passed. Fresh instances of
  all three models reproduced validation probabilities exactly in the existing
  environment; independent clean-environment/cross-machine checks remain pending.

### Initial local candidate

`submissions/a_q1_20261107_v1_svm_full10000.csv` contains 3,000 probabilities
after full-data refitting with selected Q1 settings. The checked schema is
`id,label`, where `label` is the AI probability. Metadata records provenance
and the CSV hash. No Kaggle upload, submission-slot use, or leaderboard score
was recorded. Team-wide final selection awaits Q3/Q5 evidence.

## Reproduction and development records

Experiments ran from scaffold commit
`17aba0e1f0c7b87fa597b4afb53e0cf8db61b2f9` with uncommitted changes. The actual
dirty state and executed-source hashes are retained, with source snapshots in
each study. The subsequent real archive commits are documented in
`docs/development_history.md`; no execution-time commits were fabricated.
Raw passages and model weights are excluded from Git.

The original local `old_rubric.tex` is unchanged. Q1 follows its criteria and
the supplied Project Expectations, but the latest template, final grading
threshold and deadline have not been independently verified.

## AI-use disclosure draft for Lin to review

Codex assisted with experimental design, Python implementation, execution,
automated verification, interpretation, plots, and the English Q1 draft. The
assistant checked source/split hashes, fold-local feature fitting, calibration
boundaries, probability/schema correctness, metric reconstruction and fresh
refits. Team members' personal review has not been observed or claimed. Lin
should review the implementation and explanations and record the checks Lin
personally performed or modified before adapting this disclosure for Q6.3.
Local sklearn models generated predictions; no external LLM API labeled
competition passages, and no hidden test labels were obtained.

## Decisions and unresolved hypotheses

Compare classifiers with matched representations, tune within training data,
compare families on the fixed validation set, and retain negative results.
Tracks run independently and exchange predictions by ID to reduce dependencies.
SVM has the nominal best score; LR is faster and the difference is unresolved.

The later Q5 study above now measures character-feature gains under the fixed
SVM protocol, including a larger-word-vocabulary resource reference. The added
value of combining words with characters over characters alone, near-duplicate/
source leakage, independent reproduction and hidden-test generalization remain
open. No extra search is needed to complete the four-condition Q5 study.
