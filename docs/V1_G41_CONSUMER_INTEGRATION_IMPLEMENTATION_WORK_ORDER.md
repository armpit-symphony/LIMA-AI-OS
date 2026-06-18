# V1-G41 Consumer Integration Implementation Work Order

Date: 2026-06-17
Branch: `prepare-v1-g41-consumer-integration-implementation-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `request_only_not_approved`

## Objective

Prepare an operator decision gate for the smallest bounded consumer integration implementation evidence slice after V1-G40.

The requested future implementation would create deterministic static consumer integration implementation evidence for Sparkbot and Arc-Bot-shell without editing runtime/source files, implementing shell runtime wiring, calling adapter symbols, or dispatching live provider/model requests. This work order does not approve or implement that slice.

## Inputs

- `docs/V1_G40_SHELL_WIRING_DESIGN.md`
- `docs/V1_G40_SHELL_WIRING_DESIGN_CLOSEOUT.md`
- `docs/audits/V1_G40_SHELL_WIRING_DESIGN_AUDIT.md`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G40_AUDIT.md`
- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G40.md`
- `docs/readiness/V1_POST_G40_NEXT_LANE_DECISION_MATRIX.md`

## Request-Only File Scope

- `docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION_APPROVAL_REQUEST.md`
- `docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION_WORK_ORDER.md`
- `docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION_PREFLIGHT_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_g41_consumer_integration_implementation_approval_request.json`
- `tests/test_v1_g41_consumer_integration_implementation_approval_request.py`

## Proposed Implementation File Scope If Approved Later

LIMA-AI-OS:

- `docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION.md`
- `docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g41_consumer_integration_implementation.json`
- `tests/test_v1_g41_consumer_integration_implementation.py`

Sparkbot:

- `tests/fixtures/sparkbot_lima_v1_g41_consumer_integration_implementation.json`
- `tests/test_sparkbot_lima_v1_g41_consumer_integration_implementation.py`

Arc-Bot-shell:

- `tests/fixtures/arc_bot_shell_lima_v1_g41_consumer_integration_implementation.json`
- `tests/test_arc_bot_shell_lima_v1_g41_consumer_integration_implementation.py`

## Guardrails

- No `lima/` runtime file changes.
- No Sparkbot or Arc-Bot-shell file changes outside exact approved test/fixture paths if later approved.
- No consumer runtime/source file changes.
- No raw patch body persistence.
- No adapter symbol calls.
- No consumer runtime module imports.
- No shell runtime wiring implementation.
- No provider/model calls or dispatch.
- No secret lookup or credential access.
- No connector/browser/network/device/robotics/physical-world behavior.
- No external sends.
- No product-readiness or production-readiness claims.

## Validation For This Request Packet

- `python -m pytest -q tests/test_v1_g41_consumer_integration_implementation_approval_request.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g40_shell_wiring_design.py -p no:cacheprovider`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit

## Next Action

Ask the operator to approve, revise, or pause the V1-G41 implementation request. Implementation must not begin until the operator records `Approve-V1-G41` with the exact approval wording from the request.
