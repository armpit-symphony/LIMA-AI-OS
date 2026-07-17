# V1-G12 Durable Audit/Evidence Persistence Audit

Date: 2026-06-14
Audit branch: `audit-v1-g12-durable-audit-evidence-persistence`
Audited implementation branch: `v1-g12-durable-audit-evidence-persistence`
Audited implementation commit: `457b654a50e100ef7c000de25bb6d2c7493b9fc6`
API status: `CANDIDATE_ONLY`

## Verdict

Verdict: `PASS WITH WARNINGS`

The V1-G12 durable audit/evidence persistence implementation is acceptable as the approved narrow runtime slice. It is local, deterministic, redacted, append-only through an explicit local audit-store path, scoped by tenant and shell for reads, and non-authorizing.

This audit adds no runtime behavior and does not approve any next runtime lane by itself.

## Files Audited

- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_OPERATOR_DECISION_PACKET.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md`
- `lima/spine/v1_audit_evidence.py`
- `lima/spine/__init__.py`
- `lima/persistence/v1_audit_store.py`
- `lima/persistence/__init__.py`
- `tests/fixtures/runtime_extraction/v1_g12_durable_audit_evidence_persistence.json`
- `tests/test_v1_g12_durable_audit_evidence_persistence.py`

## Scope Audit

Implementation diff from `f15261de86869bf68d555ed75f88785b06926a7c` to `457b654a50e100ef7c000de25bb6d2c7493b9fc6` changed:

- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_OPERATOR_DECISION_PACKET.md`
- `lima/persistence/__init__.py`
- `lima/persistence/v1_audit_store.py`
- `lima/spine/__init__.py`
- `lima/spine/v1_audit_evidence.py`
- `tests/fixtures/runtime_extraction/v1_g12_durable_audit_evidence_persistence.json`
- `tests/test_v1_g12_durable_audit_evidence_persistence.py`

Runtime implementation files stayed within the approved V1-G12 runtime map:

- `lima/spine/v1_audit_evidence.py`
- `lima/spine/__init__.py`
- `lima/persistence/v1_audit_store.py`
- `lima/persistence/__init__.py`

The operator decision packet changed because the operator explicitly instructed LIMA to record `Approve-V1-G12` before implementation. That change is non-runtime decision evidence, but it is still recorded as a warning because the packet is outside the implementation file map listed under "If `Approve-V1-G12` Is Recorded."

Result: pass with warning.

## Operator Decision Audit

`docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_OPERATOR_DECISION_PACKET.md` records:

- Recorded choice: `Approve-V1-G12`
- Recorded approval wording: exact required approval wording from the packet
- Approved implementation branch: `v1-g12-durable-audit-evidence-persistence`
- Runtime implementation approved: yes

Result: pass.

## Audit/Evidence Builder Audit

`build_v1_audit_event_record(request, decision, metadata)` in `lima/spine/v1_audit_evidence.py`:

- accepts only `ConsequentialActionRequest`, matching `GuardianDecision`, and redacted metadata
- requires V1-G11 source runtime metadata on both request and decision
- requires non-executing decision constraints
- requires tenant ref, actor ref, shell ID, lineage ID, event ID, request ID, decision ID, risk class, evidence refs, redaction metadata, and redacted summary
- rejects raw secrets, approval PINs, approval tokens, prompts, file contents, customer data, and provider credentials
- rejects execution, side-effect, provider/model, shell wiring, HumanInput bridge, connector, browser, network, device, robotics, and physical-world authority claims
- requires destructive file operations to carry `approval_id` and `approval_evidence_ref`
- requires approval evidence refs to appear in `evidence_refs`
- emits deterministic record hashes over sanitized record content
- emits proof-not-authority flags with execution and approval-token fields false

Result: pass.

## Lineage Builder Audit

`build_v1_audit_lineage_record(event_record)`:

- accepts only validated `v1_audit_event` records
- preserves tenant, actor, shell, lineage, event, input, intent, decision, approval, risk, privacy, redaction, retention, visibility, and evidence refs
- emits deterministic record hashes
- keeps `audit_record_is_authority`, `execution_allowed`, and `approval_token_issued` false

Result: pass.

## Local Audit Store Audit

`V1LocalAuditStore` in `lima/persistence/v1_audit_store.py`:

- requires an explicit caller-provided local store directory
- writes only `v1_audit_records.jsonl` under that directory
- validates records before appending
- rejects duplicate append-only record keys
- supports lookup by event ID, lineage ID, and decision ID
- requires tenant and shell scope on every lookup
- fails closed on cross-tenant or cross-shell lookup attempts
- returns redacted records and non-authorizing write acknowledgements only
- does not use external databases, migrations, queues, workers, daemons, subprocesses, threads, connectors, or network behavior

