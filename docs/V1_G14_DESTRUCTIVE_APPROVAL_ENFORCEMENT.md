# V1-G14 Destructive Approval Enforcement

Date: 2026-06-15
Branch: `v1-g14-destructive-approval-enforcement`
API status: `CANDIDATE_ONLY`

Implementation verdict: `complete_as_approved_candidate_runtime_slice`

V1-G14 implements the approved local destructive edit/delete approval-enforcement runtime slice. It validates sanitized approval evidence for already-reviewed V1-G11 destructive file-mutation requests and returns a redacted non-executing approval-enforcement record.

This implementation does not mutate files, execute tools, issue approval tokens, persist records, route providers/models, wire shells, activate HumanInput, invoke connectors, send external messages, or claim product readiness.

## Operator Decision

The operator decision was recorded in `docs/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G14` template.

Approved implementation branch:

- `v1-g14-destructive-approval-enforcement`

Approved runtime scope:

- `destructive_edit_delete_approval_enforcement_runtime_slice`

## Runtime Files

- `lima/guardian/v1_approval_enforcement.py`
- `lima/guardian/__init__.py`

## Runtime Symbols

- `V1ApprovalEnforcementError`
- `enforce_v1_destructive_approval`

## Behavior Added

V1-G14 adds one deterministic local approval-enforcement gate:

- accepts only V1-G11-style `ConsequentialActionRequest` and `GuardianDecision` metadata
- requires destructive file-mutation shape
- requires a V1-G11 decision with `NEEDS_OPERATOR_PIN`
- requires sanitized approval metadata with `approval_id`, `approval_evidence_ref`, `approving_actor_ref`, `approval_recorded_at`, `approval_scope`, `tenant_ref`, `shell_id`, `request_id`, `decision_id`, `actor_id`, `target_ref`, `approval_state`, `approval_freshness`, and `approval_replay_status`
- requires `approval_scope: destructive_edit_delete_file_mutation`
- requires `approval_state: granted`
- requires `approval_freshness: fresh`
- requires `approval_replay_status: not_replayed`
- requires `approval_evidence_ref` to appear in `evidence_refs`
- returns a redacted approval-enforcement record with deterministic `record_hash`
- keeps `execution_allowed`, `side_effects_allowed`, `approval_token_issued`, `provider_model_routed`, `shell_wired`, and `file_mutation_executed` false

## Fail-Closed Cases

The gate rejects:

- non-V1-G11 request/decision metadata
- non-destructive safe informational/planning/drafting requests
- non-file-mutation requests
- missing approval evidence
- missing approval ID
- missing approval evidence reference
- missing approving actor reference
- missing approval recorded timestamp
- missing or mismatched approval scope
- request/decision identity mismatch
- request, decision, actor, shell, target, tenant, or evidence mismatch
- expired approval state
- revoked approval state
- denied approval state
- superseded approval state
- stale approval freshness
- replayed approval evidence
- raw approval PINs
- raw approval tokens
- raw secrets
- raw prompts
- raw file contents
- raw customer data
- forged approval claims
- forged decision metadata
- provider/model routing claims
- tool execution claims
- browser/network/device/robotics/physical-world claims
- approval metadata as execution authority

## Boundaries

- Runtime behavior added: yes, only the approved non-executing approval-enforcement gate.
- File mutation behavior added: no.
- Approval-token issuance added: no.
- Raw PIN verification added: no.
- Persistence added: no.
- External database writes added: no.
- Provider/model routing added: no.
- Shell runtime wiring added: no.
- HumanInput bridge activated: no.
- Connector behavior added: no.
- Browser/network/device/robotics/physical-world behavior added: no.
- Consumer integration added: no.
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell code copied or imported: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- V1 product readiness approved: no.
- Production readiness approved: no.

## Readiness Result

V1-G14 is ready for independent audit.

The next smallest safe step is a separate V1-G14 audit branch. Do not proceed to consumer integration, shell wiring, provider/model routing, or product release work from this implementation branch.
