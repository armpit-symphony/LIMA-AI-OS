# Roadmap

Current phase and branch guidance lives in `docs/CURRENT_PROJECT_STATE.md`. Read that file before using this roadmap for implementation sequencing.

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

### Phase 1.18: AuthContext / Trust Contract Extension

Goal: Add contract types for trusted device context, identity confidence, session context, and owner-autonomy context.

Acceptance criteria:

- contracts exist
- no live verification
- no enforcement
- references remain passive
- tests pass

### Phase 1.19: Adapter Fixture Tests with Fake AuthContext

Goal: Add test-only fixtures proving HumanInput adapter metadata can carry fake AuthContext/trust references passively.

Acceptance criteria:

- fake AuthContext/trust fixtures only
- references remain passive
- adapter returns HumanInput only
- no live auth/trust/autonomy enforcement
- tests pass

### Phase 1.20: Real Adapter Readiness Review

Goal: Review readiness for real Sparkbot adapter implementation after fake AuthContext fixture tests.

Deliverables:

- `docs/PHASE_1_20_REAL_ADAPTER_READINESS_REVIEW.md`
- Sparkbot freshness check
- ready/not-ready list
- production adapter go/no-go decision
- recommended Phase 1.21 branch
- risk register

Acceptance criteria:

- Sparkbot origin/main rechecked
- production adapter decision documented
- next safe branch identified
- no runtime behavior added
- tests pass

### Phase 1.21: Sparkbot Payload Fixture Mirror

Goal: Create LIMA-owned synthetic fixtures mirroring Sparkbot input payload shapes to reduce drift risk before real adapter work.

Acceptance criteria:

- synthetic fixtures exist
- Sparkbot commit recorded
- fixture tests pass
- no Sparkbot imports
- production adapter remains blocked

### Phase 1.22: Payload Drift Check Contract

Goal: Define repeatable payload drift review between LIMA-owned fixtures and Sparkbot origin/main before real adapter work.

Acceptance criteria:

- drift contract/doc exists
- fixture metadata includes drift fields
- dirty worktree rule exists
- tests pass
- production adapter remains blocked

### Phase 1.23: Adapter Boundary Hardening

Goal: Add tests preventing unsafe imports and behavior-bearing methods from entering lima/adapters.

Acceptance criteria:

- adapter boundary tests exist
- no Sparkbot imports
- no route wiring
- no model/tool execution
- no terminal/PTY
- no persistence
- tests pass

### Phase 1.24: Phase One Adapter Safety Review

Goal: Review adapter safety work and decide whether Phase 1 can close.

Deliverables:

- docs/PHASE_1_24_PHASE_ONE_ADAPTER_SAFETY_REVIEW.md
- Sparkbot freshness check
- adapter safety summary
- fixture/drift status
- identity/trust status
- Phase 2 recommendation
- no-go list

Acceptance criteria:

- production adapter remains blocked
- Phase 2 start defined
- tests pass
- no runtime behavior added

### Phase 2.0: Non-production Adapter Fixture Harness

Goal: Create a fixture-only harness proving LIMA-owned Sparkbot payload fixtures can flow through SparkbotHumanInputAdapter, HumanInputFakePipelineBridge, FakeGuardianPipeline, and fake lineage.

Acceptance criteria:

- fixture harness exists
- no Sparkbot imports
- no production wiring
- no execution
- critical/unknown requests do not auto-approve
- tests pass

### Phase 2.1: Fixture Harness Coverage Review

Goal: Review fixture and harness coverage before expanding the non-production harness.

Deliverables:

- `docs/PHASE_2_1_FIXTURE_HARNESS_COVERAGE_REVIEW.md`
- Sparkbot freshness check
- coverage matrix
- gap decision
- recommended Phase 2.2 branch
- still-blocked list

Acceptance criteria:

- coverage review exists
- Sparkbot origin/main checked
- production adapter remains blocked
- next safe branch identified
- no runtime behavior added
- tests pass

### Phase 2.2: Fixture Coverage Expansion

Goal: Add synthetic fixtures for frontend chat, Workstation, SparkBud, auth/session context, and model-routing/autonomous pacing context.

Acceptance criteria:

- new fixture categories exist
- tests cover fixture metadata
- safe harness handling exists
- no runtime behavior added
- production adapter remains blocked

### Phase 2.3: Harness Coverage Readiness Review

Goal: Review expanded fixture/harness coverage and decide whether to build a fixture regression harness.

Deliverables:

- `docs/PHASE_2_3_HARNESS_COVERAGE_READINESS_REVIEW.md`
- Sparkbot freshness check
- coverage readiness matrix
- Phase 2.4 recommendation
- still-blocked list
- risk register

Acceptance criteria:

- coverage reviewed
- Sparkbot origin/main checked
- production adapter remains blocked
- next safe branch identified
- tests pass
- no runtime behavior added

### Phase 2.4: Fixture Regression Harness

Goal: Add non-production regression harness over all LIMA-owned Sparkbot payload fixtures.

Acceptance criteria:

- all fixtures loaded
- compatible fixtures run through harness
- unsupported categories explicit
- critical/unknown no auto-approval
- no Sparkbot imports
- no production wiring
- tests pass

### Phase 2.5: Fixture Regression Readiness Review

