# Phase 13.3 Threat Fixture Matrix

Phase 13.3 defines future fixture requirements for threat-derived test cases.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add production fixtures for runtime execution, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Fixture Matrix

Future fixture families should cover:

- malformed candidate
- unknown status
- stale candidate
- replayed candidate
- approval-bypass wording
- shell command attempt
- browser or network attempt
- file mutation attempt
- robotics or physical-world attempt
- Sparkbot integration attempt
- HumanInput bridge attempt

Each fixture must remain synthetic, inert, non-executing, and marked as test-only.

## Next Step

Phase 13.4 should close the lane with future acceptance gates before any Phase 14 decision.
