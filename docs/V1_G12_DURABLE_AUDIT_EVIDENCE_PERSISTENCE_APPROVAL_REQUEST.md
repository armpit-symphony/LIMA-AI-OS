# V1-G12 Durable Audit/Evidence Persistence Approval Request

Date: 2026-06-14
Branch: `v1-g12-durable-audit-evidence-persistence-approval-request`
Source branch: `audit-v1-g11-runtime-request-decision-gate`
Source commit: `5ff60a0536485cc3b87792c7ffb93c7e92a59520`
API status: `CANDIDATE_ONLY`

Request verdict: `ready_for_operator_decision_not_approved`

This is an approval request only. It does not approve runtime implementation, change runtime behavior, modify `lima/`, add storage, write files, create query APIs, or claim product readiness.

## Exact Approval Question

Do you explicitly approve V1-G12 implementation of the durable audit/evidence persistence runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

Approval must be explicit before implementation begins. The V1-G11 audit `PASS`, prior V1-G8 static contract evidence, general V1 product direction, or this request packet do not count as implementation approval.

## Proposed V1-G12 Objective

Implement the smallest local runtime slice that:

- accepts only already-reviewed V1 request and GuardianDecision metadata
- validates required audit lineage fields before persistence
- creates redacted `AuditEventRecord` and `AuditLineageRecord`-shaped dictionaries
- stores those redacted records through a local explicit audit store
- supports minimal scoped lookup by record ID, lineage ID, and decision ID
- keeps audit/evidence records as proof, not authorization
- never executes tools, files outside the explicit audit store, connectors, browsers, networks, devices, robots, models, or physical-world actions

## Approved Files If Operator Says Yes

Runtime files:

- `lima/spine/v1_audit_evidence.py` (new)
- `lima/spine/__init__.py` (candidate export only)
- `lima/persistence/v1_audit_store.py` (new)
- `lima/persistence/__init__.py` (candidate export only)

Docs/tests/fixtures:

- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g12_durable_audit_evidence_persistence.json`
- `tests/test_v1_g12_durable_audit_evidence_persistence.py`

Any other file requires a new gate update before implementation.

## Allowed Runtime Behavior If Approved

V1-G12 may add only deterministic, local, audit-persistence behavior that proves:

- only V1-G11-style request/decision metadata can enter the persistence slice
- missing lineage ID fails closed
- missing event ID fails closed
- missing tenant reference fails closed
- missing actor reference fails closed
- missing shell ID fails closed
- consequential records without `decision_id` fail closed
- destructive edit/delete records without approval evidence fail closed
- raw secrets, raw approval PINs, raw approval tokens, raw prompts, raw file contents, and raw customer data fail closed
- audit records are proof, not authorization
- record hashes are deterministic over sanitized content
- records are append-only through the explicit local audit store
- minimal local lookup returns redacted records only
- query scope requires tenant and shell constraints

## Explicitly Forbidden

V1-G12 must not add:

- provider/model calls or routing
- tool execution
- arbitrary file mutation outside the explicit audit store path
- browser or network behavior
- connector behavior
- shell runtime wiring
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy
- external database writes
- migrations
- queues, workers, daemons, subprocesses, or threads
- live auth, live trust lookup, or HumanInput bridge activation
- live approval enforcement or approval-token issuance
- audit records as execution authority
- raw secret, prompt, file, customer, approval token, or PIN persistence
- haptic device behavior
- device, robotics, IoT, drone, robot, humanoid, or physical-world behavior
- runtime export cleanup
- final API freeze
- V1 product readiness or production readiness claims

## Required Acceptance Tests If Approved

The implementation must include tests proving:

- safe V1-G11 request/decision metadata can create a redacted audit event
- audit event records require lineage ID, event ID, tenant ref, actor ref, shell ID, and decision ID for consequential actions
- destructive edit/delete evidence requires approval ID and approval evidence ref
- raw secret values are rejected
- raw approval PINs and tokens are rejected
- raw prompts and raw file contents are rejected
- unknown privacy class fails closed
- record hashes are deterministic for sanitized records
- append-only store writes and reads redacted records from an explicit local audit-store path
- lookup by event ID works within tenant/shell scope
- lookup by lineage ID works within tenant/shell scope
- lookup by decision ID works within tenant/shell scope
- cross-tenant or cross-shell lookup fails closed
- records do not authorize execution or emit approval tokens
- provider/model/tool/browser/network/device/robotics/physical-world claims remain blocked without Guardian and audit linkage

## Rollback Plan If Approved

Rollback must remove only:

- `lima/spine/v1_audit_evidence.py`
- `lima/persistence/v1_audit_store.py`
- candidate exports added to `lima/spine/__init__.py`
- candidate exports added to `lima/persistence/__init__.py`
- V1-G12 docs/tests/fixtures

Rollback must not require shell repo changes, Sparkbot changes, database migrations, provider configuration changes, external service changes, or production deployment changes.

## Stop Conditions

Stop before implementation or revert the implementation if any of these appear:

- file scope exceeds the approved V1-G12 files
- persistence writes outside the explicit audit store path
- raw secrets, raw prompts, raw file contents, approval PINs, approval tokens, or raw customer data can persist
- audit metadata becomes execution authority
- destructive edit/delete records can persist without approval evidence
- consequential records can persist without `decision_id`
- tenant, actor, shell, lineage, or event scope can be omitted
- cross-tenant or cross-shell query leakage appears
- provider/model calls or routing are added
- tools, arbitrary files, browsers, networks, connectors, devices, robots, or physical-world systems are invoked
- external database writes, migrations, queues, workers, daemons, subprocesses, or threads are added
- shell runtime wiring is added
- Sparkbot code is imported or copied
- runtime exports are cleaned up or frozen
- validation fails

## Boundary Confirmation

- Approval request packet only: yes.
- Runtime implementation approved by this request: no.
- Operator approval recorded: no.
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
- API status remains: `CANDIDATE_ONLY`.

## Recommended Next Step

Operator decision on the exact approval question above.

If approved, create the V1-G12 implementation branch and implement only the approved durable audit/evidence persistence slice. If not approved, revise the request or keep LIMA at `CANDIDATE_ONLY`.
