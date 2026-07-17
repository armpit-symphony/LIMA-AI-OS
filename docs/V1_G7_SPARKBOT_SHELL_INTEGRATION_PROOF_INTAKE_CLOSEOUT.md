# V1-G7 Sparkbot_shell Integration Proof Intake Closeout

## Intake Verdict

Recommended verdict: `accept_static_shell_integration_evidence_only`

Sparkbot_shell delivered the requested V1-G7 proof packet. LIMA can accept it as static shell integration evidence only.

## Accepted Evidence

- Requested proof packet is present.
- Requested audit is present.
- Machine-readable fixture is present.
- Static proof test is present.
- Sparkbot_shell validation is reported as passing.
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
- Haptics remain shell-owned.
- LIMA does not own haptic device behavior.
- Destructive edit/delete posture remains blocked or operator-approval-required before runtime.
- No LIMA runtime wiring is added.
- No Sparkbot code is copied/imported into LIMA.
- No unsafe provider/model/tool/file/network/browser/device/robotics claims are accepted.

## Rejected / Non-Accepted Claims

Do not accept this packet as proof of:

- live LIMA runtime parity
- live Sparkbot-style streaming parity
- real approval enforcement
- real `GuardianDecision` authority
- provider/model runtime routing
- durable audit persistence
- haptic device implementation
- connector sends, tool dispatch, shell execution, file mutation, browser/network behavior, device control, robotics, or physical-world behavior
- runtime export cleanup approval
- final API freeze
- V1 product readiness
- production readiness

## Remaining V1-G7 Blockers

- `Sparkbot` V1-G7 proof packet not delivered.
- `Arc-Bot-shell` V1-G7 proof packet not delivered.
- `Sparkbot` LIMA intake audit not complete.
- `Arc-Bot-shell` LIMA intake audit not complete.
- Consolidated V1-G7 closeout not complete.
- No live LIMA runtime wiring.
- No real approval enforcement.
- No real `GuardianDecision` path.
- No provider/model runtime routing.
- No audit persistence.
- No haptic device behavior.
- No production behavior.

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Sparkbot_shell wiring added to LIMA: no.
- Sparkbot import added to LIMA: no.
- Sparkbot code copied to LIMA: no.
- Arc-Bot-shell wiring added to LIMA: no.
- Provider/model routing added: no.
- Provider/model calls added: no.
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

Option `V1-G7S`: Create or request the `Sparkbot` V1-G7 behavior-reference proof packet, then intake it in LIMA.

Option `V1-G7A`: Create or request the `Arc-Bot-shell` V1-G7 proof packet, then intake it in LIMA.

Option `V1-G7C`: Stop after this Sparkbot_shell intake and wait for external shell packets.

## Recommendation

Recommended: `V1-G7S`.

Sparkbot_shell is now accepted as static V1-G7 evidence. The next safest step is to produce or request the `Sparkbot` behavior-reference packet, because Sparkbot is the R&D behavior reference for approvals, Guardian posture, provider/model routing, memory/audit posture, and shell response feel. Keep LIMA docs/tests/fixtures-only until all first-shell packets are delivered and audited.
