# V1-G11 Pre-Implementation File Export Absence Guard

Date: 2026-06-14
Branch: `v1-g11-runtime-slice-approval-request`
API status: `CANDIDATE_ONLY`

This guard records the pre-approval runtime file and export boundary for V1-G11.

It does not approve runtime implementation, change runtime behavior, modify `lima/`, approve runtime export cleanup, approve final freeze, or record an operator decision.

## Guard Purpose

V1-G11 is ready for an operator decision, but the current Decision Record remains empty.

Until a valid `Approve-V1-G11` record is present in `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md`, the proposed V1-G11 implementation files and exports must remain absent.

## Required Pre-Approval State

V1-G11 runtime files must remain absent before approval.

Current lima.kernel exports must remain unchanged before approval.

Current lima.guardian exports must remain unchanged before approval.

The current approved state is:

- API status: `CANDIDATE_ONLY`
- Operator approval recorded: no
- Runtime implementation approved: no
- Runtime behavior added: no
- Runtime exports changed: no
- Runtime export cleanup approved: no
- Final API freeze approved: no
- Approved implementation branch: none

## Files That Must Stay Absent Before Approval

The following proposed implementation files must not exist before a valid `Approve-V1-G11` decision is recorded:

- `lima/kernel/v1_runtime_request.py`
- `lima/guardian/v1_decision_gate.py`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`
- `tests/test_v1_g11_runtime_request_decision_gate.py`

## Exports That Must Stay Absent Before Approval

The following proposed future symbols must not be exported before approval:

- `V1RuntimeRequestError`
- `build_v1_runtime_request`
- `V1GuardianDecisionGateError`
- `review_v1_runtime_request`

## Current Kernel Export Surface

The current `lima.kernel.__all__` surface is limited to:

- `ALLOWED_CANDIDATE_STATUSES`
- `CandidatePreview`
- `CandidateStatusError`
- `IntakeCandidateError`
- `RuntimeStateSnapshot`
- `build_intake_candidate`
- `inspect_runtime_state`
- `normalize_candidate_status`
- `preview_candidate`
- `validate_candidate`

## Current Guardian Export Surface

The current `lima.guardian.__all__` surface is limited to:

- `FakeApprovalRecorder`
- `FakeAuthProvider`
- `FakeBreakglassProvider`
- `FakeGuardianDecisionEvaluator`
- `FakeGuardianPipeline`
- `FakeGuardianPipelineResult`
- `FakePolicyRiskEvaluator`
- `FakeSpineAuditRecorder`
- `FakeVaultProvider`
- `AdapterFixtureHarness`
- `AdapterFixtureHarnessResult`
- `HumanInputFakePipelineBridge`
- `HumanInputPipelineBridgeConfig`

## Approval Path

The only path that can change this guard is a valid `Approve-V1-G11` Decision Record with:

- exact approval wording from the operator decision packet
- approved implementation branch `v1-g11-runtime-request-decision-gate`
- runtime implementation approved set to `yes`

Any other state must be treated as no runtime approval.

## Boundary Results

- Docs/tests/fixtures-only: yes.
- Runtime implementation approved: no.
- Operator approval recorded: no.
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

Record exactly one valid operator choice in the V1-G11 operator decision packet.

If `Approve-V1-G11` is recorded with the exact required wording, create `v1-g11-runtime-request-decision-gate` and implement only the approved typed request and GuardianDecision preflight runtime slice inside the V1-G10/V1-G11 file-touch map.
