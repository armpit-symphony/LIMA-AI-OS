# V1-G46 Live Provider Model Call Execution Work Order

Date: 2026-06-17
Branch: `prepare-v1-g46-live-provider-model-call-execution-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `request_only_not_approved`

## Objective

Prepare an operator decision gate for the first bounded live provider/model call execution slice after V1-G45.

The requested future implementation would add a LIMA harness execution wrapper that requires prevalidated V1-G44 authority metadata and an injected provider executor. This work order does not approve or implement that slice.

## Inputs

- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH.md`
- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_CLOSEOUT.md`
- `docs/audits/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_AUDIT.md`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G45_AUDIT.md`
- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G45.md`
- `docs/readiness/V1_POST_G45_NEXT_LANE_DECISION_MATRIX.md`
- `docs/V1_G44_LIVE_PROVIDER_MODEL_CALL_AUTHORITY.md`
- `docs/V1_G43_PROVIDER_MODEL_DISPATCH.md`
- `docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY.md`

## Request-Only File Scope

- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_APPROVAL_REQUEST.md`
- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_WORK_ORDER.md`
- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_PREFLIGHT_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_g46_live_provider_model_call_execution_approval_request.json`
- `tests/test_v1_g46_live_provider_model_call_execution_approval_request.py`

## Proposed Implementation File Scope If Approved Later

LIMA-AI-OS runtime files:

- `lima/harness/v1_live_provider_model_call_execution.py`
- `lima/harness/__init__.py`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION.md`
- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g46_live_provider_model_call_execution.json`
- `tests/test_v1_g46_live_provider_model_call_execution.py`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`

Sparkbot:

- none

Arc-Bot-shell:

- none

## Guardrails

- Prevalidated V1-G44 authority metadata is required for future execution.
- The provider executor must be injected by the caller.
- No built-in provider SDK clients.
- No direct network client implementation.
- No ambient environment secret lookup.
- No credential value persistence.
- No fallback execution.
- No consumer repo edits.
- No connector/browser/network/device/robotics/physical-world behavior beyond the explicitly injected provider executor boundary if approved.
- No external sends.
- No product-readiness or production-readiness claims.

## Validation For This Request Packet

- `python -m pytest -q tests/test_v1_g46_live_provider_model_call_execution_approval_request.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g46_live_provider_model_call_execution_approval_request.py tests/test_v1_g45_runtime_export_cleanup_public_api_refresh.py tests/test_v1_g44_live_provider_model_call_authority.py tests/test_v1_g22_final_public_api_freeze.py tests/test_v1_g20_provider_model_routing_authority.py -p no:cacheprovider`
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit

## Next Action

Ask the operator to approve, revise, or pause the V1-G46 implementation request. Implementation must not begin until the operator records `Approve-V1-G46` with the exact approval wording from the request.
