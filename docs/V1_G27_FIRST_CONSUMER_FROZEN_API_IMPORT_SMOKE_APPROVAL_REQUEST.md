# V1-G27 First Consumer Frozen API Import-Smoke Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g27-first-consumer-frozen-api-import-smoke-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit consumer repositories, edit `lima/` runtime files, import consumer code, call consumer runtimes, wire shells, clean up runtime exports, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G27 implementation of the first consumer frozen API import-smoke slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G26, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G27 Objective

Implement the smallest first consumer frozen API import-smoke slice.

The slice should add test-only consumer repo import-smoke fixtures/tests proving Sparkbot and Arc-Bot-shell can import the frozen G22 LIMA candidate public API surface without calling consumer runtimes, invoking LIMA runtime behavior, wiring shells, calling providers/models, accessing credentials, or claiming product readiness.

Approved import-smoke surface:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.V1ConsumerIntegrationCompatibilityError`

The tests may locate LIMA-AI-OS by an explicit `LIMA_AI_OS_REPO` environment variable or by a local sibling repo path for local operator validation. They must not vendor, copy, or modify LIMA source.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE.md`
- `docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g27_first_consumer_frozen_api_import_smoke.json`
- `tests/test_v1_g27_first_consumer_frozen_api_import_smoke.py`

Sparkbot tests/fixtures:

- `tests/fixtures/sparkbot_lima_v1_g27_frozen_api_import_smoke.json`
- `tests/test_sparkbot_lima_v1_g27_frozen_api_import_smoke.py`

Arc-Bot-shell tests/fixtures:

- `tests/fixtures/arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.json`
- `tests/test_arc_bot_shell_lima_v1_g27_frozen_api_import_smoke.py`

No `lima/` runtime files may be created or edited in V1-G27.

No Sparkbot or Arc-Bot-shell runtime/source files may be created or edited in V1-G27. Consumer repository edits are limited to the exact static tests/fixtures files above.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G27 may add only deterministic local docs/tests/fixtures that describe and validate test-only frozen API import-smoke evidence.

Allowed if approved:

- add one Sparkbot import-smoke fixture
- add one Sparkbot focused import-smoke test
- add one Arc-Bot-shell import-smoke fixture
- add one Arc-Bot-shell focused import-smoke test
- add one LIMA-side intake evidence fixture for the two import-smoke records
- add one LIMA-side focused intake test
- import only the approved frozen G22 LIMA API symbols in consumer tests
- assert imported symbols exist without invoking runtime behavior
- link import-smoke records to V1-G22, V1-G24, V1-G25, and V1-G26 evidence
- enforce no live consumer runtime call confirmation
- enforce no runtime wiring confirmation
- enforce no runtime export cleanup confirmation
- enforce no raw file content, prompt, customer data, credential, provider token, API key, secret, raw diff, raw patch, or full patch content confirmation
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G27 must not add:

- `lima/` runtime file changes
- Sparkbot runtime/source edits
- Arc-Bot-shell runtime/source edits
- consumer application imports of LIMA outside focused tests
- consumer runtime calls
- LIMA runtime behavior invocation
- calls to `validate_v1_consumer_integration_compatibility_freeze`
- consumer integration
- shell runtime wiring
- runtime export cleanup
- live provider/model calls
- model request dispatch
- secret lookup
- credential access
- tool execution
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures files
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- raw diff persistence
- full patch content persistence
- raw file content persistence
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA fixture records `CANDIDATE_ONLY`
- Sparkbot import-smoke record exists and remains test-only
- Arc-Bot-shell import-smoke record exists and remains test-only
- each consumer smoke test imports only the approved frozen G22 LIMA API symbols
- no approved frozen API symbol is called by the consumer smoke tests
- consumer repository edits are limited to approved tests/fixtures
- no `lima/` runtime files are required
- no Sparkbot or Arc-Bot-shell runtime/source files are required
- no consumer runtime calls are added
- no runtime export cleanup is approved
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no raw content/secret/credential/customer-data/raw-diff/raw-patch persistence is added
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G27 tests
- LIMA focused V1-G26 tests
- LIMA focused V1-G22 tests
- LIMA focused adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- Sparkbot focused V1-G27 import-smoke test
- Arc-Bot-shell focused V1-G27 import-smoke test
- `git diff --check` in each edited repo
- `git diff --cached --check` in each edited repo before each commit
- `git status --short --branch` in each edited repo

Do not require or run live provider/model calls, live consumer runtime calls, connector calls, browser/network calls, migrations, services, workers, or production deploys.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G27 files:

- LIMA-AI-OS V1-G27 implementation docs/tests/fixtures listed above
- Sparkbot V1-G27 import-smoke tests/fixtures listed above
- Arc-Bot-shell V1-G27 import-smoke tests/fixtures listed above

Rollback must not require `lima/` runtime file changes, consumer runtime/source changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G27 files
- `lima/` runtime file changes are required
- Sparkbot runtime/source edits are required
- Arc-Bot-shell runtime/source edits are required
- consumer application code imports LIMA outside focused tests
- approved frozen API symbols are invoked instead of import-smoked
- consumer runtime calls are added
- LIMA runtime behavior is invoked
- consumer integration is added
- shell runtime wiring is added
- runtime export cleanup is required
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- import-smoke metadata can grant edit, import, execution, or integration authority
- tool execution is added
- action execution is added
- file mutation execution outside the exact approved docs/tests/fixtures files is added
- connector/browser/network/device/robotics/physical-world behavior is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Consumer frozen API import-smoke implementation added: no.
- `lima/` runtime files changed: no.
- Sparkbot runtime/source mutation added: no.
- Arc-Bot-shell runtime/source mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Shell runtime wiring added: no.
- Runtime export cleanup approved: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g27-first-consumer-frozen-api-import-smoke` in LIMA-AI-OS and matching implementation branches in Sparkbot and Arc-Bot-shell. Implement only the exact test-only import-smoke slice. Do not add runtime calls, shell wiring, export cleanup, provider/model calls, connector behavior, browser/network behavior, physical-world behavior, or product-readiness claims.
