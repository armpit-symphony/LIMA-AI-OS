# V1-G21 Consumer Integration Compatibility Freeze Work Order

Date: 2026-06-17
Branch: `prepare-v1-g21-consumer-integration-compatibility-freeze-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_consumer_integration_compatibility_freeze_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit consumer repos, import consumer code, call consumer runtimes, wire shells, freeze the final public API, or add runtime execution.

## Approval Dependency

V1-G21 implementation may start only after the operator explicitly approves:

`docs/V1_G21_CONSUMER_INTEGRATION_COMPATIBILITY_FREEZE_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `lima/adapters/v1_consumer_integration_compatibility.py`.
2. Add deterministic validators for sanitized consumer compatibility/freeze metadata.
3. Require compatibility packet id metadata.
4. Require consumer packet family, name, repository, branch/ref, and commit SHA metadata.
5. Require candidate export surface refs.
6. Require runtime symbol refs.
7. Require import surface expectation metadata.
8. Require fixture compatibility matrix metadata.
9. Require version compatibility metadata.
10. Require Guardian boundary compatibility metadata.
11. Require approval boundary compatibility metadata.
12. Require provider/model route boundary compatibility metadata.
13. Require consumer runtime call prohibition metadata.
14. Require no consumer repo mutation confirmation.
15. Require no live import/call confirmation.
16. Require final public API freeze not claimed confirmation.
17. Require audit/evidence linkage metadata.
18. Require proof-not-authority confirmation.
19. Reject raw contents, prompts, customer data, credentials, provider tokens, API keys, and secrets.
20. Keep consumer integration unimplemented.
21. Keep final public API freeze unimplemented.
22. Keep provider/model calls, secret lookup, and execution unimplemented.
23. Add candidate exports only in `lima/adapters/__init__.py`.
24. Add V1-G21 docs/tests/fixtures.

## Required Validation If Approved

Run at minimum:

- focused V1-G21 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G21 file map
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- final public API freeze
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

Record exactly one valid operator choice in the V1-G21 operator decision packet.

If approved, implement only the LIMA-side consumer integration compatibility/freeze metadata slice on branch `v1-g21-consumer-integration-compatibility-freeze`. Do not edit consumer repos, import consumer code, call consumer runtimes, freeze the final public API, or claim product readiness.