Result: pass.

## Behavior Audit

| Required behavior | Audit result |
| --- | --- |
| Safe reviewed V1 request/decision metadata creates redacted audit event | Pass. Covered by tests and builder validation. |
| Missing lineage ID fails closed | Pass. Builder requires lineage from metadata or decision linkage. |
| Missing event ID fails closed | Pass. Builder requires `event_id`. |
| Missing tenant ref fails closed | Pass. Builder requires `tenant_ref`. |
| Missing actor ref fails closed | Pass. Builder requires `actor_ref`. |
| Missing shell ID fails closed | Pass. Decision/request shell ID is required and must match. |
| Missing decision ID fails closed | Pass. Decision ID is required. |
| Destructive edit/delete requires approval evidence | Pass. File-operation destructive records require `approval_id` and `approval_evidence_ref`. |
| Raw secrets, PINs, tokens, prompts, file contents, and customer data fail closed | Pass. Sensitive keys and known raw value markers are rejected recursively. |
| Unknown privacy class fails closed | Pass. Privacy class must be one of the allowed classes. |
| Record hashes are deterministic | Pass. Hash is built from sorted sanitized JSON. |
| Append-only local store writes and reads redacted records | Pass. Store appends JSONL and tests read back event/lineage records. |
| Lookup by event, lineage, and decision respects tenant/shell scope | Pass. Every lookup requires tenant and shell. |
| Cross-tenant or cross-shell lookup fails closed | Pass. Scoped mismatch raises `V1AuditStoreError`. |
| Records do not authorize execution or emit approval tokens | Pass. Records and acknowledgements set authority and token fields false. |
| Provider/model/tool/browser/network/device/robotics claims remain blocked | Pass. Future-policy evidence can be persisted only as denied/non-executing evidence, and execution claims are rejected. |

## Boundary Audit

| Boundary | Audit result |
| --- | --- |
| Consumer repos touched | No. |
| Sparkbot touched | No. |
| Sparkbot_shell touched | No. |
| Arc-Bot-shell touched | No. |
| LIMA Robo OS touched | No. |
| LIMA Office touched | No. |
| Provider/model routing added | No. |
| Provider/model calls added | No. |
| Tool execution added | No. |
| Shell runtime wiring added | No. |
| HumanInput bridge activated | No. |
| Connector behavior added | No. |
| Browser/file/network/device/robotics/physical-world behavior added | No. |
| External database writes added | No. |
| Migrations added | No. |
| Queues/workers/daemons/subprocesses/threads added | No. |
| Raw sensitive content persistence allowed | No. |
| Audit metadata becomes execution authority | No. |
| Approval tokens or PINs emitted | No. |
| Product readiness claimed | No. |
| Final API freeze claimed | No. |

## Test Evidence Reviewed

`tests/test_v1_g12_durable_audit_evidence_persistence.py` covers:

- approved-scope fixture metadata
- redacted non-authorizing event construction
- deterministic record hashes
- required field fail-closed cases
- missing shell and decision fail-closed cases
- destructive edit/delete approval evidence requirements
- raw secret, PIN, token, prompt, file content, and customer data rejection
- unknown privacy class rejection
- forged authority rejection
- future-policy denial evidence
- redacted non-authorizing lineage construction
- append-only store write/read behavior
- duplicate record rejection
- cross-tenant and cross-shell lookup denial
- absence of sensitive values in records and acknowledgements

The fixture records the same forbidden boundaries under `forbidden_behavior`.

## Warnings

- The implementation commit updated `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_OPERATOR_DECISION_PACKET.md` in addition to the implementation file map. This was operator-directed decision recording and did not add runtime behavior, but it is outside the implementation file list in the packet's approved-file section.
- `V1LocalAuditStore` is a local explicit JSONL store, not an external database, retention worker, export/delete workflow, or production audit service.
- Some safe V1-G11 decisions can carry decision status `approved`; V1-G12 preserves that status as evidence only. Downstream code must continue to rely on Guardian execution gates, not audit records, for authority.

## Recommended Next Lane

If this audit is accepted, prepare a separate docs/tests/fixtures-only V1-G13 readiness-gap refresh and next-lane decision gate.

The refresh should update post-V1-G12 V1 readiness evidence and choose the next narrow blocker explicitly before any provider/model routing, shell wiring, HumanInput bridge activation, live approval enforcement, external database persistence, runtime export cleanup, final freeze, or product-readiness work.
