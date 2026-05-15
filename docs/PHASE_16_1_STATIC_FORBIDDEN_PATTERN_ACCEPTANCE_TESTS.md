# Phase 16.1 Static Forbidden-Pattern Acceptance Tests

Phase 16.1 implements test-only static forbidden-pattern acceptance checks for the existing non-executing kernel candidate files.

This phase is tests/docs/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Acceptance Test Scope

The static checks inspect only these existing runtime files:

- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`
- `lima/kernel/__init__.py`

## Implemented Acceptance Checks

- no Sparkbot imports
- no live adapter imports
- no HumanInput runtime bridge imports
- no shell, browser, network, file mutation, robotics, physical-world, subprocess, worker, daemon, queue, thread, or database-write calls
- no approval enforcement, execution, dispatch, or audit persistence calls
- no authority-producing assignments such as `execution_allowed = True`, `side_effects_allowed = True`, `approved = True`, or `approval_state = "approved"`

The checks are intentionally stdlib-only and local to the Phase 16.1 test file.
