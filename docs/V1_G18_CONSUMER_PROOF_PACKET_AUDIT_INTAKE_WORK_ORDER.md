# V1-G18 Consumer Proof Packet Audit Intake Work Order

Date: 2026-06-16
Branch: `prepare-v1-consumer-proof-packet-audit-intake-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_consumer_proof_packet_audit_intake_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, touch consumer repos, import consumer code, wire consumers, or add runtime execution.

## Approval Dependency

V1-G18 implementation may start only after the operator explicitly approves:

`docs/V1_G18_CONSUMER_PROOF_PACKET_AUDIT_INTAKE_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `lima/guardian/v1_consumer_proof_packet_intake.py`.
2. Add deterministic validators for consumer proof packet metadata.
3. Require Sparkbot, Arc Bot, LIMA Robo OS, LIMA Office, and future shell packet family support.
4. Require repo/ref/commit/path evidence metadata.
5. Require proposed import/call shape evidence.
6. Require normalized metadata examples.
7. Require capability profile expectations.
8. Require Guardian/approval boundary expectations.
9. Require dry-run and non-execution confirmation.
10. Require confirmation that no live consumer runtime path calls LIMA yet.
11. Require no bypass claims for tool/model/connector/browser/file/network/scheduled task/external send/device/robot/drone/IoT/physical-world behavior.
12. Require independent audit requirement.
13. Normalize received/missing/blocked/rejected/accepted-static-evidence packet statuses.
14. Reject raw sensitive content.
15. Keep consumer integration unimplemented.
16. Add candidate exports only in `lima/guardian/__init__.py`.
17. Add V1-G18 docs/tests/fixtures.

## Required Validation If Approved

Run at minimum:

- focused V1-G18 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G18 file map
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- proof packet metadata becoming runtime authority
- raw sensitive content persistence
- live provider/model routing
- connector/browser/network/device/robotics/physical-world behavior
- file mutation execution
- scheduled task execution
- external sends
- final API freeze
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G18 operator decision packet.

If approved, implement only the LIMA-side consumer proof packet audit intake metadata slice on branch `v1-g18-consumer-proof-packet-audit-intake`. Do not touch consumer repos.
