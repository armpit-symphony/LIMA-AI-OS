# V1-G12 Durable Audit/Evidence Persistence

Date: 2026-06-14
Branch: `v1-g12-durable-audit-evidence-persistence`
Operator decision: `Approve-V1-G12`
API status: `CANDIDATE_ONLY`

This document records the approved V1-G12 runtime slice. The slice adds deterministic, local, redacted audit/evidence record construction and an explicit local append-only audit store. It does not add provider/model routing, shell runtime wiring, HumanInput bridge activation, connector behavior, external database writes, migrations, queues, workers, daemons, subprocesses, threads, browser/file/network/device/robotics/physical-world behavior, runtime export cleanup, final API freeze, or product readiness.

## Approved Scope

Runtime files:

- `lima/spine/v1_audit_evidence.py`
- `lima/spine/__init__.py`
- `lima/persistence/v1_audit_store.py`
- `lima/persistence/__init__.py`

Docs/tests/fixtures:

- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g12_durable_audit_evidence_persistence.json`
- `tests/test_v1_g12_durable_audit_evidence_persistence.py`

The operator decision was recorded in `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_OPERATOR_DECISION_PACKET.md` using the exact `Approve-V1-G12` template.

## Runtime Symbols

- `V1AuditEvidenceError`
- `build_v1_audit_event_record`
- `build_v1_audit_lineage_record`
- `V1AuditStoreError`
- `V1LocalAuditStore`

## Behavior Added

`build_v1_audit_event_record` accepts only a reviewed V1-G11 `ConsequentialActionRequest`, its matching non-executing `GuardianDecision`, and redacted metadata. It builds a redacted `v1_audit_event` dictionary with:

- tenant, actor, shell, event, lineage, request, input, intent, and decision linkage
- required privacy, redaction, retention, and visibility classes
- evidence refs and redacted summary
- deterministic `record_hash`
- proof-not-authority flags that keep execution, side effects, provider/model routing, shell wiring, and approval-token issuance false

`build_v1_audit_lineage_record` accepts a validated event record and builds a redacted `v1_audit_lineage` dictionary with deterministic hash and the same proof-not-authority boundaries.

`V1LocalAuditStore` writes validated records as append-only JSON Lines under an explicit caller-provided local audit-store directory. It provides scoped lookup by event ID, lineage ID, and decision ID. Every lookup requires tenant and shell scope, and cross-tenant or cross-shell matches fail closed.

## Fail-Closed Rules

The slice rejects:

- missing lineage ID
- missing event ID
- missing tenant ref
- missing actor ref
- missing shell ID
- missing decision ID
- destructive edit/delete file records without `approval_id`
- destructive edit/delete file records without `approval_evidence_ref`
- approval evidence refs not present in `evidence_refs`
- raw secret values
- raw approval PINs
- raw approval tokens
- raw prompts
- raw file contents
- raw customer data
- unknown privacy class
- forged execution authority
- provider/model, tool, browser, network, device, robotics, or physical-world execution claims
- duplicate append-only record keys
- cross-tenant or cross-shell lookup attempts

## Store Boundary

The local audit store writes only to:

- `<explicit_store_dir>/v1_audit_records.jsonl`

The store does not create migrations, use an external database, start background workers, create queues, spawn subprocesses, or open network connections.

## Authority Boundary

Audit/evidence records are proof, not execution authority.

The records and store acknowledgements do not:

- approve execution
- issue approval tokens
- mark mutation instructions as approved
- route providers or models
- wire shells
- activate HumanInput
- invoke connectors
- invoke browser, file, network, device, robotics, or physical-world actions

## Readiness Result

V1-G12 is complete as a narrow candidate runtime slice for local durable audit/evidence persistence. It remains `CANDIDATE_ONLY` and does not pass the V1 product release boundary by itself.
