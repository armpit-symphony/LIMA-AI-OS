# V1-G19 Live Approval Evidence Capture

Date: 2026-06-16
Branch: `v1-g19-live-approval-evidence-capture`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_live_approval_evidence_capture_slice`

V1-G19 implements the approved LIMA-side live approval evidence/capture metadata slice. It validates sanitized approval evidence metadata that may be captured by a shell, harness, or future approval provider and returns a deterministic proof record for later Guardian/audit review.

This implementation does not verify raw PINs, persist raw approval factors, issue approval tokens, execute actions, mutate files, touch consumer repositories, import consumer code, call consumer runtimes, wire consumers, route providers/models, activate HumanInput, invoke connectors, execute browser/network/file/device/robotics/physical-world behavior, run scheduled tasks, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G19_LIVE_APPROVAL_EVIDENCE_CAPTURE_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G19` template.

Approved implementation branch:

- `v1-g19-live-approval-evidence-capture`

Approved runtime scope:

- `live_approval_evidence_capture_metadata_slice`

## Runtime Files

- `lima/guardian/v1_live_approval_evidence.py`
- `lima/guardian/__init__.py`

## Runtime Symbols

- `V1LiveApprovalEvidenceError`
- `validate_v1_live_approval_evidence_capture`

## Behavior Added

V1-G19 adds one deterministic local approval evidence metadata validator:

- requires approval evidence id and challenge id metadata
- requires request id or Guardian decision id linkage
- requires tenant, shell, actor, session, and approver scope metadata
- requires approval intent and action-scope metadata
- requires action risk class and action family metadata
- normalizes `approved`, `denied`, `revoked`, `stale`, `expired`, `superseded`, and `blocked` outcomes
- requires approval freshness status
- requires approval expiration metadata
- requires replay-prevention metadata
- requires factor evidence summary without raw factor values
- requires capture source metadata
- requires audit/evidence linkage metadata
- requires proof-not-authority confirmation
- requires no raw PIN/token/secret/customer-data confirmation
- requires no approval-token issuance confirmation
- requires no execution-authority confirmation
- returns a deterministic `record_hash`
- keeps execution, side-effect, token issuance, raw PIN verification/persistence, file mutation, provider/model routing, consumer integration, connector/browser/network/device/robotics/physical-world, final freeze, and product readiness flags false

## Required Distinction

V1-G19 separates:

- sanitized approval evidence metadata: implemented as validation
- raw PIN/token/secret/customer-data handling: not accepted
- approval-token issuance: not approved and not implemented
- action execution authority: not approved and not implemented
- consumer integration: not approved and not implemented

## Fail-Closed Cases

The validator rejects:

- missing approval evidence metadata fields
- missing request or GuardianDecision linkage
- linkage metadata that claims authority
- unbound approval intent scope
- approval intent metadata that grants execution
- unsupported risk classes
- unsupported action families
- unsupported approval outcomes
- invalid freshness, expiration, or replay metadata
- raw factor values
- factor summaries that are not redacted
- untrusted capture source metadata
- consumer runtime invocation claims
- missing audit/evidence linkage
- audit/evidence metadata that claims authority
- missing proof-not-authority confirmation
- missing no raw PIN/token/secret/customer-data confirmation
- missing no approval-token issuance confirmation
- missing no execution-authority confirmation
- raw PINs, approval tokens, secrets, prompts, file contents, credentials, and customer data
- approval-token issuance claims
- execution-authority claims
- consumer repo mutation, consumer imports/calls, provider/model routing, connector/browser/network/device/robotics/physical-world claims

## Boundaries

- Runtime behavior added: yes, only the approved non-executing live approval evidence metadata validator.
- Raw PIN verification added: no.
- Raw PIN persistence added: no.
- Approval-token persistence added: no.
- Approval-token issuance added: no.
- Action execution added: no.
- File mutation execution added: no.
- Consumer repo mutation added: no.
- Consumer code import added: no.
- Consumer runtime calls added: no.
- Consumer integration added: no.
- Shell runtime wiring added: no.
- Provider/model routing added: no.
- Tool execution added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/file/device/robotics/physical-world behavior added: no.
- Scheduled task execution added: no.
- External sends added: no.
- External database writes added: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- Product readiness approved: no.

## Readiness Result

V1-G19 is ready for independent audit.

The next smallest safe step is a separate V1-G19 audit branch. Do not proceed to action execution, actual file mutation execution, consumer integration, shell wiring, provider/model routing, connector/browser/network authority, final API freeze, physical-world authority, or product-readiness claims from this implementation branch.
