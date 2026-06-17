# V1-G34 Live Consumer Import/Call Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g34-live-consumer-import-call-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit Sparkbot, edit Arc-Bot-shell, create consumer test files, call consumer runtimes, execute adapter validators, execute fake call envelopes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, persist raw patches in LIMA evidence, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G34 implementation of the live consumer import/call test slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G33, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G34 Objective

Implement the smallest live consumer import/call test slice.

The slice should add deterministic LIMA-side docs/tests/fixtures and exact Sparkbot and Arc-Bot-shell focused test/fixture files that perform local test-only imports and calls of approved candidate LIMA adapter validator functions with sanitized metadata. It must not call providers/models, access credentials, invoke connectors, use browser/network/device/robotics/physical-world behavior, wire shells, import consumer runtime modules, mutate runtime/source files, or claim product readiness.

The only candidate LIMA adapter symbols proposed for test-only calls are:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run`

If approved, those symbols may be called only from the exact approved focused consumer tests using static sanitized metadata fixtures. No other LIMA runtime behavior is approved.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL.md`
- `docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g34_live_consumer_import_call.json`
- `tests/test_v1_g34_live_consumer_import_call.py`

Sparkbot tests/fixtures:

- `tests/fixtures/sparkbot_lima_v1_g34_live_consumer_import_call.json`
- `tests/test_sparkbot_lima_v1_g34_live_consumer_import_call.py`

Arc-Bot-shell tests/fixtures:

- `tests/fixtures/arc_bot_shell_lima_v1_g34_live_consumer_import_call.json`
- `tests/test_arc_bot_shell_lima_v1_g34_live_consumer_import_call.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G34.

No Sparkbot or Arc-Bot-shell runtime/source files may be created, edited, removed, imported, or renamed in V1-G34. Consumer changes, if approved, are limited to the exact test/fixture files above.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G34 may add only deterministic docs/tests/fixtures and exact focused consumer tests that prove local test-only import/call compatibility with the approved candidate adapter validators.

Allowed if approved:

- add one LIMA-side live consumer import/call fixture for Sparkbot and Arc-Bot-shell
- add one focused LIMA-side live consumer import/call evidence test
- add one focused Sparkbot test and fixture that call only the approved LIMA adapter validators with sanitized metadata
- add one focused Arc-Bot-shell test and fixture that call only the approved LIMA adapter validators with sanitized metadata
- reference V1-G27 import-smoke, V1-G28 export cleanup, V1-G29 planning, V1-G30 fake-runtime evidence, V1-G31 preview evidence, V1-G32 consumer test edit evidence, and V1-G33 smoke evidence
- enforce no runtime/source file change confirmation
- enforce no consumer runtime module import confirmation
- enforce no shell wiring confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce no raw diff, patch, prompt, credential, customer-data, or raw file content persistence in LIMA evidence
- enforce proof-not-product-readiness confirmation

## Explicitly Forbidden

V1-G34 must not add:

- `lima/` runtime file changes
- Sparkbot runtime/source file edits
- Arc-Bot-shell runtime/source file edits
- consumer files outside the exact approved test/fixture files
- consumer runtime module imports
- shell runtime wiring
- live provider/model calls
- model request dispatch
- fallback execution
- secret lookup
- credential access
- connector behavior
- browser or network behavior
- device, robot, drone, IoT, humanoid, or physical-world behavior
- fake call envelope execution
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures files
- HumanInput bridge activation
- scheduled task execution
- external sends
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- raw diff or full patch content persistence in LIMA evidence
- raw prompts, customer data, credentials, provider tokens, API keys, or secrets in LIMA evidence
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA live consumer import/call fixture records `CANDIDATE_ONLY`
- implementation files are limited to approved LIMA docs/tests/fixtures
- consumer files are limited to approved Sparkbot and Arc-Bot-shell test/fixture files
- no `lima/` runtime files are changed
- no Sparkbot or Arc-Bot-shell runtime/source files are changed
- Sparkbot focused consumer test calls only the approved candidate adapter validators
- Arc-Bot-shell focused consumer test calls only the approved candidate adapter validators
- calls use sanitized metadata fixtures only
- no consumer runtime modules are imported
- no fake call envelopes are executed
- V1-G27, V1-G28, V1-G29, V1-G30, V1-G31, V1-G32, and V1-G33 evidence is linked
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no secret/credential/customer-data/raw-diff/raw-patch persistence is added to LIMA evidence
- proof-not-product-readiness confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G34 tests
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
- Sparkbot focused V1-G34 live consumer import/call test
- Sparkbot focused V1-G32 consumer test
- Sparkbot focused V1-G27 import-smoke test
- Arc-Bot-shell focused V1-G34 live consumer import/call test
- Arc-Bot-shell focused V1-G32 consumer test
- Arc-Bot-shell focused V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

Do not require or run live provider/model calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G34 docs/tests/fixtures:

LIMA-AI-OS:

- `docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL.md`
- `docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g34_live_consumer_import_call.json`
- `tests/test_v1_g34_live_consumer_import_call.py`

Sparkbot:

- `tests/fixtures/sparkbot_lima_v1_g34_live_consumer_import_call.json`
- `tests/test_sparkbot_lima_v1_g34_live_consumer_import_call.py`

Arc-Bot-shell:

- `tests/fixtures/arc_bot_shell_lima_v1_g34_live_consumer_import_call.json`
- `tests/test_arc_bot_shell_lima_v1_g34_live_consumer_import_call.py`

Rollback must not require `lima/` runtime file changes, consumer runtime/source file repair, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G34 files
- `lima/` runtime file changes are required
- Sparkbot or Arc-Bot-shell runtime/source file edits are required
- consumer runtime modules are imported
- shell runtime wiring is added
- unapproved adapter symbols are imported or called
- approved adapter validators are called outside the exact focused consumer tests
- fake call envelopes are executed
- provider/model calls are added
- model request dispatch is added
- fallback execution is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit in LIMA evidence
- connector/browser/network/device/robotics/physical-world behavior is added
- action execution is added
- file mutation execution outside the exact approved docs/tests/fixtures files is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Live consumer import/call implementation approved: no.
- Live consumer import/call implementation added: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added by this request: no.
- Consumer test files created by this request: no.
- Consumer runtime/source files changed by this request: no.
- Consumer runtime modules imported: no.
- Shell runtime wiring added: no.
- Planned adapter symbols called: no.
- Fake call envelopes executed: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Raw diff, patch, prompt, customer-data, credential, or raw file content persisted in LIMA evidence: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g34-live-consumer-import-call` in LIMA-AI-OS, Sparkbot, and Arc-Bot-shell. Implement only the exact live consumer import/call test slice. Do not edit runtime files, wire shells, call providers/models, access secrets, invoke connector/browser/network behavior, add physical-world behavior, persist raw sensitive content in LIMA evidence, or claim product readiness.
