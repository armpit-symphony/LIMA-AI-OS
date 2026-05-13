# Phase 5.7 HumanInput Runtime Bridge Design Proposal

Phase 5.7 proposes the shape of a future runtime HumanInput to IntentEnvelope bridge. It is design metadata only.

This is docs/tests/fixtures only. It does not implement a runtime bridge, does not add live adapter code, does not modify `lima/`, does not modify `tests/support/`, does not change the Phase 5.4 test-only helper, does not wire Sparkbot, does not implement real IntentCompiler behavior, does not implement real GuardianDecision behavior, does not enforce approval, does not execute, and does not persist audit.

## Future Bridge Purpose

A future bridge may normalize an operator-originated HumanInput request into an IntentEnvelope candidate for Guardian review. HumanInput is intent context, not execution permission.

The future bridge must produce non-executable candidate metadata only until a later explicitly approved runtime implementation phase defines and validates live behavior.

## Allowed Inputs

- HumanInput records from an approved runtime intake boundary.
- Source metadata for shell, channel, room, actor, session, timestamp, and lineage seed.
- Operator intent text and requested action text.
- Passive trust and autonomy references.
- Privacy, redaction, retention, and visibility metadata.

## Rejected Inputs

- Missing, empty, malformed, replayed, or stale HumanInput records.
- Inputs without provenance.
- Inputs that claim approval only through operator/admin/Phil/trusted wording.
- Inputs that request shell, browser, network, file mutation, robotics, or physical-world action without an explicit approval-required state.
- Any payload that attempts to carry execution instructions as permission.

## Candidate Requirements

Every future IntentEnvelope candidate must preserve source, source channel, operator intent, raw text, normalized request, requested action, risk tier, approval state, blocked reason, and provenance.

Every candidate remains non-executable by default:

- `executable`: false
- `execution_allowed`: false
- `side_effects_allowed`: false

Risk tier and approval state are classification metadata only. They do not enforce approval and do not permit execution.

## Trust And Autonomy Rules

Operator intent may raise priority, but it must not bypass Guardian review. Trust and autonomy references remain passive context until a later approved GuardianDecision phase defines enforcement.

## Blocked Behavior

- live runtime bridge implementation
- live adapter code
- Phase 5.4 helper reuse as runtime classifier logic
- Sparkbot import or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

## Next Gate

Phase 5.8 may continue with a docs/tests/fixtures-only threat model. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
