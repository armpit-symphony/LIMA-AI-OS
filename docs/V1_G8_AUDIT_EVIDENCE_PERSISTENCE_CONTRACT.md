# V1-G8 Audit/Evidence Persistence Contract

Date: 2026-06-14
Branch: `v1-g8a-audit-evidence-persistence-contract-threat-model`
Source branch: `v1-g8-audit-evidence-persistence-request-gate`
Source commit: `b24eecec638db72a46a5c3eec9a9cc3b915380d1`
API status: `CANDIDATE_ONLY`

This contract defines the static V1-G8 audit/evidence persistence shape required before any future runtime persistence implementation can be proposed.

It does not implement storage, persistence, query APIs, database writes, runtime behavior, shell wiring, provider/model calls, live approval enforcement, real `GuardianDecision` authority, connector/file/browser/network/device/robotics behavior, haptic device behavior, shell execution, runtime export cleanup, final freeze, V1 product readiness, or production readiness.

## Contract Purpose

LIMA needs durable, redacted, queryable audit/evidence lineage before live approval, real `GuardianDecision`, provider/model routing, destructive edit/delete enforcement, and shell runtime wiring can safely move forward.

This static contract defines:

- record families
- required fields
- redaction and retention envelopes
- query contracts
- evidence hash/reference rules
- fail-closed cases
- shell evidence consumption boundaries
- runtime implementation blockers

## Existing Contract Anchors

This contract builds on:

- `docs/SPINE_AUDIT_LINEAGE_CONTRACT.md`
- `docs/REDACTION_PRIVACY_CONTRACT.md`
- `docs/CONTRACTS.md`
- `lima/contracts/spine.py`
- `lima/contracts/privacy.py`
- `lima/contracts/storage.py`

Existing fake Spine/Audit helpers remain test-only. They are not durable persistence.

## Core Rule

Audit evidence is proof, not authority.

No audit event, lineage record, redaction envelope, retention class, evidence ref, or query result may approve or authorize execution. `GuardianDecision` remains the authority boundary. Approval metadata remains operator evidence when policy requires approval.

## Required Record Families

### `AuditEventRecord`

Canonical immutable event record.

Required fields:

- `event_id`
- `lineage_id`
- `root_event_id`
- `parent_event_id`
- `event_type`
- `status`
- `created_at`
- `tenant_ref`
- `actor_ref`
- `shell_id`
- `session_ref`
- `input_id`
- `intent_id`
- `decision_id`
- `approval_id`
- `policy_ref`
- `provider_model_route_ref`
- `tool_pack_scope_ref`
- `action_type`
- `target_ref`
- `risk_class`
- `evidence_refs`
- `redaction_envelope_ref`
- `retention_envelope_ref`
- `result_ref`
- `error_ref`
- `record_hash`
- `supersedes_event_id`
- `metadata`

### `AuditLineageRecord`

Materialized lineage summary.

Required fields:

- `lineage_id`
- `root_event_id`
- `latest_event_id`
- `tenant_ref`
- `actor_ref`
- `shell_id`
- `input_id`
- `intent_id`
- `decision_id`
- `approval_id`
- `risk_class`
- `status`
- `created_at`
- `updated_at`
- `closed_at`
- `evidence_refs`
- `record_hash`
- `metadata`

### `EvidenceArtifactRef`

Reference to externalized evidence.

Required fields:

- `evidence_ref`
- `lineage_id`
- `event_id`
- `artifact_type`
- `storage_ref`
- `content_hash`
- `privacy_class`
- `redaction_class`
- `retention_class`
- `visibility_class`
- `created_at`
- `expires_at`
- `metadata`

The `storage_ref` is a reference only. It is not a storage implementation.

### `GuardianDecisionEvidenceRef`

Reference to decision evidence.

Required fields:

- `decision_id`
- `lineage_id`
- `event_id`
- `decision_status`
- `risk_class`
- `policy_ref`
- `constraints_ref`
- `evidence_refs`
- `record_hash`

### `ApprovalEvidenceRef`

Reference to operator approval evidence.

Required fields:

- `approval_id`
- `decision_id`
- `lineage_id`
- `approved_by_ref`
- `approval_method`
- `approval_level`
- `approval_status`
- `scope_ref`
- `expires_at`
- `revoked_at`
- `evidence_refs`
- `record_hash`

Raw PINs, approval tokens, hardware-key material, signed token secrets, or breakglass secrets are forbidden.

### `ProviderModelRouteEvidenceRef`

Reference to provider/model route posture.

Required fields:

- `route_ref`
- `lineage_id`
- `decision_id`
- `shell_id`
- `tool_pack_scope_ref`
- `provider_ref`
- `model_ref`
- `budget_ref`
- `privacy_ref`
- `policy_ref`
- `fallback_ref`
- `status`
- `evidence_refs`
- `record_hash`

### `ToolExposureEvidenceRef`

Reference to tool-pack/tool exposure posture.

Required fields:

