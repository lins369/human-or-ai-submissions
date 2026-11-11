# Course-package verification

Automated checks performed during the November 11, 2026 packaging pass:

- The 10 existing shared data/split/prediction contract tests passed.
- The original training-file hash and committed 8,000/2,000 split IDs passed
  `python -m human_ai.prepare_data`.
- Every version pinned in `requirements-final.txt` matched the executing
  Python 3.11.15 neural environment.
- The independent `train.py` entrypoint completed a CPU smoke run with six
  balanced training examples, eight validation examples, and one epoch. Six
  examples exercise the partial gradient-accumulation update.
- Saving and loading that model reproduced all eight validation probabilities
  exactly (maximum absolute difference 0.0).
- `predict.py` preserved the first eight original test IDs in a preview run.
- The `--full-data` training branch completed a separate CPU smoke run with six
  balanced examples and the default two epochs, without validation scoring.
- The reloaded smoke model generated predictions for all 3,000 original test
  rows. `human_ai.check_predictions --kind submission` confirmed the required
  `id,label` schema, unique original IDs, and finite probabilities in [0, 1].
- All 24 imported development commits retained their original identities,
  timestamps, messages, and development topology. Every changed path relative
  to the course base is under `submissions/group-number-28/`.
- Q2/Q4 notebook cell sources match the supplied team version. Its saved
  outputs and execution counts were cleared throughout the imported history.

The smoke models and generated CSVs are ignored local artifacts. These checks
verify the entrypoint and serialization pipeline; the six-example fits are not
competition models or reported scientific results.

The pinned public checkpoint was loaded from the existing local cache. A new
virtual-environment installation, complete 8,000/10,000-example refits, GPU
execution of the new entrypoints, cross-device agreement, and reruns of the
historical experiments were not performed during this packaging pass. Historical
scores retain the provenance recorded in the original experiment archives.
