# V1-G52 Consumer Fake-Executor Provider Invocation Smoke

Date: 2026-06-18
Branch: `v1-g52-consumer-fake-executor-provider-invocation-smoke`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_consumer_fake_executor_provider_invocation_smoke_slice`

V1-G52 implements the approved consumer fake-executor provider invocation smoke slice. It adds only focused Sparkbot and Arc-Bot-shell tests/fixtures plus LIMA-side evidence docs/tests/fixtures proving that both consumer repositories can import the public V1-G51 `lima.harness` symbols and call the V1-G51 executable provider invocation wrapper with an in-process fake provider executor.

This slice does not edit `lima/` runtime files, edit consumer production runtime/source files, call real providers, add provider SDK clients, resolve provider endpoints, make network calls, look up secrets, access credential values, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw prompts/model responses/customer data/secrets/credentials/provider tokens/API keys/raw diffs/raw patches, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G52` approval wording.

Approved implementation branch:

- `v1-g52-consumer-fake-executor-provider-invocation-smoke`

Approved scope:

- `consumer_fake_executor_provider_invocation_smoke_slice`

## Consumer Smoke Result

The V1-G52 smoke result is:

- `consumer_fake_executor_provider_invocation_smoke_evidence_created`

This means both consumer repositories have deterministic test evidence that imports the approved V1-G51 public harness surface, builds sanitized V1-G50 invocation envelope metadata, and executes the wrapper with a fake in-process provider executor only.

It does not approve real provider credentials, provider network egress, built-in provider SDK clients, endpoint resolution, fallback execution, connector/browser/network authority, physical-world behavior, or product readiness.

## Consumer Files Added

Sparkbot:

- Repository: `sparkpit-labs/Sparkbot`
- Branch: `v1-g52-consumer-fake-executor-provider-invocation-smoke`
- Saved commit: `77838a00f981bbae1e2f299055df4f4ee7d9663a`
- Files:
  - `tests/test_sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.py`
  - `tests/fixtures/sparkbot_lima_v1_g52_fake_executor_provider_invocation_smoke.json`

Arc-Bot-shell:

- Repository: `armpit-symphony/Arc-Bot-shell`
- Branch: `v1-g52-consumer-fake-executor-provider-invocation-smoke`
- Saved commit: `8358b8c3afb0bc18b886b19452e160c3c560e3cf`
- Files:
  - `tests/test_arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.py`
  - `tests/fixtures/arc_bot_shell_lima_v1_g52_fake_executor_provider_invocation_smoke.json`

## Imported Public Symbols

Both consumer tests import only these approved public harness symbols from the local sibling LIMA checkout:

- `V1ExecutableRealProviderExecutorInvocationError`
- `execute_v1_executable_real_provider_executor_invocation`

The tests build sanitized V1-G50 invocation envelope metadata and call `execute_v1_executable_real_provider_executor_invocation` with a fake in-process provider executor only.

## LIMA Files Added

V1-G52 changed only these LIMA-AI-OS files:

- `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE.md`
- `docs/V1_G52_CONSUMER_FAKE_EXECUTOR_PROVIDER_INVOCATION_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g52_consumer_fake_executor_provider_invocation_smoke.json`
- `tests/test_v1_g52_consumer_fake_executor_provider_invocation_smoke.py`

No `lima/` runtime file was created, edited, removed, renamed, imported by implementation docs, or expanded by this slice.

## Required Distinction

V1-G52 separates:

- consumer fake-executor provider invocation smoke evidence: approved and implemented
- new LIMA runtime behavior: not added
- consumer production runtime integration: not added
- real provider credential access: not approved and not implemented
- provider network egress: not approved and not implemented
- built-in provider SDK clients: not approved and not implemented
- provider endpoint resolution: not approved and not implemented
- fallback execution: not approved and not implemented
- connector/browser/network/file/device/robotics/physical-world behavior: not approved and not implemented
- raw sensitive content persistence: not approved and not implemented
- product readiness: not approved and not claimed

## Boundaries

- Consumer fake-executor provider invocation smoke approved: yes.
- Consumer fake-executor provider invocation smoke added: yes.
- Sparkbot approved test/fixture files added: yes.
- Arc-Bot-shell approved test/fixture files added: yes.
- `lima/` runtime files changed: no.
- LIMA public API expanded by V1-G52: no.
- Consumer production runtime/source files changed: no.
- New LIMA runtime behavior added by V1-G52: no.
- V1-G50 invocation envelope metadata used: yes.
- Fake in-process provider executor invoked by consumer tests: yes.
- Actual external provider invoked: no.
- Live provider credentials used: no.
- Built-in provider SDK added: no.
- Direct network code added: no.
- Provider endpoint resolution added: no.
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

V1-G52 is ready for independent audit.

The next smallest safe step is a separate V1-G52 audit branch. Do not proceed to built-in provider SDK clients, provider credential access, provider network egress, endpoint resolution, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, or product-readiness claims from this implementation branch.
