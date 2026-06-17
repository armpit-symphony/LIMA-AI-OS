# V1-G24 First Consumer Import-Plan Evidence Packets Work Order

Date: 2026-06-17
Branch: `prepare-v1-g24-first-consumer-import-plan-evidence-packets-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_first_consumer_import_plan_evidence_packets_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit consumer repos, import consumer code, call consumer runtimes, wire shells, clean up runtime exports, or add runtime execution.

## Approval Dependency

V1-G24 implementation may start only after the operator explicitly approves:

`docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS.md`.
2. Add `tests/fixtures/runtime_extraction/v1_g24_first_consumer_import_plan_evidence_packets.json`.
3. Add one Sparkbot import-plan evidence packet.
4. Add one Arc-Bot-shell import-plan evidence packet.
5. Link proof packet, compatibility packet, and frozen API refs.
6. Encode proposed imports and call sites as metadata only.
7. Encode adapter, Guardian, approval, and provider/model boundary mappings.
8. Encode dry-run expected test command metadata.
9. Encode rollback metadata.
10. Validate each packet through the V1-G23 validator in tests.
11. Keep consumer repo edits unimplemented.
12. Keep live imports/calls unimplemented.
13. Keep runtime export cleanup unimplemented.
14. Add `docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS_CLOSEOUT.md`.

## Required Validation If Approved

Run at minimum:

- focused V1-G24 tests
- focused V1-G23 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G24 file map
- `lima/` runtime file changes
- Sparkbot repo edits
- Arc-Bot-shell repo edits
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
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

Record exactly one valid operator choice in the V1-G24 operator decision packet.

If approved, implement only the LIMA-side first consumer import-plan evidence packets slice on branch `v1-g24-first-consumer-import-plan-evidence-packets`. Do not edit consumer repos, import consumer code, call consumer runtimes, clean up exports, or claim product readiness.
