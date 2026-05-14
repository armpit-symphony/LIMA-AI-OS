# Phase 9.2 Non-executing Kernel Intake-to-Candidate Coordinator Implementation

Phase 9.2 implements the first narrow Phase 9 runtime slice: a pure in-process, non-executing kernel intake-to-candidate coordinator.

This phase touches only Phase 8.1 eligible runtime files:

- `lima/kernel/__init__.py`
- `lima/kernel/intake_candidate.py`

This phase does not implement HumanInput runtime bridge behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Implemented Behavior

The coordinator accepts only already-normalized synthetic intake metadata marked `synthetic: true` and `test_only: true`.

It returns a plain dictionary containing non-executable candidate metadata:

- source and source channel
- operator intent
- normalized request
- requested action
- conservative risk tier
- approval state
- non-executable markers
- blocked/not-ready reason
- provenance
- future Guardian review boundary references

## Safety Properties

Every candidate output has:

- `executable: false`
- `execution_allowed: false`
- `side_effects_allowed: false`
- `approved: false`
- `needs_guardian_review: true`
- `intent_envelope_created: false`
- `guardian_decision_created: false`
- `phase_5_humaninput_runtime_bridge_gated: true`

The coordinator fails closed for malformed input, missing synthetic/test-only markers, raw HumanInput-like payload keys, stale intake, replayed intake, and unknown action categories.

Operator/admin/Phil/trusted wording is preserved only as metadata. It never bypasses approval or creates execution authority.

## Still Blocked

- HumanInput runtime bridge behavior.
- Real IntentEnvelope creation.
- Real GuardianDecision creation.
- IntentCompiler runtime behavior.
- Approval enforcement.
- Execution.
- Audit persistence.
- Sparkbot imports or wiring.
- Live adapters.
- Model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects.

## Rollback / Audit Proof

The implementation is independently revertible because it is limited to two new `lima/kernel` files plus Phase 9.2 docs, fixtures, and tests. Audit proof remains test evidence only; no audit persistence is added.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
