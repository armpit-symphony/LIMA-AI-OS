# V1-G31 Fake-Runtime Consumer Repository Test Preview Work Order

Date: 2026-06-17
Branch: `prepare-v1-g31-fake-runtime-consumer-repo-test-preview-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_fake_runtime_consumer_repo_test_preview_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit runtime files, edit consumer repos, create consumer tests, call consumer runtimes, wire shells, or add runtime execution.

## Approval Dependency

V1-G31 implementation may start only after the operator explicitly approves:

`docs/V1_G31_FAKE_RUNTIME_CONSUMER_REPO_TEST_PREVIEW_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G31 implementation docs/tests/fixture.
2. Keep implementation limited to approved docs/tests/fixtures.
3. Record Sparkbot future test file path previews as metadata only.
4. Record Arc-Bot-shell future test file path previews as metadata only.
5. Reference only the approved V1-G30 fake-runtime evidence records and candidate adapter symbols.
6. Link V1-G27 import-smoke, V1-G28 export cleanup, V1-G29 planning, and V1-G30 fake-runtime evidence.
7. Encode no-runtime-file-change, no-consumer-repo-mutation, no-consumer-test-creation, no-live-call, no-adapter-symbol-call, no-provider/model, no-secret, no-network, no-raw-content, and proof-not-authority confirmations.
8. Run focused G31, G30, G29, G28, G27, and adapter-boundary tests.
9. Run Sparkbot and Arc-Bot-shell V1-G27 import-smoke tests without editing consumer repos.
10. Run the LIMA full suite.
11. Keep consumer repository edits unimplemented.
12. Keep live consumer runtime calls unimplemented.
13. Keep provider/model calls unimplemented.
14. Keep product readiness unclaimed.

## Required Validation If Approved

Run at minimum:

- focused LIMA V1-G31 tests
- focused LIMA V1-G30 tests
- focused LIMA V1-G29 tests
- focused LIMA V1-G28 tests
- focused LIMA V1-G27 tests
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

- files outside the approved V1-G31 file map
- `lima/` runtime file changes
- Sparkbot file edits
- Arc-Bot-shell file edits
- consumer test files
- raw consumer test file contents
- raw diff or full patch content persistence
- consumer runtime calls
- live consumer imports/calls
- LIMA runtime behavior beyond static preview metadata checks
- calls to planned adapter symbols
- fake call envelope execution
- consumer integration
- shell runtime wiring
- live provider/model calls
- model request dispatch
- secret lookup or credential access
- raw sensitive content persistence
- tool execution
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures files
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G31 operator decision packet.

If approved, implement only the fake-runtime consumer repository test preview metadata slice. Do not edit runtime files, edit consumer repos, create consumer tests, add live calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, persist raw patch/file content, or claim product readiness.
