# V1-G47 Consumer Fake-Executor Provider Model Call Smoke

Date: 2026-06-17
Branch: `v1-g47-consumer-fake-executor-provider-model-call-smoke`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_consumer_fake_executor_provider_model_call_smoke_slice`

V1-G47 implements the approved consumer fake-executor provider/model call smoke slice. It adds only focused Sparkbot and Arc-Bot-shell tests/fixtures plus LIMA-side evidence docs/tests/fixtures proving that both consumer repositories can import the public V1-G46 `lima.harness` symbols and call the V1-G46 wrapper with an in-process fake provider executor.

This slice does not edit `lima/` runtime files, edit consumer production runtime/source files, call real providers, add provider SDK clients, make network calls, look up secrets, access credential values, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw prompts/model responses/customer data/secrets/credentials/provider tokens/API keys/raw diffs/raw patches, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G47` approval wording.

Approved implementation branch:

- `v1-g47-consumer-fake-executor-provider-model-call-smoke`

Approved scope:

- `consumer_fake_executor_provider_model_call_smoke_slice`

## Consumer Smoke Result

The V1-G47 smoke result is:

- `consumer_fake_executor_provider_model_call_smoke_evidence_created`

This means both consumer repositories have deterministic test evidence that imports the approved V1-G46 public harness surface and executes the wrapper with a fake in-process provider executor only.

It does not approve real provider executors, real provider credentials, provider network egress, built-in provider SDK clients, fallback execution, connector/browser/network authority, physical-world behavior, or product readiness.

## Consumer Files Added

Sparkbot:

- Repository: `sparkpit-labs/Sparkbot`
- Branch: `v1-g47-consumer-fake-executor-provider-model-call-smoke`
- Saved commit: `83918032f52f069d16796865066ea78dfd182d58`
- Files:
  - `tests/fixtures/sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.json`
  - `tests/test_sparkbot_lima_v1_g47_fake_executor_provider_model_call_smoke.py`

Arc-Bot-shell:

- Repository: `armpit-symphony/Arc-Bot-shell`
- Branch: `v1-g47-consumer-fake-executor-provider-model-call-smoke`
- Saved commit: `3edf31f2ee3143756db8d9410009cd87e98bba71`
- Files:
  - `tests/fixtures/arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.json`
  - `tests/test_arc_bot_shell_lima_v1_g47_fake_executor_provider_model_call_smoke.py`

## Imported Public Symbols

Both consumer tests import only these approved public harness symbols from the local sibling LIMA checkout:

- `V1LiveProviderModelCallExecutionError`
- `execute_v1_live_provider_model_call`
- `validate_v1_live_provider_model_call_authority`

The tests build sanitized V1-G44 authority metadata and call `execute_v1_live_provider_model_call` with a fake in-process provider executor only.

## LIMA Files Added

V1-G47 changed only these LIMA-AI-OS files:

- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE.md`
- `docs/V1_G47_CONSUMER_FAKE_EXECUTOR_PROVIDER_MODEL_CALL_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g47_consumer_fake_executor_provider_model_call_smoke.json`
- `tests/test_v1_g47_consumer_fake_executor_provider_model_call_smoke.py`

No `lima/` runtime file was created, edited, removed, renamed, imported by implementation docs, or expanded by this slice.

## Validation Notes

Required focused validation passed for the new consumer tests and the prior G42 shell wiring tests.

An optional full consumer-suite run was attempted in both consumer repositories and reproduced a pre-existing order/state limitation even with `v1_g47` deselected: the older G34 live import/call tests load `lima`, then older static G38/G39/G41/G42 tests assert that `lima` is absent from `sys.modules`. V1-G47 did not edit those older tests because that is outside the approved file scope.

## Required Distinction

V1-G47 separates:

- fake in-process provider executor smoke evidence: approved and implemented
- real provider executor invocation: not approved and not implemented
- provider credential access: not approved and not implemented
- provider network egress: not approved and not implemented
- built-in provider SDK clients: not approved and not implemented
- fallback execution: not approved and not implemented
- consumer production runtime integration: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- raw sensitive content persistence: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Consumer fake-executor provider/model call smoke approved: yes.
- Consumer fake-executor provider/model call smoke added: yes.
- Sparkbot approved test/fixture files added: yes.
- Arc-Bot-shell approved test/fixture files added: yes.
- `lima/` runtime files changed: no.
- LIMA public API expanded: no.
- Consumer production runtime/source files changed: no.
- Real provider executor invoked: no.
- Live provider/model calls added by V1-G47: no.
- Built-in provider SDK added: no.
- Direct network code added: no.
- Network call performed: no.
- Ambient secret lookup added: no.
- Secret lookup added: no.
- Credential value access added: no.
- Provider token or API key access added: no.
- Fallback execution added: no.
- Provider readiness network check added: no.
- Token Guardian live routing added: no.
- Tool execution outside local tests added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- Raw prompt, raw model response, raw customer data, raw secret, raw credential, provider token, API key, raw diff, full patch, or raw file content persistence added: no.
- Product readiness approved: no.

## Readiness Result

V1-G47 is ready for independent audit.

The next smallest safe step is a separate V1-G47 audit branch. Do not proceed to real provider executor integration, provider credential access, provider network egress, built-in provider SDK clients, fallback execution, connector/browser/network authority, physical-world authority, or product-readiness claims from this implementation branch.
