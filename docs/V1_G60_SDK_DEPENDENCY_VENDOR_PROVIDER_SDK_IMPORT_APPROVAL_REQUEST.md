# V1-G60 SDK Dependency Vendor Provider SDK Import Approval Request

Date: 2026-06-20
Branch: `prepare-v1-g60-sdk-dependency-vendor-provider-sdk-import-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, add SDK dependencies, edit dependency manifests, edit lockfiles, import vendor provider SDKs, add built-in provider SDK clients, construct provider clients, implement direct provider SDK code, resolve provider endpoints, add DNS/HTTP/socket/network clients, make network calls, perform direct provider egress, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G60 implementation of the LIMA-side SDK dependency addition and vendor provider SDK import approval slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G59, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G60 Objective

Implement the smallest LIMA-side approval slice that can prove a declared SDK dependency and vendor provider SDK import are authorized without creating a provider client or executing any provider call.

The proposed implementation would add docs/tests/fixtures and, only if explicitly approved, a minimal dependency manifest change to declare a specific provider SDK dependency plus a local importability proof. The implementation must distinguish dependency declaration, dependency installation, manifest edit, lockfile edit, vendor import, provider client construction, credential access, endpoint resolution, network egress, fallback, and runtime invocation as separate authority steps.

The approved future implementation must remain non-executing beyond local test/import validation. It must not add built-in provider SDK clients, construct provider clients, implement direct provider SDK call behavior, perform endpoint resolution, add LIMA-owned DNS/HTTP/socket/network clients, make LIMA-owned network calls, perform direct provider egress, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, integrate consumer production runtime paths, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- none

Dependency manifest files:

- `pyproject.toml`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT.md`
- `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g60_sdk_dependency_vendor_provider_sdk_import.json`
- `tests/test_v1_g60_sdk_dependency_vendor_provider_sdk_import.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any lockfile edit, new runtime file, consumer file, or other file requires a new gate update before implementation unless the exact operator approval explicitly adds that file.

## Allowed Behavior If Approved

V1-G60 may add only LIMA-side SDK dependency addition and vendor provider SDK import approval evidence.

Allowed if approved:

- add a narrowly declared provider SDK dependency to `pyproject.toml`
- add docs/tests/fixtures proving the dependency addition is explicitly approved
- add a local test/importability proof for the approved vendor provider SDK module
- require linkage to V1-G48, V1-G53, V1-G54, V1-G55, V1-G56, V1-G57, V1-G58, and V1-G59 evidence
- require Guardian gate and explicit operator approval linkage before any later SDK client construction or provider call lane
- require sanitized evidence refs only
- require supply-chain review metadata
- require license/security posture metadata
- require dependency name/version constraint metadata
- require vendor import declaration metadata
- require no network at import time
- require no client construction at import time
- require no credential lookup at import time
- require no endpoint resolution at import time
- require no provider/model calls at import time
- require denial-by-default posture for all behavior beyond dependency declaration and importability proof
- require no raw prompts, raw model responses, raw customer data, secrets, credentials, provider tokens, API keys, raw diffs, full patches, or raw file contents in evidence

## Explicitly Forbidden

V1-G60 must not add:

- `lima/` runtime file changes
- public API export changes
- Sparkbot file changes
- Arc-Bot-shell file changes
- consumer production runtime/source edits
- live provider/model calls
- lockfile edits unless a revised approval explicitly includes the lockfile
- built-in provider SDK clients
- provider client construction
- direct provider SDK call implementation by LIMA
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
- credential-value access
- provider token or API key access
- credential storage, rotation, provisioning, or migration
- provider configuration changes
- fallback execution
- Token Guardian live routing
- connector behavior
- browser or network behavior
- tool execution outside local test execution
- action execution outside local tests
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
- final public API freeze claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA evidence fixture records `CANDIDATE_ONLY`
- approved file scope is exact
- no `lima/` runtime files are changed
- no public API exports are changed
- no Sparkbot files are changed
- no Arc-Bot-shell files are changed
- no consumer production runtime/source files are changed
- dependency manifest edit is limited to the approved dependency declaration
- no lockfile is edited unless explicitly approved
- vendor provider SDK import is limited to importability proof
- built-in provider SDK client implementation remains blocked
- provider client construction remains blocked
- Guardian gate and operator approval linkage are required
- supply-chain review metadata is required
- license/security posture metadata is required
- dependency name/version constraint metadata is required
- credential references remain reference-only
- network policy references remain reference-only
- endpoint authority references remain reference-only
- denial-by-default posture is recorded
- direct provider SDK call implementation remains blocked
- LIMA-owned endpoint resolution execution remains blocked
- LIMA-owned DNS, HTTP, socket, network calls, and direct provider egress remain blocked
- secret lookup remains blocked
- credential-value access remains blocked
- provider token/API key access remains blocked
- provider configuration changes remain blocked
- fallback execution remains blocked
- consumer production runtime integration remains blocked
- connector/browser/network/device/robotics/physical-world behavior remains blocked
- raw prompts, raw model responses, raw customer data, secrets, credentials, provider tokens, API keys, raw diffs, full patches, and raw file content are not persisted
- product-readiness and production-readiness claims remain blocked
- final public API freeze remains blocked

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G60 implementation tests
- LIMA focused V1-G59 implementation and audit tests
- LIMA focused V1 runtime readiness rollup through G59 tests
- LIMA focused V1 post-G59 next-lane decision matrix tests
- LIMA focused V1-G58 implementation and audit tests
- LIMA focused V1-G57 implementation and audit tests
- LIMA focused V1-G56 consumer fake-executor provider SDK/network egress smoke tests
- LIMA focused V1-G55 real provider SDK/network egress tests
- LIMA focused V1-G54 fake SDK/fake-egress harness tests
- LIMA focused V1-G53 provider SDK/network/credential authority tests
- LIMA focused V1-G48 provider credential/network hardening tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run real provider credentials, built-in provider SDK clients, provider client construction, provider endpoint resolution, LIMA-owned network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G60 changes:

- remove the approved provider SDK dependency declaration from `pyproject.toml`
- remove `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT.md`
- remove `docs/V1_G60_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_CLOSEOUT.md`
- remove `tests/fixtures/runtime_extraction/v1_g60_sdk_dependency_vendor_provider_sdk_import.json`
- remove `tests/test_v1_g60_sdk_dependency_vendor_provider_sdk_import.py`

Rollback must not require `lima/` runtime file changes, public API repair, Sparkbot changes, Arc-Bot-shell changes, consumer production runtime/source file repair, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G60 files
- `lima/` runtime file changes are required
- public API export changes are required
- Sparkbot or Arc-Bot-shell file changes are required
- consumer production runtime/source files must change
- live provider/model calls are added
- unapproved SDK dependencies are added
- dependency manifest edits exceed the approved dependency declaration
- lockfiles are edited without explicit approval
- vendor provider SDK imports do more than local importability proof
- provider SDK clients are added
- built-in provider SDK clients are added
- provider client construction is added
- direct provider SDK call implementation is added
- provider endpoint resolution execution owned by LIMA is added
- direct network client implementation owned by LIMA is added
- DNS, HTTP, socket, network calls, or direct provider egress owned by LIMA are added
- ambient secret lookup, secret lookup, credential-value access, or provider token/API key access is added
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
- final public API freeze is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- SDK dependency addition and vendor provider SDK import approved: no.
- SDK dependency added: no.
- Dependency manifest edited by this request: no.
- Lockfile edited by this request: no.
- Vendor provider SDK import added: no.
- Built-in provider SDK client implementation approved: no.
- Built-in provider SDK client implementation added: no.
- Provider client construction added: no.
- `lima/` runtime files changed by this request: no.
- LIMA public API changed by this request: no.
- Sparkbot files changed by this request: no.
- Arc-Bot-shell files changed by this request: no.
- Direct provider SDK call implementation added: no.
- Provider endpoint resolution added: no.
- Provider endpoint resolution performed: no.
- Direct network code added: no.
- DNS lookup added: no.
- HTTP client added: no.
- Socket client added: no.
- Network call performed by LIMA: no.
- Direct provider egress performed by LIMA: no.
- Credential-reference metadata only: yes.
- Network-policy metadata only: yes.
- Endpoint-authority metadata only: yes.
- Secret lookup added: no.
- Secret lookup performed: no.
- Credential-value access added: no.
- Credential value accessed: no.
- Provider token or API key access added: no.
- Provider token or API key accessed: no.
- Provider configuration changes added: no.
- Fallback execution added: no.
- Tool execution added: no.
- Consumer production runtime integration added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- Final public API freeze claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g60-sdk-dependency-vendor-provider-sdk-import` in LIMA-AI-OS. Implement only the exact LIMA-side SDK dependency addition and vendor provider SDK import approval slice. Do not add built-in provider SDK clients, construct clients, implement direct provider SDK call behavior, perform LIMA-owned provider endpoint resolution execution, make LIMA-owned network calls, perform LIMA-owned direct provider egress, perform secret lookup, access credential values, access provider token/API key values, change provider configuration, execute fallback, integrate consumer production runtime paths, invoke connectors, perform physical-world behavior, claim product readiness, or claim final public API freeze.
