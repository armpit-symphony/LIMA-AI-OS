# Phase 5.4 Test-only HumanInput to IntentEnvelope Bridge Harness Implementation

Phase 5.4 implements a narrow test-only HumanInput to IntentEnvelope bridge helper under `tests/support/`.

This is not a live runtime bridge. It is not a live adapter, not Sparkbot integration, not real IntentCompiler behavior, not real GuardianDecision behavior, not authorization, not approval enforcement, not execution, not audit persistence, and not a trust lookup.

## Helper Boundary

The helper lives at `tests/support/test_only_humaninput_to_intentenvelope_bridge.py`.

It accepts only synthetic HumanInput-shaped dictionaries that explicitly declare:

- synthetic
- test-only
- non-runtime
- source metadata
- source channel
- operator intent
- requested action
- raw text
- provenance

It returns an IntentEnvelope-candidate-shaped dictionary for tests only. The candidate is always non-executable and always marks execution, side effects, authorization, approval enforcement, runtime wiring, live adapter behavior, Sparkbot integration, IntentCompiler runtime behavior, GuardianDecision behavior, and audit persistence as unavailable.

## Risk And Approval Handling

The helper classifies test-only risk conservatively:

- low-risk requests become non-executable proposed candidates
- shell and terminal requests require approval
- browser and network requests require approval
- file mutation requests require approval
- robotics and physical-world requests require approval
- unknown or ambiguous requests are blocked

Operator, admin, trusted, or Phil wording never bypasses approval. Operator intent is context, not permission.

## Failure Rules

The helper fails closed when input is missing, empty, non-synthetic, non-test-only, runtime-marked, production-marked, pre-approved, missing provenance, missing lineage seed metadata, or tied to live source/audit persistence.

## Phase 5.5 Gate

Phase 5.5 or later remains gated. A readiness review may inspect whether the Phase 5.4 helper stayed constrained, but live/runtime HumanInput to IntentEnvelope implementation is still not approved.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
