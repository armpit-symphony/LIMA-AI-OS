# V1-G52 Consumer Fake-Executor Provider Invocation Smoke Work Order

Date: 2026-06-18
Branch: `prepare-v1-g52-consumer-fake-executor-provider-invocation-smoke-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `request_only_not_approved`

## Objective

Prepare an operator decision gate for consumer fake-executor smoke tests against the V1-G51 public harness wrapper.

The requested future implementation would add focused Sparkbot and Arc-Bot-shell tests/fixtures that import the V1-G51 public `lima.harness` executable provider invocation wrapper and call it with fake in-process provider executors only. This work order does not approve or implement that slice.

## Inputs

- `docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION.md`
- `docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md`
- `docs/audits/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION_AUDIT.md`
- `docs/audits/V1_RUNTIME_AUTHORITY_CHAIN_THROUGH_G51_AUDIT.md`
- `docs/readiness/V1_RUNTIME_READINESS_ROLLUP_THROUGH_G51.md`
- `docs/readiness/V1_POST_G51_NEXT_LANE_DECISION_MATRIX.md`
- `docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION.md`
- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE.md`
- `docs/V1_G42_SHELL_WIRING_IMPLEMENTATION.md`
- `docs/V1_G41_CONSUMER_INTEGRATION_IMPLEMENTATION.md`

## Request-Only File Scope

- `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_APPROVAL_REQUEST.md`
- `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_WORK_ORDER.md`
- `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_PREFLIGHT_AUDIT.md`
- `tests/fixtures/runtime_extraction/v1_g52_consumer_fake_executor_provider_invocation_smoke_approval_request.json`
- `tests/test_v1_g52_consumer_fake_executor_provider_invocation_smoke_approval_request.py`

## Proposed Implementation File Scope If Approved Later

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE.md`
- `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g52_consumer_fake_executor_provider_invocation_smoke.json`
- `tests/test_v1_g52_consumer_fake_executor_provider_invocation_smoke.py`

Sparkbot:

- `tests/test_sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.py`
- `tests/fixtures/sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.json`

Arc-Bot-shell:

- `tests/test_arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.py`
- `tests/fixtures/arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.json`

No `lima/` runtime files may be changed.

## Guardrails

- Fake in-process provider executor only.
- No real provider credentials.
- No real provider/network calls.
- No built-in provider SDK clients.
- No provider endpoint resolution.
- No direct network client implementation.
- No ambient environment secret lookup.
- No credential value access.
- No fallback execution.
- No consumer production runtime/source edits.
- No connector/browser/network/device/robotics/physical-world behavior.
- No external sends.
- No product-readiness or production-readiness claims.

## Validation For This Request Packet

- `python -m pytest -q tests/test_v1_g52_consumer_fake_executor_provider_invocation_smoke_approval_request.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g52_consumer_fake_executor_provider_invocation_smoke_approval_request.py tests/test_v1_g51_executable_real_provider_executor_invocation.py tests/test_v1_g50_real_provider_executor_invocation.py tests/test_v1_g22_final_public_api_freeze.py -p no:cacheprovider`
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit

## Next Action

Ask the operator to approve, revise, or pause the V1-G52 implementation request. Implementation must not begin until the operator records `Approve-V1-G52` with the exact approval wording from the request.
