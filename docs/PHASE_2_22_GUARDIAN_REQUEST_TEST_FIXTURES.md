# Phase 2.22 Guardian Request Test Fixtures

## Purpose

Create synthetic fixtures for explicit IntentEnvelope-like inputs and expected Guardian request shapes.

This phase does not implement GuardianDecision.
This phase does not enforce policy.
This phase does not approve actions.
This phase does not execute tools.
This phase does not persist audit data.

## Fixture Rule

Guardian request fixtures describe request shapes only.

They do not authorize anything.

## Fixture Categories

- `valid_guardian_request_fixtures.json`
- `invalid_guardian_request_fixtures.json`
- `safety_critical_guardian_request_fixtures.json`
- `approval_required_guardian_request_fixtures.json`

## Request Shape Fields

- `request_id`
- `lineage_id`
- `intent_envelope_ref`
- `actor_ref`
- `session_ref`
- `shell_id`
- `action_type`
- `risk_class`
- `requested_tool_packs`
- `target_ref`
- `typed_args`
- `evidence_refs`
- `privacy_class`
- `redaction_class`
- `approval_requirement_ref`
- `autonomy_context_ref`
- `reason`
- `confidence`
- `created_at`
- `metadata`

## Boundary Rules

- Guardian request is not GuardianDecision.
- Guardian request is not approval.
- `requested_tool_packs` are requests only.
- `autonomy_context_ref` is passive only.
- `approval_requirement_ref` is descriptive only.
- privacy/redaction metadata is not enforcement.
- no ApprovalMetadata is created.
- no audit persistence is created.
- no execution occurs.

## Safety-Critical Rules

Safety-critical fixtures must not imply approval.

Terminal, robot, secret, payment, deploy, admin, filesystem delete, and destructive requests require later Guardian/policy/approval review.

## Acceptance Criteria

- fixture files exist
- fixtures are synthetic/no secrets
- valid request fixtures include explicit request fields
- invalid fixtures do not imply request acceptance
- safety-critical fixtures require later Guardian/policy/approval review
- approval-required fixtures do not create approval
- no GuardianDecision creation
- no runtime behavior added
