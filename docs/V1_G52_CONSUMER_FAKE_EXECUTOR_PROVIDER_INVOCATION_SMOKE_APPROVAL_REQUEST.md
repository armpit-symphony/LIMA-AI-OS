# V1-G52 Consumer Fake-Executor Provider Invocation Smoke Approval Request

Date: 2026-06-18
Branch: `prepare-v1-g52-consumer-fake-executor-provider-invocation-smoke-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create consumer tests, invoke fake provider executors, execute live provider/model calls, add provider SDK clients, make network calls, read secrets, access credential values, execute fallback, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G52 implementation of the consumer fake-executor provider invocation smoke slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G51, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G52 Objective

Implement the smallest consumer-facing fake-executor smoke slice for the V1-G51 public harness wrapper.

The proposed implementation would add focused Sparkbot and Arc-Bot-shell tests/fixtures that import the public V1-G51 `lima.harness` executable provider invocation wrapper and call it with a fake in-process provider executor only. The slice is meant to prove that both consumer repositories can exercise the public import/call shape without live provider credentials, real network calls, built-in provider SDK clients, endpoint resolution, connector behavior, production runtime calls, or product-readiness claims.

Future consumer imports if approved:

- `V1ExecutableRealProviderExecutorInvocationError`
- `execute_v1_executable_real_provider_executor_invocation`

The approved future implementation must use a fake in-process provider executor only. It must not use real provider credentials, make network calls, add built-in provider SDK clients, resolve provider endpoints, execute fallback, invoke connectors, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- none

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

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G52 may add only deterministic fake-executor smoke tests/fixtures and LIMA-side evidence docs/tests/fixtures.

Allowed if approved:

- add focused Sparkbot tests/fixtures for fake-executor V1-G51 import/call smoke
- add focused Arc-Bot-shell tests/fixtures for fake-executor V1-G51 import/call smoke
- add LIMA-side docs/tests/fixtures recording the consumer evidence
- import the approved V1-G51 public harness symbols in consumer tests
- build sanitized V1-G50 invocation envelope metadata in consumer tests
- call the V1-G51 wrapper with a fake in-process provider executor only
- prove returned evidence is sanitized
- prove no live provider credentials, real network calls, built-in provider SDKs, endpoint resolution, fallback, connectors, browser/network/device/robotics/physical-world behavior, or product-readiness claims are added
- run focused consumer tests and record sanitized results in LIMA evidence

## Explicitly Forbidden

V1-G52 must not add:

- `lima/` runtime file changes
- consumer production runtime code edits
- live provider/model calls
- built-in provider SDK clients
- direct network client implementation
- provider endpoint resolution
- network calls
- ambient environment secret lookup
- secret lookup
- credential value access
- provider token or API key access
- fallback execution
- provider readiness network checks
- Token Guardian live routing
- connector behavior
- browser or network behavior
- tool execution outside local test execution
- action execution outside local fake-executor tests
- file mutation execution outside the exact approved files
- HumanInput bridge activation
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, background services, subprocesses, or threads
- raw diff persistence in LIMA evidence
- full patch content persistence in LIMA evidence
- raw file content persistence in LIMA evidence
- raw prompt, raw model response, raw customer data, raw secret, raw credential, provider token, or API key persistence
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA evidence fixture records `CANDIDATE_ONLY`
- no `lima/` runtime files are changed
- Sparkbot file edits stay limited to the approved two test/fixture files
- Arc-Bot-shell file edits stay limited to the approved two test/fixture files
- Sparkbot imports the approved V1-G51 public harness symbols
- Arc-Bot-shell imports the approved V1-G51 public harness symbols
- Sparkbot calls the V1-G51 wrapper with a fake in-process provider executor only
- Arc-Bot-shell calls the V1-G51 wrapper with a fake in-process provider executor only
- returned evidence is sanitized and does not persist raw prompts, raw model responses, raw customer data, secrets, credentials, provider tokens, API keys, raw diffs, or raw patches
- no live provider credentials, real network calls, built-in provider SDK clients, endpoint resolution, fallback execution, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G52 tests
- LIMA focused V1-G51 tests
- LIMA focused V1-G50 tests
- LIMA focused V1-G22 final public API freeze tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- Sparkbot focused V1-G52 fake-executor smoke test
- Sparkbot focused V1-G47 fake-executor smoke test
- Arc-Bot-shell focused V1-G52 fake-executor smoke test
- Arc-Bot-shell focused V1-G47 fake-executor smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

Do not require or run real provider credentials, real network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G52 changes:

- remove the V1-G52 LIMA docs/tests/fixture
- remove the V1-G52 Sparkbot test/fixture
- remove the V1-G52 Arc-Bot-shell test/fixture

Rollback must not require `lima/` runtime file changes, consumer production runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G52 files
- `lima/` runtime file changes are required
- consumer production runtime/source files must change
- live provider/model calls are added
- built-in provider SDK clients are added
- direct network client implementation is added
- provider endpoint resolution is added
- network calls are added
- ambient secret lookup or credential value access is added
- raw prompts, raw model responses, raw customer data, credentials, provider tokens, API keys, secrets, raw diffs, or full patches can persist or emit in evidence
- fallback execution is added
- provider readiness network checks are added
- Token Guardian live routing is added
- connector/browser/network/device/robotics/physical-world behavior is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Consumer fake-executor provider invocation smoke approved: no.
- Consumer fake-executor provider invocation smoke added: no.
- Consumer repository edits approved: no.
- `lima/` runtime files changed by this request: no.
- Sparkbot files changed by this request: no.
- Arc-Bot-shell files changed by this request: no.
- Fake provider executor invoked by this request: no.
- Live provider/model calls added: no.
- No live provider credentials used: yes.
- Network calls performed: no.
- Secret lookup added: no.
- Credential value access added: no.
- Provider endpoint resolution added: no.
- Fallback execution added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g52-consumer-fake-executor-provider-invocation-smoke` in LIMA-AI-OS and corresponding scoped consumer branches as needed. Implement only the exact fake-executor consumer smoke slice. Do not add live provider credentials, real network calls, built-in provider SDK clients, endpoint resolution, fallback, connectors, physical-world behavior, or product readiness claims.
