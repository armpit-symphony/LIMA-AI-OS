# Phase 4.10 Non-production Test-only HumanInput Adapter Harness Proposal

Phase 4.10 proposes a future test-only HumanInput adapter harness.

This is proposal metadata only. It is not harness code, not adapter code, not executable, not runtime wiring, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not a trust lookup.

## Purpose

The proposed future harness would validate synthetic shell intake metadata against the HumanInput boundary fixture contract in a later explicitly approved phase.

The proposal exists to describe the harness shape before any code is introduced.

## Proposed Future Harness Purpose

A future test-only harness may validate that synthetic shell intake metadata can be compared with the HumanInput boundary fixture contract without creating runtime behavior.

It may check:

- synthetic shell/channel/room references
- synthetic actor/session references
- passive trust/autonomy references
- transcript confidence metadata
- privacy, redaction, retention, and visibility metadata
- lineage seed references
- future IntentEnvelope handoff requirements as non-executable metadata
- future GuardianDecision handoff requirements as non-executable metadata
- HumanInput-only output shape expectations

## Expected Synthetic Inputs

The future harness proposal may describe synthetic input records only:

- synthetic text intake metadata
- synthetic voice transcript metadata
- shell, channel, room, actor, and session references
- passive trust and autonomy references
- redacted content references or summaries
- transcript confidence values
- privacy and retention hints
- lineage seed references

No live shell, session, auth, trust, Sparkbot, model, tool, terminal, robot, or production source is approved.

## Expected HumanInput Fixture Output Shape

The proposal may describe validation against the Phase 4.4 HumanInput fixture contract:

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

The future harness must not create IntentEnvelope, GuardianDecision, ApprovalMetadata, execution records, audit records, or runtime objects.

## Safety Boundaries

Phase 4.10 keeps the following blocked:

- harness code
- live adapter code
- files under `lima/`
- Sparkbot imports or wiring
- runtime behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- execution
- audit persistence
- model calls
- tool execution
- terminal or PTY behavior
- robot or physical-world behavior
- live trust/session/auth lookup
- production shell integration

## Validation Requirements For Any Future Harness Proposal

A later phase that proposes harness code must first prove:

- the harness is test-only
- the harness accepts synthetic fixtures only
- the harness validates HumanInput shape only
- the harness has no live source lookup
- the harness has no Sparkbot import or wiring
- the harness has no runtime adapter behavior
- the harness does not call models, tools, terminals, robots, or drivers
- the harness does not approve, enforce, execute, or persist audit data
- the harness does not imply production adapter readiness

## Decision

CONDITIONAL GO for Phase 4.11 Test-only HumanInput Adapter Harness Proposal Readiness Review.

NO-GO for test-only harness implementation.

NO-GO for live adapter implementation.

NO-GO for runtime extraction implementation.

NO-GO for Sparkbot integration.

NO-GO for physical-world action.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
