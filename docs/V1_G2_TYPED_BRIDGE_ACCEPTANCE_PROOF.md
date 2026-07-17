# V1-G2 Typed Bridge Acceptance Proof

This document records the V1-G2 typed bridge acceptance proof.

It is docs/tests/fixtures-only. It does not implement runtime bridge behavior, a runtime test harness, `tests/support` helpers, `lima/` changes, shell wiring, provider/model routing, real `GuardianDecision`, approval enforcement, execution, dispatch, persistence, haptic device behavior, browser/file/network/device/robotics behavior, or production behavior.

## Proof Source

- Proof branch: `v1-g2-typed-bridge-acceptance-proof`
- Gate branch: `v1-g2-typed-bridge-acceptance-proof-gate`
- Gate commit: `d8956f0838b6d1183ab625928e37c1c978af1d78`
- Gate document: `docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF_GATE.md`
- Source branch before gate: `intake-sparkbot-shell-thinking-state-proof-packet`
- Source commit before gate: `5f6472becee8c409b0a330053cf9a619e2be4d74`
- API status: `CANDIDATE_ONLY`

## Proof Files

- `tests/fixtures/runtime_extraction/v1_g2_typed_bridge_acceptance_proof.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_preview_only_positive.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_approval_bypass.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_runtime_claim.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_missing_guardian_request.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_execution_claim.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_provider_model_tool_driver_claim.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_browser_file_network_device_robotics_claim.json`
- `tests/test_typed_bridge_acceptance_preview_only.py`
- `tests/test_typed_bridge_acceptance_fail_closed.py`

## What This Proves

V1-G2 proves static typed bridge acceptance evidence for:

- source request metadata
- typed IntentEnvelope candidate metadata
- Guardian request metadata
- future GuardianDecision metadata constrained to absent, pending, or blocked
- kernel status to shell packet status mapping
- fail-closed handling for approval bypass, forged GuardianDecision authority, missing Guardian request metadata, runtime execution claims, execution/dispatch/persistence claims, provider/model/tool/driver claims, and browser/file/network/device/robotics claims

## Status Mapping Proven

The static fixtures prove the expected shell-facing packet status mapping:

- `proposed` -> `preview_only`
- `needs_review` -> `explain_plan`
- `blocked` -> `blocked`

The accepted packet status catalog is:

- `preview_only`
- `explain_plan`
- `blocked`
- `deferred`

## What This Does Not Prove

V1-G2 does not prove:

- live runtime bridge behavior
- real IntentCompiler behavior
- real Guardian request runtime behavior
- real GuardianDecision authority
- live approval enforcement
- provider/model routing
- tool, adapter, driver, browser, file, network, device, robotics, haptic device, or physical-world behavior
- audit persistence
- shell runtime wiring
- production readiness

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

## Acceptance Verdict

V1-G2 is complete as static docs/tests/fixtures acceptance proof only.

It is not runtime parity and does not approve runtime implementation.

## Recommended Next Step

Move to `V1-G3`: destructive edit/delete operator-approval contract design and static acceptance tests.
