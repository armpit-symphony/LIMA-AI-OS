# V1-G8 Audit/Evidence Persistence Audit Criteria

Date: 2026-06-14
Branch: `v1-g8-audit-evidence-persistence-request-gate`
API status: `CANDIDATE_ONLY`

This document defines how LIMA will audit future V1-G8 audit/evidence persistence proof artifacts.

It is audit criteria only. It does not approve runtime behavior, storage implementation, database writes, shell wiring, provider/model calls, real `GuardianDecision` authority, approval enforcement, connector/file/browser/network/device/robotics behavior, haptic device behavior, runtime export cleanup, final freeze, V1 product readiness, or production readiness.

## Required Audit Questions

Future V1-G8 proof must answer:

- Did the proof define durable audit/evidence record families?
- Did the proof define the full lineage chain from `HumanInput` through result/evidence?
- Did the proof preserve `GuardianDecision.decision_id` for consequential action evidence?
- Did the proof preserve approval metadata for destructive edit/delete and other approval-required actions?
- Did the proof distinguish audit evidence from authorization?
- Did the proof distinguish redaction metadata from approval/enforcement?
- Did the proof define tenant, actor/operator, shell, and session/trust references?
- Did the proof define parent/root/lineage linkage?
- Did the proof define evidence refs and hashes for externalized content?
- Did the proof define privacy, redaction, retention, and visibility classes?
- Did the proof prevent raw secrets, raw approval tokens/PINs, raw customer data, raw file contents, and raw prompt/context payloads from appearing inline?
- Did the proof define query semantics by lineage, decision, approval, shell, actor, tenant, risk, status, time, provider/model route, tool pack, and evidence ref?
- Did the proof define cross-tenant query denial behavior?
- Did the proof define export/delete review refs and approval requirements?
- Did the proof preserve provider/model route evidence refs and budget/privacy/audit scope?
- Did the proof preserve shell-owned haptic rendering and avoid haptic device behavior claims?
- Did the proof reject raw natural-language-to-tool execution shortcuts?
- Did the proof reject connector/file/browser/network/device/robotics/physical-world behavior without Guardian and audit linkage?
- Did the proof include machine-readable fixture evidence?
- Did the proof include static tests for required positive and negative cases?
- Did the proof avoid runtime storage, persistence implementation, external DB writes, and shell wiring?
- Did the proof avoid runtime export cleanup, final freeze, V1 readiness, and production readiness claims?

## Static Acceptance

LIMA may accept a V1-G8 proof as static evidence when it proves:

- record family coverage
- lineage ID and parent/root linkage
- decision and approval linkage
- destructive edit/delete approval evidence linkage
- privacy/redaction/retention/visibility requirements
- reference-only handling for sensitive content
- query-scope requirements
- cross-tenant denial
- export/delete review requirements
- provider/model route evidence linkage
- shell evidence consumption boundaries
- required negative cases fail closed
- no runtime persistence behavior is added

Static acceptance is not durable runtime persistence.

## Required Positive Cases

Static fixtures should include at least:

- low-risk preview lineage
- model-route planning lineage
- approval-required destructive edit/delete lineage
- denied/blocked action lineage
- provider/model route evidence linkage
- shell haptic-intent evidence reference
- Arc-style office task evidence reference
- audit export review request
- audit deletion review request

## Required Negative Cases

Static fixtures should reject or mark blocked:

- consequential record without `decision_id`
- destructive edit/delete record without approval metadata
- route record without provider/model route evidence ref
- tool exposure without policy decision ref
- result event without lineage ID
- record without tenant/customer context
- record without actor/operator ref
- record without shell ID
- raw secret inline
- raw approval token/PIN inline
- raw prompt/context inline without reference/redaction
- file contents inline instead of referenced
- unknown privacy class treated as safe
- cross-tenant query leakage
- export/delete without review ref
- connector/file/browser/network/device/robotics claim without Guardian/audit linkage

## Rejection Conditions

Return or reject a V1-G8 proof if it:

- claims runtime persistence from static fixtures
- claims production audit readiness
- adds database writes or external storage behavior without approval
- omits decision/approval linkage for consequential actions
- omits destructive edit/delete operator approval evidence
- treats audit events as authorization
- stores raw secrets inline
- allows cross-tenant query leakage
- omits retention/export/delete posture
- omits provider/model route evidence refs
- omits shell consumption boundaries
- requires unapproved runtime export cleanup or final freeze

## Consolidated V1 Rule

V1-G8 cannot make LIMA V1-ready by itself. After V1-G8 static evidence is complete, LIMA still needs a V1-G9 product release boundary audit and any separately approved runtime implementation gates before production readiness can be claimed.
