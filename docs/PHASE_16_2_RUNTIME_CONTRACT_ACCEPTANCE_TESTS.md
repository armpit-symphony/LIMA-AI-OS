# Phase 16.2 Runtime Contract Acceptance Tests

Phase 16.2 implements test-only runtime contract acceptance tests for existing non-executing candidate APIs.

This phase is tests/docs/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Acceptance Test Scope

The tests exercise existing APIs only:

- `lima.kernel.build_intake_candidate`
- `lima.kernel.normalize_candidate_status`
- `lima.kernel.validate_candidate`

## Implemented Acceptance Checks

- valid low-risk intake remains non-executing
- risky intake requires review without gaining authority
- malformed candidate metadata is invalid or blocked safely
- unknown status fails closed
- stale and replayed candidates remain blocked or invalid
- `execution_allowed` remains false
- `side_effects_allowed` remains false
- `approval_state` never becomes `approved`
- provenance is preserved
- operator/admin/Phil/trusted wording does not bypass safety
- no IntentEnvelope or GuardianDecision records are created
- Phase 5 HumanInput runtime bridge remains gated
