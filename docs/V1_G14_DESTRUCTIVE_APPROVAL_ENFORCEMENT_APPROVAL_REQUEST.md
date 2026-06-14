# V1-G14 Destructive Approval Enforcement Approval Request

Date: 2026-06-14
Branch: `v1-g14-destructive-approval-enforcement-approval-request`
Source branch: `v1-g13-readiness-gap-refresh-next-lane-decision-gate`
Source commit: `7d2b736ef522595c23bfc6aa6a1f2787bf6fb203`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve runtime implementation, change runtime behavior, modify `lima/`, enforce approvals, issue approval tokens, mutate files, wire shells, route providers/models, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G14 implementation of the destructive edit/delete approval-enforcement runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G11, V1-G12, V1-G13, prior static V1-G3 approval-contract evidence, general V1 product direction, or this request packet do not count as implementation approval.

## Proposed V1-G14 Objective

Implement the smallest local runtime slice that:

- accepts only already-reviewed V1-G11 `ConsequentialActionRequest` and `GuardianDecision` metadata for destructive edit/delete/file-mutation shaped requests
- requires explicit operator approval evidence metadata before a destructive request can be marked as approval-enforcement satisfied
- rejects claimed approval, raw approval PINs, raw approval tokens, raw secrets, raw prompts, raw file contents, and raw customer data
- links the approval evidence reference to request, decision, tenant, shell, actor, and V1-G12 audit/evidence metadata
- returns a redacted, non-executing approval-enforcement record
- keeps approval-enforcement metadata as a prerequisite proof only, not execution authority
- never executes file mutations, tools, connectors, browsers, networks, devices, robots, models, external sends, or physical-world actions

## Approved Files If Operator Says Yes

Runtime files:

- `lima/guardian/v1_approval_enforcement.py` (new)
- `lima/guardian/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT.md`
- `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g14_destructive_approval_enforcement.json`
- `tests/test_v1_g14_destructive_approval_enforcement.py`

Any other file requires a new gate update before implementation.

## Allowed Runtime Behavior If Approved

V1-G14 may add only deterministic, local, non-executing approval-enforcement behavior that proves:

- only V1-G11-style request/decision metadata can enter the approval-enforcement slice
- destructive edit/delete/file-mutation shaped requests require approval metadata
- required approval metadata includes `approval_id`, `approval_evidence_ref`, `approving_actor_ref`, `approval_recorded_at`, `approval_scope`, `tenant_ref`, and `shell_id`
- approval evidence must link to the same request ID, decision ID, actor ID, shell ID, tenant reference, and target reference
- missing approval evidence fails closed
- expired, revoked, denied, superseded, or stale approval evidence fails closed
- replayed approval evidence fails closed
- mismatched request/decision/approval metadata fails closed
- forged approval, approval token, operator PIN, or decision metadata fails closed
- raw sensitive content fails closed
- approval-enforcement records do not authorize execution, issue tokens, route providers/models, or mutate state

## Explicitly Forbidden

V1-G14 must not add:

- provider/model calls or routing
- tool execution
- file mutation, delete, overwrite, or external file action behavior
- browser or network behavior
- connector behavior
- shell runtime wiring
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- live auth, live trust lookup, or HumanInput bridge activation
- approval-token issuance
- raw approval PIN verification or raw PIN persistence
- audit metadata as execution authority
- raw secret, prompt, file, customer, approval token, or PIN persistence
- haptic device behavior
- device, robotics, IoT, drone, robot, humanoid, or physical-world behavior
- runtime export cleanup
- final API freeze
- V1 product readiness or production readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- destructive edit/delete/file-mutation requests without approval metadata fail closed
- destructive edit/delete/file-mutation requests with complete sanitized approval evidence produce a non-executing approval-enforcement record
- safe informational/planning/drafting requests are not upgraded into destructive approval-enforcement records
- request and decision identity mismatches fail closed
- tenant, actor, shell, decision, request, target, and approval evidence mismatches fail closed
- missing `approval_id` fails closed
- missing `approval_evidence_ref` fails closed
- missing `approving_actor_ref` fails closed
- missing `approval_recorded_at` fails closed
- expired, revoked, denied, superseded, stale, or replayed approval evidence fails closed
- raw approval PINs, raw approval tokens, raw secrets, raw prompts, raw file contents, and raw customer data fail closed
- forged approval/decision metadata fails closed
- provider/model/tool/browser/network/device/robotics/physical-world claims remain blocked
- approval-enforcement records do not authorize execution, emit approval tokens, mutate files, or persist raw sensitive content

## Rollback Plan If Approved

Rollback must remove only:

- `lima/guardian/v1_approval_enforcement.py`
- V1-G14 candidate exports added to `lima/guardian/__init__.py`
- V1-G14 docs/tests/fixtures

Rollback must not require shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, or production deployment changes.

## Stop Conditions

Stop before implementation or revert the implementation if any of these appear:

- file scope exceeds the approved V1-G14 files
- approval metadata becomes execution authority
- raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, or raw customer data can persist or be emitted
- approval tokens are issued
- destructive edit/delete/file-mutation requests can pass without approval evidence
- expired, revoked, denied, superseded, stale, replayed, forged, or mismatched approval evidence can pass
- provider/model calls or routing are added
- tools, arbitrary files, browsers, networks, connectors, devices, robots, or physical-world systems are invoked
- external database writes, migrations, queues, workers, daemons, subprocesses, or threads are added
- shell runtime wiring is added
- Sparkbot code is imported or copied
- runtime exports are cleaned up or frozen
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Runtime implementation approved by this request: no.
- Operator approval recorded: no.
- Runtime behavior added: no.
- Approval enforcement added: no.
- File mutation behavior added: no.
- Provider/model calls added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/file/network/device/robotics/physical-world behavior added: no.
- External database writes added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Shell repositories changed: no.
- Sparkbot code copied or imported: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create the V1-G14 implementation branch and implement only the approved destructive edit/delete approval-enforcement slice. If not approved, revise the request or keep LIMA at `CANDIDATE_ONLY`.
