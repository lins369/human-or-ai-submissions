# Learning curves and generalization — Q2, Q4

Owner: B. Build your own baseline directly from original data and canonical IDs;
do not wait on A's model. Add runnable scripts, configs and tested dependencies.
Write outputs to `results/generalization/<run_id>/`.

Q2: fixed model/settings, five required sizes, same held-out partition.
Q4: create a reusable evaluator taking `id,label,p_ai`, producing train/validation
gap, >=3 observable subgroups, and >=5 FP / >=5 FN. State error threshold and
do not claim inferred domains/generators as ground truth. Initially analyze your
own model; update the final report with selected-model predictions at integration.

