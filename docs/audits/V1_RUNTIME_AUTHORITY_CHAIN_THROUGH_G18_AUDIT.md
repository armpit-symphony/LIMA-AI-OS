# V1 Runtime Authority Chain Through G18 Audit

Date: 2026-06-16
Branch: `audit-v1-runtime-authority-chain-through-g18`
API status: `CANDIDATE_ONLY`

Audit verdict: `PASS`

This audit reviews the V1 authority chain through V1-G18:

- V1-G11 runtime request decision/preflight
- V1-G12 durable audit/evidence persistence
- V1-G14 destructive approval enforcement
- V1-G15 shell/harness guiderail input contract
- V1-G16 guarded file mutation policy contract
- V1-G17 file mutation preview/diff runtime behavior
- V1-G18 consumer proof packet audit intake

The audit does not add runtime behavior, wire consumers, route providers/models, activate HumanInput, invoke connectors, mutate files, execute browser/network/device/robotics/physical-world actions, run scheduled tasks, send external messages, or claim product readiness.

## Inputs Reviewed

- `lima/kernel/v1_runtime_request.py`
- `lima/guardian/v1_decision_gate.py`
- `lima/spine/v1_audit_evidence.py`
- `lima/persistence/v1_audit_store.py`
- `lima/guardian/v1_approval_enforcement.py`
- `lima/shells/contracts/v1_guiderail_input.py`
- `lima/guardian/v1_file_mutation_policy.py`
- `lima/guardian/v1_file_mutation_preview.py`
- `lima/guardian/v1_consumer_proof_packet_intake.py`
- `docs/architecture/LIMA_CAPABILITY_OPEN_AUTHORITY_GATED_MODEL.md`
- `docs/audits/V1_G15_SHELL_HARNESS_GUIDERAIL_CONTRACT_AUDIT.md`
- `docs/audits/V1_G16_GUARDED_FILE_MUTATION_POLICY_AUDIT.md`
- `docs/audits/V1_G17_FILE_MUTATION_PREVIEW_DIFF_AUDIT.md`
- `docs/audits/V1_G18_CONSUMER_PROOF_PACKET_AUDIT_INTAKE_AUDIT.md`
- `docs/V1_G18_CONSUMER_PROOF_PACKET_AUDIT_INTAKE.md`
- `tests/fixtures/runtime_extraction/v1_g18_consumer_proof_packet_audit_intake.json`

## Chain Findings

- V1-G11 builds typed runtime request decision/preflight metadata: pass.
- V1-G12 records only redacted durable audit/evidence metadata: pass.
- V1-G14 enforces destructive edit/delete approval evidence without execution: pass.
- V1-G15 validates shell/harness guiderail input metadata without wiring shells or executing capabilities: pass.
- V1-G16 validates guarded file mutation policy metadata without reading, writing, deleting, overwriting, or patching files: pass.
- V1-G17 validates dry-run preview and redacted diff/patch metadata without reading, writing, deleting, overwriting, or patching files: pass.
- V1-G18 validates consumer proof packet metadata without touching consumer repositories, importing consumer code, calling consumer runtimes, or wiring consumers: pass.
- LIMA remains capability-open and authority-gated: pass.
- Shell/harness guiderails shape authority through explicit metadata but do not bypass LIMA gates: pass.
- File mutation preview/diff exists as a non-mutating candidate runtime slice, not as an execution path: pass.
- Consumer proof packet intake exists as a non-executing evidence intake slice, not as consumer integration: pass.

## Authority Invariants

- Approval evidence cannot be forged into broad authority: pass.
- Audit/evidence metadata cannot become execution authority: pass.
- Guiderail input metadata cannot become execution authority: pass.
- File mutation policy metadata cannot become execution authority: pass.
- File mutation preview/diff metadata cannot become execution authority: pass.
- Consumer proof packet metadata cannot become runtime authority: pass.
- Destructive edit/delete/file mutation remains approval-gated: pass.
- File mutation preview/diff exists but actual mutation execution remains unimplemented: pass.
- Consumer proof packet intake exists but consumer integration remains unimplemented: pass.
- Provider/model behavior remains blocked unless a future explicit authority lane approves it: pass.
- Tool behavior remains blocked unless a future explicit authority lane approves it: pass.
- Browser/network behavior remains blocked unless a future explicit authority lane approves it: pass.
- Connector behavior remains blocked unless a future explicit authority lane approves it: pass.
- Device/robotics/physical-world behavior remains blocked unless a future explicit physical-world authority/safety lane approves it: pass.

## Data Protection Invariants

- Raw secrets are not persisted or emitted: pass.
- Raw prompts are not persisted or emitted: pass.
- Raw file contents are not persisted or emitted: pass.
- Raw diff or patch contents are not persisted or emitted: pass.
- Raw approval PINs are not persisted or emitted: pass.
- Raw approval tokens are not persisted or emitted: pass.
- Raw credentials are not persisted or emitted: pass.
- Raw customer data is not persisted or emitted: pass.

## Scope And Isolation Invariants

- Tenant scope remains explicit in V1-G15, V1-G16, and V1-G17 metadata: pass.
- Shell scope remains explicit in V1-G15, V1-G16, and V1-G17 metadata: pass.
- Actor scope remains explicit in V1-G15, V1-G16, and V1-G17 metadata: pass.
- Session scope remains explicit in V1-G15, V1-G16, and V1-G17 metadata: pass.
- Consumer repository, branch/ref, commit SHA, proof packet path, audit packet path, and summary path are metadata only in V1-G18: pass.
- Cross-tenant, cross-shell, cross-actor, cross-session, or cross-consumer authority leakage was not introduced: pass.

## Integration Invariants

- Consumer integration remains blocked: pass.
- Sparkbot was not touched: pass.
- Sparkbot_shell was not touched: pass.
- Arc-Bot-shell was not touched: pass.
- LIMA Robo OS was not touched: pass.
- LIMA Office was not touched: pass.
- Consumer code imports were not added: pass.
- Consumer runtime calls were not added: pass.
- Product readiness remains unclaimed: pass.
- Final public API freeze remains unapproved: pass.

## Residual Gaps

- Actual guarded file mutation execution remains unapproved.
- Live approval capture/enforcement beyond current metadata gates remains unapproved.
- Provider/model routing authority remains unapproved.
- Connector authority remains unapproved.
- Browser/network authority remains unapproved.
- Consumer integration remains blocked.
- Physical-world/device/robot/drone/IoT authority remains blocked pending a dedicated safety lane.
- Final API freeze remains incomplete.
- Product readiness remains incomplete.

## Audit Conclusion

The V1 authority chain through G18 preserves the capability-open, authority-gated posture while preventing current bypass. V1-G18 advances consumer proof-packet evidence intake without approving consumer integration or runtime wiring.

Recommended next safe step: update readiness rollup through G18, then prepare the next exact approval gate based on the preferred lane. Do not implement consumer integration, actual file mutation execution, live approval capture, provider/model routing, connector/browser/network authority, physical-world behavior, final API freeze, or product-readiness claims without future exact approvals.
