# V1-G4 Real GuardianDecision And Live Approval Path Audit

## Audit Verdict

Verdict: `accept_static_guardian_decision_live_approval_path_gate_only`.

`V1-G4` satisfies the static request to define a future real `GuardianDecision` and live approval path gate. It is insufficient for runtime authority, live approval enforcement, or V1 product readiness.

## Audit Questions

Did V1-G4 define the required future decision outcome families?

- Yes. The gate defines `allow`, `confirm`, `deny`, `privileged`, `expired`, `revoked`, and `blocked`.

Did V1-G4 map existing GuardianDecision statuses to V1 outcome families?

- Yes. The gate maps `approved`, `needs_human_confirmation`, `needs_operator_pin`, `needs_breakglass`, `denied`, `expired`, `revoked`, `superseded`, `needs_clarification`, and `escalated`.

Did V1-G4 preserve approval metadata as subordinate to GuardianDecision?

- Yes. The gate requires decision plus approval metadata for high/critical/destructive actions and rejects approval metadata as replacement authority.

Did V1-G4 provide machine-readable fixture evidence?

- Yes. `tests/fixtures/runtime_extraction/v1_g4_real_guardian_decision_live_approval_path_gate.json` summarizes the static gate and lists all case fixtures.

Did V1-G4 evaluate allow, confirm, deny, privileged, expired, revoked, and blocked cases?

- Yes. The case fixtures cover each required outcome family.

Did V1-G4 preserve `CANDIDATE_ONLY` API status?

- Yes. The aggregate fixture keeps `api_status: CANDIDATE_ONLY`.

Did V1-G4 add real GuardianDecision runtime behavior?

- No. The branch adds only docs/tests/fixtures static evidence.

Did V1-G4 add approval enforcement or approval token issuance?

- No. Live approval capture, enforcement, and token issuance remain unimplemented.

Did V1-G4 modify `lima/`, `tests/support`, or current `lima.kernel` exports?

- No.

Did V1-G4 import, copy, or wire Sparkbot, Sparkbot_shell, or Arc-Bot-shell?

- No.

Did V1-G4 add provider/model routing?

- No. Provider/model routing remains the next gap.

Did V1-G4 avoid browser/file/network/device/robotics/haptic/physical-world behavior?

- Yes. All control flags deny those behaviors.

## Accepted Evidence

- Static future outcome-family design.
- Static GuardianDecision status-to-outcome mapping.
- Static decision-scope requirements.
- Static approval-decision dependency.
- Static fail-closed evidence for missing, forged, expired, revoked, privileged, denied, and blocked cases.
- Static allow-shape evidence for a low-risk read-only future decision that still does not execute in this branch.

## Rejected / Non-Accepted Claims

- runtime GuardianDecision authority
- live approval enforcement
- approval token issuance
- runtime execution
- dispatch
- audit persistence
- provider/model routing
- connector/tool/browser/file/network/device/robotics behavior
- shell runtime wiring
- haptic device behavior
- production readiness
- V1 product readiness

## Remaining Gaps

- no provider/model routing contract and acceptance-test design
- no haptic intent metadata contract
- no first-shell integration proof
- no audit persistence
- no runtime approval enforcement
- no production behavior

## Next Recommendation

Move to `V1-G5`: provider/model routing contract and acceptance-test design before any runtime routing implementation.
