# Fake GuardianDecision Test Fixtures

These fixtures describe fake/test-only GuardianDecision shapes.

They are synthetic test artifacts only.

They do not create real GuardianDecision records.
They do not authorize production action.
They do not approve actions.
They do not create ApprovalMetadata.
They do not enforce policy.
They do not execute tools.
They do not call models.
They do not persist audit data.

## Files

- `allow_test_only_decision_fixtures.json`
- `deny_test_only_decision_fixtures.json`
- `needs_approval_test_only_decision_fixtures.json`
- `blocked_test_only_decision_fixtures.json`
- `safety_critical_decision_fixtures.json`
- `expired_revoked_superseded_decision_fixtures.json`

## Boundary

`allow_test_only` is not production allow.

`approval_ref` is a reference only and is not ApprovalMetadata.

`requires_approval` means approval is still required. It is not approval granted.

Safety-critical fake decisions must not auto-approve.
