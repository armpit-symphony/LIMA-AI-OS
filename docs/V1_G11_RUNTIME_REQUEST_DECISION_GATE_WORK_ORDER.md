# V1-G11 Runtime Request Decision Gate Work Order

Date: 2026-06-14
Branch: `v1-g11-runtime-slice-approval-request`
Source branch: `v1-g11-runtime-slice-approval-request`
Source commit: `3f844a5097e2be60653e2b85bbbec9ce758cbc48`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_runtime`

This is a work order only. It does not record operator approval, does not approve runtime implementation, and does not change `lima/`.

## Approval Dependency

V1-G11 implementation may start only after the operator explicitly approves:

`docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_APPROVAL_REQUEST.md`

Until that approval is recorded, the allowed work remains docs/tests/fixtures-only.

## Existing Runtime Shapes To Reuse

The implementation must reuse the existing local contracts and candidate helpers:

- `lima.contracts.guardian.ConsequentialActionRequest`
- `lima.contracts.guardian.ConsequentialActionType`
- `lima.contracts.guardian.GuardianDecision`
- `lima.contracts.guardian.GuardianDecisionStatus`
- `lima.kernel.validate_candidate`
- `lima.kernel.normalize_candidate_status`

Do not create a parallel Guardian request model unless an implementation review proves the existing contract cannot represent the slice.

## Implementation Sequence If Approved

1. Add `lima/kernel/v1_runtime_request.py`.
2. In that file, add a narrow builder that accepts validated candidate metadata and returns `ConsequentialActionRequest` metadata only.
3. The builder must reject raw natural-language keys, invalid candidates, missing provenance, stale/replayed candidates, caller-supplied approval claims, and caller-supplied decision authority.
4. Add `lima/guardian/v1_decision_gate.py`.
5. In that file, add a deterministic local decision gate that maps reviewed requests to `GuardianDecision` metadata.
6. The gate must map safe informational/planning/drafting requests to reviewed non-executing decisions.
7. The gate must map destructive edit/delete and other risky categories to approval-required or fail-closed statuses without execution or token issuance.
8. Add candidate exports only in `lima/kernel/__init__.py` and `lima/guardian/__init__.py`.
9. Add `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`.
10. Add `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`.
11. Add `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`.
12. Add `tests/test_v1_g11_runtime_request_decision_gate.py`.

## Expected Candidate Runtime Symbols If Approved

The implementation should expose only candidate V1 symbols such as:

- `V1RuntimeRequestError`
- `build_v1_runtime_request`
- `V1GuardianDecisionGateError`
- `review_v1_runtime_request`

The exact symbol names may change during implementation only if the V1-G11 implementation doc records the reason and tests lock the exported surface.

## Required Mapping Rules If Approved

- `informational` -> reviewed, non-executing, no approval token
- `planning` -> reviewed, non-executing, no approval token
- `drafting` -> reviewed, non-executing, no approval token
- `file_mutation` -> approval-required, non-executing
- destructive edit -> approval-required, non-executing
- destructive delete -> approval-required, non-executing
- `model_call` -> blocked or future-policy-required, no routing
- `tool_call` -> blocked or future-policy-required, no execution
- `browser_network` -> blocked or future-policy-required, no browser/network action
- `robotics_physical_world` -> blocked or future-policy-required, no physical action
- unknown category -> denied or blocked

## Required Output Boundaries If Approved

The runtime slice may output:

- typed request metadata
- GuardianDecision metadata
- non-persistent audit/evidence linkage metadata
- redacted summaries
- deterministic reason codes

The runtime slice must not output:

- raw secrets
- raw prompts
- raw file contents
- approval PINs
- approval tokens
- provider credentials
- executable commands
- mutation instructions marked approved

## Required Validation If Approved

Run at minimum:

- `cmd /c "python3 --version || python --version"`
- `cmd /c "python3 -m compileall lima || python -m compileall lima"`
- `cmd /c "python3 -m pytest -q tests\test_v1_g11_runtime_request_decision_gate.py || python -m pytest -q tests\test_v1_g11_runtime_request_decision_gate.py"`
- `cmd /c "python3 -m pytest -q || python -m pytest -q"`
- `git diff --check`
- `git diff --cached --check` before commit

## Rollback If Approved

Rollback must be possible by removing only:

- `lima/kernel/v1_runtime_request.py`
- `lima/guardian/v1_decision_gate.py`
- V1-G11 candidate exports in `lima/kernel/__init__.py`
- V1-G11 candidate exports in `lima/guardian/__init__.py`
- V1-G11 docs/tests/fixtures

Rollback must not require shell repo changes, Sparkbot changes, database migrations, provider configuration changes, or production deployment changes.

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G11 file map
- raw natural-language parsing
- execution, dispatch, persistence, queues, workers, daemons, subprocesses, or threads
- provider/model calls or routing
- shell runtime wiring
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy
- approval-token issuance
- destructive edit/delete approval without operator approval evidence
- browser/file/network/device/robotics/physical-world behavior
- haptic device behavior
- runtime export cleanup
- final API freeze
- V1 product-readiness or production-readiness claims

## Boundary Confirmation

- Work order only: yes.
- Operator approval recorded: no.
- Runtime implementation approved by this work order: no.
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

## Recommended Next Step

Operator decision on the exact V1-G11 approval request.

If approved, create the V1-G11 implementation branch and execute this work order exactly. If not approved, keep LIMA at `CANDIDATE_ONLY` or revise the request.
