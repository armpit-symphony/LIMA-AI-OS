# V1-G38 Consumer Repository Edit Work Order

Date: 2026-06-17
Branch: `prepare-v1-g38-consumer-repository-edit-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_consumer_repository_edit_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit runtime files, edit consumer repos, create consumer tests, apply patches, call adapter symbols, import consumer runtimes, wire shells, or add integration authority.

## Approval Dependency

V1-G38 implementation may start only after the operator explicitly approves:

`docs/V1_G38_CONSUMER_REPOSITORY_EDIT_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G38 implementation docs/tests/fixture.
2. Add only the exact approved Sparkbot static test/fixture files.
3. Add only the exact approved Arc-Bot-shell static test/fixture files.
4. Link V1-G37 patch-preview, audit, authority-chain, readiness rollup, and next-lane decision evidence.
5. Record Sparkbot and Arc-Bot-shell commit evidence after edits.
6. Encode no-LIMA-runtime-file-change, no-unapproved-consumer-file-edit, no-consumer-runtime-source-change, no-adapter-call, no-consumer-runtime-module-import, no-consumer-integration, no-shell-wiring-implementation, no-provider/model, no-secret, no-network, no-raw-sensitive-content, proof-not-integration-authority, and proof-not-product-readiness confirmations.
7. Run focused G38, G37, G36, G35, G34, G33, G32, G31, G30, G29, G28, G27, and adapter-boundary tests.
8. Run Sparkbot focused V1-G38, V1-G34, V1-G31, and V1-G27 tests.
9. Run Arc-Bot-shell focused V1-G38, V1-G34, V1-G31, and V1-G27 tests.
10. Run the LIMA full suite.
11. Keep consumer integration unimplemented.
12. Keep provider/model calls unimplemented.
13. Keep product readiness unclaimed.

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G38 file map
- `lima/` runtime file changes
- Sparkbot or Arc-Bot-shell file edits outside exact approved paths
- consumer runtime/source file edits outside exact approved paths
- raw patch body persistence in LIMA evidence
- unapproved patch application
- adapter symbol calls
- consumer runtime module imports
- consumer integration
- shell runtime wiring implementation
- provider/model calls
- model request dispatch
- fallback execution
- secret lookup or credential access
- raw sensitive content persistence in LIMA evidence
- action execution
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G38 operator decision packet.
