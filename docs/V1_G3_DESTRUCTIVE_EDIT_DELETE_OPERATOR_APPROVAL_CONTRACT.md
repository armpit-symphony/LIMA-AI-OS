# V1-G3 Destructive Edit/Delete Operator Approval Contract

## Verdict

`V1-G3` is complete as a static destructive-action approval contract.

This document is docs/tests/fixtures-only. It does not add runtime behavior, approval enforcement, a real `GuardianDecision`, file mutation, provider/model routing, shell wiring, audit persistence, haptic device behavior, robotics behavior, or production behavior.

## Purpose

V1 requires that deleting or editing anything requires operator approval in LIMA-AI-OS and in the first shell consumers:

- `Sparkbot_shell`
- `Sparkbot`
- `Arc-Bot-shell`

This contract prevents destructive edits, deletes, overwrites, connector writes, and state mutations from being normalized as ordinary preview or drafting work before a real approval path exists.

## Source Evidence

- `docs/V1_PRODUCT_READINESS_TARGET.md` records that deleting or editing anything requires operator approval in LIMA-AI-OS and shells.
- `docs/V1_READINESS_GAP_MATRIX.md` identifies `V1-G3` as the destructive edit/delete operator-approval contract lane.
- `docs/APPROVAL_METADATA_CONTRACT.md` records that approval metadata does not replace `GuardianDecision`.
- `docs/OWNER_AUTONOMY_SAFETY_POLICY.md` records that destructive actions require PIN or stronger approval by default.
- `docs/TOOL_PACK_RISK_POLICY.md` records that destructive file operations are critical and require operator approval.
- `docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md` records the static typed bridge metadata and fail-closed status mapping used by this contract.

## Destructive Action Classes

The following action classes require explicit operator approval before any future runtime may execute them:

- delete file
- edit or mutate file
- overwrite existing content
- delete record, memory, message, task, event, customer data, or shell-owned state
- edit or mutate record, memory, message, task, event, customer data, or shell-owned state
- connector or customer-record write
- destructive admin action

The requirement applies even when the request says the user, owner, operator, admin, or Phil already approved the action. Static text is not approval.

## Non-Destructive Classes

The following classes may remain preview-only or explain-only when they do not mutate state, reveal secrets, execute external actions, bypass Guardian policy, or imply approval:

- read-only inspection
- draft generation
- preview-only planning
- explain-only plan

These classes still cannot execute, dispatch, persist, call providers/models/tools, mutate files, call connectors, or perform physical-world behavior in this branch.

## Required Approval Metadata

Any destructive case must carry:

- `operator_approval_required: true`
- `operator_approval_state`
- action type
- target class
- target reference
- requested actor and shell context
- risk class
- rollback or recovery evidence requirement when available

Allowed future `operator_approval_state` values:

- `missing`
- `required_not_granted`
- `granted`
- `expired`
- `revoked`
- `denied`

`granted` is listed only as a future runtime state. V1-G3 does not create or verify real operator approval. A docs/fixture claim that approval is `granted` must fail closed in this branch.

## Static V1-G3 Acceptance Rules

For this static branch:

- destructive actions with missing approval are blocked
- destructive actions with approval required but not granted are blocked
- expired, revoked, or denied approval states are blocked
- claimed `granted` approval is rejected as an approval-bypass claim
- `approval_granted` remains false in accepted static evidence
- no `approval_id` becomes authority
- no `GuardianDecision.decision_id` is created
- no execution, dispatch, persistence, provider/model call, tool call, driver call, connector call, file mutation, browser/network/device/robotics call, haptic device behavior, or physical-world action is allowed

## Packet-State Mapping

Destructive cases without real operator approval must map to shell-safe status:

- `blocked -> blocked`
- `needs_review -> explain_plan`

Non-destructive preview-only cases may map to:

- `proposed -> preview_only`

V1-G3 does not approve any destructive action to map to `preview_only` as if it were safe.

## What V1-G3 Proves

V1-G3 proves as static evidence:

- destructive edit/delete/overwrite/action classes are identified
- destructive classes require operator approval metadata
- static approval-bypass claims fail closed
- safe draft/preview work can remain preview-only without approval
- status mappings keep destructive actions blocked or explain-only
- LIMA remains `CANDIDATE_ONLY`

## What V1-G3 Does Not Prove

V1-G3 does not prove:

- live approval enforcement
- real operator approval capture
- real `GuardianDecision`
- runtime edit/delete blocking
- runtime file, connector, memory, or shell-state mutation
- provider/model routing
- shell runtime wiring
- haptic device behavior
- audit persistence
- production behavior
- V1 product readiness

## Boundary Confirmation

- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Sparkbot_shell wired into LIMA: no.
- Sparkbot imported into LIMA: no.
- Sparkbot code copied into LIMA: no.
- Arc-Bot-shell wired into LIMA: no.
- Provider/model routing added: no.
- Real `GuardianDecision` added: no.
- Approval enforcement added: no.
- Execution, dispatch, or persistence added: no.
- Browser/file/network/device/robotics behavior added: no.
- Haptic device behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.

## Recommended Next Step

Recommended: `V1-G4`.

The next smallest safe step is a real `GuardianDecision` and live approval path design gate before any runtime enforcement slice.
