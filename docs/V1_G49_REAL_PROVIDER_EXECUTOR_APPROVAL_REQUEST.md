# V1-G49 Real Provider Executor Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g49-real-provider-executor-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, add provider SDK clients, invoke provider executors, execute live provider/model calls, make network calls, read secrets, access credential values, resolve provider endpoints, execute fallback, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G49 implementation of the LIMA-side real provider executor authority design metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G48, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G49 Objective

Implement the smallest metadata-only real provider executor authority design slice.

The proposed implementation would add LIMA-side docs/tests/fixtures that define and validate sanitized metadata for a future real provider executor authority lane:

- executor authority record shape
- provider scope and model scope references
- credential policy linkage to V1-G48 reference-only hardening
- provider network policy linkage to V1-G48 deny-by-default hardening
- audit and redaction evidence linkage
- stop conditions before any real invocation
- blocked future authorities for SDK clients, endpoint resolution, network egress, secret lookup, credential value access, fallback, connectors, physical-world behavior, and product readiness

The approved future implementation must remain metadata-only. It must not invoke real or fake provider executors, add provider SDK clients, read secrets, access credential values, resolve endpoints, make network calls, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- none

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G49_REAL_PROVIDER_EXECUTOR.md`
- `docs/V1_G49_REAL_PROVIDER_EXECUTOR_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g49_real_provider_executor.json`
- `tests/test_v1_g49_real_provider_executor.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G49 may add only deterministic metadata docs/tests/fixtures for a future real provider executor authority design.

Allowed if approved:

- define real provider executor authority metadata only
- define provider/model scope references only
- link to V1-G48 credential and network hardening metadata by reference only
- define sanitized audit and redaction evidence linkage
- define blocked future authorities for real invocation, SDK clients, secret lookup, credential value access, provider endpoint resolution, network egress, fallback, connectors, physical-world behavior, and product readiness
- add fail-closed tests for metadata that attempts to claim provider invocation, SDK use, secret access, credential values, endpoint resolution, network calls, fallback, connectors, or product readiness
- record rollback metadata for removing only V1-G49 docs/tests/fixtures

## Explicitly Forbidden

V1-G49 must not add:

- `lima/` runtime file changes
- consumer repository edits
- consumer production runtime/source edits
- live provider/model calls
- real provider executor invocation
- fake provider executor invocation
- built-in provider SDK clients
- direct network client implementation
- provider endpoint resolution
- network calls
- ambient environment secret lookup
- secret lookup
- credential value access
- provider token or API key access
- credential storage, rotation, migration, or provisioning
- provider configuration changes
- fallback execution
- provider readiness network checks
- Token Guardian live routing
- connector behavior
- browser or network behavior
- tool execution outside local test execution
- action execution
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
- no consumer repository files are changed
- executor authority metadata remains non-executing
- provider/model scope is reference-only
- V1-G48 credential hardening linkage is reference-only
- V1-G48 network hardening linkage is reference-only and deny-by-default
- provider executors are not invoked
- provider SDK clients are not added
- endpoint resolution and network calls are not accepted or claimed
- credential values, secrets, provider tokens, and API keys are not accepted or persisted
- fallback execution remains blocked
- connector/browser/network/device/robotics/physical-world behavior remains blocked
- product-readiness and production-readiness claims remain blocked

## Required Validation If Approved

Run at minimum:

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

Rollback must remove only the exact approved V1-G49 changes:

- remove the V1-G49 LIMA docs/tests/fixture

Rollback must not require `lima/` runtime file changes, consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G49 files
- `lima/` runtime file changes are required
- consumer repository edits are required
- live provider/model calls are added
- real or fake provider executor invocation is added
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
- Real provider executor authority design approved: no.
- Real provider executor authority design added: no.
- `lima/` runtime files changed by this request: no.
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

If approved, create branch `v1-g49-real-provider-executor` in LIMA-AI-OS. Implement only the exact metadata-only real provider executor authority design slice. Do not add real provider execution, provider SDK clients, secret lookup, credential value access, network calls, fallback, connectors, physical-world behavior, or product readiness claims.
