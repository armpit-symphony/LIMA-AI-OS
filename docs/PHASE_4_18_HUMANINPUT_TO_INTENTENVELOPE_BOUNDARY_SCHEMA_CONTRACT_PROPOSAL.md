# Phase 4.18 HumanInput to IntentEnvelope Boundary Schema / Contract Proposal

Phase 4.18 proposes a static, non-runtime boundary schema for a future test-only HumanInput to IntentEnvelope lane.

This is docs/tests/fixtures only. It is not a bridge implementation, not a real IntentCompiler, not runtime wiring, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not a trust lookup.

## Proposal Rule

The proposed boundary may describe what metadata must exist before a future test-only component can produce an IntentEnvelope-shaped fixture.

It must not produce an IntentEnvelope in this phase.

## Proposed Input Groups

HumanInput references:

- `input_ref`
- `boundary_id`
- `input_kind`
- `source_ref`
- `actor_ref`
- `session_ref`
- `lineage_seed_ref`

Explicit typed intent metadata:

- `intent_type`
- `action_type`
- `risk_class`
- `target_ref`
- `typed_args`
- `evidence_refs`
- `requested_tool_packs`
- `approval_level`
- `privacy_class`
- `redaction_class`
- `lineage_id`
- `reason`
- `confidence`

Safety markers:

- `raw_text_inert`
- `explicit_metadata_only`
- `no_hidden_parser`
- `no_model_call`
- `no_tool_execution`
- `no_guardian_decision`
- `no_authorization`
- `guardian_required_before_consequential_behavior`

## Proposed Output Boundary

A future explicitly approved test-only phase may validate that explicit metadata could form an IntentEnvelope-shaped fixture.

That future shape must remain:

- test-only
- non-runtime
- non-authorizing
- before GuardianDecision
- blocked from execution
- blocked from tool/model/terminal/robot behavior
- blocked from Sparkbot wiring

## Recommended Next Phase

Phase 4.19 - HumanInput to IntentEnvelope Boundary Readiness Review.

That review should decide whether this schema proposal is clear enough before a Phase 5 gate / implementation readiness closeout.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
