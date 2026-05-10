# Phase 2.20 IntentEnvelope Safety Gate Readiness Review

## Purpose

Review whether `docs/INTENTENVELOPE_SAFETY_GATE.md` is complete enough to serve as the standing safety gate for IntentEnvelope-adjacent work.

This review is review-only.
This review does not implement real IntentCompiler.
This review does not parse natural language.
This review does not create GuardianDecision.
This review does not authorize execution.

## Current Gate Status

- `docs/INTENTENVELOPE_SAFETY_GATE.md` exists
- `raw_text` inert rule exists
- explicit typed metadata rule exists
- required tests are listed
- forbidden behaviors are listed
- PR blocking conditions are listed
- manual review requirements are listed
- real IntentCompiler exit criteria are listed
- Phil/operator approval is required before real IntentCompiler discussion

## What The Gate Proves

- IntentEnvelope-adjacent PRs have a clear checklist
- `raw_text` must remain inert
- explicit typed metadata is required for tests
- fixture harness remains test-only
- IntentEnvelope is not authorization
- GuardianDecision remains mandatory
- safety-critical intent requires later Guardian/policy/approval review
- real IntentCompiler remains blocked
- natural-language inference remains blocked

## What The Gate Does Not Prove

- real IntentCompiler behavior
- production intent compilation
- natural-language inference safety
- model-based intent extraction safety
- GuardianDecision safety
- policy/approval enforcement
- tool execution safety
- audit persistence
- redaction runtime
- production Sparkbot behavior

## Readiness Decision

GO to pause IntentEnvelope safety-gate work and move to the next non-production kernel area.

NO-GO for real IntentCompiler, natural-language inference, execution, or GuardianDecision creation.

## Recommended Next Area

`phase-2-21-guardian-request-test-design-review`

Purpose:

Move to the next kernel boundary after IntentEnvelope: how an IntentEnvelope may later become a Guardian request in test/design only.

Reason:

HumanInput and IntentEnvelope are now gated. The next safe boundary is Guardian request design, still with:

- no real Guardian enforcement
- no execution
- no policy/approval enforcement
- no tool/model calls
- no production wiring

## Why Guardian Request Test Design Next

IntentEnvelope is not authorization.

The next logical boundary is a test-only design review for Guardian request shape.

This should not:

- create real GuardianDecision
- enforce policy
- approve actions
- execute tools
- persist audit data

## Still Blocked

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device/autonomy enforcement
- audit persistence
- redaction runtime
- real Guardian / policy / approval enforcement

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| IntentEnvelope gate forgotten in future work | High | `docs/INTENTENVELOPE_SAFETY_GATE.md` is the standing gate and is covered by doc tests | Phase 2.21 must reference the gate before Guardian request design |
| `raw_text` parsed as intent | High | Gate blocks `raw_text` parsing and fixture harness validates explicit metadata only | Keep raw text inert in every IntentEnvelope-adjacent PR |
| expected envelope shape mistaken for production behavior | High | Gate keeps fixture harness test-only and production behavior blocked | Phase 2.21 must treat request shapes as design/test artifacts only |
| IntentEnvelope mistaken for authorization | High | Gate states IntentEnvelope is not authorization and GuardianDecision remains mandatory | Guardian request design must not approve or execute |
| real IntentCompiler started too early | High | Gate requires explicit readiness review and Phil/operator approval | Keep compiler implementation blocked |
| natural-language inference added too early | High | Gate blocks natural-language inference and hidden parsers | Require future safety design before any inference discussion |
| Guardian request work starts enforcing too early | High | Recommended next area is design/test-only and no real enforcement | Phase 2.21 must block policy, approval, and GuardianDecision creation |
| safety-critical intent mistaken for approval | High | Gate requires later Guardian/policy/approval review | Keep safety-critical examples non-authorizing |
| references mistaken for authority | Medium | Gate states references are not authority | Keep evidence refs as review context, not approval |

## Final Decision

GO for Phase 2.21 Guardian Request Test Design Review.

NO-GO for real IntentCompiler, natural-language inference, execution, or GuardianDecision creation.