Goal: Review whether the fixture regression harness is ready to become a standing safety gate for future adapter work.

Deliverables:

- `docs/PHASE_2_5_FIXTURE_REGRESSION_READINESS_REVIEW.md`
- Sparkbot freshness check
- regression status summary
- safety gate decision
- Phase 2.6 recommendation
- still-blocked list

Acceptance criteria:

- regression harness reviewed
- Sparkbot origin/main checked
- safety gate decision documented
- production adapter remains blocked
- no runtime behavior added
- tests pass

### Phase 2.6: Fixture Regression CI Gate Docs

Goal: Document fixture regression as required safety gate before adapter-adjacent changes.

Deliverables:

- `docs/PHASE_2_6_FIXTURE_REGRESSION_CI_GATE_DOCS.md`
- required test list
- PR blocking conditions
- manual review requirements
- non-production reminder

Acceptance criteria:

- docs exist
- production adapter remains blocked
- tests pass
- no runtime behavior added

### Phase 2.7: Phase Two Readiness Review

Goal: Review Phase 2 progress and choose next safe branch.

Deliverables:

- `docs/PHASE_2_7_PHASE_TWO_READINESS_REVIEW.md`
- Sparkbot freshness check
- Phase 2 proven/not-proven list
- safety gate status
- Phase 2.8 recommendation
- still-blocked list

Acceptance criteria:

- review exists
- Sparkbot origin/main checked
- production adapter remains blocked
- next safe branch identified
- no runtime behavior added
- tests pass

### Phase 2.8: Fixture Regression Report Artifact

Goal: Add test-only report helpers for fixture regression results.

Acceptance criteria:

- markdown/dict report helpers exist
- report includes safety notice
- no file writes by default
- report is not audit persistence
- tests pass

### Phase 2.9: Regression Report Readiness Review

Goal: Review fixture regression report artifact readiness before using it as a standing adapter review artifact.

Deliverables:

- `docs/PHASE_2_9_REGRESSION_REPORT_READINESS_REVIEW.md`
- readiness decision
- report status
- gap list
- recommended Phase 2.10 branch
- still-blocked list

Acceptance criteria:

- review exists
- production adapter remains blocked
- report remains non-persistent/non-production
- tests pass

### Phase 2.10: Regression Report Gate Hardening

Goal: Add explicit gate/review context to fixture regression report outputs.

Acceptance criteria:

- gate fields present
- markdown/dict reports include gate context
- report remains non-production
- no file writes by default
- tests pass

### Phase 2.11: Regression Gate Readiness Review

Goal: Review whether the fixture regression report gate is strong enough to serve as the standing adapter-adjacent safety gate.

Deliverables:

- `docs/PHASE_2_11_REGRESSION_GATE_READINESS_REVIEW.md`
- Sparkbot freshness check
- current gate status
- proven/not-proven list
- Phase 2.12 recommendation
- still-blocked list

Acceptance criteria:

- review exists
- Sparkbot origin/main checked
- production adapter remains blocked
- next safe branch identified
- no runtime behavior added
- tests pass

### Phase 2.12: Adapter Safety Gate Finalization

Goal: Consolidate adapter safety rules into one standing safety gate doc.

Deliverables:

- `docs/ADAPTER_SAFETY_GATE.md`
- `docs/PHASE_2_12_ADAPTER_SAFETY_GATE_FINALIZATION.md`
- adapter safety gate doc tests

Acceptance criteria:

- consolidated gate doc exists
- required checks listed
- forbidden imports/behaviors listed
- production adapter remains blocked
- tests pass
- no runtime behavior added

### Phase 2.13: Adapter Safety Gate Readiness Review

Goal: Review whether `docs/ADAPTER_SAFETY_GATE.md` is sufficient as the standing adapter-adjacent safety gate.

Deliverables:

- `docs/PHASE_2_13_ADAPTER_SAFETY_GATE_READINESS_REVIEW.md`
- Sparkbot freshness check
- gate status summary
- readiness decision
- recommended next area
- still-blocked list

Acceptance criteria:

- review exists
- Sparkbot origin/main checked
- production adapter remains blocked
- next safe branch identified
- no runtime behavior added
- tests pass

### Phase 2.14: IntentEnvelope Test Design Review

Goal: Design the next safe kernel boundary for HumanInput-to-IntentEnvelope testing without real IntentCompiler or natural-language inference.

Deliverables:

- `docs/PHASE_2_14_INTENT_ENVELOPE_TEST_DESIGN_REVIEW.md`
- IntentEnvelope boundary decision
- explicit typed intent metadata design
- raw_text inference block
- Phase 2.15 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no natural-language inference
- no model/tool execution
- adapter remains HumanInput-only
- tests pass

### Phase 2.15: IntentEnvelope Test Fixtures

Goal: Add synthetic fixtures for explicit typed intent metadata and expected IntentEnvelope shapes.

Acceptance criteria:

- fixtures exist
- explicit typed metadata only
- raw_text not parsed
- no real IntentCompiler
- no GuardianDecision
- tests pass

### Phase 2.16: IntentEnvelope Fixture Readiness Review

Goal: Review IntentEnvelope test fixtures before creating a test-only fixture harness.

Deliverables:

