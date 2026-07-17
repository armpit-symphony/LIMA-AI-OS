# V1-G25 First Consumer Repo Patch-Preview Evidence Work Order

Date: 2026-06-17
Branch: `prepare-v1-g25-first-consumer-repo-patch-preview-evidence-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_first_consumer_repo_patch_preview_evidence_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, edit consumer repos, write patch files, persist raw diffs, import consumer code, call consumer runtimes, wire shells, clean up runtime exports, or add runtime execution.

## Approval Dependency

V1-G25 implementation may start only after the operator explicitly approves:

`docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE.md`.
2. Add `tests/fixtures/runtime_extraction/v1_g25_first_consumer_repo_patch_preview_evidence.json`.
3. Add one Sparkbot patch-preview evidence packet.
4. Add one Arc-Bot-shell patch-preview evidence packet.
5. Link each packet to V1-G24 import-plan evidence.
6. Link proof packet, compatibility packet, frozen API, and V1-G23 import-plan refs.
7. Encode proposed consumer file targets as sanitized metadata only.
8. Encode proposed import/call-site edit intent as metadata only.
9. Encode approval, rollback, validation, and audit metadata.
10. Encode no-write, no-raw-diff, and proof-not-authority confirmations.
11. Keep consumer repo edits unimplemented.
12. Keep live imports/calls unimplemented.
13. Keep runtime export cleanup unimplemented.
14. Add `docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE_CLOSEOUT.md`.

## Required Validation If Approved

Run at minimum:

- focused V1-G25 tests
- focused V1-G24 tests
- focused adapter boundary tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G25 file map
- `lima/` runtime file changes
- Sparkbot repo edits
- Arc-Bot-shell repo edits
- consumer repo edits
- consumer repo file writes
- patch files outside the approved fixture/doc paths
- raw diff persistence
- full patch content persistence
- raw sensitive content persistence
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- runtime export cleanup
- live provider/model calls
- model request dispatch
- secret lookup or credential access
- tool execution
- action execution
- file mutation execution
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G25 operator decision packet.

If approved, implement only the LIMA-side first consumer repo patch-preview evidence slice on branch `v1-g25-first-consumer-repo-patch-preview-evidence`. Do not edit consumer repos, write patch files, persist raw diffs, import consumer code, call consumer runtimes, clean up exports, or claim product readiness.
