# Phase 16.0 Test-Only Acceptance Implementation Charter

Phase 16.0 opens the test-only acceptance-gate implementation lane.

This phase is limited to docs, tests, and synthetic fixtures. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Phase 15 Inputs

- Phase 15.1 future static forbidden-pattern test implementation plan
- Phase 15.2 future runtime contract test implementation plan
- Phase 15.3 future threat fixture test implementation plan
- Phase 15.4 test-only implementation readiness gate / closeout

## Approved Phase 16 Implementation Groups

- Phase 16.1 may implement static forbidden-pattern acceptance tests under `tests/test_phase_16_1_*.py`.
- Phase 16.2 may implement runtime contract acceptance tests under `tests/test_phase_16_2_*.py`.
- Phase 16.3 may implement synthetic threat fixture acceptance tests and `phase_16_*` fixtures under `tests/fixtures/runtime_extraction/`.
- Phase 16.4 may review the test-only implementation.
- Phase 16.5 may archive Phase 16 and gate Phase 17.

## Acceptance Boundary

Phase 16 tests may inspect existing runtime source text and exercise existing non-executing candidate APIs. They must not mutate runtime files, introduce reusable scanner helpers, add support helpers, call external services, execute commands, dispatch actions, persist audit, or create live integration paths.

## Next Step

Phase 16.1 should implement static forbidden-pattern acceptance tests.
