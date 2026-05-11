# Phase 2.29 Fake GuardianDecision Test Fixtures

## Purpose

Create synthetic fixtures for fake GuardianDecision test shapes.

This phase does not create real GuardianDecision.
This phase does not enforce policy.
This phase does not approve actions.
This phase does not execute tools.
This phase does not persist audit data.

## Fixture Rule

Fake GuardianDecision fixtures describe test decision shapes only.

They do not authorize production action.

## Fixture Categories

- `allow_test_only_decision_fixtures.json`
- `deny_test_only_decision_fixtures.json`
- `needs_approval_test_only_decision_fixtures.json`
- `blocked_test_only_decision_fixtures.json`
- `safety_critical_decision_fixtures.json`
- `expired_revoked_superseded_decision_fixtures.json`

## Fake Decision Shape Fields

- `decision_id`
- `request_id`
- `lineage_id`
- `decision_status`
- `risk_class`
- `action_type`
- `allow`
- `requires_approval`
- `denied`
- `blocked`
- `reason`
- `policy_refs`
- `approval_requirement_ref`
- `approval_ref`
- `tool_pack_refs`
- `safety_flags`
- `privacy_class`
- `redaction_class`
- `expires_at`
- `supersedes_decision_id`
- `metadata`

## Boundary Rules

- Fake GuardianDecision is not real GuardianDecision.
- Fake GuardianDecision is not production authorization.
- `allow_test_only` is not production allow.
- `approval_ref` is not ApprovalMetadata.
- `requires_approval` is not approval granted.
- requested/selected tool packs are not executed.
- no ApprovalMetadata is created.
- no policy enforcement occurs.
- no execution occurs.
- no audit persistence occurs.

## Safety-Critical Rules

Safety-critical fake decisions must not auto-approve.

Robot, terminal, secret, payment, deploy, admin, filesystem delete, and destructive decisions require later Guardian/policy/approval review.

Human safety and law override owner command.

## Acceptance Criteria

- fixture files exist
- fixtures are synthetic/no secrets
- fake decision shape fields are present
- statuses are test-only
- safety-critical fixtures do not allow by default
- approval-required fixtures do not create approval
- no real GuardianDecision
- no enforcement
- no execution
- no audit persistence
- tests pass
