# V1-G4 Real GuardianDecision And Live Approval Path Closeout

## Intake Verdict

`V1-G4` is complete as a static real `GuardianDecision` and live approval path design gate.

This closeout is docs/tests/fixtures-only. It does not make LIMA V1 product-ready.

## Accepted Evidence

- Future decision outcome families are defined:
  - `allow`
  - `confirm`
  - `deny`
  - `privileged`
  - `expired`
  - `revoked`
  - `blocked`
- Existing `GuardianDecisionStatus` values are mapped to V1 outcome families.
- Future decision scope requirements are recorded.
- Approval metadata remains required evidence for high/critical/destructive actions but does not replace `GuardianDecision`.
- Static fixture cases cover allow, confirm, deny, privileged, expired, revoked, and blocked outcomes.
- Static tests verify all outcomes remain non-executing in this branch.

## Rejected / Non-Accepted Claims

- real `GuardianDecision` runtime behavior
- live approval enforcement
- live approval capture
- approval token issuance
- execution, dispatch, or persistence
- provider/model routing
- connector/tool/browser/file/network/device/robotics behavior
- shell runtime wiring
- haptic device behavior
- production readiness
- V1 product readiness

## Remaining V1 Blockers

- no provider/model routing contract and acceptance-test design
- no provider/model routing runtime
- no haptic intent metadata contract
- no first-shell integration proof across `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`
- no LIMA runtime wiring
- no audit persistence
- no production behavior

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Real `GuardianDecision` added: no.
- Approval enforcement added: no.
- Approval token issuance added: no.
- Provider/model routing added: no.
- Sparkbot_shell wiring added: no.
- Sparkbot import added: no.
- Sparkbot code copied: no.
- Arc-Bot-shell wiring added: no.
- Execution, dispatch, or persistence added: no.
- Browser/file/network/device/robotics behavior added: no.
- Haptic device behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Choices

Option `V1-G5`: provider/model routing contract and acceptance-test design under Guardian, shell tool-pack scope, secret policy, and audit/evidence rules.

Option `V1-G6`: haptic intent metadata as shell-contract metadata only.

Option `V1-G7`: first-shell integration proof packets for `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`.

## Recommendation

Recommended: `V1-G5`.

`V1-G4` closes the static decision/approval-path design gate. Provider/model routing is now the next smallest safe V1 gap because model calls are consequential and must be constrained before shell runtime integration can be claimed.
