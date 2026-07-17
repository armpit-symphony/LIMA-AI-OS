# V1-G32 Consumer Repository Test Edit Work Order

Date: 2026-06-17
Branch: `prepare-v1-g32-consumer-repository-test-edit-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_consumer_repository_test_edit_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit runtime files, edit consumer repos, create consumer tests, call consumer runtimes, wire shells, or add runtime execution.

## Approval Dependency

V1-G32 implementation may start only after the operator explicitly approves:

`docs/V1_G32_CONSUMER_REPOSITORY_TEST_EDIT_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G32 implementation docs/tests/fixture.
2. Add only the exact Sparkbot test/fixture files approved in the request.
3. Add only the exact Arc-Bot-shell test/fixture files approved in the request.
4. Keep consumer runtime/source files untouched.
5. Reference only the approved V1-G31 preview records and candidate adapter symbols.
6. Link V1-G27 import-smoke, V1-G28 export cleanup, V1-G29 planning, V1-G30 fake-runtime evidence, and V1-G31 preview evidence.
7. Encode no-runtime-file-change, no-consumer-runtime-source-change, no-live-call, no-adapter-symbol-call, no-provider/model, no-secret, no-network, no-raw-patch-in-LIMA-evidence, and proof-not-authority confirmations.
8. Run focused G32, G31, G30, G29, G28, G27, and adapter-boundary tests.
9. Run Sparkbot focused V1-G32 and V1-G27 tests.
10. Run Arc-Bot-shell focused V1-G32 and V1-G27 tests.
11. Run the LIMA full suite.
12. Keep live consumer runtime calls unimplemented.
13. Keep provider/model calls unimplemented.
14. Keep product readiness unclaimed.

## Required Validation If Approved

Run at minimum:

- focused LIMA V1-G32 tests
- focused LIMA V1-G31 tests
- focused LIMA V1-G30 tests
- focused LIMA V1-G29 tests
- focused LIMA V1-G28 tests
- focused LIMA V1-G27 tests
- focused LIMA adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- focused Sparkbot V1-G32 consumer test
- focused Sparkbot V1-G27 import-smoke test
- focused Arc-Bot-shell V1-G32 consumer test
- focused Arc-Bot-shell V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G32 file map
- `lima/` runtime file changes
- Sparkbot runtime/source file edits
- Arc-Bot-shell runtime/source file edits
- consumer files outside the exact approved tests/fixtures
- consumer runtime calls
- live consumer imports/calls
- LIMA runtime behavior beyond static evidence metadata checks and test-only import checks
- calls to planned adapter symbols
- fake call envelope execution
- consumer integration
- shell runtime wiring
- live provider/model calls
- model request dispatch
- secret lookup or credential access
- raw sensitive content persistence in LIMA evidence
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures files
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G32 operator decision packet.

If approved, implement only the exact consumer repository test edit slice. Do not edit runtime files, add live calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, persist raw patch content in LIMA evidence, or claim product readiness.
