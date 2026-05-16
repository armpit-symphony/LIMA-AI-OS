# Phase 20.3 Acceptance Test And Rollback Plan

Phase 20.3 defines future acceptance tests and rollback/audit proof requirements for the candidate provenance hardening slice.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `candidate_status.py` or `intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not approve execution, does not enforce approval, does not dispatch, does not persist audit, and does not add shell, browser, network, file mutation, robotics, or physical-world behavior.

## Future Acceptance Tests

A future explicitly approved Phase 21 runtime slice must provide acceptance tests proving:

- candidate construction rejects missing provenance
- candidate construction rejects empty provenance
- candidate construction rejects non-mapping provenance
- candidate validation marks missing provenance invalid
- candidate validation marks malformed provenance invalid
- status normalization preserves valid provenance
- provenance hardening never changes `executable`, `execution_allowed`, or `side_effects_allowed` to true
- provenance hardening never sets `approval_state` to `approved`
- stale or replayed candidates remain blocked or invalid
- operator/admin/Phil/trusted/urgent/override/approve wording does not bypass safety
- no Sparkbot, HumanInput runtime bridge, live adapter, execution, dispatch, approval enforcement, audit persistence, shell, browser, network, file mutation, robotics, or physical-world behavior is reachable
- only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py` are changed as runtime files

## Rollback And Audit Proof

A future Phase 21 implementation must prove:

- no database migration, queue, worker, daemon, subprocess, thread, external call, or persistence path was added
- rollback is a clean revert of only the eligible runtime files and Phase 21 tests/docs/fixtures
- `git diff --check` passes
- `python -m compileall lima` passes
- all Phase 21 targeted tests pass
- full suite passes
- `git diff --name-only` shows no runtime files outside the Phase 20.2 eligible list
- Phase 5 HumanInput runtime bridge remains gated

## Gate

Phase 20.3 does not approve Phase 21. Phase 20.4 must preserve the exact implementation approval question and close the no-code design lane.
