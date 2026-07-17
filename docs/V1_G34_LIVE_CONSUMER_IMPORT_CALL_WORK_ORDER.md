# V1-G34 Live Consumer Import/Call Work Order

Date: 2026-06-17
Branch: `prepare-v1-g34-live-consumer-import-call-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_live_consumer_import_call_test_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit runtime files, edit consumer repos, create consumer tests, call consumer runtimes, execute adapter validators, wire shells, or add provider/model execution.

## Approval Dependency

V1-G34 implementation may start only after the operator explicitly approves:

`docs/V1_G34_LIVE_CONSUMER_IMPORT_CALL_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G34 implementation docs/tests/fixture.
2. Add only the approved Sparkbot focused test and fixture.
3. Add only the approved Arc-Bot-shell focused test and fixture.
4. Keep LIMA implementation limited to approved docs/tests/fixtures.
5. Keep consumer implementation limited to approved focused test/fixture files.
6. Call only the two approved LIMA adapter validators from the exact focused consumer tests.
7. Use only static sanitized metadata fixtures.
8. Do not import Sparkbot or Arc-Bot-shell runtime modules.
9. Do not wire shells.
10. Do not call providers/models, access secrets, invoke connectors, use browser/network behavior, or add physical-world behavior.
11. Link V1-G27 import-smoke, V1-G28 export cleanup, V1-G29 planning, V1-G30 fake-runtime evidence, V1-G31 preview evidence, V1-G32 consumer test edit evidence, and V1-G33 smoke evidence.
12. Run focused G34, G33, G32, G31, G30, G29, G28, G27, and adapter-boundary tests.
13. Run Sparkbot focused V1-G34, V1-G32, and V1-G27 tests.
14. Run Arc-Bot-shell focused V1-G34, V1-G32, and V1-G27 tests.
15. Run the LIMA full suite.
16. Keep provider/model calls, connector/browser/network behavior, physical-world behavior, and product readiness unimplemented.

## Required Validation If Approved

Run at minimum:

- focused LIMA V1-G34 tests
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
- focused Sparkbot V1-G34 live consumer import/call test
- focused Sparkbot V1-G32 consumer test
- focused Sparkbot V1-G27 import-smoke test
- focused Arc-Bot-shell V1-G34 live consumer import/call test
- focused Arc-Bot-shell V1-G32 consumer test
- focused Arc-Bot-shell V1-G27 import-smoke test
- `git diff --check` in each checked repo
- `git diff --cached --check` before each commit
- `git status --short --branch` in each checked repo

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G34 file map
- `lima/` runtime file changes
- Sparkbot or Arc-Bot-shell runtime/source file edits
- consumer runtime module imports
- shell runtime wiring
- unapproved adapter symbols
- provider/model calls
- model request dispatch
- fallback execution
- secret lookup or credential access
- raw sensitive content persistence in LIMA evidence
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures files
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G34 operator decision packet.

If approved, implement only the exact live consumer import/call test slice. Do not edit runtime files, wire shells, call providers/models, access secrets, invoke connector/browser/network behavior, add physical-world behavior, persist raw sensitive content in LIMA evidence, or claim product readiness.
