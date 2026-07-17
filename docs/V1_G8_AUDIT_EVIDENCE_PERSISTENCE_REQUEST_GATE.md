# V1-G8 Audit/Evidence Persistence Request Gate

Date: 2026-06-14
Branch: `v1-g8-audit-evidence-persistence-request-gate`
Source branch: `v1-g7-first-shell-integration-proof-closeout`
Source commit: `ea5122c89c8cf9953a74d4829227102f3e07aea8`
API status: `CANDIDATE_ONLY`

This document opens the V1-G8 request gate for durable audit/evidence persistence.

It is a request/design gate only. It does not implement storage, persistence, runtime behavior, shell wiring, live approval enforcement, real `GuardianDecision` authority, provider/model routing, connector behavior, file/browser/network/device/robotics behavior, haptic device behavior, shell execution, runtime export cleanup, final freeze, V1 product readiness, or production readiness.

## Why V1-G8 Exists

V1-G1 through V1-G7 provide static proof that LIMA has a V1 target, typed bridge shape, destructive edit/delete approval contract, future `GuardianDecision`/approval path design, provider/model routing contract, haptic intent metadata contract, and first-shell static integration evidence.

The next blocker is durable evidence lineage. Live approval, real `GuardianDecision`, provider/model routing, destructive edit/delete enforcement, shell runtime wiring, and product release readiness all need queryable proof of what happened, who approved it, which policy and shell scope applied, which evidence was referenced, and what result was recorded.

V1-G8 defines the request gate for that proof without adding persistence implementation.

## Existing Static Evidence

Reviewed LIMA evidence:

- `docs/SPINE_AUDIT_LINEAGE_CONTRACT.md`
- `docs/REDACTION_PRIVACY_CONTRACT.md`
- `docs/CONTRACTS.md`
- `lima/contracts/spine.py`
- `lima/contracts/privacy.py`
- `lima/contracts/storage.py`
- `lima/guardian/spine_fakes.py`
- `tests/test_guardian_fake_pipeline.py`
- `tests/test_humaninput_fake_pipeline_bridge.py`
- `tests/test_v1_g7_first_shell_integration_proof_closeout.py`

These artifacts define lineage, privacy/redaction, reference-based evidence, storage interfaces, fake in-memory audit recorders for tests, and V1 first-shell evidence. They do not prove durable audit persistence.

## Request Target

The future V1-G8 persistence proof must show that consequential LIMA actions can produce durable, redacted, queryable evidence lineage.

The proof must preserve this chain:

```text
HumanInput
  -> IntentEnvelope
  -> GuardianDecision
  -> ApprovalMetadata when required
  -> ToolPackScope / PolicyDecision / ProviderModelRouteDecision when applicable
  -> planned model/tool/driver/file/browser/network/device/robotics/shell event
  -> result or blocked/denied/deferred event
  -> SpineEvent
  -> AuditLineageRecord
  -> EvidenceArtifactRef
```

No future action may claim durable execution readiness unless the relevant event lineage can be reconstructed by ID and inspected without exposing raw secrets.

## Required Future Persistence Record Families

The future V1-G8 contract must define, at minimum:

- `AuditEventRecord`
- `AuditLineageRecord`
- `EvidenceArtifactRef`
- `GuardianDecisionEvidenceRef`
- `ApprovalEvidenceRef`
- `PolicyDecisionEvidenceRef`
- `ProviderModelRouteEvidenceRef`
- `ToolExposureEvidenceRef`
- `ExecutionAttemptEvidenceRef`
- `ResultEvidenceRef`
- `RedactionEnvelope`
- `RetentionEnvelope`
- `ExportReviewRef`
- `DeletionReviewRef`

These are contract names for the request gate. They are not implemented here.

## Minimum Durable Fields

Future durable audit/evidence records must carry:

- stable record ID
- lineage ID
- parent/root event references
- tenant/customer context reference
- actor/operator reference
- shell ID
- session/trust reference when available
- input ID
- intent ID
- `GuardianDecision.decision_id` when consequential
- approval ID when policy requires approval
- policy/version references
- provider/model route reference when a model route is used
- tool-pack/scope reference when tools are exposed
- action type
- target reference
- risk class
- status
- timestamp
- evidence refs
- redaction/privacy/retention/visibility classes
- content hash or evidence hash when content is externalized
- result/error refs
- immutable audit metadata