- `docs/PHASE_2_16_INTENTENVELOPE_FIXTURE_READINESS_REVIEW.md`
- fixture inventory
- coverage assessment
- readiness decision
- Phase 2.17 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no real IntentCompiler
- no natural-language inference
- no execution
- tests pass

### Phase 2.17: IntentEnvelope Fixture Harness

Goal: Add a test-only harness validating explicit typed intent metadata and expected IntentEnvelope fixture shapes.

Acceptance criteria:

- test-only harness exists
- no real IntentCompiler
- no natural-language inference
- raw_text not parsed
- no GuardianDecision
- tests pass

### Phase 2.18: IntentEnvelope Harness Readiness Review

Goal: Review the test-only IntentEnvelope fixture harness and decide whether it is ready to become a standing safety gate.

Deliverables:

- `docs/PHASE_2_18_INTENTENVELOPE_HARNESS_READINESS_REVIEW.md`
- harness status summary
- proven/not-proven list
- readiness decision
- Phase 2.19 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no real IntentCompiler
- no natural-language inference
- tests pass

### Phase 2.19: IntentEnvelope Safety Gate Docs

Goal: Create a standing safety gate for IntentEnvelope-adjacent work.

Acceptance criteria:

- gate doc exists
- tests validate gate doc
- real IntentCompiler remains blocked
- no runtime behavior added
- tests pass

### Phase 2.20: IntentEnvelope Safety Gate Readiness Review

Goal: Review whether `docs/INTENTENVELOPE_SAFETY_GATE.md` is sufficient as the standing gate for IntentEnvelope-adjacent work.

Deliverables:

- `docs/PHASE_2_20_INTENTENVELOPE_SAFETY_GATE_READINESS_REVIEW.md`
- current gate status
- proven/not-proven list
- readiness decision
- Phase 2.21 recommendation
- still-blocked list

Acceptance criteria:

- review exists
- no runtime behavior added
- no real IntentCompiler
- no natural-language inference
- production behavior remains blocked
- tests pass

### Phase 2.21: Guardian Request Test Design Review

Goal: Design test-only Guardian request shape after IntentEnvelope, without real GuardianDecision or enforcement.

Deliverables:

- `docs/PHASE_2_21_GUARDIAN_REQUEST_TEST_DESIGN_REVIEW.md`
- Guardian request boundary rule
- proposed test shape
- risk/safety rules
- Phase 2.22 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no GuardianDecision creation
- no enforcement
- no execution
- tests pass

### Phase 2.22: Guardian Request Test Fixtures

Goal: Add synthetic fixtures for expected Guardian request shapes after IntentEnvelope.

Acceptance criteria:

- fixtures exist
- request shape fields present
- Guardian request remains non-authorizing
- no GuardianDecision
- no approval/enforcement/execution
- tests pass

### Phase 2.23: Guardian Request Fixture Readiness Review

Goal: Review Guardian request fixtures before creating a test-only Guardian request fixture harness.

Deliverables:

- docs/PHASE_2_23_GUARDIAN_REQUEST_FIXTURE_READINESS_REVIEW.md
- fixture inventory
- coverage assessment
- readiness decision
- Phase 2.24 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no GuardianDecision
- no enforcement
- no approval
- no execution
- tests pass

### Phase 2.24: Guardian Request Fixture Harness

Goal: Add a test-only harness validating explicit Guardian request fixture shapes.

Acceptance criteria:

- test-only harness exists
- no GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

### Phase 2.25: Guardian Request Harness Readiness Review

Goal: Review the test-only Guardian request fixture harness and decide whether it is ready to become a standing safety gate.

Deliverables:

- docs/PHASE_2_25_GUARDIAN_REQUEST_HARNESS_READINESS_REVIEW.md
- harness status summary
- proven/not-proven list
- readiness decision
- Phase 2.26 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

### Phase 2.26: Guardian Request Safety Gate Docs

Goal: Create a standing safety gate for Guardian-request-adjacent work.

Acceptance criteria:

- gate doc exists
- tests validate gate doc
- real GuardianDecision remains blocked
- no runtime behavior added
- tests pass

### Phase 2.27: Guardian Request Safety Gate Readiness Review

Goal: Review whether `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` is sufficient as the standing safety gate for Guardian-request-adjacent work.

Deliverables:

- docs/PHASE_2_27_GUARDIAN_REQUEST_SAFETY_GATE_READINESS_REVIEW.md
- current gate status
- proven/not-proven list
- readiness decision
- Phase 2.28 recommendation
- still-blocked list

Acceptance criteria:

- review exists
- no runtime behavior added
- no GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

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

## Phase 2.28 — Fake GuardianDecision Test Design Review

Goal:

Design fake/test GuardianDecision fixture shapes without creating real GuardianDecision or enforcement.

Deliverables:

- `docs/PHASE_2_28_FAKE_GUARDIANDECISION_TEST_DESIGN_REVIEW.md`
- fake GuardianDecision boundary rule
- proposed fake decision shape
- decision status rules
- safety/risk rules
- Phase 2.29 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

## Phase 2.29 — Fake GuardianDecision Test Fixtures

Goal:

Add synthetic fixtures for fake/test GuardianDecision shapes while keeping real GuardianDecision blocked.

Acceptance criteria:

- fixtures exist
- statuses are test-only
- fake decision is not production authorization
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

## Phase 2.30 — Fake GuardianDecision Fixture Readiness Review

