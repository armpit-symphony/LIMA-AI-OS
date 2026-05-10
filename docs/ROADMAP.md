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

### M0.15: Extraction Readiness Review

Goal: produce final Phase 0 readiness review and Phase 1 extraction order.

Deliverables:

- `docs/EXTRACTION_READINESS_REVIEW.md`.
- readiness score.
- ready/blocked area list.
- first safe extraction target.
- Phase 1 extraction order.
- Phase 1 PR #1 work order.
- go/no-go decision.
- risk register.

Acceptance criteria:

- reference repos rechecked.
- blocked items explicit.
- first safe extraction target identified.
- Phase 1 no-go areas documented.
- no implementation copied.
- no runtime behavior added.

### M1.0: Guardian Suite Decoupling Audit

Goal: audit Guardian Suite coupling before any runtime behavior moves.

Deliverables:

- `docs/PHASE_1_0_GUARDIAN_SUITE_DECOUPLING_AUDIT.md`.
- Guardian Suite reference commit table.
- coupling inventory for Sparkbot `app.crud`, `app.models`, `app.services`, direct database, vault/auth persistence, and runtime side effects.
- forbidden imports list for future `lima.guardian` code.
- first extraction seam recommendation.
- import-boundary test for `lima.guardian`.

Acceptance criteria:

- LIMA-Guardian-Suite is inspected read-only.
- Guardian Suite coupling blockers are explicit.
- Future `lima.guardian` code is protected from Sparkbot backend imports.
- No Guardian runtime behavior is migrated.
- No Sparkbot or Guardian Suite production code is modified.
- No enforcement, tool execution, vault migration, database migration, or live service wiring is added.

### M1.1: Vault/Auth Interface Skeleton

Goal: define non-executing Vault/Auth contracts to decouple Guardian from Sparkbot backend internals.

Deliverables:

- auth contract
- vault contract
- breakglass session reference contract
- non-executing provider protocols
- tests proving no forbidden Guardian imports
- documentation of forbidden live behavior

Acceptance criteria:

- no raw secret value fields
- no Sparkbot imports
- no live auth/vault behavior
- no PIN verification
- no encryption/decryption
- no DB/storage
- contracts/tests pass

### M1.2: Vault/Auth Provider Boundary Tests

Goal: add tests that prevent future Vault/Auth providers from importing Sparkbot internals or exposing live secret/auth behavior.

Deliverables:

- provider-boundary tests
- forbidden import list
- forbidden method/field checks
- docs for future provider rules

Acceptance criteria:

- no Sparkbot imports under LIMA provider paths
- no raw secret fields
- no live auth/vault/breakglass methods in protocols
- tests pass with current minimal package layout
- no implementation added

### M1.3: Vault/Auth Fake Providers

Goal: add test-only fake Auth, Vault, and Breakglass providers for contract validation.

Deliverables:

- fake auth provider
- fake vault provider
- fake breakglass provider
- tests proving fake providers are in-memory and non-executing
- docs for fake provider safety rules

Acceptance criteria:

- fake providers are in-memory only
- no real secrets
- no live auth or PIN verification
- no encryption/decryption
- no DB/storage
- no breakglass enforcement
- provider-boundary tests pass
- no implementation copied from reference repos

### M1.4: Guardian Decision Fake Evaluator

Goal: add fake in-memory Guardian decision evaluator for contract tests only.

Deliverables:

- fake evaluator
- tests for `ConsequentialActionRequest` to `GuardianDecision`
- docs explaining no real enforcement
- safety rules preventing execution

Acceptance criteria:

- no real enforcement
- no tool/model/driver execution
- no Sparkbot imports
- fake decisions carry `decision_id`
- critical actions do not auto-approve by default
- tests pass

### M1.5: Policy/Risk Fake Evaluator

Goal: add fake in-memory policy/risk evaluator for contract tests only.

Deliverables:

- fake policy/risk evaluator
- tests for `PolicyEvaluationContext` to `PolicyDecision`
- docs explaining no real enforcement
- safety rules preventing high/critical auto-approval

Acceptance criteria:

- no real enforcement
- no tool/model/driver execution
- no Sparkbot imports
- unknown packs/tools denied by default
- high/critical packs do not auto-allow
- `PolicyDecision` does not replace `GuardianDecision`
- tests pass

### M1.6: Approval Fake Recorder