## Required Query Capabilities

Future persistence must support query by:

- lineage ID
- root event ID
- event ID
- input ID
- intent ID
- decision ID
- approval ID
- actor/operator reference
- shell ID
- tenant/customer context reference
- action type
- target reference
- risk class
- status
- provider/model route reference
- tool pack
- evidence ref
- time window

Queries must return redacted records by default and must not reveal raw secrets, credentials, private file contents, raw customer data, raw prompt/context payloads, or raw approval tokens/PINs.

## Required Negative Cases

Future V1-G8 static tests must reject or fail closed when:

- consequential event lacks `decision_id`
- destructive edit/delete event lacks approval metadata
- high/critical event lacks risk class
- event lacks tenant/customer context
- event lacks actor/operator reference
- event lacks shell ID
- event lacks lineage ID
- event loses parent/root linkage
- evidence ref is missing for consequential result
- raw secret appears inline
- raw approval token or PIN appears inline
- raw prompt/context appears inline without approved reference/redaction envelope
- file contents are embedded instead of referenced
- provider/model route lacks policy/route evidence ref
- connector/file/browser/network/device/robotics event claims execution without Guardian decision
- deletion/export of audit evidence lacks approval/review ref
- retention class is missing
- unknown privacy class is treated as safe
- cross-tenant query returns records outside scope

## Required Shell Relevance

The V1-G8 proof must preserve first-shell needs:

- `Sparkbot_shell` needs shell-state, haptic-intent, approval, and blocked/deferred evidence refs.
- `Sparkbot` needs approval, Guardian, provider/model route, tool, memory, and audit/spine evidence refs.
- `Arc-Bot-shell` needs task, approval queue, worker/supervisor, connector readiness, model-route posture, and evidence panel refs.

Shells must consume evidence references, not raw audit stores. LIMA owns the future persistence contract; shells own rendering.

## Request Acceptance Criteria

The future V1-G8 proof can be accepted only if it:

- keeps API status `CANDIDATE_ONLY` until a later release gate
- defines durable audit/evidence record shapes
- defines redaction/privacy/retention/visibility requirements
- defines query semantics without raw secret leakage
- preserves `GuardianDecision` and approval linkage for consequential actions
- preserves destructive edit/delete operator-approval evidence
- preserves provider/model route evidence refs
- preserves shell-owned haptic rendering boundary
- rejects raw natural-language-to-tool execution shortcuts
- rejects unsafe connector/file/browser/network/device/robotics/physical-world claims without Guardian and audit lineage
- includes fixture evidence and static tests
- does not add runtime storage, persistence implementation, external database writes, shell wiring, or production claims

## Request Rejection Criteria

LIMA should reject a V1-G8 proof if it:

- claims durable persistence without storage contract evidence
- stores raw secrets or approval tokens inline
- lets destructive edit/delete bypass operator approval evidence
- treats audit records as authorization
- treats redaction metadata as approval
- omits `GuardianDecision` linkage for consequential action
- omits tenant/shell/actor scope
- allows cross-tenant query leakage
- claims provider/model routing without route evidence refs and budget/privacy/audit scope
- claims connector/file/browser/network/device/robotics/physical-world behavior without Guardian and audit linkage
- approves runtime export cleanup or final freeze
- claims V1 product readiness or production readiness from static evidence

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Runtime behavior added: no.
- Durable persistence added: no.
- Storage adapter added: no.
- External database writes added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Runtime exports changed: no.
- Shell wiring added: no.
- Provider/model calls added: no.
- Runtime `GuardianDecision` added: no.
- Approval enforcement added: no.
- Haptic device behavior added: no.
- Physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.

## Recommended Next Step

Create the V1-G8 static audit/evidence persistence contract and threat model, including fixtures and static tests for the required negative cases above. Keep the next lane docs/tests/fixtures-only unless a later explicit implementation gate approves runtime persistence.