- `exposure_ref`
- `lineage_id`
- `decision_id`
- `policy_decision_id`
- `shell_id`
- `requested_tool_pack`
- `allowed_tool_packs`
- `denied_tool_packs`
- `selected_tools`
- `risk_class`
- `evidence_refs`
- `record_hash`

### `ExecutionAttemptEvidenceRef`

Reference to a future execution attempt.

Required fields:

- `execution_id`
- `lineage_id`
- `decision_id`
- `approval_id` when required
- `event_id`
- `action_type`
- `target_ref`
- `tool_pack`
- `status`
- `result_ref`
- `error_ref`
- `evidence_refs`
- `record_hash`

This reference does not approve execution. Future runtime execution still needs explicit implementation approval.

### `ExportReviewRef` And `DeletionReviewRef`

References for audit export/delete governance.

Required fields:

- `review_ref`
- `lineage_id`
- `requested_by_ref`
- `decision_id`
- `approval_id`
- `scope_ref`
- `reason`
- `status`
- `created_at`
- `expires_at`
- `evidence_refs`
- `record_hash`

Audit export and deletion review cannot bypass retention, legal hold, tenant scope, or operator approval.

## Redaction And Retention Envelopes

Every persistent event or evidence ref must carry:

- `privacy_class`
- `redaction_class`
- `retention_class`
- `visibility_class`
- `contains_secret`
- `contains_biometric`
- `contains_safety_critical`
- `data_subject_ref` when applicable
- `content_refs`
- `redacted_summary`
- `retention_expires_at`

Default rules:

- Unknown privacy defaults to blocked/review, not public.
- Raw secrets are forbidden.
- Raw approval PINs/tokens are forbidden.
- Raw prompt/context is reference-only unless explicitly marked safe.
- File contents are referenced, not embedded.
- Customer data is private/confidential/restricted by default.
- Robot/device/safety data defaults safety-critical or biometric as applicable.

## Query Contract

Future query APIs must be scoped, redacted, and deny-by-default.

Required query keys:

- `lineage_id`
- `event_id`
- `root_event_id`
- `input_id`
- `intent_id`
- `decision_id`
- `approval_id`
- `tenant_ref`
- `actor_ref`
- `shell_id`
- `session_ref`
- `action_type`
- `target_ref`
- `risk_class`
- `status`
- `provider_model_route_ref`
- `tool_pack`
- `evidence_ref`
- `time_window`

Query rules:

- tenant scope is mandatory
- shell scope is mandatory
- operator/admin/security visibility must be enforced by future auth policy
- records return redacted views by default
- raw secrets never appear in query results
- cross-tenant query leakage fails closed
- missing retention or privacy metadata fails closed
- export/delete query flows require review refs

## Destructive Edit/Delete Evidence Rule

Any future destructive edit/delete event must carry:

- `decision_id`
- `approval_id`
- `ApprovalEvidenceRef`
- target reference
- action type
- risk class high or critical unless a stricter policy applies
- evidence refs
- result/error refs
- retention envelope
- redaction envelope

Without approval evidence, the event must be blocked or denied.

## Provider/Model Evidence Rule

Any future provider/model route event must carry:

- `decision_id`
- `ProviderModelRouteEvidenceRef`
- provider/model refs
- route status
- budget/cost ref
- privacy/redaction ref
- policy ref
- fallback ref when applicable
- audit evidence refs

Routes are evidence, not execution authority.

## Shell Consumption Boundary

Shells consume audit/evidence references and redacted summaries. Shells do not own the durable audit store.

Required shell boundaries:

- `Sparkbot_shell` may render state, haptic-intent, approval, blocked/deferred, and evidence refs.
- `Sparkbot` may render approval, Guardian, route, tool, memory, and spine/audit refs.
- `Arc-Bot-shell` may render task, approval queue, worker/supervisor, connector readiness, model-route posture, and evidence-panel refs.

Shell rendering must not imply LIMA runtime parity or execution authority.

## Static Positive Cases

V1-G8 accepts these positive static cases:

- low-risk preview lineage with reference-only content
- model-route planning lineage with route evidence ref
- destructive edit/delete blocked without approval evidence
- destructive edit/delete allowed only as future path with decision and approval evidence
- denied/blocked action lineage remains auditable
- haptic intent evidence remains shell-owned and non-device
- Arc office task evidence uses task/evidence refs
- export/delete request requires review ref

## Static Negative Cases

V1-G8 rejects:

- consequential event without `decision_id`
- destructive edit/delete without `approval_id`
- route evidence without provider/model route ref
- tool exposure without policy decision ref
- event without lineage ID
- event without tenant ref
- event without actor ref
- event without shell ID
- raw secret inline
- raw PIN/token inline
- raw prompt/context inline without redaction/reference envelope
- file contents inline
- unknown privacy class treated as safe
- cross-tenant query leakage
- export/delete without review ref
- connector/file/browser/network/device/robotics claim without Guardian/audit linkage

## Boundary Confirmation

- Docs/tests/fixtures-only: yes.
- Durable persistence implemented: no.
- Storage adapter added: no.
- Query API added: no.
- External database writes added: no.
- Runtime behavior added: no.
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
