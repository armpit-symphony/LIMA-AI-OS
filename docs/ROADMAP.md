# Roadmap

LIMA Runtime is SparkPit Labs' trust-gated automation and robotics runtime. Sparkbot is the R&D shell and parity source. Arc / LIMA AI Office becomes the office shell. Robo-OS becomes the robotics driver layer. SparkPit becomes the web, community, and research shell.

## Near-Term Milestones

### M0: Phase 0 Contracts

- Land docs, contracts, and package skeleton.
- Validate imports.
- Review architecture decisions before implementation extraction.

### M0.5: Intent Compiler Boundary

Goal: define how human language becomes governed action before Harness extraction.

Deliverables:

- `IntentEnvelope` contract.
- `HumanInput` contract.
- `ClarificationRequest` contract.
- `RiskClass` enum.
- `IntentCompilerProtocol`.
- Intent Compiler boundary doc.
- `IntentLifecycle` / intent status contract.
- `IntentStatus` enum.
- `IntentType` enum.
- `ApprovalLevel` enum.
- `EvidenceRequirement` contract.
- `IntentCompilationResult` contract.
- Clarification lifecycle.
- Confidence/risk thresholds as policy-owned, not compiler-owned.
- Sparkbot chat/voice adapter requirements.
- Approval UX requirements.
- Voice/text normalization rules.
- Future BCI safety constraints.
- Raw language execution prohibition.
- Future BCI confirmation-only rule.
- Audit trail linking raw human input -> typed intent -> Guardian decision -> action/result.

Acceptance criteria:

- No tool, model, driver, file, browser, network, admin, or robot action can execute from raw natural language.
- Raw chat/voice cannot directly execute tools in the architecture.
- Every consequential command has an `IntentEnvelope`.
- Ambiguous commands trigger clarification instead of execution.
- High-risk intent requires Guardian approval.
- `IntentCompilerProtocol` remains non-executing.
- `GuardianDecision` is required before consequential Harness/Driver/Tool execution.
- Phase 1 Harness extraction is blocked until this boundary is reviewed.
- Future thought/BCI input is documented as confirm-only, never direct execution.
- Sparkbot can later adapt its chat/voice commands into this contract without losing current behavior.

### M0.6: Sparkbot Entrypoint Inventory

Goal: inventory Sparkbot's current chat/voice/tool/model/Guardian/terminal/file/network/meeting entrypoints before extraction.

Deliverables:

- `docs/SPARKBOT_ENTRYPOINT_INVENTORY.md`.
- Mapping from current Sparkbot entrypoints to future LIMA contracts.
- Raw chat-to-tool shortcut risk notes.
- Guardian coverage notes.
- Tool-pack scoping notes.
- Extraction blockers list.

Acceptance criteria:

- No Sparkbot code is copied.
- No LIMA runtime implementation is added.
- Current entrypoints are mapped to `HumanInput`, `IntentEnvelope`, `GuardianDecision`, Harness, Driver, Spine, ToolPack, or Shell contracts.
- Potential raw chat-to-tool shortcuts are identified.
- Future Sparkbot adapter requirements are documented.
- Phase 1 extraction remains blocked until inventory is reviewed.

### M0.7: Guardian Decision ID Contract

Goal: define the mandatory `decision_id` contract linking `IntentEnvelope` to every consequential action and audit event.

Deliverables:

- `docs/GUARDIAN_DECISION_CONTRACT.md`.
- `GuardianDecisionStatus` contract.
- `ConsequentialActionRequest` contract.
- `decision_id` requirements for Harness, Tool, Driver, Terminal, Robot, File, Browser, Network, Admin, Payment actions.
- Spine/Audit event linkage requirements.
- Risk handling notes for terminal/PTY and robot actions.

Acceptance criteria:

- Every consequential execution path must require `decision_id` in architecture.
- Denied, escalated, and expired decisions are auditable.
- `decision_id` cannot be reused for unrelated actions.
- Harness/Driver contracts mention `GuardianDecision` requirements.
- Phase 1 extraction remains blocked until the `decision_id` contract is reviewed.

