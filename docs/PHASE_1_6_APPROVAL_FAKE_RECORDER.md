# Phase 1.6 Approval Fake Recorder

## Purpose

Define a fake, in-memory `ApprovalMetadata` recorder for contract tests.

It records approval metadata and approval scope objects without enforcing approval or authorizing execution.

## Non-Goals

- no real approval enforcement
- no PIN verification
- no breakglass enforcement
- no live approval tokens
- no Guardian enforcement
- no policy enforcement
- no tool execution
- no model calls
- no driver calls
- no Sparkbot integration
- no Guardian Suite implementation copied

## Fake Recorder Rules

- in-memory only
- metadata only
- no external services
- no env vars
- no DB/storage
- no secrets
- no raw PINs/tokens/keys
- no production authorization

## ApprovalMetadata Safety

`ApprovalMetadata` is evidence only.

`ApprovalMetadata` does not replace `GuardianDecision`.

`ApprovalMetadata` does not authorize execution by itself.

Future execution paths still require `GuardianDecision.decision_id` and policy checks.

## Breakglass Safety

The fake recorder may store breakglass-style approval metadata, but it must not:

- open live breakglass sessions
- bypass Guardian
- bypass approval
- create privileged sessions
- execute actions

## Future Path

Future real approval enforcement remains blocked until:

- PIN verification design
- breakglass enforcement design
- Guardian enforcement design
- policy enforcement design
- audit lineage emission
- redaction/privacy implementation
- Sparkbot adapter review
