# V1-G45 Runtime Export Cleanup Public API Refresh Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g45-runtime-export-cleanup-public-api-refresh-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit `lima/` runtime files, change public exports, refresh frozen public API fixtures, edit consumer repositories, call providers/models, execute live model requests, make network calls, read secrets, access credential values, execute fallback, execute tools, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G45 implementation of the runtime export cleanup/public API refresh slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G44, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G45 Objective

Implement the smallest runtime export cleanup/public API refresh slice for the existing V1-G44 validator.

The slice should expose the existing V1-G44 live provider/model call authority symbols through `lima.harness.__all__`, then refresh the V1-G22 final public API freeze fixture so frozen public API tests match the new candidate harness export surface.

Approved cleanup target:

- Package: `lima.harness`
- Runtime file: `lima/harness/__init__.py`
- Export surface: `lima.harness.__all__`
- Existing V1-G44 symbols to expose through `__all__`:
  - `V1LiveProviderModelCallAuthorityError`
  - `validate_v1_live_provider_model_call_authority`

The approved cleanup may only add those two existing module-level symbols to `lima.harness.__all__` and refresh the frozen public API fixture for that exact export change. It must not change validator behavior, add a new validator, remove or rename existing exports, edit consumer repositories, call providers/models, make network calls, access credentials, or claim product readiness.

## Approved Files If Operator Says Yes

LIMA-AI-OS runtime files:

- `lima/harness/__init__.py`

LIMA-AI-OS docs/tests/fixtures:

- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH.md`
- `docs/V1_G45_RUNTIME_EXPORT_CLEANUP_PUBLIC_API_REFRESH_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g45_runtime_export_cleanup_public_api_refresh.json`
- `tests/test_v1_g45_runtime_export_cleanup_public_api_refresh.py`
- `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`

Sparkbot:

- none

Arc-Bot-shell:

- none

No Sparkbot or Arc-Bot-shell files may be created, edited, removed, or renamed in V1-G45.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G45 may add only deterministic local runtime export cleanup/public API refresh metadata and tests.

Allowed if approved:

- add `V1LiveProviderModelCallAuthorityError` to `lima.harness.__all__`
- add `validate_v1_live_provider_model_call_authority` to `lima.harness.__all__`
- preserve every existing frozen V1-G22 `lima.harness.__all__` export
- preserve V1-G44 validator behavior exactly
- refresh the candidate public API freeze fixture to include the G45-approved harness export cleanup
- add a G45 cleanup evidence fixture
- add focused G45 tests proving export cleanup only
- document rollback and closeout evidence
- enforce no runtime behavior change confirmation
- enforce no consumer repo mutation confirmation
- enforce no live provider/model execution confirmation
- enforce no network, secret, credential, fallback, connector, browser/network, file/device/robotics/physical-world behavior confirmation
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G45 must not add:

- any `lima/` runtime file changes outside `lima/harness/__init__.py`
- new validator behavior
- changes to `lima/harness/v1_live_provider_model_call_authority.py`
- changes to `lima/harness/v1_provider_model_routing_authority.py`
- removal or rename of existing frozen V1-G22 harness exports
- removal or rename of any currently importable harness symbol
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer application imports of LIMA outside focused tests
- consumer runtime calls
- live provider/model call execution
- actual model request dispatch execution
- network calls
- provider readiness network checks
- Token Guardian live routing
- secret lookup
- credential value access
- fallback execution
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
- only `lima/harness/__init__.py` is approved as a runtime file
- `V1LiveProviderModelCallAuthorityError` is exported through `lima.harness.__all__`
- `validate_v1_live_provider_model_call_authority` is exported through `lima.harness.__all__`
- existing frozen V1-G22 `lima.harness.__all__` exports remain present
- no existing frozen V1-G22 harness export is removed or renamed
- G22 final public API freeze fixture is refreshed only for the approved G45 harness export cleanup
- V1-G44 validator tests still pass without behavior changes
- no Sparkbot or Arc-Bot-shell files are edited
- no live provider/model execution, network calls, secret lookup, credential value access, fallback execution, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved
- no raw content/secret/credential/customer-data/raw-diff/raw-patch persistence is added
- proof-not-authority confirmation is enforced

## Required Validation If Approved

Run at minimum:

- LIMA focused V1-G45 tests
- LIMA focused V1-G44 tests
- LIMA focused V1-G22 final public API freeze tests
- LIMA focused V1-G20 provider/model routing authority tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check` before commit
- `git status --short --branch`

Do not require or run live provider/model calls, network calls, connector calls, browser/network calls, migrations, services, workers, production deploys, or physical-world/device behavior.

## Rollback Plan If Approved

Rollback must remove only the exact approved V1-G45 changes:

- remove `V1LiveProviderModelCallAuthorityError` from `lima.harness.__all__`
- remove `validate_v1_live_provider_model_call_authority` from `lima.harness.__all__`
- restore `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json` to the pre-G45 harness export list
- remove the V1-G45 implementation docs/tests/fixtures listed above

Rollback must not require consumer repository changes, shell runtime changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G45 files
- any `lima/` runtime file outside `lima/harness/__init__.py` must change
- existing frozen V1-G22 harness exports would be removed or renamed
- validator behavior must change
- Sparkbot file edits are required
- Arc-Bot-shell file edits are required
- consumer runtime calls are added
- live provider/model call execution is added
- actual model request dispatch execution is added
- network calls are added
- provider readiness network checks are added
- Token Guardian live routing is added
- secret lookup or credential value access is added
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- cleanup metadata can grant edit, import, execution, integration, provider/model, connector/browser/network, or physical-world authority
- fallback execution is added
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
- Runtime export cleanup/public API refresh approved: no.
- Runtime export cleanup/public API refresh added: no.
- `lima/` runtime files changed by this request: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Live provider/model call execution added: no.
- Network calls added: no.
- Secret lookup added: no.
- Credential value access added: no.
- Fallback execution added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g45-runtime-export-cleanup-public-api-refresh` in LIMA-AI-OS. Implement only the exact export cleanup/public API refresh slice. Do not edit consumer repositories, add runtime calls, call providers/models, make network calls, access credentials, invoke connector/browser/network behavior, add physical-world behavior, or claim product readiness.
