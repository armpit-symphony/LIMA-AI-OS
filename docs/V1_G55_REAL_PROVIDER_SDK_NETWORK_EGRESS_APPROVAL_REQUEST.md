# V1-G55 Real Provider SDK Network Egress Approval Request

Date: 2026-06-18
Branch: `prepare-v1-g55-real-provider-sdk-network-egress-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, add real provider SDK clients, add SDK dependencies, implement direct provider SDK code, resolve provider endpoints, add DNS/HTTP/socket/network clients, make network calls, perform direct provider egress, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G55 implementation of the LIMA-side bounded real provider SDK/network egress authority slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G54, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G55 Objective

Implement the smallest LIMA-side bounded real provider SDK/network egress authority slice after V1-G54.

The proposed implementation would add one versioned LIMA harness wrapper plus docs/tests/fixtures. The wrapper would validate V1-G48 credential/network hardening, V1-G50 invocation envelope metadata, V1-G51 caller-injected executor boundary, V1-G53 provider SDK/network/credential authority metadata, and V1-G54 fake SDK/fake-egress harness evidence before calling a caller-injected provider SDK/network executor.

The approved future implementation must not add built-in provider SDK clients, SDK dependencies, direct provider SDK implementation, LIMA-owned endpoint resolution execution, LIMA-owned DNS/HTTP/socket/network clients, ambient secret lookup, secret lookup, credential value access, provider token/API key access, provider configuration changes, fallback execution, consumer production runtime integration, connector/browser/network/file/device/robotics/physical-world behavior, or product-readiness claims.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- `lima/harness/v1_real_provider_sdk_network_egress.py`
- `lima/harness/__init__.py`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS.md`
- `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g55_real_provider_sdk_network_egress.json`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`
- `tests/test_v1_g55_real_provider_sdk_network_egress.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G55 may add only the bounded LIMA-side real provider SDK/network egress authority wrapper and its docs/tests/fixtures.

Allowed if approved:

- add a versioned `lima.harness` wrapper for real provider SDK/network egress authority
- call only a caller-injected provider SDK/network executor supplied by the caller
- require V1-G48 credential/network hardening linkage
- require V1-G50 invocation envelope linkage
- require V1-G51 caller-injected executable wrapper boundary linkage
- require V1-G53 provider SDK/network/credential authority metadata linkage
- require V1-G54 fake SDK/fake-egress harness evidence linkage
- require sanitized input refs, sanitized output refs, audit refs, timeout policy refs, cost policy refs, endpoint policy refs, and denial policy refs
- return sanitized evidence only
- use test-module-local fake injected executors for local tests
- prove no built-in provider SDK clients, SDK dependencies, direct provider SDK implementation, LIMA-owned endpoint resolution, LIMA-owned DNS/HTTP/socket/network clients, LIMA-owned network calls, ambient secret lookup, secret lookup, credential value access, provider token/API key access, provider configuration changes, fallback, connectors, browser/network/device/robotics/physical-world behavior, consumer production runtime integration, or product-readiness claims are added

## Explicitly Forbidden

V1-G55 must not add:

- unapproved file changes outside the scope above
- Sparkbot file changes
- Arc-Bot-shell file changes
- consumer production runtime/source edits
- built-in provider SDK clients
- SDK dependencies
- direct provider SDK implementation
- provider SDK imports for specific vendors
- provider endpoint resolution execution owned by LIMA
- direct network client implementation owned by LIMA
- DNS lookups owned by LIMA
- HTTP clients owned by LIMA
- socket clients owned by LIMA
- network calls performed by LIMA
- direct provider egress performed by LIMA
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
- browser or network behavior outside the approved injected executor boundary
- tool execution outside local test execution
- action execution outside the approved wrapper boundary
- file mutation execution outside exact approved files
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
- approved file scope is exact
- public API export change is limited to the approved wrapper symbol
- no Sparkbot files are changed
- no Arc-Bot-shell files are changed
- no consumer production runtime/source files are changed
- wrapper requires caller-injected provider SDK/network executor
- local tests use fake injected executors only
- wrapper requires V1-G48 credential/network hardening linkage
- wrapper requires V1-G50 invocation envelope linkage
- wrapper requires V1-G51 caller-injected executable wrapper boundary linkage
- wrapper requires V1-G53 provider SDK/network/credential authority linkage
- wrapper requires V1-G54 fake SDK/fake-egress harness evidence linkage
- built-in provider SDK clients remain blocked
- SDK dependencies remain blocked
- direct provider SDK implementation remains blocked
- LIMA-owned endpoint resolution execution remains blocked
- LIMA-owned DNS, HTTP, socket, network calls, and direct provider egress remain blocked
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

- LIMA focused V1-G55 implementation tests
- LIMA focused V1-G54 fake SDK/fake-egress harness tests
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

Do not require or run real provider credentials, built-in provider SDK clients, provider endpoint resolution, LIMA-owned network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G55 changes:

- remove `lima/harness/v1_real_provider_sdk_network_egress.py`
- remove the V1-G55 export additions from `lima/harness/__init__.py`
- remove `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS.md`
- remove `docs/V1_G55_REAL_PROVIDER_SDK_NETWORK_EGRESS_CLOSEOUT.md`
- remove `tests/fixtures/runtime_extraction/v1_g55_real_provider_sdk_network_egress.json`
- restore `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json` to the pre-G55 export state
- remove `tests/test_v1_g55_real_provider_sdk_network_egress.py`

Rollback must not require Sparkbot changes, Arc-Bot-shell changes, consumer production runtime/source file repair, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G55 files
- Sparkbot or Arc-Bot-shell file changes are required
- consumer production runtime/source files must change
- built-in provider SDK clients are added
- SDK dependencies are added
- direct provider SDK implementation is added
- vendor provider SDK imports are added
- provider endpoint resolution execution owned by LIMA is added
- direct network client implementation owned by LIMA is added
- DNS, HTTP, socket, network calls, or direct provider egress owned by LIMA are added
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
- Bounded real provider SDK/network egress authority approved: no.
- Bounded real provider SDK/network egress wrapper added: no.
- `lima/` runtime files changed by this request: no.
- LIMA public API changed by this request: no.
- Sparkbot files changed by this request: no.
- Arc-Bot-shell files changed by this request: no.
- Built-in provider SDK client added: no.
- Real provider SDK client added by LIMA: no.
- SDK dependency added: no.
- Direct provider SDK added: no.
- Provider SDK import added: no.
- Provider endpoint resolution added: no.
- Provider endpoint resolution performed: no.
- Direct network code added: no.
- DNS lookup added: no.
- HTTP client added: no.
- Socket client added: no.
- Network call performed by LIMA: no.
- Direct provider egress performed by LIMA: no.
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

If approved, create branch `v1-g55-real-provider-sdk-network-egress` in LIMA-AI-OS. Implement only the exact LIMA-side bounded real provider SDK/network egress authority slice. Do not add built-in provider SDK clients, SDK dependencies, direct provider SDK implementation, LIMA-owned provider endpoint resolution execution, LIMA-owned network calls, LIMA-owned direct provider egress, secret lookup, credential value access, provider token/API key access, provider configuration changes, fallback, consumer production runtime integration, connectors, physical-world behavior, or product readiness claims.