Goal: add fake in-memory `ApprovalMetadata` recorder for contract tests only.

Deliverables:

- fake approval recorder
- tests for `ApprovalScope` / `ApprovalMetadata` recording
- docs explaining no approval enforcement
- safety rules preventing PIN/breakglass behavior

Acceptance criteria:

- no real enforcement
- no PIN verification
- no breakglass enforcement
- no approval tokens
- no tool/model/driver execution
- no Sparkbot imports
- approval metadata does not replace `GuardianDecision`
- tests pass

### M1.7: Spine/Audit Fake Recorder

Goal: add fake in-memory Spine/Audit recorder for contract tests only.

Deliverables:

- fake Spine/Audit recorder
- tests for `SpineEvent` / `AuditLineageRecord` recording
- docs explaining no persistence
- safety rules preventing raw sensitive data persistence

Acceptance criteria:

- no real persistence
- no DB/storage
- no file writes
- no raw secrets
- no raw prompts/transcripts/tool outputs/terminal output/sensor data
- no tool/model/driver execution
- no Sparkbot imports
- tests pass

### M1.8: Guardian Fake Pipeline

Goal: compose fake policy, Guardian decision, approval, and Spine/Audit components into a test-only contract pipeline.

Deliverables:

- `FakeGuardianPipeline`
- `FakeGuardianPipelineResult`
- tests for low-risk, critical, and unknown requests
- docs explaining no real enforcement/execution

Acceptance criteria:

- no real enforcement
- no tool/model/driver execution
- no Sparkbot imports
- no audit persistence
- critical actions do not auto-approve
- unknown actions deny/escalate
- fake lineage is recorded
- tests pass

### M1.9: Fake Pipeline Readiness Review

Goal: review fake pipeline integration and decide whether LIMA is ready for first adapter-design work.

Deliverables:

- `docs/PHASE_1_9_FAKE_PIPELINE_READINESS_REVIEW.md`
- fake pipeline readiness decision
- blocked areas list
- recommended next branch
- Phase 1.10 acceptance criteria

Acceptance criteria:

- fake pipeline reviewed
- ready/not-ready decision documented
- first adapter-design branch identified
- production integration remains blocked
- tests pass

### M1.10: Sparkbot HumanInput Adapter Design

Goal: design how Sparkbot input surfaces map to LIMA `HumanInput` records before any adapter implementation.

Deliverables:

- `docs/PHASE_1_10_SPARKBOT_HUMANINPUT_ADAPTER_DESIGN.md`
- Sparkbot input surface inventory
- HumanInput mapping table
- actor/shell/session mapping notes
- privacy/redaction defaults
- raw chat-to-tool shortcut block

Acceptance criteria:

- no Sparkbot changes
- no adapter wiring
- no model/tool execution
- HumanInput mapping exists for chat/voice/meeting/operator surfaces
- raw chat-to-tool shortcut remains blocked
- production integration remains blocked

### M1.11: HumanInput Adapter Contract

Goal: create non-executing adapter design contracts for mapping Sparkbot input surfaces to LIMA `HumanInput`.

Deliverables:

- `lima/contracts/adapters.py`
- `HumanInputAdapterSurface`
- `HumanInputAdapterMapping`
- `HumanInputAdapterDesign`
- describe-only `AdapterDesignProtocol`
- tests confirming no live adapter methods

Acceptance criteria:

- no Sparkbot imports
- no runtime behavior
- no adapt/execute methods
- raw chat-to-tool shortcut remains blocked
- tests pass

### Phase 1.12A: Owner Autonomy & Safety Policy

Goal: Define owner-controlled autonomy so LIMA can act naturally within configured boundaries without asking for PIN/approval for everything.

Deliverables:

- `docs/OWNER_AUTONOMY_SAFETY_POLICY.md`
- autonomy levels for manual, assisted, trusted, bounded autonomous, robot-safe, and locked-down operation
- capability rule matrix for owner policy
- trusted device/session policy
- identity confidence and verbal approval policy
- breakglass configuration guidance
- vault, personal data, external communication, destructive action, payment, deploy, terminal, and robot safety defaults
- robot/humanoid safety constitution and robot safety modes

Acceptance criteria:

