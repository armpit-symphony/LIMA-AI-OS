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

- explicit operator runtime implementation decision

Status:

- complete
- tagged as `phase-8.4-runtime-implementation-approval-gate-closeout`

Reserved from Phase 3.4:

- Phase 3.5 - LIMA Product Family and Adaptive Trust Doctrine
- product-family and adaptive-trust doctrine is deferred and not implemented in Phase 3.4
- reserve LIMA AI OS as the trust-governed runtime underneath shells
- reserve Sparkbot as the open-source hobby/R&D shell and reference source
- reserve ARC Bot as a future commercial office-worker shell
- reserve custom business and private-sector bots as future client-specific shells
- reserve Robo/automation systems as future driver-plane consumers
- reserve adaptive trust gates as the default future UX, with breakglass as rare emergency or privileged override
