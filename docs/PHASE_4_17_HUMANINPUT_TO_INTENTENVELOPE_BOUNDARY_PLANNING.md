# Phase 4.17 HumanInput to IntentEnvelope Boundary Planning

Phase 4.17 opens the HumanInput to IntentEnvelope boundary planning lane after the HumanInput boundary lane closeout.

This is docs/tests/fixtures only. It does not implement a bridge, schema, adapter, runtime path, IntentCompiler, GuardianDecision, approval, enforcement, execution, audit persistence, live lookup, model/tool/terminal/robot behavior, or Sparkbot wiring.

## Planning Question

What should the next safe non-runtime lane examine before any HumanInput to IntentEnvelope schema proposal?

## Source Context

- Phase 4.16 closed the HumanInput boundary lane.
- `docs/INTENTENVELOPE_SAFETY_GATE.md` is the standing gate for IntentEnvelope-adjacent work.
- Phase 2.14 through Phase 2.20 already established that IntentEnvelope test work must use explicit typed metadata and must not infer intent from raw text.

## Planning Direction

The next phase may propose a boundary schema/contract for a future test-only HumanInput to IntentEnvelope path.

That proposal must preserve:

- HumanInput is not IntentEnvelope.
- IntentEnvelope is not authorization.
- GuardianDecision remains mandatory before consequential behavior.
- Raw text remains inert.
- Explicit typed metadata is required for test IntentEnvelope shapes.
- No hidden parser.
- No heuristic free-text interpretation.
- No model calls.
- No tool execution.
- No live adapter code.
- No production Sparkbot wiring.
- No approval, enforcement, execution, or audit persistence.

## Recommended Next Phase

Phase 4.18 - HumanInput to IntentEnvelope Boundary Schema / Contract Proposal.

That phase should remain docs/tests/fixtures only and propose metadata shape, not implementation.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
