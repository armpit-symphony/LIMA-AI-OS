# V1-G12 Durable Audit/Evidence Persistence Operator Decision Packet

Date: 2026-06-14
Branch: `v1-g12-durable-audit-evidence-persistence-approval-request`
API status: `CANDIDATE_ONLY`

Decision packet status: `awaiting_operator_decision`

This packet records the valid operator choices for the exact V1-G12 durable audit/evidence persistence approval request. It does not change runtime behavior, modify `lima/`, approve persistence implementation, or approve product readiness by itself.

## Decision Source

The decision source is:

- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_APPROVAL_REQUEST.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_PREFLIGHT_AUDIT.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_WORK_ORDER.md`
- `docs/audits/V1_G11_RUNTIME_REQUEST_DECISION_GATE_AUDIT.md`

The approval request asks:

> Do you explicitly approve V1-G12 implementation of the durable audit/evidence persistence runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions below?

General V1 product direction, prior static gates, the V1-G11 audit, this packet, or broad statements that durable audit/evidence persistence is needed do not count as implementation approval.

## Current Decision State

- Operator approval recorded: no.
- Runtime implementation approved: no.
- Approved next implementation branch: none.
- Current next action: operator decision, request revision, or pause.

## Decision Record

One operator choice must be recorded before implementation.

- Recorded choice: `none`
- Recorded approval wording: `none`
- Recorded revision request: `none`
- Recorded pause reason: `none`
- Approved implementation branch: `none`
- Runtime implementation approved: no

Only `Approve-V1-G12`, `Revise-V1-G12`, or `Pause` is valid here. Any other text is commentary, not a decision.

## Decision Record Validation Rules

- `none`: valid only while every Decision Record field remains `none` and runtime implementation approved remains `no`.
- `Approve-V1-G12`: valid only with the exact required approval wording, approved branch `v1-g12-durable-audit-evidence-persistence`, no revision request, no pause reason, and runtime implementation approved set to `yes`.
- `Revise-V1-G12`: valid only with a non-empty revision request, no approval wording, no approved implementation branch, no pause reason, and runtime implementation approved set to `no`.
- `Pause`: valid only with a non-empty pause reason, no approval wording, no approved implementation branch, no revision request, and runtime implementation approved set to `no`.
- Any mixed state is invalid and must be treated as no approval.
- Missing, misspelled, or extra choice values are invalid and must be treated as no approval.
- Runtime implementation may start only from the valid `Approve-V1-G12` state.

## Decision Record Templates

Use one template only.

Template for no recorded choice:

```text
Recorded choice: none
Recorded approval wording: none
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: none
Runtime implementation approved: no
```

Template for `Approve-V1-G12`:

```text
Recorded choice: Approve-V1-G12
Recorded approval wording: I explicitly approve V1-G12 implementation of the durable audit/evidence persistence runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_APPROVAL_REQUEST.md.
Recorded revision request: none
Recorded pause reason: none
Approved implementation branch: v1-g12-durable-audit-evidence-persistence
Runtime implementation approved: yes
```

Template for `Revise-V1-G12`:

```text
Recorded choice: Revise-V1-G12
Recorded approval wording: none
Recorded revision request: <required revision request>
Recorded pause reason: none
Approved implementation branch: none
Runtime implementation approved: no
```

Template for `Pause`:

```text
Recorded choice: Pause
Recorded approval wording: none
Recorded revision request: none
Recorded pause reason: <required pause reason>
Approved implementation branch: none
Runtime implementation approved: no
```

## Valid Operator Choices

### `Approve-V1-G12`

This choice is valid only if the operator explicitly approves the exact V1-G12 request scope.

Required approval wording:

`I explicitly approve V1-G12 implementation of the durable audit/evidence persistence runtime slice, limited to the file scope, behavior scope, tests, rollback plan, and stop conditions in docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_APPROVAL_REQUEST.md.`

If recorded, the next branch may be:

- `v1-g12-durable-audit-evidence-persistence`

If recorded, the only approved runtime scope is:

- `durable_audit_evidence_persistence_runtime_slice`

### `Revise-V1-G12`

This choice asks for a narrower or different request. It keeps runtime implementation unapproved.

Revision must name the requested change, such as:

- narrower file scope
- different storage boundary
- no local file-backed store
- additional negative tests
- stricter query scope requirements
- pause until another audit lands

### `Pause`

This choice keeps LIMA at `CANDIDATE_ONLY` and does not start V1-G12 runtime implementation.

## If `Approve-V1-G12` Is Recorded

Implementation must stay inside the already named V1-G12 scope:

- `lima/spine/v1_audit_evidence.py`
- `lima/spine/__init__.py`
- `lima/persistence/v1_audit_store.py`
- `lima/persistence/__init__.py`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE.md`
- `docs/V1_G12_DURABLE_AUDIT_EVIDENCE_PERSISTENCE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/v1_g12_durable_audit_evidence_persistence.json`
- `tests/test_v1_g12_durable_audit_evidence_persistence.py`

Any different file requires a new gate update before implementation.

## Boundaries While Awaiting Decision

- Runtime implementation approved: no.
- Operator approval recorded: no.
- Runtime behavior added: no.
- Durable persistence added: no.
- Storage adapter added: no.
- Query API added: no.
- External database writes added: no.
- `lima/` runtime files changed: no.
- `tests/support` changed: no.
- Shell repositories changed: no.
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell imports or code copy added: no.
- Provider/model calls or routing added: no.
- Shell runtime wiring added: no.
- Haptic device behavior added: no.
- Browser/file/network/device/robotics/physical-world behavior added: no.
- Runtime export cleanup approved: no.
- Final API freeze approved: no.
- V1 product readiness approved: no.
- Production readiness approved: no.

## Non-Negotiable Stop Conditions

Stop before implementation or revert if any of the following appear without a new explicit gate:

- file scope exceeds the V1-G12 request
- persistence writes outside the explicit audit store path
- raw sensitive content can persist
- audit metadata becomes execution authority
- consequential records can persist without `decision_id`
- destructive edit/delete records can persist without approval evidence
- tenant, actor, shell, lineage, or event scope can be omitted
- cross-tenant or cross-shell query leakage appears
- provider/model calls or routing are added
- tool/file/browser/network/device/robotics/physical-world behavior is invoked
- external database writes, migrations, queues, workers, daemons, subprocesses, or threads are added
- shell runtime wiring is added
- Sparkbot, Sparkbot_shell, or Arc-Bot-shell code is imported or copied
- runtime exports are cleaned up or frozen
- validation fails

## Recommended Next Step

Record one valid operator choice.

Keep LIMA at `CANDIDATE_ONLY` and stop before implementation until `Approve-V1-G12` is explicitly recorded.
