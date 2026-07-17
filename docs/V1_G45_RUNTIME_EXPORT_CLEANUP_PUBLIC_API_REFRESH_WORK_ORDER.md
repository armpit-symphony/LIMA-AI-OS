# V1-G45 Runtime Export Cleanup Public API Refresh Work Order

Date: 2026-06-17
Branch: `prepare-v1-g45-runtime-export-cleanup-public-api-refresh-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `request_only_not_approved`

## Objective

Prepare an operator decision gate for the smallest runtime export cleanup/public API refresh slice after V1-G44.

The requested future implementation would expose the existing V1-G44 validator symbols through `lima.harness.__all__` and refresh the V1-G22 final public API freeze fixture for that exact export change. This work order does not approve or implement that slice.

## Inputs

- `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY.md`
- `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY_CLOSEOUT.md`
- `docs/audits/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY_AUDIT.md`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G44_AUDIT.md`
- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G44.md`
- `docs/readiness/V1_POST_G44_NEXT_LANE_DECISION_MATRIX.md`
- `docs/V1_G22_FINAL_PUBLIC_API_FREEZE.md`
- `docs/V1_G28_RUNTIME_EXPORT_CLEANUP.md`

## Request-Only File Scope

- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_APPROVAL_REQUEST.md`
- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_WORK_ORDER.md`
- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_PREFLIGHT_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_g45_runtime_export_cleanup_public_api_refresh_approval_request.json`
- `tests/test_v1_g45_runtime_export_cleanup_public_api_refresh_approval_request.py`

## Proposed Implementation File Scope If Approved Later

LIMA-AI-OS runtime files:

- `lima/harness/__init__.py`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH.md`
- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g45_runtime_export_cleanup_public_api_refresh.json`
- `tests/test_v1_g45_runtime_export_cleanup_public_api_refresh.py`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`

Sparkbot:

- none

Arc-Bot-shell:

- none

## Guardrails

- No validator behavior changes.
- No live provider/model call execution.
- No actual model request dispatch execution.
- No network calls.
- No provider readiness network checks.
- No Token Guardian live routing.
- No secret lookup or credential value access.
- No fallback execution.
- No tool execution.
- No consumer repo edits.
- No consumer runtime/source file changes.
- No connector/browser/network/device/robotics/physical-world behavior.
- No external sends.
- No product-readiness or production-readiness claims.

## Validation For This Request Packet

- `python -m pytest -q tests/test_v1_g45_runtime_export_cleanup_public_api_refresh_approval_request.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g44_live_provider_model_call_authority.py tests/test_v1_g22_final_public_api_freeze.py -p no:cacheprovider`
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit

## Next Action

Ask the operator to approve, revise, or pause the V1-G45 implementation request. Implementation must not begin until the operator records `Approve-V1-G45` with the exact approval wording from the request.
