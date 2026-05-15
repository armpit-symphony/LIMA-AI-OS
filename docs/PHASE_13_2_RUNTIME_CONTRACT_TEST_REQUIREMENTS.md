# Phase 13.2 Runtime Contract Test Requirements

Phase 13.2 defines future runtime contract test requirements for non-executing candidate invariants.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add contract-test implementation code, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Contract Test Requirements

Future contract tests should prove:

- `execution_allowed` is always false
- `side_effects_allowed` is always false
- `approval_state` is never `approved`
- `approved` is never true
- provenance is preserved
- malformed candidates are rejected or marked invalid safely
- unknown status becomes blocked, invalid, or needs-review
- stale or replayed candidates are blocked or invalid
- operator, admin, Phil, or trusted wording does not bypass safety
- Phase 5 HumanInput runtime bridge remains gated
- candidate validation cannot create IntentEnvelope or GuardianDecision records

## Contract-Test Scope

These are requirements for future tests, not new runtime behavior.

## Next Step

Phase 13.3 should define the threat fixture matrix.
