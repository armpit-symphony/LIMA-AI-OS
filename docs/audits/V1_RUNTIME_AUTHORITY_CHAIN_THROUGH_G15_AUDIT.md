# V1 Runtime Authority Chain Through G15 Audit

Date: 2026-06-15
Branch: `audit-v1-runtime-authority-chain-through-g15`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit reviews the V1 authority chain through V1-G15:

- V1-G11 runtime request decision/preflight
- V1-G12 durable audit/evidence persistence
- V1-G14 destructive approval enforcement
- V1-G15 shell/harness guiderail input contract

The audit does not add runtime behavior, wire consumers, route providers/models, activate HumanInput, invoke connectors, mutate files, execute browser/network/device/robotics/physical-world actions, or claim product readiness.

## Inputs Reviewed

- `lima/kernel/v1_runtime_request.py`
- `lima/guardian/v1_decision_gate.py`
- `lima/spine/v1_audit_evidence.py`
- `lima/persistence/v1_audit_store.py`
- `lima/guardian/v1_approval_enforcement.py`
- `lima/shells/contracts/v1_guiderail_input.py`
- `docs/architecture/LIMA_CAPABILITY_OPEN_AUTHORITY_GATED_MODEL.md`
- `docs/audits/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_AUDIT.md`

## Chain Findings

- V1-G11 builds typed runtime request decision/preflight metadata: pass.
- V1-G12 records only redacted durable audit/evidence metadata: pass.
- V1-G14 enforces destructive edit/delete approval evidence without execution: pass.
- V1-G15 validates shell/harness guiderail input metadata without wiring shells or executing capabilities: pass.
- LIMA is capability-open but authority-gated: pass.
- Shell/harness guiderails can shape request authority through explicit capability profiles, guardrail mode, approval policy, actor/session/tenant/shell scope, allowed lanes, and policy expectations: pass.

## Authority Invariants

- Approval evidence cannot be forged into broad authority: pass.
- Audit/evidence metadata cannot become execution authority: pass.
- Guiderail input metadata cannot become execution authority: pass.
- Destructive edit/delete/file mutation remains approval-gated: pass.
- File mutation execution remains unimplemented and unapproved: pass.
- Provider/model behavior remains blocked unless a future explicit authority lane approves it: pass.
- Tool behavior remains blocked unless a future explicit authority lane approves it: pass.
- Browser/network behavior remains blocked unless a future explicit authority lane approves it: pass.
- Connector behavior remains blocked unless a future explicit authority lane approves it: pass.
- Device/robotics/physical-world behavior remains blocked unless a future explicit physical-world authority/safety lane approves it: pass.

## Data Protection Invariants

- Raw secrets are not persisted or emitted: pass.
- Raw prompts are not persisted or emitted: pass.
- Raw file contents are not persisted or emitted: pass.
- Raw approval PINs are not persisted or emitted: pass.
- Raw approval tokens are not persisted or emitted: pass.
- Raw customer data is not persisted or emitted: pass.

## Integration Invariants

- Consumer integration remains blocked: pass.
- Sparkbot was not touched: pass.
- Sparkbot_shell was not touched: pass.
- Arc-Bot-shell was not touched: pass.
- LIMA Robo OS was not touched: pass.
- LIMA Office was not touched: pass.
- Product readiness remains unclaimed: pass.
- Final API freeze remains unapproved: pass.

## Residual Gaps

- Guarded file mutation policy approval request is not yet prepared.
- Actual file mutation execution remains unapproved.
- Live approval capture remains unapproved.
- Provider/model routing authority remains unapproved.
- Connector authority remains unapproved.
- Browser/network authority remains unapproved.
- Physical-world authority/safety lane remains unapproved.
- Consumer proof packet audits and final API freeze remain incomplete.

## Audit Conclusion

The V1 authority chain through G15 preserves capability-open, authority-gated posture while preventing current bypass.

Recommended next safe step: update readiness rollup through G15, then prepare the V1-G16 guarded file mutation policy approval request. Do not implement V1-G16 file mutation policy or actual file mutation behavior without exact approval.
