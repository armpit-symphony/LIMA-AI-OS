# V1-G28 Runtime Export Cleanup Work Order

Date: 2026-06-17
Branch: `prepare-v1-g28-runtime-export-cleanup-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_runtime_export_cleanup_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit runtime exports, edit consumer repos, call consumer runtimes, wire shells, or add runtime execution.

## Approval Dependency

V1-G28 implementation may start only after the operator explicitly approves:

`docs/V1_G28_RUNTIME_EXPORT_CLEANUP_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G28 implementation docs/tests/fixture.
2. Edit only `lima/adapters/__init__.py` as the approved runtime file.
3. Add `V1ConsumerImportDryRunError` to `lima.adapters.__all__`.
4. Add `validate_v1_consumer_integration_proof_to_import_dry_run` to `lima.adapters.__all__`.
5. Preserve every existing frozen V1-G22 adapter export.
6. Refresh `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json` only for the approved adapter export cleanup.
7. Add focused tests proving no export removal or rename.
8. Run focused G28, G27, G23, G22, and adapter-boundary tests.
9. Run Sparkbot and Arc-Bot-shell V1-G27 import-smoke tests without editing consumer repos.
10. Run the LIMA full suite.
11. Keep live consumer runtime calls unimplemented.
12. Keep provider/model calls unimplemented.
13. Keep product readiness unclaimed.

## Required Validation If Approved

Run at minimum:

- focused LIMA V1-G28 tests
- focused LIMA V1-G27 tests
- focused LIMA V1-G23 tests
- focused LIMA V1-G22 tests
- focused LIMA adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- focused Sparkbot V1-G27 import-smoke test
- focused Arc-Bot-shell V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G28 file map
- any `lima/` runtime file change outside `lima/adapters/__init__.py`
- existing frozen adapter export removal or rename
- validator behavior changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer runtime calls
- LIMA runtime behavior beyond import/export metadata checks
- consumer integration
- shell runtime wiring
- live provider/model calls
- model request dispatch
- secret lookup or credential access
- raw sensitive content persistence
- raw diff or full patch content persistence
- tool execution
- action execution
- file mutation execution outside the exact approved files
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G28 operator decision packet.

If approved, implement only the runtime export cleanup slice. Do not edit consumer repos, add runtime calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, or claim product readiness.
