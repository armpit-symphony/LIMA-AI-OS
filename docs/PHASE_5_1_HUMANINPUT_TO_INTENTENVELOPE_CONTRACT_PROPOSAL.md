# Phase 5.1 HumanInput to IntentEnvelope Contract Proposal

Phase 5.1 proposes the HumanInput to IntentEnvelope boundary contract as static non-runtime metadata.

This is docs/tests/fixtures only. It is not a bridge implementation, not test-only bridge code, not a real IntentCompiler, not runtime wiring, not Sparkbot integration, not authorization, not approval enforcement, not execution, not audit persistence, and not a trust lookup.

## Contract Rule

HumanInput may become an IntentEnvelope candidate only as an explicitly marked non-executable test/specification artifact.

The proposed contract must preserve:

- HumanInput reference and source metadata.
- Operator intent summary.
- Requested action type.
- Target reference.
- Risk tier.
- Required approval state.
- Confidence and evidence references.
- Trust and autonomy references as passive metadata.
- Privacy, redaction, retention, and visibility metadata.
- Not-executable-yet status.
- Lineage seed references.

## Proposed Candidate States

- `proposed`
- `ready_for_review`
- `approval_required`
- `denied`
- `blocked_missing_metadata`
- `blocked_unsafe_request`

These states are descriptive only. They do not enforce approval, execute actions, persist audit, call models, call tools, or create GuardianDecision records.

## Required Invariants

- HumanInput is not an execution command.
- IntentEnvelope candidate is not authorization.
- Operator intent is not automatic permission.
- Raw text is inert.
- Explicit typed metadata is required.
- GuardianDecision remains required before consequential behavior.
- No bridge code or runtime wiring is approved.

## Recommended Next Phase

Phase 5.2 - Test-only Bridge Harness Proposal.

That phase may propose a future test-only harness, but must not implement it.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
