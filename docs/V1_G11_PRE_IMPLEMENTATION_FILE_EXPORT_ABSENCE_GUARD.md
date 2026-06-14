# V1-G11 Pre-Implementation File Export Absence Guard

Date: 2026-06-14
Branch: `v1-g11-runtime-slice-approval-request`
API status: `CANDIDATE_ONLY`

This guard recorded the pre-approval runtime file and export boundary for V1-G11.

The valid `Approve-V1-G11` decision is now recorded. This guard is retired and must not block the approved implementation branch from creating the V1-G11 files and candidate exports named in the request.

## Guard Purpose

V1-G11 was ready for an operator decision, and the current Decision Record now records `Approve-V1-G11`.

The proposed V1-G11 implementation files and candidate exports may be added only on `v1-g11-runtime-request-decision-gate` and only inside the approved V1-G11 file map.

## Required Pre-Approval State

V1-G11 runtime files were required to remain absent before approval.

Current lima.kernel exports were required to remain unchanged before approval.

Current lima.guardian exports were required to remain unchanged before approval.

The current approved state is:

- API status: `CANDIDATE_ONLY`
- Operator approval recorded: yes
- Runtime implementation approved: yes, limited to the exact V1-G11 request scope
- Runtime behavior added: no
- Runtime exports changed: no
- Runtime export cleanup approved: no
- Final API freeze approved: no
- Approved implementation branch: none

## Files Previously Required To Stay Absent Before Approval

The following proposed implementation files were required to stay absent before approval and are now eligible only on the approved implementation branch:

- `lima/kernel/v1_runtime_request.py`
- `lima/guardian/v1_decision_gate.py`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate.json`
- `tests/test_v1_g11_runtime_request_decision_gate.py`

## Exports Previously Required To Stay Absent Before Approval

The following proposed future symbols were required to stay absent before approval and are now eligible only as candidate V1-G11 exports:

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

The only path that retired this guard is the valid `Approve-V1-G11` Decision Record with:

- exact approval wording from the operator decision packet
- approved implementation branch `v1-g11-runtime-request-decision-gate`
- runtime implementation approved set to `yes`

Any other state must be treated as no runtime approval.

## Boundary Results

- Docs/tests/fixtures-only: yes.
- Runtime implementation approved: yes, limited to the exact V1-G11 request scope.
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
