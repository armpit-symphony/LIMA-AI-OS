# V1-G22 Final Public API Freeze Work Order

Date: 2026-06-17
Branch: `prepare-v1-g22-final-public-api-freeze-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_final_public_api_freeze_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, freeze the final public API, clean up runtime exports, edit consumer repos, import consumer code, call consumer runtimes, wire shells, or add runtime execution.

## Approval Dependency

V1-G22 implementation may start only after the operator explicitly approves:

`docs/V1_G22_FINAL_PUBLIC_API_FREEZE_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `docs/V1_G22_FINAL_PUBLIC_API_FREEZE.md`.
2. Add `tests/fixtures/runtime_extraction/v1_g22_final_public_api_freeze.json`.
3. Add `tests/test_v1_g22_final_public_api_freeze.py`.
4. Record final API freeze packet id metadata.
5. Record public package import surfaces.
6. Record public subpackage `__all__` export surfaces.
7. Record V1 runtime symbol surfaces.
8. Record candidate export inventory refs.
9. Record consumer compatibility refs.
10. Record import surface expectation refs.
11. Record backward compatibility policy.
12. Record future public API change gate policy.
13. Record runtime export cleanup as not approved.
14. Record Guardian, approval, and provider/model route boundary confirmations.
15. Record no consumer repo mutation confirmation.
16. Record no live import/call confirmation.
17. Record no runtime behavior change confirmation.
18. Record no secret/credential/customer-data confirmation.
19. Record proof-not-authority confirmation.
20. Add tests that local `__all__` exports match the freeze fixture.
21. Add tests that frozen symbols are importable locally.
22. Keep `lima/` runtime files unchanged.
23. Add `docs/V1_G22_FINAL_PUBLIC_API_FREEZE_CLOSEOUT.md`.

## Required Validation If Approved

Run at minimum:

- focused V1-G22 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G22 file map
- `lima/` runtime file changes
- runtime export cleanup
- symbol removal or rename from current exports
- unreviewed public exports
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
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

Record exactly one valid operator choice in the V1-G22 operator decision packet.

If approved, implement only the LIMA-side final public API freeze docs/tests/fixtures slice on branch `v1-g22-final-public-api-freeze`. Do not edit `lima/` runtime files, clean up exports, edit consumer repos, import consumer code, call consumer runtimes, or claim product readiness.