- owner autonomy policy is reviewed before behavior-bearing adapter, skeleton, enforcement, robot, or tool work
- approval means owner policy plus trusted context, identity confidence, risk class, capability boundary, and escalation only when needed
- low-risk owner-approved actions can avoid repeated prompts when Guardian verifies context
- high/critical, secret, destructive, terminal/PTY, production deploy, payment, and physical-world actions escalate by policy
- law, human safety, and configured safety policy override owner command
- Guardian remains mandatory
- no runtime behavior is added

### Phase 1.12: Sparkbot Adapter Readiness Review

Goal: Decide whether LIMA is ready for first non-production Sparkbot HumanInput adapter skeleton.

Deliverables:

- `docs/PHASE_1_12_SPARKBOT_ADAPTER_READINESS_REVIEW.md`
- Sparkbot freshness check
- readiness decision
- Phase 1.13 scope
- adapter skeleton guardrails
- owner-autonomy context
- still-blocked list
- risk register

Acceptance criteria:

- Sparkbot origin/main rechecked
- GO/NO-GO decision documented
- Phase 1.13 allowed scope defined
- owner autonomy policy included as passive metadata context only
- production wiring remains blocked
- `stream_chat_with_tools` remains blocked
- no implementation added

### Phase 1.13: Sparkbot HumanInput Adapter Skeleton

Goal: Create non-production adapter skeleton converting neutral Sparkbot-style payloads into HumanInput records.

Deliverables:

- `lima/adapters/sparkbot_humaninput.py`
- `docs/PHASE_1_13_SPARKBOT_HUMANINPUT_ADAPTER_SKELETON.md`
- neutral payload dataclasses for chat, voice, meeting, and operator input
- pure conversion methods returning `HumanInput`
- tests proving mapping behavior and forbidden import/method boundaries

Acceptance criteria:

- neutral payloads only
- returns HumanInput only
- no Sparkbot imports
- no route wiring
- no model/tool execution
- no autonomy enforcement
- tests pass

### Phase 1.14: HumanInput Adapter Readiness Review

Goal: Decide whether the non-production HumanInput adapter skeleton is ready to be composed with the fake Guardian pipeline in a test-only branch.

Deliverables:

- `docs/PHASE_1_14_HUMANINPUT_ADAPTER_READINESS_REVIEW.md`
- readiness decision
- Phase 1.15 allowed scope
- bridge-vs-adapter boundary clarification
- still-blocked list
- risk register

Acceptance criteria:

- adapter remains HumanInput-only
- bridge, if allowed, is separate and test-only
- production wiring remains blocked
- model/tool execution remains blocked
- autonomy enforcement remains blocked
- tests pass

### Phase 1.15: HumanInput Fake Pipeline Bridge

Goal: Create test-only bridge from HumanInput to FakeGuardianPipeline while keeping adapter and bridge separate.

Deliverables:

- `lima/guardian/humaninput_pipeline_fakes.py`
- `docs/PHASE_1_15_HUMANINPUT_FAKE_PIPELINE_BRIDGE.md`
- tests proving explicit-metadata request creation
- tests proving adapter/bridge separation

Acceptance criteria:

- bridge is test-only
- adapter remains HumanInput-only
- no Sparkbot imports
- no production wiring
- no natural-language intent inference
- no model/tool execution
- fake pipeline only
- tests pass

### Phase 1.16: Phase One Readiness Review

Goal: Review Phase 1 fake pipeline and adapter skeleton progress before deciding next step.

Deliverables:

- `docs/PHASE_1_16_PHASE_ONE_READINESS_REVIEW.md`
- Sparkbot freshness check
- proven/not-proven list
- readiness decision
- recommended next branch
- updated roadmap recommendation
- risk register

Acceptance criteria:

- no runtime behavior added
- Sparkbot origin/main checked
- production adapter remains blocked unless explicitly approved
- next step identified
- tests pass

### Phase 1.17: Identity / Session / Trust Context Mapping Review

Goal: Review how actor/session/trusted-context/autonomy metadata should map to future AuthContext and trust contracts before real adapter work.

Deliverables:

- `docs/PHASE_1_17_IDENTITY_SESSION_TRUST_CONTEXT_REVIEW.md`
- Sparkbot freshness check
- identity mapping proposal
- session mapping proposal
- trusted device mapping proposal
- identity confidence mapping proposal
- owner autonomy mapping notes
- Phase 1.18 recommendation

Acceptance criteria:

- no live auth/session lookup
- no trusted device enforcement
- no autonomy enforcement
- actor/session/trusted context remain passive metadata
- next contract extension identified

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
