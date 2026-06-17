# V1-G33 Consumer Fake-Runtime Import/Call Smoke Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g33-consumer-fake-runtime-import-call-smoke-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create consumer test files, call consumer runtimes, execute adapter validators, execute fake call envelopes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw patches in LIMA evidence, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G33 implementation of the consumer fake-runtime import/call smoke evidence slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G32, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G33 Objective

Implement the smallest LIMA-side consumer fake-runtime import/call smoke evidence slice.

The slice should add deterministic LIMA-side docs/tests/fixtures that record fake-runtime import/call smoke evidence for Sparkbot and Arc-Bot-shell based on the V1-G32 consumer tests. It must not edit consumer repositories, call consumer runtimes, call adapter symbols, execute fake call envelopes, wire shells, call providers/models, access credentials, invoke connectors, use network/browser/device/robotics/physical-world behavior, or claim product readiness.

The smoke evidence may reference only these existing candidate LIMA adapter symbols:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run`

The implementation, if approved, may record sanitized smoke evidence metadata and validation results. It must not call those symbols or create new consumer files.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE.md`
- `docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g33_consumer_fake_runtime_import_call_smoke.json`
- `tests/test_v1_g33_consumer_fake_runtime_import_call_smoke.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G33.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G33. Existing V1-G32 consumer tests may be run and referenced as validation evidence only.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G33 may add only deterministic LIMA-side docs/tests/fixtures that describe and validate consumer fake-runtime import/call smoke evidence metadata.

Allowed if approved:

- add one LIMA-side consumer fake-runtime import/call smoke fixture for Sparkbot and Arc-Bot-shell
- add one focused LIMA-side smoke evidence test
- document existing V1-G32 consumer test results as evidence
- document fake call shape smoke metadata without executing fake call envelopes
- reference the approved V1-G32 consumer repository test edit records
- reference V1-G27 import-smoke, V1-G28 export cleanup, V1-G29 planning, V1-G30 fake-runtime evidence, and V1-G31 preview evidence
- enforce no runtime file change confirmation
- enforce no consumer repo mutation confirmation
- enforce no consumer test file creation confirmation
- enforce no live consumer runtime call confirmation
- enforce no adapter symbol execution confirmation
- enforce no fake call envelope execution confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce no raw diff, patch, or raw file content persistence in LIMA evidence
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G33 must not add:

- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer test files
- consumer runtime/source file edits
- consumer application imports of LIMA outside existing approved focused tests
- consumer runtime calls
- live consumer imports/calls
- LIMA runtime behavior beyond static smoke evidence metadata checks
- calls to planned LIMA adapter symbols
- fake call envelope execution
- consumer integration
- shell runtime wiring
- live provider/model calls
- model request dispatch
- secret lookup
- credential access
- tool execution outside local test execution
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
- raw diff or full patch content persistence in LIMA evidence
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA consumer fake-runtime import/call smoke fixture records `CANDIDATE_ONLY`
- implementation files are limited to approved LIMA docs/tests/fixtures
- no `lima/` runtime files are changed
- no Sparkbot or Arc-Bot-shell files are changed
- Sparkbot smoke evidence record exists and remains metadata-only
- Arc-Bot-shell smoke evidence record exists and remains metadata-only
- smoke evidence references only approved candidate adapter symbols
- planned adapter symbols are not called
- fake call envelopes are not executed
- existing V1-G32 consumer test results are linked
- V1-G27, V1-G28, V1-G29, V1-G30, V1-G31, and V1-G32 evidence is linked
- no live consumer runtime calls are approved
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no secret/credential/customer-data/raw-diff/raw-patch persistence is added to LIMA evidence
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G33 tests
- LIMA focused V1-G32 tests
- LIMA focused V1-G31 tests
- LIMA focused V1-G30 tests
- LIMA focused V1-G29 tests
- LIMA focused V1-G28 tests
- LIMA focused V1-G27 tests
- LIMA focused adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- Sparkbot focused V1-G32 consumer test
- Sparkbot focused V1-G27 import-smoke test
- Arc-Bot-shell focused V1-G32 consumer test
- Arc-Bot-shell focused V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

Do not require or run live provider/model calls, live consumer runtime calls, connector calls, browser/network calls, migrations, services, workers, or production deploys.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G33 docs/tests/fixtures:

- `docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE.md`
- `docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g33_consumer_fake_runtime_import_call_smoke.json`
- `tests/test_v1_g33_consumer_fake_runtime_import_call_smoke.py`

Rollback must not require `lima/` runtime file changes, consumer repository changes, consumer runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G33 files
- `lima/` runtime file changes are required
- Sparkbot or Arc-Bot-shell file edits are required
- consumer runtime/source file edits are required
- consumer runtime calls are added
- live consumer imports/calls are added
- LIMA runtime behavior beyond static smoke evidence metadata checks is invoked
- planned adapter symbols are called
- fake call envelopes are executed
- consumer integration is added
- shell runtime wiring is added
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit in LIMA evidence
- smoke evidence can grant import, execution, integration, provider/model, connector/browser/network, or physical-world authority
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
- Consumer fake-runtime import/call smoke evidence approved: no.
- Consumer fake-runtime import/call smoke evidence added: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added by this request: no.
- Consumer test files created by this request: no.
- Consumer runtime/source files changed by this request: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Live consumer imports/calls added: no.
- Planned adapter symbols called: no.
- Fake call envelopes executed: no.
- Shell runtime wiring added: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Raw diff, patch, or raw file content persisted in LIMA evidence: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g33-consumer-fake-runtime-import-call-smoke` in LIMA-AI-OS. Implement only the exact consumer fake-runtime import/call smoke evidence slice. Do not edit runtime files, edit consumer repos, add live calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, persist raw patch content in LIMA evidence, or claim product readiness.
