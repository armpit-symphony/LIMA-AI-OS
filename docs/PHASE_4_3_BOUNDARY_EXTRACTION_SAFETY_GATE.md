# Phase 4.3 Boundary Extraction Safety Gate

Phase 4.3 defines the safety gate for the selected Phase 4.2 boundary candidate:

`humaninput_intake_boundary_for_chat_and_voice`

It is a safety gate only. It does not add runtime behavior, create adapters, import Sparkbot, wire routes, call models, execute tools, enforce approvals, persist audit events, or control physical-world systems.

## Gate Purpose

The purpose of this gate is to decide what must be true before LIMA can extend fixtures/contracts around HumanInput intake for Sparkbot-like chat and voice inputs.

This gate does not approve extraction implementation. It only defines the conditions for Phase 4.4 Boundary Fixture Contract Extension, if approved.

## Selected Candidate

Selected candidate from Phase 4.2:

- HumanInput intake boundary for chat and voice.

Candidate classification:

- non-executing input boundary
- shell-facing reference boundary
- before IntentEnvelope
- before GuardianDecision
- before model harness
- before tool exposure
- before execution

## Allowed Future Phase 4.4 Shape

If Phase 4.4 is approved, it may extend fixture/contract metadata for synthetic HumanInput intake records.

Allowed fixture/contract topics:

- synthetic input identifiers
- input kind such as text or voice
- shell reference metadata
- channel, room, or conversation reference metadata
- actor and session reference metadata
- passive trust-context reference metadata
- redacted content references or summaries
- transcript confidence and normalization metadata
- attachment/file references
- privacy, redaction, retention, and visibility classes
- owner-autonomy context references
- lineage seed references
- explicit handoff requirements to future IntentEnvelope and GuardianDecision boundaries

This work must remain describe-only and non-executing.

## Safety Requirements

Any Phase 4.4 follow-up must prove:

- HumanInput cannot parse raw language into action.
- HumanInput cannot call models.
- HumanInput cannot select, expose, or execute tools.
- HumanInput cannot approve or enforce policy.
- HumanInput cannot write terminal/PTY input.
- HumanInput cannot call robotics or physical-world drivers.
- HumanInput cannot persist audit data.
- HumanInput cannot perform live auth/session/trust lookup.
- HumanInput cannot import or wire Sparkbot.
- Raw text and transcripts must use synthetic, redacted, or referenced content in fixtures.
- Actor, session, room, shell, trust, and autonomy fields must be references only.
- The next boundary after HumanInput must remain IntentEnvelope/IntentCompiler work.
- Consequential behavior must remain blocked until a later GuardianDecision gate.

## Required Tests For Future Phase 4.4

Future Phase 4.4 tests must include:

- fixture shape tests for text and voice examples
- checks that input records have no execution capability
- checks that no Sparkbot modules are imported
- checks that no runtime adapter modules are added
- checks that no raw private or operational content is embedded
- checks that voice examples include transcript confidence metadata
- checks that source identity fields are references rather than live lookup
- checks that no model, tool, terminal, robotics, approval, enforcement, or audit persistence path exists

## Hard Blockers

The following remain hard blockers:

- Sparkbot imports, wiring, route imports, or code copy
- production Sparkbot adapter implementation
- real auth/session/trust lookup
- natural-language parsing into action
- real IntentCompiler
- real GuardianDecision
- model calls
- tool exposure or tool execution
- terminal/PTY execution
- robotics command execution
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot, drone, IoT, or physical-world control

## Phase 4.3 GO

Phase 4.3 may add:

- this safety gate document
- static safety gate fixture metadata
- static safety gate tests
- project tracking updates

## Phase 4.3 NO-GO

Phase 4.3 must not add:

- runtime behavior
- executable pipeline
- test-only composition harness
- Sparkbot import, wiring, route import, or code copy
- model calls
- tool execution
- terminal or PTY execution
- robotics command execution
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

## Gate Decision

GO for Phase 4.4 Boundary Fixture Contract Extension if explicitly approved.

NO-GO for runtime extraction implementation.

NO-GO for Sparkbot integration.

NO-GO for product shell implementation.

NO-GO for physical-world action.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
