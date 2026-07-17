# V1-G12 Durable Audit/Evidence Persistence Preflight Audit

Date: 2026-06-14
Branch: `v1-g12-durable-audit-evidence-persistence-approval-request`
Source branch: `audit-v1-g11-runtime-request-decision-gate`
Source commit: `5ff60a0536485cc3b87792c7ffb93c7e92a59520`
API status: `CANDIDATE_ONLY`

Preflight verdict: `approval_request_ready_runtime_not_approved`

This audit reviews whether the V1-G12 approval request is specific enough to govern a later durable audit/evidence persistence implementation decision.

## Evidence Reviewed

- `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_REQUEST_GATE.md`
- `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_CONTRACT.md`
- `docs/V1_G8_AUDIT_EVIDENCE_PERSISTENCE_THREAT_MODEL.md`
- `docs/V1_G9_PRODUCT_RELEASE_BOUNDARY_AUDIT.md`
- `docs/V1_G11_RUNTIME_REQUEST_DECISION_GATE_CLOSEOUT.md`
- `docs/audits/V1_G11_RUNTIME_REQUEST_DECISION_GATE_AUDIT.md`
- `lima/contracts/spine.py`
- `lima/contracts/storage.py`
- `lima/spine/__init__.py`
- `lima/persistence/__init__.py`

## Audit Results

Did V1-G11 pass independent audit before this request?

- Yes. `docs/audits/V1_G11_RUNTIME_REQUEST_DECISION_GATE_AUDIT.md` records verdict `PASS`.

Did the request name exact runtime files?

- Yes. It limits future runtime implementation to `lima/spine/v1_audit_evidence.py`, `lima/spine/__init__.py`, `lima/persistence/v1_audit_store.py`, and `lima/persistence/__init__.py`.

Did the request name exact docs/tests/fixtures?

- Yes. It names the future V1-G12 implementation doc, closeout, fixture, and test only.

Does this packet approve runtime implementation?

- No. It is a request/preflight packet only. Operator approval is not recorded.

Does the request preserve `CANDIDATE_ONLY` API status?

- Yes. API status remains `CANDIDATE_ONLY`.

Does the request keep audit/evidence records as proof instead of authority?

- Yes. It explicitly blocks audit records, redaction metadata, and stored evidence refs from authorizing execution.

Does the request preserve Guardian and approval linkage for consequential work?

- Yes. Consequential records require `decision_id`; destructive edit/delete requires approval evidence.

Does the request block raw sensitive persistence?

- Yes. Raw secrets, raw prompts, raw file contents, raw customer data, approval PINs, and approval tokens must fail closed.

Does the request block external side effects outside the audit store?

- Yes. It blocks arbitrary file mutation, external database writes, provider/model calls, tools, browser/network behavior, connectors, shell wiring, devices, robotics, and physical-world behavior.

Does the request include acceptance tests?

- Yes. Required tests cover required fields, redaction, destructive approval evidence, deterministic hashes, append-only local store behavior, scoped lookups, cross-tenant/cross-shell denial, and no authority leakage.

Does the request include rollback and stop conditions?

- Yes. Rollback is limited to V1-G12 files and stop conditions cover file-scope creep, raw sensitive persistence, audit-as-authority, missing decision/approval linkage, query leakage, external side effects, Sparkbot imports, runtime export cleanup, final freeze, and validation failure.

## Accepted For Operator Decision

- The request is specific enough for an operator to approve, revise, or pause.
- The request maps V1-G8/V1-G8A static persistence evidence to a narrow runtime implementation candidate.
- The request builds on V1-G11's local request/decision metadata without expanding provider/model, shell, connector, or physical-world behavior.
- The request preserves `CANDIDATE_ONLY` and keeps final API freeze unapproved.

## Not Accepted

Do not treat this preflight as proof of:

- runtime implementation approval
- durable audit/evidence persistence implementation
- live query/read authorization
- real redaction enforcement beyond proposed tests
- external database readiness
- live approval enforcement
- provider/model runtime routing
- shell runtime wiring
- runtime export cleanup approval
- final API freeze
- V1 product readiness
- production readiness

## Recommended Next Choices

Option `Approve-V1-G12`: Operator explicitly approves the exact V1-G12 scope in the approval request.

Option `Revise-V1-G12`: Operator asks for a narrower or different persistence request.

Option `Pause`: Keep LIMA at `CANDIDATE_ONLY` and do not start V1-G12 runtime implementation.

## Recommendation

Recommended: `Approve-V1-G12` only if the operator accepts the exact file scope, local persistence boundary, redaction requirements, validation requirements, rollback plan, and stop conditions.

Until that approval is recorded, the next safe action is operator decision or request revision, not implementation.
