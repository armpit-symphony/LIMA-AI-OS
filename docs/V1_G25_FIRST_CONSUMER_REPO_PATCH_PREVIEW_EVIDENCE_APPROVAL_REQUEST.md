# V1-G25 First Consumer Repo Patch-Preview Evidence Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g25-first-consumer-repo-patch-preview-evidence-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit Sparkbot, edit Arc-Bot-shell, edit any consumer repository, write patch files, persist raw diffs, import consumer code, call consumer runtimes, wire shells, clean up runtime exports, call providers/models, read secrets, execute tools, mutate files, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G25 implementation of the LIMA-side first consumer repo patch-preview evidence slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G24, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G25 Objective

Implement the smallest LIMA-side first consumer repo patch-preview evidence slice.

The slice should create sanitized patch-preview evidence for the first Sparkbot and Arc-Bot-shell consumer import-plan patches using V1-G24 import-plan evidence packets. The preview must describe proposed consumer repository file targets, intent, required approvals, rollback expectations, and validation commands as metadata only. It must not write consumer repository files, persist raw diffs or full patch contents, import consumer code, call consumer runtimes, wire shells, clean up exports, or claim product readiness.

## Approved Files If Operator Says Yes

Docs/tests/fixtures only:

- `docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE.md`
- `docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g25_first_consumer_repo_patch_preview_evidence.json`
- `tests/test_v1_g25_first_consumer_repo_patch_preview_evidence.py`

No `lima/` runtime files may be created or edited in V1-G25.

No Sparkbot, Arc-Bot-shell, or other consumer repository files may be created, edited, removed, renamed, staged, committed, or pushed in V1-G25.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G25 may add only deterministic local docs/tests/fixtures that describe and validate sanitized patch-preview evidence.

Allowed if approved:

- create one Sparkbot patch-preview evidence packet
- create one Arc-Bot-shell patch-preview evidence packet
- link each packet to its V1-G24 import-plan evidence packet
- link each packet to V1-G18 proof packet refs
- link each packet to V1-G21 compatibility packet refs
- link each packet to V1-G22 frozen API packet refs
- link each packet to V1-G23 dry-run import-plan refs
- record proposed consumer repository file targets as sanitized metadata only
- record proposed import/call-site edit intent as metadata only
- record patch risk, approval, rollback, and validation metadata
- record no-write and no-raw-diff confirmations
- enforce no consumer repo mutation confirmation
- enforce no live import/call confirmation
- enforce no runtime export cleanup confirmation
- enforce no raw file content, prompt, customer data, credential, provider token, API key, secret, raw diff, raw patch, or full patch content confirmation
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G25 must not add:

- `lima/` runtime file changes
- Sparkbot repo edits
- Arc-Bot-shell repo edits
- any consumer repo edits
- consumer repository file writes
- generated patch files outside the approved fixture/doc paths
- raw diff persistence
- full patch content persistence
- raw file content persistence
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- runtime export cleanup
- live provider/model calls
- model request dispatch
- secret lookup
- credential access
- tool execution
- action execution
- file mutation execution
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- fixture records `CANDIDATE_ONLY`
- Sparkbot patch-preview evidence packet exists
- Arc-Bot-shell patch-preview evidence packet exists
- each packet links to V1-G24 import-plan evidence
- proof packet refs are present
- compatibility packet refs are present
- frozen API packet refs are present
- V1-G23 import-plan refs are present
- proposed consumer file target metadata is sanitized metadata-only
- proposed edit intent metadata does not include raw diffs or full patch contents
- approval, rollback, and validation metadata are present
- no consumer repo mutation confirmation is enforced
- no live import/call confirmation is enforced
- no runtime export cleanup confirmation is enforced
- no raw content/secret/credential/customer-data/raw-diff/raw-patch confirmation is enforced
- proof-not-authority confirmation is enforced
- no `lima/` runtime file changes are required
- no consumer repo edits, live imports/calls, provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved

## Rollback Plan If Approved

Rollback must remove only:

- `docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE.md`
- `docs/V1_G25_FIRST_CONSUMER_REPO_PATCH_PREVIEW_EVIDENCE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g25_first_consumer_repo_patch_preview_evidence.json`
- `tests/test_v1_g25_first_consumer_repo_patch_preview_evidence.py`

Rollback must not require `lima/` runtime file changes, consumer repo changes, shell repo changes, Sparkbot changes, Arc-Bot-shell changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G25 files
- `lima/` runtime file changes are required
- Sparkbot repo edits are required
- Arc-Bot-shell repo edits are required
- consumer repo edits are required
- consumer repo file writes are required
- patch files outside the approved fixture/doc paths are generated
- raw contents, raw diffs, full patch contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- patch-preview metadata can grant edit, import, execution, or integration authority
- consumer code is imported
- consumer runtime calls are added
- consumer integration is added
- shell runtime wiring is added
- runtime export cleanup is required
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- tool execution is added
- action execution is added
- file mutation execution is added
- connector/browser/network/device/robotics/physical-world behavior is added
- scheduled task execution is added
- external sends are added
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- First consumer repo patch-preview evidence added: no.
- `lima/` runtime files changed: no.
- Sparkbot repo mutation added: no.
- Arc-Bot-shell repo mutation added: no.
- Consumer repo mutation added: no.
- Consumer repo file writes added: no.
- Raw diff or full patch persistence added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Consumer code imports added: no.
- Shell runtime wiring added: no.
- Runtime export cleanup approved: no.
- Live provider/model calls added: no.
- Secret lookup added: no.
- Credential access added: no.
- Tool execution added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g25-first-consumer-repo-patch-preview-evidence` and implement only the LIMA-side first consumer repo patch-preview evidence slice. Do not edit consumer repos, write patch files, persist raw diffs, import consumer code, call consumer runtimes, clean up exports, or claim product readiness.
