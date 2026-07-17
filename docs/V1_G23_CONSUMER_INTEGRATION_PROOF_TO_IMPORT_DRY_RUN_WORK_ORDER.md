# V1-G23 Consumer Integration Proof-To-Import Dry Run Work Order

Date: 2026-06-17
Branch: `prepare-v1-g23-consumer-integration-proof-to-import-dry-run-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_consumer_integration_proof_to_import_dry_run_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit consumer repos, import consumer code, call consumer runtimes, wire shells, clean up runtime exports, or add runtime execution.

## Approval Dependency

V1-G23 implementation may start only after the operator explicitly approves:

`docs/V1_G23_CONSUMER_INTEGRATION_PROOF_TO_IMPORT_DRY_RUN_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `lima/adapters/v1_consumer_import_dry_run.py`.
2. Add deterministic validators for sanitized dry-run import-plan metadata.
3. Require import plan id metadata.
4. Require consumer packet family, name, repository, branch/ref, and commit SHA metadata.
5. Require proof packet ref metadata.
6. Require compatibility packet ref metadata.
7. Require frozen API packet ref metadata.
8. Require proposed import metadata and keep it metadata-only.
9. Require proposed call-site metadata and keep it metadata-only.
10. Require adapter, Guardian, approval, and provider/model boundary mapping metadata.
11. Require expected test command metadata.
12. Require rollback metadata.
13. Require no consumer repo mutation confirmation.
14. Require no live import/call confirmation.
15. Require no runtime export cleanup confirmation.
16. Require no raw content/secret/credential/customer-data confirmation.
17. Require proof-not-authority confirmation.
18. Keep consumer integration unimplemented.
19. Keep runtime export cleanup unimplemented.
20. Keep provider/model calls, secret lookup, and execution unimplemented.
21. Add candidate exports only in `lima/adapters/__init__.py`.
22. Add V1-G23 docs/tests/fixtures.

## Required Validation If Approved

Run at minimum:

- focused V1-G23 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G23 file map
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- runtime export cleanup
- live provider/model calls
- model request dispatch
- secret lookup or credential access
- raw sensitive content persistence
- tool execution
- action execution
- file mutation execution
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G23 operator decision packet.

If approved, implement only the LIMA-side consumer integration proof-to-import dry-run metadata slice on branch `v1-g23-consumer-integration-proof-to-import-dry-run`. Do not edit consumer repos, import consumer code, call consumer runtimes, clean up exports, or claim product readiness.
