# kaggle_ai_vs_human — Cornell Tech (2026)

Private team repository: https://github.com/lins369/kaggle_ai_vs_human

Team workspace scaffold for three independent experiment tracks and a shared,
reproducible evaluation protocol. **The initial Q1 comparison is now archived:** three tuned models, honest held-out results, and a full-data candidate. See `experiments/supervised/README.md` and `docs/development_history.md`.

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
report/sections/           Report stubs organized by question Q0–Q6
report/figures/            Figures named with question/run identifiers
docs/                     Contracts, ownership, merge and Kaggle workflow
tests/                    Split-integrity and prediction-contract checks
old_rubric.tex            Original supplied template; unchanged
```

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

Final model, environment and prediction commands will be documented after actual
model selection. The team repository is owned by `lins369`; the owner manages
collaborator invitations. Inspect the course repository template before preparing
the required final course PR. See `docs/team_workflow.md`.
