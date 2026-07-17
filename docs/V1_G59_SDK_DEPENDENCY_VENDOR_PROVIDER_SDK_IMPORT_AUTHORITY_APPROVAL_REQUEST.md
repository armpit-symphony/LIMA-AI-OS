# V1-G59 SDK Dependency Vendor Provider SDK Import Authority Approval Request

Date: 2026-06-20
Branch: `prepare-v1-g59-sdk-dependency-vendor-provider-sdk-import-authority-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, add SDK dependencies, edit dependency manifests or lockfiles, import vendor provider SDKs, add built-in provider SDK clients, construct provider clients, implement direct provider SDK code, resolve provider endpoints, add DNS/HTTP/socket/network clients, make network calls, perform direct provider egress, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G59 implementation of the LIMA-side SDK dependency and vendor provider SDK import authority metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G58, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G59 Objective

Implement the smallest LIMA-side metadata-only SDK dependency and vendor provider SDK import authority slice after V1-G58.

The proposed implementation would add docs/tests/fixtures defining the authority criteria that must be satisfied before any future SDK dependency addition or vendor provider SDK import can be considered. It is intended to define minimum metadata expectations around Guardian gating, operator approval, dependency declaration, vendor import declaration, supply-chain review, license/security posture, credential-reference policy, network-policy-reference policy, endpoint authority, redaction, denial-by-default posture, audit evidence, rollback, and stop conditions.

The approved future implementation must remain contract metadata only. It must not add SDK dependencies, edit dependency manifests or lockfiles, import vendor provider SDKs, add built-in provider SDK clients, construct provider clients, implement direct provider SDK code, perform endpoint resolution, add LIMA-owned DNS/HTTP/socket/network clients, make LIMA-owned network calls, perform direct provider egress, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, integrate consumer production runtime paths, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- none

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md`
- `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.json`
- `tests/test_v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G59 may add only LIMA-side SDK dependency and vendor provider SDK import authority docs/tests/fixtures.

Allowed if approved:

- record metadata-only SDK dependency and vendor provider SDK import authority criteria
- require linkage to V1-G48, V1-G53, V1-G54, V1-G55, V1-G56, V1-G57, and V1-G58 evidence
- require Guardian gate and explicit operator approval linkage before any later dependency addition or vendor SDK import
- require sanitized evidence refs only
- require SDK dependency declaration metadata
- require vendor provider SDK import declaration metadata
- require supply-chain review metadata
- require license/security posture metadata
- require credential references and network policy references only
- require endpoint authority references only
- require denial-by-default posture for unapproved dependency/import behavior
- require no raw prompts, raw model responses, raw customer data, secrets, credentials, provider tokens, API keys, raw diffs, full patches, or raw file contents in evidence
- prove no SDK dependencies, dependency manifest edits, lockfile edits, vendor SDK imports, built-in provider SDK clients, client construction, direct provider SDK implementation, LIMA-owned endpoint resolution, LIMA-owned DNS/HTTP/socket/network clients, LIMA-owned network calls, LIMA-owned direct provider egress, secret lookup, credential-value access, provider token/API key access, provider configuration changes, fallback, connectors, browser/network/device/robotics/physical-world behavior, consumer production runtime integration, or product-readiness claims are added

## Explicitly Forbidden

V1-G59 must not add:

- `lima/` runtime file changes
- public API export changes
- Sparkbot file changes
- Arc-Bot-shell file changes
- consumer production runtime/source edits
- live provider/model calls
- SDK dependencies
- dependency manifest edits
- lockfile edits
- vendor provider SDK imports
- provider SDK clients
- built-in provider SDK clients
- provider client construction
- direct provider SDK implementation by LIMA
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
- SDK dependency and vendor provider SDK import authority remains metadata-only
- SDK dependency additions remain blocked until later explicit approval
- dependency manifest edits remain blocked
- lockfile edits remain blocked
- vendor provider SDK imports remain blocked
- built-in provider SDK client implementation remains blocked
- provider client construction remains blocked
- Guardian gate and operator approval linkage are required
- SDK dependency declaration metadata is required
- vendor provider SDK import declaration metadata is required
- supply-chain review metadata is required
- license/security posture metadata is required
- credential references remain reference-only
- network policy references remain reference-only
- endpoint authority references remain reference-only
- denial-by-default posture is recorded
- direct provider SDK implementation remains blocked
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

- LIMA focused V1-G59 implementation tests
- LIMA focused V1-G58 implementation tests
- LIMA focused V1-G58 audit tests
- LIMA focused V1 runtime readiness rollup through G58 tests
- LIMA focused V1 post-G58 next-lane decision matrix tests
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

Do not require or run real provider credentials, SDK dependencies, vendor provider SDK imports, built-in provider SDK clients, provider endpoint resolution, LIMA-owned network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G59 changes:

- remove `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY.md`
- remove `docs/V1_G59_SDK_DEPENDENCY_VENDOR_PROVIDER_SDK_IMPORT_AUTHORITY_CLOSEOUT.md`
- remove `tests/fixtures/runtime_extraction/v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.json`
- remove `tests/test_v1_g59_sdk_dependency_vendor_provider_sdk_import_authority.py`

Rollback must not require `lima/` runtime file changes, public API repair, Sparkbot changes, Arc-Bot-shell changes, consumer production runtime/source file repair, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G59 files
- `lima/` runtime file changes are required
- public API export changes are required
- Sparkbot or Arc-Bot-shell file changes are required
- consumer production runtime/source files must change
- live provider/model calls are added
- SDK dependencies are added
- dependency manifests are edited
- lockfiles are edited
- vendor provider SDK imports are added
- provider SDK clients are added
- built-in provider SDK clients are added
- provider client construction is added
- direct provider SDK implementation is added
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
- SDK dependency and vendor provider SDK import authority approved: no.
- SDK dependency and vendor provider SDK import authority evidence added: no.
- SDK dependency addition approved: no.
- SDK dependency added: no.
- Dependency manifest edited: no.
- Lockfile edited: no.
- Vendor provider SDK import approved: no.
- Vendor provider SDK import added: no.
- Built-in provider SDK client implementation approved: no.
- Built-in provider SDK client implementation added: no.
- Provider client construction added: no.
- `lima/` runtime files changed by this request: no.
- LIMA public API changed by this request: no.
- Sparkbot files changed by this request: no.
- Arc-Bot-shell files changed by this request: no.
- Direct provider SDK added: no.
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

If approved, create branch `v1-g59-sdk-dependency-vendor-provider-sdk-import-authority` in LIMA-AI-OS. Implement only the exact LIMA-side metadata-only SDK dependency and vendor provider SDK import authority slice. Do not add SDK dependencies, edit dependency manifests or lockfiles, import vendor SDKs, add provider SDK clients, construct clients, implement direct provider SDK code, perform LIMA-owned provider endpoint resolution execution, make LIMA-owned network calls, perform LIMA-owned direct provider egress, perform secret lookup, access credential values, access provider token/API key values, change provider configuration, execute fallback, integrate consumer production runtime paths, invoke connectors, perform physical-world behavior, claim product readiness, or claim final public API freeze.
