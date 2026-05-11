# Phase 2.25 Guardian Request Harness Readiness Review

## Purpose

Review whether the test-only Guardian request fixture harness is ready to become a standing safety gate for future Guardian-request-adjacent work.

This review does not create GuardianDecision.
This review does not enforce policy.
This review does not approve actions.
This review does not record ApprovalMetadata.
This review does not execute tools.
This review does not persist audit data.

## Current Harness Status

- helper exists under `tests/helpers`
- test-only only
- fixture files loaded
- explicit request fields validated
- `expected_guardian_request` shape validated
- no GuardianDecision creation
- no policy enforcement
- no approval enforcement
- no ApprovalMetadata recording
- no execution
- no audit persistence
- no production behavior

Current counts:

- total: 19
- valid: 4
- invalid: 3
- needs_review: 2
- safety_critical: 4
- approval_required: 6
- failed: 0

## What The Harness Proves

- explicit Guardian request fields can be validated
- expected Guardian request shapes can be checked
- invalid/missing request cases are represented
- needs_review cases are represented
- safety-critical cases are represented
- approval-required cases are represented
- `requested_tool_packs` remain requests only
- `approval_requirement_ref` remains descriptive
- `autonomy_context_ref` remains passive
- privacy/redaction metadata remains non-enforcing
- GuardianDecision is absent
- approval is absent
- execution is absent
- audit persistence is absent

## What The Harness Does Not Prove

- real GuardianDecision behavior
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- tool execution safety
- model call safety
- audit persistence
- redaction runtime
- production Guardian request behavior
- production Sparkbot behavior

## Readiness Decision

GO for Phase 2.26 Guardian Request Safety Gate Docs.

Reason:

Before future Guardian-request-adjacent work, consolidate the request-vs-decision boundary, fixture harness requirements, forbidden behaviors, and manual review requirements into a standing safety gate.

NO-GO for real GuardianDecision, enforcement, approval, execution, or audit persistence.

## Recommended Next Branch

Recommend:

`phase-2-26-guardian-request-safety-gate-docs`

Purpose:

Create a standing safety gate for Guardian-request-adjacent work.

The gate should require:

- Guardian request remains non-authorizing
- GuardianDecision remains blocked
- `requested_tool_packs` remain requests only
- approval refs remain descriptive
- autonomy refs remain passive
- fixture harness tests pass
- no enforcement, approval, execution, or persistence

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
| Guardian request mistaken for GuardianDecision | High | Harness metadata and docs state request is not decision. | Safety gate must block decision fields and creation behavior. |
| harness mistaken for production Guardian | High | Harness lives under `tests/helpers` and validates shapes only. | Safety gate must require test-only placement and no production imports. |
| `requested_tool_packs` mistaken for allowed/granted tools | High | Harness rejects allowed/granted tool pack fields. | Safety gate must preserve requested-only semantics. |
| `approval_requirement_ref` mistaken for ApprovalMetadata | High | Harness treats approval refs as descriptive and rejects approval metadata fields. | Safety gate must keep approval recording blocked. |
| `autonomy_context_ref` mistaken for authorization | High | Harness treats autonomy refs as passive. | Safety gate must block autonomy enforcement and risk reduction. |
| privacy metadata mistaken for redaction enforcement | Medium | Harness treats privacy/redaction fields as metadata only. | Safety gate must keep redaction runtime blocked. |
| safety-critical request mistaken for approval | High | Harness requires later Guardian/policy/approval review notes and no auto-approval posture. | Safety gate must keep safety-critical request non-authorizing. |
| approval_required request mistaken for approval granted | High | Harness requires approval-required fixtures to remain descriptive and reject `approval_granted`. | Safety gate must block approval grants and ApprovalMetadata recording. |

## Final Decision

GO for Phase 2.26 Guardian Request Safety Gate Docs.

NO-GO for real GuardianDecision, enforcement, approval, execution, or audit persistence.