Goal:

Review fake GuardianDecision fixtures before creating a test-only fixture harness.

Deliverables:

- `docs/PHASE_2_30_FAKE_GUARDIANDECISION_FIXTURE_READINESS_REVIEW.md`
- tag/milestone check
- fixture inventory
- coverage assessment
- readiness decision
- Phase 2.31 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

## Phase 2.31 — Fake GuardianDecision Fixture Harness

Goal:

Add a test-only harness validating fake GuardianDecision fixture shapes and test-only statuses.

Acceptance criteria:

- test-only harness exists
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

## Phase 2.32 — Fake GuardianDecision Harness Readiness Review

Goal:

Review the test-only fake GuardianDecision fixture harness and decide whether it is ready to become a standing safety gate.

Deliverables:

- `docs/PHASE_2_32_FAKE_GUARDIANDECISION_HARNESS_READINESS_REVIEW.md`
- harness status summary
- proven/not-proven list
- readiness decision
- Phase 2.33 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

## Phase 2.33 — Fake GuardianDecision Safety Gate Docs

Goal:

Create a standing safety gate for fake GuardianDecision-adjacent work.

Acceptance criteria:

- gate doc exists
- tests validate gate doc
- real GuardianDecision remains blocked
- no runtime behavior added
- tests pass

## Phase 2.34 — Fake GuardianDecision Safety Gate Readiness Review

Goal:

Review whether `docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md` is sufficient as the standing gate for fake GuardianDecision-adjacent work.

Deliverables:

- `docs/PHASE_2_34_FAKE_GUARDIANDECISION_SAFETY_GATE_READINESS_REVIEW.md`
- current gate status
- proven/not-proven list
- readiness decision
- Phase 2.35 recommendation
- still-blocked list

Acceptance criteria:

- review exists
- no runtime behavior added
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass

## Phase 2.35 — Phase Two Final Readiness Review

Goal:

Review all Phase 2 non-production kernel boundary work and decide whether Phase 3 can begin.

Deliverables:

- `docs/PHASE_2_35_PHASE_TWO_FINAL_READINESS_REVIEW.md`
- standing gate summary
- proven/not-proven list
- validation baseline
- Phase 3 readiness decision
- Phase 3.0 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- Phase 3.0 scope defined
- production integration remains blocked
- tests pass

## Phase 3.0 — Non-production Kernel Pipeline Design Review

Goal:

Design the end-to-end non-production kernel fixture pipeline without implementing runtime behavior.

Deliverables:

- `docs/PHASE_3_0_NONPRODUCTION_KERNEL_PIPELINE_DESIGN_REVIEW.md`
- Phase 2 baseline
- pipeline design path
- boundary responsibility table
- required gate list
- Phase 3.1 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no production integration
- no real IntentCompiler
- no real GuardianDecision
- no enforcement
- no execution
- tests pass

## Phase 3.1 — Non-production Kernel Pipeline Fixture Map

Goal:

Map fixture families across the proposed non-production kernel pipeline without implementing runtime behavior.

Acceptance criteria:

- fixture map doc exists
- compatibility matrix exists
- safety gates listed
- no runtime behavior added
- tests pass

## Phase 3.2 — Non-production Kernel Pipeline Map Readiness Review

Goal:

Review the Phase 3.1 fixture map before adding relationship metadata.

Deliverables:

- `docs/PHASE_3_2_NONPRODUCTION_KERNEL_PIPELINE_MAP_READINESS_REVIEW.md`
- Phase 3.1 tag check
- map status
- proven/not-proven list
- Phase 3.3 recommendation

Acceptance criteria:

- review exists
- no runtime behavior added
- no pipeline implementation
- production integration remains blocked
- tests pass

## Phase 3.3 — Non-production Kernel Pipeline Relationship Metadata

Goal:

Add non-runtime relationship metadata across fixture families.

Acceptance criteria:

- relationship metadata exists
- metadata is non_runtime
- safety gates referenced
- no runtime behavior added
- tests pass

Status:

- complete
- tagged as `phase-3.3-nonproduction-kernel-pipeline-relationship-metadata`

## Phase 3.4 - Non-production Kernel Pipeline Relationship Metadata Readiness Review

Goal:

Review the Phase 3.3 relationship metadata before future non-production report/map artifact work.

Deliverables:

- `docs/PHASE_3_4_NONPRODUCTION_KERNEL_PIPELINE_RELATIONSHIP_METADATA_READINESS_REVIEW.md`
- readiness review fixture
- readiness review tests

Acceptance criteria:

- relationship metadata remains non-runtime
- no runtime behavior added
- no executable pipeline added
- no production integration added
- no composition harness added
- safety gates referenced
- tests pass

Status:

- complete
- tagged as `phase-3.4-nonproduction-kernel-pipeline-relationship-metadata-readiness-review`

## Phase 3.5 - LIMA Product Family and Adaptive Trust Doctrine

Goal:

Document the non-runtime product-family, adaptive trust, breakglass evolution, and human-safety doctrine for LIMA AI OS.

Deliverables:

