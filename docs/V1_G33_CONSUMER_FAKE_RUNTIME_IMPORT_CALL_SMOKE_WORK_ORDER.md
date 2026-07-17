# V1-G33 Consumer Fake-Runtime Import/Call Smoke Work Order

Date: 2026-06-17
Branch: `prepare-v1-g33-consumer-fake-runtime-import-call-smoke-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_consumer_fake_runtime_import_call_smoke_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit runtime files, edit consumer repos, create consumer tests, call consumer runtimes, execute fake call envelopes, wire shells, or add runtime execution.

## Approval Dependency

V1-G33 implementation may start only after the operator explicitly approves:

`docs/V1_G33_CONSUMER_FAKE_RUNTIME_IMPORT_CALL_SMOKE_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G33 implementation docs/tests/fixture.
2. Keep implementation limited to approved docs/tests/fixtures.
3. Record Sparkbot fake-runtime import/call smoke evidence metadata.
4. Record Arc-Bot-shell fake-runtime import/call smoke evidence metadata.
5. Reference only the approved V1-G32 consumer tests and candidate adapter symbols.
6. Link V1-G27 import-smoke, V1-G28 export cleanup, V1-G29 planning, V1-G30 fake-runtime evidence, V1-G31 preview evidence, and V1-G32 test edit evidence.
7. Encode no-runtime-file-change, no-consumer-repo-mutation, no-live-call, no-adapter-symbol-call, no-fake-envelope-execution, no-provider/model, no-secret, no-network, no-raw-patch-in-LIMA-evidence, and proof-not-authority confirmations.
8. Run focused G33, G32, G31, G30, G29, G28, G27, and adapter-boundary tests.
9. Run Sparkbot focused V1-G32 and V1-G27 tests.
10. Run Arc-Bot-shell focused V1-G32 and V1-G27 tests.
11. Run the LIMA full suite.
12. Keep live consumer runtime calls unimplemented.
13. Keep provider/model calls unimplemented.
14. Keep product readiness unclaimed.

## Required Validation If Approved

Run at minimum:

- focused LIMA V1-G33 tests
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

- files outside the approved V1-G33 file map
- `lima/` runtime file changes
- Sparkbot or Arc-Bot-shell file edits
- consumer runtime/source file edits
- consumer runtime calls
- live consumer imports/calls
- LIMA runtime behavior beyond static smoke evidence metadata checks
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

Record exactly one valid operator choice in the V1-G33 operator decision packet.

If approved, implement only the exact consumer fake-runtime import/call smoke evidence slice. Do not edit runtime files, edit consumer repos, add live calls, wire shells, call providers/models, invoke connector/browser/network behavior, add physical-world behavior, persist raw patch content in LIMA evidence, or claim product readiness.
