# Phase 36.0 Phase 35 Runtime Implementation Audit Charter

Phase 36.0 opens the explicitly approved narrow runtime implementation lane for Option C from Phase 35: a non-executing, local-only, read-only, non-authoritative candidate preview helper over caller-provided data only.

This phase is preflight audit and charter only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, and does not approve any scope beyond the bounded Phase 36 candidate preview helper.

## Phase 35 Audit Result

Phase 35.0 through Phase 35.4 passed audit.

The audit verified:

- `main` was clean and synced with `origin/main`.
- Phase 35 merge commits and tags exist.
- No runtime files changed in Phase 35.
- `lima/kernel/runtime_state.py` did not change in Phase 35.
- `lima/kernel/__init__.py` did not change in Phase 35.
- `lima/kernel/intake_candidate.py` did not change.
- `lima/kernel/candidate_status.py` did not change.
- No other forbidden `lima/` files changed.
- `tests/support/` did not change.
- No Sparkbot wiring/imports were added.
- No HumanInput runtime bridge behavior was added.
- No live adapter was added.
- No IntentCompiler or GuardianDecision runtime behavior changed.
- No execution, approval enforcement, dispatch, audit persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external service call, background worker, queue, daemon, subprocess, thread, database write, or hidden side effect was added.
- Phase 35 targeted tests passed.
- The full suite passed.
- `python -m compileall lima` passed.
- `git diff --check` passed.

## Approved Runtime Scope

Phase 36 may add only:

- `lima/kernel/candidate_preview.py`
- `lima/kernel/__init__.py` only if a safe public export is required by existing package convention

The existing package convention exports safe kernel primitives from `lima/kernel/__init__.py`, so a safe candidate preview export is eligible if implementation lands.

## Forbidden Scope

Phase 36 must not change `runtime_state.py`, `intake_candidate.py`, `candidate_status.py`, any other `lima/` file, or `tests/support/`.

It must not add HumanInput bridge behavior, Sparkbot wiring, live adapters, IntentCompiler behavior, GuardianDecision behavior, approval enforcement, execution, dispatch, persistence, audit persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external calls, workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Continue

Continue only to Phase 36.1 candidate preview acceptance design.
