# V1-G35 Consumer Integration Compatibility Review Work Order

Date: 2026-06-17
Branch: `prepare-v1-g35-consumer-integration-compatibility-review-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_consumer_integration_compatibility_review_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit runtime files, edit consumer repos, create consumer tests, call adapter validators, import consumer runtimes, wire shells, or add integration authority.

## Approval Dependency

V1-G35 implementation may start only after the operator explicitly approves:

`docs/V1_G35_CONSUMER_INTEGRATION_COMPATIBILITY_REVIEW_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work in LIMA-AI-OS.

## Implementation Sequence If Approved

1. Add the LIMA-side V1-G35 implementation docs/tests/fixture.
2. Keep implementation limited to approved docs/tests/fixtures.
3. Record Sparkbot compatibility review metadata.
4. Record Arc-Bot-shell compatibility review metadata.
5. Link V1-G27 through V1-G34 evidence.
6. Record review gaps and next-lane recommendations.
7. Encode no-runtime-file-change, no-consumer-repo-mutation, no-adapter-call, no-consumer-runtime-module-import, no-shell-wiring, no-provider/model, no-secret, no-network, no-raw-sensitive-content, proof-not-integration-authority, and proof-not-product-readiness confirmations.
8. Run focused G35, G34, G33, G32, G31, G30, G29, G28, G27, and adapter-boundary tests.
9. Run Sparkbot focused V1-G34, V1-G32, and V1-G27 tests.
10. Run Arc-Bot-shell focused V1-G34, V1-G32, and V1-G27 tests.
11. Run the LIMA full suite.
12. Keep consumer integration unimplemented.
13. Keep provider/model calls unimplemented.
14. Keep product readiness unclaimed.

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G35 file map
- `lima/` runtime file changes
- Sparkbot or Arc-Bot-shell file edits
- adapter symbol calls
- consumer runtime module imports
- shell runtime wiring
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

Record exactly one valid operator choice in the V1-G35 operator decision packet.
