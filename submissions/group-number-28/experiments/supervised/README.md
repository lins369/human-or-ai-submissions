# Supervised comparisons and controlled improvements — Q1, Q5

Owner: A (Lin). This directory is intentionally independent of the other tracks.
Add your runnable training scripts, configurations, and exact tested dependencies.
Use `human_ai.load_partitions` via `from human_ai.data import load_partitions`.
Write run artifacts to `results/supervised/<run_id>/`, following
`docs/experiment_contract.md`. This scaffold supplies no trained model or scores.

Suggested starting experiments: word TF-IDF + Logistic Regression, Naive Bayes,
and calibrated linear SVM. For Q5, fix classifier/hyperparameters and compare word,
character, and combined features. Treat the value of character features as a
hypothesis until measured. Record actual candidate grids for >=2 approaches.

