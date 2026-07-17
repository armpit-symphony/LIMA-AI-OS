# V1-G19 Live Approval Evidence Capture Work Order

Date: 2026-06-16
Branch: `prepare-v1-g19-live-approval-evidence-capture-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_live_approval_evidence_capture_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, capture live approvals, verify raw PINs, issue approval tokens, execute actions, touch consumer repos, import consumer code, wire consumers, or add runtime execution.

## Approval Dependency

V1-G19 implementation may start only after the operator explicitly approves:

`docs/V1_G19_LIVE_APPROVAL_EVIDENCE_CAPTURE_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `lima/guardian/v1_live_approval_evidence.py`.
2. Add deterministic validators for sanitized live approval evidence metadata.
3. Require approval evidence id and challenge id metadata.
4. Require request id or Guardian decision id linkage.
5. Require tenant, shell, actor, session, and approver scope metadata.
6. Require approval intent and action-scope metadata.
7. Require risk class and action family metadata.
8. Normalize approved/denied/revoked/stale/expired/superseded/blocked outcomes.
9. Require freshness, expiration, and replay-prevention metadata.
10. Require factor evidence summary without raw factors.
11. Require capture source metadata.
12. Require audit/evidence linkage metadata.
13. Require proof-not-authority confirmation.
14. Reject raw PINs, approval tokens, credentials, secrets, raw prompts, raw file contents, and customer data.
15. Keep approval-token issuance unimplemented.
16. Keep execution authority unimplemented.
17. Keep consumer integration unimplemented.
18. Add candidate exports only in `lima/guardian/__init__.py`.
19. Add V1-G19 docs/tests/fixtures.

## Required Validation If Approved

Run at minimum:

- focused V1-G19 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G19 file map
- raw PIN verification or persistence
- approval-token issuance
- action execution
- file mutation execution
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- approval evidence metadata becoming runtime authority
- raw sensitive content persistence
- live provider/model routing
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- final API freeze
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G19 operator decision packet.

If approved, implement only the LIMA-side live approval evidence/capture metadata slice on branch `v1-g19-live-approval-evidence-capture`. Do not verify raw PINs, issue approval tokens, execute actions, or touch consumer repos.
