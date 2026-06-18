# V1-G51 Executable Real Provider Executor Invocation Approval Request

Date: 2026-06-18
Branch: `prepare-v1-g51-executable-real-provider-executor-invocation-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, invoke real or fake provider executors, execute live provider/model calls, add provider SDK clients, make network calls, read secrets, access credential values, resolve provider endpoints, execute fallback, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G51 implementation of the LIMA-side executable real provider executor invocation wrapper slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G50, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G51 Objective

Implement the smallest bounded executable real provider executor invocation wrapper slice.

The proposed implementation would add a LIMA harness wrapper that validates V1-G50 invocation envelope metadata, V1-G49 executor authority metadata, V1-G48 credential/network hardening linkages, redaction/audit policy, timeout/cost/failure metadata, and then calls only a caller-injected provider executor.

The proposed implementation would not add built-in provider SDK clients, provider endpoint resolution, direct network client code, ambient secret lookup, credential value access, provider token/API key access, fallback execution, connector/browser/network authority, consumer repository edits, or product-readiness claims.

The approved future implementation must use local tests with injected fake executors only. It must not require real provider credentials, real network access, real provider SDK installation, real endpoint resolution, consumer repository edits, production services, or physical-world behavior.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- `lima/harness/v1_executable_real_provider_executor_invocation.py`
- `lima/harness/__init__.py`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION.md`
- `docs/V1_G51_EXECUTABLE_REAL_PROVIDER_EXECUTOR_INVOCATION_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g51_executable_real_provider_executor_invocation.json`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`
- `tests/test_v1_g51_executable_real_provider_executor_invocation.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G51 may add only a bounded LIMA harness wrapper and tests for caller-injected provider executor invocation.

Allowed if approved:

- validate V1-G50 invocation request envelope metadata
- validate V1-G50 invocation response evidence requirements
- validate V1-G49 executor authority linkage by reference
- validate V1-G48 credential and network hardening linkage by reference
- validate sanitized audit and redaction evidence linkage
- validate timeout, retry, cost, error, and failure-boundary metadata
- call only a caller-injected provider executor
- return sanitized evidence only
- update `lima.harness.__all__` only for the new approved public wrapper symbols
- update the V1-G22 public API freeze fixture only to preserve prior exports and include the new approved harness exports
- add fail-closed tests for raw prompts, raw model responses, raw customer data, secrets, credential values, provider token/API keys, provider SDK claims, endpoint resolution claims, direct network claims, fallback claims, connector claims, physical-world claims, and product-readiness claims
- record rollback metadata for removing only V1-G51 changes

## Explicitly Forbidden

V1-G51 must not add:

- runtime files outside the exact approved `lima/harness` files
- public API export changes outside the exact approved `lima.harness` symbols
- consumer repository edits
- consumer production runtime/source edits
- built-in provider SDK clients
- SDK imports for provider services
- direct network client implementation
- provider endpoint resolution
- DNS, HTTP, socket, or provider readiness network checks
- real provider credentials
- ambient environment secret lookup
- secret lookup
- credential value access
- provider token or API key access
- credential storage, rotation, migration, or provisioning
- provider configuration changes
- fallback execution
- Token Guardian live routing
- connector behavior
- browser or network behavior outside local test execution
- tool execution outside local test execution
- action execution outside the approved wrapper call to a caller-injected test executor
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
- runtime scope is limited to the approved harness files
- public API export changes are limited to approved harness symbols
- prior frozen public API exports remain present
- no consumer repository files are changed
- V1-G50 invocation envelope metadata is required
- V1-G49 executor authority linkage is required
- V1-G48 credential hardening linkage is required and reference-only
- V1-G48 network hardening linkage is required, reference-only, and deny-by-default
- the wrapper calls only a caller-injected provider executor
- local tests use fake injected executors only
- built-in provider SDK clients are not added
- endpoint resolution and direct network calls are not added or claimed
- credential values, secrets, provider tokens, and API keys are not accepted or persisted
- fallback execution remains blocked
- connector/browser/network/device/robotics/physical-world behavior remains blocked
- product-readiness and production-readiness claims remain blocked

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G51 tests
- LIMA focused V1-G50 tests
- LIMA focused V1-G49 tests
- LIMA focused V1-G48 tests
- LIMA focused V1-G47 tests
- LIMA focused V1-G46 tests
- LIMA focused V1-G22 final public API freeze tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run real provider credentials, real network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G51 changes:

- remove `lima/harness/v1_executable_real_provider_executor_invocation.py`
- remove only the V1-G51 exports from `lima/harness/__init__.py`
- remove only the V1-G51 public API fixture additions from `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`
- remove the V1-G51 LIMA docs/tests/fixture

Rollback must not require consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G51 files
- runtime scope exceeds the approved harness files
- public API export scope exceeds the approved harness symbols
- consumer repository edits are required
- live provider credentials are required
- real network calls are required
- built-in provider SDK clients are added
- direct network client implementation is added
- provider endpoint resolution is added
- DNS, HTTP, socket, or provider readiness checks are added
- ambient secret lookup or credential value access is added
- provider token/API key access is added
- raw prompts, raw model responses, raw customer data, credentials, provider tokens, API keys, secrets, raw diffs, or full patches can persist or emit in evidence
- fallback execution is added
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
- Executable real provider executor invocation wrapper approved: no.
- Executable real provider executor invocation wrapper added: no.
- `lima/` runtime files changed by this request: no.
- LIMA public API changed by this request: no.
- Sparkbot files changed by this request: no.
- Arc-Bot-shell files changed by this request: no.
- Provider executor invoked by this request: no.
- Live provider/model calls added: no.
- Credential values allowed: no.
- Secret lookup allowed: no.
- Network calls allowed: no.
- Provider SDK clients allowed: no.
- Fallback execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g51-executable-real-provider-executor-invocation` in LIMA-AI-OS. Implement only the exact bounded caller-injected executable wrapper slice. Do not add provider SDK clients, secret lookup, credential value access, direct network calls, endpoint resolution, fallback, connectors, physical-world behavior, consumer repository edits, or product readiness claims.
