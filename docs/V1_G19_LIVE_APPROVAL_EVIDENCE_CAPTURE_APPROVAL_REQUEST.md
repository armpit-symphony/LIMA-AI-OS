# V1-G19 Live Approval Evidence Capture Approval Request

Date: 2026-06-16
Branch: `prepare-v1-g19-live-approval-evidence-capture-approval-request`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve implementation, capture live approvals, verify raw PINs, issue approval tokens, execute actions, mutate files, touch consumer repositories, import consumer code, wire consumers, route providers/models, activate HumanInput, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G19 implementation of the LIMA-side live approval evidence/capture metadata slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. V1-G18, readiness rollups, decision matrices, broad product direction, or this request packet do not count as implementation approval.

## Proposed V1-G19 Objective

Implement the smallest LIMA-side live approval evidence/capture metadata slice.

The slice should define how LIMA validates sanitized approval evidence that may be captured by a shell, harness, or future approval provider without storing raw PINs, issuing approval tokens, executing actions, or wiring consumers.

Approval evidence families covered:

- approval challenge metadata
- approver actor/session/tenant/shell scope metadata
- approval intent and action-scope metadata
- approval factor result metadata without raw factors
- approval freshness and expiration metadata
- replay-prevention metadata
- denial, revoked, stale, expired, superseded, and blocked outcome metadata
- approval-to-audit/evidence linkage metadata
- destructive edit/delete/file-mutation approval evidence metadata

## Required Artifact Fields

Each approval evidence packet should provide metadata for:

- approval evidence id
- approval challenge id
- request id or Guardian decision id linkage
- tenant scope
- shell scope
- actor scope
- session scope
- approver actor ref
- approval intent scope
- action risk class
- action family
- approval outcome
- approval freshness status
- approval expiration metadata
- replay prevention metadata
- factor evidence summary
- capture source metadata
- audit evidence linkage
- proof-not-authority confirmation
- no raw PIN/token/secret/customer-data confirmation
- no approval-token issuance confirmation
- no execution-authority confirmation

## Required Distinction

V1-G19 must clearly separate:

- sanitized approval evidence metadata
- raw PIN, raw token, secret, credential, or customer data
- approval-token issuance
- action execution authority
- consumer integration

Approval evidence remains proof for a later Guardian decision or action gate. It is not broad runtime authority and must not execute any action by itself.

## Approved Files If Operator Says Yes

Candidate runtime files:

- `lima/guardian/v1_live_approval_evidence.py` (new)
- `lima/guardian/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G19_LIVE_APPROVAL_EVIDENCE_CAPTURE.md`
- `docs/V1_G19_LIVE_APPROVAL_EVIDENCE_CAPTURE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g19_live_approval_evidence_capture.json`
- `tests/test_v1_g19_live_approval_evidence_capture.py`

Any other file requires a new gate update before implementation.

## Allowed Behavior If Approved

V1-G19 may add only deterministic local non-executing approval evidence metadata validation.

Allowed if approved:

- validate approval evidence id and challenge id metadata
- validate request id or Guardian decision id linkage
- validate tenant, shell, actor, session, and approver scope metadata
- validate approval intent and action-scope metadata
- validate risk class and action family metadata
- normalize approval outcomes: `approved`, `denied`, `revoked`, `stale`, `expired`, `superseded`, `blocked`
- validate approval freshness and expiration metadata
- validate replay-prevention metadata
- validate factor evidence summary without raw factors
- validate capture source metadata
- validate audit/evidence linkage metadata
- validate proof-not-authority confirmation
- reject raw PINs, raw approval tokens, credentials, secrets, raw prompts, raw file contents, and customer data
- prove approval evidence metadata cannot issue approval tokens, grant execution authority, mutate files, call consumers, route providers/models, or invoke connectors/browser/network/device/robotics/physical-world behavior

## Explicitly Forbidden

V1-G19 must not add:

- raw PIN verification
- raw PIN persistence
- raw approval-token persistence
- approval-token issuance
- credential or secret access
- action execution
- file mutation execution
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- shell runtime wiring
- live provider/model routing
- tool execution
- HumanInput bridge activation
- connector behavior
- browser or network behavior
- scheduled task execution
- external sends
- device, robot, drone, IoT, humanoid, or physical-world behavior
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- final API freeze
- product-readiness or production-readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- fixture records `CANDIDATE_ONLY`
- required approval evidence fields are enforced
- request or GuardianDecision linkage is required
- tenant/shell/actor/session/approver scope is required
- approval intent scope is required
- action risk class and action family are required
- approval outcome statuses are normalized
- freshness, expiration, and replay prevention metadata are required
- factor evidence summary is required without raw factor values
- capture source metadata is required
- audit/evidence linkage is required
- proof-not-authority confirmation is enforced
- raw PINs, raw approval tokens, credentials, secrets, raw prompts, raw file contents, and customer data fail closed
- approval-token issuance claims fail closed
- execution-authority claims fail closed
- consumer repo mutation, consumer imports/calls, provider/model routing, connector/browser/network/device/robotics/physical-world claims fail closed

## Rollback Plan If Approved

Rollback must remove only:

- `lima/guardian/v1_live_approval_evidence.py`
- V1-G19 candidate exports added to `lima/guardian/__init__.py`
- V1-G19 docs/tests/fixtures

Rollback must not require consumer repo changes, shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, user file repair, or production deployment changes.

## Stop Conditions

Stop before implementation or revert implementation if any of these appear:

- file scope exceeds the approved V1-G19 files
- raw PIN verification or persistence is added
- approval-token issuance is added
- approval evidence metadata can grant execution authority
- action execution is added
- file mutation execution is added
- consumer repo work is required
- consumer code is imported
- consumer runtime calls are added
- consumer integration is added
- raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, credentials, or customer data can persist or emit
- live provider/model routing is added
- connector/browser/network/device/robotics/physical-world behavior is added
- scheduled task execution is added
- external sends are added
- final API freeze is claimed
- product readiness is claimed
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Implementation approved by this request: no.
- Operator approval recorded: no.
- Live approval evidence/capture behavior added: no.
- Raw PIN verification or persistence added: no.
- Approval-token issuance added: no.
- Execution authority added: no.
- Consumer repo mutation added: no.
- Consumer integration added: no.
- Consumer runtime calls added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- Connector/browser/network/file/device/robotics/physical-world behavior added: no.
- Final API freeze approved: no.
- Product readiness claimed: no.
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create branch `v1-g19-live-approval-evidence-capture` and implement only the LIMA-side live approval evidence/capture metadata slice. Do not verify raw PINs, issue approval tokens, execute actions, touch consumer repos, or implement consumer integration.
