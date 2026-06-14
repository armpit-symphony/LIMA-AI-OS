# V1-G5 Provider/Model Routing Closeout

## Intake Verdict

`V1-G5` is complete as a static provider/model routing contract and acceptance-test design.

This closeout is docs/tests/fixtures-only. It does not make LIMA V1 product-ready.

## Accepted Evidence

- Provider/model route families are defined.
- Required route metadata is defined.
- Guardian, shell, tool-pack, secret, budget, privacy, and audit gates are explicit.
- Fallback route inheritance is constrained.
- Static fixtures cover safe route shape and fail-closed routing cases.
- Static tests verify no runtime provider/model calls are added.

## Rejected / Non-Accepted Claims

- runtime provider/model routing
- provider/model calls
- provider readiness checks
- live Token Guardian routing
- fallback execution
- secret lookup
- runtime `GuardianDecision`
- approval enforcement
- audit persistence
- shell runtime wiring
- haptic device behavior
- production readiness
- V1 product readiness

## Remaining V1 Blockers

- no haptic intent metadata contract
- no first-shell integration proof across `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`
- no LIMA runtime wiring
- no audit persistence
- no runtime provider/model routing
- no production behavior

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Provider/model routing added: no.
- Provider/model calls added: no.
- Secret access added: no.
- Runtime `GuardianDecision` added: no.
- Approval enforcement added: no.
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

Option `V1-G6`: haptic intent metadata as shell-contract metadata only.

Option `V1-G7`: first-shell integration proof packets for `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`.

Option `V1-G8`: audit/evidence persistence design, storage contract, and threat model.

## Recommendation

Recommended: `V1-G6`.

Provider/model routing is now statically constrained. Haptic intent metadata is the next smallest safe shell-contract gap because shells own rendering and device behavior, so LIMA can define intent metadata without adding physical or device behavior.
