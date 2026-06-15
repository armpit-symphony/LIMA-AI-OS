# V1 Runtime Request Evidence Approval Invariants Audit

Date: 2026-06-15
Branch: `audit-v1-runtime-request-evidence-approval-invariants`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit reviews the V1-G11, V1-G12, and V1-G14 runtime chain:

- V1-G11 typed runtime request and GuardianDecision preflight metadata
- V1-G12 redacted durable audit/evidence metadata
- V1-G14 destructive edit/delete approval evidence enforcement

The audit does not add runtime behavior, change authority, wire consumers, route providers/models, activate HumanInput, invoke connectors, execute file mutations, or claim product readiness.

## Inputs Reviewed

- `lima/kernel/v1_runtime_request.py`
- `lima/guardian/v1_decision_gate.py`
- `lima/spine/v1_audit_evidence.py`
- `lima/persistence/v1_audit_store.py`
- `lima/guardian/v1_approval_enforcement.py`
- `tests/test_v1_g11_runtime_request_decision_gate.py`
- `tests/test_v1_g12_durable_audit_evidence_persistence.py`
- `tests/test_v1_g14_destructive_approval_enforcement.py`
- `docs/audits/V1_G14_DESTRUCTIVE_APPROVAL_ENFORCEMENT_AUDIT.md`
- `docs/architecture/LIMA_CAPABILITY_OPEN_AUTHORITY_GATED_MODEL.md`

## Chain Findings

- V1-G11 builds typed runtime request metadata from validated candidates: pass.
- V1-G11 reviews typed runtime request metadata into non-executing `GuardianDecision` metadata: pass.
- V1-G11 safe informational/planning/drafting candidates remain non-executing: pass.
- V1-G11 destructive file-mutation shaped requests map to `NEEDS_OPERATOR_PIN`: pass.
- V1-G11 provider/model/tool/browser/network/device/robotics/physical-world shaped claims remain denied or blocked under the current gate: pass.
- V1-G12 accepts only reviewed V1-G11 request/decision metadata: pass.
- V1-G12 persists only redacted audit/evidence metadata through the local candidate store: pass.
- V1-G12 audit/evidence records are proof, not execution authority: pass.
- V1-G12 rejects raw secrets, prompts, file contents, approval PINs, approval tokens, and customer data: pass.
- V1-G12 scoped lookup blocks cross-tenant or cross-shell leakage: pass.
- V1-G14 enforces destructive edit/delete approval evidence without execution: pass.
- V1-G14 requires V1-G11 request/decision metadata and destructive file-mutation shape: pass.
- V1-G14 requires sanitized approval evidence before producing a proof record: pass.
- V1-G14 returns redacted proof metadata only: pass.

## Authority Invariants

- Audit/evidence metadata never becomes broad execution authority: pass.
- Approval metadata cannot be forged into authority: pass.
- Approval tokens are not issued by V1-G11, V1-G12, or V1-G14: pass.
- Raw approval PIN verification is absent and unapproved: pass.
- Destructive edit/delete/file mutation remains approval-gated: pass.
- Real file mutation execution remains blocked until a future approved guarded file mutation policy lane: pass.
- Provider/model/tool/browser/network/device/robotics/physical-world claims remain blocked unless a future explicit authority lane approves them: pass.
- Current blocking means "not authorized by the current gate," not "impossible forever": pass.

## Data Protection Invariants

- Raw secrets are not persisted or emitted: pass.
- Raw prompts are not persisted or emitted: pass.
- Raw file contents are not persisted or emitted: pass.
- Raw approval PINs are not persisted or emitted: pass.
- Raw approval tokens are not persisted or emitted: pass.
- Raw customer data is not persisted or emitted: pass.
- Redacted summaries and evidence references are the permitted evidence shape in current candidate lanes: pass.

## Scope Invariants

- Cross-tenant leakage is blocked or not introduced: pass.
- Cross-shell leakage is blocked or not introduced: pass.
- Cross-actor approval scope mismatch fails closed in V1-G14: pass.
- Consumer repos remain untouched: pass.
- Sparkbot remains untouched: pass.
- Sparkbot_shell remains untouched: pass.
- Arc-Bot-shell remains untouched: pass.
- LIMA Robo OS remains untouched: pass.
- LIMA Office remains untouched: pass.
- Product readiness remains unclaimed: pass.
- Final API freeze remains unapproved: pass.

## Residual Gaps

- Shell/harness guiderail input contract is not implemented.
- Guarded file mutation execution policy is not implemented.
- Live approval capture or raw PIN verification is not implemented.
- Provider/model routing authority lane is not implemented.
- Connector authority lane is not implemented.
- Browser/network authority lane is not implemented.
- Physical-world/device/robot/drone/IoT authority lane is not implemented.
- Consumer integration is not approved.
- Final public API freeze is not approved.

## Audit Conclusion

The V1-G11 -> V1-G12 -> V1-G14 chain preserves the required request, evidence, and approval invariants.

Recommended next step: create a next authority-lane decision matrix and then prepare a V1-G15 shell/harness guiderail input contract approval request. Do not start V1-G15 runtime implementation without an exact operator approval gate.