- `docs/LIMA_PRODUCT_FAMILY.md`
- `docs/HUMAN_SAFETY_DOCTRINE.md`
- `docs/ADAPTIVE_TRUST_GATES.md`
- `docs/BREAKGLASS_EVOLUTION.md`
- `docs/PHASE_3_5_LIMA_PRODUCT_FAMILY_ADAPTIVE_TRUST_DOCTRINE.md`
- product-family fixture
- adaptive trust gate fixture
- human-safety doctrine fixture
- doctrine metadata tests

Acceptance criteria:

- docs/tests/fixtures only
- no runtime behavior added
- no Sparkbot import or wiring
- ARC Bot remains future shell doctrine only
- custom business/private-sector bots remain future shell doctrine only
- Robo/automation consumers remain future driver-plane doctrine only
- adaptive trust gates remain doctrine only
- breakglass behavior remains unchanged
- human-safety doctrine remains non-runtime and non-executable
- tests pass

Next likely phase:

- return to non-production pipeline report/map artifact work unless a readiness review says otherwise

Status:

- complete
- tagged as `phase-3.5-lima-product-family-adaptive-trust-doctrine`

## Phase 3.6 - Non-production Kernel Pipeline Report Map Artifact

Goal:

Add a static, non-runtime report/map artifact summarizing the current non-production kernel pipeline fixture path, relationship metadata, readiness status, known gaps, and doctrine references.

Deliverables:

- `docs/KERNEL_PIPELINE_REPORT_MAP_ARTIFACT.md`
- `docs/PHASE_3_6_NONPRODUCTION_KERNEL_PIPELINE_REPORT_MAP_ARTIFACT.md`
- `tests/fixtures/kernel_pipeline/pipeline_report_map_artifact.json`
- report/map artifact tests

Acceptance criteria:

- docs/tests/fixtures only
- no runtime behavior added
- no report generator added
- no executable pipeline added
- no test-only composition harness added
- no Sparkbot import or wiring
- no ARC Bot implementation
- no custom bot implementation
- no robot control or Robo-OS driver behavior
- no adaptive trust enforcement
- no approval, execution, enforcement, or audit persistence
- Phase 3.3 relationships remain `non_runtime: true`
- Phase 3.4 readiness metadata remains non-runtime
- Phase 3.5 doctrine metadata remains non-runtime
- tests pass

Ready for:

- non-production pipeline composition safety gate documentation
- further non-runtime review of the mapped fixture path
- future readiness review before any test-only harness

Not ready for:

- executable pipeline
- test-only composition harness
- runtime composition
- production Sparkbot integration
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence
- ARC Bot implementation
- custom bot implementation
- robot control
- physical-world action

Next likely phase:

- Phase 3.7 - Pipeline Composition Safety Gate Docs

Status:

- complete
- tagged as `phase-3.6-nonproduction-kernel-pipeline-report-map-artifact`

## Phase 3.7 - Pipeline Composition Safety Gate Docs

Goal:

Add a standing non-runtime safety gate for future kernel pipeline composition work.

Deliverables:

- `docs/PIPELINE_COMPOSITION_SAFETY_GATE.md`
- `docs/PHASE_3_7_PIPELINE_COMPOSITION_SAFETY_GATE_DOCS.md`
- `tests/fixtures/kernel_pipeline/pipeline_composition_safety_gate.json`
- safety gate tests

Acceptance criteria:

- docs/tests/fixtures only
- no runtime behavior added
- no executable pipeline added
- no test-only composition harness added
- no Sparkbot import or wiring
- no real IntentCompiler or GuardianDecision
- no model calls or tool execution
- no approval, enforcement, execution, or audit persistence
- no ARC Bot, LIMA AI Office, custom bot, robot, drone, IoT, or physical-world implementation
- future harness conditions require later readiness review
- tests pass

Next likely phase:

- Phase 3.8 - Pipeline Composition Safety Gate Readiness Review

Status:

- complete
- tagged as `phase-3.7-pipeline-composition-safety-gate-docs`

## Phase 3.8 - Pipeline Composition Safety Gate Readiness Review

Goal:

Review the Phase 3.7 Pipeline Composition Safety Gate before any final Phase 3 readiness decision.

Deliverables:

- `docs/PIPELINE_COMPOSITION_SAFETY_GATE_READINESS_REVIEW.md`
- `docs/PHASE_3_8_PIPELINE_COMPOSITION_SAFETY_GATE_READINESS_REVIEW.md`
- `tests/fixtures/kernel_pipeline/pipeline_composition_safety_gate_readiness_review.json`
- readiness review tests

Acceptance criteria:

- docs/tests/fixtures only
- no runtime behavior added
- no executable pipeline added
- no test-only composition harness added
- no Sparkbot import or wiring
- no product shell implementation
- no robot, drone, IoT, or physical-world control
- no approval, enforcement, execution, or audit persistence
- readiness result identifies Phase 3 final readiness review as the next safe step
- tests pass

Next likely phase:

- Phase 3 final readiness review

Status:

- complete
- tagged as `phase-3.8-pipeline-composition-safety-gate-readiness-review`

## Phase 3.9 - Final Readiness Review

Goal:

Review Phase 3 as a whole and decide whether Phase 4 planning may begin.

Deliverables:

- `docs/PHASE_3_FINAL_READINESS_REVIEW.md`
- `docs/PHASE_3_9_FINAL_READINESS_REVIEW.md`
- `tests/fixtures/kernel_pipeline/phase_3_final_readiness_review.json`
- final readiness review tests

