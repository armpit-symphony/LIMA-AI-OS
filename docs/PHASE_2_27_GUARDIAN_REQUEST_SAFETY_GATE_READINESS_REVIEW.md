# Phase 2.27 Guardian Request Safety Gate Readiness Review

## Purpose

Review whether `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` is complete enough to serve as the standing safety gate for Guardian-request-adjacent work.

This review is review/docs only.
This review does not create GuardianDecision.
This review does not implement fake GuardianDecision fixtures.
This review does not enforce policy.
This review does not approve actions.
This review does not record ApprovalMetadata.
This review does not execute tools.
This review does not persist audit data.

## Current Gate Status

- `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` exists
- Guardian request vs GuardianDecision rule exists
- request vs approval rule exists
- `requested_tool_packs` request-only rule exists
- `approval_requirement_ref` descriptive-only rule exists
- `autonomy_context_ref` passive-only rule exists
- privacy/redaction non-enforcement rule exists
- required tests listed
- forbidden behaviors listed
- PR blocking conditions listed
- manual review requirements listed
- real GuardianDecision exit criteria listed
- Phil/operator approval required before real GuardianDecision discussion

## What The Gate Proves

- Guardian-request-adjacent PRs have a clear checklist
- Guardian request remains non-authorizing
- Guardian request fixture harness is test-only
- `requested_tool_packs` remain requests only
- `approval_requirement_ref` remains descriptive
- `autonomy_context_ref` remains passive
- privacy/redaction metadata remains non-enforcing
- GuardianDecision remains blocked
- approval/enforcement/execution remain blocked
- audit persistence remains blocked

## What The Gate Does Not Prove

- real GuardianDecision behavior
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- tool execution safety
- model call safety
- audit persistence safety
- redaction runtime
- production Guardian request behavior
- production Sparkbot behavior

## Readiness Decision

GO to pause Guardian-request safety-gate work and move to fake GuardianDecision test design.

NO-GO for real GuardianDecision, enforcement, approval, execution, or audit persistence.

## Recommended Next Branch

Recommend:

`phase-2-28-fake-guardiandecision-test-design-review`

Purpose:

Design the next safe non-production kernel boundary: fake GuardianDecision fixture design.

This should remain:

- design/review only
- fake/test only
- no real Guardian enforcement
- no policy enforcement
- no approval enforcement
- no execution
- no audit persistence

## Why Fake GuardianDecision Test Design Next

Guardian request is now gated.

The next logical boundary is what a fake/test GuardianDecision shape may look like.

But fake GuardianDecision must not be treated as production authorization.

It must remain a test artifact only.

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
| Guardian request gate forgotten in future work | High | `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` is the standing gate and lists required checks. | Keep the gate referenced in future Guardian-request-adjacent PRs. |
| Guardian request mistaken for GuardianDecision | High | Gate states request is not GuardianDecision and blocks decision creation. | Phase 2.28 must preserve request-vs-decision separation. |
| `requested_tool_packs` mistaken for granted tools | High | Gate states requested packs are not allowed or granted packs. | Future fake decision design must keep granted/allowed semantics separate. |
| `approval_requirement_ref` mistaken for ApprovalMetadata | High | Gate treats approval refs as descriptive and blocks ApprovalMetadata recording. | Future design must keep approval evidence separate from request metadata. |
| fake GuardianDecision mistaken for production authorization | High | This review recommends design-only fake/test work. | Phase 2.28 must state fake decision artifacts are non-production and non-authorizing. |
| enforcement added too early | High | Gate blocks Guardian, policy, and approval enforcement. | Keep enforcement out of Phase 2.28 scope. |
| audit persistence added too early | High | Gate blocks audit persistence and treats lineage as non-executing. | Keep fake/test artifacts non-persistent. |
| safety-critical request mistaken for approval | High | Gate requires later Guardian/policy/approval review for safety-critical requests. | Future fake decision design must not auto-approve safety-critical paths. |

## Final Decision

GO for Phase 2.28 Fake GuardianDecision Test Design Review.

NO-GO for real GuardianDecision, enforcement, approval, execution, or audit persistence.
