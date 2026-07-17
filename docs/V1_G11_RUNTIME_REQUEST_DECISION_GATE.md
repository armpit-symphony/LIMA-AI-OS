# V1-G11 Runtime Request Decision Gate

Date: 2026-06-14
Branch: `v1-g11-runtime-request-decision-gate`
API status: `CANDIDATE_ONLY`

This document records the approved V1-G11 implementation of the typed request and GuardianDecision preflight runtime slice.

Approval source:

- Operator: Phil Lima
- Decision: `Approve-V1-G11`
- Decision packet: `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md`
- Approved implementation branch: `v1-g11-runtime-request-decision-gate`

## Implementation Scope

The implementation is limited to:

- `lima/kernel/v1_runtime_request.py`
- `lima/kernel/__init__.py`
- `lima/guardian/v1_decision_gate.py`
- `lima/guardian/__init__.py`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`
- `tests/test_v1_g11_runtime_request_decision_gate.py`

No files outside this map are required for the runtime implementation.

## Runtime Behavior Added

V1-G11 adds a deterministic local preflight slice:

- `build_v1_runtime_request(candidate)`
- `review_v1_runtime_request(request)`

The builder accepts only validated candidate metadata and returns a typed `ConsequentialActionRequest`.

The gate reviews the typed request and returns non-executing `GuardianDecision` metadata.

## Fail-Closed Rules

The slice rejects or blocks:

- raw natural-language payload keys
- missing or invalid candidate provenance
- stale or replayed candidates
- caller-supplied approval claims
- caller-supplied GuardianDecision authority
- unknown action categories
- provider/model routing claims
- tool execution claims
- browser/network action claims
- robotics or physical-world action claims

## Destructive Edit/Delete Boundary

Destructive edit/delete and file-mutation candidates map to operator-approval-required `GuardianDecision` metadata.

They do not execute, mutate files, issue approval tokens, persist audit data, or mark the action approved.

## Audit/Evidence Linkage

The slice emits non-persistent audit/evidence linkage metadata containing:

- lineage id
- request id
- candidate id
- input id
- intent id when present
- actor id
- shell id
- action type
- target ref
- risk class
- evidence refs
- redacted summary

This is metadata only. It is not durable audit persistence.

## Explicit Non-Goals

V1-G11 does not add:

- product integration
- consumer repo integration
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or wiring
- HumanInput bridge activation
- provider/model calls or routing
- connector behavior
- browser/file/network action behavior
- external sends
- live discovery, scanning, pairing, credential use, device control, robot control, drone control, IoT control, or physical-world behavior
- haptic device behavior
- durable persistence
- runtime export cleanup
- final API freeze
- V1 product readiness
- production readiness

## Boundary Results

- Runtime behavior added: yes, limited to the approved local non-executing V1-G11 preflight slice.
- Runtime exports changed: yes, candidate V1-G11 symbols only.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- Consumer integration added: no.
- Provider/model routing added: no.
- File/browser/network/device/robotics/physical-world behavior added: no.
- Durable persistence added: no.
- Product readiness approved: no.

## Current Readiness Verdict

V1-G11 moves LIMA from static V1 evidence toward a narrow local runtime preflight capability.

LIMA remains `CANDIDATE_ONLY`. The V1 product release boundary is still not passed.
