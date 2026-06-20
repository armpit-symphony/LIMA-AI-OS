# V1-G60 SDK Dependency Vendor Provider SDK Import Work Order

Date: 2026-06-20
Branch: `prepare-v1-g60-sdk-dependency-vendor-provider-sdk-import-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `request_only_not_approved`

## Objective

Prepare an operator decision gate for the next post-G59 SDK dependency addition and vendor provider SDK import approval lane.

The requested future implementation would prove whether LIMA may add a declared provider SDK dependency and perform a bounded local vendor provider SDK importability proof. This work order does not approve or implement dependency additions, dependency manifest edits, lockfile edits, vendor SDK imports, provider SDK clients, client construction, endpoint resolution, network egress, secret lookup, credential-value access, fallback execution, consumer runtime integration, connectors, browser/network/device/robotics behavior, or product readiness.

## Inputs

- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G59.md`
- `docs/readiness/V1_POST_G59_NEXT_LANE_DECISION_MATRIX.md`
- `docs/audits/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_AUDIT.md`
- `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md`
- `docs/audits/V1_G58_BUILT_IN_PROVIDER_SDK_CLIENT_AUTHORITY_CONTRACT_AUDIT.md`
- `docs/V1_G58_BUILT_IN_PROVIDER_SDK_CLIENT_AUTHORITY_CONTRACT.md`
- `docs/audits/V1_G57_PROVIDER_EXECUTION_HARDENING_AUTHORIZATION_AUDIT.md`
- `docs/V1_G56_CONSUMER_FAKE_EXECUTOR_PROVIDER_SDK_NETWORK_EGRESS_SMOKE.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS.md`
- `docs/V1_G54_FAKE_SDK_EGRESS_HARNESS.md`
- `docs/V1_G53_PROVIDER_SDK_NETWORK_CREDENTIAL_AUTHORITY.md`
- `docs/V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING.md`

## Request-Only File Scope

- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_APPROVAL_REQUEST.md`
- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_WORK_ORDER.md`
- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_PREFLIGHT_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_g60_sdk_dependency_vendor_provider_sdk_import_approval_request.json`
- `tests/test_v1_g60_sdk_dependency_vendor_provider_sdk_import_approval_request.py`

## Proposed Implementation File Scope If Approved Later

LIMA-AI-OS runtime files:

- none

Dependency manifest files:

- `pyproject.toml`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT.md`
- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g60_sdk_dependency_vendor_provider_sdk_import.json`
- `tests/test_v1_g60_sdk_dependency_vendor_provider_sdk_import.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

No `lima/` runtime files may be changed. No lockfile may be changed unless a revised approval explicitly includes the lockfile.

## Guardrails

- Request-only gate.
- No SDK dependencies in this request branch.
- No dependency manifest or lockfile edits in this request branch.
- No vendor SDK imports in this request branch.
- No built-in provider SDK clients or client construction.
- No direct provider SDK call implementation by LIMA.
- No provider endpoint resolution execution by LIMA.
- No DNS, HTTP, socket, network calls, or direct provider egress by LIMA.
- No ambient secret lookup, secret lookup, credential-value access, provider token access, or API key access.
- No provider configuration changes.
- No credential storage, rotation, migration, provisioning, or value exposure.
- No fallback execution.
- No consumer production runtime/source edits.
- No connector/browser/network/device/robotics/physical-world behavior.
- No external sends.
- No product-readiness, production-readiness, or final public API freeze claims.

## Validation For This Request Packet

- `python -m pytest -q tests/test_v1_g60_sdk_dependency_vendor_provider_sdk_import_approval_request.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g60_sdk_dependency_vendor_provider_sdk_import_approval_request.py tests/test_v1_runtime_readiness_rollup_through_g59.py tests/test_v1_post_g59_next_lane_decision_matrix.py tests/test_v1_g59_sdk_dependency_vendor_provider_sdk_import_authority_audit.py tests/test_v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.py -p no:cacheprovider`
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit

## Next Action

Ask the operator to approve, revise, or pause the V1-G60 implementation request. Implementation must not begin until the operator records `Approve-V1-G60` with the exact approval wording from the request.
