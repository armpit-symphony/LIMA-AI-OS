# Phase 2.18 IntentEnvelope Harness Readiness Review

## Purpose

Review whether the test-only IntentEnvelope fixture harness is ready to become the standing safety gate for future IntentEnvelope-adjacent work.

This review is review-only.
This review does not implement real IntentCompiler.
This review does not parse natural language.
This review does not authorize execution.

## Current Harness Status

- helper exists under `tests/helpers`
- test-only only
- fixture files loaded
- explicit metadata validated
- expected envelope shape validated
- `raw_text` remains inert
- no GuardianDecision creation
- no model/tool execution
- no production behavior

Current counts:

- total: 15
- valid: 6
- invalid: 3
- clarification_needed: 2
- safety_critical: 4
- failed: 0

## What The Harness Proves

- explicit typed metadata can be validated
- expected IntentEnvelope-like shapes can be checked
- invalid/missing metadata cases are represented
- clarification_needed cases are represented
- safety-critical cases are represented
- `raw_text` is not parsed
- safety-critical fixtures require later Guardian/policy/approval review
- IntentEnvelope is not authorization

## What The Harness Does Not Prove

- real IntentCompiler behavior
- natural-language inference
- model-based intent extraction
- production intent compilation
- GuardianDecision safety
- policy/approval enforcement
- tool execution safety
- audit persistence
- redaction runtime

## Readiness Decision

GO for Phase 2.19 IntentEnvelope Safety Gate Docs.

Reason:

Before future IntentEnvelope-adjacent work, consolidate explicit metadata rules, `raw_text` inert rule, fixture harness requirements, and no-real-compiler rules into a standing safety gate.

NO-GO for real IntentCompiler, natural-language inference, execution, or GuardianDecision creation.

## Recommended Next Branch

`phase-2-19-intentenvelope-safety-gate-docs`

Purpose:

Create a standing safety gate for IntentEnvelope-adjacent work.

The gate should require:

- explicit typed metadata
- no `raw_text` inference
- intent fixture harness passing
- no real IntentCompiler
- no model calls
- no GuardianDecision creation
- safety-critical cases requiring later Guardian/policy/approval review

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
| `raw_text` parsed as intent | High | Harness validates explicit metadata and tests mutate `raw_text` without changing validation | Phase 2.19 must make inert `raw_text` a standing gate rule |
| fixture harness mistaken for real IntentCompiler | High | Harness is under `tests/helpers` and docs label it test-only | Gate docs must distinguish shape validation from compilation |
| expected envelope shape mistaken for production behavior | High | Fixtures and harness metadata say non-production and explicit metadata only | Gate docs must require expected shapes to remain test artifacts |
| IntentEnvelope mistaken for authorization | High | Docs and safety notes state IntentEnvelope is not authorization | Gate docs must keep GuardianDecision mandatory later |
| safety-critical fixture mistaken for approval | High | Safety-critical results require later Guardian/policy/approval review and no auto-approval | Gate docs must require safety-critical non-authorization checks |
| owner autonomy metadata mistaken for approval | Medium | Existing contracts keep owner autonomy metadata passive | Gate docs must keep autonomy references non-authorizing |
| references mistaken for authority | Medium | Fixture refs are synthetic metadata only | Gate docs must keep references as evidence candidates, not authority |
| real compiler work started too early | High | Phase 2.18 keeps real IntentCompiler blocked | Phase 2.19 should gate future IntentEnvelope-adjacent work before compiler design |

## Final Decision

GO for Phase 2.19 IntentEnvelope Safety Gate Docs.

NO-GO for real IntentCompiler, natural-language inference, execution, or GuardianDecision creation.
