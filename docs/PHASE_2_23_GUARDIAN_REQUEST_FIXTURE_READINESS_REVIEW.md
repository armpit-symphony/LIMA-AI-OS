# Phase 2.23 Guardian Request Fixture Readiness Review

## Purpose

Review whether the Phase 2.22 Guardian request fixtures are ready for a future test-only Guardian request fixture harness.

This review does not create GuardianDecision.
This review does not enforce policy.
This review does not approve actions.
This review does not execute tools.
This review does not persist audit data.

## Current Fixture Inventory

| Fixture file | Fixture purpose | Expected status | Required explicit request fields | Safety notes | Non-authorizing posture |
| --- | --- | --- | --- | --- | --- |
| `valid_guardian_request_fixtures.json` | Complete synthetic Guardian request shape examples for low-risk information, scheduling, draft-only communication, and high-risk email send. | `valid` | Full explicit request shape: request identity, lineage, actor/session/shell refs, action/risk, requested tool packs, target, typed args, evidence refs, privacy/redaction classes, passive approval/autonomy refs, reason, confidence, created time, and metadata. | High-risk email send remains pending later Guardian/policy/approval review. | Request shape only; no GuardianDecision, approval, execution, or audit persistence. |
| `invalid_guardian_request_fixtures.json` | Missing or malformed request-shape examples. | `invalid`, `needs_review`, or `clarification_needed` | Deliberately incomplete or malformed explicit request fields such as missing `request_id`, missing `risk_class`, missing `action_type`, missing `intent_envelope_ref`, or malformed `requested_tool_packs`. | Invalid shape must not become an accepted Guardian request. | No accepted request shape; no GuardianDecision, approval, execution, or audit persistence. |
| `safety_critical_guardian_request_fixtures.json` | Critical and safety-critical request examples for terminal, robot, secret, and payment/deploy/admin/destructive-style work. | `safety_critical` | Complete explicit request shape with `critical` or `safety_critical` risk. | Requires later Guardian/policy/approval review; no auto-approval. | Request shape only; safety-critical status is not authorization. |
| `approval_required_guardian_request_fixtures.json` | Approval-required request examples for email send, payment, deploy, admin change, secret access, and filesystem delete. | `approval_required` | Complete explicit request shape with descriptive `approval_requirement_ref`. | Approval refs remain descriptive and do not create ApprovalMetadata. | No approval is granted; no GuardianDecision, execution, or audit persistence. |

## What The Fixtures Prove

- valid request shapes can be represented
- invalid/missing request shape cases are represented
- safety-critical request cases are represented
- approval-required request cases are represented
- `requested_tool_packs` remain requests only
- `approval_requirement_ref` remains descriptive
- `autonomy_context_ref` remains passive
- privacy/redaction metadata remains non-enforcing
- GuardianDecision is absent
- approval is absent
- execution is absent

## What The Fixtures Do Not Prove

- real GuardianDecision behavior
- real Guardian enforcement
- policy enforcement
- approval enforcement
- tool execution safety
- model call safety
- audit persistence
- redaction runtime
- production Guardian request behavior
- production Sparkbot behavior

## Fixture Coverage Assessment

| Category | Covered? | Risk class | Gap | Recommendation |
| --- | --- | --- | --- | --- |
| low-risk informational request | yes | low | None for fixture readiness. | Keep as a valid harness baseline. |
| calendar/scheduling request | yes | medium | None for fixture readiness. | Keep as a medium-risk request-shape example. |
| draft-only communication request | yes | medium | None for fixture readiness. | Keep clear that draft is not send authorization. |
| email-send approval-required request | yes | high | None for fixture readiness. | Keep approval refs descriptive only. |
| terminal critical request | yes | critical | None for fixture readiness. | Keep terminal execution blocked. |
| robot safety-critical request | yes | safety_critical | None for fixture readiness. | Keep Robo-OS physical action blocked. |
| secret access | yes | critical | None for fixture readiness. | Keep raw secret access and enforcement blocked. |
| payment/deploy/admin/destructive action | yes | critical | Covered across safety-critical and approval-required fixtures. | Keep each as request shape only. |
| missing `request_id` | yes | low | None for fixture readiness. | Future harness should report `invalid`. |
| missing `risk_class` | yes | medium/unknown | None for fixture readiness. | Future harness should report `needs_review` or `invalid`. |
| missing `action_type` | yes | medium | None for fixture readiness. | Future harness should report `invalid`. |
| missing `intent_envelope_ref` | yes | medium | None for fixture readiness. | Future harness should report `clarification_needed` or `needs_review`. |
| malformed `requested_tool_packs` | yes | low | None for fixture readiness. | Future harness should reject non-list pack metadata. |
| `approval_required` without `approval_granted` | yes | high/critical | None for fixture readiness. | Future harness should confirm no approval is granted or recorded. |

## Readiness Decision

GO for Phase 2.24 Guardian Request Fixture Harness.

NO-GO for real GuardianDecision, enforcement, approval, execution, or audit persistence.

## Recommended Next Branch

Recommend:

`phase-2-24-guardian-request-fixture-harness`

Purpose:

Create a test-only harness that validates explicit Guardian request fixtures against expected Guardian request shapes.

Allowed:

- test-only helper
- fixtures only
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- no policy evaluation
- no approval recording

## Future Harness Rules

The Phase 2.24 harness may:

- load Guardian request fixture files
- validate required explicit request fields
- validate `expected_guardian_request` shape
- report `invalid` / `needs_review` / `safety_critical` / `approval_required` status

The Phase 2.24 harness must not:

- create GuardianDecision
- enforce policy
- record ApprovalMetadata
- approve actions
- execute tools
- persist audit data
- infer from `raw_text`
- call models

## Still Blocked

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
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
| Guardian request mistaken for GuardianDecision | High | Fixtures and docs state request is not decision. | Future harness must reject decision fields. |
| request fixture mistaken for approval | High | Approval-required fixtures state no approval is granted. | Future harness must reject `approval_granted` and ApprovalMetadata fields. |
| `requested_tool_packs` mistaken for allowed tools | High | Fixtures use requested packs only and tests reject allowed/granted pack fields. | Future harness must preserve requested-only semantics. |
| `approval_requirement_ref` mistaken for ApprovalMetadata | High | Approval refs are documented as descriptive only. | Future harness must not record or validate real ApprovalMetadata. |
| `autonomy_context_ref` mistaken for authorization | High | Autonomy refs are passive fixture references. | Future harness must treat autonomy metadata as descriptive only. |
| privacy metadata mistaken for redaction enforcement | Medium | Fixtures and tests state privacy/redaction metadata is not enforcement. | Keep redaction runtime blocked. |
| safety-critical request mistaken for approval | High | Safety fixtures require later Guardian/policy/approval review and no auto-approval. | Future harness must report safety-critical without approval. |
| test harness mistaken for production Guardian | High | Next scope is test-only helper under tests. | Keep production Guardian behavior and enforcement blocked. |

## Final Decision

GO for Phase 2.24 Guardian Request Fixture Harness.

NO-GO for real GuardianDecision, enforcement, approval, execution, or audit persistence.
