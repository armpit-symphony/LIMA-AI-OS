# V1-G26 First Consumer Repository Edit Work Order

Date: 2026-06-17
Branch: `prepare-v1-g26-first-consumer-repository-edit-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_first_consumer_repository_edit_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit consumer repos, import consumer code, call consumer runtimes, wire shells, clean up runtime exports, or add runtime execution.

## Approval Dependency

V1-G26 implementation may start only after the operator explicitly approves:

`docs/V1_G26_FIRST_CONSUMER_REPOSITORY_EDIT_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G26 implementation docs/tests/fixture.
2. Add the Sparkbot static V1-G26 proof packet.
3. Add the Sparkbot static V1-G26 proof fixture.
4. Add the Sparkbot static V1-G26 proof test.
5. Add the Arc-Bot-shell static V1-G26 proof packet.
6. Add the Arc-Bot-shell static V1-G26 proof fixture.
7. Add the Arc-Bot-shell static V1-G26 proof test.
8. Link consumer proof records to V1-G24 import-plan evidence and V1-G25 patch-preview evidence.
9. Encode no-live-import, no-runtime-wiring, no-provider-call, no-secret, and proof-not-authority confirmations.
10. Run focused tests in all edited repos.
11. Run LIMA full suite.
12. Keep runtime export cleanup unimplemented.
13. Keep live consumer imports/calls unimplemented.
14. Keep product readiness unclaimed.

## Required Validation If Approved

Run at minimum:

- focused LIMA V1-G26 tests
- focused LIMA V1-G25 tests
- focused LIMA adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- focused Sparkbot V1-G26 static proof test
- focused Arc-Bot-shell V1-G26 static proof test
- `git diff --check` in each edited repo
- `git diff --cached --check` in each edited repo
- `git status --short --branch` in each edited repo

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G26 file map
- `lima/` runtime file changes
- Sparkbot runtime/source edits
- Arc-Bot-shell runtime/source edits
- consumer code imports
- consumer runtime calls
- live LIMA imports from consumer repos
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

Record exactly one valid operator choice in the V1-G26 operator decision packet.

If approved, implement only the first consumer repository edit slice. Do not add runtime imports, runtime calls, shell wiring, export cleanup, provider/model calls, connector behavior, browser/network behavior, physical-world behavior, or product-readiness claims.
