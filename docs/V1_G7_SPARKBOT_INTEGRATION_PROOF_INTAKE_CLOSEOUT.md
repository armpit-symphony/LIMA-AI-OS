# V1-G7 Sparkbot Integration Proof Intake Closeout

## Intake Verdict

Recommended verdict: `accept_static_behavior_reference_evidence_only`

Sparkbot delivered the requested V1-G7 proof packet. LIMA can accept it as static behavior-reference evidence only.

## Accepted Evidence

- Requested proof packet is present.
- Requested audit is present.
- Machine-readable fixture is present.
- Static proof test is present.
- Sparkbot validation is reported as passing.
- All required shell response states are evaluated.
- Required packet statuses are evaluated:
  - `preview_only`
  - `explain_plan`
  - `blocked`
  - `completed`
  - `deferred`
- Required kernel mappings are preserved:
  - `proposed -> preview_only`
  - `needs_review -> explain_plan`
  - `blocked -> blocked`
- Sparkbot has source-backed `received`, `thinking`, `preview_ready`, `blocked`, `needs_approval`, `completed`, and `failed_safe` behavior.
- Sparkbot classifies `deferred` as docs/fixture-only.
- Haptics remain shell-owned.
- LIMA does not own haptic device behavior.
- Sparkbot destructive edit/delete posture requires confirmation, privileged approval, or blocking.
- Sparkbot approval, policy decision, provider/model routing, audit, spine, and tool-gating behavior is source-backed reference evidence.
- No LIMA runtime wiring is added.
- No Sparkbot code is copied/imported into LIMA.
- No unsafe provider/model/tool/file/network/browser/device/robotics claims are accepted as LIMA behavior.

## Rejected / Non-Accepted Claims

Do not accept this packet as proof of:

- live LIMA runtime parity
- Sparkbot-on-LIMA runtime parity
- LIMA runtime `GuardianDecision` authority
- LIMA approval enforcement
- LIMA provider/model runtime routing
- LIMA provider/model calls
- durable LIMA audit persistence
- LIMA haptic device implementation
- LIMA connector sends, tool dispatch, shell execution, file mutation, browser/network behavior, device control, robotics, or physical-world behavior
- runtime export cleanup approval
- final API freeze
- V1 product readiness
- production readiness

## Remaining V1-G7 Blockers

- `Arc-Bot-shell` V1-G7 proof packet not accepted by LIMA.
- `Arc-Bot-shell` LIMA intake audit not complete.
- Consolidated V1-G7 closeout not complete.
- No live LIMA runtime wiring.
- No real LIMA approval enforcement.
- No real LIMA `GuardianDecision` path.
- No LIMA provider/model runtime routing.
- No LIMA audit persistence.
- No LIMA haptic device behavior.
- No production behavior.

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Sparkbot_shell wiring added to LIMA: no.
- Sparkbot wiring added to LIMA: no.
- Sparkbot import added to LIMA: no.
- Sparkbot code copied to LIMA: no.
- Arc-Bot-shell wiring added to LIMA: no.
- Provider/model routing added to LIMA: no.
- Provider/model calls added to LIMA: no.
- Runtime `GuardianDecision` added: no.
- Approval enforcement added: no.
- Execution, dispatch, or persistence added: no.
- Browser/file/network/device/robotics behavior added: no.
- Haptic device behavior added: no.
- Physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Choices

Option `V1-G7A`: Request or normalize the `Arc-Bot-shell` V1-G7 proof packet, then intake it in LIMA.

Option `V1-G7C`: Stop after Sparkbot_shell and Sparkbot intake and wait for an external Arc-Bot-shell packet.

Option `V1-G7X`: Start consolidated V1-G7 closeout now.

## Recommendation

Recommended: `V1-G7A`.

Sparkbot_shell and Sparkbot are now accepted as static V1-G7 evidence. V1-G7 should not close until `Arc-Bot-shell` is delivered and audited. Keep LIMA docs/tests/fixtures-only until all first-shell packets are accepted.
