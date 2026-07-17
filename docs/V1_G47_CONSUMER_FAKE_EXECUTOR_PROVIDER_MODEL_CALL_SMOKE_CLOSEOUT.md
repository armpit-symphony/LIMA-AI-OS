# V1-G47 Consumer Fake-Executor Provider Model Call Smoke Closeout

Date: 2026-06-17
Branch: `v1-g47-consumer-fake-executor-provider-model-call-smoke`
API status: `CANDIDATE_ONLY`

Closeout verdict: `complete_pending_independent_audit`

V1-G47 is complete as an approved consumer fake-executor provider/model call smoke slice. It proves the V1-G46 public harness import/call shape from Sparkbot and Arc-Bot-shell with fake in-process provider executors only.

## Completed Scope

LIMA runtime files changed:

- none

LIMA docs/tests/fixtures changed:

- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE.md`
- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g47_consumer_fake_executor_provider_model_call_smoke.json`
- `tests/test_v1_g47_consumer_fake_executor_provider_model_call_smoke.py`

Sparkbot test/fixture files added:

- `tests/fixtures/sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.json`
- `tests/test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py`

Arc-Bot-shell test/fixture files added:

- `tests/fixtures/arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.json`
- `tests/test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py`

## Consumer Commits

- Sparkbot: `83918032f52f069d16796865066ea78dfd182d58`
- Arc-Bot-shell: `3edf31f2ee3143756db8d9410009cd87e98bba71`

## Validation Evidence

Required validation for this implementation:

- `python -B -m pytest -q tests\test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py -p no:cacheprovider` - passed, 8 tests.
- `python -B -m pytest -q tests\test_sparkbot_lima_v1_g42_shell_wiring_implementation.py -p no:cacheprovider` - passed, 9 tests.
- `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py -p no:cacheprovider` - passed, 8 tests.
- `python -B -m pytest -q tests\test_arc_bot_shell_lima_v1_g42_shell_wiring_implementation.py -p no:cacheprovider` - passed, 9 tests.
- `git diff --check` in Sparkbot and Arc-Bot-shell - passed.
- `git diff --cached --check` in Sparkbot and Arc-Bot-shell - passed.

LIMA validation is recorded in the implementation fixture and will be refreshed before the implementation commit.

- `python -m pytest -q tests\test_v1_g47_consumer_fake_executor_provider_model_call_smoke.py tests\test_v1_g47_consumer_fake_executor_provider_model_call_smoke_approval_request.py tests\test_v1_g46_live_provider_model_call_execution.py tests\test_v1_g22_final_public_api_freeze.py -p no:cacheprovider` - passed, 77 tests.
- `python -m compileall lima` - passed.
- `python -m pytest -q tests -p no:cacheprovider` - passed, 4291 tests.

Optional consumer full-suite self-audit:

- Sparkbot full suite reproduced an existing order/state failure in older G38/G39/G41/G42 static tests after older G34 imports `lima`.
- Sparkbot full suite with `v1_g47` deselected reproduced the same failure.
- Arc-Bot-shell full suite reproduced the same existing order/state failure.
- Arc-Bot-shell full suite with `v1_g47` deselected reproduced the same failure.

No older consumer tests were edited because that would exceed the approved V1-G47 file scope.

## Boundary Results

- Consumer fake-executor smoke evidence: complete.
- Fake in-process provider executor invocation: complete in tests only.
- Real provider executor invocation: not added.
- Live provider credentials: not used.
- Provider SDK clients: not added.
- Direct network code: not added.
- Network calls: not performed.
- Ambient secret lookup: not added.
- Credential value access: not added.
- Fallback execution: not added.
- Consumer production runtime/source edits: not added.
- Connector/browser/network/file/device/robotics/physical-world behavior: not added.
- Raw prompt, raw model response, raw customer data, secret, credential, provider token, API key, raw diff, full patch body, or raw file content persistence: not added.
- Product-readiness or production-readiness claim: not added.

## Rollback

Rollback is local and reversible:

- remove the four V1-G47 LIMA docs/tests/fixture files
- remove the two V1-G47 Sparkbot test/fixture files
- remove the two V1-G47 Arc-Bot-shell test/fixture files

Rollback does not require `lima/` runtime file repair, consumer production runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Next Step

Create an independent V1-G47 audit branch. Do not proceed to real provider executor integration, provider credential access, provider network egress, built-in provider SDK clients, fallback execution, connector/browser/network authority, physical-world authority, or product-readiness claims without a later explicit approval gate.
