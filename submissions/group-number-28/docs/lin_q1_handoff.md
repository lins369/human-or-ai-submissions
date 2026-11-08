# Lin Q1 handoff

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
  and Q5 character-feature experiments have not been performed.
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

Open questions include character-feature gains, near-duplicate/source leakage,
cross-machine reproduction and hidden-test generalization. A minimal Q5 study
could fix a recorded LR or SVM configuration and the canonical split, changing
only word/character/combined representations. Collect AUROC, paired intervals,
runtime and feature counts. This is a proposed experiment, not a measured result.
