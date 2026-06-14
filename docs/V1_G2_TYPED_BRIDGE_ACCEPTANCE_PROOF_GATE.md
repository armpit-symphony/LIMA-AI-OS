# V1-G2 Typed Bridge Acceptance Proof Gate

This document creates the approval gate for V1 readiness gap `V1-G2`: typed bridge acceptance proof.

It is docs/tests/fixtures-only gate metadata. It does not implement acceptance proof cases, runtime behavior, runtime bridge behavior, a runtime test harness, `tests/support` helper behavior, shell wiring, provider/model routing, real `GuardianDecision`, approval enforcement, persistence, haptic device behavior, browser/file/network/device/robotics behavior, or production behavior.

## Gate Source

- Gate branch: `v1-g2-typed-bridge-acceptance-proof-gate`
- Source branch: `intake-sparkbot-shell-thinking-state-proof-packet`
- Source commit: `5f6472becee8c409b0a330053cf9a619e2be4d74`
- Gap matrix: `docs/V1_READINESS_GAP_MATRIX.md`
- Product target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- API status: `CANDIDATE_ONLY`

## Evidence Reviewed

- `docs/PHASE_44_0_TYPED_INTENTENVELOPE_GUARDIAN_REQUEST_BRIDGE_DESIGN_CHARTER.md`
- `docs/PHASE_45_0_TYPED_BRIDGE_ACCEPTANCE_TEST_DESIGN.md`
- `docs/PHASE_45_1_TYPED_BRIDGE_ACCEPTANCE_TEST_FIXTURE_MATRIX_SCAFFOLDING_DESIGN.md`
- `docs/PHASE_47_1_STATIC_ACCEPTANCE_TEST_IMPLEMENTATION_CHECKLIST.md`
- `docs/PHASE_48_0_IMPLEMENTATION_GATE_DECISION_CHARTER.md`
- `docs/PHASE_48_2_CONCRETE_IMPLEMENTATION_DESIGN_REVIEW.md`
- `docs/V1_PRODUCT_READINESS_TARGET.md`
- `docs/V1_READINESS_GAP_MATRIX.md`
- `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md`

## Precondition

`V1-G1` is accepted as source-backed local Sparkbot_shell `thinking` evidence only. It proves local shell UX state evidence, not live runtime parity.

The V1-G2 gate starts from that state. It does not reopen V1-G1.

## Proposed V1-G2 Proof Scope

If Phil approves the next lane, V1-G2 should create deterministic docs/tests/fixtures-only acceptance proof for:

- source request metadata
- typed IntentEnvelope candidate metadata
- Guardian request metadata
- future GuardianDecision metadata limited to absent, pending, or blocked
- kernel-to-shell status mapping that remains non-authoritative
- fail-closed negative cases for approval, authority, execution, dispatch, persistence, external-call, provider/model/tool/driver, browser/file/network/device/robotics, and physical-world claims

The proof should stay under `docs/`, `tests/fixtures/runtime_extraction/`, and `tests/`.

## Candidate Allowed Files For Next Lane

These are candidate future file names only. This gate does not create them.

- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_preview_only_positive.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_approval_bypass.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_runtime_claim.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_missing_guardian_request.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_execution_claim.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_provider_model_tool_driver_claim.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_browser_file_network_device_robotics_claim.json`
- `tests/test_typed_bridge_acceptance_preview_only.py`
- `tests/test_typed_bridge_acceptance_fail_closed.py`

## Candidate Forbidden Scope

The next lane must not modify:

- `lima/`
- `tests/support/`
- Sparkbot_shell
- Sparkbot
- Arc-Bot-shell
- adapters, drivers, persistence, runtime dispatch, shell/browser/network/file mutation, robotics, haptic device, or physical-world paths
- background workers, queues, daemons, subprocesses, threads, or database-write paths

## Required Future Assertions

The next lane must prove:

- raw natural language is not execution authority
- typed IntentEnvelope candidate metadata is not authority
- Guardian request metadata is not GuardianDecision authority
- GuardianDecision metadata cannot grant approval, execution, dispatch, persistence, adapter access, model calls, tool calls, driver calls, provider routing, external calls, robotics, haptics, or physical-world action
- `proposed` maps to shell packet status `preview_only`
- `needs_review` maps to shell packet status `explain_plan`
- `blocked` maps to shell packet status `blocked`
- packet statuses include `preview_only`, `explain_plan`, `blocked`, and `deferred`
- every negative case fails closed

## Approval Question

Does Phil approve implementing V1-G2 as a docs/tests/fixtures-only typed bridge acceptance proof limited to the candidate allowed files above, while preserving all forbidden scopes and keeping runtime behavior, `lima/`, `tests/support`, shell repos, provider/model routing, real `GuardianDecision`, approval enforcement, persistence, haptic device behavior, and physical-world behavior blocked?

Current answer: `not_approved_by_this_gate`.

## Boundary Result

- Runtime behavior added: no.
- LIMA runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Sparkbot_shell wired into LIMA: no.
- Sparkbot imported into LIMA: no.
- Sparkbot code copied into LIMA: no.
- Arc-Bot-shell wired into LIMA: no.
- Provider/model routing added: no.
- GuardianDecision runtime added: no.
- Approval enforcement added: no.
- Execution, dispatch, or persistence added: no.
- Browser/file/network/device/robotics behavior added: no.
- Haptic device behavior added: no.
- Final API freeze approved: no.
- Runtime export cleanup approved: no.
- V1 product readiness claimed: no.

## Recommended Next Step

Recommended: approve and implement the V1-G2 docs/tests/fixtures-only typed bridge acceptance proof as the next lane.

After V1-G2 proof passes, the next smallest V1 step should be `V1-G3`: destructive edit/delete operator-approval contract design and static acceptance tests.
