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

Q5 evidence is in `supervised/a_q5_20261108_v1_*`: four frozen representation
conditions, 12 training-only CV fits, exact reproduction of the old baseline,
four held-out prediction files, paired bootstrap intervals, descriptive error/
length diagnostics, and saved-model verification. WC120 validation AUROC is
0.970006 versus W60 0.943876. This development comparison has no new full-data
submission; final team selection and independent-environment reproduction are
still pending. Original Q1 evidence is unchanged.