Acceptance criteria:

- docs/tests/fixtures only
- no runtime behavior added
- no executable pipeline added
- no test-only composition harness added
- no Sparkbot import or wiring
- no product shell implementation
- no robot, drone, IoT, or physical-world control
- no approval, enforcement, execution, or audit persistence
- Phase 4 is recommended for planning only
- tests pass

Next likely phase:

- Phase 4.0 - Runtime Extraction Readiness Planning

Status:

- complete
- tagged as `phase-3.9-final-readiness-review`

## Phase 4.0 - Runtime Extraction Readiness Planning

Goal:

Define the safe Phase 4 runtime-extraction readiness sequence before moving any behavior.

Deliverables:

- `docs/PHASE_4_0_RUNTIME_EXTRACTION_READINESS_PLANNING.md`
- `tests/fixtures/runtime_extraction/phase_4_0_runtime_extraction_readiness_planning.json`
- planning tests
- project tracking updates

Acceptance criteria:

- docs/tests/fixtures only
- no runtime behavior added
- no Sparkbot import or wiring
- no production route imports
- no model calls or tool execution
- no terminal or PTY execution
- no real IntentCompiler or GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no product shell implementation
- no robot, drone, IoT, or physical-world control
- recommended Phase 4.1 is read-only Sparkbot Runtime Reference Refresh
- tests pass

Next likely phase:

- Phase 4.1 - Sparkbot Runtime Reference Refresh

Status:

- complete
- tagged as `phase-4.1-sparkbot-runtime-reference-refresh`

## Phase 4.1 - Sparkbot Runtime Reference Refresh

Goal:

Refresh Sparkbot runtime reference knowledge as read-only planning material before choosing any extraction candidate.

Deliverables:

- `docs/PHASE_4_1_SPARKBOT_RUNTIME_REFERENCE_REFRESH.md`
- `tests/fixtures/runtime_extraction/phase_4_1_sparkbot_runtime_reference_refresh.json`
- static reference-refresh tests
- project tracking updates

Acceptance criteria:

- docs/tests/fixtures only
- local Sparkbot is inspected read-only
- no Sparkbot files modified
- no Sparkbot code copied into LIMA
- no Sparkbot import or wiring
- no production route imports
- no model calls or tool execution
- no terminal or PTY execution
- no robotics command execution
- no real IntentCompiler or GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no product shell implementation
- no robot, drone, IoT, or physical-world control
- recommended Phase 4.2 is Runtime Boundary Candidate Selection
- tests pass

Next likely phase:

- Phase 4.2 - Runtime Boundary Candidate Selection

Status:

- complete
- tagged as `phase-4.2-runtime-boundary-candidate-selection`

## Phase 4.2 - Runtime Boundary Candidate Selection

Goal:

Select the first runtime boundary candidate to carry into a safety gate before any extraction work.

Deliverables:

- `docs/PHASE_4_2_RUNTIME_BOUNDARY_CANDIDATE_SELECTION.md`
- `tests/fixtures/runtime_extraction/phase_4_2_runtime_boundary_candidate_selection.json`
- static candidate-selection tests
- project tracking updates

Acceptance criteria:

- docs/tests/fixtures only
- selected candidate is HumanInput intake boundary for chat and voice
- candidate is selected for a safety gate, not extraction
- no Sparkbot files modified
- no Sparkbot code copied into LIMA
- no Sparkbot import or wiring
- no production route imports
- no model calls or tool execution
- no terminal or PTY execution
- no robotics command execution
- no real IntentCompiler or GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no product shell implementation
- no robot, drone, IoT, or physical-world control
- recommended Phase 4.3 is Boundary Extraction Safety Gate
- tests pass

Next likely phase:

- Phase 4.3 - Boundary Extraction Safety Gate

Status:

- complete
- tagged as `phase-4.3-boundary-extraction-safety-gate`

## Phase 4.3 - Boundary Extraction Safety Gate

Goal:

Define the safety gate for the selected HumanInput intake boundary before any fixture/contract extension or extraction work.

Deliverables:

- `docs/PHASE_4_3_BOUNDARY_EXTRACTION_SAFETY_GATE.md`
- `tests/fixtures/runtime_extraction/phase_4_3_boundary_extraction_safety_gate.json`
- static safety gate tests
- project tracking updates

Acceptance criteria:

- docs/tests/fixtures only
- selected candidate remains HumanInput intake boundary for chat and voice
- gate permits only Phase 4.4 fixture/contract extension if explicitly approved
- no Sparkbot files modified
- no Sparkbot code copied into LIMA
- no Sparkbot import or wiring
- no production route imports
- no model calls or tool execution
- no terminal or PTY execution
- no robotics command execution
- no real IntentCompiler or GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no live auth/session/trust lookup
- no product shell implementation
- no robot, drone, IoT, or physical-world control
- tests pass

Next possible phase:

- Phase 4.4 - Boundary Fixture Contract Extension, if explicitly approved

Status:

- complete
- tagged as `phase-4.4-boundary-fixture-contract-extension`
- hardened and tagged as `phase-4.4-boundary-fixture-contract-hardening`

## Phase 4.4 - Boundary Fixture Contract Extension

Goal:

