# V1-G27 First Consumer Frozen API Import-Smoke Work Order

Date: 2026-06-17
Branch: `prepare-v1-g27-first-consumer-frozen-api-import-smoke-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_first_consumer_frozen_api_import_smoke_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit consumer repos, import consumer runtimes, call consumer runtimes, wire shells, clean up runtime exports, or add runtime execution.

## Approval Dependency

V1-G27 implementation may start only after the operator explicitly approves:

`docs/V1_G27_FIRST_CONSUMER_FROZEN_API_IMPORT_SMOKE_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G27 implementation docs/tests/fixture.
2. Add the Sparkbot V1-G27 import-smoke fixture.
3. Add the Sparkbot V1-G27 import-smoke test.
4. Add the Arc-Bot-shell V1-G27 import-smoke fixture.
5. Add the Arc-Bot-shell V1-G27 import-smoke test.
6. Ensure consumer tests import only the approved frozen G22 LIMA API symbols.
7. Ensure consumer tests do not call imported symbols.
8. Link import-smoke records to V1-G22, V1-G24, V1-G25, and V1-G26 evidence.
9. Encode no-runtime-call, no-runtime-wiring, no-provider-call, no-secret, and proof-not-authority confirmations.
10. Run focused tests in all edited repos.
11. Run LIMA full suite.
12. Keep runtime export cleanup unimplemented.
13. Keep live consumer runtime calls unimplemented.
14. Keep product readiness unclaimed.

## Required Validation If Approved

Run at minimum:

- focused LIMA V1-G27 tests
- focused LIMA V1-G26 tests
- focused LIMA V1-G22 tests
- focused LIMA adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- focused Sparkbot V1-G27 import-smoke test
- focused Arc-Bot-shell V1-G27 import-smoke test
- `git diff --check` in each edited repo
- `git diff --cached --check` in each edited repo
- `git status --short --branch` in each edited repo

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G27 file map
- `lima/` runtime file changes
- Sparkbot runtime/source edits
- Arc-Bot-shell runtime/source edits
- consumer application imports outside focused tests
- approved frozen API symbol calls instead of import smoke
- consumer runtime calls
- LIMA runtime behavior invocation
- consumer integration
- shell runtime wiring
- runtime export cleanup
- live provider/model calls
- model request dispatch
- secret lookup or credential access
- raw sensitive content persistence
- raw diff or full patch content persistence
- tool execution
- action execution
- file mutation execution outside the exact approved docs/tests/fixtures files
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G27 operator decision packet.

If approved, implement only the first consumer frozen API import-smoke slice. Do not add runtime calls, shell wiring, export cleanup, provider/model calls, connector behavior, browser/network behavior, physical-world behavior, or product-readiness claims.
