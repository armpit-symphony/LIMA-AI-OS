# V1-G46 Live Provider Model Call Execution Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g46-live-provider-model-call-execution-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, execute live provider/model calls, invoke a provider executor, add provider SDK clients, make network calls, read secrets, access credential values, execute fallback, execute tools, edit consumer repositories, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G46 implementation of the live provider/model call execution slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G45, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G46 Objective

Implement the smallest LIMA-side live provider/model call execution slice after V1-G45.

The proposed implementation would add a guarded harness execution wrapper that can invoke a caller-supplied provider executor only when a prevalidated V1-G44 live provider/model call authority record is present. The provider executor must be injected by the caller; V1-G46 must not add built-in provider SDK clients, ambient environment secret lookup, credential value reads, fallback execution, consumer repository edits, or product-readiness claims.

Proposed execution target:

- Package: `lima.harness`
- New runtime module: `lima/harness/v1_live_provider_model_call_execution.py`
- Public export surface: `lima.harness.__all__`
- Existing authority prerequisite: prevalidated V1-G44 authority metadata/preflight record
- Future public symbols to expose through `__all__` if approved:
  - `V1LiveProviderModelCallExecutionError`
  - `execute_v1_live_provider_model_call`

The proposed implementation may define a local execution request/result record, enforce authority and redaction constraints, invoke only the injected provider executor, and return sanitized audit metadata. It must not add direct provider SDK code, direct network client code, environment variable secret lookup, raw credential persistence, fallback execution, connector/browser/network behavior, consumer runtime calls, or physical-world behavior.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- `lima/harness/v1_live_provider_model_call_execution.py`
- `lima/harness/__init__.py`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION.md`
- `docs/V1_G46_LIVE_PROVIDER_MODEL_CALL_EXECUTION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g46_live_provider_model_call_execution.json`
- `tests/test_v1_g46_live_provider_model_call_execution.py`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`

Sparkbot:

- none

Arc-Bot-shell:

- none

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G46.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G46 may add only the bounded live provider/model call execution harness described below.

Allowed if approved:

- add a LIMA harness execution wrapper for live provider/model calls
- require prevalidated V1-G44 authority metadata before execution
- require a caller-injected provider executor
- call the injected provider executor only from the approved harness function
- record sanitized execution metadata and audit linkage
- allow raw prompt/model response data to exist only as transient in-memory inputs/outputs for the single approved call path
- prohibit raw prompt/model response/customer data persistence in fixtures, docs, audit metadata, logs, or returned evidence
- expose only `V1LiveProviderModelCallExecutionError` and `execute_v1_live_provider_model_call` through `lima.harness.__all__`
- preserve every existing `lima.harness.__all__` export
- refresh the V1-G22 candidate public API freeze fixture for the approved export change only
- add focused fake-executor tests proving authority enforcement, sanitized evidence, and denied-path behavior
- document rollback and closeout evidence

## Explicitly Forbidden

V1-G46 must not add:

- any `lima/` runtime file changes outside the approved V1-G46 runtime files
- built-in provider SDK clients
- direct network client implementation
- ambient environment variable secret lookup
- raw credential value reads or persistence
- provider token or API key persistence
- fallback execution
- provider readiness network checks
- Token Guardian live routing
- unscoped model request dispatch
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer repository edits
- consumer runtime calls
- connector behavior
- browser or network behavior outside the injected provider executor boundary
- tool execution
- action execution
- file mutation execution outside the exact approved files
- HumanInput bridge activation
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, background services, subprocesses, or threads
- raw diff persistence
- full patch content persistence
- raw file content persistence
- raw prompt, raw model response, raw customer data, raw secret, raw credential, provider token, or API key persistence
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA execution fixture records `CANDIDATE_ONLY`
- only the approved V1-G46 runtime files are changed
- existing `lima.harness.__all__` exports remain present
- `V1LiveProviderModelCallExecutionError` is exported through `lima.harness.__all__`
- `execute_v1_live_provider_model_call` is exported through `lima.harness.__all__`
- V1-G22 final public API freeze fixture is refreshed only for the approved G46 harness export change
- execution fails closed without prevalidated V1-G44 authority metadata
- execution fails closed without an injected provider executor
- fake executor invocation is explicit and deterministic in tests
- returned evidence is sanitized and does not persist raw prompts, raw model responses, raw customer data, secrets, credentials, provider tokens, API keys, raw diffs, or raw patches
- fallback execution remains forbidden
- direct provider SDK code and direct network client code are not added
- no Sparkbot or Arc-Bot-shell files are edited
- no consumer repo mutation, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claim is approved

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G46 tests
- LIMA focused V1-G45 tests
- LIMA focused V1-G44 tests
- LIMA focused V1-G22 final public API freeze tests
- LIMA focused V1-G20 provider/model routing authority tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run real provider credentials, real network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior while preparing this request.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G46 changes:

- remove `lima/harness/v1_live_provider_model_call_execution.py`
- remove `V1LiveProviderModelCallExecutionError` from `lima.harness.__all__`
- remove `execute_v1_live_provider_model_call` from `lima.harness.__all__`
- restore `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json` to the pre-G46 harness export list
- remove the V1-G46 implementation docs/tests/fixtures listed above

Rollback must not require consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G46 files
- any `lima/` runtime file outside the approved V1-G46 runtime files must change
- existing harness exports would be removed or renamed
- V1-G44 authority metadata validation must be weakened
- Sparkbot file edits are required
- Arc-Bot-shell file edits are required
- consumer runtime calls are added
- built-in provider SDK clients are required
- direct network client implementation is required
- ambient secret lookup or credential value access is required
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
- Live provider/model call execution approved: no.
- Live provider/model call execution added: no.
- Provider executor invocation added: no.
- Direct provider SDK added: no.
- Direct network code added: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Network calls performed: no.
- Secret lookup added: no.
- Credential value access added: no.
- Fallback execution added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g46-live-provider-model-call-execution` in LIMA-AI-OS. Implement only the exact bounded execution wrapper slice. Do not edit consumer repositories, add built-in provider SDKs, make ambient credential lookups, add fallback, invoke connectors, add physical-world behavior, or claim product readiness.