### M0.8: Tool-Pack Scoping Contract

Goal: define deny-by-default tool-pack scoping so shells and models never receive the full tool catalogue by default.

Deliverables:

- `docs/TOOL_PACK_SCOPING.md`.
- `ToolPackManifest` expansion.
- `ShellToolScope` contract.
- `ToolExposureRequest` contract.
- `ToolExposureDecision` contract.
- Harness shortlist requirements.
- Default pack risk classes.
- Shell examples for Sparkbot, Arc, SparkPit, Robo-OS, and future humanoid/worker robots.

Acceptance criteria:

- No shell receives all tools by default.
- Tool exposure is deny-by-default.
- Every consequential tool execution requires `GuardianDecision.decision_id`.
- Critical packs require explicit approval metadata.
- Harness extraction remains blocked until Sparkbot tools are grouped into packs.

### M0.9: Sparkbot Tool-Pack Inventory

Goal: map Sparkbot's current tool surfaces into future LIMA tool packs before Harness/tool extraction.

Deliverables:

- `docs/SPARKBOT_TOOL_PACK_INVENTORY.md`.
- Proposed pack map for Sparkbot tools.
- Shell allowance draft for Sparkbot, Arc, SparkPit, Robo-OS, and future humanoid/worker robots.
- Full-catalogue exposure risk notes.
- `GuardianDecision` pack constraint notes.
- Extraction blockers.

Acceptance criteria:

- Sparkbot tools are inventoried by path/name where possible.
- Each known tool surface has a proposed pack or unknown classification.
- Critical packs are identified.
- No runtime implementation is added.
- No Sparkbot code is copied.
- Harness extraction remains blocked until the inventory is reviewed.

### M0.10: Tool-Pack Risk Policy

Goal: define default risk and approval policy for LIMA tool packs before enforcement or Harness extraction.

Deliverables:

- `docs/TOOL_PACK_RISK_POLICY.md`.
- Default risk/approval table for all packs.
- Mixed read/write pack rules.
- Dynamic skill policy.
- Scheduled/autonomous decision inheritance rules.
- Shell-specific defaults.

Acceptance criteria:

- Every starter pack has default risk guidance.
- Unknown tools are denied by default.
- Terminal/admin/robot/payment/deploy packs are critical-risk.
- Dynamic skills require classification before exposure.
- Scheduled execution inherits `decision_id` or requires renewal.
- Harness extraction remains blocked until this policy is reviewed.

### M0.11: Approval Metadata Contract

Goal: define approval metadata required for high/critical-risk actions.

Deliverables:

- `docs/APPROVAL_METADATA_CONTRACT.md`.
- `ApprovalMetadata` contract.
- `ApprovalStatus` / `ApprovalMethod` contract.
- Breakglass approval rules.
- Scheduled/autonomous approval inheritance.
- Critical pack approval guidance.

Acceptance criteria:

- Approval metadata attaches to `GuardianDecision.decision_id`.
- Approval does not replace `GuardianDecision`.
- Critical packs have explicit approval requirements.
- Breakglass is short-lived, scoped, and auditable.
- Scheduled/autonomous execution renews approval when expired/out of scope.
- No runtime implementation is added.

### M0.12: Spine / Audit Lineage Contract

Goal: define end-to-end lineage across input, intent, Guardian decision, approval, policy/tool exposure, execution, and result.

Deliverables:

- `docs/SPINE_AUDIT_LINEAGE_CONTRACT.md`.
- `AuditLineageRecord` contract.
- Expanded `SpineEvent` fields.
- Event category/status enums.
- Scheduled/autonomous lineage rules.
- Critical action lineage rules.
- Privacy/redaction guidance.

Acceptance criteria:

