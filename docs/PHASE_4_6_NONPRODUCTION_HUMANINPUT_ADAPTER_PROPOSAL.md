# Phase 4.6 Non-production HumanInput Adapter Proposal

Phase 4.6 proposes a future non-production shell intake adapter boundary for HumanInput.

This is proposal metadata only. It is not a HumanInput adapter, not executable, not runtime wiring, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not trust lookup.

## Purpose

The proposal describes how a future shell intake adapter could convert selected shell input context into the existing HumanInput boundary fixture/contract shape from Phase 4.4.

The proposal exists so a later explicitly approved phase can review adapter shape before any code is introduced.

## Proposed Adapter Boundary

Future adapter role:

- receive selected shell input context
- normalize it into a HumanInput-shaped record
- preserve source, actor, session, trust, privacy, lineage, and handoff references
- return non-authorizing HumanInput metadata

Future adapter non-role:

- no execution
- no authorization
- no approval
- no trust lookup
- no live session lookup
- no Sparkbot import or wiring
- no IntentCompiler behavior
- no GuardianDecision behavior
- no model/tool/terminal/robotics behavior
- no audit persistence

## Expected Source Inputs

A future proposal may describe shell intake source inputs such as:

- shell reference
- channel, room, or conversation reference
- input kind, such as text or voice transcript
- actor reference
- session reference
- passive trust/autonomy references
- redacted content reference or summary
- transcript confidence metadata for voice
- attachment/file references
- privacy/redaction/retention/visibility hints

All source values remain references. No live lookup is approved.

## Expected HumanInput Output Contract

The proposed output should match the Phase 4.4 HumanInput fixture contract shape:

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

Voice-shaped outputs must include transcript confidence metadata.

## Metadata Handling

The proposal preserves these rules:

- source metadata is reference-only
- actor/session metadata is reference-only
- trust/autonomy metadata is passive and non-granting
- privacy/redaction/retention/visibility metadata is explicit
- lineage is a seed reference only
- handoff points to future IntentEnvelope and GuardianDecision boundaries
- all `can_*` capability flags stay false
- authority identifiers and live integration identifiers remain forbidden

## Explicit Blocked Interpretations

This proposal must not be interpreted as:

- permission to add live adapter code
- permission to modify files under `lima/`
- permission to import or wire Sparkbot
- permission to implement ARC Bot or custom bots
- permission to add runtime behavior
- permission to call models
- permission to expose or execute tools
- permission to write terminal or PTY input
- permission to call robotics or physical-world drivers
- permission to perform live auth/session/trust lookup
- permission to implement real IntentCompiler
- permission to implement real GuardianDecision
- permission to enforce approval or policy
- permission to execute actions
- permission to persist audit events

## Phase 4.6 GO

Phase 4.6 may add:

- this proposal document
- static proposal fixture metadata
- static proposal tests
- project tracking updates

## Phase 4.6 NO-GO

Phase 4.6 must not add:

- runtime behavior
- executable pipeline
- test-only composition harness
- live adapter code
- files under `lima/`
- Sparkbot import, wiring, route import, or code copy
- ARC Bot implementation
- custom bot implementation
- model calls
- tool execution
- terminal or PTY behavior
- robotics behavior
- robot or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- execution
- audit persistence
- production shell implementation

## Decision

CONDITIONAL GO for a future explicitly approved non-production HumanInput adapter design review.

NO-GO for live adapter implementation.

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
