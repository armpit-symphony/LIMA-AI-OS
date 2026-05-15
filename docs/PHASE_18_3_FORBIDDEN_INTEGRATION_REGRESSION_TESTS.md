# Phase 18.3 Forbidden Integration Regression Tests

Phase 18.3 adds test-only regression checks that forbidden integrations remain absent from the existing non-executing candidate runtime files.

This phase is tests/docs/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Regression Checks

The Phase 18.3 tests scan the existing candidate runtime files:

- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`
- `lima/kernel/__init__.py`

The tests assert that those files do not import or call Sparkbot, HumanInput runtime bridge behavior, live adapters, IntentCompiler, GuardianDecision, subprocess, shell, browser, network, file mutation, persistence, queues, workers, dispatch, approval enforcement, robotics, or physical-world behavior.

## Boundary

These are test-only static regression checks. They are not runtime enforcement, do not add scanners under `tests/support/`, and do not approve runtime expansion.