- Every consequential action can be traced by `lineage_id`.
- `decision_id` appears in downstream execution events.
- `approval_id` appears where policy requires approval.
- Denied, blocked, expired, revoked, superseded, and failed actions remain auditable.
- No runtime implementation is added.
- Extraction remains blocked until lineage contract is reviewed.

### M0.13: Redaction / Privacy Contract

Goal: define privacy, redaction, reference, retention, and visibility contracts before Spine storage/audit persistence.

Deliverables:

- `docs/REDACTION_PRIVACY_CONTRACT.md`.
- `PrivacyClass` / `RedactionClass` / `RetentionClass` / `VisibilityClass` contracts.
- `DataReference` contract.
- Audit/spine privacy fields.
- Default handling for secrets, transcripts, model context, terminal output, files, memory, browser/network data, robot sensors, and future BCI/thought-adjacent data.

Acceptance criteria:

- Raw secrets are never stored in audit events.
- Sensitive content uses refs/summaries/redaction.
- BCI/thought data is biometric and confirm-only.
- Robot sensor data has safety/privacy defaults.
- Extraction remains blocked until redaction/privacy contract is reviewed.

### M0.14: Runtime Boundary Map

Goal: map current Sparkbot, Guardian Suite, and Robo-OS surfaces to future LIMA Runtime boundaries before extraction.

Deliverables:

- `docs/RUNTIME_BOUNDARY_MAP.md`.
- reference repo commit table.
- boundary classification types.
- boundary matrix.
- phase gate checklist.
- do-not-extract-yet list.
- future adapter plan.

Acceptance criteria:

- Sparkbot, LIMA Guardian Suite, and LIMA Robo-OS are inspected read-only.
- Current surfaces are classified by boundary type.
- Unsafe shortcuts are marked do-not-extract-yet.
- Extraction gates from Phase 0 through 0.13 are consolidated.
- No implementation is copied.
- No runtime code is added.

### M1: Guardian Extraction Readiness

- Map recent Sparkbot Guardian behavior.
- Identify direct app coupling.
- Define Sparkbot adapters.
- Build parity test list for policy, approvals, breakglass, vault references, verifier, token/cost control, memory policy, and audit.

### M2: Harness Extraction Readiness

- Map Sparkbot model routing, fallback, tool catalogue, prompt cache, and telemetry.
- Define tool-pack scoping rules.
- Ensure no public Harness API can execute unguarded tools.

### M3: Spine Extraction Readiness

- Map task/event/process ledger, pending approvals, project lineage, meeting heartbeat, recurring jobs, and audit writer.
- Define storage backend boundary.

### M4: Sparkbot On Runtime

- Run Sparkbot as a shell over LIMA Runtime contracts.
- Preserve operator UX and parity behavior.
- Keep Sparkbot as the proof shell until runtime parity is real.

### M5: Robo-OS Driver Integration

- Register robotics capabilities and telemetry requirements.
- Support dry runs and simulation first.
- Require Guardian approval for physical-world execution.
- Treat emergency stop as always available and audited.

### M6: Office And Web Shells

- Add Arc / LIMA AI Office shell contracts.
- Add SparkPit web shell contracts.
- Expand office bots and automation agents through scoped tool packs.

## Long-Term Vision

LIMA Runtime becomes the kernel for human-controlled AI infrastructure: office bots, automation agents, worker robots, humanoid robots, and AI-operated work environments.

The runtime is credible only if the trust boundary is real:

- Guardian gates action.
- Natural language compiles into typed, auditable intent.
- Spine records lineage.
- Harness scopes models and tools.
- Drivers expose capabilities without becoming brains.
- Shells remain consumers, not policy owners.

## Risks

- Extracting too early can fork behavior away from Sparkbot.
- Guardian Suite may lag Sparkbot and may preserve app coupling that should be removed.
- Robo-OS integration touches physical-world risk and must default to dry-run/simulation.
- Tool catalogues can become unsafe if shells do not declare tool packs.
- Persistence must avoid raw secret sprawl in audit/event payloads.

## Current Status

Phase 0 only. No runtime implementation yet.
