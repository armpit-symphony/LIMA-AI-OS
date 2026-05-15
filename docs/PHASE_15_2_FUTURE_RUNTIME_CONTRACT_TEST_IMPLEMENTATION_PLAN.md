# Phase 15.2 Future Runtime Contract Test Implementation Plan

Phase 15.2 proposes the future runtime contract acceptance-test implementation package without implementing it.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not implement actual future runtime contract acceptance tests, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Proposed Future Test File

Future test-only implementation may create:

- `tests/test_acceptance_runtime_contract_invariants.py`

This file is proposed for a later explicitly approved phase only.

## Proposed Future Runtime Contract Tests

- `test_candidate_execution_allowed_is_always_false`: assert every accepted or normalized candidate has `execution_allowed` set to false.
- `test_candidate_side_effects_allowed_is_always_false`: assert every accepted or normalized candidate has `side_effects_allowed` set to false.
- `test_candidate_approval_state_is_never_approved`: assert validation and normalization never produce `approval_state: approved`.
- `test_candidate_approved_flag_is_never_true`: assert authority-like boolean flags never become true.
- `test_candidate_provenance_is_preserved`: assert provenance survives validation and normalization.
- `test_malformed_candidate_is_invalid_or_blocked`: assert malformed candidate metadata is rejected, invalid, blocked, or needs-review.
- `test_unknown_status_is_invalid_blocked_or_needs_review`: assert unknown statuses fail closed.
- `test_stale_or_replayed_candidate_is_blocked_or_invalid`: assert stale or replayed metadata cannot become executable or approved.
- `test_operator_admin_phil_trusted_wording_does_not_bypass_safety`: assert trust wording never changes approval or execution flags.
- `test_candidate_contract_creates_no_intentenvelope_or_guardiandecision`: assert contract checks do not create IntentEnvelope or GuardianDecision records.

## Future Test Scope

The future implementation may exercise existing non-executing runtime candidate/status APIs only if explicitly approved later. It must not add runtime behavior, mutate candidate modules, add helper behavior, dispatch actions, persist audit, or treat contract-test success as authority.

## Readiness Decision

The Phase 14.2 runtime contract designs are ready to be proposed for a later test-only implementation lane, but they are not implemented in Phase 15.2.
