# Q1 development evidence and archive history

## What this history represents

The baseline and expanded Q1 experiments were completed in the local workspace
before their implementation/results were committed. The commits in this PR
retrospectively archive those completed stages. Their commit dates are the real
archive dates, not the original execution dates; they must not be described as
contemporaneous experiment checkpoints. The original scaffold commit is
`17aba0e1f0c7b87fa597b4afb53e0cf8db61b2f9`.

Run provenance truthfully records the scaffold commit, a dirty working tree,
the UTC execution time, dependency versions, and hashes of the code actually
executed. Study directories also preserve source snapshots. These original
records are not rewritten to point at later archive commits.

## Experimental progression

1. **Baseline:** `a_q1_20261107_v1_study` compares word TF-IDF + LR, NB and
   calibrated SVM. Three candidate values per family, three training-only folds;
   SVM validation AUROC 0.943876, LR 0.943436, NB 0.906051. The small SVM/LR
   difference is unresolved. Vocabulary/IDF and calibration avoid outer holdout
   fitting. A separate 10,000-label SVM creates the local prediction candidate.
2. **Expanded comparison:** `a_q1_expanded_20261108_v2_study` adds decision
   trees, random forests, histogram gradient boosting and an MLP, plus an SVD LR
   representation control. A predeclared coarse search and one local refinement
   evaluate 64 configurations / 192 candidate-fold fits. LR's old grid boundary
   motivates a broader C range; training-only CV selects C=33.33333333333333.
   Dense models fit fold-local SVD/scaling. The same validation set had already
   been inspected, so the expansion is a development comparison, not a fresh test.
3. **Checks and debugging:** tests exercise split/prediction contracts,
   fold-local feature fitting, calibration scope, probability class direction,
   immutable run paths and refinement behavior. A floating-point exact-equality
   assertion in the new refinement test was changed to an approximate assertion;
   this corrected the test without changing model training. The broken test
   state was not committed. The frozen training logger emits a scalar-conversion
   deprecation warning with pinned NumPy; original code/hashes are retained.
   All eight selected expanded models were refit in fresh instances and matched
   their saved validation probabilities exactly in the existing environment.
4. **Selection and handoff:** SVM remains the nominal candidate; retuned LR
   is only 0.000177 behind. Full search tables, conditional bootstrap intervals,
   negative results, MLP seed variability and experiment figures are retained.
   The expanded full-data candidate is byte-identical to the baseline candidate.
   No Kaggle upload or leaderboard-based model selection occurred.

## Evidence index

- `experiments/supervised/README.md`: current results, exact dependencies,
  Python version, training/evaluation/export commands, and limitations.
- `results/supervised/*_study/`: plans, code snapshots, source/split hashes,
  fitting IDs, fold assignments, all candidate scores and selection rationale.
- `results/supervised/*/{config.json,metrics.json,validation_predictions.csv}`:
  actual settings, observed metrics/timing, and probabilities aligned by ID.
- `results/supervised/*_verification.json` and delivery/candidate checks:
  model reloads, fresh refits, metric reconstruction and output-contract checks.
- `report/figures/`: experiment comparison and search figures. Report prose,
  TeX sources, build entrypoints and PDFs are maintained separately in Overleaf
  and are excluded from the current code PR.
- `submissions/*.metadata.json`: candidate provenance and SHA-256; the matching
  small probability CSVs are included, without raw passages or model weights.
- `docs/lin_q1_handoff.md`: team transfer details and AI-use disclosure draft.

## Scope and remaining work

The original archive is an internal Q1 PR in the private team repository. It
is not the final course submission. Q5 has now been measured separately as
described below. Q2-Q4/Q6, team-wide final selection, and a clean-environment
cross-machine reproduction remain to be integrated. Team members' personal
verification is not claimed on their behalf. The final course PR must retain
the substantive archive/development commits when moving into the course fork's
per-team directory; record any old/new commit mapping if that migration changes
commit IDs. Do not squash away this evidence before course review.

Future experiments and fixes should be committed when they happen, with the
hypothesis, measured result and resulting decision recorded alongside the code.

## Subsequent Q5 execution

After the four-condition protocol was discussed and the user authorized its
execution, `a_q5_20261108_v1_study` ran from commit
`2c6f5960fa4f1d5266b8e5321a0c0cf0b18c508e` with the new Q5 files uncommitted.
Its provenance preserves that actual dirty state, exact executing-source
hashes and frozen snapshots. The subsequent real archive commits are
listed below; their dates are archive dates, not earlier execution checkpoints.

- Q5 implementation: [cccc067](https://github.com/lins369/kaggle_ai_vs_human/commit/cccc067bb48e8d35a13447247d13a6b513b12d7f)
- Q5 measured evidence: [784adce](https://github.com/lins369/kaggle_ai_vs_human/commit/784adce0691d0bd8f97dbffb190dd7c4f290f66e)

The fixed SVM/representation comparison records W60 0.943876, C60 0.969550,
WC120 0.970006, and W120 0.944597. The primary WC120-W60 difference is
+0.026130, conditional paired interval [+0.020083, +0.031971]. Training-only
folds agree in direction; the original W60 probabilities reproduce exactly.
Four Q5 tests and ten shared tests passed, and the saved-model/metric/bootstrap
verification passed. The detached local job finished without interruption.
No adaptive grid, new full-data submission, or Kaggle upload was added.
Independent reproduction, hidden-test transfer, source leakage, and the small
WC120-C60 difference remain unresolved. Technical results/commands are in the
supervised README; report prose remains in Overleaf.

## Archive commits in this PR

- baseline: [4696415](https://github.com/lins369/kaggle_ai_vs_human/commit/469641522e434d896d1f6afe3a240ccc664d491a)
- expanded: [0936f15](https://github.com/lins369/kaggle_ai_vs_human/commit/0936f152c7f66d0a897f004a8614ae815fd314e0)
- checks: [7640f1b](https://github.com/lins369/kaggle_ai_vs_human/commit/7640f1b5b0e90176b5b04a123f650a5ff683cbf8)

Consolidated documentation was added in the following documentation commit.
These are real archive commits created after the recorded experiments.
That earlier commit also included local report artifacts; a later scope
correction removes them from the current tree because report writing belongs
in the team's separate Overleaf project. Original execution records and
substantive experiment history remain unchanged. Historical delivery receipts
may retain checksums of those earlier local PDFs; these are historical checks,
not a requirement to include or regenerate reports in the code repository.
