# V1-G28 Runtime Export Cleanup Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g28-runtime-export-cleanup-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, change public exports, edit consumer repositories, call consumer runtimes, wire shells, call providers/models, read secrets, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G28 implementation of the runtime export cleanup slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G27, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G28 Objective

Implement the smallest runtime export cleanup slice.

The slice should promote the existing V1-G23 consumer import dry-run adapter symbols into the explicit `lima.adapters.__all__` candidate public export surface, then update metadata/tests proving the cleanup preserved all frozen V1-G22 adapter exports and did not add runtime behavior.

Approved cleanup target:

- Package: `lima.adapters`
- Runtime file: `lima/adapters/__init__.py`
- Existing candidate symbols to expose through `__all__`:
  - `V1ConsumerImportDryRunError`
  - `validate_v1_consumer_integration_proof_to_import_dry_run`

The approved cleanup may only add those two existing module-level symbols to `lima.adapters.__all__`. It must not add a new validator, remove or rename existing exports, change validator behavior, edit consumer repositories, call imported symbols from consumers, wire shells, call providers/models, access credentials, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- `lima/adapters/__init__.py`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G28_RUNTIME_EXPORT_CLEANUP.md`
- `docs/V1_G28_RUNTIME_EXPORT_CLEANUP_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g28_runtime_export_cleanup.json`
- `tests/test_v1_g28_runtime_export_cleanup.py`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`

No other `lima/` runtime files may be created, edited, removed, or renamed in V1-G28.

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G28. Consumer repository validation may be run, but consumer repo file edits are not approved.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G28 may add only deterministic local runtime export metadata cleanup and tests.

Allowed if approved:

- add `V1ConsumerImportDryRunError` to `lima.adapters.__all__`
- add `validate_v1_consumer_integration_proof_to_import_dry_run` to `lima.adapters.__all__`
- preserve every existing frozen V1-G22 `lima.adapters.__all__` export
- preserve current symbol importability for Sparkbot and Arc-Bot-shell V1-G27 import-smoke tests
- refresh the candidate public API freeze fixture to include the G28-approved adapter export cleanup
- add a G28 cleanup evidence fixture
- add focused G28 tests proving export cleanup only
- document rollback and closeout evidence
- enforce no runtime behavior change confirmation
- enforce no consumer repo mutation confirmation
- enforce no live consumer runtime call confirmation
- enforce no provider/model, secret, credential, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G28 must not add:

- any `lima/` runtime file changes outside `lima/adapters/__init__.py`
- new validator behavior
- changes to `lima/adapters/v1_consumer_import_dry_run.py`
- changes to `lima/adapters/v1_consumer_integration_compatibility.py`
- removal or rename of existing frozen V1-G22 adapter exports
- removal or rename of any currently importable adapter symbol
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer application imports of LIMA outside existing focused tests
- consumer runtime calls
- LIMA runtime behavior invocation beyond import/export metadata checks
- consumer integration
- shell runtime wiring
- live provider/model calls
- model request dispatch
- secret lookup
- credential access
- tool execution
- action execution
- file mutation execution outside the exact approved files
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

- LIMA cleanup fixture records `CANDIDATE_ONLY`
- only `lima/adapters/__init__.py` is approved as a runtime file
- `V1ConsumerImportDryRunError` is exported through `lima.adapters.__all__`
- `validate_v1_consumer_integration_proof_to_import_dry_run` is exported through `lima.adapters.__all__`
- existing frozen V1-G22 `lima.adapters.__all__` exports remain present
- no existing frozen V1-G22 adapter export is removed or renamed
- G22 final public API freeze fixture is refreshed only for the approved adapter export cleanup
- Sparkbot V1-G27 import-smoke test still passes without consumer runtime calls
- Arc-Bot-shell V1-G27 import-smoke test still passes without consumer runtime calls
- no Sparkbot or Arc-Bot-shell files are edited
- no live consumer runtime calls are added
- no provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no raw content/secret/credential/customer-data/raw-diff/raw-patch persistence is added
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G28 tests
- LIMA focused V1-G27 tests
- LIMA focused V1-G23 tests
- LIMA focused V1-G22 tests
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

Rollback must remove only the exact approved V1-G28 changes:

- remove `V1ConsumerImportDryRunError` from `lima.adapters.__all__`
- remove `validate_v1_consumer_integration_proof_to_import_dry_run` from `lima.adapters.__all__`
- restore `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json` to the pre-G28 adapter export list
- remove the V1-G28 implementation docs/tests/fixtures listed above

Rollback must not require consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G28 files
- any `lima/` runtime file outside `lima/adapters/__init__.py` must change
- existing frozen V1-G22 adapter exports would be removed or renamed
- validator behavior must change
- Sparkbot file edits are required
- Arc-Bot-shell file edits are required
- consumer runtime calls are added
- LIMA runtime behavior beyond import/export metadata checks is invoked
- consumer integration is added
- shell runtime wiring is added
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- cleanup metadata can grant edit, import, execution, integration, provider/model, connector/browser/network, or physical-world authority
- tool execution is added
- action execution is added
- file mutation execution outside the exact approved files is added
- connector/browser/network/device/robotics/physical-world behavior is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Runtime export cleanup approved: no.
- Runtime export cleanup added: no.
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

If approved, create branch `v1-g28-runtime-export-cleanup` in LIMA-AI-OS. Implement only the exact runtime export cleanup slice. Do not edit consumer repositories, add runtime calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, or claim product readiness.
