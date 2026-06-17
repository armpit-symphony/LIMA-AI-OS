# V1-G28 Runtime Export Cleanup Closeout

Date: 2026-06-17
Branch: `v1-g28-runtime-export-cleanup`
API status: `CANDIDATE_ONLY`

Closeout verdict: `complete_with_live_integration_blocked`

V1-G28 is complete as the approved runtime export cleanup slice.

## Completed Scope

- Added `V1ConsumerImportDryRunError` to `lima.adapters.__all__`.
- Added `validate_v1_consumer_integration_proof_to_import_dry_run` to `lima.adapters.__all__`.
- Preserved every prior frozen V1-G22 adapter export.
- Refreshed the candidate final public API freeze fixture for the approved adapter export cleanup.
- Added LIMA-side cleanup evidence fixture and focused tests.
- Confirmed Sparkbot and Arc-Bot-shell V1-G27 import-smoke tests still pass without consumer runtime calls.

## Confirmed Non-Scope

- No runtime file outside `lima/adapters/__init__.py` was changed.
- No validator behavior was changed.
- No Sparkbot file was changed.
- No Arc-Bot-shell file was changed.
- No consumer runtime calls were added.
- No consumer integration was added.
- No shell runtime wiring was added.
- No provider/model calls were added.
- No secret lookup or credential access was added.
- No tool/action execution was added.
- No file mutation execution outside approved files was added.
- No connector/browser/network/device/robotics/physical-world behavior was added.
- No raw diffs, full patch bodies, or raw file contents were persisted.
- No product-readiness or production-readiness claim was made.

## Validation Required

Before this closeout is accepted, run:

- `python -m pytest -q tests/test_v1_g28_runtime_export_cleanup.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g28_runtime_export_cleanup_approval_request.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g27_first_consumer_frozen_api_import_smoke.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g23_consumer_integration_proof_to_import_dry_run.py -p no:cacheprovider`
- `python -m pytest -q tests/test_v1_g22_final_public_api_freeze.py -p no:cacheprovider`
- `python -m pytest -q tests/test_adapter_boundaries.py -p no:cacheprovider`
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- Sparkbot focused V1-G27 import-smoke test
- Arc-Bot-shell focused V1-G27 import-smoke test
- `git diff --check`
- `git diff --cached --check`

## Next Step

Create a separate V1-G28 audit branch.

After audit, the next approval gate may request live consumer import/call planning. That work must remain blocked until the operator explicitly approves exact file scope, validation, rollback, and stop conditions.
