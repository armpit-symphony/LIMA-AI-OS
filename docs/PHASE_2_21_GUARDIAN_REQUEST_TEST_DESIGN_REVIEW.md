# Phase 2.21 Guardian Request Test Design Review

## Purpose

Review how LIMA should safely design a test-only IntentEnvelope-to-Guardian-request path in a future phase.

This review does not create GuardianDecision.
This review does not enforce policy.
This review does not approve actions.
This review does not execute tools.
This review does not persist audit data.

## Current Boundary State

- HumanInput boundary exists.
- IntentEnvelope fixture harness exists.
- IntentEnvelope is not authorization.
- GuardianDecision remains mandatory before consequential behavior.
- No real IntentCompiler exists.
- No real Guardian enforcement exists.
- No real policy/approval enforcement exists.
- No production wiring exists.

## Guardian Request Boundary Rule

A Guardian request is a request for review/decision, not a decision.

It must not:

- approve actions
- execute actions
- call tools
- call drivers
- persist audit records
- bypass policy
- bypass approval
- bypass GuardianDecision

## Test-Only Design Direction

Recommend future Phase 2.22:

`phase-2-22-guardian-request-test-fixtures`

Purpose:

Create synthetic test fixtures for explicit IntentEnvelope-like inputs and expected Guardian request shapes.

Allowed:

- fixtures only
- explicit metadata only
- no real GuardianDecision
- no enforcement
- no policy evaluation
- no approval recording
- no execution
- no audit persistence

## Proposed Guardian Request Shape

Future test fixtures may use fields like:

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

Important:

These are test-shape fields only.

They do not authorize anything.

## Required Source Data

Guardian request test fixtures may use explicit IntentEnvelope fixture metadata.

They must not:

- infer from `raw_text`
- infer from missing metadata
- call real IntentCompiler
- call models
- call policy engine
- call approval engine

## Risk / Safety Rules

- missing `risk_class` must produce `invalid` / `needs_review` / `clarification_needed` in future fixtures
- `safety_critical` / `critical` request must require later Guardian/policy/approval review
- `requested_tool_packs` are requests only, not granted access
- `autonomy_context_ref` is passive only
- `approval_requirement_ref` is descriptive only
- privacy/redaction metadata is not enforcement

## GuardianDecision Boundary

Guardian request is not GuardianDecision.

No GuardianDecision is created in Phase 2.21.

Future test fixtures must not imply approval.

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
| Guardian request mistaken for GuardianDecision | High | This review states request is not decision | Phase 2.22 fixtures must avoid decision fields/statuses |
| request fixture mistaken for approval | High | Request shape is documented as non-authorizing | Fixture notes must state no approval is granted |
| `requested_tool_packs` mistaken for allowed tools | High | Tool packs are documented as requests only | Future fixtures must distinguish requested from allowed packs |
| `autonomy_context_ref` mistaken for authorization | High | Autonomy refs remain passive only | Keep autonomy context descriptive and non-enforcing |
| `approval_requirement_ref` mistaken for ApprovalMetadata | High | Approval requirement ref is descriptive only | Future fixtures must not create ApprovalMetadata |
| privacy metadata mistaken for redaction enforcement | Medium | Privacy/redaction metadata is not enforcement | Keep redaction runtime blocked |
| safety-critical request mistaken for approval | High | Safety-critical requests require later Guardian/policy/approval review | Future fixtures must never auto-approve critical paths |
| fake/test request mistaken for production enforcement | High | Design is test-only and no production wiring exists | Keep helper/fixtures under tests and docs only |

## Final Decision

GO for Phase 2.22 Guardian Request Test Fixtures.

NO-GO for real GuardianDecision, real Guardian enforcement, policy/approval enforcement, execution, or audit persistence.
