# V1-G32 Consumer Repository Test Edit Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g32-consumer-repository-test-edit-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create consumer test files, call consumer runtimes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw patches in LIMA evidence, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G32 implementation of the consumer repository test edit slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G31, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G32 Objective

Implement the smallest consumer repository test edit slice.

The slice should add the exact Sparkbot and Arc-Bot-shell test/fixture files previewed by V1-G31, plus deterministic LIMA-side docs/tests/fixtures that intake those edits as evidence. It must not edit consumer runtime/source files outside the approved test/fixture paths, call consumer runtimes, execute adapter validators, wire shells, call providers/models, access credentials, invoke connectors, use network/browser/device/robotics/physical-world behavior, or claim product readiness.

The approved consumer tests, if implemented, may import only these existing candidate LIMA adapter symbols as test-only references and must not call them:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run`

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G32_CONSUMER_REPOSITORY_TEST_EDIT.md`
- `docs/V1_G32_CONSUMER_REPOSITORY_TEST_EDIT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g32_consumer_repository_test_edit.json`
- `tests/test_v1_g32_consumer_repository_test_edit.py`

Sparkbot test/fixture files:

- `tests/fixtures/sparkbot_lima_v1_g31_fake_runtime_consumer_call_preview.json`
- `tests/test_sparkbot_lima_v1_g31_fake_runtime_consumer_call_preview.py`

Arc-Bot-shell test/fixture files:

- `tests/fixtures/arc_bot_shell_lima_v1_g31_fake_runtime_consumer_call_preview.json`
- `tests/test_arc_bot_shell_lima_v1_g31_fake_runtime_consumer_call_preview.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G32.

No Sparkbot or Arc-Bot-shell files outside the exact approved test/fixture files may be created, edited, removed, or renamed in V1-G32.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G32 may add only deterministic docs/tests/fixtures and the exact consumer test/fixture files listed above.

Allowed if approved:

- add one Sparkbot fake-runtime consumer call preview fixture
- add one Sparkbot fake-runtime consumer call preview test
- add one Arc-Bot-shell fake-runtime consumer call preview fixture
- add one Arc-Bot-shell fake-runtime consumer call preview test
- add one LIMA-side consumer repository test edit evidence fixture
- add one focused LIMA-side evidence test
- document the consumer repo test edits as evidence
- reference V1-G31 preview records
- reference V1-G27 import-smoke, V1-G28 export cleanup, V1-G29 planning, and V1-G30 fake-runtime evidence
- enforce no runtime/source file change confirmation
- enforce no consumer runtime call confirmation
- enforce no adapter symbol execution confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce no raw patch persistence in LIMA evidence
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G32 must not add:

- `lima/` runtime file changes
- Sparkbot files outside the exact approved test/fixture files
- Arc-Bot-shell files outside the exact approved test/fixture files
- Sparkbot runtime/source file edits
- Arc-Bot-shell runtime/source file edits
- consumer application imports of LIMA outside the exact approved focused tests
- consumer runtime calls
- live consumer imports/calls
- LIMA runtime behavior beyond static evidence metadata checks and test-only import checks
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

- LIMA consumer repository test edit fixture records `CANDIDATE_ONLY`
- implementation files are limited to approved LIMA docs/tests/fixtures and approved consumer test/fixture files
- no `lima/` runtime files are changed
- no Sparkbot files outside approved tests/fixtures are changed
- no Arc-Bot-shell files outside approved tests/fixtures are changed
- no consumer runtime/source files are changed
- Sparkbot consumer test edit record exists
- Arc-Bot-shell consumer test edit record exists
- consumer tests import only approved candidate adapter symbols and do not call them
- fake call envelopes are not executed
- V1-G27, V1-G28, V1-G29, V1-G30, and V1-G31 evidence is linked
- no live consumer runtime calls are approved
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no secret/credential/customer-data/raw-diff/raw-patch persistence is added to LIMA evidence
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

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

Rollback must remove only the exact approved V1-G32 files:

LIMA-AI-OS:

- `docs/V1_G32_CONSUMER_REPOSITORY_TEST_EDIT.md`
- `docs/V1_G32_CONSUMER_REPOSITORY_TEST_EDIT_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g32_consumer_repository_test_edit.json`
- `tests/test_v1_g32_consumer_repository_test_edit.py`

Sparkbot:

- `tests/fixtures/sparkbot_lima_v1_g31_fake_runtime_consumer_call_preview.json`
- `tests/test_sparkbot_lima_v1_g31_fake_runtime_consumer_call_preview.py`

Arc-Bot-shell:

- `tests/fixtures/arc_bot_shell_lima_v1_g31_fake_runtime_consumer_call_preview.json`
- `tests/test_arc_bot_shell_lima_v1_g31_fake_runtime_consumer_call_preview.py`

Rollback must not require `lima/` runtime file changes, consumer runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G32 files
- `lima/` runtime file changes are required
- Sparkbot runtime/source file edits are required
- Arc-Bot-shell runtime/source file edits are required
- consumer files outside the exact approved tests/fixtures are required
- consumer runtime calls are added
- live consumer imports/calls are added
- LIMA runtime behavior beyond static evidence metadata checks and test-only import checks is invoked
- planned adapter symbols are called
- fake call envelopes are executed
- consumer integration is added
- shell runtime wiring is added
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit in LIMA evidence
- test edit evidence can grant import, execution, integration, provider/model, connector/browser/network, or physical-world authority
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
- Consumer repository test edit approved: no.
- Consumer repository test edit added: no.
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

If approved, create branch `v1-g32-consumer-repository-test-edit` in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell as needed. Implement only the exact consumer repository test edit slice. Do not edit runtime files, add live calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, persist raw patch content in LIMA evidence, or claim product readiness.
