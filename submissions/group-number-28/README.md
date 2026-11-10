# kaggle_ai_vs_human — Cornell Tech (2026)

Private team repository: https://github.com/lins369/kaggle_ai_vs_human

**Latest public result (November 9): RoBERTa reaches 0.96970**, up **0.09571**
from the previous WC120 score of 0.87399, according to the user-supplied Kaggle
screenshot. The submitted file is
[`a_roberta_20261109_v1_raw_full10000.csv`](submissions/a_roberta_20261109_v1_raw_full10000.csv).
It uses the fixed raw-text RoBERTa-base recipe refit on all 10,000 labels, with
all 3,000 test IDs/probabilities and full saved-model reload agreement verified.
See the [score and screenshot](docs/roberta_public_result_20261109.md),
[seven-fit comparison](docs/roberta_context_results_20261109.md) and
[whitespace diagnostic](docs/roberta_prefix_whitespace_results_20261109.md).
Private-score transfer remains unknown; the raw model's format sensitivity is
preserved in the evidence. Neural fitting uses `python_course` on M4 Pro.

The following paragraphs retain the earlier classical-model stages. At the
first public-score review, WC120 led at **0.87399**; quote normalization scored
**0.87225** and C60+richness **0.85812** in the user-supplied screenshot.
Submission integrity checks passed. Paired stress
and data-shift diagnostics, plus a two-fit crop-training pilot, are documented in
[`docs/public_score_research_20261109.md`](docs/public_score_research_20261109.md).
These findings motivate stronger robustness evaluation; higher random-split
development AUROC has not consistently transferred to the public set.

The planned weak-crop follow-up has now completed under its stopping rule.
Six diagnostic random-CV fits measured clean AUROC 0.965186 -> 0.962823 and
prefix AUROC 0.855860 -> 0.906588. Random screening passed, but the frozen
topic proxy failed quality checks; no later fits or candidate export occurred.
See [the execution record](docs/q5_crop_results_20261109.md). That stage retained WC120.

An authorized adaptive continuation converted only the content-topic count and
maximum held-size checks to diagnostics, reusing the exact groups/folds/reviews.
Twelve new fits measured topic clean AUROC 0.932745 -> 0.929526 and prefix
0.816874 -> 0.854561. The unchanged clean-loss budget was narrowly exceeded;
no export occurred. See [the revised results](docs/q5_crop_revised_results_20261109.md).

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
that stage retained the existing Q5 submission. Measured quote/dash
sensitivity and the negative tuning result are retained for error analysis.

The later quote-canonicalization study, `a_q5_quotes_20261108_v3_study`,
completed 12 CV fits and two normalized 8,000-row models. WC120 improves from
0.967153 to 0.968675 on the quote-change condition while its original-text
AUROC decreases from 0.970006 to 0.968675. A separately refit candidate is
available at `submissions/a_q5_quotes_20261108_v3_wc120_norm_full10000.csv`,
classified as an **exploratory robustness tradeoff**, not an established overall
improvement. It has 3,000 verified predictions and public AUROC 0.87225;
the original WC120 public score of 0.87399 led that comparison. Its companion
metadata records checksums, the full-label refit and the exact source study.

The four-group length/richness study, `a_q5_richness_20261108_v4_study`,
retains the original split, character features, C=1 and calibration. Validation
AUROCs are 0.969550 (characters), 0.969825 (+length), 0.974508 (+richness),
and 0.974838 (+length+richness). The primary increment from richness after
explicit length adjustment is +0.005013, conditional paired 95% interval
[+0.00200635, +0.008241825], with positive gains in all three training folds.
The training-CV-selected character+richness model exceeds the old WC120
validation score by 0.004502. These are development findings, not new public
scores; that stage retained the public-0.87399 submission. Export eligibility
and execution receipts are recorded separately in the study artifacts. One
eligible full-10,000-label refit produced
`submissions/a_q5_richness_20261108_v4_c60_richness_full10000.csv` with 3,000
checked probabilities and exact model-reload agreement. That refit has no
local held-out evaluation. The user's later screenshot records public AUROC
0.85812, below WC120. RoBERTa's later 0.96970 result is the current public leader
among the repository's reported submissions.

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
