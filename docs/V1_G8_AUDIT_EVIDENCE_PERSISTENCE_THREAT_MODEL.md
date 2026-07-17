# V1-G8 Audit/Evidence Persistence Threat Model

Date: 2026-06-14
Branch: `v1-g8a-audit-evidence-persistence-contract-threat-model`
API status: `CANDIDATE_ONLY`

This threat model covers the static V1-G8 audit/evidence persistence contract.

It does not implement persistence, storage, query APIs, live auth, live approval enforcement, real `GuardianDecision`, provider/model routing, shell wiring, haptic device behavior, connector/file/browser/network/device/robotics behavior, or production behavior.

## Assets

Protected assets:

- audit events
- lineage records
- evidence artifact refs
- Guardian decision evidence
- approval evidence
- provider/model route evidence
- tool exposure evidence
- destructive edit/delete evidence
- export/delete review refs
- redaction and retention envelopes
- tenant/customer scope references
- shell/actor/session/trust references

## Trust Boundaries

Trust boundaries:

- shell UI to LIMA evidence reference boundary
- operator approval to audit evidence boundary
- Guardian decision to audit record boundary
- provider/model route to evidence reference boundary
- tool exposure to selected-tools evidence boundary
- future storage adapter to contract boundary
- future query/read API to visibility/redaction boundary
- export/delete review to retention/legal hold boundary

## Threats And Required Mitigations

### T1: Audit Record As Authorization

Threat: a shell or runtime treats an audit event as permission to execute.

Required mitigation:

- contract states audit evidence is proof, not authority
- future execution requires `GuardianDecision.decision_id`
- tests reject records that imply authorization from audit metadata alone

### T2: Missing Decision Linkage

Threat: consequential events are recorded without `decision_id`.

Required mitigation:

- consequential records require `decision_id`
- missing decision records are blocked/denied
- future tests cover model, tool, file, browser, network, device, robotics, shell execution, and destructive actions

### T3: Destructive Edit/Delete Approval Bypass

Threat: destructive edit/delete is recorded or executed without operator approval evidence.

Required mitigation:

- destructive edit/delete requires `approval_id` and `ApprovalEvidenceRef`
- missing approval evidence blocks the path
- approval scope must bind action type, target ref, shell, actor, risk, and expiry

### T4: Raw Secret Leakage

Threat: secrets, tokens, passwords, API keys, approval PINs, or signed token secrets are stored inline.

Required mitigation:

- raw secrets are forbidden
- use `secret_ref`, `approval_ref`, or evidence ref only
- static negative fixtures reject raw secret and raw approval token/PIN fields

### T5: Raw Customer Or Prompt Data Leakage

Threat: private customer data, prompt/context payloads, file contents, or connector data are stored inline.

Required mitigation:

- default to reference-only or summary-only
- require privacy/redaction/retention/visibility envelopes
- reject inline file contents and unredacted raw prompt/context

### T6: Cross-Tenant Query Leakage

Threat: query results return records outside tenant/customer scope.

Required mitigation:

- tenant/customer context is a required query scope
- cross-tenant query leakage fails closed
- future query APIs must return redacted scoped records only

### T7: Evidence Tampering Or Orphaning

Threat: records are modified, lineage links are lost, or evidence refs do not match stored artifacts.

Required mitigation:

- records carry hashes
- parent/root/lineage IDs are required
- supersession creates new events instead of hidden mutation
- evidence refs carry content hashes

### T8: Retention Or Deletion Abuse

Threat: audit/evidence records are deleted, exported, or hidden without review.

Required mitigation:

- export/delete requires `ExportReviewRef` or `DeletionReviewRef`
- retention class is mandatory
- legal hold and do-not-store rules override deletion shortcuts
- raw deletion behavior remains unimplemented until future approval

### T9: Provider/Model Route Evidence Loss

Threat: model routing happens without route evidence, budget/privacy policy, or fallback record.

Required mitigation:

- provider/model route events require `ProviderModelRouteEvidenceRef`
- include provider/model/budget/privacy/policy/fallback refs
- route evidence is not execution authority

### T10: Shell Over-Trust

Threat: shell rendering treats an evidence ref as live runtime parity or approval.

Required mitigation:

- shells consume redacted evidence refs only
- shell rendering remains shell-owned
- shell evidence does not imply execution authority
- haptic intent evidence remains non-device and shell-owned

### T11: Connector/File/Browser/Network/Device/Robotics Claim Without Guardian

Threat: physical or external behavior is claimed without Guardian decision and audit linkage.

Required mitigation:

- connector/file/browser/network/device/robotics/physical-world records require `decision_id`
- high/critical paths require approval when policy says so
- static tests reject claims without Guardian/audit linkage

## Threat Model Acceptance

V1-G8A is acceptable as static evidence if:

- every threat above has a contract mitigation
- every mitigation maps to fixture fields or static assertions
- no runtime behavior is added
- no storage adapter is added
- no query API is added
- no shell wiring is added
- no production readiness is claimed

## Remaining Runtime Risks

These remain open after V1-G8A:

- no durable storage implementation
- no live query/read authorization
- no real redaction enforcement
- no evidence hash verification runtime
- no live export/delete review workflow
- no real GuardianDecision runtime authority
- no live approval enforcement
- no provider/model runtime routing
- no shell runtime wiring
- no production readiness
