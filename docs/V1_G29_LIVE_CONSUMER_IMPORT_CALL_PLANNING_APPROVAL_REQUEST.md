# V1-G29 Live Consumer Import/Call Planning Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g29-live-consumer-import-call-planning-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, edit consumer repositories, import consumer code, call consumer runtimes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G29 implementation of the live consumer import/call planning slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G28, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G29 Objective

Implement the smallest live consumer import/call planning slice.

The slice should add deterministic LIMA-side docs/tests/fixtures that plan fake-runtime/no-network consumer import/call boundaries for Sparkbot and Arc-Bot-shell after the V1-G28 adapter export cleanup. It must not add live calls, consumer source edits, shell wiring, provider/model calls, credential access, connector behavior, network behavior, or product-readiness claims.

Planned future call surfaces may reference only these existing candidate LIMA adapter symbols:

- `lima.adapters.validate_v1_consumer_integration_compatibility_freeze`
- `lima.adapters.validate_v1_consumer_integration_proof_to_import_dry_run`

The implementation, if approved, may describe planned future call shapes as metadata. It must not call those symbols from consumer repositories or wire them into Sparkbot or Arc-Bot-shell runtime code.

## Approved Files If Operator Says Yes

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G29_LIVE_CONSUMER_IMPORT_CALL_PLANNING.md`
- `docs/V1_G29_LIVE_CONSUMER_IMPORT_CALL_PLANNING_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g29_live_consumer_import_call_planning.json`
- `tests/test_v1_g29_live_consumer_import_call_planning.py`

No `lima/` runtime files may be created, edited, removed, or renamed in V1-G29.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G29. Consumer repository validation may be referenced as prior evidence, but consumer repo file edits are not approved.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G29 may add only deterministic local docs/tests/fixtures that describe and validate planning metadata.

Allowed if approved:

- add one LIMA-side planning fixture for Sparkbot and Arc-Bot-shell
- add one focused LIMA-side planning test
- document fake-runtime/no-network consumer import/call boundary plans
- reference the approved V1-G28 adapter export surface
- reference V1-G27 consumer import-smoke evidence
- record planned future call shapes as metadata only
- enforce no runtime file change confirmation
- enforce no consumer repo mutation confirmation
- enforce no live consumer runtime call confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G29 must not add:

- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer application imports of LIMA outside existing focused tests
- consumer runtime calls
- LIMA runtime behavior invocation beyond static planning metadata checks
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

- LIMA planning fixture records `CANDIDATE_ONLY`
- implementation files are limited to approved docs/tests/fixtures
- no `lima/` runtime files are changed
- no Sparkbot or Arc-Bot-shell files are changed
- Sparkbot planning record exists and remains metadata-only
- Arc-Bot-shell planning record exists and remains metadata-only
- planned future call surfaces reference only the approved adapter symbols
- planned future call shapes are not executed
- fake-runtime/no-network/no-secret/provider-model-blocked boundaries are recorded
- V1-G27 import-smoke and V1-G28 export cleanup evidence is linked
- no live consumer runtime calls are approved
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no raw content/secret/credential/customer-data/raw-diff/raw-patch persistence is added
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

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

Rollback must remove only the exact approved V1-G29 docs/tests/fixtures:

- `docs/V1_G29_LIVE_CONSUMER_IMPORT_CALL_PLANNING.md`
- `docs/V1_G29_LIVE_CONSUMER_IMPORT_CALL_PLANNING_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g29_live_consumer_import_call_planning.json`
- `tests/test_v1_g29_live_consumer_import_call_planning.py`

Rollback must not require `lima/` runtime file changes, consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G29 files
- `lima/` runtime file changes are required
- Sparkbot file edits are required
- Arc-Bot-shell file edits are required
- consumer runtime calls are added
- LIMA runtime behavior beyond static planning metadata checks is invoked
- planned adapter symbols are called
- consumer integration is added
- shell runtime wiring is added
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- planning metadata can grant edit, import, execution, integration, provider/model, connector/browser/network, or physical-world authority
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
- Live consumer import/call planning approved: no.
- Live consumer import/call planning added: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
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

If approved, create branch `v1-g29-live-consumer-import-call-planning` in LIMA-AI-OS. Implement only the exact planning metadata slice. Do not edit runtime files, edit consumer repositories, add live calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, or claim product readiness.
