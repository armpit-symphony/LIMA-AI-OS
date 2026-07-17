# V1-G47 Consumer Fake-Executor Provider Model Call Smoke Audit

Date: 2026-06-17
Branch: `audit-v1-g47-consumer-fake-executor-provider-model-call-smoke`
Audited LIMA implementation branch: `v1-g47-consumer-fake-executor-provider-model-call-smoke`
Audited LIMA implementation commit: `3b252a4a8c75fbe3278b98a7f260a45e8bdd54a4`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit independently reviews the V1-G47 consumer fake-executor provider/model call smoke implementation. It validates that Sparkbot and Arc-Bot-shell can import the approved V1-G46 public harness symbols and execute the wrapper with fake in-process provider executors only.

The audit does not add or approve `lima/` runtime file changes, consumer production runtime/source edits, real provider executor invocation, live provider/model calls, provider SDK clients, direct network code, network calls, ambient secret lookup, credential value access, fallback execution, tools, connectors, browser/network/file/device/robotics/physical-world behavior, scheduled tasks, external sends, raw sensitive content persistence, or product readiness.

## Scope Reviewed

LIMA-AI-OS:

- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_APPROVAL_REQUEST.md`
- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE.md`
- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g47_consumer_fake_executor_provider_model_call_smoke.json`
- `tests/test_v1_g47_consumer_fake_executor_provider_model_call_smoke.py`

Sparkbot:

- Branch: `v1-g47-consumer-fake-executor-provider-model-call-smoke`
- Commit: `83918032f52f069d16796865066ea78dfd182d58`
- `tests/fixtures/sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.json`
- `tests/test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py`

Arc-Bot-shell:

- Branch: `v1-g47-consumer-fake-executor-provider-model-call-smoke`
- Commit: `3edf31f2ee3143756db8d9410009cd87e98bba71`
- `tests/fixtures/arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.json`
- `tests/test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py`

## Decision And File-Map Findings

- Exact `Approve-V1-G47` decision was recorded: pass.
- Exact approval wording was recorded: pass.
- Approved LIMA branch recorded as `v1-g47-consumer-fake-executor-provider-model-call-smoke`: pass.
- LIMA runtime file changes stayed empty: pass.
- LIMA docs/tests/fixtures changes stayed inside the approved four-file map: pass.
- Sparkbot changes stayed limited to the approved test/fixture pair: pass.
- Arc-Bot-shell changes stayed limited to the approved test/fixture pair: pass.
- Consumer production runtime/source files were not changed: pass.
- Product readiness was not claimed: pass.

## Consumer Import/Call Findings

- Sparkbot imports the approved V1-G46 public harness symbols: pass.
- Arc-Bot-shell imports the approved V1-G46 public harness symbols: pass.
- Sparkbot validates sanitized V1-G44 authority metadata before execution: pass.
- Arc-Bot-shell validates sanitized V1-G44 authority metadata before execution: pass.
- Sparkbot calls `execute_v1_live_provider_model_call` with a fake in-process provider executor only: pass.
- Arc-Bot-shell calls `execute_v1_live_provider_model_call` with a fake in-process provider executor only: pass.
- Missing fake executor fails closed through `V1LiveProviderModelCallExecutionError`: pass.
- Returned evidence is sanitized and records redacted refs only: pass.
- Tests avoid consumer runtime imports and production runtime calls: pass.

## Boundary Findings

- `lima/` runtime files were not changed by V1-G47: pass.
- LIMA public API exports were not expanded by V1-G47: pass.
- Real provider executor invocation was not added: pass.
- Live provider/model calls were not added by V1-G47: pass.
- Live provider credentials were not used: pass.
- Built-in provider SDK clients were not added: pass.
- Direct network client code was not added: pass.
- Network calls were not performed: pass.
- Ambient environment secret lookup was not added: pass.
- Secret lookup was not added: pass.
- Credential access and credential value access were not added: pass.
- Provider readiness network checks were not added: pass.
- Token Guardian live routing was not added: pass.
- Fallback execution was not added: pass.
- Tool execution outside local tests was not added: pass.
- Connector/browser/network/file/device/robotics/physical-world behavior was not added: pass.
- Scheduled task execution was not added: pass.
- External sends were not added: pass.
- Product readiness was not claimed: pass.

## Data Protection Findings

- Raw prompts were not persisted or emitted in LIMA evidence: pass.
- Raw model responses were not persisted or emitted in LIMA evidence: pass.
- Raw customer data was not persisted or emitted: pass.
- Raw secrets were not persisted or emitted: pass.
- Raw credentials were not persisted or emitted: pass.
- Provider tokens and API keys were not persisted or emitted: pass.
- Raw diffs or full patch bodies were not persisted: pass.
- Raw file contents were not persisted in LIMA evidence: pass.

## Full Consumer Suite Self-Audit

Optional full consumer-suite runs were attempted in both Sparkbot and Arc-Bot-shell. They failed on an existing order/state limitation that also reproduces with `v1_g47` deselected:

- Older G34 live import/call tests import `lima`.
- Older static G38/G39/G41/G42 tests later assert `lima` is absent from `sys.modules`.

This is not treated as a V1-G47 required validation failure because the V1-G47 approval request required focused V1-G47 and G42 consumer tests, those focused tests passed, and editing older tests would exceed the approved V1-G47 file scope.

## Residual Gaps

- Real provider executor integration remains unapproved.
- Built-in provider SDK integration remains unapproved.
- Direct provider network egress remains unapproved.
- Secret lookup and credential value access remain unapproved.
- Provider readiness network checks remain unapproved.
- Fallback execution remains unapproved.
- Connector/browser/network authority remains unapproved.
- Consumer production runtime call expansion remains approval-gated.
- Physical-world/device/robot/drone/IoT authority remains blocked pending a dedicated safety lane.
- Product readiness remains incomplete.

## Validation Evidence

- Sparkbot `python -B -m pytest -q tests\test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py -p no:cacheprovider`: pass, `8 passed`.
- Sparkbot `python -B -m pytest -q tests\test_sparkbot_lima_v1_g42_shell_wiring_implementation.py -p no:cacheprovider`: pass, `9 passed`.
- Arc-Bot-shell `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py -p no:cacheprovider`: pass, `8 passed`.
- Arc-Bot-shell `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g42_shell_wiring_implementation.py -p no:cacheprovider`: pass, `9 passed`.
- LIMA `python -m pytest -q tests\test_v1_g47_consumer_fake_executor_provider_model_call_smoke.py tests\test_v1_g47_consumer_fake_executor_provider_model_call_smoke_approval_request.py tests\test_v1_g46_live_provider_model_call_execution.py tests\test_v1_g22_final_public_api_freeze.py -p no:cacheprovider`: pass, `77 passed`.
- LIMA `python -m compileall lima`: pass.
- LIMA `python -m pytest -q tests -p no:cacheprovider`: pass, `4291 passed`.
- `git diff --check` in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell: pass.
- `git diff --cached --check`: pass before implementation commit.

## Audit Conclusion

V1-G47 passes audit as a candidate consumer fake-executor provider/model call smoke slice. It proves that Sparkbot and Arc-Bot-shell can exercise the approved V1-G46 public harness wrapper with fake in-process provider executors only, while preserving the no-real-provider, no-network, no-secret, no-fallback, no-connector, no-physical-world, and no-product-readiness boundaries.

Recommended next safe step: audit the V1 runtime authority chain through V1-G47, then update readiness and decide the next exact approval-gated lane. The likely next lane is provider credential/network hardening as a request-only gate before any real provider SDK, credential, or network work.
