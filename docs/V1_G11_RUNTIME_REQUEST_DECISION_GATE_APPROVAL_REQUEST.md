# V1-G11 Runtime Request Decision Gate Approval Request

Date: 2026-06-14
Branch: `v1-g11-runtime-slice-approval-request`
Source branch: `v1-g10-minimum-runtime-implementation-gate`
Source commit: `39b866a3be3756d10287e3cefbd674ace7d2d469`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve runtime implementation, change runtime behavior, modify `lima/`, or create a real `GuardianDecision`.

## Exact Approval Question

Do you explicitly approve V1-G11 implementation of the typed request and GuardianDecision preflight runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. General V1 product direction, prior static gates, or this request packet do not count as implementation approval.

## Proposed V1-G11 Objective

Implement the smallest local runtime slice that:

- accepts only validated non-executing candidate metadata
- converts that candidate into typed `ConsequentialActionRequest` metadata
- evaluates the request through a fail-closed Guardian decision gate
- emits non-persistent audit/evidence linkage metadata
- never executes tools, files, connectors, browsers, networks, devices, robots, models, or physical-world actions

## Approved Files If Operator Says Yes

Runtime files:

- `lima/kernel/v1_runtime_request.py` (new)
- `lima/kernel/__init__.py` (candidate export only)
- `lima/guardian/v1_decision_gate.py` (new)
- `lima/guardian/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`
- `tests/test_v1_g11_runtime_request_decision_gate.py`

Any other file requires a new gate update before implementation.

## Allowed Runtime Behavior If Approved

V1-G11 may add only deterministic, local, in-process, side-effect-free behavior that proves:

- raw natural language is not accepted
- only validated candidate metadata can enter the slice
- missing candidate provenance fails closed
- caller-supplied `approved=true` fails closed
- caller-supplied `GuardianDecision` authority fails closed
- unknown action category fails closed
- destructive edit/delete maps to approval-required status, not execution
- provider/model/tool/file/browser/network/device/robotics claims fail closed or require a later policy gate
- `ConsequentialActionRequest` carries required request, actor, shell, target, risk, typed-args, and evidence metadata
- reviewed requests produce GuardianDecision metadata
- approval-required decisions do not execute and do not issue approval tokens
- audit/evidence linkage metadata is present and non-persistent

## Explicitly Forbidden

V1-G11 must not add:

- raw natural-language parsing
- HumanInput live bridge behavior
- real provider/model calls or routing
- tool execution
- file mutation
- browser or network behavior
- connector behavior
- shell runtime wiring
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy
- durable persistence, database writes, audit storage, queues, workers, daemons, subprocesses, or threads
- haptic device behavior
- device, robotics, IoT, drone, robot, humanoid, or physical-world behavior
- runtime export cleanup
- final API freeze
- V1 product readiness or production readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- safe informational candidate produces a reviewed decision without execution
- planning/drafting candidate stays non-executing
- destructive edit candidate requires operator approval
- destructive delete candidate requires operator approval
- caller-supplied approval claim is blocked
- caller-supplied decision authority is blocked
- stale or replayed candidate is blocked
- missing provenance is blocked
- unknown action type is denied or blocked
- provider/model request is not routed
- file/browser/network/device/robotics claims do not execute
- audit/evidence linkage is present and non-persistent
- no raw secret, raw prompt, raw file contents, approval PIN, or approval token is emitted

## Rollback Plan If Approved

Rollback must remove only:

- `lima/kernel/v1_runtime_request.py`
- `lima/guardian/v1_decision_gate.py`
- candidate exports added to `lima/kernel/__init__.py`
- candidate exports added to `lima/guardian/__init__.py`
- V1-G11 docs/tests/fixtures

Rollback must not require shell repo changes, Sparkbot changes, persistence migration, external service changes, provider configuration changes, or production deployment changes.

## Stop Conditions

Stop before implementation or revert the implementation if any of these appear:

- file scope exceeds the approved V1-G11 files
- raw natural language reaches the runtime slice
- request metadata executes directly
- approval metadata becomes execution authority
- destructive edit/delete can become approved without operator approval evidence
- caller metadata can forge GuardianDecision authority
- provider/model calls are made
- tools, files, browsers, networks, devices, robots, or physical-world systems are invoked
- persistent storage or database writes are added
- shell runtime wiring is added
- Sparkbot code is imported or copied
- runtime exports are cleaned up or frozen
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Runtime implementation approved by this request: no.
- Operator approval recorded: no.
- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Shell repositories changed: no.
- Sparkbot code copied or imported: no.
- Provider/model calls added: no.
- Runtime `GuardianDecision` added: no.
- Approval enforcement added: no.
- Durable persistence added: no.
- Haptic device behavior added: no.
- Physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create the V1-G11 implementation branch and implement only the approved typed request plus GuardianDecision preflight slice. If not approved, revise the request or keep LIMA at `CANDIDATE_ONLY`.
