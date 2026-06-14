# V1-G7 First-Shell Integration Proof Request Closeout

## Request Verdict

`V1-G7` request gate is complete.

This closeout does not complete V1-G7 itself. It creates the request and audit criteria for first-shell proof packets from `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`.

## Accepted Evidence

- The first-shell proof target is explicit.
- Required proof branches are named for all three shell repos.
- Required proof packet files are named.
- Required machine-readable fields are defined.
- Required shell response states and status mappings are defined.
- Haptic ownership boundaries are preserved.
- Destructive edit/delete operator approval expectations are explicit.
- Approval, `GuardianDecision`, provider/model routing, audit/evidence, connector/tool, and physical-world classifications are required.
- LIMA audit criteria are defined.
- Existing local partial evidence is recorded as partial only, not accepted as V1-G7 completion.

## Rejected / Non-Accepted Claims

- first-shell integration proof complete
- live LIMA runtime parity
- shell runtime wiring
- provider/model runtime routing through LIMA
- runtime `GuardianDecision` authority
- live approval enforcement
- haptic device behavior through LIMA
- audit persistence
- runtime export cleanup approval
- final API freeze approval
- production readiness
- V1 product readiness

## Remaining V1-G7 Blockers

- `Sparkbot_shell` V1-G7 proof packet not yet delivered to LIMA.
- `Sparkbot` V1-G7 proof packet not yet delivered to LIMA.
- `Arc-Bot-shell` V1-G7 proof packet not yet delivered to LIMA.
- LIMA intake audits for all three shell packets are not complete.
- Consolidated V1-G7 closeout is not complete.
- Live runtime wiring remains unapproved.

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Shell repos changed: no.
- Provider/model routing added: no.
- Provider/model calls added: no.
- Runtime `GuardianDecision` added: no.
- Approval enforcement added: no.
- Haptic device behavior added: no.
- Device vibration command added: no.
- Sparkbot_shell wiring added: no.
- Sparkbot import added: no.
- Sparkbot code copied: no.
- Arc-Bot-shell wiring added: no.
- Execution, dispatch, or persistence added: no.
- Browser/file/network/device/robotics behavior added: no.
- Physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Choices

Option `V1-G7A`: Ask `Sparkbot_shell` for its V1-G7 proof packet first, then intake it in LIMA.

Option `V1-G7B`: Ask `Sparkbot` for its V1-G7 behavior-reference proof packet first, then intake it in LIMA.

Option `V1-G7C`: Ask `Arc-Bot-shell` for its V1-G7 proof packet first, then intake it in LIMA.

Option `V1-G7D`: Ask all three shells for proof packets in parallel, then create one LIMA intake branch per returned packet.

## Recommendation

Recommended: `V1-G7D`.

V1-G7 is a compatibility gate across three first shells. The safest next step is to request all three proof packets in parallel while keeping LIMA static and evidence-only. LIMA should then intake each packet separately before any consolidated V1-G7 closeout or runtime wiring proposal.
