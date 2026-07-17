# V1-G31 Fake-Runtime Consumer Repository Test Preview Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g31-fake-runtime-consumer-repo-test-preview-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit consumer repositories, create consumer test files, call consumer runtimes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw patch or file content, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G31 implementation of the fake-runtime consumer repository test preview slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G30, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G31 Objective

Implement the smallest LIMA-side fake-runtime consumer repository test preview slice.

The slice should add deterministic LIMA-side docs/tests/fixtures that preview future Sparkbot and Arc-Bot-shell test file paths and expected assertion categories for fake-runtime consumer call evidence. It must not edit Sparkbot, edit Arc-Bot-shell, create consumer test files, persist raw test file contents, persist raw patches, execute adapter validators, call consumer runtimes, wire shells, call providers/models, access credentials, invoke connectors, use network/browser/device/robotics/physical-world behavior, or claim product readiness.

The preview may reference only the V1-G30 fake-runtime evidence records and these existing candidate LIMA adapter symbols:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run`

The implementation, if approved, may record sanitized future consumer test metadata. It must not create or modify those consumer files.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW.md`
- `docs/V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g31_fake_runtime_consumer_repo_test_preview.json`
- `tests/test_v1_g31_fake_runtime_consumer_repo_test_preview.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G31.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G31. Future consumer test file paths may be previewed as metadata only, but consumer repo file edits are not approved.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G31 may add only deterministic local docs/tests/fixtures that describe and validate fake-runtime consumer repository test preview metadata.

Allowed if approved:

- add one LIMA-side fake-runtime consumer repo test preview fixture for Sparkbot and Arc-Bot-shell
- add one focused LIMA-side fake-runtime consumer repo test preview test
- document future consumer test file paths as metadata only
- document expected future assertion categories without raw test content
- reference the approved V1-G30 fake-runtime evidence records
- reference V1-G27 import-smoke, V1-G28 export cleanup, and V1-G29 planning evidence
- enforce no runtime file change confirmation
- enforce no consumer repo mutation confirmation
- enforce no consumer test file creation confirmation
- enforce no live consumer runtime call confirmation
- enforce no adapter symbol execution confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce no raw diff, patch, or raw file content persistence
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G31 must not add:

- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer test files
- raw consumer test file contents
- raw diffs, patches, or full patch bodies
- consumer application imports of LIMA outside existing focused tests
- consumer runtime calls
- live consumer imports/calls
- LIMA runtime behavior beyond static preview metadata checks
- calls to planned LIMA adapter symbols
- fake call envelope execution
- consumer integration
- shell runtime wiring
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
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA fake-runtime consumer repo test preview fixture records `CANDIDATE_ONLY`
- implementation files are limited to approved docs/tests/fixtures
- no `lima/` runtime files are changed
- no Sparkbot or Arc-Bot-shell files are changed
- no consumer test files are created
- Sparkbot preview record exists and remains metadata-only
- Arc-Bot-shell preview record exists and remains metadata-only
- previewed consumer test paths are metadata only and not approved edits
- fake call surfaces reference only the approved adapter symbols
- fake call envelopes are not executed
- no adapter symbol is called
- V1-G27, V1-G28, V1-G29, and V1-G30 evidence is linked
- no live consumer runtime calls are approved
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no raw content/secret/credential/customer-data/raw-diff/raw-patch/raw-test-content persistence is added
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G31 tests
- LIMA focused V1-G30 tests
- LIMA focused V1-G29 tests
- LIMA focused V1-G28 tests
- LIMA focused V1-G27 tests
- LIMA focused adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- Sparkbot focused V1-G27 import-smoke test
- Arc-Bot-shell focused V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

Do not require or run live provider/model calls, live consumer runtime calls, connector calls, browser/network calls, migrations, services, workers, or production deploys.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G31 docs/tests/fixtures:

- `docs/V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW.md`
- `docs/V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g31_fake_runtime_consumer_repo_test_preview.json`
- `tests/test_v1_g31_fake_runtime_consumer_repo_test_preview.py`

Rollback must not require `lima/` runtime file changes, consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G31 files
- `lima/` runtime file changes are required
- Sparkbot file edits are required
- Arc-Bot-shell file edits are required
- consumer test files are created
- raw consumer test file contents are persisted
- raw diffs or full patch contents are persisted
- consumer runtime calls are added
- live consumer imports/calls are added
- LIMA runtime behavior beyond static preview metadata checks is invoked
- planned adapter symbols are called
- fake call envelopes are executed
- consumer integration is added
- shell runtime wiring is added
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- preview metadata can grant edit, import, execution, integration, provider/model, connector/browser/network, or physical-world authority
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
- Fake-runtime consumer repository test preview approved: no.
- Fake-runtime consumer repository test preview added: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added: no.
- Consumer test files created: no.
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
- Raw diff, patch, or raw file content persisted: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g31-fake-runtime-consumer-repo-test-preview` in LIMA-AI-OS. Implement only the fake-runtime consumer repository test preview metadata slice. Do not edit runtime files, edit consumer repos, create consumer tests, add live calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, persist raw patch/file content, or claim product readiness.
