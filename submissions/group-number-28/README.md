# kaggle_ai_vs_human — Cornell Tech (2026)

Private team repository: https://github.com/lins369/kaggle_ai_vs_human

Team workspace for three independent experiment tracks and shared evaluation.
**Q1 and Q5 are complete locally:** Q1 covers seven classifier families plus a
representation control and 64 searched settings. The separate frozen Q5 study
improves validation AUROC from 0.943876 (word SVM) to 0.970006 (word + character
SVM). A separate full-10,000-label Q5 candidate is now available at
`submissions/a_q5_20261108_v1_wc120_full10000.csv`, with validated test IDs and
probabilities. The scripts have not uploaded it to Kaggle. Team-wide final
selection and other questions remain in progress. See
`experiments/supervised/README.md` for results and reproduction commands.

A separate six-configuration C60/WC120 regularization follow-up selected the
original C=1 for both representations. It produced no replacement candidate;
the existing Q5 submission remains the incumbent. Measured quote/dash
sensitivity and the negative tuning result are retained for error analysis.

The later quote-canonicalization study, `a_q5_quotes_20261108_v3_study`,
completed 12 CV fits and two normalized 8,000-row models. WC120 improves from
0.967153 to 0.968675 on the quote-change condition while its original-text
AUROC decreases from 0.970006 to 0.968675. A separately refit candidate is
available at `submissions/a_q5_quotes_20261108_v3_wc120_norm_full10000.csv`,
classified as an **exploratory robustness tradeoff**, not an established overall
improvement. It has 3,000 verified predictions and no recorded Kaggle score;
the original WC120 public score of 0.87399 remains the incumbent. Its companion
metadata records checksums, the full-label refit and the exact source study.

The four-group length/richness study, `a_q5_richness_20261108_v4_study`,
retains the original split, character features, C=1 and calibration. Validation
AUROCs are 0.969550 (characters), 0.969825 (+length), 0.974508 (+richness),
and 0.974838 (+length+richness). The primary increment from richness after
explicit length adjustment is +0.005013, conditional paired 95% interval
[+0.00200635, +0.008241825], with positive gains in all three training folds.
The training-CV-selected character+richness model exceeds the old WC120
validation score by 0.004502. These are development findings, not new public
scores; the public-0.87399 submission remains the incumbent. Export eligibility
and execution receipts are recorded separately in the study artifacts. One
eligible full-10,000-label refit produced
`submissions/a_q5_richness_20261108_v4_c60_richness_full10000.csv` with 3,000
checked probabilities and exact model-reload agreement. That refit has no
held-out evaluation and has not been uploaded to Kaggle.

## Quick start

Data utilities require Python >=3.11 and no third-party packages.

1. Obtain the five original competition CSVs and put them in `data/raw/`.
   The existing competition-named local directory is also supported, unchanged.
2. From this repository root run:

   ```sh
   python3 -m human_ai.prepare_data
   python3 -m unittest discover -s tests -v
   ```

3. Read `docs/experiment_contract.md`, then start in your experiment directory.
   Add modeling dependencies with exact tested versions when you run experiments.

Preparation verifies the committed 8,000/2,000 stratified split and creates local
raw-text CSVs under `data/processed/`. Git tracks IDs and hashes, not passages.
It never silently overwrites canonical split files. Use the held-out partition
for comparisons; only after selection may final training use all 10,000 labels.

## Layout

```text
data/raw/                  Original CSVs; ignored by Git
data/splits/               Committed train/validation IDs + source/split hashes
data/processed/            Recreated train/validation CSVs; ignored by Git
human_ai/                  Shared split loading, preparation, prediction checks
experiments/supervised/    A: Q1 model comparisons + Q5 improvements
experiments/generalization/ B: Q2 learning curves + Q4 error analysis
experiments/semisupervised/ C: Q3 unlabeled learning
results/<track>/<run_id>/  Per-run config, metrics, validation predictions
submissions/               Candidate test predictions + actual upload log
report/figures/            Experiment figures named with question/run identifiers
docs/                     Contracts, ownership, merge and Kaggle workflow
tests/                    Split-integrity and prediction-contract checks
old_rubric.tex            Original supplied template; unchanged
```

Report prose and the final PDF are maintained separately in Overleaf. Do not
generate or upload local report sections, report build entrypoints, or PDFs.
Use the recorded experiment code/results to support later Overleaf writing.

## Integrating independently developed work

Share only input IDs and output contracts; models do not need the same classes.
Each member must be able to train and export predictions independently. Combine
predictions by ID, never by row position. Use small PRs and preserve meaningful
intermediate commits. C coordinates final reproducibility/README; each member
writes their own report sections and contribution/AI-use notes.

Validation output: `id,label,p_ai` (true label plus AI probability). Kaggle output:
`id,label` (label column contains AI probability). Verify both with:

```sh
python3 -m human_ai.check_predictions PATH --kind validation
python3 -m human_ai.check_predictions PATH --kind submission
```

Q1 dependencies and prediction commands are in the supervised-track README;
team-wide final environment/pipeline remain to be integrated.
The team repository is owned by `lins369`; the owner manages
collaborator invitations. Inspect the course repository template before preparing
the required final course PR. See `docs/team_workflow.md`.
