# V1-G52 Consumer Fake-Executor Provider Invocation Smoke Audit

Date: 2026-06-18
Branch: `audit-v1-g52-consumer-fake-executor-provider-invocation-smoke`
API status: `CANDIDATE_ONLY`

Audit verdict: `pass_bounded_consumer_fake_executor_provider_invocation_smoke`

This audit reviews the approved V1-G52 consumer fake-executor provider invocation smoke slice. The implementation adds focused Sparkbot and Arc-Bot-shell tests/fixtures plus LIMA-side evidence proving both consumer repositories can import the public V1-G51 `lima.harness` executable provider invocation wrapper and call it with a fake in-process provider executor only.

## Reviewed Evidence

- Approval request: `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_APPROVAL_REQUEST.md`
- Operator decision packet: `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_OPERATOR_DECISION_PACKET.md`
- Implementation doc: `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE.md`
- Closeout doc: `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_CLOSEOUT.md`
- LIMA evidence fixture: `tests/fixtures/runtime_extraction/v1_g52_consumer_fake_executor_provider_invocation_smoke.json`
- LIMA test module: `tests/test_v1_g52_consumer_fake_executor_provider_invocation_smoke.py`
- Sparkbot fixture: `../Sparkbot/tests/fixtures/sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.json`
- Sparkbot test: `../Sparkbot/tests/test_sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.py`
- Arc-Bot-shell fixture: `../Arc-Bot-shell/tests/fixtures/arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.json`
- Arc-Bot-shell test: `../Arc-Bot-shell/tests/test_arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.py`
- Prior wrapper evidence: `docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION.md`
- Prior invocation envelope evidence: `docs/V1_G50_REAL_PROVIDER_EXECUTOR_INVOCATION.md`

## Scope Audit

- Exact `Approve-V1-G52` approval wording recorded: pass.
- Approved implementation branch used in all three repos: pass.
- LIMA changes stayed limited to the four approved docs/tests/fixture files: pass.
- LIMA `lima/` runtime files changed by V1-G52: none, pass.
- LIMA public API changed by V1-G52: none, pass.
- Sparkbot changes stayed limited to the two approved test/fixture files: pass.
- Arc-Bot-shell changes stayed limited to the two approved test/fixture files: pass.
- Consumer production runtime/source files changed: none, pass.
- Consumer branches and commits are recorded in LIMA evidence: pass.
- Rollback metadata removes only exact approved V1-G52 files: pass.

## Consumer Evidence Audit

- Sparkbot saved commit: `77838a00f981bbae1e2f299055df4f4ee7d9663a`.
- Arc-Bot-shell saved commit: `8358b8c3afb0bc18b886b19452e160c3c560e3cf`.
- Sparkbot imports only `V1ExecutableRealProviderExecutorInvocationError` and `execute_v1_executable_real_provider_executor_invocation`: pass.
- Arc-Bot-shell imports only `V1ExecutableRealProviderExecutorInvocationError` and `execute_v1_executable_real_provider_executor_invocation`: pass.
- Sparkbot builds sanitized V1-G50 invocation envelope metadata: pass.
- Arc-Bot-shell builds sanitized V1-G50 invocation envelope metadata: pass.
- Sparkbot calls the V1-G51 wrapper with a fake in-process provider executor only: pass.
- Arc-Bot-shell calls the V1-G51 wrapper with a fake in-process provider executor only: pass.
- Consumer tests do not import Sparkbot runtime modules, Arc runtime modules, FastAPI routes, WebSocket routes, `stream_chat_with_tools`, `execute_tool`, or production shell wiring: pass.

## Behavior Audit

- No new LIMA runtime behavior added by V1-G52: pass.
- V1-G51 wrapper remains the existing public runtime boundary: pass.
- V1-G52 uses fake in-process provider executors only: pass.
- Actual external provider invocation remains absent: pass.
- Live provider credentials remain absent: pass.
- Built-in provider SDK clients remain absent: pass.
- Direct provider SDK usage remains absent: pass.
- Direct network client code remains absent: pass.
- Provider endpoint resolution remains absent: pass.
- Network calls remain absent: pass.
- Secret lookup and credential value access remain absent: pass.
- Provider token/API key access remains absent: pass.
- Provider configuration changes remain absent: pass.
- Fallback execution remains absent: pass.
- Provider readiness network checks remain absent: pass.
- Token Guardian live routing remains absent: pass.
- Connector/browser/network/file/device/robotics/physical-world behavior remains absent: pass.
- Scheduled task execution and external sends remain absent: pass.
- Product-readiness and production-readiness claims remain absent: pass.

## Redaction And Evidence Audit

- Consumer fixtures persist sanitized refs and expected sanitized execution records only: pass.
- Raw prompt persistence is not allowed and not present: pass.
- Raw model response persistence is not allowed and not present: pass.
- Raw customer data persistence is not allowed and not present: pass.
- Raw secret, credential, provider token, or API key persistence is not allowed and not present: pass.
- Raw diff, patch, and file content persistence is not allowed and not present: pass.
- LIMA fixture and docs avoid raw patch bodies and sensitive markers: pass.

## Validation Evidence

- `python -B -m pytest -q tests\test_sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.py -p no:cacheprovider` - passed, 8 tests.
- `python -B -m pytest -q tests\test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py -p no:cacheprovider` - passed, 8 tests.
- `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.py -p no:cacheprovider` - passed, 8 tests.
- `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py -p no:cacheprovider` - passed, 8 tests.
- `python -m pytest -q tests\test_v1_g52_consumer_fake_executor_provider_invocation_smoke.py -p no:cacheprovider` - passed, 12 tests.
- `python -m pytest -q tests\test_v1_g52_consumer_fake_executor_provider_invocation_smoke.py tests\test_v1_g51_executable_real_provider_executor_invocation.py tests\test_v1_g50_real_provider_executor_invocation.py tests\test_v1_g22_final_public_api_freeze.py -p no:cacheprovider` - passed, 144 tests.
- `python -m compileall lima` - passed.
- `python -m pytest -q tests -p no:cacheprovider` - passed, 4536 tests.
- `git diff --check` - passed in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell.
- `git diff --cached --check` - must pass before this audit commit.

## Residual Risk

V1-G52 is candidate-only consumer smoke evidence. It proves consumer import/call compatibility with the V1-G51 wrapper through fake in-process executors only. It does not approve built-in provider SDK integration, endpoint resolution, direct provider egress, secret lookup, credential value access, fallback execution, connector/browser/network authority, physical-world behavior, consumer production runtime integration, shell runtime wiring, or product readiness.

Arc-Bot-shell status still reports a `.pytest_cache/` permission warning during `git status`. The warning is unrelated to V1-G52 tracked file scope and does not affect `git diff --check` or the approved files.

## Audit Decision

V1-G52 passes independent audit as a bounded consumer fake-executor provider invocation smoke slice.

Recommended next step: create a V1 runtime authority chain audit through G52, then update readiness/next-lane metadata. Do not proceed to built-in provider SDK clients, provider credential access, provider network egress, endpoint resolution, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, or product-readiness claims from this audit branch.
