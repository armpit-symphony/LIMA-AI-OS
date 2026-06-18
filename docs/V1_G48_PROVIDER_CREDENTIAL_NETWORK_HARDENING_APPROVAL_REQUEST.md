# V1-G48 Provider Credential Network Hardening Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g48-provider-credential-network-hardening-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, add provider SDK clients, invoke provider executors, execute live provider/model calls, make network calls, read secrets, access credential values, resolve provider endpoints, execute fallback, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G48 implementation of the LIMA-side provider credential/network hardening metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G47, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G48 Objective

Implement the smallest metadata-only provider credential/network hardening slice before any real provider executor, built-in provider SDK client, secret lookup, credential value access, or provider network egress is approved.

The proposed implementation would add LIMA-side docs/tests/fixtures that define and validate sanitized metadata for:

- credential reference policy
- provider egress policy references
- deny-by-default network stance
- redaction and audit evidence linkage
- failure and stop conditions before real provider execution
- blocked future authorities for real credentials, network, SDKs, fallback, connectors, and product readiness

The approved future implementation must remain metadata-only. It must not read secrets, access credential values, resolve endpoints, make network calls, add provider SDK clients, invoke provider executors, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- none

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING.md`
- `docs/V1_G48_PROVIDER_CREDENTIAL_NETWORK_HARDENING_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g48_provider_credential_network_hardening.json`
- `tests/test_v1_g48_provider_credential_network_hardening.py`

Sparkbot:

- none

Arc-Bot-shell:

- none

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G48 may add only deterministic metadata docs/tests/fixtures for provider credential/network hardening.

Allowed if approved:

- define credential reference metadata only
- define provider network policy reference metadata only
- define deny-by-default egress metadata
- define sanitized audit and redaction evidence linkage
- define blocked future authorities for real provider executors, SDK clients, secret lookup, credential value access, provider egress, fallback, connectors, physical-world behavior, and product readiness
- add fail-closed tests for metadata that attempts to claim secret access, credential values, network calls, SDKs, provider execution, fallback, or product readiness
- record rollback metadata for removing only V1-G48 docs/tests/fixtures

## Explicitly Forbidden

V1-G48 must not add:

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
- credential policy remains reference-only
- credential values, secrets, provider tokens, and API keys are not accepted or persisted
- network policy remains reference-only
- network calls and provider endpoint resolution are not accepted or claimed
- provider SDK clients are not added
- provider executors are not invoked
- fallback execution remains blocked
- connector/browser/network/device/robotics/physical-world behavior remains blocked
- product-readiness and production-readiness claims remain blocked

## Required Validation If Approved

Run at minimum:

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

Rollback must remove only the exact approved V1-G48 changes:

- remove the V1-G48 LIMA docs/tests/fixture

Rollback must not require `lima/` runtime file changes, consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G48 files
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
- Provider credential/network hardening approved: no.
- Provider credential/network hardening added: no.
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

If approved, create branch `v1-g48-provider-credential-network-hardening` in LIMA-AI-OS. Implement only the exact metadata-only provider credential/network hardening slice. Do not add real provider executors, provider SDK clients, secret lookup, credential value access, network calls, fallback, connectors, physical-world behavior, or product readiness claims.