Extend synthetic HumanInput intake fixture/contract metadata for the selected chat and voice boundary while keeping all behavior blocked.

Deliverables:

- `docs/PHASE_4_4_BOUNDARY_FIXTURE_CONTRACT_EXTENSION.md`
- `tests/fixtures/runtime_extraction/phase_4_4_humaninput_intake_fixture_contract.json`
- static inertness and boundary tests
- project tracking updates

Acceptance criteria:

- docs/tests/fixtures only
- synthetic text input fixture shape exists
- synthetic voice transcript fixture shape exists
- source, actor, session, trust, privacy, lineage, and handoff metadata are reference-only
- fixtures cannot imply authorization, approval, execution, trust lookup, or production integration
- no Sparkbot files modified
- no Sparkbot code copied into LIMA
- no live adapter code
- no Sparkbot import or wiring
- no production route imports
- no model calls or tool execution
- no terminal or PTY behavior
- no robotics behavior
- no live auth/session/trust lookup
- no real IntentCompiler or GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no product shell implementation
- no robot, drone, IoT, or physical-world control
- tests pass

Next likely phase:

- Phase 4.5 - Boundary Readiness Review

Status:

- complete
- tagged as `phase-4.5-boundary-readiness-review`

## Phase 4.5 - Boundary Readiness Review

Goal:

Review the selected HumanInput intake boundary after Phase 4.4 fixture/contract extension and decide whether it is ready for a future explicitly approved narrow non-production proposal.

Deliverables:

- `docs/PHASE_4_5_BOUNDARY_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_4_5_boundary_readiness_review.json`
- static readiness review tests
- project tracking updates

Acceptance criteria:

- docs/tests/fixtures only
- HumanInput intake remains non-authorizing input
- readiness is conditional on explicit operator approval for any next narrow non-production phase
- no Sparkbot files modified
- no Sparkbot code copied into LIMA
- no live adapter code
- no Sparkbot import or wiring
- no production route imports
- no model calls or tool execution
- no terminal or PTY behavior
- no robotics behavior
- no live auth/session/trust lookup
- no real IntentCompiler or GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no product shell implementation
- no robot, drone, IoT, or physical-world control
- tests pass

Next gate:

- Phase 4.6 - Non-production HumanInput Adapter Proposal, explicitly approved as docs/tests/fixtures only

Status:

- complete
- tagged as `phase-4.5-boundary-readiness-review`

## Phase 4.6 - Non-production HumanInput Adapter Proposal

Goal:

Add a non-production proposal describing how a future shell intake adapter could convert selected shell input context into the existing HumanInput boundary fixture/contract shape.

Deliverables:

- `docs/PHASE_4_6_NONPRODUCTION_HUMANINPUT_ADAPTER_PROPOSAL.md`
- `tests/fixtures/runtime_extraction/phase_4_6_humaninput_adapter_proposal.json`
- `tests/test_phase_4_6_humaninput_adapter_proposal.py`

Acceptance criteria:

- docs/tests/fixtures only
- proposal is metadata only
- proposal is not a HumanInput adapter
- no files under `lima/` are modified
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no model calls
- no tool execution
- no terminal or PTY behavior
- no robotics or physical-world behavior
- no live auth/session/trust lookup
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- Phase 4.4 HumanInput fixture contract remains synthetic, inert, and non-runtime
- Phase 4.5 readiness review remains non-runtime
- tests pass

Next gate:

- STOP for explicit operator approval before any next narrow non-production phase

Status:

- complete
- tagged as `phase-4.6-nonproduction-humaninput-adapter-proposal`

## Phase 4.7 - Non-production HumanInput Adapter Proposal Readiness Review

Goal:

Review whether the Phase 4.6 HumanInput adapter proposal is clear, safe, constrained, and explicitly non-runtime enough before future adapter safety gate documentation.

Deliverables:

