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

## Phase 4.13 - Phase 4 HumanInput Boundary Readiness Review

Goal:

Review the full HumanInput boundary lane and decide whether it is ready for a future explicitly approved test-only HumanInput adapter harness implementation phase or needs more non-runtime review.

Deliverables:

- `docs/PHASE_4_13_PHASE_4_HUMANINPUT_BOUNDARY_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_4_13_phase_4_humaninput_boundary_readiness_review.json`
- `tests/test_phase_4_13_phase_4_humaninput_boundary_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- readiness review metadata only
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
- ready-for list is limited to a future explicitly approved test-only harness implementation phase or further non-runtime review
- tests pass

Status:

- complete
- tagged as `phase-4.13-phase-4-humaninput-boundary-readiness-review`

## Phase 4.14 - Test-only HumanInput Adapter Harness Implementation

Goal:

Implement a deterministic test-only harness that validates synthetic shell intake fixture shapes against the HumanInput boundary fixture/contract shape.

Deliverables:

- `docs/PHASE_4_14_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_IMPLEMENTATION.md`
- `tests/support/test_only_humaninput_adapter_harness.py`
- `tests/fixtures/runtime_extraction/phase_4_14_test_only_humaninput_adapter_harness.json`
- `tests/test_phase_4_14_test_only_humaninput_adapter_harness.py`

Acceptance criteria:

- test-only helper code stays under `tests/`
- docs/tests/fixtures only outside test support
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- no live auth/session/trust lookup
- fail closed on missing synthetic/test-only/non-runtime markers
- tests pass

Next likely phase:

- Phase 4.15 - Test-only HumanInput Adapter Harness Implementation Readiness Review

Status:

- complete
- tagged as `phase-4.14-test-only-humaninput-adapter-harness-implementation`

## Phase 4.15 - Test-only HumanInput Adapter Harness Implementation Readiness Review

Goal:

Review whether the Phase 4.14 test-only HumanInput adapter harness remained constrained, deterministic, synthetic-only, and non-runtime.

Deliverables:

- `docs/PHASE_4_15_TEST_ONLY_HUMANINPUT_ADAPTER_HARNESS_IMPLEMENTATION_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_4_15_test_only_humaninput_adapter_harness_implementation_readiness_review.json`
- `tests/test_phase_4_15_test_only_humaninput_adapter_harness_implementation_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no new harness behavior unless fixing a safety bug under `tests/support/`
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- no live auth/session/trust lookup
- tests pass

Next likely phase:

- Phase 4.16 - HumanInput Boundary Lane Closeout Review

Status:

- complete
- tagged as `phase-4.15-test-only-humaninput-adapter-harness-implementation-readiness-review`

## Phase 4.16 - HumanInput Boundary Lane Closeout Review

Goal:

Close out the HumanInput boundary lane and decide whether it is complete enough to stop Phase 4 HumanInput work and propose the next explicitly approved lane, likely HumanInput to IntentEnvelope boundary planning.

Deliverables:

- `docs/PHASE_4_16_HUMANINPUT_BOUNDARY_LANE_CLOSEOUT_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_4_16_humaninput_boundary_lane_closeout_review.json`
- `tests/test_phase_4_16_humaninput_boundary_lane_closeout_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no new harness behavior
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no HumanInput to IntentEnvelope implementation
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- no live auth/session/trust lookup
- tests pass

Status:

- complete
- tagged as `phase-4.16-humaninput-boundary-lane-closeout-review`

## Phase 4.17 - HumanInput to IntentEnvelope Boundary Planning

Goal:

Open the HumanInput to IntentEnvelope boundary planning lane while preserving the standing IntentEnvelope safety gate.

Deliverables:

- `docs/PHASE_4_17_HUMANINPUT_TO_INTENTENVELOPE_BOUNDARY_PLANNING.md`
- `tests/fixtures/runtime_extraction/phase_4_17_humaninput_to_intentenvelope_boundary_planning.json`
- `tests/test_phase_4_17_humaninput_to_intentenvelope_boundary_planning.py`

Acceptance criteria:

- docs/tests/fixtures only
- planning only
- no schema implementation
- no bridge code
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- tests pass

Next likely phase:

- Phase 4.18 - HumanInput to IntentEnvelope Boundary Schema / Contract Proposal

Status:

- complete
- tagged as `phase-4.17-humaninput-to-intentenvelope-boundary-planning`

## Phase 4.18 - HumanInput to IntentEnvelope Boundary Schema / Contract Proposal

Goal:

Propose a static non-runtime boundary schema/contract for future test-only HumanInput to IntentEnvelope work.

Deliverables:

- `docs/PHASE_4_18_HUMANINPUT_TO_INTENTENVELOPE_BOUNDARY_SCHEMA_CONTRACT_PROPOSAL.md`
- `tests/fixtures/runtime_extraction/phase_4_18_humaninput_to_intentenvelope_boundary_schema_contract_proposal.json`
- `tests/test_phase_4_18_humaninput_to_intentenvelope_boundary_schema_contract_proposal.py`

Acceptance criteria:

- docs/tests/fixtures only
- schema/contract proposal only
- no bridge code
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- tests pass

Next likely phase:

- Phase 4.19 - HumanInput to IntentEnvelope Boundary Readiness Review

Status:

- complete
- tagged as `phase-4.18-humaninput-to-intentenvelope-boundary-schema-contract-proposal`

## Phase 4.19 - HumanInput to IntentEnvelope Boundary Readiness Review

Goal:

Review whether the Phase 4.18 HumanInput to IntentEnvelope boundary schema/contract proposal is clear, safe, constrained, and explicitly non-runtime enough before a Phase 5 gate / implementation readiness closeout.

Deliverables:

- `docs/PHASE_4_19_HUMANINPUT_TO_INTENTENVELOPE_BOUNDARY_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_4_19_humaninput_to_intentenvelope_boundary_readiness_review.json`
- `tests/test_phase_4_19_humaninput_to_intentenvelope_boundary_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- readiness review only
- no bridge code
- no test-only bridge code
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- tests pass

Next likely phase:

- Phase 4.20 - Phase 5 Gate / Implementation Readiness Closeout

Status:

- complete
- tagged as `phase-4.19-humaninput-to-intentenvelope-boundary-readiness-review`

## Phase 4.20 - Phase 5 Gate / Implementation Readiness Closeout

Goal:

Close the HumanInput to IntentEnvelope non-runtime planning lane at a clear Phase 5 gate and identify the operator decisions required before any Phase 5 runtime, test-only bridge, or implementation work.

Deliverables:

- `docs/PHASE_4_20_PHASE_5_GATE_IMPLEMENTATION_READINESS_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_4_20_phase_5_gate_implementation_readiness_closeout.json`
- `tests/test_phase_4_20_phase_5_gate_implementation_readiness_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 5 gate / implementation readiness closeout only
- no bridge code
- no test-only bridge code
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no model, tool, terminal, robot, or physical-world behavior
- tests pass

Next likely phase:

- explicit operator decision for Phase 5 scope

Status:

- complete
- tagged as `phase-4.20-phase-5-gate-implementation-readiness-closeout`

## Phase 5.0 - Phase 5 Scope Charter / HumanInput IntentEnvelope Boundary Decision Record

Goal:

Open Phase 5 as non-runtime planning only and record the approved HumanInput to IntentEnvelope boundary scope, human UX flow, approval semantics, trust/autonomy handling, and safety boundary.

Deliverables:

- `docs/PHASE_5_0_PHASE_5_SCOPE_CHARTER_HUMANINPUT_INTENTENVELOPE_BOUNDARY_DECISION_RECORD.md`
- `tests/fixtures/runtime_extraction/phase_5_0_phase_5_scope_charter_humaninput_intentenvelope_boundary_decision_record.json`
- `tests/test_phase_5_0_phase_5_scope_charter_humaninput_intentenvelope_boundary_decision_record.py`

Acceptance criteria:

- docs/tests/fixtures only
- scope charter / decision record only
- no bridge code
- no test-only bridge code
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, robot, or physical-world behavior
- tests pass

Next likely phase:

- Phase 5.1 - HumanInput to IntentEnvelope Contract Proposal

Status:

- complete
- tagged as `phase-5.0-phase-5-scope-charter-humaninput-intentenvelope-boundary-decision-record`

## Phase 5.1 - HumanInput to IntentEnvelope Contract Proposal

Goal:

Propose the HumanInput to IntentEnvelope contract as static non-runtime metadata, preserving source, operator intent, requested action, risk tier, approval state, and not-executable-yet status.

Deliverables:

- `docs/PHASE_5_1_HUMANINPUT_TO_INTENTENVELOPE_CONTRACT_PROPOSAL.md`
- `tests/fixtures/runtime_extraction/phase_5_1_humaninput_to_intentenvelope_contract_proposal.json`
- `tests/test_phase_5_1_humaninput_to_intentenvelope_contract_proposal.py`

Acceptance criteria:

- docs/tests/fixtures only
- contract proposal only
- no bridge code
- no test-only bridge code
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, robot, or physical-world behavior
- tests pass

Next likely phase:

- Phase 5.2 - Test-only Bridge Harness Proposal

## Phase 5.2 - Test-only Bridge Harness Proposal

Goal:

Propose a future test-only HumanInput to IntentEnvelope bridge harness as non-runtime metadata, without implementing the harness.

Deliverables:

- `docs/PHASE_5_2_TEST_ONLY_BRIDGE_HARNESS_PROPOSAL.md`
- `tests/fixtures/runtime_extraction/phase_5_2_test_only_bridge_harness_proposal.json`
- `tests/test_phase_5_2_test_only_bridge_harness_proposal.py`

Acceptance criteria:

- docs/tests/fixtures only
- harness proposal only
- no bridge implementation
- no test-only bridge code
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, robot, or physical-world behavior
- tests pass

Next likely phase:

- Phase 5.3 - Test-only Bridge Harness Readiness Review

Status:

- complete
- tagged as `phase-5.1-humaninput-to-intentenvelope-contract-proposal`

## Phase 5.3 - Test-only Bridge Harness Readiness Review

Goal:

Review whether the Phase 5.2 test-only bridge harness proposal is clear and safe enough to stop at an implementation gate before any harness code.

Deliverables:

- `docs/PHASE_5_3_TEST_ONLY_BRIDGE_HARNESS_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_5_3_test_only_bridge_harness_readiness_review.json`
- `tests/test_phase_5_3_test_only_bridge_harness_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- readiness review only
- no bridge implementation
- no test-only bridge code
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, robot, or physical-world behavior
- tests pass

Next likely phase:

- implementation gate requiring explicit operator approval

Status:

- complete
- tagged as `phase-5.2-test-only-bridge-harness-proposal`

Implementation gate status:

- Phase 5.3 complete
- tagged as `phase-5.3-test-only-bridge-harness-readiness-review`
- Phase 5.4 explicit operator approval received for test-only helper implementation only

## Phase 5.4 - Test-only HumanInput to IntentEnvelope Bridge Harness Implementation

Goal:

Implement a deterministic test-only HumanInput to IntentEnvelope bridge helper under `tests/support/`.

Deliverables:

- `docs/PHASE_5_4_TEST_ONLY_HUMANINPUT_TO_INTENTENVELOPE_BRIDGE_HARNESS_IMPLEMENTATION.md`
- `tests/fixtures/runtime_extraction/phase_5_4_test_only_humaninput_to_intentenvelope_bridge_harness_implementation.json`
- `tests/test_phase_5_4_test_only_humaninput_to_intentenvelope_bridge_harness_implementation.py`
- `tests/support/test_only_humaninput_to_intentenvelope_bridge.py`

Acceptance criteria:

- helper code lives under `tests/support/` only
- accepts only synthetic, test-only, non-runtime HumanInput-shaped dictionaries
- returns non-executable IntentEnvelope-candidate-shaped test dictionaries only
- preserves source, source channel, operator intent, requested action, raw text, risk tier, approval state, blocked reason, and provenance
- operator/admin/Phil/trusted wording does not bypass approval
- risky shell, browser, network, file mutation, robotics, and physical-world requests remain non-executable and approval-required
- missing or empty input fails closed
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 5.5 - explicit operator decision for readiness review or next narrow test-only scope

Status:

- complete
- tagged as `phase-5.4-test-only-humaninput-to-intentenvelope-bridge-harness-implementation`

## Phase 5.5 - Test-only Bridge Harness Readiness Review

Goal:

Review whether the Phase 5.4 test-only HumanInput to IntentEnvelope bridge helper remained constrained, deterministic, non-runtime, and unsuitable for live/runtime reuse.

Deliverables:

