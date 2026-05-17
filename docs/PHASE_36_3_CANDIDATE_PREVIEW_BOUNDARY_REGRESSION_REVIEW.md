# Phase 36.3 Candidate Preview Boundary Regression Review

Phase 36.3 reviews the Phase 36.2 candidate preview runtime implementation and confirms it stayed inside the approved boundary.

This phase does not add new runtime behavior, does not modify `lima/`, and does not modify `tests/support/`.

## Phase 36.2 Boundary Result

Phase 36.2 changed only approved runtime files:

- `lima/kernel/candidate_preview.py`
- `lima/kernel/__init__.py` for safe public export

It did not change:

- `lima/kernel/runtime_state.py`
- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`
- any other existing `lima/` file
- `tests/support/`

## Candidate Preview Safety Evidence

The implementation remains:

- deterministic
- local-only
- read-only
- non-authoritative
- non-executing
- side-effect free
- caller-provided-data only
- safe by default

Acceptance tests cover benign input, missing input, malformed input, unknown values, suspicious values, nested suspicious metadata, bypass wording, explicit authority flags, and static forbidden-import/call checks.

## Stale Phase 35 Test Adjustment

One stale prior-phase test was adjusted:

- `tests/test_phase_35_1_second_runtime_slice_candidate_inventory.py`

Reason: Phase 35 correctly asserted that `candidate_preview.py` was only a possible future Phase 36 file scope and not approved or implemented in Phase 35. After Phil explicitly approved Phase 36, the old absolute non-existence assertion became stale.

No other old phase tests were adjusted.

## Continue

Continue only to Phase 36.4 runtime slice archive and closeout.
