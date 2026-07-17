# V1-G4 Real GuardianDecision And Live Approval Path Gate

## Verdict

`V1-G4` is complete as a static design gate for a future real `GuardianDecision` and live approval path.

This document is docs/tests/fixtures-only. It does not add runtime behavior, create real `GuardianDecision` authority, enforce approval, issue approval tokens, mutate files, wire shells, call providers/models/tools, persist audit events, add haptic device behavior, add robotics behavior, or approve production behavior.

## Purpose

V1 needs a real `GuardianDecision` and live approval path before consequential actions can execute. `V1-G4` defines the exact design gate and static fixture evidence required before any later runtime slice can be considered.

The gate connects:

- typed request metadata from `V1-G2`
- destructive operator-approval metadata from `V1-G3`
- existing `GuardianDecision` contract requirements
- future shell-safe response states for `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`

## Source Evidence

- `docs/GUARDIAN_DECISION_CONTRACT.md` defines `GuardianDecision` as the mandatory execution gate.
- `docs/APPROVAL_METADATA_CONTRACT.md` defines approval metadata as evidence attached to a decision, not a replacement for it.
- `docs/TOOL_PACK_RISK_POLICY.md` defines deny-by-default tool-pack risk and approval expectations.
- `docs/SPINE_AUDIT_LINEAGE_CONTRACT.md` requires downstream lineage to carry `decision_id`.
- `docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md` defines static typed bridge status mappings.
- `docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CONTRACT.md` defines destructive action approval metadata requirements.
- `docs/V1_READINESS_GAP_MATRIX.md` identifies `V1-G4` as the next gap after the destructive approval contract.

## Future Decision Outcome Families

The future live path must distinguish these outcome families before consequential execution:

- `allow`: low-risk or policy-allowed action may continue only when decision scope matches and all constraints are valid.
- `confirm`: action requires explicit human confirmation before execution.
- `deny`: action is denied and must not execute.
- `privileged`: action requires operator PIN, breakglass, or stronger privileged approval.
- `expired`: a prior decision or approval is expired and must not execute.
- `revoked`: a prior decision or approval is revoked and must not execute.
- `blocked`: request is malformed, missing authority, policy-blocked, scope-mismatched, or otherwise unsafe.

`blocked` is the V1 gate outcome for cases that do not have a valid executable decision. It is not a substitute approval state.

## Existing GuardianDecision Status Mapping

The existing status vocabulary maps into V1 outcome families as follows:

- `approved -> allow`
- `needs_human_confirmation -> confirm`
- `needs_operator_pin -> privileged`
- `needs_breakglass -> privileged`
- `denied -> deny`
- `expired -> expired`
- `revoked -> revoked`
- `superseded -> blocked`
- `needs_clarification -> blocked`
- `escalated -> blocked`

Any missing, forged, reused, stale, scope-mismatched, or malformed `decision_id` maps to `blocked`.

## Required Future Live Path

A later runtime implementation may proceed only after a separate approval gate names file scope, tests, rollback plan, and stop conditions. That future path must prove:

- each consequential action has a scoped `GuardianDecision.decision_id`
- `decision_id` is unique, immutable, non-reused, and carried downstream
- decision scope includes actor, shell, input, intent, action type, target, allowed tool packs, risk class, approval level, expiry, constraints, and policy version
- high/critical/destructive actions require valid `ApprovalMetadata`
- approval metadata cannot replace `GuardianDecision`
- execution is allowed only for valid in-scope `allow` decisions whose approval requirements are satisfied
- `confirm`, `deny`, `privileged`, `expired`, `revoked`, and `blocked` outcomes do not execute
- expired, revoked, superseded, denied, and blocked outcomes remain auditable

## Shell Packet Mapping

Future shells should receive bounded state:

- `allow -> preview_only` or future execute-ready state only after a separate runtime approval gate
- `confirm -> explain_plan`
- `privileged -> blocked` or shell approval prompt state
- `deny -> blocked`
- `expired -> blocked`
- `revoked -> blocked`
- `blocked -> blocked`

In this branch all outcomes remain static evidence only and no future execute-ready packet state is added.

## Static V1-G4 Acceptance Rules

For this branch:

- no real `decision_id` is issued
- no approval is granted
- no approval token is issued
- no runtime enforcement exists
- no consequential action executes
- no downstream audit event is persisted
- no provider/model/tool/driver/browser/file/network/device/robotics/haptic/physical-world behavior occurs
- forged, missing, reused, expired, revoked, or scope-mismatched authority claims fail closed

## What V1-G4 Proves

V1-G4 proves as static evidence:

- the future decision outcome families are defined
- existing GuardianDecision statuses map to V1 outcome families
- approval metadata remains subordinate to `GuardianDecision`
- destructive actions require decision plus approval metadata
- forged, expired, revoked, and missing authority cases fail closed
- the next runtime implementation gate must be explicit before any live authority is created

## What V1-G4 Does Not Prove

V1-G4 does not prove:

- real `GuardianDecision` runtime behavior
- live approval capture
- approval enforcement
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

## Boundary Confirmation

- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Real `GuardianDecision` added: no.
- Approval enforcement added: no.
- Approval token issuance added: no.
- Provider/model routing added: no.
- Sparkbot_shell wired into LIMA: no.
- Sparkbot imported into LIMA: no.
- Sparkbot code copied into LIMA: no.
- Arc-Bot-shell wired into LIMA: no.
- Execution, dispatch, or persistence added: no.
- Browser/file/network/device/robotics behavior added: no.
- Haptic device behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.

## Recommended Next Step

Recommended: `V1-G5`.

The next smallest safe step is provider/model routing contract and acceptance-test design, constrained by Guardian, shell tool-pack scope, secret policy, and audit/evidence rules.
