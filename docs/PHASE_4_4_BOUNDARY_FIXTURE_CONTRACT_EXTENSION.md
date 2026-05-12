# Phase 4.4 Boundary Fixture Contract Extension

Phase 4.4 extends fixture/contract metadata for the selected HumanInput intake boundary:

`humaninput_intake_boundary_for_chat_and_voice`

This phase is docs/tests/fixtures only. It does not add runtime behavior, create live adapters, import Sparkbot, wire routes, call models, execute tools, enforce approvals, persist audit events, or control physical-world systems.

## Approved Scope

Phase 4.4 may define synthetic HumanInput intake fixture shapes for:

- text input
- voice transcript input
- shell/source metadata
- channel, room, or conversation references
- actor and session references
- passive trust and autonomy references
- transcript confidence metadata
- privacy, redaction, retention, and visibility classes
- lineage seed references
- downstream handoff requirements toward future IntentEnvelope and GuardianDecision boundaries

All examples are synthetic. Raw user content is represented by redacted summaries or reference identifiers.

## Contract Shape

Each HumanInput intake fixture record must include:

- `fixture_id`
- `boundary_id`
- `input_kind`
- `synthetic`
- `non_runtime`
- `content`
- `source`
- `actor`
- `session`
- `trust_context`
- `privacy`
- `lineage`
- `handoff`
- `capability_flags`
- `blocked_capabilities`

Voice records must also include `voice`.

## Content Rules

Fixture content must stay synthetic and non-operational.

Content fields may include:

- redacted content reference
- short synthetic summary
- normalized language marker
- attachment/file reference placeholders

Content fields must not include:

- raw private user text
- raw transcripts from a real user
- credentials or secrets
- URLs or live system addresses
- execution commands
- production configuration
- model prompts
- tool invocation payloads

## Reference Metadata Rules

Actor, session, channel, room, trust, autonomy, and shell metadata are references only.

They must not:

- perform live lookup
- verify identity
- grant trust
- approve action
- authorize execution
- represent a live session
- imply production integration

## Capability Flags

Every Phase 4.4 fixture must explicitly state that it cannot:

- parse action
- call models
- select tools
- expose tools
- execute tools
- write terminal or PTY input
- call robotics
- approve
- enforce policy
- persist audit data
- perform live auth/session/trust lookup
- import Sparkbot
- wire Sparkbot

## Handoff Rules

HumanInput intake is before IntentEnvelope and before GuardianDecision.

The only permitted handoff semantics are:

- future IntentEnvelope boundary receives a HumanInput reference
- future GuardianDecision boundary remains required before consequential behavior
- future lineage can start from a lineage seed reference
- future privacy/redaction policy must govern raw content access

The fixture cannot imply authorization, approval, execution, trust lookup, or production integration.

## Phase 4.4 GO

Phase 4.4 may add:

- this fixture/contract extension document
- synthetic text and voice HumanInput intake fixtures
- static tests proving the fixtures are inert
- project tracking updates

## Phase 4.4 NO-GO

Phase 4.4 must not add:

- runtime behavior
- executable pipeline
- test-only composition harness
- live adapter code
- Sparkbot import, wiring, route import, or code copy
- model calls
- tool execution
- terminal or PTY behavior
- robotics behavior
- live auth/session/trust lookup
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

## Decision

GO for Phase 4.5 Boundary Readiness Review.

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
