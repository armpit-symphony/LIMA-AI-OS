# Phase 14.2 Runtime Contract Test Design

Phase 14.2 converts Phase 13.2 runtime contract requirements into concrete future test names and expected assertions.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add contract-test implementation code, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Test Designs

- `test_candidate_contract_keeps_execution_flags_false`: assert `execution_allowed` and `side_effects_allowed` remain false.
- `test_candidate_contract_never_approves`: assert `approval_state` is never `approved` and `approved` is never true.
- `test_candidate_contract_preserves_provenance`: assert source provenance survives normalization and validation.
- `test_candidate_contract_blocks_malformed_unknown_stale_replayed`: assert malformed, unknown, stale, and replayed candidates become blocked, invalid, or needs-review.
- `test_candidate_contract_blocks_operator_bypass_language`: assert operator, admin, Phil, or trusted wording does not grant approval.
- `test_candidate_contract_creates_no_bridge_or_decision_records`: assert no IntentEnvelope, GuardianDecision, or HumanInput bridge record is created.

## Next Step

Phase 14.3 should design fixture-based acceptance tests for the threat matrix.
