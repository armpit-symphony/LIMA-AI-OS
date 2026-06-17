# V1-G30 Fake-Runtime Consumer Call Evidence Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g30-fake-runtime-consumer-call-evidence-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit consumer repositories, call consumer runtimes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G30 implementation of the fake-runtime consumer call evidence slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G29, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G30 Objective

Implement the smallest fake-runtime consumer call evidence slice.

The slice should add deterministic LIMA-side docs/tests/fixtures that record fake-runtime consumer call evidence for Sparkbot and Arc-Bot-shell based on the V1-G29 planning metadata. It must not execute adapter validators, call consumer runtimes, edit consumer repositories, wire shells, call providers/models, access credentials, invoke connectors, use network/browser/device/robotics/physical-world behavior, or claim product readiness.

Fake-runtime evidence may reference only these existing candidate LIMA adapter symbols:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run`

The implementation, if approved, may record deterministic fake call envelopes as metadata. It must not call those symbols from LIMA runtime code, Sparkbot, or Arc-Bot-shell.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE.md`
- `docs/V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g30_fake_runtime_consumer_call_evidence.json`
- `tests/test_v1_g30_fake_runtime_consumer_call_evidence.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G30.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G30. Consumer repository validation may be referenced as prior evidence, but consumer repo file edits are not approved.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G30 may add only deterministic local docs/tests/fixtures that describe and validate fake-runtime evidence metadata.

Allowed if approved:

- add one LIMA-side fake-runtime evidence fixture for Sparkbot and Arc-Bot-shell
- add one focused LIMA-side fake-runtime evidence test
- document deterministic fake call envelopes as metadata
- reference the approved V1-G29 planning records
- reference V1-G27 import-smoke and V1-G28 export cleanup evidence
- enforce no runtime file change confirmation
- enforce no consumer repo mutation confirmation
- enforce no live consumer runtime call confirmation
- enforce no adapter symbol execution confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G30 must not add:

- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer application imports of LIMA outside existing focused tests
- consumer runtime calls
- live consumer imports/calls
- LIMA runtime behavior invocation beyond static fake-runtime evidence metadata checks
- calls to planned LIMA adapter symbols
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
- raw diff persistence
- full patch content persistence
- raw file content persistence
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include and run tests proving:

- LIMA fake-runtime evidence fixture records `CANDIDATE_ONLY`
- implementation files are limited to approved docs/tests/fixtures
- no `lima/` runtime files are changed
- no Sparkbot or Arc-Bot-shell files are changed
- Sparkbot fake-runtime evidence record exists and remains metadata-only
- Arc-Bot-shell fake-runtime evidence record exists and remains metadata-only
- fake call surfaces reference only the approved adapter symbols
- fake call envelopes are not executed
- no adapter symbol is called
- fake-runtime/no-network/no-secret/provider-model-blocked boundaries are recorded
- V1-G27, V1-G28, and V1-G29 evidence is linked
- no live consumer runtime calls are approved
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no raw content/secret/credential/customer-data/raw-diff/raw-patch persistence is added
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

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

Rollback must remove only the exact approved V1-G30 docs/tests/fixtures:

- `docs/V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE.md`
- `docs/V1_G30_FAKE_RUNTIME_CONSUMER_CALL_EVIDENCE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g30_fake_runtime_consumer_call_evidence.json`
- `tests/test_v1_g30_fake_runtime_consumer_call_evidence.py`

Rollback must not require `lima/` runtime file changes, consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G30 files
- `lima/` runtime file changes are required
- Sparkbot file edits are required
- Arc-Bot-shell file edits are required
- consumer runtime calls are added
- live consumer imports/calls are added
- LIMA runtime behavior beyond static fake-runtime evidence metadata checks is invoked
- planned adapter symbols are called
- consumer integration is added
- shell runtime wiring is added
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- fake-runtime evidence metadata can grant edit, import, execution, integration, provider/model, connector/browser/network, or physical-world authority
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
- Fake-runtime consumer call evidence approved: no.
- Fake-runtime consumer call evidence added: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Live consumer imports/calls added: no.
- Planned adapter symbols called: no.
- Shell runtime wiring added: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g30-fake-runtime-consumer-call-evidence` in LIMA-AI-OS. Implement only the exact fake-runtime evidence metadata slice. Do not edit runtime files, edit consumer repositories, add live calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, or claim product readiness.
