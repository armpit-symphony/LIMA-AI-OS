# V1-G24 First Consumer Import-Plan Evidence Packets Approval Request

Date: 2026-06-17
Branch: `prepare-v1-g24-first-consumer-import-plan-evidence-packets-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, edit Sparkbot, edit Arc-Bot-shell, edit any consumer repository, import consumer code, call consumer runtimes, wire shells, clean up runtime exports, call providers/models, read secrets, execute tools, mutate files, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G24 implementation of the LIMA-side first consumer import-plan evidence packets slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G23, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G24 Objective

Implement the smallest LIMA-side first consumer import-plan evidence packets slice.

The slice should create sanitized evidence packets for Sparkbot and Arc-Bot-shell import-plan review using V1-G18 proof intake, V1-G21 compatibility metadata, V1-G22 frozen API surfaces, and V1-G23 dry-run import-plan validation. It must not edit consumer repositories, import consumer code, call consumer runtimes, wire shells, clean up exports, or claim product readiness.

## Approved Files If Operator Says Yes

Docs/tests/fixtures only:

- `docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS.md`
- `docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g24_first_consumer_import_plan_evidence_packets.json`
- `tests/test_v1_g24_first_consumer_import_plan_evidence_packets.py`

No `lima/` runtime files may be created or edited in V1-G24.

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G24 may add only deterministic local docs/tests/fixtures that describe and validate sanitized import-plan evidence packets.

Allowed if approved:

- create one Sparkbot import-plan evidence packet
- create one Arc-Bot-shell import-plan evidence packet
- link each packet to V1-G18 proof packet refs
- link each packet to V1-G21 compatibility packet refs
- link each packet to V1-G22 frozen API packet refs
- validate each packet through the V1-G23 dry-run import-plan validator
- record proposed import metadata as metadata only
- record proposed call-site metadata as metadata only
- record adapter, Guardian, approval, and provider/model boundary mappings
- record expected dry-run test command metadata
- record rollback metadata
- enforce no consumer repo mutation confirmation
- enforce no live import/call confirmation
- enforce no runtime export cleanup confirmation
- enforce no raw content/secret/credential/customer-data confirmation
- enforce proof-not-authority confirmation

## Explicitly Forbidden

V1-G24 must not add:

- `lima/` runtime file changes
- Sparkbot repo edits
- Arc-Bot-shell repo edits
- any consumer repo edits
- consumer file writes
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
- Sparkbot evidence packet exists
- Arc-Bot-shell evidence packet exists
- each packet validates through `validate_v1_consumer_integration_proof_to_import_dry_run`
- proof packet refs are present
- compatibility packet refs are present
- frozen API packet refs are present
- proposed import metadata is metadata-only
- proposed call-site metadata is metadata-only
- adapter, Guardian, approval, and provider/model boundary mappings are present
- expected test command metadata is dry-run-only
- rollback metadata requires no consumer repo changes and no export cleanup
- no consumer repo mutation confirmation is enforced
- no live import/call confirmation is enforced
- no runtime export cleanup confirmation is enforced
- no raw content/secret/credential/customer-data confirmation is enforced
- proof-not-authority confirmation is enforced
- no `lima/` runtime file changes are required
- no consumer repo edits, live imports/calls, provider/model calls, connector/browser/network/device/robotics/physical-world behavior, or product-readiness claims are approved

## Rollback Plan If Approved

Rollback must remove only:

- `docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS.md`
- `docs/V1_G24_FIRST_CONSUMER_IMPORT_PLAN_EVIDENCE_PACKETS_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g24_first_consumer_import_plan_evidence_packets.json`
- `tests/test_v1_g24_first_consumer_import_plan_evidence_packets.py`

Rollback must not require `lima/` runtime file changes, consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, credential rotation, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G24 files
- `lima/` runtime file changes are required
- Sparkbot repo edits are required
- Arc-Bot-shell repo edits are required
- consumer repo edits are required
- consumer code is imported
- consumer runtime calls are added
- consumer integration is added
- shell runtime wiring is added
- runtime export cleanup is required
- live provider/model calls are added
- model request dispatch is added
- secret lookup or credential access is added
- raw contents, prompts, customer data, credentials, provider tokens, API keys, or secrets can persist or emit
- evidence packet metadata can grant execution authority
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
- First consumer import-plan evidence packets added: no.
- `lima/` runtime files changed: no.
- Sparkbot repo mutation added: no.
- Arc-Bot-shell repo mutation added: no.
- Consumer repo mutation added: no.
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

If approved, create branch `v1-g24-first-consumer-import-plan-evidence-packets` and implement only the LIMA-side first consumer import-plan evidence packets slice. Do not edit consumer repos, import consumer code, call consumer runtimes, clean up exports, or claim product readiness.
