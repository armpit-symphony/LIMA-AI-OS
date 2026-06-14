# V1-G6 Haptic Intent Metadata Contract

## Verdict

`V1-G6` is complete as a static haptic intent metadata contract and shell fixture proof.

This document is docs/tests/fixtures-only. It does not add runtime behavior, shell wiring, haptic device behavior, tactile hardware calls, vibration commands, provider/model routing, runtime `GuardianDecision`, approval enforcement, execution, dispatch, persistence, robotics behavior, or production behavior.

## Purpose

V1 requires shell response states to feel consistent across the first shell consumers:

- `Sparkbot_shell`
- `Sparkbot`
- `Arc-Bot-shell`

Haptics are part of shell experience, not LIMA device authority. LIMA may define non-device-specific haptic intent metadata so shells can render their own feedback consistently. Shells own tactile rendering, animation, vibration APIs, accessibility preferences, and device-specific feedback.

## Source Evidence

- `docs/V1_PRODUCT_READINESS_TARGET.md` accepts shell haptic intent support as a future V1 capability.
- `docs/V1_READINESS_GAP_MATRIX.md` identifies `V1-G6` as haptic intent metadata.
- `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md` confirms Sparkbot_shell owns haptics and LIMA does not own device feedback.
- `docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md` recommends `V1-G6` after provider/model routing is statically constrained.
- `docs/SHELL_RESPONSE_STATE_GUIDANCE.md` and Sparkbot-style UX notes define the shell response-state vocabulary that haptic intent metadata must follow when present.

## Required Shell State Mapping

The static V1-G6 contract maps response states to intent families only:

| Shell response state | Haptic intent family | Notes |
| --- | --- | --- |
| `received` | `soft_ack` | Acknowledges input receipt without implying execution. |
| `thinking` | `progress_pulse` | Indicates local shell progress or streaming posture without implying model routing. |
| `preview_ready` | `light_tap` | Indicates a preview or candidate is available. |
| `blocked` | `warning` | Indicates a blocked state without device enforcement. |
| `needs_approval` | `attention` | Indicates operator attention is needed, not that approval is granted. |
| `completed` | `success` | Indicates shell result completion. |
| `failed_safe` | `error_alert` | Indicates safe failure or fail-closed behavior. |
| `deferred` | `neutral_hold` | Indicates work is deferred or queued outside current runtime behavior. |

## Required Haptic Intent Metadata

Any future haptic intent metadata must be non-device-specific and may carry only:

- `intent_id`
- `source_shell`
- `response_state`
- `packet_status`
- `kernel_status`
- `haptic_intent_family`
- `urgency`
- `intensity_hint`
- `duration_hint_ms`
- `accessibility_respect`
- `fallback_visual_state`
- `fallback_auditory_state`
- `reason_code`
- `audit_evidence_ref`
- `policy_version`

The metadata is descriptive shell-contract data. It is not permission to vibrate, actuate, call a device API, bypass accessibility settings, or render anything in LIMA.

## Forbidden Device Fields

Haptic intent metadata must not carry:

- `actuator_id`
- `device_id`
- `vibration_command`
- `motor_pattern`
- `os_haptic_api`
- `execute_haptic_now`
- `hardware_target`
- `physical_feedback_command`

If any fixture or future payload claims those fields as LIMA-owned behavior, the claim must fail closed.

## Static V1-G6 Acceptance Rules

For this branch:

- no haptic device behavior occurs
- no vibration or tactile hardware command is emitted
- no shell rendering is invoked
- no device, OS, browser, robotics, or physical-world API is called
- no runtime `GuardianDecision` is created
- no approval is granted or enforced
- no provider/model route executes
- no file, connector, or shell state is mutated
- no execution, dispatch, persistence, external call, tool call, driver call, or adapter call is allowed

Static fixture claims of LIMA-owned haptics, actuator IDs, device vibration commands, shell-rendering bypass, or `execute_haptic_now` must fail closed.

## What V1-G6 Proves

V1-G6 proves as static evidence:

- shell response states have haptic intent families
- haptic intent metadata fields are defined
- device-specific haptic fields are forbidden
- haptics remain shell-owned
- accessibility and visual/auditory fallback metadata are required
- forged device haptic claims fail closed
- LIMA remains `CANDIDATE_ONLY`

## What V1-G6 Does Not Prove

V1-G6 does not prove:

- haptic device implementation
- vibration, tactile feedback, or physical feedback
- shell rendering behavior
- runtime shell wiring
- runtime `GuardianDecision`
- approval enforcement
- provider/model routing or model calls
- audit persistence
- production readiness
- V1 product readiness

## Boundary Confirmation

- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Shell repos changed: no.
- Haptic intent metadata contract added: yes.
- Haptic device behavior added: no.
- Device vibration command added: no.
- Shell rendering invoked: no.
- Provider/model routing added: no.
- Provider/model calls added: no.
- Runtime `GuardianDecision` added: no.
- Approval enforcement added: no.
- Sparkbot_shell wired into LIMA: no.
- Sparkbot imported into LIMA: no.
- Sparkbot code copied into LIMA: no.
- Arc-Bot-shell wired into LIMA: no.
- Execution, dispatch, or persistence added: no.
- Browser/file/network/device/robotics behavior added: no.
- Physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.

## Recommended Next Step

Recommended: `V1-G7`.

The next smallest safe step is first-shell integration proof packets and LIMA intake audits for `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`, still without runtime wiring until a later explicit implementation approval.
