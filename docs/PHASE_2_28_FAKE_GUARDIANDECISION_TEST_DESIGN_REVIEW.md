# Phase 2.28 Fake GuardianDecision Test Design Review

## Purpose

Design a future test-only fake GuardianDecision fixture shape.

This review does not create real GuardianDecision.
This review does not enforce policy.
This review does not approve actions.
This review does not execute tools.
This review does not persist audit data.

## Current Boundary State

- Guardian request safety gate exists.
- Guardian request fixture harness exists.
- Guardian request is not GuardianDecision.
- Guardian request is not approval.
- Real GuardianDecision remains blocked.
- Real Guardian enforcement remains blocked.
- Policy/approval enforcement remains blocked.
- Execution remains blocked.
- Audit persistence remains blocked.

## Fake GuardianDecision Boundary Rule

Fake GuardianDecision is test-only.

It must not:

- authorize production action
- approve real-world execution
- enforce policy
- record ApprovalMetadata
- execute tools
- call models
- write audit records
- bypass required approval
- bypass human safety/law rules
- replace real GuardianDecision

## Test-Only Design Direction

Recommend future Phase 2.29:

`phase-2-29-fake-guardiandecision-test-fixtures`

Purpose:

Create synthetic fixtures for fake GuardianDecision shapes based on explicit Guardian request fixtures.

Allowed:

- fixtures only
- explicit request/decision metadata only
- fake/test-only decision shapes
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence

## Proposed Fake GuardianDecision Shape

Design a future test fixture shape with fields like:

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

Important:

These are fake/test-shape fields only.

They do not authorize production action.

## Decision Status Rules

Proposed statuses:

- `allow_test_only`
- `deny_test_only`
- `needs_approval_test_only`
- `blocked_test_only`
- `needs_review_test_only`
- `expired_test_only`
- `revoked_test_only`
- `superseded_test_only`

Rules:

- status must include `test_only` or be clearly documented as fake.
- critical/safety-critical actions must not default to allow.
- denied/blocked/expired/revoked/superseded remain auditable later, but this phase does not add audit persistence.
- `approval_ref` is a reference only and does not create ApprovalMetadata.

## Safety / Risk Rules

- safety-critical actions must require later Guardian/policy/approval review.
- robot/terminal/secret/payment/deploy/admin/destructive decisions must not auto-allow.
- owner autonomy metadata cannot approve by itself.
- trusted context metadata cannot approve by itself.
- requested_tool_packs are not granted tools.
- `allow_test_only` is not production authorization.

## Relationship To Existing Contracts

- PolicyDecision does not replace GuardianDecision.
- ApprovalMetadata is evidence, not execution.
- Spine/Audit records, it does not execute.
- Fake GuardianDecision does not persist audit.
- Fake GuardianDecision does not bypass ToolPackRiskPolicy.
- Fake GuardianDecision does not bypass human safety/law.

## Still Blocked

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device/autonomy enforcement
- redaction runtime

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| fake GuardianDecision mistaken for production authorization | High | This review states fake decisions are test-only and non-authorizing. | Future fixtures must remain under test-only paths and use fake status names. |
| `allow_test_only` mistaken for allow | High | Status names include `test_only` and are documented as fake. | Future harness must reject production `approved`/`allow` semantics. |
| `approval_ref` mistaken for ApprovalMetadata | High | Approval refs are references only and do not create approval records. | Future fixtures must not include ApprovalMetadata payloads. |
| `requires_approval` mistaken for approval granted | High | Required approval is a need, not a grant. | Future harness must distinguish required approval from approved status. |
| safety-critical decision auto-approved | Critical | Safety/risk rules forbid default allow for critical categories. | Future fixtures must encode review/approval-required posture for critical actions. |
| owner autonomy metadata mistaken for approval | High | Owner autonomy metadata is passive and cannot approve by itself. | Future fixtures must keep autonomy fields descriptive only. |
| trusted context metadata mistaken for approval | High | Trusted context metadata is passive and cannot approve by itself. | Future fixtures must keep trust fields descriptive only. |
| fake decision mistaken for audit evidence | High | This phase does not add audit persistence and fake decisions are not audit records. | Future harness must not write audit data or claim persistence. |
| production enforcement added too early | Critical | Still-blocked list forbids enforcement, approval, execution, and persistence. | Keep Phase 2.29 limited to fixtures only. |

## Final Decision

GO for Phase 2.29 Fake GuardianDecision Test Fixtures.

NO-GO for real GuardianDecision, real enforcement, approval, execution, or audit persistence.