- `docs/PHASE_4_7_NONPRODUCTION_HUMANINPUT_ADAPTER_PROPOSAL_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_4_7_humaninput_adapter_proposal_readiness_review.json`
- `tests/test_phase_4_7_humaninput_adapter_proposal_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- readiness review is metadata only
- readiness review is not a HumanInput adapter
- Phase 4.4 HumanInput fixture contract remains synthetic, inert, and non-runtime
- Phase 4.5 readiness review remains non-runtime
- Phase 4.6 adapter proposal remains non-runtime
- ready-for scope is limited to future adapter safety gate docs or further non-runtime review
- no files under `lima/` are modified
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no model calls
- no tool execution
- no terminal or PTY behavior
- no robotics or physical-world behavior
- no live auth/session/trust lookup
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- tests pass

Next likely phase:

- Phase 4.8 - HumanInput Adapter Safety Gate Docs

Status:

- complete
- tagged as `phase-4.7-nonproduction-humaninput-adapter-proposal-readiness-review`

## Phase 4.8 - HumanInput Adapter Safety Gate Docs

Goal:

Define safety gate documentation for any future HumanInput adapter while keeping adapter code and runtime behavior blocked.

Deliverables:

- `docs/HUMANINPUT_ADAPTER_SAFETY_GATE.md`
- `docs/PHASE_4_8_HUMANINPUT_ADAPTER_SAFETY_GATE_DOCS.md`
- `tests/fixtures/runtime_extraction/phase_4_8_humaninput_adapter_safety_gate_docs.json`
- `tests/test_phase_4_8_humaninput_adapter_safety_gate_docs.py`

Acceptance criteria:

- docs/tests/fixtures only
- safety gate is metadata only
- adapter must return HumanInput only
- no files under `lima/` are modified
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- no live auth/session/trust lookup
- Phase 4.4 HumanInput fixture contract remains synthetic, inert, and non-runtime
- Phase 4.7 readiness review remains non-runtime and recommends safety gate docs only
- tests pass

Next gate:

- STOP for explicit operator approval before any next narrow non-production phase

Status:

- complete
- tagged as `phase-4.8-humaninput-adapter-safety-gate-docs`

## Phase 4.9 - HumanInput Adapter Implementation Readiness Review

Goal:

Review whether the HumanInput intake boundary, fixture contract, adapter proposal, readiness review, and safety gate are clear enough before any future test-only adapter harness proposal.

Deliverables:

- `docs/PHASE_4_9_HUMANINPUT_ADAPTER_IMPLEMENTATION_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_4_9_humaninput_adapter_implementation_readiness_review.json`
- `tests/test_phase_4_9_humaninput_adapter_implementation_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- readiness review is metadata only
- readiness review is not an adapter
- readiness review is not a test-only harness
- no files under `lima/` are modified
- no live adapter code
- no test-only adapter harness code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- no live auth/session/trust lookup
- Phase 4.4 HumanInput fixture contract remains synthetic, inert, and non-runtime
- Phase 4.8 safety gate remains non-runtime
- readiness is limited to a future explicitly approved test-only adapter harness proposal or further non-runtime review
- tests pass

Next gate:

- STOP for explicit operator approval before any next narrow non-production phase

Status:

- complete
- tagged as `phase-4.9-humaninput-adapter-implementation-readiness-review`

## Phase 4.10 - Non-production Test-only HumanInput Adapter Harness Proposal

Goal:

Propose a future test-only harness that could validate synthetic shell intake metadata against the HumanInput boundary fixture contract in a later explicitly approved phase.

Deliverables:

- `docs/PHASE_4_10_NONPRODUCTION_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_PROPOSAL.md`
- `tests/fixtures/runtime_extraction/phase_4_10_test_only_humaninput_adapter_harness_proposal.json`
- `tests/test_phase_4_10_test_only_humaninput_adapter_harness_proposal.py`

Acceptance criteria:

- docs/tests/fixtures only
- proposal metadata only
- no harness code
- no live adapter code
- no files under `lima/`
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- no live auth/session/trust lookup
- tests pass

Next likely phase:

- Phase 4.11 - Test-only HumanInput Adapter Harness Proposal Readiness Review

Status:

- complete
- tagged as `phase-4.10-nonproduction-test-only-humaninput-adapter-harness-proposal`

## Phase 4.11 - Test-only HumanInput Adapter Harness Proposal Readiness Review

Goal:

Review whether the Phase 4.10 test-only harness proposal is clear and safe enough for a future safety gate documentation phase.

Deliverables:

- `docs/PHASE_4_11_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_PROPOSAL_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_4_11_test_only_humaninput_adapter_harness_proposal_readiness_review.json`
- `tests/test_phase_4_11_test_only_humaninput_adapter_harness_proposal_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- readiness review metadata only
- no harness code
- no live adapter code
- no files under `lima/`
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- no live auth/session/trust lookup
- tests pass

Next likely phase:

- Phase 4.12 - Test-only HumanInput Adapter Harness Safety Gate Docs

Status:

- complete
- tagged as `phase-4.11-test-only-humaninput-adapter-harness-proposal-readiness-review`

## Phase 4.12 - Test-only HumanInput Adapter Harness Safety Gate Docs

Goal:

Define safety gate documentation for any future test-only HumanInput adapter harness.

Deliverables:

- `docs/TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_SAFETY_GATE.md`
- `docs/PHASE_4_12_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_SAFETY_GATE_DOCS.md`
- `tests/fixtures/runtime_extraction/phase_4_12_test_only_humaninput_adapter_harness_safety_gate_docs.json`
- `tests/test_phase_4_12_test_only_humaninput_adapter_harness_safety_gate_docs.py`

Acceptance criteria:

- docs/tests/fixtures only
- safety gate metadata only
- no harness implementation
- no live adapter implementation
- no files under `lima/`
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- no live auth/session/trust lookup
- test-only harness cannot imply production adapter readiness
- tests pass

Next likely phase:

- Phase 4.13 - Phase 4 HumanInput Boundary Readiness Review

Status:

- complete
- tagged as `phase-4.12-test-only-humaninput-adapter-harness-safety-gate-docs`

Reserved from Phase 3.4:

- Phase 3.5 - LIMA Product Family and Adaptive Trust Doctrine
- product-family and adaptive-trust doctrine is deferred and not implemented in Phase 3.4
- reserve LIMA AI OS as the trust-governed runtime underneath shells
- reserve Sparkbot as the open-source hobby/R&D shell and reference source
- reserve ARC Bot as a future commercial office-worker shell
- reserve custom business and private-sector bots as future client-specific shells
- reserve Robo/automation systems as future driver-plane consumers
- reserve adaptive trust gates as the default future UX, with breakglass as rare emergency or privileged override
