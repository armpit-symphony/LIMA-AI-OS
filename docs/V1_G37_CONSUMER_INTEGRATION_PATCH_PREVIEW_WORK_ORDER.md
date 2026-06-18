# V1-G37 Consumer Integration Patch-Preview Work Order

Date: 2026-06-17
Branch: `prepare-v1-g37-consumer-integration-patch-preview-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_consumer_integration_patch_preview_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit runtime files, edit consumer repos, create consumer tests, persist raw patch bodies, apply patches, call adapter symbols, import consumer runtimes, wire shells, or add integration authority.

## Approval Dependency

V1-G37 implementation may start only after the operator explicitly approves:

`docs/V1_G37_CONSUMER_INTEGRATION_PATCH_PREVIEW_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G37 implementation docs/tests/fixture.
2. Keep implementation limited to approved docs/tests/fixtures.
3. Record Sparkbot consumer integration patch-preview metadata.
4. Record Arc-Bot-shell consumer integration patch-preview metadata.
5. Link V1-G36 bounded design, audit, authority-chain, readiness rollup, and next-lane decision evidence.
6. Define future candidate consumer edit intent categories without applying edits.
7. Define future candidate consumer file refs without mutating files.
8. Encode no-runtime-file-change, no-consumer-repo-mutation, no-raw-patch-body, no-patch-application, no-adapter-call, no-consumer-runtime-module-import, no-consumer-integration, no-shell-wiring-implementation, no-provider/model, no-secret, no-network, no-raw-sensitive-content, proof-not-edit-authority, proof-not-integration-authority, and proof-not-product-readiness confirmations.
9. Run focused G37, G36, G35, G34, G33, G32, G31, G30, G29, G28, G27, and adapter-boundary tests.
10. Run Sparkbot focused V1-G34, V1-G31, and V1-G27 tests.
11. Run Arc-Bot-shell focused V1-G34, V1-G31, and V1-G27 tests.
12. Run the LIMA full suite.
13. Keep consumer repository edits unimplemented.
14. Keep consumer integration unimplemented.
15. Keep provider/model calls unimplemented.
16. Keep product readiness unclaimed.

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G37 file map
- `lima/` runtime file changes
- Sparkbot or Arc-Bot-shell file edits
- raw patch body persistence
- patch application
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

Record exactly one valid operator choice in the V1-G37 operator decision packet.