- `docs/PHASE_5_5_TEST_ONLY_BRIDGE_HARNESS_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_5_5_test_only_bridge_harness_readiness_review.json`
- `tests/test_phase_5_5_test_only_bridge_harness_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- readiness review only
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no runtime behavior
- no runtime reuse of the helper classifier
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 5.6 - explicit operator scope decision required

Status:

- complete
- tagged as `phase-5.5-test-only-bridge-harness-readiness-review`

## Phase 5.6 - HumanInput Runtime Bridge Safety Gate / Next-Scope Decision Record

Goal:

Define what, if anything, may follow the Phase 5.4 test-only helper and Phase 5.5 readiness review before any future live/runtime HumanInput to IntentEnvelope work.

Deliverables:

- `docs/PHASE_5_6_HUMANINPUT_RUNTIME_BRIDGE_SAFETY_GATE_NEXT_SCOPE_DECISION_RECORD.md`
- `tests/fixtures/runtime_extraction/phase_5_6_humaninput_runtime_bridge_safety_gate_next_scope_decision_record.json`
- `tests/test_phase_5_6_humaninput_runtime_bridge_safety_gate_next_scope_decision_record.py`

Acceptance criteria:

- docs/tests/fixtures only
- safety gate and next-scope decision record only
- Phase 5.4 helper remains test-only
- helper classifier is not approved for runtime reuse
- live/runtime HumanInput to IntentEnvelope implementation remains blocked
- any future runtime bridge requires explicit Phil approval
- any future runtime bridge must start with runtime design before implementation
- next safe lane, if approved later, is planning/design only
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 5.7 - explicit operator scope decision required

Status:

- complete
- tagged as `phase-5.6-humaninput-runtime-bridge-safety-gate-next-scope-decision-record`

## Phase 5.7 - HumanInput Runtime Bridge Design Proposal

Goal:

Document the shape of a future runtime HumanInput to IntentEnvelope bridge without implementing it.

Deliverables:

- `docs/PHASE_5_7_HUMANINPUT_RUNTIME_BRIDGE_DESIGN_PROPOSAL.md`
- `tests/fixtures/runtime_extraction/phase_5_7_humaninput_runtime_bridge_design_proposal.json`
- `tests/test_phase_5_7_humaninput_runtime_bridge_design_proposal.py`

Acceptance criteria:

- docs/tests/fixtures only
- design proposal only
- allowed inputs documented
- rejected inputs documented
- provenance requirements documented
- non-executable candidate requirements documented
- approval-required semantics documented
- risk-tier semantics documented
- trust/autonomy rules documented
- operator/admin/Phil/trusted wording cannot bypass approval
- live/runtime implementation remains blocked
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 5.8 - HumanInput Runtime Bridge Threat Model

Status:

- complete
- tagged as `phase-5.7-humaninput-runtime-bridge-design-proposal`

## Phase 5.8 - HumanInput Runtime Bridge Threat Model

Goal:

Threat-model a future HumanInput to IntentEnvelope runtime bridge without implementing it.

Deliverables:

- `docs/PHASE_5_8_HUMANINPUT_RUNTIME_BRIDGE_THREAT_MODEL.md`
- `tests/fixtures/runtime_extraction/phase_5_8_humaninput_runtime_bridge_threat_model.json`
- `tests/test_phase_5_8_humaninput_runtime_bridge_threat_model.py`

Acceptance criteria:

- docs/tests/fixtures only
- threat model only
- prompt injection covered
- operator impersonation covered
- trust bypass covered
- accidental execution covered
- shell/browser/network/file/robotics action escalation covered
- audit gaps covered
- approval confusion covered
- helper classifier misuse covered
- unsafe reuse of test-only code covered
- malformed, replayed, stale, and ambiguous input risks covered
- future runtime review and semantic tests required before live behavior
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 5.9 - HumanInput Runtime Bridge Boundary Validation Matrix

Status:

- complete
- tagged as `phase-5.8-humaninput-runtime-bridge-threat-model`

## Phase 5.9 - HumanInput Runtime Bridge Boundary Validation Matrix

Goal:

Define a machine-checkable matrix of allowed, blocked, approval-required, and rejected HumanInput categories for a future runtime bridge design.

Deliverables:

- `docs/PHASE_5_9_HUMANINPUT_RUNTIME_BRIDGE_BOUNDARY_VALIDATION_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_5_9_humaninput_runtime_bridge_boundary_validation_matrix.json`
- `tests/test_phase_5_9_humaninput_runtime_bridge_boundary_validation_matrix.py`

Acceptance criteria:

- docs/tests/fixtures only
- validation matrix only
- low-risk informational request included
- shell command request included
- browser/network request included
- file mutation request included
- robotics/physical-world request included
- admin/trusted/Phil bypass attempt included
- ambiguous request included
- empty request included
- malformed request included
- replayed/stale request included
- every row is non-executable
- side-effect-bearing rows require approval or are blocked
- empty, malformed, replayed, or stale rows are rejected or blocked
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 5.10 - Runtime Bridge Implementation Gate / Closeout Review

Status:

- complete
- tagged as `phase-5.9-humaninput-runtime-bridge-boundary-validation-matrix`

## Phase 5.10 - Runtime Bridge Implementation Gate / Closeout Review

Goal:

Close the Phase 5 HumanInput runtime bridge design lane with an implementation gate.

Deliverables:

- `docs/PHASE_5_10_RUNTIME_BRIDGE_IMPLEMENTATION_GATE_CLOSEOUT_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_5_10_runtime_bridge_implementation_gate_closeout_review.json`
- `tests/test_phase_5_10_runtime_bridge_implementation_gate_closeout_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- closeout review only
- implementation gate only
- designed artifacts listed
- unimplemented runtime pieces listed
- future runtime implementation requirements listed
- explicit Phil approval required for any next scope
- live/runtime implementation remains blocked
- Phase 5.4 helper remains test-only and cannot be reused as runtime classifier logic
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- explicit operator next-scope decision

Status:

- complete
- tagged as `phase-5.10-runtime-bridge-implementation-gate-closeout-review`

## Phase 5.11 - Phase 5 HumanInput Bridge Design Lane Audit Archive / Closeout

Goal:

Archive the completed Phase 5 HumanInput to IntentEnvelope design lane and produce a clean decision point before any future runtime work.

Deliverables:

- `docs/PHASE_5_11_PHASE_5_HUMANINPUT_BRIDGE_DESIGN_LANE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_5_11_phase_5_humaninput_bridge_design_lane_audit_archive_closeout.json`
- `tests/test_phase_5_11_phase_5_humaninput_bridge_design_lane_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 5.0 through Phase 5.10 listed as complete
- Phase 5.7 through Phase 5.10 archived as design/specification only
- Phase 5 live implementation remains gated
- Phase 5.4 helper remains test-only
- helper classifier is not approved for runtime reuse
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- explicit operator next-scope decision

Status:

- complete
- tagged as `phase-5.11-phase-5-humaninput-bridge-design-lane-audit-archive-closeout`

## Phase 6.0 - Post-Phase-5 Roadmap Reorientation

Goal:

Reorient the roadmap after the Phase 5 HumanInput bridge design lane archive and select the safest next architectural planning lane.

Deliverables:

- `docs/PHASE_6_0_POST_PHASE_5_ROADMAP_REORIENTATION.md`
- `tests/fixtures/runtime_extraction/phase_6_0_post_phase_5_roadmap_reorientation.json`
- `tests/test_phase_6_0_post_phase_5_roadmap_reorientation.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 5 closeout preserved
- kernel lifecycle planning selected as the safest next lane
- future lanes separated
- runtime bridge prerequisites listed
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 6.1 - LIMA Kernel Lifecycle Planning

Status:

- complete
- tagged as `phase-6.0-post-phase-5-roadmap-reorientation`

## Phase 6.1 - LIMA Kernel Lifecycle Planning

Goal:

Define a planning-only lifecycle map for the LIMA Kernel before any future runtime bridge implementation.

Deliverables:

- `docs/PHASE_6_1_LIMA_KERNEL_LIFECYCLE_PLANNING.md`
- `tests/fixtures/runtime_extraction/phase_6_1_lima_kernel_lifecycle_planning.json`
- `tests/test_phase_6_1_lima_kernel_lifecycle_planning.py`

Acceptance criteria:

- docs/tests/fixtures only
- shell intake, boundary normalization, candidate formation, Guardian review, GuardianDecision, spine/audit/memory, and driver handoff stages documented
- HumanInput remains intent context
- IntentEnvelope candidates remain non-executable
- GuardianDecision remains future authority boundary
- audit/spine/memory design precedes persistence
- Sparkbot remains reference shell, not kernel
- Robo-OS remains gated driver-plane surface
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no physical-world side effects
- tests pass

Next likely phase:

- Phase 6.2 - IntentEnvelope and GuardianDecision Lifecycle Boundary Map

Status:

- complete
- tagged as `phase-6.1-lima-kernel-lifecycle-planning`

## Phase 6.2 - IntentEnvelope and GuardianDecision Lifecycle Boundary Map

Goal:

Map the lifecycle boundary between non-executable IntentEnvelope candidate metadata and future GuardianDecision authority before any runtime implementation.

Deliverables:

- `docs/PHASE_6_2_INTENTENVELOPE_GUARDIANDECISION_LIFECYCLE_BOUNDARY_MAP.md`
- `tests/fixtures/runtime_extraction/phase_6_2_intentenvelope_guardiandecision_lifecycle_boundary_map.json`
- `tests/test_phase_6_2_intentenvelope_guardiandecision_lifecycle_boundary_map.py`

Acceptance criteria:

- docs/tests/fixtures only
- IntentEnvelope candidates remain non-executable
- IntentEnvelope candidates are not commands, approvals, authorization, execution, or audit persistence
- GuardianDecision remains future authority and is not implemented
- approval state metadata remains descriptive only
- audit/spine/memory references remain lineage planning only
- driver/tool handoff remains blocked
- operator/admin/Phil/trusted wording does not bypass approval
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no physical-world side effects
- tests pass

Next likely phase:

- Phase 6.3 - Approval / Audit / Memory Boundary Planning

Status:

- complete
- tagged as `phase-6.2-intentenvelope-guardiandecision-lifecycle-boundary-map`

## Phase 6.3 - Approval / Audit / Memory Boundary Planning

Goal:

Plan approval, audit/spine, and memory boundaries before any future runtime bridge implementation.

Deliverables:

- `docs/PHASE_6_3_APPROVAL_AUDIT_MEMORY_BOUNDARY_PLANNING.md`
- `tests/fixtures/runtime_extraction/phase_6_3_approval_audit_memory_boundary_planning.json`
- `tests/test_phase_6_3_approval_audit_memory_boundary_planning.py`

Acceptance criteria:

- docs/tests/fixtures only
- approval states remain descriptive metadata only
- approval references do not enforce, authorize, or open breakglass
- audit/spine references remain lineage planning only
- audit persistence and ledger writes remain blocked
- memory references remain reference-only
- memory reads, writes, embedding updates, and summary storage remain blocked
- HumanInput remains intent context
- IntentEnvelope candidates remain non-executable
- GuardianDecision remains future authority
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no memory IO or spine ledger write
- no physical-world side effects
- tests pass

Next likely phase:

- Phase 6.4 - Phase 6 Roadmap Gate / Next-Lane Closeout

Status:

- complete
- tagged as `phase-6.3-approval-audit-memory-boundary-planning`

## Phase 6.4 - Phase 6 Roadmap Gate / Next-Lane Closeout

Goal:

Close the current Phase 6 broader LIMA OS roadmap planning lane and produce a clean next-scope decision gate.

Deliverables:

- `docs/PHASE_6_4_PHASE_6_ROADMAP_GATE_NEXT_LANE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_6_4_phase_6_roadmap_gate_next_lane_closeout.json`
- `tests/test_phase_6_4_phase_6_roadmap_gate_next_lane_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 6.0 through Phase 6.3 listed as complete
- planned kernel, HumanInput, IntentEnvelope, GuardianDecision, approval, audit/spine, memory, Sparkbot, and Robo-OS boundaries summarized
- runtime bridge remains unimplemented
- live adapter remains unimplemented
- real IntentCompiler remains unimplemented
- real GuardianDecision remains unimplemented
- approval enforcement, execution, audit persistence, memory IO, and spine ledger writes remain blocked
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no physical-world side effects
- next-scope options documented
- no Phase 6.5 or Phase 7 work approved
- tests pass

Next likely phase:

- explicit operator next-scope decision

Status:

- complete
- tagged as `phase-6.4-phase-6-roadmap-gate-next-lane-closeout`

## Phase 6.5 - Phase 6 Roadmap Planning Lane Audit Archive / Closeout

Goal:

Archive Phase 6 as a completed roadmap/planning lane and create a clean decision point before any future runtime, Sparkbot, Robo-OS, or product-roadmap lane.

Deliverables:

- `docs/PHASE_6_5_PHASE_6_ROADMAP_PLANNING_LANE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_6_5_phase_6_roadmap_planning_lane_audit_archive_closeout.json`
- `tests/test_phase_6_5_phase_6_roadmap_planning_lane_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 6.0 through Phase 6.4 listed as complete
- Phase 6 archived as roadmap/planning only
- Phase 5 runtime bridge remains gated
- docs, fixtures, static tests, and roadmap/state updates listed as the only added artifact categories
- no runtime behavior
- no `lima/` runtime changes
- no `tests/support/` changes
- no helper behavior changes
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- next options documented and require explicit Phil approval
- tests pass

Next likely phase:

- explicit operator next-scope decision

Status:

- complete
- tagged as `phase-6.5-phase-6-roadmap-planning-lane-audit-archive-closeout`

## Phase 7.0 - Kernel Runtime Implementation Charter

Goal:

Open Phase 7 as a no-code kernel runtime implementation charter lane and define the smallest future runtime implementation slice that could be considered later.

Deliverables:

