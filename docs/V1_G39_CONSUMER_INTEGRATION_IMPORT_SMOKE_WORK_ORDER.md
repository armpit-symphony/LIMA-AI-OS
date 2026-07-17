# V1-G39 Consumer Integration Import-Smoke Work Order

Date: 2026-06-17
Branch: `prepare-v1-g39-consumer-integration-import-smoke-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `request_only_not_approved`

## Objective

Prepare an operator decision gate for the smallest consumer integration import-smoke slice after V1-G38.

The requested future implementation would create exact static import-smoke evidence files for Sparkbot and Arc-Bot-shell plus deterministic LIMA-side docs/tests/fixtures. This work order does not approve or implement that slice.

## Inputs

- `docs/V1_G38_CONSUMER_REPOSITORY_EDIT.md`
- `docs/V1_G38_CONSUMER_REPOSITORY_EDIT_CLOSEOUT.md`
- `docs/audits/V1_G38_CONSUMER_REPOSITORY_EDIT_AUDIT.md`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G38_AUDIT.md`
- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G38.md`
- `docs/readiness/V1_POST_G38_NEXT_LANE_DECISION_MATRIX.md`

## Request-Only File Scope

- `docs/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE_APPROVAL_REQUEST.md`
- `docs/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE_WORK_ORDER.md`
- `docs/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE_PREFLIGHT_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_g39_consumer_integration_import_smoke_approval_request.json`
- `tests/test_v1_g39_consumer_integration_import_smoke_approval_request.py`

## Proposed Implementation File Scope If Approved Later

LIMA-AI-OS:

- `docs/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE.md`
- `docs/V1_G39_CONSUMER_INTEGRATION_IMPORT_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g39_consumer_integration_import_smoke.json`
- `tests/test_v1_g39_consumer_integration_import_smoke.py`

Sparkbot:

- `tests/fixtures/sparkbot_lima_v1_g39_consumer_integration_import_smoke.json`
- `tests/test_sparkbot_lima_v1_g39_consumer_integration_import_smoke.py`

Arc-Bot-shell:

- `tests/fixtures/arc_bot_shell_lima_v1_g39_consumer_integration_import_smoke.json`
- `tests/test_arc_bot_shell_lima_v1_g39_consumer_integration_import_smoke.py`

## Guardrails

- No `lima/` runtime file changes.
- No consumer runtime/source file changes.
- No consumer file changes outside exact future approved paths.
- No raw patch body persistence.
- No adapter symbol calls.
- No consumer runtime module imports.
- No consumer integration implementation.
- No shell runtime wiring implementation.
- No provider/model calls or dispatch.
- No secret lookup or credential access.
- No connector/browser/network/device/robotics/physical-world behavior.
- No external sends.
- No product-readiness or production-readiness claims.

## Validation For This Request Packet

- `python -m pytest -q tests/test_v1_g39_consumer_integration_import_smoke_approval_request.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g38_consumer_repository_edit.py -p no:cacheprovider`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit

## Next Action

Ask the operator to approve, revise, or pause the V1-G39 implementation request. Implementation must not begin until the operator records `Approve-V1-G39` with the exact approval wording from the request.
