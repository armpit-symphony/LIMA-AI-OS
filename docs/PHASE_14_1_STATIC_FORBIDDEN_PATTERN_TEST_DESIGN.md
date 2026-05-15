# Phase 14.1 Static Forbidden-Pattern Test Design

Phase 14.1 converts Phase 13.1 static requirements into concrete future test names and expected assertions.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add static scanner implementation, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Test Designs

- `test_runtime_slice_has_no_forbidden_imports`: assert runtime files do not import shell, network, browser, threading, multiprocessing, Sparkbot, or live-adapter modules.
- `test_runtime_slice_has_no_forbidden_side_effect_calls`: assert runtime files do not call execution, filesystem mutation, dispatch, approval, or persistence functions.
- `test_runtime_slice_has_no_forbidden_boundary_names`: assert runtime files do not introduce HumanInput bridge, IntentCompiler, GuardianDecision, Sparkbot, Robo-OS driver, approval enforcer, or audit writer boundaries.
- `test_runtime_slice_has_no_authority_claims`: assert docs and fixtures do not claim approval granted, execution allowed, side effects allowed, dispatch, persistence, or live adapter connection.

## Expected Assertion Style

Future tests should be static and deterministic. They may inspect text or parsed Python syntax, but they must not import Sparkbot, start adapters, call external services, mutate files, or execute tools.

## Next Step

Phase 14.2 should design runtime contract acceptance tests.