- `docs/PHASE_7_0_KERNEL_RUNTIME_IMPLEMENTATION_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_7_0_kernel_runtime_implementation_charter.json`
- `tests/test_phase_7_0_kernel_runtime_implementation_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no-code charter only
- smallest future runtime slice described but not approved for implementation
- future slice accepts only typed explicit inputs
- future slice produces non-executable candidate metadata only
- future slice does not parse raw natural language
- future slice does not execute, enforce approval, persist audit, call models, call network services, mutate files, wire Sparkbot, or touch physical-world drivers
- preconditions before runtime code are listed
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 7.1 - First Runtime Slice Eligibility Map

Status:

- complete
- tagged as `phase-7.0-kernel-runtime-implementation-charter`

## Phase 7.1 - First Runtime Slice Eligibility Map

Goal:

Map exactly which files could be eligible for a later explicitly approved first runtime slice and which files remain forbidden.

Deliverables:

- `docs/PHASE_7_1_FIRST_RUNTIME_SLICE_ELIGIBILITY_MAP.md`
- `tests/fixtures/runtime_extraction/phase_7_1_first_runtime_slice_eligibility_map.json`
- `tests/test_phase_7_1_first_runtime_slice_eligibility_map.py`

Acceptance criteria:

- docs/tests/fixtures only
- future eligible existing files listed exactly
- future eligible new files listed only as explicitly approved future candidates
- forbidden runtime surfaces listed
- `tests/support/**` remains forbidden
- eligibility is not approval to modify files now
- future code must remain non-executing and candidate-metadata-only
- future code must not parse raw natural language
- future code must not create real GuardianDecision
- future code must not approve, enforce, execute, persist audit, or hand off to drivers
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 7.2 - Kernel Runtime Safety Preconditions

Status:

- complete
- tagged as `phase-7.1-first-runtime-slice-eligibility-map`

## Phase 7.2 - Kernel Runtime Safety Preconditions

Goal:

Define the safety preconditions that must be satisfied before any future kernel runtime implementation can be approved.

Deliverables:

- `docs/PHASE_7_2_KERNEL_RUNTIME_SAFETY_PRECONDITIONS.md`
- `tests/fixtures/runtime_extraction/phase_7_2_kernel_runtime_safety_preconditions.json`
- `tests/test_phase_7_2_kernel_runtime_safety_preconditions.py`

Acceptance criteria:

- docs/tests/fixtures only
- required test preconditions listed
- rollback expectations listed
- audit proof requirements listed
- input/output shape constraints listed
- safety gate preconditions listed
- Phase 5 runtime bridge gate remains active
- future candidate outputs remain non-executable
- future output must not include approval, execution, driver handoff, or persistence authority
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 7.3 - Runtime Implementation Test Plan

Status:

- complete
- tagged as `phase-7.2-kernel-runtime-safety-preconditions`

## Phase 7.3 - Runtime Implementation Test Plan

Goal:

Define the test plan required before any future kernel runtime implementation can be approved.

Deliverables:

- `docs/PHASE_7_3_RUNTIME_IMPLEMENTATION_TEST_PLAN.md`
- `tests/fixtures/runtime_extraction/phase_7_3_runtime_implementation_test_plan.json`
- `tests/test_phase_7_3_runtime_implementation_test_plan.py`

Acceptance criteria:

- docs/tests/fixtures only
- future test families listed
- required negative tests listed
- positive tests limited to non-executable metadata behavior
- validation commands listed
- Sparkbot coupling rejection included
- GuardianDecision non-creation included
- approval bypass rejection included
- side-effect rejection included
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 7.4 - Phase 7 Implementation Decision Gate / Closeout

Status:

- complete
- tagged as `phase-7.3-runtime-implementation-test-plan`

## Phase 7.4 - Phase 7 Implementation Decision Gate / Closeout

Goal:

Close the no-code Phase 7 kernel runtime implementation charter lane at a clean implementation decision gate.

Deliverables:

- `docs/PHASE_7_4_PHASE_7_IMPLEMENTATION_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_7_4_phase_7_implementation_decision_gate_closeout.json`
- `tests/test_phase_7_4_phase_7_implementation_decision_gate_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 7.0 through Phase 7.3 listed as complete
- Phase 7 decisions summarized
- runtime behavior remains unimplemented
- `lima/` changes remain unimplemented
- `tests/support/` changes remain unimplemented
- Sparkbot wiring remains unimplemented
- live adapters remain unimplemented
- IntentCompiler and GuardianDecision runtime behavior remain unimplemented
- approval enforcement, execution, and audit persistence remain blocked
- shell, browser, network, file mutation, robot, and physical-world side effects remain blocked
- decision options documented
- explicit Phil approval required before runtime code
- tests pass

Next likely phase:

- Phase 7.5 - Phase 7 No-Code Kernel Runtime Charter Audit Archive / Closeout

Status:

- complete
- tagged as `phase-7.4-phase-7-implementation-decision-gate-closeout`

## Phase 7.5 - Phase 7 No-Code Kernel Runtime Charter Audit Archive / Closeout

Goal:

Archive Phase 7 as a completed no-code kernel runtime implementation charter lane and create a clean decision point before any Phase 8 implementation design review or future runtime slice.

Deliverables:

- `docs/PHASE_7_5_PHASE_7_NO_CODE_KERNEL_RUNTIME_CHARTER_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_7_5_phase_7_no_code_kernel_runtime_charter_audit_archive_closeout.json`
- `tests/test_phase_7_5_phase_7_no_code_kernel_runtime_charter_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 7.0 through Phase 7.4 listed as complete
- Phase 7 archived as no-code charter/planning only
- no runtime implementation approved
- Phase 5 runtime bridge remains gated
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- next options documented and require explicit Phil approval
- tests pass

Next likely phase:

- Phase 8.0 - Implementation Design Review Charter

Status:

- complete
- tagged as `phase-7.5-phase-7-no-code-kernel-runtime-charter-audit-archive-closeout`

## Phase 8.0 - Implementation Design Review Charter

Goal:

Open Phase 8 as a no-code implementation design review lane and convert the Phase 7 charter into a precise future implementation design package without modifying runtime code.

Deliverables:

- `docs/PHASE_8_0_IMPLEMENTATION_DESIGN_REVIEW_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_8_0_implementation_design_review_charter.json`
- `tests/test_phase_8_0_implementation_design_review_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 7.0 through Phase 7.5 reviewed as source context
- narrowest future runtime slice named
- future design package requirements listed
- Phase 5 runtime bridge remains gated
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 8.1 - Exact Runtime File-Touch Map

Status:

- complete
- tagged as `phase-8.0-implementation-design-review-charter`

## Phase 8.1 - Exact Runtime File-Touch Map

Goal:

Map the exact future file-touch surface for the narrowest possible runtime slice without modifying any runtime files.

Deliverables:

- `docs/PHASE_8_1_EXACT_RUNTIME_FILE_TOUCH_MAP.md`
- `tests/fixtures/runtime_extraction/phase_8_1_exact_runtime_file_touch_map.json`
- `tests/test_phase_8_1_exact_runtime_file_touch_map.py`

Acceptance criteria:

- docs/tests/fixtures only
- exact future eligible existing files listed
- exact future eligible new files listed
- forbidden runtime surfaces listed
- eligibility is not approval to modify files now
- future touch rules require targeted tests
- future candidate outputs remain non-executable and authority-free
- Phase 5 runtime bridge remains gated
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 8.2 - Runtime Acceptance Test Design

Status:

- complete
- tagged as `phase-8.1-exact-runtime-file-touch-map`

## Phase 8.2 - Runtime Acceptance Test Design

Goal:

Define the acceptance tests that must exist before any future first runtime slice implementation can be approved.

Deliverables:

- `docs/PHASE_8_2_RUNTIME_ACCEPTANCE_TEST_DESIGN.md`
- `tests/fixtures/runtime_extraction/phase_8_2_runtime_acceptance_test_design.json`
- `tests/test_phase_8_2_runtime_acceptance_test_design.py`

Acceptance criteria:

- docs/tests/fixtures only
- future required test families listed
- required negative cases listed
- limited positive cases constrained to non-executable candidate metadata
- validation commands listed
- Phase 5 runtime bridge remains gated
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 8.3 - Rollback / Audit Proof Plan

Status:

- complete
- tagged as `phase-8.2-runtime-acceptance-test-design`

## Phase 8.3 - Rollback / Audit Proof Plan

Goal:

Define rollback and audit proof requirements that must be satisfied before any future first runtime slice implementation can be approved.

Deliverables:

- `docs/PHASE_8_3_ROLLBACK_AUDIT_PROOF_PLAN.md`
- `tests/fixtures/runtime_extraction/phase_8_3_rollback_audit_proof_plan.json`
- `tests/test_phase_8_3_rollback_audit_proof_plan.py`

Acceptance criteria:

- docs/tests/fixtures only
- future rollback requirements listed
- future audit proof requirements listed
- future success criteria listed
- future failure criteria listed
- audit proof remains test evidence only
- Phase 5 runtime bridge remains gated
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 8.4 - Runtime Implementation Approval Gate / Closeout

Status:

- complete
- tagged as `phase-8.3-rollback-audit-proof-plan`

## Phase 8.4 - Runtime Implementation Approval Gate / Closeout

Goal:

Close the no-code Phase 8 implementation design review lane at a clean runtime implementation approval gate.

Deliverables:

- `docs/PHASE_8_4_RUNTIME_IMPLEMENTATION_APPROVAL_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_8_4_runtime_implementation_approval_gate_closeout.json`
- `tests/test_phase_8_4_runtime_implementation_approval_gate_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 8.0 through Phase 8.3 listed as complete
- designed future runtime slice summarized
- future eligible file scope listed
- runtime implementation preconditions listed
- still-out-of-scope surfaces listed
- exact future runtime implementation approval question documented
- Phase 5 runtime bridge remains gated
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- tests pass

Next likely phase:

- Phase 8.5 - Phase 8 No-Code Implementation Design Review Audit Archive / Closeout

Status:

- complete
- tagged as `phase-8.4-runtime-implementation-approval-gate-closeout`

## Phase 8.5 - Phase 8 No-Code Implementation Design Review Audit Archive / Closeout

Goal:

Archive Phase 8 as a completed no-code implementation design review lane and create a clean decision point before any Phase 9 runtime implementation slice.

Deliverables:

- `docs/PHASE_8_5_PHASE_8_NO_CODE_IMPLEMENTATION_DESIGN_REVIEW_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_8_5_phase_8_no_code_implementation_design_review_audit_archive_closeout.json`
- `tests/test_phase_8_5_phase_8_no_code_implementation_design_review_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 8.0 through Phase 8.4 listed as complete
- Phase 8 archived as no-code design review only
- no runtime implementation approved
- Phase 5 runtime bridge remains gated
- exact Phase 9 approval question preserved
- no helper behavior changes
- no `tests/support/` changes
- no files under `lima/`
- no live adapter code
- no Sparkbot import or wiring
- no real IntentCompiler
- no real GuardianDecision
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robot, or physical-world side effects
- next options documented and require explicit Phil approval
- tests pass

Next likely phase:

- explicit operator runtime implementation decision

Status:

- complete
- tagged as `phase-8.5-phase-8-no-code-implementation-design-review-audit-archive-closeout`

## Phase 9.0 - Runtime Slice Preflight Audit / Eligible File Confirmation

Goal:

Confirm the Phase 8.1 eligible runtime file-touch map before any Phase 9 runtime implementation work proceeds.

Deliverables:

- `docs/PHASE_9_0_RUNTIME_SLICE_PREFLIGHT_AUDIT_ELIGIBLE_FILE_CONFIRMATION.md`
- `tests/fixtures/runtime_extraction/phase_9_0_runtime_slice_preflight_audit_eligible_file_confirmation.json`
- `tests/test_phase_9_0_runtime_slice_preflight_audit_eligible_file_confirmation.py`

Acceptance criteria:

- docs/tests/fixtures only
- exact eligible existing runtime files listed
- exact eligible new runtime files listed
- no files under `lima/`
- no `tests/support/` changes
- no runtime behavior
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- Phase 9.1 acceptance test scaffolding identified as the next step
- tests pass

Next likely phase:

- Phase 9.1 - Runtime Slice Acceptance Test Scaffolding

Status:

- complete
- tagged as `phase-9.0-runtime-slice-preflight-audit-eligible-file-confirmation`

## Phase 9.1 - Runtime Slice Acceptance Test Scaffolding

Goal:

Convert the Phase 8.2 acceptance-test design into concrete Phase 9 scaffolding before the first runtime slice implementation.

Deliverables:

- `docs/PHASE_9_1_RUNTIME_SLICE_ACCEPTANCE_TEST_SCAFFOLDING.md`
- `tests/fixtures/runtime_extraction/phase_9_1_runtime_slice_acceptance_test_scaffolding.json`
- `tests/test_phase_9_1_runtime_slice_acceptance_test_scaffolding.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 9.2 acceptance cases listed
- forbidden runtime interpretations listed
- Phase 9.2 touch scope limited to Phase 8.1 eligible files
- no files under `lima/`
- no `tests/support/` changes
- no runtime behavior
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 9.2 - Non-executing Kernel Intake-to-Candidate Coordinator Implementation

Status:

- complete
- tagged as `phase-9.1-runtime-slice-acceptance-test-scaffolding`

## Phase 9.2 - Non-executing Kernel Intake-to-Candidate Coordinator Implementation

Goal:

Implement the first narrow runtime slice as a pure in-process coordinator that produces non-executable candidate metadata from already-normalized synthetic intake metadata.

Deliverables:

- `lima/kernel/__init__.py`
- `lima/kernel/intake_candidate.py`
- `docs/PHASE_9_2_NON_EXECUTING_KERNEL_INTAKE_TO_CANDIDATE_COORDINATOR_IMPLEMENTATION.md`
- `tests/fixtures/runtime_extraction/phase_9_2_non_executing_kernel_intake_to_candidate_coordinator_implementation.json`
- `tests/test_phase_9_2_non_executing_kernel_intake_to_candidate_coordinator_implementation.py`

Acceptance criteria:

- only Phase 8.1 eligible runtime files touched
- coordinator is pure and in-process
- accepts only synthetic already-normalized intake metadata
- candidate output is non-executable
- `execution_allowed` is false
- `side_effects_allowed` is false
- `approval_state` is never approved
- provenance is preserved
- stale, replayed, malformed, raw, or unknown intake fails closed
- no `tests/support/` changes
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 9.3 - Runtime Slice Readiness Review

Status:

- complete
- tagged as `phase-9.2-non-executing-kernel-intake-to-candidate-coordinator-implementation`

## Phase 9.3 - Runtime Slice Readiness Review

Goal:

Review the Phase 9.2 coordinator and decide whether it is constrained enough for Phase 9.4 audit/archive closeout.

Deliverables:

- `docs/PHASE_9_3_RUNTIME_SLICE_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_9_3_runtime_slice_readiness_review.json`
- `tests/test_phase_9_3_runtime_slice_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no runtime code changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 9.2 coordinator reviewed
- coordinator remains non-executing
- ready only for Phase 9.4 closeout or further non-runtime review
- not ready for runtime expansion
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 9.4 - Phase 9 Runtime Slice Audit Archive / Closeout

Status:

- complete
- tagged as `phase-9.3-runtime-slice-readiness-review`

## Phase 9.4 - Phase 9 Runtime Slice Audit Archive / Closeout

Goal:

Archive the Phase 9 first runtime slice lane and stop at a clean next-scope decision gate.

Deliverables:

- `docs/PHASE_9_4_PHASE_9_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_9_4_phase_9_runtime_slice_audit_archive_closeout.json`
- `tests/test_phase_9_4_phase_9_runtime_slice_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no runtime code changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 9.0 through Phase 9.3 listed as complete
- Phase 9 runtime slice archived as pure in-process non-executing candidate metadata coordinator
- only Phase 8.1 eligible runtime files touched in Phase 9
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- next options require explicit Phil approval
- tests pass

Next likely phase:

- explicit operator next-scope decision

Status:

- complete
- tagged as `phase-9.4-phase-9-runtime-slice-audit-archive-closeout`

## Phase 9.5 - First Runtime Slice Audit Archive / Closeout

Goal:

Archive Phase 9 as a completed first narrow runtime slice after a dedicated Phase 9.0 through Phase 9.4 audit.

Deliverables:

- `docs/PHASE_9_5_FIRST_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_9_5_first_runtime_slice_audit_archive_closeout.json`
- `tests/test_phase_9_5_first_runtime_slice_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- Phase 9.0 through Phase 9.4 listed as complete
- only `lima/kernel/__init__.py` and `lima/kernel/intake_candidate.py` listed as approved runtime files touched
- no new `lima/` changes
- no `tests/support/` changes
- runtime remains non-executing
- `execution_allowed` remains always false
- `side_effects_allowed` remains always false
- `approval_state` is never approved
- Phase 8.1 test-update warning preserved and explained
- no HumanInput runtime bridge
- no Sparkbot import or wiring
- no live adapter
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- Phase 10 requires explicit Phil approval
- tests pass

Next likely phase:

- explicit operator next-scope decision

Status:

- complete
- tagged as `phase-9.5-first-runtime-slice-audit-archive-closeout`

## Phase 10.0 - Post-Phase-9 Runtime Slice Review

Goal:

Open Phase 10 as a no-code design lane by reviewing what the first Phase 9 runtime slice proved and did not prove.

Deliverables:

- `docs/PHASE_10_0_POST_PHASE_9_RUNTIME_SLICE_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_10_0_post_phase_9_runtime_slice_review.json`
- `tests/test_phase_10_0_post_phase_9_runtime_slice_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 9.0 through Phase 9.5 reviewed
- Phase 9 runtime files listed exactly as `lima/kernel/__init__.py` and `lima/kernel/intake_candidate.py`
- Phase 9 proof and gap lists documented
- runtime remains non-executing
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- Phase 11 runtime implementation remains unapproved
- tests pass

Next likely phase:

- Phase 10.1 - Next Runtime Slice Design Options

Status:

- complete
- tagged as `phase-10.0-post-phase-9-runtime-slice-review`

## Phase 10.1 - Next Runtime Slice Design Options

Goal:

Evaluate the safest possible next runtime slice after Phase 9 without implementing it.

Deliverables:

- `docs/PHASE_10_1_NEXT_RUNTIME_SLICE_DESIGN_OPTIONS.md`
- `tests/fixtures/runtime_extraction/phase_10_1_next_runtime_slice_design_options.json`
- `tests/test_phase_10_1_next_runtime_slice_design_options.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- candidate validation evaluated
- candidate status normalization evaluated
- candidate lifecycle metadata evaluated
- intake error taxonomy evaluated
- provenance hardening evaluated
- no further runtime work evaluated
- recommended future slice remains non-executing and requires Phase 11 approval
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 10.2 - Exact File-Touch Map for Next Runtime Slice

Status:

- complete
- tagged as `phase-10.1-next-runtime-slice-design-options`

## Phase 10.2 - Exact File-Touch Map for Next Runtime Slice

Goal:

Map the exact future runtime file-touch surface for a possible Phase 11 candidate validation and status normalization slice without implementing it.

Deliverables:

- `docs/PHASE_10_2_EXACT_FILE_TOUCH_MAP_FOR_NEXT_RUNTIME_SLICE.md`
- `tests/fixtures/runtime_extraction/phase_10_2_exact_file_touch_map_for_next_runtime_slice.json`
- `tests/test_phase_10_2_exact_file_touch_map_for_next_runtime_slice.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- future-eligible files listed exactly
- forbidden runtime surfaces listed
- `lima/kernel/intake_candidate.py` limited to pure validation/status metadata touch only
- `lima/kernel/__init__.py` limited to safe side-effect-free exports only
- possible `lima/kernel/candidate_status.py` listed as future file only
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 10.3 - Acceptance Test and Rollback Plan

Status:

- complete
- tagged as `phase-10.2-exact-file-touch-map-for-next-runtime-slice`

## Phase 10.3 - Acceptance Test and Rollback Plan

Goal:

Define future acceptance-test, rollback, and audit-proof requirements for the possible Phase 11 candidate validation and status normalization slice.

Deliverables:

- `docs/PHASE_10_3_ACCEPTANCE_TEST_AND_ROLLBACK_PLAN.md`
- `tests/fixtures/runtime_extraction/phase_10_3_acceptance_test_and_rollback_plan.json`
- `tests/test_phase_10_3_acceptance_test_and_rollback_plan.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- future acceptance tests require non-authoritative candidate safety
- future acceptance tests reject missing or true execution/side-effect flags
- future acceptance tests reject approved approval state
- future statuses limited to proposed, needs_review, or blocked
- rollback plan is source-only and validation-heavy
- audit proof requires exact file scope and side-effect review
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 10.4 - Phase 10 Runtime Expansion Approval Gate / Closeout

Status:

- complete
- tagged as `phase-10.3-acceptance-test-and-rollback-plan`

## Phase 10.4 - Phase 10 Runtime Expansion Approval Gate / Closeout

Goal:

Close the Phase 10 no-code design lane and preserve the exact Phase 11 approval question before any runtime expansion.

Deliverables:

- `docs/PHASE_10_4_PHASE_10_RUNTIME_EXPANSION_APPROVAL_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_10_4_phase_10_runtime_expansion_approval_gate_closeout.json`
- `tests/test_phase_10_4_phase_10_runtime_expansion_approval_gate_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 10.0 through Phase 10.3 listed as complete
- future Phase 11 eligible files listed exactly
- exact Phase 11 approval question preserved
- runtime candidate validation and status normalization remain unimplemented
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- explicit Phil decision on Phase 11 runtime implementation scope

Status:

- complete
- tagged as `phase-10.4-phase-10-runtime-expansion-approval-gate-closeout`

## Phase 10.5 - Phase 10 Next Runtime Slice Design Lane Audit Archive / Closeout

Goal:

Archive Phase 10 as a completed no-code next-runtime-slice design lane before any Phase 11 runtime expansion decision.

Deliverables:

- `docs/PHASE_10_5_PHASE_10_NEXT_RUNTIME_SLICE_DESIGN_LANE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_10_5_phase_10_next_runtime_slice_design_lane_audit_archive_closeout.json`
- `tests/test_phase_10_5_phase_10_next_runtime_slice_design_lane_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- no helper behavior changes
- no `lima/kernel/candidate_status.py`
- Phase 10.0 through Phase 10.4 listed as complete
- Phase 10 archived as no-code design only
- exact Phase 11 approval question preserved
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- explicit Phil decision on Phase 11 runtime implementation scope

Status:

- complete
- tagged as `phase-10.5-phase-10-next-runtime-slice-design-lane-audit-archive-closeout`

## Phase 11.0 - Runtime Slice Preflight Audit / Eligible File Confirmation

Goal:

Confirm the Phase 10.2 eligible runtime file list before Phase 11 runtime implementation work.

Deliverables:

- `docs/PHASE_11_0_RUNTIME_SLICE_PREFLIGHT_AUDIT_ELIGIBLE_FILE_CONFIRMATION.md`
- `tests/fixtures/runtime_extraction/phase_11_0_runtime_slice_preflight_audit_eligible_file_confirmation.json`
- `tests/test_phase_11_0_runtime_slice_preflight_audit_eligible_file_confirmation.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 10.2 eligible files listed exactly
- `lima/kernel/candidate_status.py` remains absent before implementation
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 11.1 - Candidate Status Acceptance Test Scaffolding

Status:

- complete
- tagged as `phase-11.0-runtime-slice-preflight-audit-eligible-file-confirmation`

## Phase 11.1 - Candidate Status Acceptance Test Scaffolding

Goal:

Translate Phase 10.3 acceptance obligations into concrete test families for Phase 11.2 and Phase 11.3.

Deliverables:

- `docs/PHASE_11_1_CANDIDATE_STATUS_ACCEPTANCE_TEST_SCAFFOLDING.md`
- `tests/fixtures/runtime_extraction/phase_11_1_candidate_status_acceptance_test_scaffolding.json`
- `tests/test_phase_11_1_candidate_status_acceptance_test_scaffolding.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 11.2 status normalization tests scaffolded
- Phase 11.3 validation tests scaffolded
- shared forbidden-behavior tests scaffolded
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 11.2 - Candidate Status Normalization Runtime Implementation

Status:

- complete
- tagged as `phase-11.1-candidate-status-acceptance-test-scaffolding`

## Phase 11.2 - Candidate Status Normalization Runtime Implementation

Goal:

Implement candidate status normalization for existing non-executing intake candidates.

Deliverables:

- `docs/PHASE_11_2_CANDIDATE_STATUS_NORMALIZATION_RUNTIME_IMPLEMENTATION.md`
- `lima/kernel/candidate_status.py`
- safe exports in `lima/kernel/__init__.py`
- `tests/fixtures/runtime_extraction/phase_11_2_candidate_status_normalization_runtime_implementation.json`
- `tests/test_phase_11_2_candidate_status_normalization_runtime_implementation.py`

Acceptance criteria:

- only Phase 10.2 eligible runtime files touched
- no `tests/support/` changes
- status normalization is pure and in-process
- allowed statuses limited to proposed, needs_review, and blocked
- `execution_allowed` remains false
- `side_effects_allowed` remains false
- approved state never survives normalization
- provenance is preserved
- unknown, stale, replayed, execution-enabled, side-effect-enabled, or approved states block safely
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 11.3 - Candidate Validation Runtime Implementation

Status:

- complete
- tagged as `phase-11.2-candidate-status-normalization-runtime-implementation`

## Phase 11.3 - Candidate Validation Runtime Implementation

Goal:

Implement fail-closed candidate validation for existing non-executing intake candidates.

Deliverables:

- `docs/PHASE_11_3_CANDIDATE_VALIDATION_RUNTIME_IMPLEMENTATION.md`
- validation behavior in `lima/kernel/candidate_status.py`
- safe export in `lima/kernel/__init__.py`
- `tests/fixtures/runtime_extraction/phase_11_3_candidate_validation_runtime_implementation.json`
- `tests/test_phase_11_3_candidate_validation_runtime_implementation.py`

Acceptance criteria:

- only Phase 10.2 eligible runtime files touched
- no `tests/support/` changes
- malformed candidates fail closed
- missing safety fields fail closed
- executable, execution_allowed, side_effects_allowed, approved, stale, and replayed states fail closed
- validation cannot approve, execute, persist, or dispatch
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 11.4 - Runtime Slice Readiness Review

Status:

- complete
- tagged as `phase-11.3-candidate-validation-runtime-implementation`

## Phase 11.4 - Runtime Slice Readiness Review

Goal:

Review the Phase 11.2 and Phase 11.3 runtime slice before archival closeout.

Deliverables:

- `docs/PHASE_11_4_RUNTIME_SLICE_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_11_4_runtime_slice_readiness_review.json`
- `tests/test_phase_11_4_runtime_slice_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no new `lima/` changes
- no `tests/support/` changes
- reviewed runtime files remain limited to `lima/kernel/candidate_status.py` and `lima/kernel/__init__.py`
- candidate status normalization and validation remain non-executing
- execution_allowed remains false
- side_effects_allowed remains false
- approval_state never becomes approved
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- tests pass

Next likely phase:

- Phase 11.5 - Phase 11 Runtime Slice Audit Archive / Closeout

Status:

- complete
- tagged as `phase-11.4-runtime-slice-readiness-review`

## Phase 11.5 - Phase 11 Runtime Slice Audit Archive / Closeout

Goal:

Archive Phase 11 as a completed narrow runtime slice and stop before any Phase 12 runtime expansion.

Deliverables:

- `docs/PHASE_11_5_PHASE_11_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_11_5_phase_11_runtime_slice_audit_archive_closeout.json`
- `tests/test_phase_11_5_phase_11_runtime_slice_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no new `lima/` changes
- no `tests/support/` changes
- Phase 11.0 through Phase 11.4 listed as complete
- approved runtime files touched listed as `lima/kernel/candidate_status.py` and `lima/kernel/__init__.py`
- `lima/kernel/intake_candidate.py` remains eligible but untouched by Phase 11
- runtime remains non-executing
- execution_allowed remains false
- side_effects_allowed remains false
- approval_state never becomes approved
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no live adapter
- no HumanInput runtime bridge
- no IntentCompiler or GuardianDecision runtime behavior
- no approval, enforcement, execution, dispatch, or audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world side effects
- Phase 12 requires explicit Phil approval
- tests pass

Next likely phase:

- Phase 12 - gated pending explicit Phil approval

Status:

- complete
- tagged as `phase-11.5-phase-11-runtime-slice-audit-archive-closeout`

## Phase 12.0 - Post-Phase-11 Runtime Slice Review

Goal:

Open Phase 12 as a docs/tests/fixtures-only planning lane and review the completed Phase 11 runtime slice.

Deliverables:

- `docs/PHASE_12_0_POST_PHASE_11_RUNTIME_SLICE_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_12_0_post_phase_11_runtime_slice_review.json`
- `tests/test_phase_12_0_post_phase_11_runtime_slice_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 11 runtime file scope preserved
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no HumanInput runtime bridge
- no live adapter
- no approval, enforcement, execution, dispatch, audit persistence, or physical-world behavior
- Phase 12 next-direction options listed
- tests pass

Next likely phase:

- Phase 12.1 - Next Direction Options: Runtime / Sparkbot / Robo-OS / Pause

Status:

- complete
- tagged as `phase-12.0-post-phase-11-runtime-slice-review`

## Phase 12.1 - Next Direction Options: Runtime / Sparkbot / Robo-OS / Pause

Goal:

Compare safe next-direction options after Phase 11 without approving implementation.

Deliverables:

- `docs/PHASE_12_1_NEXT_DIRECTION_OPTIONS_RUNTIME_SPARKBOT_ROBO_OS_PAUSE.md`
- `tests/fixtures/runtime_extraction/phase_12_1_next_direction_options_runtime_sparkbot_robo_os_pause.json`
- `tests/test_phase_12_1_next_direction_options_runtime_sparkbot_robo_os_pause.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- pause, runtime design, Sparkbot boundary, Robo-OS boundary, and threat-model options reviewed
- no implementation approval granted
- Phase 5 runtime bridge remains gated
- no Sparkbot import or wiring
- no HumanInput runtime bridge
- no live adapter
- no approval, enforcement, execution, dispatch, audit persistence, or physical-world behavior
- tests pass

Next likely phase:

- Phase 12.2 - Threat Model and Safety Gap Review

Status:

- complete
- tagged as `phase-12.1-next-direction-options-runtime-sparkbot-robo-os-pause`

## Phase 12.2 - Threat Model and Safety Gap Review

Goal:

Review threats and safety gaps before selecting any next lane after Phase 11.

Deliverables:

- `docs/PHASE_12_2_THREAT_MODEL_AND_SAFETY_GAP_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_12_2_threat_model_and_safety_gap_review.json`
- `tests/test_phase_12_2_threat_model_and_safety_gap_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- candidate-status approval confusion reviewed
- HumanInput bridge pressure reviewed
- Sparkbot wiring drift reviewed
- Robo-OS driver/physical-world drift reviewed
- operator/admin/Phil/trusted bypass risk reviewed
- side-effect escalation reviewed
- Phase 5 runtime bridge remains gated
- no approval, enforcement, execution, dispatch, audit persistence, or physical-world behavior
- tests pass

Next likely phase:

- Phase 12.3 - Next Lane Recommendation Matrix

Status:

- complete
- tagged as `phase-12.2-threat-model-and-safety-gap-review`

## Phase 12.3 - Next Lane Recommendation Matrix

Goal:

Record a machine-checkable recommendation matrix for the safest next lane after Phase 12.

Deliverables:

- `docs/PHASE_12_3_NEXT_LANE_RECOMMENDATION_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_12_3_next_lane_recommendation_matrix.json`
- `tests/test_phase_12_3_next_lane_recommendation_matrix.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- all Phase 12 options listed
- threat-model-derived test planning recommended as next
- runtime expansion deferred
- Sparkbot wiring deferred
- Robo-OS driver behavior deferred
- Phase 5 runtime bridge remains gated
- no approval, enforcement, execution, dispatch, audit persistence, or physical-world behavior
- tests pass

Next likely phase:

- Phase 12.4 - Phase 12 Decision Gate / Closeout

Status:

- complete
- tagged as `phase-12.3-next-lane-recommendation-matrix`

## Phase 12.4 - Phase 12 Decision Gate / Closeout

Goal:

Close Phase 12 as a docs/tests/fixtures-only planning lane and stop before Phase 13.

Deliverables:

- `docs/PHASE_12_4_PHASE_12_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_12_4_phase_12_decision_gate_closeout.json`
- `tests/test_phase_12_4_phase_12_decision_gate_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 12.0 through Phase 12.3 listed as complete
- threat-model-derived test planning preserved as recommended next lane
- Phase 13 requires explicit Phil approval
- runtime implementation remains blocked
- Sparkbot wiring remains blocked
- HumanInput runtime bridge remains blocked
- live adapter remains blocked
- approval, enforcement, execution, dispatch, audit persistence, and physical-world behavior remain blocked
- tests pass

Next likely phase:

- Phase 13 - gated pending explicit Phil approval

Status:

- complete
- tagged as `phase-12.4-phase-12-decision-gate-closeout`

## Phase 13.0 - Threat-Derived Test Planning Charter

Goal:

Open Phase 13 as a docs/tests/fixtures-only threat-model-derived test planning lane.

Deliverables:

- `docs/PHASE_13_0_THREAT_DERIVED_TEST_PLANNING_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_13_0_threat_derived_test_planning_charter.json`
- `tests/test_phase_13_0_threat_derived_test_planning_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 12.2 threats listed as source threats
- static, contract, fixture, and future acceptance planning outputs listed
- Phase 5 runtime bridge remains gated
- runtime implementation remains blocked
- Sparkbot wiring remains blocked
- HumanInput runtime bridge remains blocked
- approval, enforcement, execution, dispatch, audit persistence, and physical-world behavior remain blocked
- tests pass

Next likely phase:

- Phase 13.1 - Static Forbidden-Pattern Test Requirements

Status:

- complete
- tagged as `phase-13.0-threat-derived-test-planning-charter`

## Phase 13.1 - Static Forbidden-Pattern Test Requirements

Goal:

Define future static forbidden-pattern test requirements before any future runtime expansion.

Deliverables:

- `docs/PHASE_13_1_STATIC_FORBIDDEN_PATTERN_TEST_REQUIREMENTS.md`
- `tests/fixtures/runtime_extraction/phase_13_1_static_forbidden_pattern_test_requirements.json`
- `tests/test_phase_13_1_static_forbidden_pattern_test_requirements.py`

Acceptance criteria:

- docs/tests/fixtures only
- no static scanner implementation
- no `lima/` changes
- no `tests/support/` changes
- forbidden imports, calls, boundary names, and behavior claims listed
- static checks are not claimed sufficient alone
- Phase 5 runtime bridge remains gated
- no approval, enforcement, execution, dispatch, audit persistence, or physical-world behavior
- tests pass

Next likely phase:

- Phase 13.2 - Runtime Contract Test Requirements

Status:

- complete
- tagged as `phase-13.1-static-forbidden-pattern-test-requirements`

## Phase 13.2 - Runtime Contract Test Requirements

Goal:

Define future runtime contract test requirements for non-executing candidate invariants.

Deliverables:

- `docs/PHASE_13_2_RUNTIME_CONTRACT_TEST_REQUIREMENTS.md`
- `tests/fixtures/runtime_extraction/phase_13_2_runtime_contract_test_requirements.json`
- `tests/test_phase_13_2_runtime_contract_test_requirements.py`

Acceptance criteria:

- docs/tests/fixtures only
- no contract-test implementation
- no `lima/` changes
- no `tests/support/` changes
- non-executing candidate invariants listed
- Phase 5 runtime bridge remains gated
- no approval, enforcement, execution, dispatch, audit persistence, or physical-world behavior
- tests pass

Status:

- complete
- tagged as `phase-13.2-runtime-contract-test-requirements`

## Phase 13.3 - Threat Fixture Matrix

Goal:

Define future synthetic fixture families for threat-derived test cases.

Deliverables:

- `docs/PHASE_13_3_THREAT_FIXTURE_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_13_3_threat_fixture_matrix.json`
- `tests/test_phase_13_3_threat_fixture_matrix.py`

Acceptance criteria:

- docs/tests/fixtures only
- no production runtime fixtures
- no `lima/` changes
- no `tests/support/` changes
- malformed, unknown, stale/replayed, approval-bypass, side-effect, Sparkbot, and HumanInput bridge fixture families listed
- fixtures required to remain synthetic, inert, non-executing, and test-only
- tests pass

Status:

- complete
- tagged as `phase-13.3-threat-fixture-matrix`

## Phase 13.4 - Future Acceptance Gate / Closeout

Goal:

Close Phase 13 and preserve the Phase 14 approval gate.

Deliverables:

- `docs/PHASE_13_4_FUTURE_ACCEPTANCE_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_13_4_future_acceptance_gate_closeout.json`
- `tests/test_phase_13_4_future_acceptance_gate_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 13.0 through Phase 13.3 listed as complete
- future acceptance gate requirements listed
- Phase 14 requires explicit Phil approval
- runtime implementation remains blocked
- Sparkbot wiring remains blocked
- HumanInput runtime bridge remains blocked
- approval, enforcement, execution, dispatch, audit persistence, and physical-world behavior remain blocked
- tests pass

Next likely phase:

- Phase 14 - gated pending explicit Phil approval

Status:

- complete
- tagged as `phase-13.4-future-acceptance-gate-closeout`

## Phase 14.0 - Acceptance-Gate Test Design Charter

Goal:

Open Phase 14 as a docs/tests/fixtures-only acceptance-gate test design lane.

Deliverables:

- `docs/PHASE_14_0_ACCEPTANCE_GATE_TEST_DESIGN_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_14_0_acceptance_gate_test_design_charter.json`
- `tests/test_phase_14_0_acceptance_gate_test_design_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- Phase 13 static, contract, and fixture requirements listed as inputs
- future test names and expected assertions identified as outputs
- Phase 5 runtime bridge remains gated
- runtime implementation remains blocked
- tests pass

Status:

- complete
- tagged as `phase-14.0-acceptance-gate-test-design-charter`

## Phase 14.1 - Static Forbidden-Pattern Test Design

Goal:

Design concrete future static tests for forbidden imports, calls, side-effect patterns, boundary names, and authority claims.

Deliverables:

- `docs/PHASE_14_1_STATIC_FORBIDDEN_PATTERN_TEST_DESIGN.md`
- `tests/fixtures/runtime_extraction/phase_14_1_static_forbidden_pattern_test_design.json`
- `tests/test_phase_14_1_static_forbidden_pattern_test_design.py`

Acceptance criteria:

- docs/tests/fixtures only
- no scanner implementation
- no `lima/` changes
- no `tests/support/` changes
- future static test names and assertions listed
- Sparkbot, HumanInput bridge, live adapter, execution, persistence, dispatch, and physical-world patterns remain blocked
- tests pass

Status:

- complete
- tagged as `phase-14.1-static-forbidden-pattern-test-design`

## Phase 14.2 - Runtime Contract Test Design

Goal:

Design concrete future runtime contract tests for non-executing candidate invariants.

Deliverables:

- `docs/PHASE_14_2_RUNTIME_CONTRACT_TEST_DESIGN.md`
- `tests/fixtures/runtime_extraction/phase_14_2_runtime_contract_test_design.json`
- `tests/test_phase_14_2_runtime_contract_test_design.py`

Acceptance criteria:

- docs/tests/fixtures only
- no contract-test implementation
- no `lima/` changes
- no `tests/support/` changes
- execution and side-effect flags remain false
- approval state never becomes approved
- provenance, malformed/unknown/stale/replayed safety, and operator-bypass resistance are covered
- tests pass

Status:

- complete
- tagged as `phase-14.2-runtime-contract-test-design`

## Phase 14.3 - Threat Fixture Acceptance Test Design

Goal:

Design concrete future fixture-based acceptance tests for the Phase 13.3 threat fixture families.

Deliverables:

- `docs/PHASE_14_3_THREAT_FIXTURE_ACCEPTANCE_TEST_DESIGN.md`
- `tests/fixtures/runtime_extraction/phase_14_3_threat_fixture_acceptance_test_design.json`
- `tests/test_phase_14_3_threat_fixture_acceptance_test_design.py`

Acceptance criteria:

- docs/tests/fixtures only
- no fixture-execution implementation
- no `lima/` changes
- no `tests/support/` changes
- malformed, unknown, stale/replayed, approval-bypass, shell/network/browser/file/robotics, Sparkbot, and HumanInput bridge fixture test names listed
- future fixtures remain synthetic, inert, non-runtime, and side-effect-free
- tests pass

Status:

- complete
- tagged as `phase-14.3-threat-fixture-acceptance-test-design`

## Phase 14.4 - Future Runtime Acceptance Gate / Closeout

Goal:

Close Phase 14 and preserve the Phase 15 decision gate.

Deliverables:

- `docs/PHASE_14_4_FUTURE_RUNTIME_ACCEPTANCE_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_14_4_future_runtime_acceptance_gate_closeout.json`
- `tests/test_phase_14_4_future_runtime_acceptance_gate_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no acceptance-gate test implementation
- no `lima/` changes
- no `tests/support/` changes
- Phase 14.0 through Phase 14.3 listed as complete
- future acceptance-gate requirements listed
- Phase 15 requires explicit Phil approval
- runtime implementation remains blocked
- Sparkbot wiring remains blocked
- HumanInput runtime bridge remains blocked
- approval, enforcement, execution, dispatch, audit persistence, and physical-world behavior remain blocked
- tests pass

Next likely phase:

- Phase 15 - gated pending explicit Phil approval

Status:

- complete
- tagged as `phase-14.4-future-runtime-acceptance-gate-closeout`

## Phase 15.0 - Acceptance-Gate Implementation Proposal Charter

Goal:

Open Phase 15 as a docs/tests/fixtures-only acceptance-gate implementation proposal/readiness lane.

Deliverables:

- `docs/PHASE_15_0_ACCEPTANCE_GATE_IMPLEMENTATION_PROPOSAL_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_15_0_acceptance_gate_implementation_proposal_charter.json`
- `tests/test_phase_15_0_acceptance_gate_implementation_proposal_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no actual future acceptance-test implementation
- no `lima/` changes
- no `tests/support/` changes
- Phase 14 inputs listed
- future proposal outputs listed
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-15.0-acceptance-gate-implementation-proposal-charter`

## Phase 15.1 - Future Static Test Implementation Plan

Goal:

Propose the future static forbidden-pattern test implementation package without implementing it.

Deliverables:

- `docs/PHASE_15_1_FUTURE_STATIC_TEST_IMPLEMENTATION_PLAN.md`
- `tests/fixtures/runtime_extraction/phase_15_1_future_static_test_implementation_plan.json`
- `tests/test_phase_15_1_future_static_test_implementation_plan.py`

Acceptance criteria:

- docs/tests/fixtures only
- no static test implementation
- no scanner utilities
- future static test file and test names listed
- no `lima/` changes
- no `tests/support/` changes
- tests pass

Status:

- complete
- tagged as `phase-15.1-future-static-test-implementation-plan`

## Phase 15.2 - Future Runtime Contract Test Implementation Plan

Goal:

Propose the future runtime contract acceptance-test implementation package without implementing it.

Deliverables:

- `docs/PHASE_15_2_FUTURE_RUNTIME_CONTRACT_TEST_IMPLEMENTATION_PLAN.md`
- `tests/fixtures/runtime_extraction/phase_15_2_future_runtime_contract_test_implementation_plan.json`
- `tests/test_phase_15_2_future_runtime_contract_test_implementation_plan.py`

Acceptance criteria:

- docs/tests/fixtures only
- no runtime contract acceptance-test implementation
- future runtime contract test file and test names listed
- no `lima/` changes
- no `tests/support/` changes
- runtime behavior remains unchanged
- tests pass

Status:

- complete
- tagged as `phase-15.2-future-runtime-contract-test-implementation-plan`

## Phase 15.3 - Future Threat Fixture Test Implementation Plan

Goal:

Propose the future threat fixture acceptance-test implementation package without implementing it.

Deliverables:

- `docs/PHASE_15_3_FUTURE_THREAT_FIXTURE_TEST_IMPLEMENTATION_PLAN.md`
- `tests/fixtures/runtime_extraction/phase_15_3_future_threat_fixture_test_implementation_plan.json`
- `tests/test_phase_15_3_future_threat_fixture_test_implementation_plan.py`

Acceptance criteria:

- docs/tests/fixtures only
- no future threat fixture test implementation
- no future threat fixtures added
- future threat fixture test file, fixture names, and content requirements listed
- no `lima/` changes
- no `tests/support/` changes
- tests pass

Status:

- complete
- tagged as `phase-15.3-future-threat-fixture-test-implementation-plan`

## Phase 15.4 - Test-Only Implementation Readiness Gate / Closeout

Goal:

Close Phase 15 and preserve the Phase 16 decision gate.

Deliverables:

- `docs/PHASE_15_4_TEST_ONLY_IMPLEMENTATION_READINESS_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_15_4_test_only_implementation_readiness_gate_closeout.json`
- `tests/test_phase_15_4_test_only_implementation_readiness_gate_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no actual future acceptance-test implementation
- no future acceptance fixtures added
- no `lima/` changes
- no `tests/support/` changes
- Phase 15.0 through Phase 15.3 listed as complete
- Phase 14 designed tests marked ready only for later explicitly approved test-only implementation
- Phase 16 requires explicit Phil approval
- runtime implementation remains blocked
- Sparkbot wiring remains blocked
- HumanInput runtime bridge remains blocked
- approval, enforcement, execution, dispatch, audit persistence, and physical-world behavior remain blocked
- tests pass

Next likely phase:

- Phase 16 - gated pending explicit Phil approval

Status:

- complete
- tagged as `phase-15.4-test-only-implementation-readiness-gate-closeout`

## Phase 16.0 - Test-Only Acceptance Implementation Charter

Goal:

Open Phase 16 as an explicitly approved test-only acceptance-gate implementation lane.

Deliverables:

- `docs/PHASE_16_0_TEST_ONLY_ACCEPTANCE_IMPLEMENTATION_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_16_0_test_only_acceptance_implementation_charter.json`
- `tests/test_phase_16_0_test_only_acceptance_implementation_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- acceptance implementation scope is limited to future Phase 16 tests and synthetic fixtures
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-16.0-test-only-acceptance-implementation-charter`

## Phase 16.1 - Static Forbidden-Pattern Acceptance Tests

Goal:

Implement static forbidden-pattern acceptance tests against explicit existing non-executing kernel candidate files.

Deliverables:

- `docs/PHASE_16_1_STATIC_FORBIDDEN_PATTERN_ACCEPTANCE_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_16_1_static_forbidden_pattern_acceptance_tests.json`
- `tests/test_phase_16_1_static_forbidden_pattern_acceptance_tests.py`

Acceptance criteria:

- tests/docs/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no scanner helper implementation outside the phase test
- forbidden Sparkbot, HumanInput bridge, live adapter, execution, approval, dispatch, persistence, shell, browser, network, file mutation, robotics, and physical-world patterns are checked
- tests pass

Status:

- complete
- tagged as `phase-16.1-static-forbidden-pattern-acceptance-tests`

## Phase 16.2 - Runtime Contract Acceptance Tests

Goal:

Implement test-only contract acceptance coverage against existing non-executing candidate APIs.

Deliverables:

- `docs/PHASE_16_2_RUNTIME_CONTRACT_ACCEPTANCE_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_16_2_runtime_contract_acceptance_tests.json`
- `tests/test_phase_16_2_runtime_contract_acceptance_tests.py`

Acceptance criteria:

- tests/docs/fixtures only
- no runtime code changes
- no `lima/` changes
- no `tests/support/` changes
- execution and side-effect flags remain false
- approval state never becomes approved
- provenance is preserved
- malformed, unknown, stale, replayed, and approval-bypass inputs fail closed
- tests pass

Status:

- complete
- tagged as `phase-16.2-runtime-contract-acceptance-tests`

## Phase 16.3 - Threat Fixture Acceptance Tests

Goal:

Implement synthetic threat fixture acceptance tests for risky candidate categories without live commands, live targets, credentials, private infrastructure, robot instructions, approval tokens, or runtime behavior.

Deliverables:

- `docs/PHASE_16_3_THREAT_FIXTURE_ACCEPTANCE_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_16_3_threat_fixture_acceptance_cases.json`
- `tests/fixtures/runtime_extraction/phase_16_3_threat_fixture_acceptance_tests.json`
- `tests/test_phase_16_3_threat_fixture_acceptance_tests.py`

Acceptance criteria:

- tests/docs/fixtures only
- synthetic inert fixtures only
- no `lima/` changes
- no `tests/support/` changes
- malformed, unknown, stale/replayed, approval-bypass, shell/network/browser/file/robotics, Sparkbot, and HumanInput bridge attempts are covered
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-16.3-threat-fixture-acceptance-tests`

## Phase 16.4 - Test-Only Acceptance Implementation Readiness Review

Goal:

Review the Phase 16.1 through Phase 16.3 test-only acceptance implementation before archive/closeout.

Deliverables:

- `docs/PHASE_16_4_TEST_ONLY_ACCEPTANCE_IMPLEMENTATION_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_16_4_test_only_acceptance_implementation_readiness_review.json`
- `tests/test_phase_16_4_test_only_acceptance_implementation_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- static, contract, and fixture acceptance coverage reviewed as test-only
- Phase 16 ready for archive/closeout
- tests pass

Status:

- complete
- tagged as `phase-16.4-test-only-acceptance-implementation-readiness-review`

## Phase 16.5 - Phase 16 Test-Only Acceptance Archive / Closeout

Goal:

Archive Phase 16 as a completed test-only acceptance-gate implementation lane and preserve the Phase 17 decision gate.

Deliverables:

- `docs/PHASE_16_5_PHASE_16_TEST_ONLY_ACCEPTANCE_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_16_5_phase_16_test_only_acceptance_archive_closeout.json`
- `tests/test_phase_16_5_phase_16_test_only_acceptance_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no new `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- no helper behavior changes
- Phase 16.0 through Phase 16.4 listed as complete
- Phase 5 runtime bridge remains gated
- Phase 17 requires explicit Phil approval
- runtime expansion, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, and physical-world behavior remain blocked
- tests pass

Next likely phase:

- Phase 17 - gated pending explicit Phil approval

Status:

- complete
- tagged as `phase-16.5-phase-16-test-only-acceptance-archive-closeout`

## Phase 17.0 - Phase 16 Acceptance Test Audit Charter

Goal:

Open Phase 17 as a docs/tests/fixtures-only acceptance-gate audit/archive and next-lane decision phase.

Deliverables:

- `docs/PHASE_17_0_PHASE_16_ACCEPTANCE_TEST_AUDIT_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_17_0_phase_16_acceptance_test_audit_charter.json`
- `tests/test_phase_17_0_phase_16_acceptance_test_audit_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 16.0 through Phase 16.5 are in audit scope
- Phase 18 options are listed for later evaluation
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-17.0-phase-16-acceptance-test-audit-charter`

## Phase 17.1 - Acceptance Test Coverage Review

Goal:

Review Phase 16 acceptance-test coverage and identify static/test-only limitations.

Deliverables:

- `docs/PHASE_17_1_ACCEPTANCE_TEST_COVERAGE_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_17_1_acceptance_test_coverage_review.json`
- `tests/test_phase_17_1_acceptance_test_coverage_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 16 static, contract, and threat fixture test coverage is mapped
- runtime expansion remains unapproved
- limitations are explicit
- tests pass

Status:

- complete
- tagged as `phase-17.1-acceptance-test-coverage-review`

## Phase 17.2 - Remaining Safety Gap Review

Goal:

Review remaining safety gaps before any future runtime expansion or integration lane.

Deliverables:

- `docs/PHASE_17_2_REMAINING_SAFETY_GAP_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_17_2_remaining_safety_gap_review.json`
- `tests/test_phase_17_2_remaining_safety_gap_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- remaining gaps are listed
- runtime expansion blockers are explicit
- Sparkbot, HumanInput bridge, live adapter, approval enforcement, audit persistence, and physical-world work remain blocked
- tests pass

Status:

- complete
- tagged as `phase-17.2-remaining-safety-gap-review`

## Phase 17.3 - Next-Lane Decision Matrix

Goal:

Compare Phase 18 options and recommend the safest next lane.

Deliverables:

- `docs/PHASE_17_3_NEXT_LANE_DECISION_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_17_3_next_lane_decision_matrix.json`
- `tests/test_phase_17_3_next_lane_decision_matrix.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- all five Phase 18 options are evaluated
- recommended next direction is explicit
- Phase 18 requires explicit Phil approval
- tests pass

Status:

- complete
- tagged as `phase-17.3-next-lane-decision-matrix`

## Phase 17.4 - Phase 17 Acceptance-Gate Audit Archive / Closeout

Goal:

Archive Phase 17 and preserve the Phase 18 approval question.

Deliverables:

- `docs/PHASE_17_4_PHASE_17_ACCEPTANCE_GATE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_17_4_phase_17_acceptance_gate_audit_archive_closeout.json`
- `tests/test_phase_17_4_phase_17_acceptance_gate_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 17.0 through Phase 17.3 listed as complete
- Phase 16 acceptance tests archived as test-only
- recommended Phase 18 direction is preserved
- Phase 18 requires explicit Phil approval
- tests pass

Next likely phase:

- Phase 18 - gated pending explicit Phil approval

Status:

- complete
- tagged as `phase-17.4-phase-17-acceptance-gate-audit-archive-closeout`

## Phase 18.0 - Regression Hardening Charter

Goal:

Open Phase 18 as a test-only regression hardening lane.

Deliverables:

- `docs/PHASE_18_0_REGRESSION_HARDENING_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_18_0_regression_hardening_charter.json`
- `tests/test_phase_18_0_regression_hardening_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 18 work is limited to regression tests and synthetic fixtures
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-18.0-regression-hardening-charter`

## Phase 18.1 - Candidate API Regression Tests

Goal:

Add regression tests for existing non-executing candidate APIs.

Deliverables:

- `docs/PHASE_18_1_CANDIDATE_API_REGRESSION_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_18_1_candidate_api_regression_tests.json`
- `tests/test_phase_18_1_candidate_api_regression_tests.py`

Acceptance criteria:

- tests/docs/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- non-executing candidate invariants are protected
- dangerous wording does not bypass safety
- raw HumanInput-like payloads remain rejected
- tests pass

Status:

- complete
- tagged as `phase-18.1-candidate-api-regression-tests`

## Phase 18.2 - Acceptance Boundary Regression Fixtures

Goal:

Add synthetic acceptance-boundary regression fixtures and fixture tests.

Deliverables:

- `docs/PHASE_18_2_ACCEPTANCE_BOUNDARY_REGRESSION_FIXTURES.md`
- `tests/fixtures/runtime_extraction/phase_18_2_acceptance_boundary_regression_fixtures.json`
- `tests/fixtures/runtime_extraction/phase_18_2_acceptance_boundary_regression_cases.json`
- `tests/test_phase_18_2_acceptance_boundary_regression_fixtures.py`

Acceptance criteria:

- tests/docs/fixtures only
- synthetic inert fixture cases only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- boundary fixture cases remain non-executing or rejected
- tests pass

Status:

- complete
- tagged as `phase-18.2-acceptance-boundary-regression-fixtures`

## Phase 18.3 - Forbidden Integration Regression Tests

Goal:

Add test-only static regression checks for forbidden integration imports, calls, and side-effect patterns.

Deliverables:

- `docs/PHASE_18_3_FORBIDDEN_INTEGRATION_REGRESSION_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_18_3_forbidden_integration_regression_tests.json`
- `tests/test_phase_18_3_forbidden_integration_regression_tests.py`

Acceptance criteria:

- tests/docs/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- candidate runtime files are scanned by tests only
- forbidden integration imports and calls remain absent
- tests pass

Status:

- complete
- tagged as `phase-18.3-forbidden-integration-regression-tests`

## Phase 18.4 - Regression Hardening Readiness Review

Goal:

Review the Phase 18 regression hardening package before archive/closeout.

Deliverables:

- `docs/PHASE_18_4_REGRESSION_HARDENING_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_18_4_regression_hardening_readiness_review.json`
- `tests/test_phase_18_4_regression_hardening_readiness_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 18.1 through Phase 18.3 reviewed
- ready for archive/closeout
- not ready for runtime implementation
- tests pass

Status:

- complete
- tagged as `phase-18.4-regression-hardening-readiness-review`

## Phase 18.5 - Phase 18 Regression Hardening Archive / Closeout

Goal:

Archive Phase 18 and preserve the Phase 19 decision gate.

Deliverables:

- `docs/PHASE_18_5_PHASE_18_REGRESSION_HARDENING_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_18_5_phase_18_regression_hardening_archive_closeout.json`
- `tests/test_phase_18_5_phase_18_regression_hardening_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 18.0 through Phase 18.4 listed as complete
- Phase 18 archived as test-only regression hardening
- recommended Phase 19 direction is preserved
- Phase 19 requires explicit Phil approval
- tests pass

Next likely phase:

- Phase 19 - gated pending explicit Phil approval

Status:

- complete
- tagged as `phase-18.5-phase-18-regression-hardening-archive-closeout`

## Phase 19.0 - Phase 18 Regression Hardening Audit Charter

Goal:

Open Phase 19 as a docs/tests/fixtures-only audit/archive lane for the Phase 18 regression hardening package.

Deliverables:

- `docs/PHASE_19_0_PHASE_18_REGRESSION_HARDENING_AUDIT_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_19_0_phase_18_regression_hardening_audit_charter.json`
- `tests/test_phase_19_0_phase_18_regression_hardening_audit_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 18.0 through Phase 18.5 are in audit scope
- Phase 20 options are listed for later evaluation
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-19.0-phase-18-regression-hardening-audit-charter`

## Phase 19.1 - Regression Coverage Review

Goal:

Review whether the Phase 18 regression hardening package provides meaningful coverage before any next-lane decision.

Deliverables:

- `docs/PHASE_19_1_REGRESSION_COVERAGE_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_19_1_regression_coverage_review.json`
- `tests/test_phase_19_1_regression_coverage_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 18 candidate API, fixture, forbidden integration, readiness, and archive coverage are reviewed
- static/test-only limitations are documented
- Phase 5 runtime bridge remains gated
- Phase 20 remains unapproved
- tests pass

Status:

- complete
- tagged as `phase-19.1-regression-coverage-review`

## Phase 19.2 - Remaining Regression Gap Review

Goal:

Identify remaining regression gaps before recommending a Phase 20 lane.

Deliverables:

- `docs/PHASE_19_2_REMAINING_REGRESSION_GAP_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_19_2_remaining_regression_gap_review.json`
- `tests/test_phase_19_2_remaining_regression_gap_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- remaining static/test-only limitations are listed
- direct runtime expansion remains blocked
- Phase 5 runtime bridge remains gated
- Phase 20 remains unapproved
- tests pass

Status:

- complete
- tagged as `phase-19.2-remaining-regression-gap-review`

## Phase 19.3 - Next-Lane Decision Matrix

Goal:

Compare Phase 20 options and recommend the safest next lane before any future runtime expansion.

Deliverables:

- `docs/PHASE_19_3_NEXT_LANE_DECISION_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_19_3_next_lane_decision_matrix.json`
- `tests/test_phase_19_3_next_lane_decision_matrix.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- all approved Phase 20 options are evaluated
- recommended Phase 20 direction is no-code design only
- Phase 20 still requires explicit Phil approval
- tests pass

Status:

- complete
- tagged as `phase-19.3-next-lane-decision-matrix`

## Phase 19.4 - Phase 19 Regression Audit Archive / Closeout

Goal:

Archive Phase 19 and preserve the exact Phase 20 approval question.

Deliverables:

- `docs/PHASE_19_4_PHASE_19_REGRESSION_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_19_4_phase_19_regression_audit_archive_closeout.json`
- `tests/test_phase_19_4_phase_19_regression_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 19.0 through Phase 19.3 are listed as complete
- Phase 20 direction and approval question are preserved
- Phase 20 remains unapproved
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-19.4-phase-19-regression-audit-archive-closeout`

## Phase 20.0 - Post-Regression Runtime Slice Design Charter

Goal:

Open Phase 20 as a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice.

Deliverables:

- `docs/PHASE_20_0_POST_REGRESSION_RUNTIME_SLICE_DESIGN_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_20_0_post_regression_runtime_slice_design_charter.json`
- `tests/test_phase_20_0_post_regression_runtime_slice_design_charter.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 18 and Phase 19 inputs are listed
- candidate next-slice options are listed
- Phase 5 runtime bridge remains gated
- Phase 21 remains unapproved
- tests pass

Status:

- complete
- tagged as `phase-20.0-post-regression-runtime-slice-design-charter`

## Phase 20.1 - Next Runtime Slice Options Review

Goal:

Compare next runtime slice options and recommend exactly one future slice or no runtime work.

Deliverables:

- `docs/PHASE_20_1_NEXT_RUNTIME_SLICE_OPTIONS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_20_1_next_runtime_slice_options_review.json`
- `tests/test_phase_20_1_next_runtime_slice_options_review.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- all candidate slice options are reviewed
- exactly one future runtime slice is recommended
- Phase 5 runtime bridge remains gated
- Phase 21 remains unapproved
- tests pass

Status:

- complete
- tagged as `phase-20.1-next-runtime-slice-options-review`

## Phase 20.2 - Exact File-Touch Map For Candidate Slice

Goal:

Define the exact future file-touch map for the candidate provenance hardening slice.

Deliverables:

- `docs/PHASE_20_2_EXACT_FILE_TOUCH_MAP_FOR_CANDIDATE_SLICE.md`
- `tests/fixtures/runtime_extraction/phase_20_2_exact_file_touch_map_for_candidate_slice.json`
- `tests/test_phase_20_2_exact_file_touch_map_for_candidate_slice.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- exact eligible runtime files are listed
- future forbidden runtime files are listed
- Phase 5 runtime bridge remains gated
- Phase 21 remains unapproved
- tests pass

Status:

- complete
- tagged as `phase-20.2-exact-file-touch-map-for-candidate-slice`

## Phase 20.3 - Acceptance Test And Rollback Plan

Goal:

Define future acceptance tests and rollback/audit proof for the candidate provenance hardening slice.

Deliverables:

- `docs/PHASE_20_3_ACCEPTANCE_TEST_AND_ROLLBACK_PLAN.md`
- `tests/fixtures/runtime_extraction/phase_20_3_acceptance_test_and_rollback_plan.json`
- `tests/test_phase_20_3_acceptance_test_and_rollback_plan.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- future provenance acceptance tests are listed
- rollback/audit proof requirements are listed
- Phase 5 runtime bridge remains gated
- Phase 21 remains unapproved
- tests pass

Status:

- complete
- tagged as `phase-20.3-acceptance-test-and-rollback-plan`

## Phase 20.4 - Phase 20 Runtime Slice Approval Gate / Closeout

Goal:

Archive Phase 20 and preserve the exact Phase 21 approval question.

Deliverables:

- `docs/PHASE_20_4_PHASE_20_RUNTIME_SLICE_APPROVAL_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_20_4_phase_20_runtime_slice_approval_gate_closeout.json`
- `tests/test_phase_20_4_phase_20_runtime_slice_approval_gate_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 20.0 through Phase 20.3 are listed as complete
- Phase 21 approval question is preserved
- Phase 21 remains unapproved
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-20.4-phase-20-runtime-slice-approval-gate-closeout`

## Phase 20.5 - Phase 20 Next Runtime Slice Design Lane Audit Archive / Closeout

Goal:

Archive Phase 20 as a completed no-code design lane before any Phase 21 candidate provenance hardening runtime decision.

Deliverables:

- `docs/PHASE_20_5_PHASE_20_NEXT_RUNTIME_SLICE_DESIGN_LANE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_20_5_phase_20_next_runtime_slice_design_lane_audit_archive_closeout.json`
- `tests/test_phase_20_5_phase_20_next_runtime_slice_design_lane_audit_archive_closeout.py`

Acceptance criteria:

- docs/tests/fixtures only
- no `lima/` changes
- no `tests/support/` changes
- no runtime behavior changes
- Phase 20.0 through Phase 20.4 are listed as complete
- Phase 20 is archived as no-code design only
- Phase 21 approval question is preserved
- Phase 21 remains unapproved
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-20.5-phase-20-next-runtime-slice-design-lane-audit-archive-closeout`

## Phase 21.0 - Runtime Slice Preflight Audit / Eligible File Confirmation

Goal:

Confirm Phase 21 eligible runtime files before any implementation.

Deliverables:

- `docs/PHASE_21_0_RUNTIME_SLICE_PREFLIGHT_AUDIT_ELIGIBLE_FILE_CONFIRMATION.md`
- `tests/fixtures/runtime_extraction/phase_21_0_runtime_slice_preflight_audit_eligible_file_confirmation.json`
- `tests/test_phase_21_0_runtime_slice_preflight_audit_eligible_file_confirmation.py`

Acceptance criteria:

- no runtime implementation yet
- eligible runtime files are exactly `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`
- `lima/kernel/__init__.py`, new runtime modules, all other `lima/` files, and `tests/support/` remain forbidden
- Phase 5 runtime bridge remains gated
- tests pass

Status:

- complete
- tagged as `phase-21.0-runtime-slice-preflight-audit-eligible-file-confirmation`

## Phase 21.1 - Candidate Provenance Acceptance Test Scaffolding

Goal:

Scaffold deterministic candidate provenance acceptance tests before runtime implementation.

Deliverables:

- `docs/PHASE_21_1_CANDIDATE_PROVENANCE_ACCEPTANCE_TEST_SCAFFOLDING.md`
- `tests/fixtures/runtime_extraction/phase_21_1_candidate_provenance_acceptance_test_scaffolding.json`
- `tests/fixtures/runtime_extraction/phase_21_1_candidate_provenance_acceptance_cases.json`
- `tests/test_phase_21_1_candidate_provenance_acceptance_test_scaffolding.py`

Acceptance criteria:

- no runtime implementation yet
- valid candidate provenance is preserved by existing candidate APIs
- missing, empty, or non-mapping provenance is rejected or invalid
- suspicious provenance wording does not bypass safety
- stale and replayed candidates remain blocked or invalid
- no forbidden integration, execution, dispatch, approval enforcement, audit persistence, or physical-world surface is reachable

Status:

- complete
- tagged as `phase-21.1-candidate-provenance-acceptance-test-scaffolding`

## Phase 21.2 - Candidate Provenance Hardening Runtime Implementation

Goal:

Implement the narrow candidate provenance hardening runtime slice.

Deliverables:

- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`
- `docs/PHASE_21_2_CANDIDATE_PROVENANCE_HARDENING_RUNTIME_IMPLEMENTATION.md`
- `tests/fixtures/runtime_extraction/phase_21_2_candidate_provenance_hardening_runtime_implementation.json`
- `tests/test_phase_21_2_candidate_provenance_hardening_runtime_implementation.py`

Acceptance criteria:

- runtime edits are limited to `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`
- `lima/kernel/__init__.py`, new runtime modules, all other `lima/` files, and `tests/support/` remain untouched
- provenance construction rejects malformed provenance keys and missing provenance values
- status normalization and validation block malformed or suspicious provenance
- valid provenance is preserved
- execution, approval enforcement, dispatch, audit persistence, Sparkbot wiring, HumanInput bridge behavior, live adapters, and physical-world behavior remain absent

Status:

- complete
- tagged as `phase-21.2-candidate-provenance-hardening-runtime-implementation`

## Phase 21.3 - Candidate Provenance Regression Review

Goal:

Review the Phase 21.2 provenance hardening runtime slice for regression coverage.

Deliverables:

- `docs/PHASE_21_3_CANDIDATE_PROVENANCE_REGRESSION_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_21_3_candidate_provenance_regression_review.json`
- `tests/test_phase_21_3_candidate_provenance_regression_review.py`

Acceptance criteria:

- no runtime changes
- valid provenance remains preserved
- malformed provenance fails closed
- suspicious provenance authority claims remain blocked or invalid
- execution, approval enforcement, dispatch, audit persistence, Sparkbot wiring, HumanInput bridge behavior, live adapters, and physical-world behavior remain absent

Status:

- complete
- tagged as `phase-21.3-candidate-provenance-regression-review`

## Phase 21.4 - Runtime Slice Readiness Review

Goal:

Confirm the Phase 21 candidate provenance hardening runtime slice is ready for archive closeout.

Deliverables:

- `docs/PHASE_21_4_RUNTIME_SLICE_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_21_4_runtime_slice_readiness_review.json`
- `tests/test_phase_21_4_runtime_slice_readiness_review.py`

Acceptance criteria:

- no runtime changes
- Phase 21.0 through Phase 21.3 are reviewed as complete
- candidate provenance hardening remains limited to the approved runtime files
- valid provenance remains preserved
- malformed or suspicious provenance fails closed
- Phase 22 remains gated and requires explicit Phil approval

Status:

- complete
- tagged as `phase-21.4-runtime-slice-readiness-review`

## Phase 21.5 - Phase 21 Runtime Slice Audit Archive / Closeout

Goal:

Archive Phase 21 as a completed narrow runtime slice.

Deliverables:

- `docs/PHASE_21_5_PHASE_21_RUNTIME_SLICE_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_21_5_phase_21_runtime_slice_audit_archive_closeout.json`
- `tests/test_phase_21_5_phase_21_runtime_slice_audit_archive_closeout.py`

Acceptance criteria:

- no runtime changes
- Phase 21.0 through Phase 21.4 are listed as complete
- exact Phase 21 runtime files touched are recorded
- `lima/kernel/__init__.py`, new runtime modules, all other `lima/` files, and `tests/support/` remain outside scope
- runtime remains non-executing, approval-free, dispatch-free, persistence-free, Sparkbot-free, HumanInput-bridge-free, and physical-world-free
- Phase 22 remains gated and requires explicit Phil approval

Status:

- complete
- tagged as `phase-21.5-phase-21-runtime-slice-audit-archive-closeout`

## Phase 22.0 - Post-Phase-21 Runtime Slice Audit Charter

Goal:

Open the Phase 22 no-code decision lane after auditing Phase 21.

Deliverables:

- `docs/PHASE_22_0_POST_PHASE_21_RUNTIME_SLICE_AUDIT_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_22_0_post_phase_21_runtime_slice_audit_charter.json`
- `tests/test_phase_22_0_post_phase_21_runtime_slice_audit_charter.py`

Acceptance criteria:

- no runtime changes
- Phase 21 audit baseline is recorded
- Phase 22 options are listed
- Phase 23 remains gated

Status:

- complete
- tagged as `phase-22.0-post-phase-21-runtime-slice-audit-charter`

## Phase 22.1 - Candidate Provenance Coverage Review

Goal:

Review existing provenance hardening coverage and identify test-only gaps.

Deliverables:

- `docs/PHASE_22_1_CANDIDATE_PROVENANCE_COVERAGE_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_22_1_candidate_provenance_coverage_review.json`
- `tests/test_phase_22_1_candidate_provenance_coverage_review.py`

Acceptance criteria:

- no runtime changes
- covered provenance areas are listed
- remaining test-only coverage limits are documented
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-22.1-candidate-provenance-coverage-review`

## Phase 22.2 - Remaining Safety Gap Review

Goal:

Review remaining safety gaps after Phase 21 and the Phase 22.1 coverage review.

Deliverables:

- `docs/PHASE_22_2_REMAINING_SAFETY_GAP_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_22_2_remaining_safety_gap_review.json`
- `tests/test_phase_22_2_remaining_safety_gap_review.py`

Acceptance criteria:

- no runtime changes
- remaining gaps are identified as test or planning gaps
- no immediate runtime work is recommended
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-22.2-remaining-safety-gap-review`

## Phase 22.3 - Next-Lane Decision Matrix

Goal:

Recommend exactly one Phase 23 direction from the Phase 22 options.

Deliverables:

- `docs/PHASE_22_3_NEXT_LANE_DECISION_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_22_3_next_lane_decision_matrix.json`
- `tests/test_phase_22_3_next_lane_decision_matrix.py`

Acceptance criteria:

- no runtime changes
- exactly one Phase 23 direction is recommended
- runtime and integration expansion options are deferred
- Phase 23 approval question preserves forbidden scope

Status:

- complete
- tagged as `phase-22.3-next-lane-decision-matrix`

## Phase 22.4 - Phase 22 Decision Gate / Closeout

Goal:

Close the Phase 22 decision lane and preserve the Phase 23 approval question.

Deliverables:

- `docs/PHASE_22_4_PHASE_22_DECISION_GATE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_22_4_phase_22_decision_gate_closeout.json`
- `tests/test_phase_22_4_phase_22_decision_gate_closeout.py`

Acceptance criteria:

- no runtime changes
- Phase 22.0 through Phase 22.3 are listed as complete
- Phase 23 direction is test-only hardening for provenance and candidate invariants
- Phase 23 requires explicit Phil approval

Status:

- complete
- tagged as `phase-22.4-phase-22-decision-gate-closeout`

## Phase 23.0 - Provenance Invariant Test Hardening Charter

Goal:

Open the test-only hardening lane for provenance and candidate invariants.

Deliverables:

- `docs/PHASE_23_0_PROVENANCE_INVARIANT_TEST_HARDENING_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_23_0_provenance_invariant_test_hardening_charter.json`
- `tests/test_phase_23_0_provenance_invariant_test_hardening_charter.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- hardening goals are documented
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-23.0-provenance-invariant-test-hardening-charter`

## Phase 23.1 - Candidate Provenance Regression Tests

Goal:

Add deterministic regression tests for existing candidate provenance behavior.

Deliverables:

- `docs/PHASE_23_1_CANDIDATE_PROVENANCE_REGRESSION_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_23_1_candidate_provenance_regression_tests.json`
- `tests/test_phase_23_1_candidate_provenance_regression_tests.py`

Acceptance criteria:

- no runtime changes
- valid provenance is preserved
- missing or malformed provenance fails closed
- stale and replayed candidates remain blocked or invalid
- non-executing invariants remain preserved

Status:

- complete
- tagged as `phase-23.1-candidate-provenance-regression-tests`

## Phase 23.2 - Suspicious Provenance Fixture Hardening

Goal:

Add synthetic suspicious provenance fixtures and tests.

Deliverables:

- `docs/PHASE_23_2_SUSPICIOUS_PROVENANCE_FIXTURE_HARDENING.md`
- `tests/fixtures/runtime_extraction/phase_23_2_suspicious_provenance_cases.json`
- `tests/fixtures/runtime_extraction/phase_23_2_suspicious_provenance_fixture_hardening.json`
- `tests/test_phase_23_2_suspicious_provenance_fixture_hardening.py`

Acceptance criteria:

- no runtime changes
- suspicious provenance authority claims fail closed
- risky action metadata remains non-executing
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-23.2-suspicious-provenance-fixture-hardening`

## Phase 23.3 - Bypass-Wording Provenance Tests

Goal:

Add explicit test-only bypass-wording provenance coverage.

Deliverables:

- `docs/PHASE_23_3_BYPASS_WORDING_PROVENANCE_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_23_3_bypass_wording_cases.json`
- `tests/fixtures/runtime_extraction/phase_23_3_bypass_wording_provenance_tests.json`
- `tests/test_phase_23_3_bypass_wording_provenance_tests.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phil/operator/admin/trusted/urgent/override/approve/emergency wording does not bypass safety
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-23.3-bypass-wording-provenance-tests`

## Phase 23.4 - Provenance Hardening Readiness Review

Goal:

Review Phase 23.0 through Phase 23.3 as a completed test-only provenance hardening package.

Deliverables:

- `docs/PHASE_23_4_PROVENANCE_HARDENING_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_23_4_provenance_hardening_readiness_review.json`
- `tests/test_phase_23_4_provenance_hardening_readiness_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 23.0 through Phase 23.3 are reviewed
- Phase 24 remains gated

Status:

- complete
- tagged as `phase-23.4-provenance-hardening-readiness-review`

## Phase 23.5 - Phase 23 Test-Only Hardening Archive / Closeout

Goal:

Archive Phase 23 as a completed test-only hardening lane.

Deliverables:

- `docs/PHASE_23_5_PHASE_23_TEST_ONLY_HARDENING_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_23_5_phase_23_test_only_hardening_archive_closeout.json`
- `tests/test_phase_23_5_phase_23_test_only_hardening_archive_closeout.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 23.0 through Phase 23.4 are archived
- Phase 5 runtime bridge remains gated
- Phase 24 requires explicit approval

Status:

- complete
- tagged as `phase-23.5-phase-23-test-only-hardening-archive-closeout`

## Phase 24.0 - Phase 23 Hardening Audit Charter

Goal:

Open the docs/tests/fixtures-only audit/archive and next-lane decision phase for the Phase 23 package.

Deliverables:

- `docs/PHASE_24_0_PHASE_23_HARDENING_AUDIT_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_24_0_phase_23_hardening_audit_charter.json`
- `tests/test_phase_24_0_phase_23_hardening_audit_charter.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 23 hardening package is named as audit target
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-24.0-phase-23-hardening-audit-charter`

## Phase 24.1 - Provenance Hardening Coverage Review

Goal:

Review the Phase 23 provenance and candidate-invariant coverage.

Deliverables:

- `docs/PHASE_24_1_PROVENANCE_HARDENING_COVERAGE_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_24_1_provenance_hardening_coverage_review.json`
- `tests/test_phase_24_1_provenance_hardening_coverage_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 23 coverage is summarized
- coverage limitations remain static/test-only

Status:

- complete
- tagged as `phase-24.1-provenance-hardening-coverage-review`

## Phase 24.2 - Remaining Candidate Invariant Gap Review

Goal:

Identify remaining provenance and candidate-invariant gaps as planning inputs.

Deliverables:

- `docs/PHASE_24_2_REMAINING_CANDIDATE_INVARIANT_GAP_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_24_2_remaining_candidate_invariant_gap_review.json`
- `tests/test_phase_24_2_remaining_candidate_invariant_gap_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- remaining gaps are documented as planning inputs only
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-24.2-remaining-candidate-invariant-gap-review`

## Phase 24.3 - Next-Lane Decision Matrix

Goal:

Evaluate Phase 25 options and recommend exactly one next direction.

Deliverables:

- `docs/PHASE_24_3_NEXT_LANE_DECISION_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_24_3_next_lane_decision_matrix.json`
- `tests/test_phase_24_3_next_lane_decision_matrix.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- all recommended Phase 25 options are evaluated
- exactly one Phase 25 direction is recommended

Status:

- complete
- tagged as `phase-24.3-next-lane-decision-matrix`

## Phase 24.4 - Phase 24 Hardening Audit Archive / Closeout

Goal:

Archive Phase 24 and preserve the Phase 25 decision gate.

Deliverables:

- `docs/PHASE_24_4_PHASE_24_HARDENING_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_24_4_phase_24_hardening_audit_archive_closeout.json`
- `tests/test_phase_24_4_phase_24_hardening_audit_archive_closeout.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 24.0 through Phase 24.3 are archived
- Phase 25 requires explicit approval

Status:

- complete
- tagged as `phase-24.4-phase-24-hardening-audit-archive-closeout`

## Phase 25.0 - Cross-API Candidate Invariant Matrix Charter

Goal:

Open a test-only hardening lane for a cross-API candidate invariant matrix.

Deliverables:

- `docs/PHASE_25_0_CROSS_API_CANDIDATE_INVARIANT_MATRIX_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_25_0_cross_api_candidate_invariant_matrix_charter.json`
- `tests/test_phase_25_0_cross_api_candidate_invariant_matrix_charter.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- cross-API matrix APIs and invariants are declared
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-25.0-cross-api-candidate-invariant-matrix-charter`

## Phase 25.1 - Candidate API Matrix Fixtures

Goal:

Add synthetic fixtures for the cross-API candidate invariant matrix.

Deliverables:

- `docs/PHASE_25_1_CANDIDATE_API_MATRIX_FIXTURES.md`
- `tests/fixtures/runtime_extraction/phase_25_1_candidate_api_matrix_cases.json`
- `tests/fixtures/runtime_extraction/phase_25_1_candidate_api_matrix_fixtures.json`
- `tests/test_phase_25_1_candidate_api_matrix_fixtures.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- matrix cases cover valid, malformed, suspicious, stale, replayed, risky, and bypass-wording scenarios

Status:

- complete
- tagged as `phase-25.1-candidate-api-matrix-fixtures`

## Phase 25.2 - Cross-API Non-Execution Invariant Tests

Goal:

Add deterministic tests proving existing candidate-facing APIs preserve non-execution invariants.

Deliverables:

- `docs/PHASE_25_2_CROSS_API_NON_EXECUTION_INVARIANT_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_25_2_cross_api_non_execution_invariant_tests.json`
- `tests/test_phase_25_2_cross_api_non_execution_invariant_tests.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- construction, normalization, and validation remain non-executing
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-25.2-cross-api-non-execution-invariant-tests`

## Phase 25.3 - Cross-API Provenance and Status Invariant Tests

Goal:

Add deterministic tests for provenance and status invariants across existing candidate-facing APIs.

Deliverables:

- `docs/PHASE_25_3_CROSS_API_PROVENANCE_AND_STATUS_INVARIANT_TESTS.md`
- `tests/fixtures/runtime_extraction/phase_25_3_cross_api_provenance_and_status_invariant_tests.json`
- `tests/test_phase_25_3_cross_api_provenance_and_status_invariant_tests.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- valid, suspicious, stale, replayed, unknown, malformed, and risky cases remain safe
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-25.3-cross-api-provenance-and-status-invariant-tests`

## Phase 25.4 - Cross-API Boundary Readiness Review

Goal:

Review Phase 25.0 through Phase 25.3 as ready for archive/closeout.

Deliverables:

- `docs/PHASE_25_4_CROSS_API_BOUNDARY_READINESS_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_25_4_cross_api_boundary_readiness_review.json`
- `tests/test_phase_25_4_cross_api_boundary_readiness_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 25.0 through Phase 25.3 are reviewed
- Phase 26 requires explicit approval

Status:

- complete
- tagged as `phase-25.4-cross-api-boundary-readiness-review`

## Phase 25.5 - Phase 25 Test-Only Hardening Archive / Closeout

Goal:

Archive Phase 25 as a completed test-only cross-API candidate invariant hardening lane.

Deliverables:

- `docs/PHASE_25_5_PHASE_25_TEST_ONLY_HARDENING_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_25_5_phase_25_test_only_hardening_archive_closeout.json`
- `tests/test_phase_25_5_phase_25_test_only_hardening_archive_closeout.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 25.0 through Phase 25.4 are archived
- Phase 26 requires explicit approval

Status:

- complete
- tagged as `phase-25.5-phase-25-test-only-hardening-archive-closeout`

## Phase 26.0 - Phase 25 Cross-API Invariant Audit Charter

Goal:

Open the approved docs/tests/fixtures-only audit/archive and next-lane decision lane for the Phase 25 package.

Deliverables:

- `docs/PHASE_26_0_PHASE_25_CROSS_API_INVARIANT_AUDIT_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_26_0_phase_25_cross_api_invariant_audit_charter.json`
- `tests/test_phase_26_0_phase_25_cross_api_invariant_audit_charter.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 25.0 through Phase 25.5 are in audit scope
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-26.0-phase-25-cross-api-invariant-audit-charter`

## Phase 26.1 - Cross-API Invariant Coverage Review

Goal:

Review Phase 25 cross-API candidate invariant coverage.

Deliverables:

- `docs/PHASE_26_1_CROSS_API_INVARIANT_COVERAGE_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_26_1_cross_api_invariant_coverage_review.json`
- `tests/test_phase_26_1_cross_api_invariant_coverage_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- existing candidate construction, status normalization, validation, and provenance hardening coverage is reviewed
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-26.1-cross-api-invariant-coverage-review`

## Phase 26.2 - Remaining Cross-API Gap Review

Goal:

Record remaining cross-API candidate invariant gaps as planning inputs only.

Deliverables:

- `docs/PHASE_26_2_REMAINING_CROSS_API_GAP_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_26_2_remaining_cross_api_gap_review.json`
- `tests/test_phase_26_2_remaining_cross_api_gap_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- remaining gaps are planning inputs only
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-26.2-remaining-cross-api-gap-review`

## Phase 26.3 - Next-Lane Decision Matrix

Goal:

Evaluate Phase 27 options and recommend exactly one next direction.

Deliverables:

- `docs/PHASE_26_3_NEXT_LANE_DECISION_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_26_3_next_lane_decision_matrix.json`
- `tests/test_phase_26_3_next_lane_decision_matrix.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- all recommended Phase 27 options are evaluated
- exactly one Phase 27 direction is recommended
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-26.3-next-lane-decision-matrix`

## Phase 26.4 - Phase 26 Cross-API Audit Archive / Closeout

Goal:

Archive Phase 26 and preserve the Phase 27 decision gate.

Deliverables:

- `docs/PHASE_26_4_PHASE_26_CROSS_API_AUDIT_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_26_4_phase_26_cross_api_audit_archive_closeout.json`
- `tests/test_phase_26_4_phase_26_cross_api_audit_archive_closeout.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 26.0 through Phase 26.3 are archived
- Phase 27 requires explicit approval

Status:

- complete
- tagged as `phase-26.4-phase-26-cross-api-audit-archive-closeout`

## Phase 27.0 - Phase 26 Preservation Audit Charter

Goal:

Open the approved docs/tests/fixtures-only preservation and roadmap decision lane after Phase 26.

Deliverables:

- `docs/PHASE_27_0_PHASE_26_PRESERVATION_AUDIT_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_27_0_phase_26_preservation_audit_charter.json`
- `tests/test_phase_27_0_phase_26_preservation_audit_charter.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 26.0 through Phase 26.4 are in audit scope
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-27.0-phase-26-preservation-audit-charter`

## Phase 27.1 - Current Runtime/Test State Preservation Record

Goal:

Record and preserve the current known-good runtime/test state.

Deliverables:

- `docs/PHASE_27_1_CURRENT_RUNTIME_TEST_STATE_PRESERVATION_RECORD.md`
- `tests/fixtures/runtime_extraction/phase_27_1_current_runtime_test_state_preservation_record.json`
- `tests/test_phase_27_1_current_runtime_test_state_preservation_record.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- constrained non-executing candidate API state is preserved
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-27.1-current-runtime-test-state-preservation-record`

## Phase 27.2 - Gated Runtime Boundary Review

Goal:

Review the runtime and integration boundaries that remain gated.

Deliverables:

- `docs/PHASE_27_2_GATED_RUNTIME_BOUNDARY_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_27_2_gated_runtime_boundary_review.json`
- `tests/test_phase_27_2_gated_runtime_boundary_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Sparkbot, HumanInput bridge, live adapters, execution, dispatch, persistence, and physical-world behavior remain absent
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-27.2-gated-runtime-boundary-review`

## Phase 27.3 - Next-Lane Risk Decision Matrix

Goal:

Evaluate Phase 28 options and recommend exactly one next direction.

Deliverables:

- `docs/PHASE_27_3_NEXT_LANE_RISK_DECISION_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_27_3_next_lane_risk_decision_matrix.json`
- `tests/test_phase_27_3_next_lane_risk_decision_matrix.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- all recommended Phase 28 options are evaluated
- exactly one Phase 28 direction is recommended
- Phase 5 runtime bridge remains gated

Status:

- complete
- tagged as `phase-27.3-next-lane-risk-decision-matrix`

## Phase 27.4 - Phase 27 Preservation Archive / Closeout

Goal:

Archive Phase 27 and preserve the Phase 28 decision gate.

Deliverables:

- `docs/PHASE_27_4_PHASE_27_PRESERVATION_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_27_4_phase_27_preservation_archive_closeout.json`
- `tests/test_phase_27_4_phase_27_preservation_archive_closeout.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 27.0 through Phase 27.3 are archived
- Phase 28 requires explicit approval

Status:

- complete
- tagged as `phase-27.4-phase-27-preservation-archive-closeout`

## Phase 28.0 - Phase 27 Preservation Status Audit Charter

Goal:

Open the approved docs/tests/fixtures-only preservation status review and prevent preservation-loop drift.

Deliverables:

- `docs/PHASE_28_0_PHASE_27_PRESERVATION_STATUS_AUDIT_CHARTER.md`
- `tests/fixtures/runtime_extraction/phase_28_0_phase_27_preservation_status_audit_charter.json`
- `tests/test_phase_28_0_phase_27_preservation_status_audit_charter.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 27.0 through Phase 27.4 are in audit scope
- Phase 29 must make a sharper decision than automatic preservation

Status:

- complete
- tagged as `phase-28.0-phase-27-preservation-status-audit-charter`

## Phase 28.1 - Stable Runtime/Test State Review

Goal:

Confirm the current runtime/test state remains stable and preserved.

Deliverables:

- `docs/PHASE_28_1_STABLE_RUNTIME_TEST_STATE_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_28_1_stable_runtime_test_state_review.json`
- `tests/test_phase_28_1_stable_runtime_test_state_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- current runtime/test state remains stable
- no concrete immediate test-only hardening gap is found

Status:

- complete
- tagged as `phase-28.1-stable-runtime-test-state-review`

## Phase 28.2 - Preservation Pause Justification Review

Goal:

Review whether continued preservation pause is still justified.

Deliverables:

- `docs/PHASE_28_2_PRESERVATION_PAUSE_JUSTIFICATION_REVIEW.md`
- `tests/fixtures/runtime_extraction/phase_28_2_preservation_pause_justification_review.json`
- `tests/test_phase_28_2_preservation_pause_justification_review.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- continued pause is not recommended without a specific documented risk
- Phase 29 direction remains no-code unless explicitly approved later

Status:

- complete
- tagged as `phase-28.2-preservation-pause-justification-review`

## Phase 28.3 - Phase 29 Decision Readiness Matrix

Goal:

Evaluate Phase 29 options and recommend exactly one sharper next direction.

Deliverables:

- `docs/PHASE_28_3_PHASE_29_DECISION_READINESS_MATRIX.md`
- `tests/fixtures/runtime_extraction/phase_28_3_phase_29_decision_readiness_matrix.json`
- `tests/test_phase_28_3_phase_29_decision_readiness_matrix.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- all recommended Phase 29 options are evaluated
- exactly one Phase 29 direction is recommended
- Phase 29 remains no-code unless explicitly approved later

Status:

- complete
- tagged as `phase-28.3-phase-29-decision-readiness-matrix`

## Phase 28.4 - Phase 28 Preservation Status Archive / Closeout

Goal:

Archive Phase 28 and preserve the Phase 29 decision gate.

Deliverables:

- `docs/PHASE_28_4_PHASE_28_PRESERVATION_STATUS_ARCHIVE_CLOSEOUT.md`
- `tests/fixtures/runtime_extraction/phase_28_4_phase_28_preservation_status_archive_closeout.json`
- `tests/test_phase_28_4_phase_28_preservation_status_archive_closeout.py`

Acceptance criteria:

- no runtime changes
- no `lima/` changes
- no `tests/support/` changes
- Phase 28.0 through Phase 28.3 are archived
- Phase 29 requires explicit approval

Status:

- complete
- tagged as `phase-28.4-phase-28-preservation-status-archive-closeout`

Reserved from Phase 3.4:

- Phase 3.5 - LIMA Product Family and Adaptive Trust Doctrine
- product-family and adaptive-trust doctrine is deferred and not implemented in Phase 3.4
- reserve LIMA AI OS as the trust-governed runtime underneath shells
- reserve Sparkbot as the open-source hobby/R&D shell and reference source
- reserve ARC Bot as a future commercial office-worker shell
- reserve custom business and private-sector bots as future client-specific shells
- reserve Robo/automation systems as future driver-plane consumers
- reserve adaptive trust gates as the default future UX, with breakglass as rare emergency or privileged override
