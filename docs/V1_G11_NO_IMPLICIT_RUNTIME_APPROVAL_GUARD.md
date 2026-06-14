# V1-G11 No Implicit Runtime Approval Guard

Date: 2026-06-14
Branch: `v1-g11-runtime-slice-approval-request`
API status: `CANDIDATE_ONLY`

This guard records a static fixture scan rule for the V1-G11 approval-request lane.

No V1-G11 fixture may record current runtime approval unless a valid operator decision is recorded in `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_OPERATOR_DECISION_PACKET.md`.

## Guard Purpose

The current V1 objective is accepted as product direction only. It does not approve the V1-G11 runtime slice.

The only current path that can authorize V1-G11 runtime implementation is a valid `Approve-V1-G11` Decision Record in the operator decision packet, with the exact approval wording, approved implementation branch, and runtime implementation approved set to `yes`.

Until that record exists, aggregate fixture evidence must keep current approval and release flags false.

## Guarded Fixture Set

The guard scans the current V1 status and V1-G11 fixtures:

- `tests/fixtures/runtime_extraction/v1_readme_status_alignment.json`
- `tests/fixtures/runtime_extraction/v1_readiness_gap_matrix.json`
- `tests/fixtures/runtime_extraction/v1_product_readiness_target.json`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate_work_order.json`
- `tests/fixtures/runtime_extraction/v1_g11_runtime_request_decision_gate_approval_request.json`
- `tests/fixtures/runtime_extraction/v1_g11_roadmap_decision_alignment.json`
- `tests/fixtures/runtime_extraction/v1_g11_operator_decision_readiness_closeout.json`
- `tests/fixtures/runtime_extraction/v1_g11_operator_decision_packet.json`
- `tests/fixtures/runtime_extraction/v1_g11_broad_goal_non_approval_audit.json`

## Forbidden Current Approval Flags

The guard fails closed if any guarded fixture records current approval, release, export cleanup, runtime wiring, runtime behavior, shell wiring, persistence, haptic device behavior, provider/model routing, or physical-world behavior as true.

The only allowed true runtime-approval value is the hypothetical Approve-V1-G11 validation rule in `tests/fixtures/runtime_extraction/v1_g11_operator_decision_packet.json`.

That rule is not a current Decision Record. It only describes what a future valid approval record would require.

## Decision Record Requirement

Current Decision Records must remain empty until an operator records one valid choice.

The guarded current records must keep:

- Recorded choice: `none`
- Recorded approval wording: `none`
- Recorded revision request: `none`
- Recorded pause reason: `none`
- Approved implementation branch: `none`
- Runtime implementation approved: no

## Boundary Results

- Docs/tests/fixtures-only: yes.
- Runtime behavior added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Shell repositories changed: no.
- Sparkbot code copied or imported: no.
- Provider/model routing added: no.
- Shell wiring added: no.
- Persistence added: no.
- Haptic device behavior added: no.
- Browser/file/network/device/robotics/physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- V1 product readiness approved: no.
- Production readiness approved: no.

## Recommended Next Step

Record exactly one valid operator choice in the V1-G11 operator decision packet.

Until that happens, keep LIMA at `CANDIDATE_ONLY` and do not start runtime implementation.
