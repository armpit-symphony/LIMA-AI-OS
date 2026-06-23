# V1-G61 Runtime Vendor SDK Import Execution Proof Approval Request

Date: 2026-06-20
Observed workspace branch: `docs-v1-post-g60-readiness-and-next-lane-matrix`
Request-stage lane label: `prepare-v1-g61-runtime-vendor-sdk-import-execution-proof-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit public API exports, edit Sparkbot, edit Arc-Bot-shell, edit dependency manifests, edit lockfiles, add runtime vendor SDK imports in `lima/`, add built-in provider SDK clients, construct provider clients, implement direct provider SDK calls, resolve provider endpoints, add DNS/HTTP/socket/network clients, make network calls, perform direct provider egress, read secrets, access credential values, access provider tokens or API keys, change provider configuration, execute fallback, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G61 implementation of the runtime vendor SDK import execution proof slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G60, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G61 Objective

Implement the smallest proof that the approved vendor SDK module declared by V1-G60 can be imported in a controlled local test context.

The future implementation, if approved, may add docs/tests/fixtures that perform an import execution proof for the already approved module name `openai`. The proof must remain test-scoped and must not create a provider client, read configuration, resolve endpoints, access credentials, make network calls, execute fallback, or wire consumer runtime paths.

The implementation must keep dependency declaration, dependency installation, lockfile edit, runtime import execution, SDK client construction, credential access, endpoint resolution, network egress, fallback, and runtime invocation as separate authority steps.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- none

Dependency manifest files:

- none

Lockfiles:

- none

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md`
- `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g61_runtime_vendor_sdk_import_execution_proof.json`
- `tests/test_v1_g61_runtime_vendor_sdk_import_execution_proof.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any lockfile edit, dependency manifest edit, runtime file, consumer file, provider client file, or other file requires a new gate update before implementation unless the exact operator approval explicitly adds that file.

## Allowed Behavior If Approved

V1-G61 may add only LIMA-side runtime vendor SDK import execution proof evidence.

Allowed if approved:

- add docs/tests/fixtures proving runtime import execution proof is explicitly approved
- import the approved vendor provider SDK module only inside the approved local test proof
- require the approved module name to be exactly `openai`
- require the approved dependency declaration to remain `openai>=1.0.0,<3.0.0`
- require no `lima/` runtime import of the vendor SDK
- require no provider client construction at import time
- require no credential lookup at import time
- require no endpoint resolution at import time
- require no network call at import time
- require no provider/model call at import time
- require no lockfile edit
- require no dependency manifest edit
- require Guardian gate and explicit operator approval linkage before any later SDK client construction or provider call lane
- require sanitized evidence refs only
- require denial-by-default posture for all behavior beyond local import proof

## Explicitly Forbidden

V1-G61 must not add:

- `lima/` runtime file changes
- public API export changes
- dependency manifest edits
- lockfile edits
- Sparkbot file changes
- Arc-Bot-shell file changes
- consumer production runtime/source edits
- runtime vendor SDK imports in `lima/`
- live provider/model calls
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
- HumanInput bridge activation
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, background services, subprocesses, or threads
- raw prompt, raw model response, raw customer data, raw secret, raw credential, provider token, API key, raw diff, full patch, or raw file content persistence
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
- no dependency manifest is changed
- no lockfile is changed
- import execution proof is limited to the approved module name
- runtime vendor SDK imports in `lima/` remain blocked
- built-in provider SDK client implementation remains blocked
- provider client construction remains blocked
- endpoint resolution remains blocked
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

- LIMA focused V1-G61 implementation tests
- LIMA focused V1-G61 approval request tests
- LIMA focused V1-G60 implementation and audit tests
- LIMA focused V1 runtime readiness rollup through G60 tests
- LIMA focused V1 post-G60 next-lane decision matrix tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run real provider credentials, built-in provider SDK clients, provider client construction, provider endpoint resolution, LIMA-owned network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G61 changes:

- remove `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF.md`
- remove `docs/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_CLOSEOUT.md`
- remove `tests/fixtures/runtime_extraction/v1_g61_runtime_vendor_sdk_import_execution_proof.json`
- remove `tests/test_v1_g61_runtime_vendor_sdk_import_execution_proof.py`

Rollback must not require `lima/` runtime file changes, public API repair, dependency manifest repair, lockfile repair, Sparkbot changes, Arc-Bot-shell changes, consumer production runtime/source file repair, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G61 files
- `lima/` runtime file changes are required
- public API export changes are required
- dependency manifest or lockfile edits are required
- Sparkbot or Arc-Bot-shell file changes are required
- consumer production runtime/source files must change
- live provider/model calls are added
- runtime vendor SDK imports are added to `lima/`
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
- Runtime vendor SDK import execution proof approved: no.
- Runtime vendor SDK import execution proof added: no.
- Dependency manifest edited by this request: no.
- Lockfile edited by this request: no.
- Vendor provider SDK import added to `lima/`: no.
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

If approved, create branch `v1-g61-runtime-vendor-sdk-import-execution-proof` in LIMA-AI-OS. Implement only the exact LIMA-side runtime vendor SDK import execution proof slice. Do not edit `lima/`, edit lockfiles, construct clients, implement direct provider SDK call behavior, perform LIMA-owned provider endpoint resolution execution, make LIMA-owned network calls, perform LIMA-owned direct provider egress, perform secret lookup, access credential values, access provider token/API key values, change provider configuration, execute fallback, integrate consumer production runtime paths, invoke connectors, perform physical-world behavior, claim product readiness, or claim final public API freeze.
