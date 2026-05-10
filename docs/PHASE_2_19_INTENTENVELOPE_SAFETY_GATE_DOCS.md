# Phase 2.19 IntentEnvelope Safety Gate Docs

## Purpose

Create `docs/INTENTENVELOPE_SAFETY_GATE.md` as the standing gate for IntentEnvelope-adjacent work.

## What Was Consolidated

- explicit metadata rules
- `raw_text` inert rule
- fixture rules
- harness rules
- no-real-compiler rule
- forbidden behaviors
- PR blockers
- manual review requirements

## Decision

IntentEnvelope Safety Gate is now the standing review gate for IntentEnvelope-adjacent work.

Real IntentCompiler remains blocked.

## Non-Goals

- no real IntentCompiler
- no natural-language inference
- no execution
- no GuardianDecision creation
- no production wiring

## Acceptance Criteria

- `docs/INTENTENVELOPE_SAFETY_GATE.md` exists
- tests validate safety gate doc
- no runtime behavior added
- real IntentCompiler remains blocked
- tests pass
