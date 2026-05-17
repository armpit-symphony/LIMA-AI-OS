# Phase 37.0 Phase 36 Candidate Preview Audit Charter

Phase 37.0 opens the docs/tests/fixtures-only audit/archive lane for the completed Phase 36 candidate preview runtime slice.

This phase does not add runtime behavior, does not modify `lima/`, does not modify `tests/support/`, and does not change any stale prior-phase tests.

## Phase 36 Audit Result

Phase 36.0 through Phase 36.4 passed audit.

The audit verified:

- `main` was clean and synced with `origin/main`.
- Phase 36 merge commits and tags exist.
- `lima/kernel/candidate_preview.py` was added only as the approved Phase 36 runtime slice.
- `lima/kernel/__init__.py` changed only for safe public export.
- `lima/kernel/runtime_state.py` did not change.
- `lima/kernel/intake_candidate.py` did not change.
- `lima/kernel/candidate_status.py` did not change.
- No other forbidden `lima/` files changed.
- `tests/support/` did not change.
- The stale Phase 35 test adjustment was limited to `tests/test_phase_35_1_second_runtime_slice_candidate_inventory.py`.
- No other pre-Phase-36 old phase tests changed.
- No Sparkbot wiring/imports were added.
- No HumanInput runtime bridge behavior was added.
- No live adapter was added.
- No IntentCompiler or GuardianDecision runtime behavior changed.
- No approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external service call, background worker, queue, daemon, subprocess, thread, database write, or hidden side effect was added.
- Phase 36 targeted tests passed.
- The full suite passed.
- `python -m compileall lima` passed.
- `git diff --check` passed.

## Phase 37 Purpose

Phase 37 will audit and archive the Phase 36 candidate preview runtime slice, record safety evidence, identify any remaining gap, and recommend the safest next lane.

## Continue

Continue only to Phase 37.1 candidate preview boundary evidence review.
