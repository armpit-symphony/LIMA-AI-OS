# V1-G12 Durable Audit/Evidence Persistence Work Order

Date: 2026-06-14
Branch: `v1-g12-durable-audit-evidence-persistence-approval-request`
Source branch: `v1-g12-durable-audit-evidence-persistence-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_runtime`

This is a work order only. It does not record operator approval, does not approve runtime implementation, and does not change `lima/`.

## Approval Dependency

V1-G12 implementation may start only after the operator explicitly approves:

`docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_APPROVAL_REQUEST.md`

Until that approval is recorded, the allowed work remains docs/tests/fixtures-only.

## Existing Shapes To Reuse

The implementation must reuse or remain compatible with:

- `lima.contracts.guardian.ConsequentialActionRequest`
- `lima.contracts.guardian.GuardianDecision`
- `lima.contracts.spine.SpineEvent`
- `lima.contracts.storage.StorageProtocol`
- V1-G11 request metadata from `build_v1_runtime_request`
- V1-G11 decision metadata from `review_v1_runtime_request`

Do not create a parallel authorization model. Audit evidence is proof, not authority.

## Implementation Sequence If Approved

1. Add `lima/spine/v1_audit_evidence.py`.
2. In that file, add deterministic builders/validators for redacted audit event and lineage records from reviewed V1 request/decision metadata.
3. The builder must reject missing lineage, event, tenant, actor, shell, decision, privacy, redaction, retention, or evidence metadata where required.
4. The builder must reject raw secrets, raw approval PINs/tokens, raw prompts, raw file contents, and raw customer data.
5. Add `lima/persistence/v1_audit_store.py`.
6. In that file, add a narrow append-only local audit store that writes sanitized records only to an explicit audit store path.
7. Add minimal scoped lookup by event ID, lineage ID, and decision ID with tenant/shell scope.
8. Add candidate exports only in `lima/spine/__init__.py` and `lima/persistence/__init__.py`.
9. Add `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE.md`.
10. Add `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md`.
11. Add `tests/fixtures/runtime_extraction/v1_g12_durable_audit_evidence_persistence.json`.
12. Add `tests/test_v1_g12_durable_audit_evidence_persistence.py`.

## Expected Candidate Runtime Symbols If Approved

The implementation should expose only candidate V1 symbols such as:

- `V1AuditEvidenceError`
- `build_v1_audit_event_record`
- `build_v1_audit_lineage_record`
- `V1AuditStoreError`
- `V1LocalAuditStore`

The exact symbol names may change during implementation only if the V1-G12 implementation doc records the reason and tests lock the exported surface.

## Required Rules If Approved

- audit records are proof, not authority
- records must be redacted before storage
- consequential records require `decision_id`
- destructive edit/delete records require `approval_id` and approval evidence ref
- tenant ref, actor ref, shell ID, lineage ID, event ID, action type, status, risk class, redaction class, retention class, and evidence refs are required
- unknown privacy class fails closed
- raw secrets, approval PINs/tokens, raw prompts, raw file contents, and raw customer data fail closed
- local store writes are append-only and scoped to the explicit audit store path
- lookups require tenant/shell scope and return redacted records only
- cross-tenant and cross-shell query leakage fails closed

## Required Output Boundaries If Approved

The runtime slice may output:

- redacted audit event dictionaries
- redacted lineage dictionaries
- evidence references
- deterministic record hashes
- local audit-store write acknowledgements
- scoped redacted query results

The runtime slice must not output:

- raw secrets
- raw prompts
- raw file contents
- raw customer records
- approval PINs
- approval tokens
- provider credentials
- executable commands
- mutation instructions marked approved

## Required Validation If Approved

Run at minimum:

- `cmd /c "python3 --version || python --version"`
- `cmd /c "python3 -m compileall lima || python -m compileall lima"`
- focused V1-G12 tests
- `cmd /c "python3 -m pytest -q tests -p no:cacheprovider || python -m pytest -q tests -p no:cacheprovider"`
- `git diff --check`
- `git diff --cached --check` before commit

## Rollback If Approved

Rollback must be possible by removing only:

- `lima/spine/v1_audit_evidence.py`
- `lima/persistence/v1_audit_store.py`
- V1-G12 candidate exports in `lima/spine/__init__.py`
- V1-G12 candidate exports in `lima/persistence/__init__.py`
- V1-G12 docs/tests/fixtures

Rollback must not require shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, or production deployment changes.

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G12 file map
- raw sensitive content persistence
- audit metadata as execution authority
- consequential records without `decision_id`
- destructive edit/delete records without approval evidence
- external database writes or migrations
- provider/model calls or routing
- tool execution
- arbitrary file/browser/network/connector behavior
- device, robotics, IoT, drone, robot, humanoid, or physical-world behavior
- live auth/trust lookup or HumanInput bridge activation
- shell runtime wiring
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy
- approval-token issuance
- queues, workers, daemons, subprocesses, or threads
- runtime export cleanup
- final API freeze
- V1 product-readiness or production-readiness claims

## Boundary Confirmation

- Work order only: yes.
- Operator approval recorded: no.
- Runtime implementation approved by this work order: no.
- Runtime behavior added: no.
- Durable persistence added: no.
- Storage adapter added: no.
- Query API added: no.
- External database writes added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Shell repositories changed: no.
- Sparkbot code copied or imported: no.
- Provider/model calls added: no.
- Provider/model routing added: no.
- Runtime `GuardianDecision` authority expanded: no.
- Approval enforcement added: no.
- Haptic device behavior added: no.
- Physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final freeze approved: no.

## Recommended Next Step

Operator decision on the exact V1-G12 approval request.

If approved, create the V1-G12 implementation branch and execute this work order exactly. If not approved, keep LIMA at `CANDIDATE_ONLY` or revise the request.
