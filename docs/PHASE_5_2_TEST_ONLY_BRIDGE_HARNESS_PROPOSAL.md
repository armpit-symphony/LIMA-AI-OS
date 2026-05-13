# Phase 5.2 Test-only Bridge Harness Proposal

Phase 5.2 proposes a future test-only HumanInput to IntentEnvelope bridge harness.

This is docs/tests/fixtures only. It does not implement the harness. It is not bridge code, not a real IntentCompiler, not runtime wiring, not Sparkbot integration, not authorization, not approval enforcement, not execution, not audit persistence, and not a trust lookup.

## Proposal Rule

A future test-only bridge harness, if explicitly approved later, may validate synthetic HumanInput metadata against the Phase 5.1 contract proposal and produce IntentEnvelope-candidate-shaped test dictionaries.

Phase 5.2 must not produce those dictionaries.

## Proposed Harness Inputs

- Synthetic HumanInput fixture reference.
- Source metadata.
- Operator intent summary.
- Requested action type.
- Target reference.
- Risk tier.
- Required approval state.
- Candidate state.
- Confidence and evidence references.
- Passive trust and autonomy references.
- Privacy, redaction, retention, and visibility metadata.
- Lineage seed references.
- Explicit not-executable-yet marker.

## Proposed Harness Outputs

A future explicitly approved test-only phase may produce an IntentEnvelope-candidate-shaped test dictionary only when all required fields and safety markers are present.

That future output must remain:

- test-only
- non-runtime
- non-authorizing
- non-executable
- before GuardianDecision
- blocked from shell, browser, network, tool, model, terminal, robotics, and physical-world behavior
- blocked from Sparkbot wiring

## Failure Modes

A future test-only harness must fail closed for:

- missing synthetic/test-only markers
- missing not-executable-yet marker
- missing source metadata
- missing operator intent summary
- missing requested action type
- missing risk tier
- missing required approval state
- missing lineage seed references
- live/runtime/prod markers
- any field implying authorization, approval enforcement, execution, audit persistence, or GuardianDecision creation

## Recommended Next Phase

Phase 5.3 - Test-only Bridge Harness Readiness Review.

That review should decide whether this proposal is clear and safe enough to stop at an implementation gate before any test-only bridge harness code.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
