# V1-G14 Destructive Approval Enforcement Operator Decision Packet

Date: 2026-06-14
Branch: `v1-g14-destructive-approval-enforcement-approval-request`
API status: `CANDIDATE_ONLY`

Decision packet status: `Approve-V1-G14_recorded`

This packet records the valid operator choices for the exact V1-G14 destructive edit/delete approval-enforcement approval request. It does not change runtime behavior, modify `lima/`, approve implementation, enforce approvals, or approve product readiness by itself.

## Decision Source

The decision source is:

- `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_APPROVAL_REQUEST.md`
- `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_PREFLIGHT_AUDIT.md`
- `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_WORK_ORDER.md`
- `docs/V1_G13_READINESS_GAP_REFRESH_AND_NEXT_LANE_DECISION_GATE.md`

The approval request asks:

> Do you explicitly approve V1-G14 implementation of the destructive edit/delete approval-enforcement runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

General V1 product direction, prior static gates, the V1-G13 recommendation, this packet, or broad statements that approval enforcement is needed do not count as implementation approval.

## Current Decision State

- Operator approval recorded: yes.
- Runtime implementation approved: yes.
- Approved next implementation branch: `v1-g14-destructive-approval-enforcement`.
- Current next action: implement the approved V1-G14 runtime slice and stop before any consumer integration.

## Decision Record

One operator choice has been recorded for implementation.

- Recorded choice: `Approve-V1-G14`
- Recorded approval wording: `I explicitly approve V1-G14 implementation of the destructive edit/delete approval-enforcement runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_APPROVAL_REQUEST.md.`
- Recorded revision request: `none`
- Recorded pause reason: `none`
- Approved implementation branch: `v1-g14-destructive-approval-enforcement`
- Runtime implementation approved: yes

## Historical Pre-Approval State

Before the operator recorded `Approve-V1-G14`, this packet was in the following request-branch state:

- Decision packet status: `awaiting_operator_decision`
- Recorded choice: `none`
- Runtime implementation approved: no

Only `Approve-V1-G14`, `Revise-V1-G14`, or `Pause` is valid here. Any other text is commentary, not a decision.

## Decision Record Validation Rules

- `none`: valid only while every Decision Record field remains `none` and runtime implementation approved remains `no`.
- `Approve-V1-G14`: valid only with the exact required approval wording, approved branch `v1-g14-destructive-approval-enforcement`, no revision request, no pause reason, and runtime implementation approved set to `yes`.
- `Revise-V1-G14`: valid only with a non-empty revision request, no approval wording, no approved implementation branch, no pause reason, and runtime implementation approved set to `no`.
- `Pause`: valid only with a non-empty pause reason, no approval wording, no approved implementation branch, no revision request, and runtime implementation approved set to `no`.
- Any mixed state is invalid and must be treated as no approval.
- Missing, misspelled, or extra choice values are invalid and must be treated as no approval.
- Runtime implementation may start only from the valid `Approve-V1-G14` state.

## Decision Record Templates

Use one template only.

Template for no recorded choice:

```text
Recorded choice: none
Recorded approval wording: none
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: none
Runtime implementation approved: no
```

Template for `Approve-V1-G14`:

```text
Recorded choice: Approve-V1-G14
Recorded approval wording: I explicitly approve V1-G14 implementation of the destructive edit/delete approval-enforcement runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_APPROVAL_REQUEST.md.
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: v1-g14-destructive-approval-enforcement
Runtime implementation approved: yes
```

Template for `Revise-V1-G14`:

```text
Recorded choice: Revise-V1-G14
Recorded approval wording: none
Recorded revision request: <required revision request>
Recorded pause reason: none
Approved implementation branch: none
Runtime implementation approved: no
```

Template for `Pause`:

```text
Recorded choice: Pause
Recorded approval wording: none
Recorded revision request: none
Recorded pause reason: <required pause reason>
Approved implementation branch: none
Runtime implementation approved: no
```

## Valid Operator Choices

### `Approve-V1-G14`

This choice is valid only if the operator explicitly approves the exact V1-G14 request scope.

Required approval wording:

`I explicitly approve V1-G14 implementation of the destructive edit/delete approval-enforcement runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_APPROVAL_REQUEST.md.`

If recorded, the next branch may be:

- `v1-g14-destructive-approval-enforcement`

If recorded, the only approved runtime scope is:

- `destructive_edit_delete_approval_enforcement_runtime_slice`

### `Revise-V1-G14`

This choice asks for a narrower or different request. It keeps runtime implementation unapproved.

Revision must name the requested change, such as:

- narrower file scope
- stricter proof linkage to V1-G12 audit evidence
- no candidate export change
- additional negative tests
- pause until a separate approval-authentication design lands
- different handling for non-file destructive actions

### `Pause`

This choice keeps LIMA at `CANDIDATE_ONLY` and does not start V1-G14 runtime implementation.

## If `Approve-V1-G14` Is Recorded

Implementation must stay inside the already named V1-G14 scope:

- `lima/guardian/v1_approval_enforcement.py`
- `lima/guardian/__init__.py`
- `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT.md`
- `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g14_destructive_approval_enforcement.json`
- `tests/test_v1_g14_destructive_approval_enforcement.py`

Any different file requires a new gate update before implementation.

## Boundaries Before Approved Implementation

- Runtime implementation approved: yes, only for the V1-G14 file map and behavior scope.
- Operator approval recorded: yes.
- Runtime behavior added: no.
- Approval enforcement added: no.
- File mutation behavior added: no.
- Provider/model calls or routing added: no.
- Shell runtime wiring added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/file/network/device/robotics/physical-world behavior added: no.
- External database writes added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Shell repositories changed: no.
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy added: no.
- Approval tokens issued: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- V1 product readiness approved: no.
- Production readiness approved: no.

## Non-Negotiable Stop Conditions

Stop before implementation or revert if any of the following appear without a new explicit gate:

- file scope exceeds the V1-G14 request
- approval metadata becomes execution authority
- raw approval PINs, approval tokens, secrets, prompts, file contents, or customer data can persist or emit
- approval tokens are issued
- destructive edit/delete/file-mutation requests can pass without approval evidence
- stale, replayed, expired, revoked, denied, superseded, forged, or mismatched approval evidence is accepted
- provider/model calls or routing are added
- tool/file/browser/network/device/robotics/physical-world behavior is invoked
- external database writes, migrations, queues, workers, daemons, subprocesses, or threads are added
- shell runtime wiring is added
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell code is imported or copied
- runtime exports are cleaned up or frozen
- validation fails

## Recommended Next Step

Record exactly one operator choice in this packet.

If `Approve-V1-G14` is recorded, implement the approved V1-G14 destructive edit/delete approval-enforcement slice on branch `v1-g14-destructive-approval-enforcement`.

Keep LIMA at `CANDIDATE_ONLY` and stop after implementation closeout.
