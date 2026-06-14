# V1-G11 Implementation Start Checklist

Date: 2026-06-14
Branch: `v1-g11-runtime-slice-approval-request`
API status: `CANDIDATE_ONLY`

This checklist records the exact preconditions that must be true before V1-G11 implementation work can start.

It does not record operator approval, approve runtime implementation, change runtime behavior, modify `lima/`, change exports, approve runtime export cleanup, or approve final freeze.

## Current Start Verdict

V1-G11 implementation is now approved only for the approved implementation branch.

The operator decision packet records `Approve-V1-G11`. Implementation must occur only on `v1-g11-runtime-request-decision-gate`.

## Required Approval Record

Implementation may start only when `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md` records exactly:

```text
Recorded choice: Approve-V1-G11
Recorded approval wording: I explicitly approve V1-G11 implementation of the typed request and GuardianDecision preflight runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md.
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: v1-g11-runtime-request-decision-gate
Runtime implementation approved: yes
```

Any missing, mixed, misspelled, or extra decision state must be treated as no approval.

## Required Implementation Branch

If and only if the valid approval record exists, the implementation branch must be:

- `v1-g11-runtime-request-decision-gate`

The approval-request branch, `v1-g11-runtime-slice-approval-request`, must not carry implementation work.

## Approved File Scope If Approved

If the valid approval record exists, implementation may touch only:

- `lima/kernel/v1_runtime_request.py`
- `lima/kernel/__init__.py`
- `lima/guardian/v1_decision_gate.py`
- `lima/guardian/__init__.py`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`
- `tests/test_v1_g11_runtime_request_decision_gate.py`

Any other file requires a new gate update before implementation.

## Required Runtime Scope If Approved

The only approved future implementation scope is:

- `typed_request_guardian_decision_preflight_runtime_slice`

That scope may add only deterministic, local, in-process, side-effect-free behavior that converts validated candidate metadata into typed request metadata, reviews it through a fail-closed GuardianDecision preflight gate, and emits non-persistent audit/evidence linkage metadata.

## Still Forbidden If Approved

Even if `Approve-V1-G11` is recorded, V1-G11 must not add:

- raw natural-language parsing
- HumanInput live bridge behavior
- provider/model calls or runtime routing
- tool execution
- file mutation
- browser or network behavior
- connector behavior
- shell runtime wiring
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy
- durable persistence, database writes, audit storage, queues, workers, daemons, subprocesses, or threads
- approval-token issuance
- destructive edit/delete approval without operator approval evidence
- haptic device behavior
- device, robotics, IoT, drone, robot, humanoid, or physical-world behavior
- runtime export cleanup
- final API freeze
- V1 product-readiness or production-readiness claims

## Required Validation If Approved

The implementation branch must run at minimum:

- `cmd /c "python3 --version || python --version"`
- `cmd /c "python3 -m compileall lima || python -m compileall lima"`
- `cmd /c "python3 -m pytest -q tests\test_v1_g11_runtime_request_decision_gate.py || python -m pytest -q tests\test_v1_g11_runtime_request_decision_gate.py"`
- `cmd /c "python3 -m pytest -q || python -m pytest -q"`
- `git diff --check`
- `git diff --cached --check` before commit

## Current Boundary Results

- Checklist only: yes.
- Runtime implementation allowed now: yes, only on `v1-g11-runtime-request-decision-gate`.
- Operator approval recorded: yes.
- Runtime implementation approved: yes, limited to the exact V1-G11 request scope.
- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Shell repositories changed: no.
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell code imported or copied: no.
- Provider/model calls or routing added: no.
- Shell runtime wiring added: no.
- Durable persistence added: no.
- Haptic device behavior added: no.
- Browser/file/network/device/robotics/physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- V1 product readiness approved: no.
- Production readiness approved: no.

## Recommended Next Step

Record exactly one valid operator choice in `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md`.

If `Approve-V1-G11` is recorded exactly, create `v1-g11-runtime-request-decision-gate` and execute only the approved work order.
