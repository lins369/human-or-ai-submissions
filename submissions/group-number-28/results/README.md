# Recorded results

One immutable folder per actual run: `<track>/<run_id>/`.
See `docs/experiment_contract.md` for schemas. Q1 now has recorded evidence under
`supervised/a_q1_20261107_v1_*`; see the supervised-track README. Commit small evidence artifacts, not model
binaries or full passages. Avoid a shared mutable results spreadsheet/file.

Current expanded comparison: `supervised/a_q1_expanded_20261108_v2_*`.
The study contains 64 configurations / 192 fold fits across seven classifier
families and one representation control. Eight model runs retain held-out
predictions; a separate full-data SVM produces the current candidate CSV.
The verification JSON checks all selected settings, stored scores and exact
fresh-refit reproduction. Initial v1 artifacts remain unchanged.

