# Phase 4.8 HumanInput Adapter Safety Gate Docs

Phase 4.8 establishes safety gate documentation for any future HumanInput adapter work.

This is docs/tests/fixtures only. It is not a HumanInput adapter, not executable, not runtime wiring, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not a trust lookup.

## Purpose

Phase 4.7 found the Phase 4.6 HumanInput adapter proposal ready only for future adapter safety gate docs. Phase 4.8 adds that gate without adding adapter behavior.

## Safety Gate Added

The standing gate lives at `docs/HUMANINPUT_ADAPTER_SAFETY_GATE.md`.

It requires any future adapter to:

- return HumanInput only
- keep source metadata passive and reference-only
- keep trust and autonomy references non-granting
- keep transcript confidence descriptive
- keep privacy, redaction, retention, and visibility as metadata
- keep lineage seeds reference-only
- stop before IntentEnvelope
- stop before GuardianDecision
- stop before model, tool, terminal, robot, driver, approval, execution, and audit behavior

## Phase 4.8 GO

Phase 4.8 may add:

- HumanInput adapter safety gate documentation
- static safety gate fixture metadata
- static safety gate tests
- project tracking updates

## Phase 4.8 NO-GO

Phase 4.8 must not add:

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

CONDITIONAL GO for a future explicitly approved non-runtime adapter design review.

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
