# Phase 5.6 HumanInput Runtime Bridge Safety Gate / Next-Scope Decision Record

Phase 5.6 defines the safety gate for anything that may follow the Phase 5.4 test-only HumanInput to IntentEnvelope bridge helper and the Phase 5.5 readiness review.

This is docs/tests/fixtures only. It does not implement a live/runtime HumanInput to IntentEnvelope bridge, does not change helper behavior, does not modify `tests/support/`, does not modify `lima/`, does not add a live adapter, does not wire Sparkbot, does not implement real IntentCompiler behavior, does not implement real GuardianDecision behavior, does not enforce approval, does not execute, and does not persist audit.

## Safety Gate Decision

The Phase 5.4 helper remains test-only. Its keyword risk classifier is test metadata only and must not be reused as runtime classifier logic.

Any future live/runtime HumanInput to IntentEnvelope bridge requires a separate explicit Phil approval. That approval must start with a runtime design proposal before implementation. The next safe lane, if approved later, should be planning/design only, not implementation.

Live HumanInput to IntentEnvelope behavior remains blocked.

## Non-bypass Rules

- HumanInput is intent context, not execution permission.
- Operator, admin, Phil, trusted, or similar wording cannot bypass approval.
- Execution, approval enforcement, audit persistence, file mutation, shell behavior, browser behavior, network behavior, robotics behavior, and physical-world action remain out of scope.
- IntentCompiler runtime behavior and GuardianDecision runtime behavior remain blocked.

## Next-Scope Options

Phil may choose one of these next:

- Option A: stop Phase 5 here and audit/archive the lane.
- Option B: continue with a docs/tests/fixtures-only runtime bridge design proposal.
- Option C: continue with a runtime threat model only.
- Option D: defer runtime bridge work and return to broader OS roadmap planning.

No option is pre-approved by this phase. Phase 5.7 or any next phase requires explicit operator approval before work begins.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
