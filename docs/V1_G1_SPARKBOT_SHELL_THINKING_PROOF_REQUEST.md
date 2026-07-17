# V1-G1 Sparkbot_shell Thinking Proof Request

This document requests the next Sparkbot_shell proof packet for V1 readiness gap `V1-G1`.

It is a request only. It does not approve LIMA runtime behavior, Sparkbot_shell wiring into LIMA, provider/model calls, GuardianDecision creation, approval enforcement, persistence, haptic device behavior, file mutation, browser/network behavior, robotics, or physical-world behavior.

## Request Target

- V1 gap: `V1-G1`
- Gap name: Sparkbot_shell `thinking` / progress proof
- Source target: `docs/V1_PRODUCT_READINESS_TARGET.md`
- Gap matrix: `docs/V1_READINESS_GAP_MATRIX.md`
- Requested consumer repo: `Sparkbot_shell`
- Requested proof branch name: `sparkbot-shell-thinking-state-proof-packet`

## Why This Is Needed

V1 shell readiness needs source-backed evidence that Sparkbot_shell can represent an in-band `thinking`, progress, or streaming state before claiming Sparkbot-style UX parity.

Static/docs-only `thinking` labels are not enough for this gap. LIMA needs evidence that the shell source can actually enter and render the state in a local/static or testable shell path.

## Requested Sparkbot_shell Files

Sparkbot_shell should provide a proof packet with at least:

- `docs/proof_packets/SPARKBOT_SHELL_THINKING_STATE_PROOF_PACKET.md`
- `docs/audits/SPARKBOT_SHELL_THINKING_STATE_PROOF_AUDIT.md`
- `tests/fixtures/sparkbot_shell_thinking_state_proof_packet.json`
- `tests/test_sparkbot_shell_thinking_state_proof_packet.py`

## Required Evidence

The packet should show:

- source file paths for the state implementation or rendering path
- evidence that `thinking` / progress / streaming is a real shell state, not only a document label
- at least one transition from `received` to `thinking`
- at least one transition from `thinking` to `preview_ready`, `completed`, `blocked`, or `failed_safe`
- desktop behavior notes, if applicable
- mobile/narrow viewport behavior notes, if applicable
- haptic notes, if any haptic intent or feedback is associated with the state
- static tests or fixture checks that prove the proof packet fields are present
- explicit boundary statements that no LIMA runtime behavior was added

## Required Machine-Readable Fields

The Sparkbot_shell fixture should include:

- `proof_gap_id`: `V1-G1`
- `state_name`: `thinking`
- `source_backed_thinking`: true
- `docs_fixture_only_thinking`: false
- `thinking_source_files`
- `thinking_render_entrypoints`
- `state_transitions`
- `desktop_behavior_reviewed`
- `mobile_behavior_reviewed`
- `haptics_shell_owned`
- `lima_owns_haptics`: false
- `haptic_implementation_added`
- `lima_runtime_behavior_added`: false
- `lima_runtime_wiring_added`: false
- `sparkbot_code_copied_to_lima`: false
- `provider_model_routing_added`: false
- `guardian_decision_runtime_added`: false
- `approval_enforcement_added`: false
- `execution_dispatch_persistence_added`: false
- `browser_file_network_device_robotics_behavior_added`: false
- `production_readiness_claimed`: false

## Acceptance Criteria

LIMA can accept the proof as source-backed shell UX evidence only if:

- `thinking` is source-backed in Sparkbot_shell
- the packet names concrete source files and render/transition entrypoints
- transitions into and out of `thinking` are represented
- fixture/static tests pass in Sparkbot_shell
- haptics remain shell-owned
- no LIMA runtime behavior, wiring, or ownership is claimed
- no provider/model/tool/browser/file/network/device/robotics behavior is claimed through LIMA
- no production or V1 readiness claim is made from this one packet

## Rejection Criteria

LIMA should reject or return the proof for clarification if:

- `thinking` is docs/fixture-only
- source files or render entrypoints are missing
- the packet treats haptics as LIMA-owned behavior
- the packet claims live LIMA runtime integration
- the packet claims GuardianDecision runtime authority or approval enforcement
- the packet claims provider/model routing through LIMA
- the packet claims execution, dispatch, persistence, browser/file/network/device/robotics behavior, or production readiness

## LIMA Boundary

This request keeps LIMA in docs/tests/fixtures-only status for `V1-G1`.

LIMA will intake the future Sparkbot_shell packet as evidence only. It will not wire Sparkbot_shell, import Sparkbot_shell, import Sparkbot, copy Sparkbot code, change runtime exports, approve runtime implementation, or claim V1 readiness from this request.

## Recommended Next Step

Ask Sparkbot_shell to create the requested `sparkbot-shell-thinking-state-proof-packet` branch and deliver the proof packet. After delivery, LIMA should create a separate intake/audit lane for the packet.
