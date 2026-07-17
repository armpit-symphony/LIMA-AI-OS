# V1-G54 Fake SDK Egress Harness Approval Request

Date: 2026-06-18
Branch: `prepare-v1-g54-fake-sdk-egress-harness-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, create fake SDK harnesses, create fake egress harnesses, add real provider SDK clients, add SDK dependencies, resolve provider endpoints, make network calls, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G54 implementation of the LIMA-side fake SDK/fake-egress harness evidence slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G53, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G54 Objective

Implement the smallest LIMA-side fake SDK/fake-egress harness evidence slice after V1-G53.

The proposed implementation would add docs/tests/fixtures that prove SDK-shaped and egress-shaped provider boundaries can be represented with deterministic in-process fake components while remaining no-secret, no-network, no-real-endpoint, no-token, no-credential-value, and fail-closed.

The approved future implementation must not add real provider SDK clients, SDK dependencies, direct provider SDK implementation, real endpoint resolution execution, network calls, direct provider egress, secret lookup, credential value access, provider token/API key access, provider configuration changes, fallback execution, consumer runtime integration, connector/browser/network/file/device/robotics/physical-world behavior, or product-readiness claims.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- none

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G54_FAKE_SDK_EGRESS_HARNESS.md`
- `docs/V1_G54_FAKE_SDK_EGRESS_HARNESS_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g54_fake_sdk_egress_harness.json`
- `tests/test_v1_g54_fake_sdk_egress_harness.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G54 may add only LIMA-side fake SDK/fake-egress harness evidence docs/tests/fixtures.

Allowed if approved:

- define deterministic fake SDK harness evidence in LIMA docs/tests/fixtures
- define deterministic fake egress harness evidence in LIMA docs/tests/fixtures
- use test-module-local fake in-process components only
- model fake SDK-shaped request and response records without real SDK dependencies
- model fake egress-shaped allow/deny records without DNS, HTTP, socket, or network calls
- prove no real provider credentials, secret lookup, credential value access, provider token/API key access, real provider SDK clients, endpoint resolution execution, network calls, direct provider egress, fallback, connectors, browser/network/device/robotics/physical-world behavior, consumer production runtime integration, or product-readiness claims are added
- link fake harness records to V1-G53 authority metadata
- link fake harness records to V1-G48 credential/network hardening metadata
- link fake harness records to V1-G50 invocation envelope metadata
- link fake harness records to V1-G51 executable wrapper boundary
- link fake harness records to V1-G52 consumer fake-executor proof

## Explicitly Forbidden

V1-G54 must not add:

- `lima/` runtime file changes
- public API export changes
- Sparkbot file changes
- Arc-Bot-shell file changes
- consumer production runtime/source edits
- live provider/model calls
- real provider SDK clients
- SDK dependencies
- direct provider SDK implementation
- provider endpoint resolution execution
- direct network client implementation
- DNS lookups
- HTTP clients
- socket clients
- network calls
- direct provider egress
- provider readiness network checks
- ambient environment secret lookup
- secret lookup
- credential value access
- provider token or API key access
- credential storage, rotation, provisioning, or migration
- provider configuration changes
- fallback execution
- Token Guardian live routing
- connector behavior
- browser or network behavior
- tool execution outside local test execution
- action execution outside local fake-harness tests
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
- no public API exports are changed
- no Sparkbot files are changed
- no Arc-Bot-shell files are changed
- fake SDK/fake-egress harness evidence is created only as docs/tests/fixtures
- any fake SDK or fake egress components are local to the approved test module
- real provider SDK clients remain blocked
- SDK dependencies remain blocked
- direct provider SDK implementation remains blocked
- endpoint resolution execution remains blocked
- DNS, HTTP, socket, network calls, and direct provider egress remain blocked
- secret lookup remains blocked
- credential value access remains blocked
- provider token/API key access remains blocked
- provider configuration changes remain blocked
- fallback execution remains blocked
- consumer production runtime integration remains blocked
- connector/browser/network/device/robotics/physical-world behavior remains blocked
- raw prompts, raw model responses, raw customer data, secrets, credentials, provider tokens, API keys, raw diffs, full patches, and raw file content are not persisted
- product-readiness and production-readiness claims remain blocked

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G54 implementation tests
- LIMA focused V1-G53 provider SDK/network/credential authority tests
- LIMA focused V1-G52 consumer fake-executor provider invocation smoke tests
- LIMA focused V1-G51 executable real provider executor invocation tests
- LIMA focused V1-G50 real provider executor invocation tests
- LIMA focused V1-G48 provider credential/network hardening tests
- LIMA focused V1-G22 final public API freeze tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run real provider credentials, real provider SDK clients, provider endpoint resolution, network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G54 changes:

- remove `docs/V1_G54_FAKE_SDK_EGRESS_HARNESS.md`
- remove `docs/V1_G54_FAKE_SDK_EGRESS_HARNESS_CLOSEOUT.md`
- remove `tests/fixtures/runtime_extraction/v1_g54_fake_sdk_egress_harness.json`
- remove `tests/test_v1_g54_fake_sdk_egress_harness.py`

Rollback must not require `lima/` runtime file repair, public API export repair, Sparkbot changes, Arc-Bot-shell changes, consumer production runtime/source file repair, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G54 files
- `lima/` runtime file changes are required
- public API export changes are required
- Sparkbot or Arc-Bot-shell file changes are required
- consumer production runtime/source files must change
- real provider SDK clients are added
- SDK dependencies are added
- direct provider SDK implementation is added
- provider endpoint resolution execution is added
- direct network client implementation is added
- DNS, HTTP, socket, network calls, or direct provider egress are added
- ambient secret lookup, secret lookup, credential value access, or provider token/API key access is added
- provider configuration changes are required
- credential storage, rotation, provisioning, or migration is added
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
- Fake SDK/fake-egress harness evidence approved: no.
- Fake SDK/fake-egress harness evidence added: no.
- `lima/` runtime files changed by this request: no.
- LIMA public API changed by this request: no.
- Sparkbot files changed by this request: no.
- Arc-Bot-shell files changed by this request: no.
- Real provider SDK client added: no.
- SDK dependency added: no.
- Direct provider SDK added: no.
- Fake SDK harness added by this request: no.
- Fake egress harness added by this request: no.
- Provider endpoint resolution added: no.
- Provider endpoint resolution performed: no.
- Direct network code added: no.
- Network call performed: no.
- Direct provider egress added: no.
- Credential-reference metadata only: yes.
- Secret lookup added: no.
- Secret lookup performed: no.
- Credential value access added: no.
- Credential value accessed: no.
- Provider token or API key access added: no.
- Provider token or API key accessed: no.
- Provider configuration changes added: no.
- Fallback execution added: no.
- Tool execution added: no.
- Consumer production runtime integration added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g54-fake-sdk-egress-harness` in LIMA-AI-OS. Implement only the exact LIMA-side fake SDK/fake-egress harness evidence slice. Do not add real provider SDK clients, SDK dependencies, direct provider SDK implementation, provider endpoint resolution execution, network calls, direct provider egress, secret lookup, credential value access, provider token/API key access, provider configuration changes, fallback, consumer production runtime integration, connectors, physical-world behavior, or product readiness claims.
