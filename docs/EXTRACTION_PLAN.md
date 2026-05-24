# Extraction Plan

Current phase and branch guidance lives in `docs/CURRENT_PROJECT_STATE.md`. Read that file before using this extraction plan for implementation sequencing.

LIMA Runtime is extracted from Sparkbot in phases. Phase 0 is contracts/docs/stubs only.

Do not migrate code until contracts are approved.

## Phase 0: Contracts, Docs, Stubs

Scope:

- Establish architecture documents.
- Define public contracts for Guardian, Harness, Spine, Driver, Storage, Shell, ToolPack, approvals, audit events, model calls, and tool calls.
- Define the Natural Language Control Plane contracts for `HumanInput`, `IntentEnvelope`, `ClarificationRequest`, risk classes, and the `IntentCompilerProtocol`.
- Create importable package skeleton.
- Add import-only validation.

Acceptance criteria:

- Repository imports cleanly.
- Contract modules compile on Python 3.11+.
- Docs state Guardian invariant and MCP boundary rule.
- No real execution paths exist.
- No Sparkbot implementation code is copied.
- No secrets or production deploys are touched.

## Phase 0.5: Natural Language Control Plane

Scope:

- Complete the Intent Compiler boundary before any Sparkbot Harness or tool execution extraction.
- Define how Sparkbot chat and voice commands later adapt into the `IntentCompilerProtocol`.
- Normalize text and voice into the same typed intent contract.
- Require ambiguity handling before execution.
- Require audit linkage from raw human input to typed intent, Guardian decision, action, and result.
- Document future thought/BCI input as confirmation-only and never a direct execution path.

Acceptance criteria:

- Sparkbot chat/voice flows have a planned adapter boundary into the Intent Compiler.
- No raw chat-to-tool behavior is preserved as a runtime contract.
- Consequential execution requires typed intent and a Guardian decision or approval token.
- Future BCI input remains low-confidence, explicit-confirmation-only, and Guardian-reviewed.

Hard gate:

Phase 0.5 must be complete before any Sparkbot Harness/tool execution extraction. Sparkbot may currently have direct chat-to-tool behavior. LIMA Runtime must not inherit that shortcut. It must inherit a governed `HumanInput -> IntentEnvelope -> GuardianDecision` path.

## Phase 0.6: Sparkbot Entrypoint Inventory

Scope:

- Review Sparkbot's current entrypoints before extracting Guardian, Harness, Spine, or tool execution paths.
- Classify inspected code paths as shell-specific, runtime/kernel candidates, Guardian gates, Harness/model concerns, Driver/tool concerns, Spine/audit concerns, or deprecated/unsafe shortcut patterns.
- Map current entrypoints to future `HumanInput`, `IntentEnvelope`, `GuardianDecision`, Harness, Driver, Spine, ToolPack, or Shell contracts.
- Identify raw chat-to-tool shortcut risks, Guardian coverage gaps, and tool-pack scoping concerns.

Acceptance criteria:

- `docs/SPARKBOT_ENTRYPOINT_INVENTORY.md` is reviewed before Phase 1 extraction begins.
- No Sparkbot code is copied.
- No runtime implementation is added.
- Potential direct chat/voice/model-to-tool paths are identified and blocked from becoming runtime contracts.

Hard gate:

Do not extract any code path that allows raw chat/voice to execute tools without `IntentEnvelope` and `GuardianDecision`.

## Phase 0.7: Guardian Decision ID Contract

Scope:

- Define the mandatory `GuardianDecision.decision_id` contract before extracting any Sparkbot execution path.
- Require every consequential Harness, Tool, Driver, Terminal, File, Browser, Network, Admin, Payment, Robot, or deployment action to carry `decision_id`.
- Require downstream Spine/Audit events to carry `decision_id`, and `intent_id` / `input_id` when available.
- Keep denied, escalated, expired, revoked, and superseded decisions auditable.

Acceptance criteria:

- `docs/GUARDIAN_DECISION_CONTRACT.md` is reviewed before Phase 1 extraction begins.
- No Sparkbot code is copied.
- No runtime implementation is added.
- Harness, Driver, Tool, Terminal, Robot, and Spine/Audit contracts have a `decision_id` boundary.

Hard gate:

No Sparkbot execution path may be extracted until it can carry or be adapted to `GuardianDecision.decision_id`.

Specific blockers:

- `stream_chat_with_tools()` must be split or wrapped so planning and execution are separated by `GuardianDecision`.
- Voice transcript paths must carry `HumanInput.input_id` and transcript confidence.
- Terminal/PTY paths must be critical-risk and decision-gated.
- Robotics bridge must require typed intent and `decision_id` before robot MCP command planning/execution.
- Tool catalogue execution must require tool-pack scoping plus `decision_id`.

## Phase 0.8: Tool-Pack Scoping Contract

Scope:

- Define deny-by-default tool-pack scoping before Harness or tool catalogue extraction.
- Require shells to declare allowed, default, denied, and critical tool packs.
- Require `GuardianDecision.allowed_tool_packs` to constrain the Harness tool shortlist.
- Require tool exposure decisions to be auditable.

Acceptance criteria:

- `docs/TOOL_PACK_SCOPING.md` is reviewed before Phase 1 extraction begins.
- No Sparkbot code is copied.
- No runtime implementation is added.
- Harness contracts receive selected tools, not the full catalogue.
- Critical packs require explicit risk and approval policy.

Hard gate:

No Harness/tool catalogue extraction until Sparkbot tools are inventoried into packs and scoped.

Specific blockers:

- `stream_chat_with_tools()` must not receive the full tool catalogue.
- Terminal/admin/robot/payment/deploy tools must be critical packs.
- File/network/browser tools must have explicit risk and approval policy.
- Tool-pack exposure must be auditable.
- `GuardianDecision.allowed_tool_packs` must constrain the Harness shortlist.

## Phase 0.9: Sparkbot Tool-Pack Inventory

Scope:

- Inventory Sparkbot's current static tools, dynamic skills, MCP manifests, routes, scripts, and workflow surfaces.
- Map known tool surfaces into future LIMA tool packs.
- Mark unknown or unclassified tool surfaces as denied by default.
- Carry full-catalogue exposure risks forward before Harness extraction.

Acceptance criteria:

- `docs/SPARKBOT_TOOL_PACK_INVENTORY.md` is reviewed before Phase 1 extraction begins.
- No Sparkbot code is copied.
- No runtime implementation is added.
- Critical packs are identified.
- Unknown tools remain denied until classified.

Hard gate:

No Harness/tool catalogue extraction until Sparkbot tool surfaces are grouped into packs and unknown tools are reviewed.

Specific blockers:

- `stream_chat_with_tools()` cannot be extracted with full-catalogue exposure.
- Terminal/admin/robot/payment/deploy tools must be critical packs.
- Files/browser/network/comms/calendar tools require risk and approval policy.
- Unknown tools must be classified before extraction.
- `GuardianDecision.allowed_tool_packs` must constrain `selected_tools`.

## Phase 0.10: Tool-Pack Risk Policy

Scope:

- Define default risk and approval policy for every starter tool pack.
- Define mixed read/write pack rules before any enforcement exists.
- Define dynamic skill classification requirements.
- Define scheduled/autonomous decision inheritance requirements.
- Keep policy as docs/contracts/tests only.

Acceptance criteria:

- `docs/TOOL_PACK_RISK_POLICY.md` is reviewed before Phase 1 extraction begins.
- No Sparkbot code is copied.
- No runtime implementation is added.
- Every starter pack has default risk and approval guidance.
- Unknown and dynamic tools remain denied until classified.

Hard gate:

No Harness/tool execution extraction until pack risk policy exists and is reviewed.

Specific blockers:

- Mixed read/write packs must have action-level risk.
- Dynamic skills must be classified before exposure.
- Scheduled/autonomous actions must inherit or renew `decision_id`.
- Terminal/admin/robot/payment/deploy packs must remain critical-risk.
- Unknown tools are denied by default.

## Phase 0.11: Approval Metadata Contract

Scope:

- Define approval metadata required for high/critical-risk actions.
- Define approval status and method contracts.
- Define breakglass approval rules.
- Define scheduled/autonomous approval inheritance.
- Keep approval metadata as docs/contracts/tests only.

Acceptance criteria:

- `docs/APPROVAL_METADATA_CONTRACT.md` is reviewed before Phase 1 extraction begins.
- No Sparkbot code is copied.
- No runtime implementation is added.
- Approval metadata attaches to `GuardianDecision.decision_id`.
- Approval does not replace `GuardianDecision`.

Hard gate:

No terminal/admin/deploy/payment/secret/robot/critical action extraction until approval metadata is defined and reviewed.

Specific blockers:

- Terminal/PTY needs OPERATOR_PIN or BREAKGLASS metadata.
- Deploy/payment/admin-write needs explicit approval metadata.
- Robot physical-world action needs explicit confirmation and dry-run/simulation metadata where available.
- Scheduled/autonomous execution must inherit or renew approval metadata.
- Breakglass must be short-lived, scoped, and auditable.

## Phase 0.12: Spine / Audit Lineage Contract

Scope:

- Define end-to-end lineage across human input, typed intent, Guardian decision, approval, policy/tool exposure, execution, and result.
- Define audit event categories and statuses.
- Define `AuditLineageRecord` and expanded `SpineEvent` contract shape.
- Define scheduled/autonomous lineage inheritance.
- Define critical action lineage requirements.
- Keep lineage as docs/contracts/tests only.

Acceptance criteria:

- `docs/SPINE_AUDIT_LINEAGE_CONTRACT.md` is reviewed before Phase 1 extraction begins.
- No Sparkbot code is copied.
- No runtime implementation is added.
- `lineage_id` links consequential chains.
- Downstream execution events carry `decision_id`.
- Denied, blocked, failed, expired, revoked, and superseded actions remain auditable.

Hard gate:

No Guardian/Harness/Spine extraction until lineage contract is reviewed.

Specific blockers:

- `stream_chat_with_tools()` must be split/wrapped to emit lineage events.
- Voice path must preserve `input_id` and transcript confidence.
- Terminal/PTY must create critical lineage events.
- Robotics bridge must create robot action lineage events.
- Dynamic skills must record `exposure_id` and `execution_id`.
- Audit events must not contain raw secrets.

## Phase 0.13: Redaction / Privacy Contract

Scope:

- Define privacy, redaction, reference, retention, and visibility contracts before audit persistence.
- Define default handling for secrets, transcripts, model context, tool args/results, terminal output, files, memory, browser/network data, robot sensors, and future BCI/thought-adjacent data.
- Add optional audit/spine privacy metadata fields.
- Keep redaction/privacy as docs/contracts/tests only.

Acceptance criteria:

- `docs/REDACTION_PRIVACY_CONTRACT.md` is reviewed before Phase 1 extraction begins.
- No Sparkbot code is copied.
- No runtime implementation is added.
- No storage or redaction implementation is added.
- Raw secrets are referenced, never stored in audit events.
- Sensitive content has privacy/redaction/retention/visibility classes.

Hard gate:

No Spine storage, audit persistence, Sparkbot adapter emission, terminal/PTY audit capture, model prompt logging, tool result logging, browser/network capture, voice transcript persistence, memory persistence, or robot sensor logging until redaction/privacy contract is reviewed.

Specific blockers:

- Raw secrets must never be written to audit events.
- Model prompts/tool args/results need privacy/redaction classes.
- Terminal output must be redaction-safe.
- Voice transcripts need `transcript_ref` and privacy class.
- BCI/thought-adjacent data is biometric and confirm-only.
- Robot sensor data needs safety/privacy defaults.
- Audit views need visibility classes.

## Phase 0.14: Runtime Boundary Map

Scope:

- Map current Sparkbot, LIMA Guardian Suite, and LIMA Robo-OS surfaces to future LIMA Runtime boundaries.
- Consolidate Phase 0 through Phase 0.13 extraction gates before Phase 1 begins.
- Mark unsafe shortcuts and unclassified surfaces as do-not-extract-yet.
- Keep the map as docs/contracts/tests only.

Acceptance criteria:

- `docs/RUNTIME_BOUNDARY_MAP.md` is reviewed before Phase 1 extraction begins.
- Reference repo commits are recorded.
- Each candidate code path is classified.
- Do-not-extract-yet paths are explicit.
- Sparkbot parity preserves behavior, not unsafe shortcuts.
- Guardian Suite coupling is documented.
- Robo-OS is classified as driver/runtime integration.
- All extraction candidates map to Phase 0 contracts.
- No Sparkbot, Guardian Suite, or Robo-OS implementation is copied.
- No runtime implementation is added.

Hard gate:

No Phase 1 extraction until Runtime Boundary Map is reviewed.

Specific requirements:

- each candidate code path must be classified
- do-not-extract-yet paths must be explicit
- Sparkbot parity must preserve behavior, not unsafe shortcuts
- Guardian Suite coupling must be documented
- Robo-OS must be classified as driver/runtime integration
- all extraction candidates must map to Phase 0 contracts

## Phase 0.15: Extraction Readiness Review

Scope:

- Produce the final Phase 0 readiness review before Phase 1 extraction.
- Recheck Sparkbot, LIMA Guardian Suite, and LIMA Robo-OS reference commits.
- Consolidate ready areas, blocked areas, do-not-extract-yet shortcuts, and Phase 1 no-go areas.
- Identify the first safe Phase 1 target.
- Keep the review as docs/contracts/tests only.

Acceptance criteria:

- `docs/EXTRACTION_READINESS_REVIEW.md` is merged.
- Reference repos are rechecked read-only.
- Blocked items are explicit.
- First safe extraction target is identified.
- Phase 1 no-go areas are documented.
- No implementation is copied.
- No runtime behavior is added.

Hard gate:

No Phase 1 extraction until Extraction Readiness Review is merged.

Recommended first Phase 1 target:

`phase-1-0-guardian-suite-decoupling-audit`

No-go areas:

- Harness/tool execution
- `stream_chat_with_tools` extraction
- terminal/PTY
- Robo-OS physical action
- audit persistence
- redaction runtime
- policy/approval enforcement

## Phase 1: Decouple Guardian

Scope:

- Review recent Sparkbot Guardian improvements before extraction.
- Decouple Guardian modules from Sparkbot imports such as `app.crud`, `app.models`, route modules, and UI-specific assumptions.
- Preserve policy, auth, vault, verifier, approvals, breakglass, memory policy, token/cost control, and audit behavior behind contracts.

Acceptance criteria:

- Guardian core can import without Sparkbot application models.
- Sparkbot adapter remains explicit.
- Secret handling uses references, not raw secret event payloads.
- Existing Sparkbot Guardian tests are mapped to runtime parity tests.

## Phase 1.0: Guardian Suite Decoupling Audit

Scope:

- Inspect LIMA-Guardian-Suite read-only.
- Identify coupling to Sparkbot `app.crud`, `app.models`, `app.services`, route modules, direct Sparkbot DB sessions, local deployment paths, and direct persistence.
- Define forbidden imports for future `lima.guardian` code.
- Add non-runtime import-boundary tests in LIMA-AI-OS.
- Keep this phase as audit/import-boundary work only.

Acceptance criteria:

- `docs/PHASE_1_0_GUARDIAN_SUITE_DECOUPLING_AUDIT.md` exists.
- Coupled Guardian Suite files are listed with recommended boundaries.
- `lima.guardian` import-boundary tests reject Sparkbot backend imports.
- First extraction seam is identified.
- No Guardian enforcement is implemented.
- No tool execution is implemented.
- No vault secret migration or DB migration is added.
- No Sparkbot or LIMA-Guardian-Suite files are modified.

Hard gate:

No Guardian extraction until Sparkbot `app.crud` / `app.models` / `app.services` coupling is removed or isolated behind LIMA contracts/adapters.

Specific no-go areas:

- modules importing `app.crud` directly
- modules importing `app.models` directly
- modules importing `app.services` directly
- live vault secret storage/reveal/use
- live PIN or breakglass enforcement
- scheduled task execution
- Sparkbot chat/tool route imports
- direct SQLite stores as Guardian core
- audit persistence

## Phase 1.1: Vault/Auth Interface Skeleton

Scope:

- Define non-executing Auth, Vault, and Breakglass reference contracts.
- Define provider protocols that describe actors, auth context, secret references, vault access decisions, and breakglass metadata.
- Keep all provider protocols as interfaces only.
- Document forbidden live behavior before any vault/auth extraction.

Acceptance criteria:

- Auth contracts exist.
- Vault contracts exist.
- Breakglass session reference contract exists.
- Protocols are non-executing.
- No raw secret value fields exist.
- No Sparkbot imports are added.
- No live auth/vault behavior is added.
- No PIN verification, encryption/decryption, DB/storage, or breakglass enforcement is added.
- Existing Guardian import-boundary tests pass.

Hard gate:

No vault/auth extraction until non-executing interfaces are reviewed.

Specific blockers:

- no raw secret value fields
- no direct Sparkbot DB access
- no Sparkbot `ChatUser` dependency
- no live PIN verification
- no live decryption
- no breakglass enforcement
- no Sparkbot deployment paths

## Phase 1.2: Vault/Auth Provider Boundary Tests

Scope:

- Add tests that protect future Vault/Auth providers and adapter skeletons from Sparkbot backend imports.
- Block raw secret fields in Vault/Auth dataclasses.
- Block live auth, vault, and breakglass method names from Vault/Auth provider protocols.
- Keep tests repo-local and safe with the current minimal package layout.
- Keep this phase as docs/tests only.

Acceptance criteria:

- Provider boundary tests exist.
- Forbidden import strings are blocked in local LIMA provider/interface paths.
- Forbidden secret/auth methods are blocked from Vault/Auth provider protocols.
- Forbidden raw secret field names are blocked from Vault/Auth dataclasses.
- No provider or adapter implementation is added.
- No reference repo inspection occurs inside tests.

Hard gate:

No Vault/Auth adapter skeletons until provider-boundary tests are merged.

Specific blockers:

- no Sparkbot imports
- no raw secret fields
- no live auth methods
- no decrypt/encrypt/get_secret methods
- no breakglass bypass/open_live_session methods
- no DB/session coupling

## Phase 1.3: Vault/Auth Fake Providers

Scope:

- Add test-only fake Auth, Vault, and Breakglass providers.
- Keep providers in memory only.
- Use contract objects only.
- Validate fake provider shape with tests.
- Keep real adapters blocked.

Acceptance criteria:

- Fake providers implement the Phase 1.1 provider protocol shape.
- Fake providers use in-memory contract metadata only.
- Fake Vault provider stores only `VaultSecretRef` metadata.
- Fake Breakglass provider stores only `BreakglassSessionRef` metadata.
- No live auth, PIN verification, decryption, DB/storage, environment access, file access, or external service calls are added.
- Provider-boundary tests continue to pass.

Hard gate:

Fake providers are allowed for tests only. Real adapters remain blocked.

Specific blockers:

- no live provider adapters
- no real secret values
- no DB/storage
- no PIN verification
- no vault encryption/decryption
- no breakglass enforcement
- no Sparkbot backend internals

## Phase 1.4: Guardian Decision Fake Evaluator

Scope:

- Add a fake in-memory Guardian decision evaluator for contract tests.
- Turn `ConsequentialActionRequest` records into `GuardianDecision` records.
- Record fake decisions in memory only.
- Keep real Guardian enforcement blocked.

Acceptance criteria:

- Fake decisions carry `decision_id`.
- Critical actions do not auto-approve by default.
- No tool, model, driver, terminal, file, network, browser, payment, deploy, or robot execution is added.
- No live approval, auth, breakglass, policy, or production behavior is added.
- Boundary tests continue to pass.

Hard gate:

Fake Guardian decision evaluator is allowed for tests only. Real Guardian enforcement remains blocked.

No real enforcement until:

- policy enforcement design
- approval enforcement design
- lineage emission design
- redaction/privacy implementation
- Sparkbot adapter review

## Phase 1.5: Policy/Risk Fake Evaluator

Scope:

- Add a fake in-memory policy/risk evaluator for contract tests.
- Turn `PolicyEvaluationContext` records into `PolicyDecision` records.
- Use in-memory `ToolPackRiskPolicy` and `ToolPackRiskRule` objects only.
- Keep real policy enforcement blocked.

Acceptance criteria:

- Unknown packs/tools deny by default.
- High/critical packs do not auto-allow.
- `PolicyDecision` does not replace `GuardianDecision`.
- No tool, model, driver, terminal, file, network, browser, payment, deploy, or robot execution is added.
- No live approval, Guardian, auth, breakglass, policy, or production behavior is added.
- Boundary tests continue to pass.

Hard gate:

Fake policy/risk evaluator is allowed for tests only. Real policy enforcement remains blocked.

No real enforcement until:

- Guardian enforcement design
- approval enforcement design
- lineage emission design
- redaction/privacy implementation
- Sparkbot adapter review
- tool-pack runtime enforcement design

## Phase 1.6: Approval Fake Recorder

Scope:

- Add a fake in-memory `ApprovalMetadata` recorder for contract tests.
- Record and retrieve `ApprovalMetadata` and `ApprovalScope` records.
- Keep real approval enforcement blocked.
- Keep PIN and breakglass behavior blocked.

Acceptance criteria:

- Approval metadata remains evidence only.
- Approval metadata does not replace `GuardianDecision`.
- No approval tokens are issued.
- No PIN verification or breakglass enforcement is added.
- No tool, model, driver, terminal, file, network, browser, payment, deploy, or robot execution is added.
- Boundary tests continue to pass.

Hard gate:

Fake approval recorder is allowed for tests only. Real approval enforcement remains blocked.

No real approval enforcement until:

- PIN verification design
- breakglass enforcement design
- Guardian enforcement design
- policy enforcement design
- lineage emission design
- redaction/privacy implementation
- Sparkbot adapter review

## Phase 1.7: Spine/Audit Fake Recorder

Scope:

- Add a fake in-memory Spine/Audit recorder for contract tests.
- Record and retrieve `SpineEvent` and `AuditLineageRecord` contract objects.
- Keep real Spine storage and audit persistence blocked.
- Keep redaction implementation blocked.

Acceptance criteria:

- No real persistence is added.
- No DB/storage or file writes are added.
- No raw secrets are stored.
- No raw prompts, transcripts, tool outputs, terminal output, or sensor data are stored.
- No tool, model, driver, terminal, file, network, browser, payment, deploy, or robot execution is added.
- Boundary tests continue to pass.

Hard gate:

Fake Spine/Audit recorder is allowed for tests only. Real Spine storage and audit persistence remain blocked.

No real persistence until:

- storage design
- redaction/privacy implementation
- audit view filtering
- secret scanning
- retention enforcement
- Sparkbot adapter emission review
- Guardian/policy/approval enforcement review

## Phase 1.8: Guardian Fake Pipeline

Scope:

- Add a fake in-memory Guardian pipeline for contract tests.
- Compose fake policy, Guardian decision, approval, and Spine/Audit components.
- Turn `ConsequentialActionRequest` records into fake policy, decision, approval, and lineage records.
- Keep real Guardian pipeline behavior blocked.

Acceptance criteria:

- Critical actions do not auto-approve.
- Unknown actions deny or escalate and remain auditable.
- Fake lineage is recorded.
- `PolicyDecision` does not replace `GuardianDecision`.
- `ApprovalMetadata` remains evidence, not execution.
- No real Guardian, policy, or approval enforcement is added.
- No tool, model, driver, terminal, file, network, browser, payment, deploy, or robot execution is added.
- Boundary tests continue to pass.

Hard gate:

Fake Guardian pipeline is allowed for tests only. Real Guardian pipeline remains blocked.

No real pipeline until:

- Guardian enforcement design
- policy enforcement design
- approval enforcement design
- redaction/privacy implementation
- lineage emission design
- Sparkbot adapter review
- tool-pack runtime enforcement design

## Phase 1.9: Fake Pipeline Readiness Review

Scope:

- Review the fake Guardian pipeline after Phase 1.8.
- Decide whether contract composition is ready for the first adapter-design branch.
- Document what the fake pipeline proves and what remains blocked.
- Keep this phase docs/tests-only.

Acceptance criteria:

- Fake pipeline readiness review exists.
- GO/NO-GO decision is documented.
- First adapter-design branch is identified.
- Production integration remains blocked.
- Real enforcement, execution, persistence, and adapters remain blocked.
- Tests continue to pass.

Hard gate:

No adapter design until fake pipeline readiness review is merged.

After merge:

GO only for Phase 1.10 Sparkbot HumanInput Adapter Design.

NO-GO for production adapter wiring, real enforcement, tool execution, Harness extraction, terminal/PTY, Robo-OS physical action, audit persistence, and redaction runtime.

## Phase 1.10: Sparkbot HumanInput Adapter Design

Scope:

- Design how Sparkbot chat, voice, meeting, Workstation, SparkBud, terminal/operator, MCP approval, and robotics natural language surfaces become LIMA `HumanInput` records.
- Inventory current Sparkbot input surfaces against future LIMA adapter boundaries.
- Define actor, shell, session, room, meeting, message, operator, and source-reference mapping candidates.
- Define privacy and redaction defaults before any adapter implementation or audit persistence.
- Keep this phase docs/tests-only.

Acceptance criteria:

- Sparkbot input surfaces are inventoried.
- Chat, voice, meeting, Workstation, SparkBud, terminal/operator, MCP, approval, and robot request surfaces have future `HumanInput` mapping notes.
- Raw chat-to-tool shortcut is blocked.
- No Sparkbot code is modified.
- No adapter implementation or production wiring is added.
- No model, tool, terminal/PTY, driver, or Robo-OS physical action execution is added.
- No audit persistence or redaction runtime is added.

Hard gate:

Sparkbot HumanInput adapter design is allowed. Production adapter implementation remains blocked.

No adapter implementation until:

- HumanInput mapping is reviewed
- privacy/redaction defaults are reviewed
- raw chat-to-tool shortcut is blocked
- lineage plan is reviewed
- Sparkbot `origin/main` is rechecked

No-go:

- `stream_chat_with_tools` extraction
- tool execution
- model execution
- terminal/PTY
- Robo-OS physical action
- audit persistence
- production Sparkbot wiring

## Phase 1.11: HumanInput Adapter Contract

Scope:

- Define describe-only contracts for mapping Sparkbot input surfaces to LIMA `HumanInput` records.
- Formalize adapter surface names, mapping metadata, blocked shortcuts, lineage notes, and privacy notes.
- Keep the protocol describe-only so future adapter implementation remains a separate reviewed phase.
- Keep this phase contracts/docs/tests-only.

Acceptance criteria:

- `lima/contracts/adapters.py` exists.
- `HumanInputAdapterSurface`, `HumanInputAdapterMapping`, `HumanInputAdapterDesign`, and `AdapterDesignProtocol` exist.
- `AdapterDesignProtocol` exposes describe methods only.
- No `adapt`, `execute`, `run`, `call_model`, `call_tool`, `wire_route`, `send`, `persist`, or `open_terminal` methods are added.
- No Sparkbot imports are added.
- No runtime behavior, production route wiring, model/tool execution, terminal/PTY, Robo-OS physical action, audit persistence, or redaction runtime is added.

Hard gate:

HumanInput adapter contracts are allowed. Production adapter implementation remains blocked.

No implementation until:

- contract reviewed
- Sparkbot `origin/main` rechecked
- identity/session mapping reviewed
- privacy/redaction defaults reviewed
- raw chat-to-tool shortcut block reviewed

No-go:

- live Sparkbot routes
- `stream_chat_with_tools` extraction
- model/tool execution
- terminal/PTY
- Robo-OS physical action
- audit persistence

## Phase 1.12A: Owner Autonomy & Safety Policy

Scope:

- Define how owner-controlled autonomy replaces constant approval prompts.
- Define autonomy levels, capability rules, trusted device/session policy, identity confidence, verbal approval, breakglass configuration, vault/personal data protection, destructive action defaults, external communication rules, robot safety constitution, and robot safety modes.
- Keep this phase docs/contracts/tests-only.

Acceptance criteria:

- `docs/OWNER_AUTONOMY_SAFETY_POLICY.md` exists and is reviewed.
- Owner autonomy is defined as policy, trusted context, identity confidence, risk class, capability boundary, and escalation only when needed.
- Guardian remains mandatory for consequential execution.
- Law, human safety, and configured safety policy override owner command.
- No runtime behavior, adapter implementation, production wiring, model/tool execution, terminal/PTY, Robo-OS physical action, audit persistence, or Sparkbot changes are added.

Hard gate:

No behavior-bearing adapter/skeleton/enforcement/robot/tool work until Owner Autonomy & Safety Policy is reviewed.

No-go:

- live Sparkbot routes
- behavior-bearing adapters
- production wiring
- Guardian enforcement implementation
- policy enforcement implementation
- model/tool execution
- terminal/PTY
- Robo-OS physical action
- audit persistence
- raw secret handling

## Phase 1.12: Sparkbot Adapter Readiness Review

Scope:

- Review whether LIMA is ready for a first non-production Sparkbot HumanInput adapter skeleton.
- Recheck Sparkbot `origin/main` read-only for adapter-relevant input surfaces.
- Include Owner Autonomy & Safety Policy as passive metadata context only.
- Keep this phase review/docs/tests-only.

Acceptance criteria:

- `docs/PHASE_1_12_SPARKBOT_ADAPTER_READINESS_REVIEW.md` exists.
- Sparkbot `origin/main` is rechecked and the inspected commit is recorded.
- GO/NO-GO decision for Phase 1.13 is documented.
- Phase 1.13 allowed skeleton scope is limited to neutral payloads -> `HumanInput`.
- Production wiring, `stream_chat_with_tools`, model/tool execution, terminal/PTY, robot action, persistence, and autonomy enforcement remain blocked.
- No adapter implementation is added.

Hard gate:

No Sparkbot HumanInput adapter skeleton until Phase 1.12 readiness review is merged.

After merge:

GO only for Phase 1.13 non-production HumanInput adapter skeleton using neutral payloads.

NO-GO:

- Sparkbot imports
- route wiring
- `stream_chat_with_tools` import
- `execute_tool` import
- model/harness calls
- terminal/PTY
- robot action
- audit persistence
- production integration
- autonomy enforcement

## Phase 1.13: Sparkbot HumanInput Adapter Skeleton

Scope:

- Add a non-production LIMA-owned Sparkbot HumanInput adapter skeleton.
- Convert neutral payload dataclasses into `HumanInput` records only.
- Carry trusted context and owner-autonomy notes as passive metadata only.
- Keep production Sparkbot wiring and execution paths blocked.

Acceptance criteria:

- `lima/adapters/sparkbot_humaninput.py` exists.
- Neutral chat, voice, meeting, and operator payload dataclasses exist.
- Adapter methods return `HumanInput` only.
- No Sparkbot imports, route wiring, model/tool execution, persistence, autonomy enforcement, `IntentEnvelope`, `GuardianDecision`, `ApprovalMetadata`, `PolicyDecision`, or `SpineEvent` creation is added.
- Tests prove mappings and forbidden import/method boundaries.

Hard gate:

Sparkbot HumanInput adapter skeleton may exist only as non-production neutral-payload conversion.

Still blocked:

- production Sparkbot route wiring
- live WebSocket integration
- `stream_chat_with_tools`
- `execute_tool`
- model/harness calls
- tool execution
- terminal/PTY
- Robo-OS
- persistence
- autonomy enforcement
- GuardianDecision creation
- IntentEnvelope creation
- ApprovalMetadata creation
- PolicyDecision creation
- SpineEvent creation

## Phase 1.14: HumanInput Adapter Readiness Review

Scope:

- Review whether the non-production Sparkbot HumanInput adapter skeleton is ready to be composed with the fake Guardian pipeline in a future test-only branch.
- Decide whether current identity, session, privacy, and passive autonomy metadata are sufficient for fake-pipeline composition.
- Clarify that any HumanInput-to-fake-pipeline bridge must remain separate from the adapter.
- Keep this phase review/docs/tests-only.

Acceptance criteria:

- `docs/PHASE_1_14_HUMANINPUT_ADAPTER_READINESS_REVIEW.md` exists.
- GO/NO-GO decision for Phase 1.15 is documented.
- Adapter remains HumanInput-only.
- Bridge, if allowed, is separate and test-only.
- Production wiring, model/tool execution, real enforcement, persistence, and autonomy enforcement remain blocked.

Hard gate:

No HumanInput-to-fake-pipeline bridge until Phase 1.14 readiness review is merged.

After merge:

GO only for Phase 1.15 test-only HumanInput Fake Pipeline Bridge.

NO-GO:

- production Sparkbot wiring
- adapter creating GuardianDecision
- adapter creating IntentEnvelope
- adapter calling fake pipeline directly
- real IntentCompiler
- real Guardian enforcement
- model/tool execution
- persistence
- autonomy enforcement
- terminal/PTY
- Robo-OS physical action

## Phase 1.15: HumanInput Fake Pipeline Bridge

Scope:

- Add a test-only bridge from `HumanInput` to `FakeGuardianPipeline`.
- Keep the bridge separate from `SparkbotHumanInputAdapter`.
- Build test-only `ConsequentialActionRequest` objects from explicit HumanInput metadata only.
- Keep adapter output limited to `HumanInput`.
- Keep production wiring, real enforcement, and execution blocked.

Acceptance criteria:

- `lima/guardian/humaninput_pipeline_fakes.py` exists.
- Bridge is test-only and calls `FakeGuardianPipeline` only.
- Adapter remains HumanInput-only and does not create `ConsequentialActionRequest`.
- No natural-language intent inference, real IntentCompiler, model/tool execution, driver calls, persistence, or autonomy enforcement is added.
- Critical/unknown requests do not auto-approve.
- Tests prove boundary separation.

Hard gate:

HumanInput fake pipeline bridge is allowed for tests only.

Still blocked:

- production Sparkbot wiring
- real IntentCompiler
- natural-language intent inference
- adapter-created ConsequentialActionRequest
- adapter-created IntentEnvelope
- adapter-created GuardianDecision
- model/tool execution
- terminal/PTY
- Robo-OS physical action
- audit persistence
- redaction runtime
- autonomy enforcement

## Phase 1.16: Phase One Readiness Review

Scope:

- Review Phase 1 progress after the HumanInput fake pipeline bridge.
- Decide whether LIMA is ready for any real Sparkbot adapter implementation.
- Recheck Sparkbot `origin/main` read-only for adapter-relevant surface movement.
- Keep this phase review/docs/tests-only.

Acceptance criteria:

- `docs/PHASE_1_16_PHASE_ONE_READINESS_REVIEW.md` exists.
- Sparkbot `origin/main` is rechecked and the inspected commit is recorded.
- Proven and not-proven areas are documented.
- Readiness decision is documented.
- Recommended next branch is identified.
- Production adapter remains blocked.
- No runtime behavior is added.

Hard gate:

No production Sparkbot adapter implementation until Phase 1.16 is merged.

After merge:

GO only for Phase 1.17 Identity / Session / Trust Context Mapping Review.

NO-GO:

- production adapter
- live auth/session lookup
- trusted device enforcement
- autonomy enforcement
- model/tool execution
- `stream_chat_with_tools`
- terminal/PTY
- Robo-OS physical action
- audit persistence
- real enforcement

## Phase 1.17: Identity / Session / Trust Context Mapping Review

Scope:

- Review how adapter metadata should map to future identity, session, trust context, and owner autonomy contracts.
- Keep `actor_ref`, `session_ref`, `trusted_context_ref`, `autonomy_notes`, and privacy metadata passive.
- Recheck Sparkbot `origin/main` read-only for identity/session/auth and adapter-relevant surfaces.
- Keep this phase review/docs/tests-only.

Acceptance criteria:

- `docs/PHASE_1_17_IDENTITY_SESSION_TRUST_CONTEXT_REVIEW.md` exists.
- Sparkbot `origin/main` is rechecked and the inspected commit is recorded.
- Future `AuthContext` mapping is proposed.
- Future `TrustedDeviceContext` mapping is proposed.
- Future `IdentityConfidence` mapping is proposed.
- Owner autonomy mapping notes remain policy-only.
- No runtime auth/session/trust/autonomy behavior is added.

Hard gate:

No production Sparkbot adapter until identity/session/trust-context mapping is reviewed and contract extensions are added if needed.

After merge:

GO only for Phase 1.18 AuthContext / Trust Contract Extension.

NO-GO:

- live auth/session lookup
- trusted device enforcement
- autonomy enforcement
- PIN verification
- face/voice recognition
- production adapter
- model/tool execution
- `stream_chat_with_tools`
- terminal/PTY
- Robo-OS physical action

## Phase 1.18: AuthContext / Trust Contract Extension

Scope:

- Add descriptive contract types for trusted device context, identity confidence, session context, and owner-autonomy context.
- Keep trust and autonomy references passive.
- Keep this phase contracts/docs/tests-only.

Acceptance criteria:

- AuthContext/trust contract extensions are allowed.
- Live auth/session/trust/autonomy implementation remains blocked.
- No enforcement or production Sparkbot adapter behavior is added.
- Tests continue to pass.

Hard gate:

AuthContext/trust contract extensions are allowed.
Live auth/session/trust/autonomy implementation remains blocked.

NO-GO:

- live auth/session lookup
- trusted device enforcement
- autonomy enforcement
- PIN verification
- face/voice recognition
- production adapter
- model/tool execution
- `stream_chat_with_tools`
- terminal/PTY
- Robo-OS physical action

## Phase 1.19: Adapter Fixture Tests with Fake AuthContext

Scope:

- Add test-only adapter fixture tests with fake AuthContext and trust contract references.
- Prove the Sparkbot HumanInput adapter skeleton can carry identity/session/trust/autonomy refs passively.
- Keep the adapter HumanInput-only.

Acceptance criteria:

- Adapter fixture tests with fake AuthContext are allowed.
- Live auth/session/trust/autonomy remains blocked.
- No enforcement or production Sparkbot adapter behavior is added.
- Tests continue to pass.

NO-GO:

- live auth/session lookup
- trusted device enforcement
- autonomy enforcement
- PIN verification
- face/voice recognition
- production adapter
- model/tool execution
- `stream_chat_with_tools`
- terminal/PTY
- Robo-OS physical action

## Phase 1.20: Real Adapter Readiness Review

Scope:

- Review readiness for real Sparkbot adapter implementation after fake AuthContext fixture tests.
- Recheck Sparkbot `origin/main` read-only for adapter-relevant movement.
- Decide the next safe Phase 1.21 branch.
- Keep this phase review/docs/tests-only.

Acceptance criteria:

- `docs/PHASE_1_20_REAL_ADAPTER_READINESS_REVIEW.md` exists.
- Sparkbot `origin/main` is rechecked.
- Production adapter go/no-go decision is documented.
- Next safe branch is identified.
- No runtime behavior is added.
- Tests continue to pass.

Hard gate:

No production Sparkbot adapter implementation until Real Adapter Readiness Review is merged.

After merge:

Proceed only with the selected Phase 1.21 safe branch.

Production wiring remains blocked unless explicitly approved.

## Phase 1.21: Sparkbot Payload Fixture Mirror

Scope:

- Create LIMA-owned synthetic fixture mirrors of Sparkbot input payload shapes.
- Cover chat, voice/transcript, meeting, operator, MCP approval, and robot request surfaces where inspected.
- Keep fixtures as tests/docs only.

Acceptance criteria:

- Payload fixture mirroring is allowed.
- Production adapter remains blocked.
- Fixtures use synthetic data only.
- Sparkbot `origin/main` is rechecked and recorded.
- No Sparkbot imports, route wiring, execution, or behavior changes are added.
- Tests continue to pass.

Hard gate:

Production adapter remains blocked.

No production adapter until:

- fixture mirror reviewed
- Sparkbot `origin/main` rechecked
- payload drift reviewed
- identity/session/trust mapping reviewed
- redaction/privacy reviewed

## Phase 1.22: Payload Drift Check Contract

Scope:

- Define the repeatable payload drift review contract.
- Add fixture drift metadata.
- Record Sparkbot `origin/main` review requirements.
- Keep this phase docs/contracts/tests only.

Acceptance criteria:

- Payload drift check contract exists.
- Fixture drift metadata exists.
- Dirty local Sparkbot files are not source of truth.
- Production adapter remains blocked.
- No Sparkbot imports, route wiring, model/tool execution, or behavior changes are added.
- Tests continue to pass.

Hard gate:

No production Sparkbot adapter until payload drift check is reviewed against Sparkbot `origin/main`.

NO-GO:

- using dirty local Sparkbot files as source of truth
- Sparkbot imports
- production wiring
- model/tool execution
- `stream_chat_with_tools`
- live auth/session lookup
- trusted device enforcement

## Phase 1.23: Adapter Boundary Hardening

Scope:

- Add tests that scan local `lima/adapters` modules.
- Block Sparkbot runtime imports, route layers, model/tool execution paths, terminal/PTY, persistence, robot paths, and external service dependencies.
- Block behavior-bearing adapter methods.
- Keep the current adapter HumanInput-only.

Acceptance criteria:

- Adapter boundary tests exist.
- No Sparkbot imports, route wiring, model/tool execution, terminal/PTY, persistence, or production behavior is added.
- Current adapter returns HumanInput only.
- Tests continue to pass.

Hard gate:

No further adapter work until adapter boundary hardening is merged.

Production adapter remains blocked.

## Phase 1.24: Phase One Adapter Safety Review

Scope:

- Review Phase 1 adapter safety work.
- Record Sparkbot freshness.
- Decide whether Phase 1 can close.
- Define the safe Phase 2.0 starting point.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Phase 1 adapter safety review exists.
- Production adapter remains blocked.
- Phase 2 start is defined.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

No Phase 2 work until Phase 1.24 is merged.

After merge:

GO only for Phase 2.0 Non-production Adapter Fixture Harness.

NO-GO:

- production Sparkbot wiring
- `stream_chat_with_tools`
- model/tool execution
- live auth/session lookup
- trusted device enforcement
- autonomy enforcement
- audit persistence
- real enforcement

## Phase 2.0: Non-production Adapter Fixture Harness

Scope:

- Compose LIMA-owned Sparkbot payload fixtures with the non-production adapter and fake Guardian pipeline.
- Run fixture dictionaries through `SparkbotHumanInputAdapter`, `HumanInputFakePipelineBridge`, `FakeGuardianPipeline`, and fake lineage records.
- Keep the harness fixture-only, in-memory, and non-production.
- Keep adapter output limited to `HumanInput`.

Acceptance criteria:

- Non-production adapter fixture harness is allowed.
- LIMA-owned fixtures are the only inputs.
- No Sparkbot imports, live routes, production wiring, model/tool/driver execution, persistence, or real enforcement is added.
- Critical and unknown requests do not auto-approve.
- Tests continue to pass.

Hard gate:

Phase 2.0 is fixture harness only. Production Sparkbot wiring remains blocked.

Still blocked:

- production Sparkbot wiring
- live routes/WebSocket adapter
- `stream_chat_with_tools`
- `execute_tool`
- model/tool execution
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device/autonomy enforcement
- audit persistence
- redaction runtime
- real IntentCompiler / Guardian / policy / approval enforcement

## Phase 2.1: Fixture Harness Coverage Review

Scope:

- Review current LIMA-owned fixture categories and Phase 2.0 harness coverage.
- Recheck Sparkbot `origin/main` read-only for adapter-relevant movement.
- Identify fixture/harness coverage gaps before expanding the non-production harness.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Fixture harness coverage review exists.
- Sparkbot `origin/main` is checked.
- Coverage gaps and next branch are documented.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

No further fixture harness expansion until coverage review is merged.

After merge:

Proceed only with selected Phase 2.2 safe branch.

Production adapter remains blocked.

## Phase 2.2: Fixture Coverage Expansion

Scope:

- Add LIMA-owned synthetic fixtures for frontend chat variants, Workstation launch context, SparkBud launch context, passive auth/session refs, and model-routing/autonomous pacing context.
- Update fixture metadata and harness tests for safe non-executing coverage.
- Keep all expanded fixtures synthetic mirrors only.

Acceptance criteria:

- Expanded fixture categories exist.
- Drift metadata is present and current for the new fixtures.
- Fixture tests and non-production harness tests cover the new categories.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, live auth/session lookup, trusted device/autonomy enforcement, or real enforcement is added.

Hard gate:

Fixture coverage expansion is allowed.

Production adapter remains blocked.

No production adapter until:

- expanded fixtures are reviewed
- drift metadata is current
- unsupported/non-executing categories are documented
- identity/session/privacy/autonomy metadata remains passive

## Phase 2.3: Harness Coverage Readiness Review

Scope:

- Review expanded Phase 2.2 fixture and harness coverage.
- Confirm Sparkbot `origin/main` freshness.
- Decide whether a repeatable fixture regression harness is safe as the next non-production step.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Harness coverage readiness review exists.
- Sparkbot `origin/main` is checked.
- Coverage readiness matrix and risks are documented.
- Phase 2.4 safe branch is identified.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

No fixture regression harness until Phase 2.3 coverage readiness review is merged.

After merge:

GO only for selected Phase 2.4 safe branch: `phase-2-4-fixture-regression-harness`.

Production adapter remains blocked.

## Phase 2.4: Fixture Regression Harness

Scope:

- Add a test-only fixture regression harness for LIMA-owned synthetic Sparkbot payload fixtures.
- Load every fixture file under `tests/fixtures/sparkbot_payloads`.
- Run compatible fixtures through `AdapterFixtureHarness`.
- Report unsupported/non-executing categories explicitly.
- Verify critical and unknown paths do not auto-approve.

Acceptance criteria:

- Fixture regression harness is allowed for tests only.
- Production adapter remains blocked.
- Regression harness is reviewed before any production adapter work.
- Fixture drift is reviewed before real adapter work.
- Unsupported categories are documented and cannot pass silently.
- Identity/session/trust mapping remains passive.
- Redaction/privacy remains reviewed before persistence.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, or real enforcement is added.

Hard gate:

No production adapter until:

- regression harness reviewed
- fixture drift reviewed
- unsupported categories documented
- identity/session/trust mapping remains passive
- redaction/privacy reviewed

## Phase 2.5: Fixture Regression Readiness Review

Scope:

- Review whether the Phase 2.4 fixture regression harness is ready to become a standing safety gate.
- Recheck Sparkbot `origin/main` read-only for fixture-relevant movement.
- Decide the next safe Phase 2.6 branch.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Fixture Regression Readiness Review is merged before future adapter expansion.
- Sparkbot `origin/main` is checked.
- Safety gate decision is documented.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

No future adapter expansion until Fixture Regression Readiness Review is merged.

After merge:

Proceed only with selected Phase 2.6 safe branch.

Production adapter remains blocked.

## Phase 2.6: Fixture Regression CI Gate Docs

Scope:

- Document fixture regression as a required safety gate before adapter-adjacent changes.
- List required validation commands and test files.
- List PR blocking conditions and manual review requirements.
- Keep this phase docs/tests only.

Acceptance criteria:

- Fixture regression CI gate documentation exists.
- Required tests and commands are documented.
- PR blocking conditions are documented.
- Manual review requirements are documented.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

Before future adapter-adjacent PRs:

- fixture regression tests must pass
- adapter boundary tests must pass
- payload drift metadata must be current
- Sparkbot origin/main must be reviewed if relevant

Production adapter remains blocked.

## Phase 2.7: Phase Two Readiness Review

Scope:

- Review Phase 2 progress and choose the next safe branch.
- Recheck Sparkbot `origin/main` read-only for fixture/harness-relevant movement.
- Summarize proven and not-proven areas.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Phase Two Readiness Review exists.
- Sparkbot `origin/main` is checked.
- Next safe Phase 2.8 branch is identified.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

No adapter-adjacent expansion until Phase 2.7 is merged.

After merge:

GO only for selected Phase 2.8 branch.

Production adapter remains blocked.

## Phase 2.8: Fixture Regression Report Artifact

Scope:

- Add test-only markdown/dict report helpers for fixture regression results.
- Keep report artifacts review-only and non-production.
- Do not write files by default.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Fixture regression report artifact is allowed for reviewability only.
- Report artifacts are not audit persistence.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

Report artifacts must not become audit persistence, production telemetry, Guardian evidence, production authorization, or runtime state.

## Phase 2.9: Regression Report Readiness Review

Scope:

- Review whether the Phase 2.8 report artifact is ready as a standing human-readable review artifact.
- Identify missing gate context before adapter-adjacent expansion.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Regression Report Readiness Review is merged before adapter-adjacent expansion.
- Report remains non-persistent and non-production.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, audit persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

No adapter-adjacent expansion until Regression Report Readiness Review is merged.

After merge:

GO only for Phase 2.10 Regression Report Gate Hardening.

Production adapter remains blocked.

## Phase 2.10: Regression Report Gate Hardening

Scope:

- Add gate/review fields to fixture regression markdown and dict report output.
- Keep report fields reviewability-only.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Fixture regression reports may include gate context for reviewability only.
- Report `gate_status` does not authorize production adapter work.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, audit persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

Report gate context must not become audit persistence, production telemetry, Guardian evidence, production authorization, or runtime state.

## Phase 2.11: Regression Gate Readiness Review

Scope:

- Review whether fixture regression reports and gate fields are strong enough as the standing adapter-adjacent safety gate.
- Recheck Sparkbot `origin/main` read-only for adapter/gate-relevant movement.
- Keep production adapter wiring blocked.

Acceptance criteria:

- Regression Gate Readiness Review is merged before adapter-adjacent expansion.
- Sparkbot `origin/main` is checked.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, audit persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

No adapter-adjacent expansion until Regression Gate Readiness Review is merged.

After merge:

GO only for selected Phase 2.12 safe branch.

Production adapter remains blocked.

## Phase 2.12: Adapter Safety Gate Finalization

Scope:

- Consolidate adapter-adjacent safety rules into `docs/ADAPTER_SAFETY_GATE.md`.
- Document required tests, Sparkbot freshness, fixture drift, forbidden imports, forbidden behaviors, regression report rules, and manual review requirements.
- Keep production adapter wiring blocked.

Acceptance criteria:

- `docs/ADAPTER_SAFETY_GATE.md` is now the standing gate for adapter-adjacent work.
- No adapter-adjacent PR may merge without satisfying that gate.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, audit persistence, or real enforcement is added.
- Tests continue to pass.

Hard gate:

No adapter-adjacent PR may merge without satisfying `docs/ADAPTER_SAFETY_GATE.md`.

Production adapter remains blocked.

## Phase 2.13: Adapter Safety Gate Readiness Review

Scope:

- Review whether `docs/ADAPTER_SAFETY_GATE.md` is complete enough as the standing adapter-adjacent safety gate.
- Decide whether adapter-safety gate work may pause.
- Identify the next non-production kernel boundary.

Acceptance criteria:

- Adapter safety gate work may pause after Phase 2.13 if the readiness decision approves.
- Sparkbot `origin/main` is checked.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, audit persistence, or real enforcement is added.
- Tests continue to pass.

After merge:

GO only for selected Phase 2.14 safe branch.

Production adapter remains blocked.

## Phase 2.14: IntentEnvelope Test Design Review

Scope:

- Review how LIMA should safely design a test-only HumanInput-to-IntentEnvelope path in a future phase.
- Define the explicit typed intent metadata expected for future fixtures.
- Keep natural-language inference, real IntentCompiler, execution, production wiring, and GuardianDecision creation blocked.

Acceptance criteria:

- No HumanInput-to-IntentEnvelope implementation until Phase 2.14 review is merged.
- After merge, GO only for Phase 2.15 IntentEnvelope Test Fixtures.
- Production adapter remains blocked.
- No runtime behavior, Sparkbot imports, production wiring, model/tool execution, persistence, audit persistence, real IntentCompiler, natural-language inference, GuardianDecision creation from adapter, or real enforcement is added.
- Tests continue to pass.

NO-GO:

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation from adapter
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- real enforcement

## Phase 2.15: IntentEnvelope Test Fixtures

IntentEnvelope test fixtures are allowed.

Still blocked:

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation from adapter
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- real enforcement

## Phase 2.16: IntentEnvelope Fixture Readiness Review

No IntentEnvelope fixture harness until Phase 2.16 readiness review is merged.

After merge:

GO only for Phase 2.17 IntentEnvelope Fixture Harness.

NO-GO:

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- real enforcement

## Phase 2.17: IntentEnvelope Fixture Harness

IntentEnvelope fixture harness is allowed for tests only.

Still blocked:

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- real enforcement

## Phase 2.18: IntentEnvelope Harness Readiness Review

No IntentEnvelope-adjacent expansion until Phase 2.18 readiness review is merged.

After merge:

GO only for Phase 2.19 IntentEnvelope Safety Gate Docs.

NO-GO:

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- real enforcement

## Phase 2.19: IntentEnvelope Safety Gate Docs

`docs/INTENTENVELOPE_SAFETY_GATE.md` is now the standing gate for IntentEnvelope-adjacent work.

No IntentEnvelope-adjacent PR may merge without satisfying it.

Real IntentCompiler remains blocked.

## Phase 2.20: IntentEnvelope Safety Gate Readiness Review

IntentEnvelope safety-gate work may pause after Phase 2.20 if readiness decision approves.

After merge:

GO only for Phase 2.21 Guardian Request Test Design Review.

NO-GO:

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation
- production Sparkbot wiring
- real enforcement

## Phase 2.29 Gate: Fake GuardianDecision Test Fixtures

Fake GuardianDecision test fixtures are allowed.

Still blocked:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2.30 Gate: Fake GuardianDecision Fixture Readiness Review

No fake GuardianDecision fixture harness until Phase 2.30 readiness review is merged.

After merge:

GO only for Phase 2.31 Fake GuardianDecision Fixture Harness.

NO-GO:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2.31 Gate: Fake GuardianDecision Fixture Harness

Fake GuardianDecision fixture harness is allowed for tests only.

Still blocked:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- real enforcement

## Phase 2.32 Gate: Fake GuardianDecision Harness Readiness Review

No fake GuardianDecision-adjacent expansion until Phase 2.32 readiness review is merged.

After merge:

GO only for Phase 2.33 Fake GuardianDecision Safety Gate Docs.

NO-GO:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2.33 Gate: Fake GuardianDecision Safety Gate Docs

`docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md` is now the standing gate for fake GuardianDecision-adjacent work.

No fake GuardianDecision-adjacent PR may merge without satisfying it.

Real GuardianDecision remains blocked.

## Phase 2.34 Gate: Fake GuardianDecision Safety Gate Readiness Review

Fake GuardianDecision safety-gate work may pause after Phase 2.34 if readiness decision approves.

After merge:

GO only for Phase 2.35 Phase Two Final Readiness Review.

NO-GO:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2.35 Gate: Phase Two Final Readiness Review

No Phase 3 work until Phase 2.35 final readiness review is merged.

After merge:

GO only for Phase 3.0 Non-production Kernel Pipeline Design Review.

NO-GO:

- production Sparkbot integration
- real IntentCompiler
- real GuardianDecision
- Guardian enforcement
- policy enforcement
- approval enforcement
- execution
- audit persistence
- real runtime behavior

## Phase 3.0 Gate: Non-production Kernel Pipeline Design Review

Phase 3 begins only as non-production kernel pipeline design.

After merge:

GO only for Phase 3.1 Non-production Kernel Pipeline Fixture Map.

NO-GO:

- production Sparkbot integration
- real IntentCompiler
- real GuardianDecision
- Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real runtime behavior

## Phase 3.1 Gate: Non-production Kernel Pipeline Fixture Map

Kernel pipeline fixture mapping is allowed as docs/tests only.

No runtime pipeline may be implemented.

After merge:

GO only for Phase 3.2 Non-production Kernel Pipeline Map Readiness Review.

NO-GO:

- runtime pipeline
- production Sparkbot integration
- real IntentCompiler
- natural-language inference
- real GuardianDecision
- Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- redaction runtime
- terminal/PTY
- Robo-OS physical action
- live auth/session/trust/autonomy enforcement

## Phase 3.2 Gate: Non-production Kernel Pipeline Map Readiness Review

No fixture relationship metadata until Phase 3.2 readiness review is merged.

After merge:

GO only for Phase 3.3 Non-production Kernel Pipeline Relationship Metadata.

NO-GO:

- runtime pipeline
- production Sparkbot integration
- real IntentCompiler
- real GuardianDecision
- enforcement
- approval
- execution
- audit persistence
- real runtime behavior

## Phase 3.3 Gate: Non-production Kernel Pipeline Relationship Metadata

Fixture relationship metadata is allowed as non-runtime metadata only.

Still blocked:

- runtime pipeline
- production Sparkbot integration
- real IntentCompiler
- real GuardianDecision
- enforcement
- approval
- execution
- audit persistence
- real runtime behavior

Status:

- complete
- tagged as `phase-3.3-nonproduction-kernel-pipeline-relationship-metadata`

After merge:

GO only for Phase 3.4 Non-production Kernel Pipeline Relationship Metadata Readiness Review.

## Phase 3.4 Gate: Non-production Kernel Pipeline Relationship Metadata Readiness Review

Phase 3.4 may review Phase 3.3 relationship metadata readiness as docs/tests/fixtures only.

GO only for:

- non-production readiness review documentation
- readiness review fixture
- readiness review tests

Still blocked:

- runtime pipeline
- executable pipeline
- test-only composition harness
- production Sparkbot integration
- real IntentCompiler
- real GuardianDecision
- enforcement
- approval
- execution
- audit persistence
- Sparkbot wiring
- robot control

Deferred:

- Phase 3.5 LIMA Product Family and Adaptive Trust Doctrine
- ARC Bot, custom business bot, and shell-family doctrine
- adaptive trust gates
- breakglass UX doctrine
- practical human-safety doctrine

Status:

- complete
- tagged as `phase-3.4-nonproduction-kernel-pipeline-relationship-metadata-readiness-review`

After merge:

GO only for Phase 3.5 LIMA Product Family and Adaptive Trust Doctrine.

## Phase 3.5 Gate: LIMA Product Family and Adaptive Trust Doctrine

Phase 3.5 may add non-runtime product-family, adaptive trust, breakglass evolution, and human-safety doctrine docs/tests/fixtures only.

GO only for:

- non-runtime product-family reference docs
- non-runtime adaptive trust doctrine reference
- non-runtime breakglass evolution doctrine
- non-runtime human-safety doctrine reference
- doctrine fixtures
- doctrine metadata tests

Still blocked:

- runtime behavior
- runtime trust gate engine
- adaptive trust enforcement
- production approvals
- real GuardianDecision
- real IntentCompiler
- Sparkbot import or wiring
- ARC Bot implementation
- custom business bot implementation
- bot generator
- robot control
- Robo-OS driver behavior
- physical-world action
- enforcement
- execution
- audit persistence

After merge:

- likely return to non-production pipeline report/map artifact work unless a readiness review says otherwise

Status:

- complete
- tagged as `phase-3.5-lima-product-family-adaptive-trust-doctrine`

## Phase 3.6 Gate: Non-production Kernel Pipeline Report Map Artifact

Phase 3.6 may add a static non-runtime report/map artifact for the current non-production kernel pipeline fixture path.

GO only for:

- report/map artifact documentation
- report/map artifact fixture
- report/map artifact tests
- project tracking doc updates

Still blocked:

- runtime behavior
- report generator
- executable pipeline
- test-only composition harness
- runtime composition
- production Sparkbot integration
- Sparkbot import or wiring
- real IntentCompiler
- real GuardianDecision
- ARC Bot implementation
- custom bot implementation
- robot control
- Robo-OS driver behavior
- adaptive trust enforcement
- approval
- enforcement
- execution
- audit persistence
- physical-world action

After merge:

- GO only for Phase 3.7 Pipeline Composition Safety Gate Docs

## Phase 3.7 Gate: Pipeline Composition Safety Gate Docs

Phase 3.7 may add standing non-runtime safety gate documentation, fixture metadata, and tests for future pipeline composition discussions.

GO only for:

- pipeline composition safety gate documentation
- safety gate fixture metadata
- safety gate tests
- project tracking doc updates

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness
- runtime composition
- production Sparkbot integration
- Sparkbot import or wiring
- real IntentCompiler
- real GuardianDecision
- model calls
- tool execution
- terminal or PTY execution
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 3.8 Pipeline Composition Safety Gate Readiness Review

## Phase 3.8 Gate: Pipeline Composition Safety Gate Readiness Review

Phase 3.8 may review the Phase 3.7 safety gate and decide whether Phase 3 can move to final readiness review.

GO only for:

- safety gate readiness review documentation
- readiness review fixture metadata
- readiness review tests
- project tracking doc updates

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness
- runtime composition
- production Sparkbot integration
- Sparkbot import or wiring
- real IntentCompiler
- real GuardianDecision
- model calls
- tool execution
- terminal or PTY execution
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 3 final readiness review

## Phase 3.9 Gate: Final Readiness Review

Phase 3.9 may review all Phase 3 non-production kernel pipeline safety work and decide whether Phase 4 planning may begin.

GO only for:

- final readiness review documentation
- final readiness fixture metadata
- final readiness tests
- project tracking doc updates

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness unless separately approved
- runtime composition
- production Sparkbot integration
- Sparkbot import or wiring
- real IntentCompiler
- real GuardianDecision
- model calls
- tool execution
- terminal or PTY execution
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 4.0 Runtime Extraction Readiness Planning

## Phase 4.0 Gate: Runtime Extraction Readiness Planning

Phase 4.0 may define the runtime-extraction readiness sequence after Phase 3.

GO only for:

- runtime extraction readiness planning documentation
- static planning fixture metadata
- planning tests
- project tracking doc updates

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness
- Sparkbot import or wiring
- production route imports
- model calls
- tool execution
- terminal or PTY execution
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 4.1 Sparkbot Runtime Reference Refresh

## Phase 4.1 Gate: Sparkbot Runtime Reference Refresh

Phase 4.1 may inspect Sparkbot as read-only reference/spec material before selecting a runtime boundary candidate.

GO only for:

- read-only Sparkbot reference inspection
- reference refresh documentation
- static reference fixture metadata
- static reference tests
- project tracking doc updates

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness
- Sparkbot import, wiring, route import, or code copy
- model calls
- tool execution
- terminal or PTY execution
- robotics command execution
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 4.2 Runtime Boundary Candidate Selection

## Phase 4.2 Gate: Runtime Boundary Candidate Selection

Phase 4.2 may select one runtime boundary candidate to carry into a safety gate. It does not approve extraction implementation.

GO only for:

- candidate selection documentation
- static candidate-selection fixture metadata
- static candidate-selection tests
- project tracking doc updates

Selected candidate:

- HumanInput intake boundary for chat and voice

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness
- Sparkbot import, wiring, route import, or code copy
- model calls
- tool execution
- terminal or PTY execution
- robotics command execution
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 4.3 Boundary Extraction Safety Gate

## Phase 4.3 Gate: Boundary Extraction Safety Gate

Phase 4.3 may define the safety gate for the selected HumanInput intake boundary. It does not approve extraction implementation.

GO only for:

- safety gate documentation
- static safety gate fixture metadata
- static safety gate tests
- project tracking doc updates

Selected candidate:

- HumanInput intake boundary for chat and voice

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness
- Sparkbot import, wiring, route import, or code copy
- production Sparkbot adapter implementation
- live auth/session/trust lookup
- natural-language parsing into action
- model calls
- tool execution
- terminal or PTY execution
- robotics command execution
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 4.4 Boundary Fixture Contract Extension if explicitly approved

## Phase 4.4 Gate: Boundary Fixture Contract Extension

Phase 4.4 may extend synthetic HumanInput intake fixture/contract metadata for the selected chat and voice boundary.

GO only for:

- fixture/contract extension documentation
- synthetic text input fixture shape
- synthetic voice transcript fixture shape
- static inertness and boundary tests
- project tracking doc updates

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness
- live adapter code
- Sparkbot import, wiring, route import, or code copy
- production Sparkbot adapter implementation
- live auth/session/trust lookup
- natural-language parsing into action
- model calls
- tool execution
- terminal or PTY behavior
- robotics behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 4.5 Boundary Readiness Review

## Phase 4.5 Gate: Boundary Readiness Review

Phase 4.5 may review whether the selected HumanInput intake boundary is ready for a future explicitly approved narrow non-production proposal.

GO only for:

- readiness review documentation
- static readiness fixture metadata
- static readiness tests
- project tracking doc updates

Still blocked:

- runtime behavior
- executable pipeline
- test-only composition harness
- live adapter code
- Sparkbot import, wiring, route import, or code copy
- production Sparkbot adapter implementation
- live auth/session/trust lookup
- natural-language parsing into action
- model calls
- tool execution
- terminal or PTY behavior
- robotics behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

After merge:

- GO only for Phase 4.6 Non-production HumanInput Adapter Proposal if explicitly approved

## Phase 4.6 Gate: Non-production HumanInput Adapter Proposal

Phase 4.6 may add proposal metadata describing how a future shell intake adapter could convert selected shell input context into the Phase 4.4 HumanInput fixture/contract shape.

GO only for:

- proposal documentation
- static proposal fixture metadata
- static proposal tests
- project tracking updates

NO-GO for:

- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

Required proof:

- fixture is valid JSON
- status is non-runtime proposal
- proposal is docs/tests/fixtures only
- Phase 4.4 HumanInput fixture contract remains synthetic, inert, and non-runtime
- Phase 4.5 readiness review remains non-runtime
- tests pass

After merge:

- STOP for explicit operator approval before any next narrow non-production phase

## Phase 4.10 Gate: Non-production Test-only HumanInput Adapter Harness Proposal

Phase 4.10 may propose a future test-only HumanInput adapter harness as docs/tests/fixtures only.

GO only for:

- proposal documentation
- static proposal fixture metadata
- static proposal tests
- project tracking updates

NO-GO for:

- files under `lima/`
- harness code
- live adapter code
- Sparkbot imports or wiring
- runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 4.11 Test-only HumanInput Adapter Harness Proposal Readiness Review

## Phase 4.11 Gate: Test-only HumanInput Adapter Harness Proposal Readiness Review

Phase 4.11 may review whether the Phase 4.10 proposal is clear and safe enough for future safety gate documentation.

GO only for:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- project tracking updates

NO-GO for:

- files under `lima/`
- harness code
- live adapter code
- Sparkbot imports or wiring
- runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 4.12 Test-only HumanInput Adapter Harness Safety Gate Docs

## Phase 4.12 Gate: Test-only HumanInput Adapter Harness Safety Gate Docs

Phase 4.12 may define safety gate docs for any future test-only HumanInput adapter harness.

GO only for:

- safety gate documentation
- static safety gate fixture metadata
- static safety gate tests
- project tracking updates

NO-GO for:

- files under `lima/`
- harness implementation
- live adapter implementation
- Sparkbot imports or wiring
- runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 4.13 Phase 4 HumanInput Boundary Readiness Review

## Phase 4.13 Gate: Phase 4 HumanInput Boundary Readiness Review

Phase 4.13 may review whether the full HumanInput boundary lane is ready for a future explicitly approved test-only harness implementation phase or further non-runtime review.

GO only for:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- project tracking updates

NO-GO for:

- files under `lima/`
- harness implementation
- live adapter implementation
- Sparkbot imports or wiring
- runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- STOP for the next explicitly approved phase

## Phase 4.14 Gate: Test-only HumanInput Adapter Harness Implementation

Phase 4.14 may implement a deterministic test-only HumanInput adapter harness under `tests/`.

GO only for:

- test-only helper code under `tests/` or `tests/support/`
- synthetic fixture loading
- deterministic fixture-to-HumanInput-shaped dictionary conversion
- schema and shape validation
- negative tests for live, runtime, production, Sparkbot, IntentEnvelope, GuardianDecision, approval, execution, audit, lookup, model, tool, terminal, robot, and physical-world indicators
- project tracking updates

NO-GO for:

- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 4.15 Test-only HumanInput Adapter Harness Implementation Readiness Review

## Phase 4.15 Gate: Test-only HumanInput Adapter Harness Implementation Readiness Review

Phase 4.15 may review whether the Phase 4.14 harness stayed constrained, deterministic, synthetic-only, and non-runtime.

GO only for:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- project tracking updates

NO-GO for:

- files under `lima/`
- new harness behavior unless fixing a safety bug under `tests/support/`
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 4.16 HumanInput Boundary Lane Closeout Review

## Phase 4.16 Gate: HumanInput Boundary Lane Closeout Review

Phase 4.16 may close out the HumanInput boundary lane and recommend the next explicitly approved lane.

GO only for:

- closeout review documentation
- static closeout fixture metadata
- static closeout tests
- project tracking updates

NO-GO for:

- files under `lima/`
- new harness behavior
- HumanInput to IntentEnvelope implementation
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- STOP for explicit operator approval before any next lane

## Phase 4.17 Gate: HumanInput to IntentEnvelope Boundary Planning

Phase 4.17 may open the HumanInput to IntentEnvelope boundary planning lane.

GO only for:

- planning documentation
- static planning fixture metadata
- static planning tests
- project tracking updates

NO-GO for:

- files under `lima/`
- schema implementation
- bridge code
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- natural-language inference
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 4.18 HumanInput to IntentEnvelope Boundary Schema / Contract Proposal

## Phase 4.18 Gate: HumanInput to IntentEnvelope Boundary Schema / Contract Proposal

Phase 4.18 may propose a static boundary schema/contract for future test-only HumanInput to IntentEnvelope work.

GO only for:

- schema/contract proposal documentation
- static schema proposal fixture metadata
- static schema proposal tests
- project tracking updates

NO-GO for:

- files under `lima/`
- bridge code
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- natural-language inference
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 4.19 HumanInput to IntentEnvelope Boundary Readiness Review

## Phase 4.19 Gate: HumanInput to IntentEnvelope Boundary Readiness Review

Phase 4.19 may review whether the Phase 4.18 schema/contract proposal is clear, safe, constrained, and explicitly non-runtime enough before a Phase 5 gate / implementation readiness closeout.

GO only for:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- project tracking updates

NO-GO for:

- files under `lima/`
- bridge code
- test-only bridge code
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- natural-language inference
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 4.20 Phase 5 Gate / Implementation Readiness Closeout

## Phase 4.20 Gate: Phase 5 Gate / Implementation Readiness Closeout

Phase 4.20 may close the HumanInput to IntentEnvelope non-runtime planning lane at a Phase 5 gate.

GO only for:

- Phase 5 gate / implementation readiness closeout documentation
- static closeout fixture metadata
- static closeout tests
- project tracking updates

NO-GO for:

- files under `lima/`
- bridge code
- test-only bridge code
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- natural-language inference
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- STOP at Phase 5 gate until the operator explicitly approves the next Phase 5 scope

Current status:

- complete
- tagged as `phase-4.20-phase-5-gate-implementation-readiness-closeout`
- Phase 5 gate reached

## Phase 5.0 Gate: Phase 5 Scope Charter / HumanInput IntentEnvelope Boundary Decision Record

Phase 5.0 may open Phase 5 as non-runtime planning only.

GO only for:

- Phase 5 scope charter documentation
- HumanInput to IntentEnvelope boundary decision record metadata
- static charter fixture metadata
- static charter tests
- project tracking updates

NO-GO for:

- files under `lima/`
- bridge code
- test-only bridge code
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- natural-language inference
- model calls
- tool execution
- shell execution
- browser execution
- network action
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 5.1 HumanInput to IntentEnvelope Contract Proposal

Current status:

- complete
- tagged as `phase-5.0-phase-5-scope-charter-humaninput-intentenvelope-boundary-decision-record`

## Phase 5.1 Gate: HumanInput to IntentEnvelope Contract Proposal

Phase 5.1 may propose the HumanInput to IntentEnvelope contract as static metadata only.

GO only for:

- contract proposal documentation
- static contract proposal fixture metadata
- static contract proposal tests
- project tracking updates

NO-GO for:

- files under `lima/`
- bridge code
- test-only bridge code
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- natural-language inference
- model calls
- tool execution
- shell execution
- browser execution
- network action
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 5.2 Test-only Bridge Harness Proposal

## Phase 5.2 Gate: Test-only Bridge Harness Proposal

Phase 5.2 may propose a future test-only HumanInput to IntentEnvelope bridge harness, but must not implement it.

GO only for:

- test-only bridge harness proposal documentation
- static proposal fixture metadata
- static proposal tests
- project tracking updates

NO-GO for:

- files under `lima/`
- bridge implementation
- test-only bridge code
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- natural-language inference
- model calls
- tool execution
- shell execution
- browser execution
- network action
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- GO only for Phase 5.3 Test-only Bridge Harness Readiness Review

Current status:

- complete
- tagged as `phase-5.1-humaninput-to-intentenvelope-contract-proposal`

## Phase 5.3 Gate: Test-only Bridge Harness Readiness Review

Phase 5.3 may review whether the Phase 5.2 proposal is clear and safe enough before an implementation gate.

GO only for:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- project tracking updates

NO-GO for:

- files under `lima/`
- bridge implementation
- test-only bridge code
- live adapter code
- Sparkbot imports or wiring
- production runtime behavior
- natural-language inference
- model calls
- tool execution
- shell execution
- browser execution
- network action
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

After merge:

- STOP at implementation gate until the operator explicitly approves any test-only bridge harness implementation scope

Current status:

- complete
- tagged as `phase-5.2-test-only-bridge-harness-proposal`

Implementation gate status:

- Phase 5.3 complete
- tagged as `phase-5.3-test-only-bridge-harness-readiness-review`
- STOP until the operator explicitly approves any Phase 5.4 test-only bridge harness implementation scope

## Phase 5.4 Gate: Test-only HumanInput to IntentEnvelope Bridge Harness Implementation

Phase 5.4 may implement a deterministic helper only under `tests/support/`.

GO:

- synthetic HumanInput-shaped test input
- non-executable IntentEnvelope-candidate-shaped test output
- conservative risk classification
- approval-required states for risky requests
- fail-closed behavior for missing, empty, runtime, production, or approved markers
- static docs, fixtures, and tests

NO-GO:

- files under `lima/`
- live adapter code
- runtime HumanInput to IntentEnvelope bridge
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

STOP until the operator explicitly approves any Phase 5.5 scope.

## Phase 5.5 Gate: Test-only Bridge Harness Readiness Review

Phase 5.5 may review the Phase 5.4 helper as docs/tests/fixtures only.

GO:

- readiness review documentation
- readiness fixture metadata
- static tests that inspect the Phase 5.4 helper boundary
- confirmation that helper classifier logic is not runtime classifier logic
- confirmation that Phase 5.6 or later remains gated

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

STOP until the operator explicitly approves any Phase 5.6 scope.

## Phase 5.6 Gate: HumanInput Runtime Bridge Safety Gate / Next-Scope Decision Record

Phase 5.6 may define a safety gate and next-scope decision record as docs/tests/fixtures only.

GO:

- safety gate documentation
- next-scope options
- decision record fixture metadata
- static tests that verify next runtime bridge work remains gated
- explicit statement that runtime bridge work must start with design before implementation

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

STOP until the operator explicitly approves any Phase 5.7 scope.

## Phase 5.7 Gate: HumanInput Runtime Bridge Design Proposal

Phase 5.7 may define a future runtime bridge design proposal as docs/tests/fixtures only.

GO:

- allowed and rejected input design
- provenance requirements
- non-executable candidate requirements
- approval-required semantics
- risk-tier semantics
- passive trust/autonomy rules
- blocked behavior list
- static tests that verify the design remains non-runtime

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 5.8 docs/tests/fixtures-only threat modeling under the approved design lane.

## Phase 5.8 Gate: HumanInput Runtime Bridge Threat Model

Phase 5.8 may threat-model a future runtime bridge as docs/tests/fixtures only.

GO:

- prompt injection risk
- operator impersonation risk
- trust bypass risk
- accidental execution risk
- shell/browser/network/file/robotics escalation risk
- audit gap risk
- approval confusion risk
- helper classifier misuse risk
- unsafe test-code reuse risk
- malformed, replayed, stale, and ambiguous input risks
- mitigations and residual-risk metadata

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 5.9 docs/tests/fixtures-only boundary validation matrix work under the approved design lane.

## Phase 5.9 Gate: HumanInput Runtime Bridge Boundary Validation Matrix

Phase 5.9 may define a boundary validation matrix as docs/tests/fixtures only.

GO:

- low-risk informational category
- shell command category
- browser/network category
- file mutation category
- robotics/physical-world category
- admin/trusted/Phil bypass category
- ambiguous request category
- empty request category
- malformed request category
- replayed/stale request category
- non-executable expected posture for every category
- approval-required or blocked posture for side-effect-bearing categories

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 5.10 docs/tests/fixtures-only implementation gate / closeout review under the approved design lane.

## Phase 5.10 Gate: Runtime Bridge Implementation Gate / Closeout Review

Phase 5.10 may close the HumanInput runtime bridge design lane as docs/tests/fixtures only.

GO:

- designed-artifacts summary
- unimplemented runtime pieces list
- future runtime implementation requirements
- explicit operator next-scope requirement
- live/runtime implementation blocked statement
- Phase 5.4 helper remains test-only statement

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

STOP until the operator explicitly approves the next scope.

## Phase 5.11 Gate: Phase 5 HumanInput Bridge Design Lane Audit Archive / Closeout

Phase 5.11 may archive the Phase 5 HumanInput bridge design lane as docs/tests/fixtures only.

GO:

- Phase 5.0 through Phase 5.10 completion summary
- added / not-added summary
- Phase 5.4 helper remains test-only statement
- Phase 5.7 through Phase 5.10 archived as design/specification only
- future runtime work requires explicit Phil approval
- recommended next options

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

STOP until the operator explicitly approves the next scope.

## Phase 6.0 Gate: Post-Phase-5 Roadmap Reorientation

Phase 6.0 may reorient the roadmap after Phase 5 as docs/tests/fixtures only.

GO:

- Phase 5 closeout review
- safest next architectural lane selection
- future lane separation
- runtime bridge prerequisite list
- kernel lifecycle planning recommendation

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 6.1 docs/tests/fixtures-only kernel lifecycle planning under the approved Phase 6 planning lane.

## Phase 6.1 Gate: LIMA Kernel Lifecycle Planning

Phase 6.1 may define the LIMA Kernel lifecycle as docs/tests/fixtures only.

GO:

- shell intake stage
- boundary normalization stage
- IntentEnvelope candidate formation stage
- Guardian review stage
- GuardianDecision record stage
- spine/audit/memory handoff stage
- driver/tool handoff blocked stage
- runtime bridge prerequisites

NO-GO:

- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live runtime bridge
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler behavior
- real GuardianDecision behavior
- approval enforcement
- execution
- audit persistence
- model, tool, shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 6.2 docs/tests/fixtures-only lifecycle boundary map work under the approved Phase 6 planning lane.

## Phase 6.2 Gate: IntentEnvelope and GuardianDecision Lifecycle Boundary Map

Phase 6.2 may map IntentEnvelope candidate and GuardianDecision lifecycle boundaries as docs/tests/fixtures only.

GO:

- document IntentEnvelope candidate lifecycle metadata
- document GuardianDecision future authority lifecycle metadata
- keep HumanInput as intent context only
- keep IntentEnvelope candidates non-executable
- keep approval state descriptive only
- keep audit/spine/memory references as lineage planning only
- keep driver/tool handoff blocked
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 6.3 docs/tests/fixtures-only approval, audit, and memory boundary planning under the approved Phase 6 planning lane.

## Phase 6.3 Gate: Approval / Audit / Memory Boundary Planning

Phase 6.3 may plan approval, audit/spine, and memory boundaries as docs/tests/fixtures only.

GO:

- document descriptive approval states
- document audit and spine lineage planning requirements
- document memory reference constraints
- keep GuardianDecision as future authority
- keep IntentEnvelope candidates non-executable
- keep HumanInput as intent context only
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- authorization
- execution
- audit persistence
- memory reads or writes
- spine ledger writes
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 6.4 docs/tests/fixtures-only roadmap gate / next-lane closeout under the approved Phase 6 planning lane.

## Phase 6.4 Gate: Phase 6 Roadmap Gate / Next-Lane Closeout

Phase 6.4 may close the current Phase 6 planning lane as docs/tests/fixtures only.

GO:

- summarize Phase 6.0 through Phase 6.3
- document planned kernel, candidate, GuardianDecision, approval, audit/spine, memory, Sparkbot, and Robo-OS boundaries
- document unimplemented runtime surfaces
- document next-scope options
- require explicit operator selection before any next phase
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- authorization
- execution
- audit persistence
- memory reads or writes
- spine ledger writes
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Stop for explicit operator next-scope selection unless a narrow docs/tests/fixtures-only audit archive closeout is explicitly approved. No Phase 7, runtime bridge, Sparkbot integration, Robo-OS integration, approval/enforcement/execution/audit, memory IO, or physical-world phase is approved by this closeout.

## Phase 6.5 Gate: Phase 6 Roadmap Planning Lane Audit Archive / Closeout

Phase 6.5 may archive Phase 6 as a completed planning lane as docs/tests/fixtures only.

GO:

- summarize Phase 6.0 through Phase 6.4 as complete
- list docs, fixtures, static tests, and roadmap/state updates as added
- list runtime behavior, `lima/` changes, `tests/support/` changes, Sparkbot wiring, live adapters, execution, approval enforcement, audit persistence, and physical-world action as not added
- confirm Phase 5 runtime bridge remains gated
- archive Phase 6 as roadmap/planning only
- document next options that require explicit Phil approval
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- authorization
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Stop for explicit operator next-scope selection. No Phase 7, Sparkbot integration planning, Robo-OS planning, product-roadmap planning, runtime implementation, approval/enforcement/execution/audit, memory IO, or physical-world phase is approved by this archive.

## Phase 7.0 Gate: Kernel Runtime Implementation Charter

Phase 7.0 may open a no-code kernel runtime implementation charter lane as docs/tests/fixtures only.

GO:

- define the smallest future runtime implementation slice that could be considered later
- keep the future slice non-executing and candidate-metadata-only
- require typed explicit input
- list preconditions before runtime code
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- model calls
- network calls
- file mutation
- shell, browser, robot, or physical-world side effects

After merge:

Continue only to Phase 7.1 docs/tests/fixtures-only first runtime slice eligibility mapping under the approved Phase 7 no-code charter lane.

## Phase 7.1 Gate: First Runtime Slice Eligibility Map

Phase 7.1 may map future eligible and forbidden runtime files as docs/tests/fixtures only.

GO:

- list future eligible existing files
- list future eligible new files only if a later charter approves them
- list forbidden runtime surfaces
- keep `tests/support/**` forbidden
- state that eligibility is not current approval
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- model calls
- network calls
- file mutation
- shell, browser, robot, or physical-world side effects

After merge:

Continue only to Phase 7.2 docs/tests/fixtures-only kernel runtime safety preconditions under the approved Phase 7 no-code charter lane.

## Phase 7.2 Gate: Kernel Runtime Safety Preconditions

Phase 7.2 may define future runtime safety preconditions as docs/tests/fixtures only.

GO:

- define required tests before runtime code
- define rollback expectations
- define audit proof requirements
- define allowed input/output shape
- define safety gates
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- model calls
- network calls
- file mutation
- shell, browser, robot, or physical-world side effects

After merge:

Continue only to Phase 7.3 docs/tests/fixtures-only runtime implementation test planning under the approved Phase 7 no-code charter lane.

## Phase 7.3 Gate: Runtime Implementation Test Plan

Phase 7.3 may define a future runtime implementation test plan as docs/tests/fixtures only.

GO:

- define future test families
- define required negative tests
- define limited positive tests
- define validation commands
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- model calls
- network calls
- file mutation
- shell, browser, robot, or physical-world side effects

After merge:

Continue only to Phase 7.4 docs/tests/fixtures-only implementation decision gate / closeout under the approved Phase 7 no-code charter lane.

## Phase 7.4 Gate: Phase 7 Implementation Decision Gate / Closeout

Phase 7.4 may close the no-code Phase 7 charter lane as docs/tests/fixtures only.

GO:

- summarize Phase 7.0 through Phase 7.3
- summarize Phase 7 decisions
- list what remains unimplemented
- document next decision options
- require explicit Phil approval before runtime code
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- runtime behavior
- helper behavior changes
- `tests/support/` changes
- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- model calls
- network calls
- file mutation
- shell, browser, robot, or physical-world side effects

After merge:

Stop for explicit operator implementation decision. No Phase 8, runtime implementation, `lima/` change, `tests/support/` change, Sparkbot integration, live adapter, approval enforcement, execution, audit persistence, or physical-world behavior is approved by this closeout.

After merge:

Continue only to Phase 7.5 docs/tests/fixtures-only no-code charter audit/archive closeout if explicitly approved by the operator.

## Phase 7.5 Gate: Phase 7 No-Code Kernel Runtime Charter Audit Archive / Closeout

Phase 7.5 may archive Phase 7 as a completed no-code charter lane as docs/tests/fixtures only.

GO:

- list Phase 7.0 through Phase 7.4 as complete
- summarize what was added
- summarize what was not added
- archive Phase 7 as no-code charter/planning only
- keep Phase 5 runtime bridge gated
- state future runtime code requires explicit Phil approval
- document recommended next options
- add static fixtures and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- runtime implementation
- live adapter code
- runtime HumanInput to IntentEnvelope bridge
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Stop for explicit operator next-scope selection. No Phase 8, runtime implementation, `lima/` change, `tests/support/` change, Sparkbot integration, live adapter, approval enforcement, execution, audit persistence, or physical-world behavior is approved by this archive.

## Phase 8.0 Gate: Implementation Design Review Charter

Phase 8.0 may open a no-code implementation design review lane as docs/tests/fixtures only.

GO:

- review Phase 7.0 through Phase 7.5 as source context
- define the design review mission
- identify the narrowest future runtime slice
- list required design package artifacts
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- runtime implementation
- live adapter code
- runtime HumanInput to IntentEnvelope bridge
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 8.1 docs/tests/fixtures-only exact runtime file-touch mapping under the approved Phase 8 no-code design review lane.

## Phase 8.1 Gate: Exact Runtime File-Touch Map

Phase 8.1 may map exact future runtime file touches as docs/tests/fixtures only.

GO:

- list future eligible existing files
- list future eligible new files
- list forbidden file surfaces
- state that eligibility is not current approval
- define future touch rules
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- runtime implementation
- live adapter code
- runtime HumanInput to IntentEnvelope bridge
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 8.2 docs/tests/fixtures-only runtime acceptance test design under the approved Phase 8 no-code design review lane.

## Phase 8.2 Gate: Runtime Acceptance Test Design

Phase 8.2 may define future runtime acceptance tests as docs/tests/fixtures only.

GO:

- list future required test families
- list required negative cases
- list limited positive cases
- list future validation commands
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- runtime implementation
- live adapter code
- runtime HumanInput to IntentEnvelope bridge
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 8.3 docs/tests/fixtures-only rollback / audit proof planning under the approved Phase 8 no-code design review lane.

## Phase 8.3 Gate: Rollback / Audit Proof Plan

Phase 8.3 may define rollback and audit proof requirements as docs/tests/fixtures only.

GO:

- list rollback requirements
- list audit proof requirements
- list future success criteria
- list future failure criteria
- keep audit proof as test evidence only
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- runtime implementation
- live adapter code
- runtime HumanInput to IntentEnvelope bridge
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 8.4 docs/tests/fixtures-only runtime implementation approval gate / closeout under the approved Phase 8 no-code design review lane.

## Phase 8.4 Gate: Runtime Implementation Approval Gate / Closeout

Phase 8.4 may close the no-code Phase 8 design review lane as docs/tests/fixtures only.

GO:

- list Phase 8.0 through Phase 8.3 as complete
- summarize the designed future runtime slice
- list the future eligible file scope
- list runtime implementation preconditions
- list still-out-of-scope surfaces
- define the exact future runtime implementation approval question for Phil
- keep Phase 5 runtime bridge gated
- add static fixtures and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- runtime implementation
- live adapter code
- runtime HumanInput to IntentEnvelope bridge
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Stop for explicit operator runtime implementation decision. No Phase 9, runtime implementation, `lima/` change, `tests/support/` change, Sparkbot integration, live adapter, approval enforcement, execution, audit persistence, or physical-world behavior is approved by this closeout.

After merge:

Continue only to Phase 8.5 docs/tests/fixtures-only no-code implementation design review audit/archive closeout if explicitly approved by the operator.

## Phase 8.5 Gate: Phase 8 No-Code Implementation Design Review Audit Archive / Closeout

Phase 8.5 may archive Phase 8 as a completed no-code implementation design review lane as docs/tests/fixtures only.

GO:

- list Phase 8.0 through Phase 8.4 as complete
- summarize what was added
- summarize what was not added
- archive Phase 8 as no-code design review only
- keep Phase 5 runtime bridge gated
- state future runtime code requires explicit Phil approval
- preserve the exact Phase 9 approval question
- document recommended next options
- add static fixtures and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- runtime implementation
- live adapter code
- runtime HumanInput to IntentEnvelope bridge
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Stop for explicit operator runtime implementation decision. No Phase 9, runtime implementation, `lima/` change, `tests/support/` change, Sparkbot integration, live adapter, approval enforcement, execution, audit persistence, or physical-world behavior is approved by this archive.

## Phase 9.0 Gate: Runtime Slice Preflight Audit / Eligible File Confirmation

Phase 9.0 may confirm the Phase 8.1 file-touch map as docs/tests/fixtures only.

GO:

- list exact eligible existing runtime files
- list exact eligible new runtime files
- confirm the file-touch map is explicit
- confirm Phase 9.1 acceptance test scaffolding is the next step
- add static fixtures and tests

NO-GO:

- files under `lima/`
- `tests/support/` changes
- runtime behavior
- Sparkbot imports or wiring
- live adapter code
- HumanInput runtime bridge behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 9.1 acceptance test scaffolding under the approved narrow Phase 9 lane.

## Phase 9.1 Gate: Runtime Slice Acceptance Test Scaffolding

Phase 9.1 may scaffold the Phase 9.2 acceptance obligations as docs/tests/fixtures only.

GO:

- list required Phase 9.2 acceptance cases
- list forbidden runtime interpretations
- preserve the Phase 8.1 eligible file-touch scope
- prove the scaffold itself adds no runtime behavior
- add static fixtures and tests

NO-GO:

- files under `lima/`
- `tests/support/` changes
- runtime behavior
- Sparkbot imports or wiring
- live adapter code
- HumanInput runtime bridge behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 9.2 non-executing kernel intake-to-candidate coordinator implementation inside the Phase 8.1 eligible file list.

## Phase 9.2 Gate: Non-executing Kernel Intake-to-Candidate Coordinator Implementation

Phase 9.2 may implement the approved narrow runtime slice inside the Phase 8.1 eligible file list.

GO:

- add `lima/kernel/__init__.py`
- add `lima/kernel/intake_candidate.py`
- accept only synthetic already-normalized intake metadata
- return non-executable candidate metadata
- preserve provenance
- fail closed for malformed, stale, replayed, raw, or unknown intake
- prove no side effects or forbidden imports
- add targeted tests, docs, and fixture

NO-GO:

- files outside the Phase 8.1 eligible runtime file list
- `tests/support/` changes
- Sparkbot imports or wiring
- live adapter code
- HumanInput runtime bridge behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 9.3 runtime slice readiness review.

## Phase 9.3 Gate: Runtime Slice Readiness Review

Phase 9.3 may review the Phase 9.2 runtime slice as docs/tests/fixtures only.

GO:

- review Phase 9.2 coordinator constraints
- verify non-executing candidate behavior remains intact
- document readiness only for Phase 9.4 closeout
- add static fixture and tests

NO-GO:

- runtime code changes
- files under `lima/`
- `tests/support/` changes
- Sparkbot imports or wiring
- live adapter code
- HumanInput runtime bridge behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Continue only to Phase 9.4 runtime slice audit/archive closeout.

## Phase 9.4 Gate: Phase 9 Runtime Slice Audit Archive / Closeout

Phase 9.4 may archive the Phase 9 runtime slice lane as docs/tests/fixtures only.

GO:

- list Phase 9.0 through Phase 9.3 as complete
- archive the Phase 9 runtime slice as non-executing candidate metadata only
- list the exact Phase 8.1 eligible runtime files touched
- document what was not added
- document next options requiring explicit Phil approval
- add static fixture and tests

NO-GO:

- runtime code changes
- files under `lima/`
- `tests/support/` changes
- Sparkbot imports or wiring
- live adapter code
- HumanInput runtime bridge behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Stop for explicit operator next-scope decision. No Phase 10 or runtime expansion is approved by this closeout.

## Phase 10.0 Gate: Post-Phase-9 Runtime Slice Review

Phase 10.0 may open the approved no-code Phase 10 design lane by reviewing the completed Phase 9 runtime slice and documenting proof/gap boundaries.

GO:

- review Phase 9.0 through Phase 9.5
- list exact Phase 9 runtime files touched
- document what the Phase 9 coordinator proved
- document what Phase 9 did not prove
- keep Phase 10.0 docs/tests/fixtures only
- keep Phase 11 runtime implementation unapproved
- add static fixture and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- helper behavior changes
- Sparkbot import or wiring
- live adapter
- HumanInput runtime bridge
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 10.1 no-code design options. No Phase 11 runtime implementation or runtime expansion is approved by this review.

## Phase 10.1 Gate: Next Runtime Slice Design Options

Phase 10.1 may evaluate the safest next runtime slice options without implementing runtime behavior.

GO:

- evaluate candidate validation
- evaluate candidate status normalization
- evaluate candidate lifecycle metadata
- evaluate intake error taxonomy
- evaluate provenance hardening
- preserve no-further-runtime-work as safe option
- recommend only a future approval candidate
- add static fixture and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- helper behavior changes
- Sparkbot import or wiring
- live adapter
- HumanInput runtime bridge
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 10.2 exact file-touch mapping. No Phase 11 runtime implementation or runtime expansion is approved by this design-options review.

## Phase 10.2 Gate: Exact File-Touch Map for Next Runtime Slice

Phase 10.2 may map the exact future file-touch surface for a possible Phase 11 candidate validation and status normalization slice.

GO:

- list future-eligible runtime files exactly
- define per-file future limits
- list forbidden runtime surfaces
- preserve Phase 5 runtime bridge gate
- add static fixture and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- helper behavior changes
- Sparkbot import or wiring
- live adapter
- HumanInput runtime bridge
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 10.3 acceptance-test and rollback planning. No Phase 11 runtime implementation or runtime expansion is approved by this file-touch map.

## Phase 10.3 Gate: Acceptance Test and Rollback Plan

Phase 10.3 may define future acceptance-test, rollback, and audit-proof requirements for the possible Phase 11 candidate validation and status normalization slice.

GO:

- define non-authoritative candidate acceptance tests
- define forbidden behavior acceptance tests
- define source-only rollback plan
- define audit-proof evidence
- preserve Phase 5 runtime bridge gate
- add static fixture and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- helper behavior changes
- Sparkbot import or wiring
- live adapter
- HumanInput runtime bridge
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 10.4 runtime expansion approval gate / closeout. No Phase 11 runtime implementation or runtime expansion is approved by this test and rollback plan.

## Phase 10.4 Gate: Runtime Expansion Approval Gate / Closeout

Phase 10.4 may close the Phase 10 no-code design lane and preserve the explicit Phase 11 approval question.

GO:

- list completed Phase 10.0 through Phase 10.3 scope
- list future Phase 11 eligible files exactly
- document what remains unimplemented
- preserve exact Phase 11 approval question
- require explicit Phil approval before Phase 11
- add static fixture and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- helper behavior changes
- Sparkbot import or wiring
- live adapter
- HumanInput runtime bridge
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Stop for explicit Phil decision. No Phase 11 runtime implementation or runtime expansion is approved by this closeout.

## Phase 10.5 Gate: Phase 10 Next Runtime Slice Design Lane Audit Archive / Closeout

Phase 10.5 may archive Phase 10.0 through Phase 10.4 as a completed no-code design lane before any Phase 11 runtime expansion decision.

GO:

- list Phase 10.0 through Phase 10.4 as complete
- document what Phase 10 added
- document what Phase 10 did not add
- confirm no `lima/` changes
- confirm no `tests/support/` changes
- confirm no `lima/kernel/candidate_status.py`
- preserve the exact Phase 11 approval question
- add static fixture and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- `lima/kernel/candidate_status.py`
- runtime behavior changes
- helper behavior changes
- Sparkbot import or wiring
- live adapter
- HumanInput runtime bridge
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Stop for explicit Phil decision. No Phase 11 runtime implementation or runtime expansion is approved by this archive.

## Phase 11.0 Gate: Runtime Slice Preflight Audit / Eligible File Confirmation

Phase 11.0 may confirm the exact Phase 10.2 eligible runtime file list before implementation phases begin.

GO:

- confirm eligible runtime files are explicit
- confirm no other runtime files are eligible
- confirm `lima/kernel/candidate_status.py` remains absent before implementation
- preserve Phase 5 runtime bridge gate
- add static fixture and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- helper behavior changes
- Sparkbot import or wiring
- live adapter
- HumanInput runtime bridge
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 11.1 acceptance test scaffolding. Candidate status and validation runtime implementation remains reserved for Phase 11.2 and Phase 11.3.

## Phase 11.1 Gate: Candidate Status Acceptance Test Scaffolding

Phase 11.1 may scaffold test obligations for candidate status normalization and candidate validation.

GO:

- list Phase 11.2 status normalization test families
- list Phase 11.3 validation test families
- list shared forbidden-behavior test families
- preserve Phase 5 runtime bridge gate
- add static fixture and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- helper behavior changes
- Sparkbot import or wiring
- live adapter
- HumanInput runtime bridge
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 11.2 candidate status normalization runtime implementation within the Phase 10.2 file map.

## Phase 11.2 Gate: Candidate Status Normalization Runtime Implementation

Phase 11.2 may implement candidate status normalization for existing non-executing intake candidates.

GO:

- create `lima/kernel/candidate_status.py`
- add safe side-effect-free exports to `lima/kernel/__init__.py`
- normalize candidate status to proposed, needs_review, or blocked only
- force execution and side-effect flags false
- prevent approved state from surviving normalization
- preserve provenance
- update obsolete pre-implementation absence tests to inspect phase fixtures
- add runtime tests and static boundary tests

NO-GO:

- runtime files outside the Phase 10.2 eligible list
- `tests/support/` changes
- HumanInput runtime bridge
- Sparkbot import or wiring
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 11.3 candidate validation runtime implementation within the Phase 10.2 file map.

## Phase 11.3 Gate: Candidate Validation Runtime Implementation

Phase 11.3 may implement fail-closed candidate validation for existing non-executing intake candidates.

GO:

- add validation behavior to `lima/kernel/candidate_status.py`
- add safe side-effect-free export to `lima/kernel/__init__.py`
- reject malformed candidates safely
- fail closed on missing safety fields
- fail closed on executable, execution_allowed, side_effects_allowed, approved, stale, or replayed candidates
- preserve Phase 5 runtime bridge gate
- add runtime tests and static boundary tests

NO-GO:

- runtime files outside the Phase 10.2 eligible list
- `tests/support/` changes
- HumanInput runtime bridge
- Sparkbot import or wiring
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 11.4 runtime slice readiness review.

## Phase 11.4 Gate: Runtime Slice Readiness Review

Phase 11.4 may review the Phase 11.2 and Phase 11.3 runtime slice before archive closeout.

GO:

- review candidate status normalization and candidate validation boundaries
- confirm the runtime files touched remain inside the Phase 10.2 file map
- confirm execution_allowed and side_effects_allowed remain false
- confirm approval_state never becomes approved
- confirm Phase 5 runtime bridge remains gated
- add readiness review docs, fixture, and static/behavioral tests

NO-GO:

- new `lima/` changes
- `tests/support/` changes
- runtime expansion
- HumanInput runtime bridge
- Sparkbot import or wiring
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 11.5 Phase 11 runtime slice audit archive / closeout.

## Phase 11.5 Gate: Phase 11 Runtime Slice Audit Archive / Closeout

Phase 11.5 may archive the completed Phase 11 narrow runtime slice and stop before Phase 12.

GO:

- list Phase 11.0 through Phase 11.4 as complete
- list only `lima/kernel/candidate_status.py` and `lima/kernel/__init__.py` as approved runtime files touched by Phase 11
- document that `lima/kernel/intake_candidate.py` remained eligible but untouched by Phase 11
- document what Phase 11 added and did not add
- preserve non-executing candidate safety guarantees
- prove Phase 12 remains gated
- add static fixture and tests

NO-GO:

- new `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- HumanInput runtime bridge
- Sparkbot import or wiring
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Stop for explicit Phil decision. No Phase 12 runtime expansion is approved by this archive.

## Phase 12.0 Gate: Post-Phase-11 Runtime Slice Review

Phase 12.0 may open a docs/tests/fixtures-only planning lane after Phase 11.

GO:

- review the Phase 11 candidate status runtime slice
- list Phase 12 next-direction options
- confirm Phase 5 runtime bridge remains gated
- add planning doc, fixture, and static tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot import or wiring
- HumanInput runtime bridge
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 12.1 next-direction options.

## Phase 12.1 Gate: Next Direction Options

Phase 12.1 may compare safe next-direction options after Phase 11.

GO:

- compare pause and preserve
- compare future narrow runtime slice design
- compare Sparkbot integration boundary planning
- compare Robo-OS / physical-world boundary planning
- compare threat-model and security-test strengthening
- recommend only the next planning/review phase

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot import or wiring
- HumanInput runtime bridge
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 12.2 threat-model and safety-gap review.

## Phase 12.2 Gate: Threat Model and Safety Gap Review

Phase 12.2 may review threat-model and safety gaps across the Phase 12 options.

GO:

- review candidate status approval confusion
- review HumanInput bridge pressure
- review Sparkbot wiring drift
- review Robo-OS driver and physical-world drift
- review operator/admin/Phil/trusted bypass risk
- review side-effect escalation and audit gaps
- recommend only a next-lane matrix

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot import or wiring
- HumanInput runtime bridge
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 12.3 next-lane recommendation matrix.

## Phase 12.3 Gate: Next Lane Recommendation Matrix

Phase 12.3 may produce a machine-checkable recommendation matrix for the next lane after Phase 12.

GO:

- compare pause and preserve
- compare future runtime slice design
- compare Sparkbot boundary planning
- compare Robo-OS / physical-world boundary planning
- compare threat-model-derived test planning
- recommend only a docs/tests/fixtures-only next lane

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot import or wiring
- HumanInput runtime bridge
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 12.4 Phase 12 decision gate / closeout.

## Phase 12.4 Gate: Phase 12 Decision Gate / Closeout

Phase 12.4 may close Phase 12 and preserve the next approval question.

GO:

- list Phase 12.0 through Phase 12.3 as complete
- preserve threat-model-derived test planning as the recommended next lane
- preserve the exact Phase 13 approval question
- prove Phase 13 remains gated
- add closeout docs, fixture, and tests

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot import or wiring
- HumanInput runtime bridge
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Stop for explicit Phil decision. No Phase 13 work is approved by this closeout.

## Phase 13.0 Gate: Threat-Derived Test Planning Charter

Phase 13.0 may open the approved docs/tests/fixtures-only threat-derived test planning lane.

GO:

- convert Phase 12.2 threats into Phase 13 planning outputs
- list static forbidden-pattern test requirements as a future phase
- list runtime contract test requirements as a future phase
- list threat fixture matrix as a future phase
- preserve future acceptance gate closeout

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot import or wiring
- HumanInput runtime bridge
- live adapter
- IntentCompiler or GuardianDecision runtime behavior
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 13.1 static forbidden-pattern test requirements.

## Phase 13.1 Gate: Static Forbidden-Pattern Test Requirements

Phase 13.1 may define future static forbidden-pattern test requirements.

GO:

- list forbidden imports
- list forbidden calls
- list forbidden boundary names
- list forbidden behavior claims
- state static checks are necessary but not sufficient

NO-GO:

- scanner implementation
- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot import or wiring
- HumanInput runtime bridge
- live adapter
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Continue only to Phase 13.2 runtime contract test requirements.

## Phase 13.2 Gate: Runtime Contract Test Requirements

Phase 13.2 may define future runtime contract test requirements.

GO:

- list non-executing candidate invariants
- list malformed/unknown/stale/replayed safety requirements
- list operator/admin/Phil/trusted bypass resistance requirements
- preserve Phase 5 runtime bridge gate

NO-GO:

- contract-test implementation
- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- approval, enforcement, execution, dispatch, or audit persistence

After merge:

Continue only to Phase 13.3 threat fixture matrix.

## Phase 13.3 Gate: Threat Fixture Matrix

Phase 13.3 may define future synthetic threat fixture families.

GO:

- list malformed, unknown, stale/replayed, approval-bypass, side-effect, Sparkbot, and HumanInput bridge fixture families
- require fixtures to remain synthetic, inert, non-executing, and test-only

NO-GO:

- production runtime fixtures
- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot wiring
- HumanInput runtime bridge
- physical-world behavior

After merge:

Continue only to Phase 13.4 future acceptance gate / closeout.

## Phase 13.4 Gate: Future Acceptance Gate / Closeout

Phase 13.4 may close Phase 13 and preserve the Phase 14 approval question.

GO:

- list Phase 13.0 through Phase 13.3 as complete
- preserve future acceptance gate requirements
- recommend Phase 14 as acceptance-gate test design only
- preserve the exact Phase 14 approval question

NO-GO:

- `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot import or wiring
- HumanInput runtime bridge
- live adapter
- approval, enforcement, execution, dispatch, or audit persistence
- shell, browser, network, file mutation, robotics, or physical-world side effects

After merge:

Stop for explicit Phil decision. No Phase 14 work is approved by this closeout.

## Phase 14.0 Gate: Acceptance-Gate Test Design Charter

Phase 14.0 may open the approved docs/tests/fixtures-only acceptance-gate test design lane.

Allowed:

- convert Phase 13 static, contract, and fixture requirements into Phase 14 design outputs
- list future acceptance-gate test families
- keep Phase 5 runtime bridge gated

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 14.1 static forbidden-pattern test design.

## Phase 14.1 Gate: Static Forbidden-Pattern Test Design

Phase 14.1 may design concrete future static tests for forbidden imports, calls, side-effect patterns, boundary names, and authority claims.

Allowed:

- docs/tests/fixtures-only static test design
- future test names and expected assertions
- forbidden import/call/name/claim categories

Blocked:

- scanner implementation
- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- execution, dispatch, persistence, or physical-world behavior

Continue only to Phase 14.2 runtime contract test design.

## Phase 14.2 Gate: Runtime Contract Test Design

Phase 14.2 may design concrete future runtime contract tests for non-executing candidate invariants.

Allowed:

- docs/tests/fixtures-only contract test design
- future test names for execution flags, approval state, provenance, malformed/unknown/stale/replayed safety, and operator-bypass resistance
- Phase 5 runtime bridge gating requirements

Blocked:

- contract-test implementation
- runtime implementation
- `lima/` changes
- `tests/support/` changes
- candidate status or intake candidate expansion
- execution, dispatch, persistence, or physical-world behavior

Continue only to Phase 14.3 threat fixture acceptance test design.

## Phase 14.3 Gate: Threat Fixture Acceptance Test Design

Phase 14.3 may design concrete future fixture-based acceptance tests for Phase 13.3 threat families.

Allowed:

- docs/tests/fixtures-only fixture acceptance test design
- future fixture families for malformed, unknown, stale/replayed, approval-bypass, shell/network/browser/file/robotics, Sparkbot, and HumanInput bridge attempts
- synthetic, inert, non-runtime fixture requirements

Blocked:

- fixture-execution implementation
- live shell commands for execution
- live network targets
- private operational data or credentials
- `lima/` changes
- `tests/support/` changes
- execution, dispatch, persistence, or physical-world behavior

Continue only to Phase 14.4 future runtime acceptance gate / closeout.

## Phase 14.4 Gate: Future Runtime Acceptance Gate / Closeout

Phase 14.4 may close Phase 14 and preserve the Phase 15 approval question.

Allowed:

- list Phase 14.0 through Phase 14.3 as complete
- preserve future acceptance-gate requirements
- recommend Phase 15 as docs/tests/fixtures-only acceptance-gate implementation proposal or readiness only
- preserve the exact Phase 15 approval question

Blocked:

- acceptance-gate test implementation
- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Stop for explicit Phil decision. No Phase 15 work is approved by this closeout.

## Phase 15.0 Gate: Acceptance-Gate Implementation Proposal Charter

Phase 15.0 may open the approved docs/tests/fixtures-only acceptance-gate implementation proposal/readiness lane.

Allowed:

- review Phase 14.0 through Phase 14.4
- define proposal/readiness outputs for a future test-only implementation package
- list future test groups and fixture requirement categories

Blocked:

- actual future acceptance-test implementation
- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, dispatch, persistence, or physical-world behavior

Continue only to Phase 15.1 future static test implementation plan.

## Phase 15.1 Gate: Future Static Test Implementation Plan

Phase 15.1 may propose future static forbidden-pattern test files, names, assertions, and scanner constraints.

Allowed:

- docs/tests/fixtures-only proposal metadata
- future static test file and test names
- scanner constraints for a later explicitly approved implementation

Blocked:

- static test implementation
- scanner utilities
- runtime imports or execution
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- execution, dispatch, persistence, or physical-world behavior

Continue only to Phase 15.2 future runtime contract test implementation plan.

## Phase 15.2 Gate: Future Runtime Contract Test Implementation Plan

Phase 15.2 may propose future runtime contract acceptance-test files, names, and assertions.

Allowed:

- docs/tests/fixtures-only proposal metadata
- future runtime contract test file and test names
- future assertions for candidate invariants and fail-closed behavior

Blocked:

- runtime contract acceptance-test implementation
- runtime behavior changes
- candidate module mutation
- `lima/` changes
- `tests/support/` changes
- execution, dispatch, persistence, or physical-world behavior

Continue only to Phase 15.3 future threat fixture test implementation plan.

## Phase 15.3 Gate: Future Threat Fixture Test Implementation Plan

Phase 15.3 may propose future threat fixture test files, fixture names, and fixture content requirements.

Allowed:

- docs/tests/fixtures-only proposal metadata
- future threat fixture test file and test names
- future synthetic fixture names and content requirements

Blocked:

- future threat fixture test implementation
- future threat fixture creation
- live shell commands, live network targets, credentials, private hostnames, deploy configs, real file mutation targets, robot instructions, approval tokens, or audit records
- `lima/` changes
- `tests/support/` changes
- execution, dispatch, persistence, or physical-world behavior

Continue only to Phase 15.4 test-only implementation readiness gate / closeout.

## Phase 15.4 Gate: Test-Only Implementation Readiness Gate / Closeout

Phase 15.4 may close Phase 15 and preserve the Phase 16 approval question.

Allowed:

- list Phase 15.0 through Phase 15.3 as complete
- state whether Phase 14 designed tests are ready for later explicitly approved test-only implementation
- preserve future Phase 16 candidate scope
- preserve the exact Phase 16 approval question

Blocked:

- actual future acceptance-test implementation
- future acceptance fixture creation
- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Stop for explicit Phil decision. No Phase 16 work is approved by this closeout.

## Phase 16.0 Gate: Test-Only Acceptance Implementation Charter

Phase 16.0 may open the explicitly approved test-only acceptance-gate implementation lane.

Allowed:

- docs/tests/fixtures only
- define Phase 16 as test-only acceptance implementation
- preserve static, contract, and fixture acceptance categories
- preserve no-runtime and no-`lima/` boundaries

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 16.1 static forbidden-pattern acceptance tests.

## Phase 16.1 Gate: Static Forbidden-Pattern Acceptance Tests

Phase 16.1 may implement static forbidden-pattern acceptance tests against explicit existing non-executing kernel candidate files.

Allowed:

- test-only static checks under `tests/`
- synthetic fixture metadata
- phase documentation
- checks for forbidden imports, forbidden calls, side-effect patterns, boundary names, and authority claims

Blocked:

- scanner helper implementation outside the phase test
- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 16.2 runtime contract acceptance tests.

## Phase 16.2 Gate: Runtime Contract Acceptance Tests

Phase 16.2 may implement test-only contract acceptance tests against existing non-executing candidate APIs.

Allowed:

- acceptance tests under `tests/`
- synthetic fixture metadata
- assertions that execution and side-effect flags remain false
- assertions that approval state never becomes approved
- assertions that provenance is preserved
- fail-closed malformed, unknown, stale/replayed, and approval-bypass cases

Blocked:

- runtime code changes
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 16.3 threat fixture acceptance tests.

## Phase 16.3 Gate: Threat Fixture Acceptance Tests

Phase 16.3 may implement synthetic threat fixture acceptance tests.

Allowed:

- synthetic inert fixture cases under `tests/fixtures/runtime_extraction/`
- acceptance tests under `tests/`
- malformed, unknown, stale/replayed, approval-bypass, shell/network/browser/file/robotics, Sparkbot, and HumanInput bridge attempt coverage

Blocked:

- live commands
- live network targets
- credentials, private hostnames, deploy configs, or private operational data
- real file mutation targets
- robot instructions
- approval tokens or audit records
- runtime implementation
- `lima/` changes
- `tests/support/` changes
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 16.4 readiness review.

## Phase 16.4 Gate: Test-Only Acceptance Implementation Readiness Review

Phase 16.4 may review the Phase 16.1 through Phase 16.3 test-only acceptance implementation before archive/closeout.

Allowed:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 16.5 archive / closeout.

## Phase 16.5 Gate: Phase 16 Test-Only Acceptance Archive / Closeout

Phase 16.5 may archive Phase 16 as a completed test-only acceptance-gate implementation lane.

Allowed:

- list Phase 16.0 through Phase 16.4 as complete
- document what Phase 16 added
- document what Phase 16 did not add
- preserve the Phase 17 decision gate
- preserve the exact Phase 17 approval question

Blocked:

- new `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Stop for explicit Phil decision. No Phase 17 work is approved by this closeout.

## Phase 17.0 Gate: Phase 16 Acceptance Test Audit Charter

Phase 17.0 may open the approved docs/tests/fixtures-only acceptance-gate audit/archive lane.

Allowed:

- audit charter documentation
- static audit charter fixture metadata
- static audit charter tests
- project tracking updates
- Phase 18 option list for later evaluation

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 17.1 acceptance test coverage review.

## Phase 17.1 Gate: Acceptance Test Coverage Review

Phase 17.1 may review the Phase 16 acceptance-test coverage.

Allowed:

- coverage review documentation
- static coverage review fixture metadata
- static coverage review tests
- mapping Phase 16 static, contract, and threat fixture tests to covered gates
- listing static/test-only limitations

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 17.2 remaining safety gap review.

## Phase 17.2 Gate: Remaining Safety Gap Review

Phase 17.2 may review remaining safety gaps before any next-lane decision.

Allowed:

- remaining gap review documentation
- static remaining gap fixture metadata
- static remaining gap tests
- list runtime expansion blockers
- preserve Phase 5 HumanInput runtime bridge gating

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 17.3 next-lane decision matrix.

## Phase 17.3 Gate: Next-Lane Decision Matrix

Phase 17.3 may compare Phase 18 options and recommend the safest next lane.

Allowed:

- decision matrix documentation
- static decision matrix fixture metadata
- static decision matrix tests
- compare no-code runtime design, test-only regression hardening, Sparkbot boundary planning, Robo-OS boundary planning, and pause options
- preserve explicit Phase 18 approval requirement

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 17.4 archive / closeout.

## Phase 17.4 Gate: Phase 17 Acceptance-Gate Audit Archive / Closeout

Phase 17.4 may archive Phase 17 and preserve the Phase 18 approval question.

Allowed:

- list Phase 17.0 through Phase 17.3 as complete
- archive Phase 16 acceptance tests as complete and test-only
- preserve recommended Phase 18 direction
- preserve exact Phase 18 approval question

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Stop for explicit Phil decision. No Phase 18 work is approved by this closeout.

## Phase 18.0 Gate: Regression Hardening Charter

Phase 18.0 may open the approved test-only regression hardening lane.

Allowed:

- regression hardening charter documentation
- static charter fixture metadata
- static charter tests
- tests/docs/fixtures-only scope definition

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 18.1 candidate API regression tests.

## Phase 18.1 Gate: Candidate API Regression Tests

Phase 18.1 may add regression tests for existing non-executing candidate APIs.

Allowed:

- test-only regression tests under `tests/`
- synthetic fixture metadata
- phase documentation
- imports of existing candidate APIs for tests only

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 18.2 acceptance boundary regression fixtures.

## Phase 18.2 Gate: Acceptance Boundary Regression Fixtures

Phase 18.2 may add synthetic acceptance-boundary regression fixtures and fixture tests.

Allowed:

- synthetic inert fixture cases under `tests/fixtures/runtime_extraction/`
- fixture tests under `tests/`
- phase documentation
- existing non-executing API exercise from tests only

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 18.3 forbidden integration regression tests.

## Phase 18.3 Gate: Forbidden Integration Regression Tests

Phase 18.3 may add test-only static regression checks for forbidden integrations.

Allowed:

- static regression checks under `tests/`
- synthetic fixture metadata
- phase documentation
- candidate runtime file scanning from tests only

Blocked:

- runtime scanner or runtime enforcement
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 18.4 regression hardening readiness review.

## Phase 18.4 Gate: Regression Hardening Readiness Review

Phase 18.4 may review the regression hardening package before archive.

Allowed:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- list ready-for and not-ready-for states

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 18.5 archive / closeout.

## Phase 18.5 Gate: Phase 18 Regression Hardening Archive / Closeout

Phase 18.5 may archive Phase 18 and preserve the Phase 19 approval question.

Allowed:

- list Phase 18.0 through Phase 18.4 as complete
- document what Phase 18 added
- document what Phase 18 did not add
- preserve recommended Phase 19 direction
- preserve exact Phase 19 approval question

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Stop for explicit Phil decision. No Phase 19 work is approved by this closeout.

## Phase 19.0 Gate: Phase 18 Regression Hardening Audit Charter

Phase 19.0 may open the approved docs/tests/fixtures-only acceptance-gate audit/archive lane.

Allowed:

- audit charter documentation
- static audit charter fixture metadata
- static audit charter tests
- project tracking updates
- Phase 20 option list for later evaluation

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Continue only to Phase 19.1 regression coverage review.

## Phase 19.1 Gate: Regression Coverage Review

Phase 19.1 may review Phase 18 regression coverage without changing runtime code.

Allowed:

- coverage review documentation
- static coverage review fixture metadata
- static coverage review tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Coverage reviewed:

- candidate API regression tests
- acceptance-boundary fixtures
- forbidden integration regression tests
- readiness and archive checks

Result:

Phase 18 coverage is meaningful as test-only regression protection. It does not create runtime enforcement or approve runtime expansion.

Continue only to Phase 19.2 remaining regression gap review.

## Phase 19.2 Gate: Remaining Regression Gap Review

Phase 19.2 may document remaining regression gaps without changing runtime code.

Allowed:

- gap review documentation
- static gap review fixture metadata
- static gap review tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Remaining gaps are static/test-only limitations. The regression suite does not create runtime monitoring, runtime enforcement, live adapter coverage, Sparkbot integration coverage, HumanInput runtime bridge behavior, or physical-world coverage.

Continue only to Phase 19.3 next-lane decision matrix.

## Phase 19.3 Gate: Next-Lane Decision Matrix

Phase 19.3 may compare Phase 20 options and recommend a lane without approving implementation.

Allowed:

- next-lane decision documentation
- static decision-matrix fixture metadata
- static decision-matrix tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Recommended direction:

Phase 20 should be a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice, if Phil explicitly approves it.

Continue only to Phase 19.4 archive closeout.

## Phase 19.4 Gate: Phase 19 Regression Audit Archive / Closeout

Phase 19.4 may archive Phase 19 and preserve the Phase 20 approval question.

Allowed:

- archive closeout documentation
- static archive fixture metadata
- static archive tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 19 is archived as completed docs/tests/fixtures-only regression audit work. Phase 20 is recommended as a no-code design lane for the next narrow runtime slice, but Phase 20 remains unapproved.

Stop for explicit Phil decision before Phase 20.

## Phase 20.0 Gate: Post-Regression Runtime Slice Design Charter

Phase 20.0 may open the approved docs/tests/fixtures-only no-code design lane for the next narrow runtime slice.

Allowed:

- design charter documentation
- static design charter fixture metadata
- static design charter tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 20 opens with candidate slice options but does not choose or implement a runtime slice yet.

Continue only to Phase 20.1 next runtime slice options review.

## Phase 20.1 Gate: Next Runtime Slice Options Review

Phase 20.1 may compare candidate slice options and recommend one future slice without implementing it.

Allowed:

- options review documentation
- static options review fixture metadata
- static options review tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Candidate provenance hardening is the recommended future slice because provenance is already required, non-executing, and audit-relevant.

Continue only to Phase 20.2 exact file-touch map for candidate slice.

## Phase 20.2 Gate: Exact File-Touch Map For Candidate Slice

Phase 20.2 may define the exact future file-touch map for the selected candidate provenance hardening slice.

Allowed:

- file-touch map documentation
- static file-touch map fixture metadata
- static file-touch map tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Future Phase 21 eligibility is limited to `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`. `lima/kernel/__init__.py`, new runtime modules, all other `lima/` files, and `tests/support/` are forbidden unless a later explicit approval changes scope.

Continue only to Phase 20.3 acceptance test and rollback plan.

## Phase 20.3 Gate: Acceptance Test And Rollback Plan

Phase 20.3 may define future acceptance tests and rollback/audit proof for the selected candidate provenance hardening slice.

Allowed:

- acceptance/rollback plan documentation
- static acceptance/rollback fixture metadata
- static acceptance/rollback tests
- project tracking updates

Blocked:

- runtime implementation
- actual future acceptance-test implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Future Phase 21 must prove provenance validation/normalization, non-executing invariants, no approval bypass, no side effects, no forbidden integrations, exact runtime file scope, full validation, and clean rollback.

Continue only to Phase 20.4 runtime slice approval gate / closeout.

## Phase 20.4 Gate: Phase 20 Runtime Slice Approval Gate / Closeout

Phase 20.4 may archive Phase 20 and preserve the Phase 21 approval question.

Allowed:

- approval gate closeout documentation
- static approval gate fixture metadata
- static approval gate tests
- project tracking updates

Blocked:

- runtime implementation
- actual future acceptance-test implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 20 is archived as no-code design only. Phase 21 remains unapproved and must not begin without explicit Phil approval.

Stop for explicit Phil decision before Phase 21.

## Phase 21.0 Gate: Runtime Slice Preflight Audit / Eligible File Confirmation

Phase 21.0 may confirm the approved candidate provenance hardening file scope before implementation.

Allowed:

- preflight audit documentation
- static preflight fixture metadata
- static preflight tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/kernel/__init__.py` changes
- new runtime modules
- any `lima/` file outside `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 20.2 is unambiguous. Future Phase 21 runtime work is limited to `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`.

Continue only to Phase 21.1 candidate provenance acceptance test scaffolding.

## Phase 21.1 Gate: Candidate Provenance Acceptance Test Scaffolding

Phase 21.1 scaffolds deterministic acceptance coverage before candidate provenance hardening runtime changes.

Allowed:

- acceptance test scaffolding under `tests/`
- synthetic Phase 21.1 fixtures under `tests/fixtures/runtime_extraction/`
- phase documentation and project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 21.1 proves the existing non-executing candidate APIs preserve valid provenance and fail closed for missing, empty, non-mapping, suspicious, stale, or replayed provenance cases.

Continue only to Phase 21.2 candidate provenance hardening runtime implementation inside `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`.

## Phase 21.2 Gate: Candidate Provenance Hardening Runtime Implementation

Phase 21.2 implements candidate provenance hardening inside the approved runtime files only.

Allowed:

- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`
- acceptance tests, synthetic fixtures, phase documentation, and project tracking updates

Blocked:

- `lima/kernel/__init__.py`
- new runtime modules
- all other `lima/` files
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Candidate construction rejects malformed provenance keys and missing provenance values. Candidate status normalization and validation block malformed or suspicious provenance while preserving valid provenance and all non-executing guarantees.

Continue only to Phase 21.3 candidate provenance regression review.

## Phase 21.3 Gate: Candidate Provenance Regression Review

Phase 21.3 reviews the Phase 21.2 runtime slice without runtime changes.

Allowed:

- regression review documentation
- static regression fixture metadata
- regression tests under `tests/`
- project tracking updates

Blocked:

- runtime changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 21.3 confirms valid provenance remains preserved, malformed provenance fails closed, suspicious provenance is blocked or invalid, and non-executing invariants remain enforced.

Continue only to Phase 21.4 runtime slice readiness review.

## Phase 21.4 Gate: Runtime Slice Readiness Review

Phase 21.4 confirms Phase 21 is ready for archive closeout without runtime expansion.

Allowed:

- readiness review documentation
- static readiness fixture metadata
- readiness tests under `tests/`
- project tracking updates

Blocked:

- runtime changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 21.0 through Phase 21.3 are complete, the runtime slice remains non-executing and provenance-hardened, and Phase 22 remains gated.

Continue only to Phase 21.5 archive closeout.

## Phase 21.5 Gate: Phase 21 Runtime Slice Audit Archive / Closeout

Phase 21.5 archives Phase 21 as a completed narrow runtime slice.

Allowed:

- archive closeout documentation
- static archive fixture metadata
- archive tests under `tests/`
- project tracking updates

Blocked:

- runtime changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 21 is archived as complete. The only runtime files touched by the lane were `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`. Phase 22 remains gated and requires explicit Phil approval.

Stop before Phase 22.

## Phase 22.0 Gate: Post-Phase-21 Runtime Slice Audit Charter

Phase 22.0 opens a no-code decision lane after auditing Phase 21.

Allowed:

- audit charter documentation
- static audit fixture metadata
- static audit tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 21 audit passes with the approved narrow-runtime-slice scope. Phase 22 may compare next-lane options without implementation.

Continue only to Phase 22.1 candidate provenance coverage review.

## Phase 22.1 Gate: Candidate Provenance Coverage Review

Phase 22.1 reviews existing provenance coverage and identifies test-only gaps.

Allowed:

- coverage review documentation
- static coverage fixture metadata
- static coverage tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Coverage is strong for existing candidate APIs, with remaining gaps best suited to test-only hardening rather than runtime expansion.

Continue only to Phase 22.2 remaining safety gap review.

## Phase 22.2 Gate: Remaining Safety Gap Review

Phase 22.2 classifies the remaining gaps after Phase 21.

Allowed:

- safety gap documentation
- static safety gap fixture metadata
- static safety gap tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Remaining gaps are test/planning gaps. Test-only hardening is the safest response before any future runtime expansion.

Continue only to Phase 22.3 next-lane decision matrix.

## Phase 22.3 Gate: Next-Lane Decision Matrix

Phase 22.3 recommends exactly one Phase 23 direction.

Allowed:

- decision matrix documentation
- static decision fixture metadata
- static decision tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 23 should be a test-only hardening lane for provenance and candidate invariants. Runtime expansion and integration planning are deferred.

Continue only to Phase 22.4 decision gate closeout.

## Phase 22.4 Gate: Phase 22 Decision Gate / Closeout

Phase 22.4 closes the Phase 22 decision lane.

Allowed:

- closeout documentation
- static closeout fixture metadata
- static closeout tests
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 22 is complete. Phase 23 should be test-only hardening for provenance and candidate invariants, but it remains gated and requires explicit Phil approval.

Stop before Phase 23.

## Phase 23.0 Gate: Provenance Invariant Test Hardening Charter

Phase 23.0 opens the approved test-only hardening lane.

Allowed:

- Phase 23 tests
- synthetic Phase 23 fixtures
- Phase 23 documentation
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 23 is constrained to deterministic offline tests and fixtures around existing candidate provenance and invariant behavior.

Continue only to Phase 23.1 candidate provenance regression tests.

## Phase 23.1 Gate: Candidate Provenance Regression Tests

Phase 23.1 adds deterministic regression tests for existing candidate provenance APIs.

Allowed:

- Phase 23.1 tests
- Phase 23.1 fixture metadata
- Phase 23.1 documentation
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Valid provenance is preserved, missing or malformed provenance fails closed, and stale or replayed candidates remain blocked or invalid.

Continue only to Phase 23.2 suspicious provenance fixture hardening.

## Phase 23.2 Gate: Suspicious Provenance Fixture Hardening

Phase 23.2 adds synthetic suspicious provenance fixtures and tests.

Allowed:

- Phase 23.2 tests
- Phase 23.2 synthetic fixtures
- Phase 23.2 documentation
- project tracking updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Suspicious provenance authority claims in values, keys, nested mappings, and lists fail closed, while risky action metadata remains non-executing.

Continue only to Phase 23.3 bypass-wording provenance tests.

## Phase 23.3 Gate: Bypass-Wording Provenance Tests

Phase 23.3 adds deterministic bypass-wording tests for provenance and risky request metadata.

Allowed:

- Phase 23.3 tests
- Phase 23.3 synthetic fixtures
- Phase 23.3 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 23.4 provenance hardening readiness review.

## Phase 23.4 Gate: Provenance Hardening Readiness Review

Phase 23.4 reviews Phase 23.0 through Phase 23.3 as ready for archive/closeout.

Allowed:

- Phase 23.4 tests
- Phase 23.4 fixture metadata
- Phase 23.4 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 23.5 archive/closeout.

## Phase 23.5 Gate: Phase 23 Test-Only Hardening Archive / Closeout

Phase 23.5 archives Phase 23 as a completed test-only hardening lane.

Allowed:

- Phase 23.5 tests
- Phase 23.5 fixture metadata
- Phase 23.5 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 23.5. Phase 24 requires explicit approval.

## Phase 24.0 Gate: Phase 23 Hardening Audit Charter

Phase 24.0 opens the approved docs/tests/fixtures-only audit/archive and next-lane decision phase for the Phase 23 package.

Allowed:

- Phase 24.0 tests
- Phase 24.0 fixture metadata
- Phase 24.0 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 24.1 provenance hardening coverage review.

## Phase 24.1 Gate: Provenance Hardening Coverage Review

Phase 24.1 reviews the Phase 23 provenance and candidate-invariant coverage.

Allowed:

- Phase 24.1 tests
- Phase 24.1 fixture metadata
- Phase 24.1 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 24.2 remaining candidate invariant gap review.

## Phase 24.2 Gate: Remaining Candidate Invariant Gap Review

Phase 24.2 identifies remaining provenance and candidate-invariant gaps as planning inputs only.

Allowed:

- Phase 24.2 tests
- Phase 24.2 fixture metadata
- Phase 24.2 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 24.3 next-lane decision matrix.

## Phase 24.3 Gate: Next-Lane Decision Matrix

Phase 24.3 recommends Phase 25 as additional test-only hardening for a cross-API candidate invariant matrix.

Allowed:

- Phase 24.3 tests
- Phase 24.3 fixture metadata
- Phase 24.3 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 24.4 archive/closeout.

## Phase 24.4 Gate: Phase 24 Hardening Audit Archive / Closeout

Phase 24.4 archives Phase 24 and preserves Phase 25 as a gated test-only hardening direction.

Allowed:

- Phase 24.4 tests
- Phase 24.4 fixture metadata
- Phase 24.4 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 24.4. Phase 25 requires explicit approval.

## Phase 25.0 Gate: Cross-API Candidate Invariant Matrix Charter

Phase 25.0 opens the approved test-only hardening lane for a cross-API candidate invariant matrix.

Allowed:

- Phase 25.0 tests
- Phase 25.0 fixture metadata
- Phase 25.0 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 25.1 candidate API matrix fixtures.

## Phase 25.1 Gate: Candidate API Matrix Fixtures

Phase 25.1 adds synthetic fixtures for cross-API candidate invariant tests.

Allowed:

- Phase 25.1 tests
- Phase 25.1 synthetic fixtures
- Phase 25.1 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 25.2 cross-API non-execution invariant tests.

## Phase 25.2 Gate: Cross-API Non-Execution Invariant Tests

Phase 25.2 adds deterministic tests proving existing candidate-facing APIs preserve non-execution invariants.

Allowed:

- Phase 25.2 tests
- Phase 25.2 fixture metadata
- Phase 25.2 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 25.3 cross-API provenance and status invariant tests.

## Phase 25.3 Gate: Cross-API Provenance and Status Invariant Tests

Phase 25.3 adds deterministic tests for provenance and status invariants across existing candidate-facing APIs.

Allowed:

- Phase 25.3 tests
- Phase 25.3 fixture metadata
- Phase 25.3 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 25.4 cross-API boundary readiness review.

## Phase 25.4 Gate: Cross-API Boundary Readiness Review

Phase 25.4 reviews the Phase 25 cross-API candidate invariant hardening package as ready for archive/closeout.

Allowed:

- Phase 25.4 tests
- Phase 25.4 fixture metadata
- Phase 25.4 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 25.5 archive/closeout.

## Phase 25.5 Gate: Phase 25 Test-Only Hardening Archive / Closeout

Phase 25.5 archives Phase 25 as a completed test-only cross-API candidate invariant hardening lane.

Allowed:

- Phase 25.5 tests
- Phase 25.5 fixture metadata
- Phase 25.5 documentation
- roadmap/state metadata

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 25.5. Phase 26 requires explicit approval.

## Phase 26.0 Gate: Phase 25 Cross-API Invariant Audit Charter

Phase 26.0 opens the approved docs/tests/fixtures-only audit/archive and next-lane decision lane for the Phase 25 package.

Allowed:

- Phase 26.0 tests
- Phase 26.0 fixture metadata
- Phase 26.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 26.1 cross-API invariant coverage review.

## Phase 26.1 Gate: Cross-API Invariant Coverage Review

Phase 26.1 reviews Phase 25 coverage across existing candidate-facing APIs.

Allowed:

- Phase 26.1 tests
- Phase 26.1 fixture metadata
- Phase 26.1 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 26.2 remaining cross-API gap review.

## Phase 26.2 Gate: Remaining Cross-API Gap Review

Phase 26.2 records remaining gaps as planning inputs only.

Allowed:

- Phase 26.2 tests
- Phase 26.2 fixture metadata
- Phase 26.2 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 26.3 next-lane decision matrix.

## Phase 26.3 Gate: Next-Lane Decision Matrix

Phase 26.3 recommends Phase 27 as a docs/tests/fixtures-only preservation and roadmap decision lane.

Allowed:

- Phase 26.3 tests
- Phase 26.3 fixture metadata
- Phase 26.3 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 26.4 archive/closeout.

## Phase 26.4 Gate: Phase 26 Cross-API Audit Archive / Closeout

Phase 26.4 archives Phase 26 and preserves Phase 27 as a gated docs/tests/fixtures-only preservation and roadmap decision lane.

Allowed:

- Phase 26.4 tests
- Phase 26.4 fixture metadata
- Phase 26.4 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 26.4. Phase 27 requires explicit approval.

## Phase 27.0 Gate: Phase 26 Preservation Audit Charter

Phase 27.0 opens the approved docs/tests/fixtures-only preservation and roadmap decision lane after the Phase 26 archive.

Allowed:

- Phase 27.0 tests
- Phase 27.0 fixture metadata
- Phase 27.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 27.1 current runtime/test state preservation record.

## Phase 27.1 Gate: Current Runtime/Test State Preservation Record

Phase 27.1 records the current known-good runtime/test state.

Allowed:

- Phase 27.1 tests
- Phase 27.1 fixture metadata
- Phase 27.1 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 27.2 gated runtime boundary review.

## Phase 27.2 Gate: Gated Runtime Boundary Review

Phase 27.2 reviews blocked runtime and integration boundaries.

Allowed:

- Phase 27.2 tests
- Phase 27.2 fixture metadata
- Phase 27.2 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 27.3 next-lane risk decision matrix.

## Phase 27.3 Gate: Next-Lane Risk Decision Matrix

Phase 27.3 recommends Phase 28 as a docs/tests/fixtures-only preservation status review.

Allowed:

- Phase 27.3 tests
- Phase 27.3 fixture metadata
- Phase 27.3 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 27.4 preservation archive/closeout.

## Phase 27.4 Gate: Phase 27 Preservation Archive / Closeout

Phase 27.4 archives Phase 27 and preserves Phase 28 as a gated docs/tests/fixtures-only preservation status review.

Allowed:

- Phase 27.4 tests
- Phase 27.4 fixture metadata
- Phase 27.4 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 27.4. Phase 28 requires explicit approval.

## Phase 28.0 Gate: Phase 27 Preservation Status Audit Charter

Phase 28.0 opens the approved docs/tests/fixtures-only preservation status review after Phase 27.

Allowed:

- Phase 28.0 tests
- Phase 28.0 fixture metadata
- Phase 28.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 28.1 stable runtime/test state review.

## Phase 28.1 Gate: Stable Runtime/Test State Review

Phase 28.1 confirms the current runtime/test state remains stable and preserved.

Allowed:

- Phase 28.1 tests
- Phase 28.1 fixture metadata
- Phase 28.1 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 28.2 preservation pause justification review.

## Phase 28.2 Gate: Preservation Pause Justification Review

Phase 28.2 reviews whether continued preservation pause remains justified.

Allowed:

- Phase 28.2 tests
- Phase 28.2 fixture metadata
- Phase 28.2 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 28.3 Phase 29 decision readiness matrix.

## Phase 28.3 Gate: Phase 29 Decision Readiness Matrix

Phase 28.3 recommends Phase 29 as a docs/tests/fixtures-only no-code design review for the next narrow runtime slice.

Allowed:

- Phase 28.3 tests
- Phase 28.3 fixture metadata
- Phase 28.3 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 28.4 preservation status archive/closeout.

## Phase 28.4 Gate: Phase 28 Preservation Status Archive / Closeout

Phase 28.4 archives Phase 28 and preserves Phase 29 as a gated docs/tests/fixtures-only no-code design review.

Allowed:

- Phase 28.4 tests
- Phase 28.4 fixture metadata
- Phase 28.4 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 28.4. Phase 29 requires explicit approval.

## Phase 29.0 Gate: Phase 28 No-Code Design Review Audit Charter

Phase 29.0 opens the approved docs/tests/fixtures-only no-code design review for the next narrow runtime slice.

Allowed:

- Phase 29.0 tests
- Phase 29.0 fixture metadata
- Phase 29.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 29.1 narrow runtime slice candidate inventory.

## Phase 29.1 Gate: Narrow Runtime Slice Candidate Inventory

Phase 29.1 inventories candidate future runtime slices and recommends the safest candidate for no-code boundary design.

Allowed:

- Phase 29.1 tests
- Phase 29.1 fixture metadata
- Phase 29.1 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 29.2 runtime slice safety boundary design.

## Phase 29.2 Gate: Runtime Slice Safety Boundary Design

Phase 29.2 defines the no-code safety boundary for a future read-only runtime state inspection slice.

Allowed:

- Phase 29.2 tests
- Phase 29.2 fixture metadata
- Phase 29.2 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 29.3 future implementation eligibility matrix.

## Phase 29.3 Gate: Future Implementation Eligibility Matrix

Phase 29.3 defines the future implementation eligibility criteria, acceptance tests, rollback/audit proof, and exact Phase 30 approval question for a possible read-only runtime state inspection slice.

Allowed:

- Phase 29.3 tests
- Phase 29.3 fixture metadata
- Phase 29.3 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 29.4 Phase 29 no-code design review archive / closeout.

## Phase 29.4 Gate: Phase 29 No-Code Design Review Archive / Closeout

Phase 29.4 archives Phase 29 as a completed docs/tests/fixtures-only no-code design review and preserves Phase 30 as a gated runtime implementation decision.

Allowed:

- Phase 29.4 tests
- Phase 29.4 fixture metadata
- Phase 29.4 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 29.4. Phase 30 requires explicit Phil approval.

## Phase 30.0 Gate: Phase 29 Runtime Implementation Audit Charter

Phase 30.0 audits Phase 29 and confirms the approved Phase 30 read-only runtime state inspection scope before runtime files are touched.

Allowed:

- Phase 30.0 tests
- Phase 30.0 fixture metadata
- Phase 30.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 30.1 read-only runtime state inspection acceptance design.

## Phase 30.1 Gate: Read-Only Runtime State Inspection Acceptance Design

Phase 30.1 defines acceptance and regression coverage for the approved read-only runtime state inspection slice before implementation.

Allowed:

- Phase 30.1 tests
- Phase 30.1 fixture metadata
- Phase 30.1 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 30.2 read-only runtime state inspection implementation.

## Phase 30.2 Gate: Read-Only Runtime State Inspection Implementation

Phase 30.2 implements the approved read-only runtime state inspection slice.

Allowed:

- `lima/kernel/runtime_state.py`
- `lima/kernel/__init__.py` only for safe public export
- Phase 30.2 tests
- Phase 30.2 fixture metadata
- Phase 30.2 documentation
- roadmap/state metadata updates

Forbidden:

- `lima/kernel/intake_candidate.py` changes
- `lima/kernel/candidate_status.py` changes
- all other `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 30.3 runtime state inspection boundary regression review.

## Phase 30.3 Gate: Runtime State Inspection Boundary Regression Review

Phase 30.3 reviews the Phase 30.2 runtime state inspection boundary and confirms the slice remains inside the approved scope.

Allowed:

- Phase 30.3 tests
- Phase 30.3 fixture metadata
- Phase 30.3 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 30.4 Phase 30 runtime slice archive / closeout.

## Phase 30.4 Gate: Phase 30 Runtime Slice Archive / Closeout

Phase 30.4 archives Phase 30 as the completed narrow read-only runtime state inspection slice and preserves the Phase 31 gate.

Allowed:

- Phase 30.4 tests
- Phase 30.4 fixture metadata
- Phase 30.4 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 30.4. Phase 31 requires explicit Phil approval.

## Phase 31.0 Gate: Phase 30 Runtime Slice Audit Charter

Phase 31.0 opens the docs/tests/fixtures-only audit/archive and next-lane decision phase for the completed Phase 30 runtime slice.

Allowed:

- Phase 31.0 tests
- Phase 31.0 fixture metadata
- Phase 31.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 31.1 read-only runtime state boundary evidence review.

## Phase 31.1 Gate: Read-Only Runtime State Boundary Evidence Review

Phase 31.1 records evidence that the completed Phase 30 runtime state inspection slice remains inside the approved read-only boundary.

Allowed:

- Phase 31.1 tests
- Phase 31.1 fixture metadata
- Phase 31.1 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 31.2 runtime slice regression and gap review.

## Phase 31.2 Gate: Runtime Slice Regression and Gap Review

Phase 31.2 reviews Phase 30 regression coverage and remaining gaps before selecting the Phase 32 direction.

Allowed:

- Phase 31.2 tests
- Phase 31.2 fixture metadata
- Phase 31.2 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 31.3 Phase 32 next-lane decision matrix.

## Phase 31.3 Gate: Phase 32 Next-Lane Decision Matrix

Phase 31.3 evaluates Phase 32 options and recommends the safest next lane after the Phase 30 runtime slice audit.

Allowed:

- Phase 31.3 tests
- Phase 31.3 fixture metadata
- Phase 31.3 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 31.4 Phase 31 runtime slice audit archive / closeout.

## Phase 31.4 Gate: Phase 31 Runtime Slice Audit Archive / Closeout

Phase 31.4 archives Phase 31 as the completed docs/tests/fixtures-only audit/archive for the Phase 30 runtime slice and preserves the Phase 32 gate.

Allowed:

- Phase 31.4 tests
- Phase 31.4 fixture metadata
- Phase 31.4 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Stop after Phase 31.4. Phase 32 requires explicit Phil approval.

## Phase 32.0 Gate: Phase 31 Next-Slice Design Audit Charter

Phase 32.0 opens the docs/tests/fixtures-only design review for the next narrow runtime slice and records the Phase 31 audit result.

Allowed:

- Phase 32.0 tests
- Phase 32.0 fixture metadata
- Phase 32.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation changes
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation/robotics/physical-world behavior

Continue only to Phase 32.1 candidate runtime slice inventory.

## Phase 32.1 Gate: Candidate Runtime Slice Inventory

Phase 32.1 inventories the requested candidate next lanes after the Phase 30 read-only runtime state inspection slice.

Allowed:

- Phase 32.1 tests
- Phase 32.1 fixture metadata
- Phase 32.1 documentation
- roadmap/state metadata updates

Recommendation:

- Phase 33 should be test-only `runtime_state` hardening with nested suspicious metadata fixtures.
- Phase 33 should not implement runtime code or change `lima/`.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior.

## Phase 33.0 Gate: Phase 32 Test-Only Hardening Audit Charter

Phase 33.0 opens the approved test-only hardening lane for the existing read-only `runtime_state` inspection slice.

Allowed:

- Phase 33.0 tests
- Phase 33.0 fixture metadata
- Phase 33.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 33.1 nested suspicious metadata fixture design.

## Phase 33.1 Gate: Nested Suspicious Metadata Fixture Design

Phase 33.1 adds synthetic caller-provided nested metadata fixtures for `runtime_state` hardening.

Allowed:

- Phase 33.1 tests
- Phase 33.1 fixture metadata
- Phase 33.1 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 33.2 runtime state nested metadata regression tests.

## Phase 33.2 Gate: Runtime State Nested Metadata Regression Tests

Phase 33.2 adds regression tests for nested suspicious metadata using the existing `inspect_runtime_state` API.

Allowed:

- Phase 33.2 tests
- Phase 33.2 fixture metadata
- Phase 33.2 documentation
- roadmap/state metadata updates

Result:

- Nested suspicious metadata remains safe.
- No runtime_state gap requiring runtime code changes was found.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 33.3 Phase 34 next-lane decision matrix.

## Phase 33.3 Gate: Phase 34 Next-Lane Decision Matrix

Phase 33.3 recommends the safest Phase 34 direction after Phase 33 nested metadata regression hardening.

Allowed:

- Phase 33.3 tests
- Phase 33.3 fixture metadata
- Phase 33.3 documentation
- roadmap/state metadata updates

Decision:

- Phase 34 should be docs/tests/fixtures-only audit/archive for Phase 33 hardening.
- Immediate runtime implementation is not recommended.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 33.4 test-only hardening archive and closeout.

## Phase 33.4 Gate: Phase 33 Test-Only Hardening Archive / Closeout

Phase 33.4 archives Phase 33 as completed test-only hardening for the existing read-only `runtime_state` inspection slice.

Allowed:

- Phase 33.4 tests
- Phase 33.4 fixture metadata
- Phase 33.4 documentation
- roadmap/state metadata updates

Decision:

- Phase 33 found no concrete runtime_state gap.
- Phase 34 should be docs/tests/fixtures-only audit/archive.
- Immediate runtime implementation is not recommended.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Stop after Phase 33.4.

## Phase 34.0 Gate: Phase 33 Hardening Audit Charter

Phase 34.0 opens the docs/tests/fixtures-only audit/archive lane for the completed Phase 33 hardening package.

Allowed:

- Phase 34.0 tests
- Phase 34.0 fixture metadata
- Phase 34.0 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 34.1 nested metadata coverage evidence review.

## Phase 34.1 Gate: Nested Metadata Coverage Evidence Review

Phase 34.1 reviews the Phase 33 nested metadata fixture and regression evidence.

Allowed:

- Phase 34.1 tests
- Phase 34.1 fixture metadata
- Phase 34.1 documentation
- roadmap/state metadata updates

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 34.2 runtime state hardening gap review.

## Phase 34.2 Gate: Runtime State Hardening Gap Review

Phase 34.2 reviews whether the Phase 33 hardening package revealed a concrete `runtime_state` gap.

Allowed:

- Phase 34.2 tests
- Phase 34.2 fixture metadata
- Phase 34.2 documentation
- roadmap/state metadata updates

Decision:

- No concrete `runtime_state` gap was found.
- No runtime code change is needed.
- No immediate additional test-only hardening is needed before archive.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 34.3 Phase 35 next-lane decision matrix.

## Phase 34.3 Gate: Phase 35 Next-Lane Decision Matrix

Phase 34.3 recommends the safest Phase 35 direction after Phase 33 hardening and Phase 34 audit evidence.

Allowed:

- Phase 34.3 tests
- Phase 34.3 fixture metadata
- Phase 34.3 documentation
- roadmap/state metadata updates

Decision:

- Phase 35 should be docs/tests/fixtures-only no-code design review for a possible second narrow runtime slice.
- Immediate runtime implementation is not recommended.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 34.4 hardening archive and closeout.

## Phase 34.4 Gate: Phase 34 Hardening Archive / Closeout

Phase 34.4 archives Phase 34 as a completed docs/tests/fixtures-only audit/archive lane.

Allowed:

- Phase 34.4 tests
- Phase 34.4 fixture metadata
- Phase 34.4 documentation
- roadmap/state metadata updates

Decision:

- Nested suspicious metadata audit result is PASS.
- No remaining gaps were found.
- Phase 35 should be docs/tests/fixtures-only no-code design review for a possible second narrow runtime slice.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior

Stop after Phase 34.4.

## Phase 35.0 Gate: Phase 34 Second-Slice Design Audit Charter

Phase 35.0 opens the docs/tests/fixtures-only no-code design review lane for a possible second narrow runtime slice.

Allowed:

- Phase 35.0 tests
- Phase 35.0 fixture metadata
- Phase 35.0 documentation
- roadmap/state metadata updates

Decision:

- Phase 34 audit result is PASS.
- Phase 35 is no-code design review only.
- No Phase 36 runtime implementation is approved.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 35.1 second runtime slice candidate inventory.

## Phase 35.1 Gate: Second Runtime Slice Candidate Inventory

Phase 35.1 inventories candidate second runtime slices without implementation.

Allowed:

- Phase 35.1 tests
- Phase 35.1 fixture metadata
- Phase 35.1 documentation
- roadmap/state metadata updates

Decision:

- Options A through H were reviewed.
- Option C, a non-executing candidate preview helper over caller-provided data only, is the leading future design candidate.
- Phase 36 implementation remains unapproved.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 35.2 second-slice safety and scope comparison.

## Phase 35.2 Gate: Second-Slice Safety And Scope Comparison

Phase 35.2 compares candidate second runtime slices by safety, usefulness, file scope, testability, rollback simplicity, and risk.

Allowed:

- Phase 35.2 tests
- Phase 35.2 fixture metadata
- Phase 35.2 documentation
- roadmap/state metadata updates

Decision:

- Option C remains the recommended future Phase 36 candidate if Phil explicitly approves it later.
- The possible future runtime file scope is limited to `lima/kernel/candidate_preview.py` and `lima/kernel/__init__.py` only if a safe public export is required.
- Existing runtime files and `tests/support/` remain forbidden.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 35.3 Phase 36 eligibility and test plan matrix.

## Phase 35.3 Gate: Phase 36 Eligibility And Test Plan Matrix

Phase 35.3 defines eligibility criteria, acceptance-test requirements, rollback/audit proof, stop conditions, and the exact future Phase 36 approval question.

Allowed:

- Phase 35.3 tests
- Phase 35.3 fixture metadata
- Phase 35.3 documentation
- roadmap/state metadata updates

Decision:

- Phase 36 implementation remains unapproved.
- Candidate preview is eligible only if it remains deterministic, local-only, read-only, non-authoritative, non-executing, caller-provided-data only, and fully testable without `tests/support/` changes.
- Stop conditions and rollback/audit proof are defined.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 35.4 Phase 35 design review archive and closeout.

## Phase 35.4 Gate: Phase 35 Design Review Archive / Closeout

Phase 35.4 archives Phase 35 as a completed docs/tests/fixtures-only no-code design review.

Allowed:

- Phase 35.4 tests
- Phase 35.4 fixture metadata
- Phase 35.4 documentation
- roadmap/state metadata updates

Decision:

- Phase 35 is archived as no-code design review only.
- The recommended Phase 36 direction is a candidate preview helper only if explicitly approved by Phil.
- Phase 36 remains gated.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Stop after Phase 35.4.

## Phase 36.0 Gate: Phase 35 Runtime Implementation Audit Charter

Phase 36.0 opens the explicitly approved narrow candidate preview runtime implementation lane after auditing Phase 35.

Allowed:

- Phase 36.0 tests
- Phase 36.0 fixture metadata
- Phase 36.0 documentation
- roadmap/state metadata updates

Decision:

- Phase 35 audit result is PASS.
- Phase 36 implementation scope is limited to `lima/kernel/candidate_preview.py` and `lima/kernel/__init__.py` only if a safe public export is required.
- Phase 36.0 itself adds no runtime implementation.

Forbidden:

- changes to `runtime_state.py`, `intake_candidate.py`, `candidate_status.py`, any other existing `lima/` file, or `tests/support/`
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 36.1 candidate preview acceptance design.

## Phase 36.1 Gate: Candidate Preview Acceptance Design

Phase 36.1 defines acceptance requirements before candidate preview implementation.

Allowed:

- Phase 36.1 tests
- Phase 36.1 fixture metadata
- Phase 36.1 documentation
- roadmap/state metadata updates

Decision:

- Candidate preview output must expose explicit safe flags.
- Missing, malformed, unknown, suspicious, nested, and bypass-worded input must remain safe.
- Static boundary scans are required before implementation can land.

Forbidden:

- runtime implementation in Phase 36.1
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 36.2 candidate preview runtime implementation.

## Phase 36.2 Gate: Candidate Preview Runtime Implementation

Phase 36.2 adds the approved candidate preview runtime helper.

Allowed:

- `lima/kernel/candidate_preview.py`
- `lima/kernel/__init__.py` only for safe public export
- Phase 36.2 tests
- Phase 36.2 fixture metadata
- Phase 36.2 documentation
- roadmap/state metadata updates

Decision:

- `preview_candidate` returns deterministic, local-only, read-only, non-authoritative, non-executing preview metadata.
- Suspicious caller-provided claims are blocked and reported as metadata only.
- Phase 5 HumanInput runtime bridge remains gated.

Forbidden:

- changes to `runtime_state.py`, `intake_candidate.py`, `candidate_status.py`, any other existing `lima/` file, or `tests/support/`
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 36.3 candidate preview boundary regression review.

## Phase 36.3 Gate: Candidate Preview Boundary Regression Review

Phase 36.3 reviews the Phase 36.2 candidate preview implementation.

Allowed:

- Phase 36.3 tests
- Phase 36.3 fixture metadata
- Phase 36.3 documentation
- roadmap/state metadata updates

Decision:

- Phase 36.2 changed only approved runtime files.
- Phase 36.3 adds no new runtime behavior.
- The stale Phase 35 test adjustment is narrow and documented.

Forbidden:

- new runtime behavior
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 36.4 runtime slice archive and closeout.

## Phase 36.4 Gate: Phase 36 Runtime Slice Archive / Closeout

Phase 36.4 archives Phase 36 as a completed narrow candidate preview runtime slice.

Allowed:

- Phase 36.4 tests
- Phase 36.4 fixture metadata
- Phase 36.4 documentation
- roadmap/state metadata updates

Decision:

- Phase 36 candidate preview runtime slice is archived.
- Phase 37 should be docs/tests/fixtures-only audit/archive and next-lane decision.
- No additional runtime implementation is approved.

Forbidden:

- new runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Stop after Phase 36.4.

## Phase 37.0 Gate: Phase 36 Candidate Preview Audit Charter

Phase 37.0 opens the docs/tests/fixtures-only audit/archive lane for the completed Phase 36 candidate preview runtime slice.

Allowed:

- Phase 37.0 tests
- Phase 37.0 fixture metadata
- Phase 37.0 documentation
- roadmap/state metadata updates

Decision:

- Phase 36 audit result is PASS.
- Phase 37 is audit/archive only.
- No new runtime implementation is approved.

Forbidden:

- new runtime implementation
- `lima/` changes
- `tests/support/` changes
- stale prior-phase test changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 37.1 candidate preview boundary evidence review.

## Phase 37.1 Gate: Candidate Preview Boundary Evidence Review

Phase 37.1 reviews Phase 36 candidate preview boundary evidence.

Allowed:

- Phase 37.1 tests
- Phase 37.1 fixture metadata
- Phase 37.1 documentation
- roadmap/state metadata updates

Decision:

- Candidate preview boundary evidence remains inert and non-authoritative.
- Static scan evidence is preserved.
- No runtime change is needed.

Forbidden:

- new runtime implementation
- `lima/` changes
- `tests/support/` changes
- stale prior-phase test changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 37.2 candidate preview regression and gap review.

## Phase 37.2 Gate: Candidate Preview Regression And Gap Review

Phase 37.2 reviews remaining candidate preview regressions or gaps.

Allowed:

- Phase 37.2 tests
- Phase 37.2 fixture metadata
- Phase 37.2 documentation
- roadmap/state metadata updates

Decision:

- No regression was found.
- No blocking gap was found.
- No immediate test-only hardening need was found.

Forbidden:

- new runtime implementation
- `lima/` changes
- `tests/support/` changes
- stale prior-phase test changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 37.3 next-lane decision matrix.

## Phase 37.3 Gate: Next-Lane Decision Matrix

Phase 37.3 evaluates next-lane options after the Phase 36 candidate preview runtime slice.

Allowed:

- Phase 37.3 tests
- Phase 37.3 fixture metadata
- Phase 37.3 documentation
- roadmap/state metadata updates

Decision:

- Pause and preserve current runtime/test state is recommended after Phase 37.4.
- No immediate runtime implementation is recommended.
- No immediate test-only hardening is recommended.

Forbidden:

- new runtime implementation
- `lima/` changes
- `tests/support/` changes
- stale prior-phase test changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, mutation, external calls, background work, robotics, or physical-world behavior

Continue only to Phase 37.4 candidate preview audit archive and closeout.

## Phase 37.4 Gate: Candidate Preview Audit Archive Closeout

Phase 37.4 archives Phase 37 as the completed docs/tests/fixtures-only audit lane for the Phase 36 candidate preview runtime slice.

Allowed:

- Phase 37.4 tests
- Phase 37.4 fixture metadata
- Phase 37.4 documentation
- README and roadmap/state documentation updates

Blocked:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- stale prior-phase test changes
- Sparkbot wiring/imports
- HumanInput runtime bridge behavior
- live adapters
- IntentCompiler runtime behavior changes
- GuardianDecision runtime behavior changes
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation
- robotics or physical-world behavior
- external service calls
- background workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects

Outcome:

- Phase 37 is complete.
- No remaining gap was found.
- Pause and preserve current runtime/test state.
- No Phase 38 approval question is required by this closeout.

## Phase 38.0 Gate: Sparkbot Alignment Audit Charter

Phase 38.0 opens Sparkbot v1.6.80 alignment intake after the Phase 37 checkpoint.

Allowed:

- Sparkbot source review as read-only reference material
- Phase 38.0 tests
- Phase 38.0 fixture metadata
- Phase 38.0 documentation
- README and roadmap/state documentation updates

Blocked:

- Sparkbot repository changes
- Sparkbot imports or wiring
- LIMA runtime changes
- `tests/support/` changes
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution
- dispatch
- audit persistence
- shell/browser/network/file mutation
- robotics or physical-world behavior
- external service calls
- background workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects

Continue only to Phase 38.1 Sparkbot v1.6.42-to-v1.6.80 concept intake.

## Phase 38.1 Gate: Sparkbot v1.6.42-to-v1.6.80 Concept Intake

Phase 38.1 records the Sparkbot concept delta as LIMA planning metadata.

Allowed:

- Concept intake documentation
- Phase 38.1 fixture metadata
- Phase 38.1 tests
- README and roadmap/state documentation updates

Blocked:

- Sparkbot code changes
- Sparkbot imports or wiring
- LIMA runtime changes
- runtime permission changes
- approval, execution, dispatch, persistence, mutation, external calls, or robotics/physical-world behavior

Continue only to Phase 38.2 LIMA consumer boundary vocabulary review.

## Phase 38.2 Gate: LIMA Consumer Boundary Vocabulary Review

Phase 38.2 defines Sparkbot-shaped vocabulary for future LIMA consumer contracts.

Allowed:

- Vocabulary documentation
- Phase 38.2 fixture metadata
- Phase 38.2 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime authority
- Sparkbot wiring
- HumanInput bridge behavior
- live adapters
- approval enforcement
- execution
- dispatch
- persistence
- MCP calls
- robotics/physical-world behavior

Continue only to Phase 38.3 Sparkbot-to-LIMA gap and risk matrix.

## Phase 38.3 Gate: Sparkbot-to-LIMA Gap and Risk Matrix

Phase 38.3 maps Sparkbot v1.6.80 concepts to current LIMA support and remaining gaps.

Allowed:

- Gap/risk documentation
- Phase 38.3 fixture metadata
- Phase 38.3 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot wiring
- HumanInput bridge behavior
- approval enforcement
- execution
- dispatch
- persistence
- MCP calls
- robotics/physical-world behavior

Continue only to Phase 38.4 alignment archive and closeout.

## Phase 38.4 Gate: Alignment Archive Closeout

Phase 38.4 archives Sparkbot v1.6.80 alignment intake.

Allowed:

- Archive documentation
- Phase 38.4 fixture metadata
- Phase 38.4 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- approval enforcement
- execution
- dispatch
- persistence
- MCP calls
- robotics/physical-world behavior

Recommended next lane:

- Phase 39 test-only `candidate_preview` hardening with Sparkbot-shaped fixtures.

## Phase 39.0 Gate: Sparkbot-Shaped Candidate Preview Hardening Charter

Phase 39.0 opens the test-only hardening lane for existing `candidate_preview` behavior.

Allowed:

- Phase 39.0 documentation
- Phase 39.0 fixture metadata
- Phase 39.0 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- stale prior-phase test changes
- approval enforcement
- execution
- dispatch
- persistence
- MCP calls
- robotics/physical-world behavior

Continue only to Phase 39.1 Sparkbot-shaped candidate preview fixtures.

## Phase 39.1 Gate: Sparkbot-Shaped Candidate Preview Fixtures

Phase 39.1 adds inert JSON fixtures for Sparkbot-shaped caller-provided candidate preview inputs.

Allowed:

- Phase 39.1 fixture metadata
- Phase 39.1 tests
- Phase 39.1 documentation
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- approval enforcement, execution, dispatch, persistence, MCP calls, external calls, robotics, or physical-world behavior

Continue only to Phase 39.2 runtime candidate preview Sparkbot-shaped regression tests.

## Phase 39.2 Gate: Candidate Preview Sparkbot-Shaped Regression Tests

Phase 39.2 tests the existing `candidate_preview` helper against Sparkbot-shaped fixtures.

Allowed:

- Phase 39.2 regression tests
- Phase 39.2 fixture metadata
- Phase 39.2 documentation
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- approval enforcement, execution, dispatch, persistence, MCP calls, external calls, robotics, or physical-world behavior

Continue only to Phase 39.3 hardening gap and next-lane decision review.

## Phase 39.3 Gate: Hardening Gap and Next-Lane Decision Review

Phase 39.3 reviews Phase 39 hardening results.

Allowed:

- Phase 39.3 decision documentation
- Phase 39.3 fixture metadata
- Phase 39.3 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- approval enforcement, execution, dispatch, persistence, MCP calls, external calls, robotics, or physical-world behavior

Continue only to Phase 39.4 archive and closeout.

## Phase 39.4 Gate: Sparkbot-Shaped Hardening Archive Closeout

Phase 39.4 archives completed Sparkbot-shaped `candidate_preview` hardening.

Allowed:

- Phase 39.4 archive documentation
- Phase 39.4 fixture metadata
- Phase 39.4 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- stale prior-phase test changes
- approval enforcement, execution, dispatch, persistence, MCP calls, external calls, robotics, or physical-world behavior

Outcome:

- Phase 39 complete.
- No remaining gap.
- Pause and preserve current runtime/test state.

## Phase 40.0 Gate: Arc Bot Consumer Boundary Clarification

Phase 40.0 clarifies the Phase 38 Sparkbot alignment intake without rewriting completed history.

Allowed:

- Phase 40.0 clarification documentation
- Phase 40.0 fixture metadata
- Phase 40.0 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- stale prior-phase test changes
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution
- dispatch
- persistence
- shell/browser/network/file mutation
- robotics/physical-world behavior
- external calls or background work

Framing:

- Sparkbot v1.6.80 concept intake for future Arc Bot / LIMA Office consumer boundary planning.
- Not direct Sparkbot integration planning.

## Phase 40.1 Gate: Arc Bot Guarded Task Consumer Boundary Review

Phase 40.1 defines Arc Bot / LIMA AI Office as a guarded task-oriented office consumer.

Allowed:

- Phase 40.1 documentation
- Phase 40.1 fixture metadata
- Phase 40.1 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 40.2 LIMA Office task/approval/audit vocabulary matrix.

## Phase 40.2 Gate: LIMA Office Task Approval Audit Vocabulary Matrix

Phase 40.2 records the planning vocabulary for Arc Bot / LIMA AI Office as a guarded task-oriented consumer.

Allowed:

- Phase 40.2 documentation
- Phase 40.2 fixture metadata
- Phase 40.2 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 40.3 Arc Bot candidate preview fixture plan.

## Phase 40.3 Gate: Arc Bot Candidate Preview Fixture Plan

Phase 40.3 defines Arc Bot-shaped fixture targets for future `candidate_preview` hardening.

Allowed:

- Phase 40.3 documentation
- Phase 40.3 fixture metadata
- Phase 40.3 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 40.4 Arc Bot consumer boundary archive / closeout.

## Phase 40.4 Gate: Arc Bot Consumer Boundary Archive / Closeout

Phase 40.4 archives Phase 40 as a completed docs/tests/fixtures-only Arc Bot / LIMA Office consumer boundary review.

Allowed:

- Phase 40.4 documentation
- Phase 40.4 fixture metadata
- Phase 40.4 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Recommended next lane:

- Phase 41 docs/tests/fixtures-only Arc Bot-shaped `candidate_preview` hardening.

## Phase 41.0 Gate: Arc Bot Candidate Preview Hardening Charter

Phase 41.0 opens the docs/tests/fixtures-only Arc Bot-shaped `candidate_preview` hardening lane.

Allowed:

- Phase 41.0 documentation
- Phase 41.0 fixture metadata
- Phase 41.0 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 41.1 Arc Bot candidate preview fixtures.

## Phase 41.1 Gate: Arc Bot Candidate Preview Fixtures

Phase 41.1 adds synthetic Arc Bot / LIMA Office fixture data for the existing `candidate_preview` helper.

Allowed:

- Phase 41.1 documentation
- Phase 41.1 fixture metadata
- Phase 41.1 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 41.2 Arc Bot candidate preview regression tests.

## Phase 41.2 Gate: Arc Bot Candidate Preview Regression Tests

Phase 41.2 adds regression tests over the Phase 41.1 Arc Bot-shaped fixture corpus using the existing `candidate_preview` helper.

Allowed:

- Phase 41.2 documentation
- Phase 41.2 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 41.3 Arc Bot hardening gap and next-lane review.

## Phase 41.3 Gate: Arc Bot Hardening Gap And Next-Lane Review

Phase 41.3 reviews the Arc Bot-shaped `candidate_preview` hardening results.

Allowed:

- Phase 41.3 documentation
- Phase 41.3 fixture metadata
- Phase 41.3 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 41.4 Arc Bot hardening archive closeout.

## Phase 41.4 Gate: Arc Bot Candidate Preview Hardening Archive / Closeout

Phase 41.4 archives the Arc Bot-shaped `candidate_preview` hardening lane.

Allowed:

- Phase 41.4 documentation
- Phase 41.4 fixture metadata
- Phase 41.4 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Recommended next lane:

- docs/tests/fixtures-only no-code Arc Bot / LIMA Office consumer contract design review.

## Phase 42.0 Gate: LIMA Universal Runtime Contract Reframing Audit

Phase 42.0 corrects the next lane from Arc-centered consumer planning to universal LIMA AI OS contract planning.

Allowed:

- Phase 42.0 documentation
- Phase 42.0 fixture metadata
- Phase 42.0 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 42.1 model-agnostic task/intent contract design.

## Phase 42.1 Gate: Model-Agnostic Task Intent Contract Design

Phase 42.1 records universal LIMA AI OS planning contracts for model-agnostic input, task/intent, candidate action preview, approval posture, telemetry/evidence, and embodiment/profile metadata.

Allowed:

- Phase 42.1 documentation
- Phase 42.1 fixture metadata
- Phase 42.1 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- runtime schemas
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, or physical-world behavior

Continue only to Phase 42.2 consumer and embodiment profile taxonomy.

## Phase 42.2 Gate: Consumer And Embodiment Profile Taxonomy

Phase 42.2 records universal LIMA AI OS consumer profiles, embodiment/action profiles, action classes, and adapter-boundary vocabulary.

Allowed:

- Phase 42.2 documentation
- Phase 42.2 fixture metadata
- Phase 42.2 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, hardware calls, or physical-world behavior

Continue only to Phase 42.3 universal safety invariants and Guardian boundary matrix.

## Phase 42.3 Gate: Universal Safety Invariants And Guardian Boundary Matrix

Phase 42.3 records hard invariants and the Guardian/future policy membrane boundary for universal LIMA AI OS planning.

Allowed:

- Phase 42.3 documentation
- Phase 42.3 fixture metadata
- Phase 42.3 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, MCP/hardware calls, adapters, or physical-world behavior

Continue only to Phase 42.4 universal runtime contract archive / closeout.

## Phase 42.4 Gate: Universal Runtime Contract Archive / Closeout

Phase 42.4 archives Phase 42 as a completed docs/tests/fixtures-only LIMA AI OS Universal Runtime Contract Design lane.

Allowed:

- Phase 42.4 documentation
- Phase 42.4 fixture metadata
- Phase 42.4 tests
- README and roadmap/state documentation updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, adapters, hardware calls, or physical-world behavior

Recommended next lane:

- Phase 43 docs/tests/fixtures-only Universal Contract Fixture Hardening.

## Phase 43.0 Gate: Universal Contract Fixture Hardening Charter

Phase 43.0 opens Phase 43 as a docs/tests/fixtures-only Universal Contract Fixture Hardening lane.

Allowed:

- Phase 43.0 documentation
- Phase 43.0 inert fixture metadata
- Phase 43.0 tests
- README, roadmap, decision, extraction-plan, and current-state updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, adapters, hardware calls, physical-world behavior, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects

Recommended next lane:

- Phase 43.1 docs/tests/fixtures-only inert universal contract profile fixture corpus.

## Phase 43.1 Gate: Universal Contract Profile Fixtures

Phase 43.1 adds inert universal contract profile fixture data only.

Allowed:

- Phase 43.1 documentation
- Phase 43.1 inert fixture metadata
- Phase 43.1 tests that validate fixture shape and safety flags
- README, roadmap, decision, extraction-plan, and current-state updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, adapters, hardware calls, physical-world behavior, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects

Recommended next lane:

- Phase 43.2 docs/tests/fixtures-only universal contract profile regression tests.

## Phase 43.2 Gate: Universal Contract Profile Regression Tests

Phase 43.2 adds regression tests over the Phase 43.1 universal profile fixture corpus using the existing `candidate_preview` helper.

Allowed:

- Phase 43.2 documentation
- Phase 43.2 fixture metadata
- Phase 43.2 tests using existing preview behavior only
- README, roadmap, decision, extraction-plan, and current-state updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, adapters, hardware calls, physical-world behavior, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects

Recommended next lane:

- Phase 43.3 docs/tests/fixtures-only universal contract hardening gap and next-lane review.

## Phase 43.3 Gate: Universal Contract Hardening Gap Review

Phase 43.3 reviews the Phase 43.0 through Phase 43.2 Universal Contract Fixture Hardening evidence.

Allowed:

- Phase 43.3 documentation
- Phase 43.3 fixture metadata
- Phase 43.3 tests
- README, roadmap, decision, extraction-plan, and current-state updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, adapters, hardware calls, physical-world behavior, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects

Recommended next lane:

- Phase 43.4 docs/tests/fixtures-only archive closeout.

## Phase 43.4 Gate: Universal Contract Hardening Archive / Closeout

Phase 43.4 archives Phase 43 as a completed docs/tests/fixtures-only Universal Contract Fixture Hardening lane.

Allowed:

- Phase 43.4 documentation
- Phase 43.4 fixture metadata
- Phase 43.4 tests
- README, roadmap, decision, extraction-plan, and current-state updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- approval enforcement, execution, dispatch, persistence, mutation, external calls, robotics, adapters, hardware calls, physical-world behavior, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects

Recommended next lane:

- Stop at the merge/tag approval gate for the Phase 43 stack.

## Phase 44.0 Gate: Typed IntentEnvelope Guardian Request Bridge Design Charter

Phase 44.0 opens a docs/tests/fixtures-only no-code design charter for the typed IntentEnvelope / Guardian Request Bridge.

Allowed:

- Phase 44.0 documentation
- Phase 44.0 inert fixture metadata
- Phase 44.0 tests
- README, roadmap, decision, extraction-plan, and current-state updates

Blocked:

- Runtime implementation
- `lima/` changes
- Sparkbot changes or wiring
- `tests/support/` changes
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- real IntentCompiler behavior
- real Guardian request behavior
- real GuardianDecision creation
- approval enforcement, execution, dispatch, persistence, mutation, external calls, model/tool/driver calls, robotics, adapters, hardware calls, physical-world behavior, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects

Required proof:

- raw natural language is not an execution surface
- typed intent is metadata, not authority
- Guardian request is not GuardianDecision
- approval state is owned by a future Guardian or policy membrane
- no `lima/` or `tests/support/` files are changed

Recommended next lane:

- Stop at review for Phase 44.0. Phase 44.1 fixture data requires Phil approval.

## Phase 32.4 Gate: Phase 32 Design Review Archive / Closeout

Phase 32.4 archives Phase 32 as a completed docs/tests/fixtures-only design review.

Allowed:

- Phase 32.4 tests
- Phase 32.4 fixture metadata
- Phase 32.4 documentation
- roadmap/state metadata updates

Decision:

- Phase 32 stops at the Phase 33 approval gate.
- Recommended Phase 33 direction is test-only `runtime_state` hardening.
- Recommended Phase 33 implementation file scope is empty.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior.

## Phase 32.3 Gate: Phase 33 Eligibility And Test Plan Matrix

Phase 32.3 defines the eligibility and test plan matrix for the recommended Phase 33 test-only hardening lane.

Allowed:

- Phase 32.3 tests
- Phase 32.3 fixture metadata
- Phase 32.3 documentation
- roadmap/state metadata updates

Decision:

- Phase 33 should be test-only `runtime_state` hardening.
- Phase 33 implementation file scope is empty.
- Phase 33 requires explicit Phil approval before beginning.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior.

## Phase 32.2 Gate: Next-Slice Safety And Scope Comparison

Phase 32.2 compares candidate lanes against safety, scope, testability, rollback, usefulness, and readiness.

Allowed:

- Phase 32.2 tests
- Phase 32.2 fixture metadata
- Phase 32.2 documentation
- roadmap/state metadata updates

Decision:

- Option A remains the safest immediate Phase 33 direction.
- Phase 33 runtime implementation is not recommended.
- Implementation file scope for recommended Phase 33 Option A is empty.

Forbidden:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- execution, approval enforcement, dispatch, audit persistence, external calls, background work, robotics, or physical-world behavior.

## Phase 20.5 Gate: Phase 20 Next Runtime Slice Design Lane Audit Archive / Closeout

Phase 20.5 may archive Phase 20 after a dedicated Phase 20.0 through Phase 20.4 audit.

Allowed:

- audit archive closeout documentation
- static audit archive fixture metadata
- static audit archive tests
- project tracking updates

Blocked:

- runtime implementation
- actual future acceptance-test implementation
- `lima/` changes
- `tests/support/` changes
- helper behavior changes
- Sparkbot wiring
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

Result:

Phase 20 is archived as no-code design only. Phase 21 remains gated and requires explicit Phil approval.

Stop for explicit Phil decision before Phase 21.

## Phase 9.5 Gate: First Runtime Slice Audit Archive / Closeout

Phase 9.5 may archive the completed first runtime slice after a dedicated Phase 9.0 through Phase 9.4 audit.

GO:

- list Phase 9.0 through Phase 9.4 as complete
- list only `lima/kernel/__init__.py` and `lima/kernel/intake_candidate.py` as approved runtime files touched
- document what Phase 9 added
- document what Phase 9 did not add
- preserve the Phase 8.1 test-update warning
- prove Phase 10 remains gated
- add static fixture and tests

NO-GO:

- new `lima/` changes
- `tests/support/` changes
- runtime behavior changes
- Sparkbot imports or wiring
- live adapter code
- HumanInput runtime bridge behavior
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- execution
- dispatch
- audit persistence
- shell, browser, network, file mutation, robot, or physical-world side effects

After merge:

Stop for explicit operator next-scope decision. No Phase 10 or runtime expansion is approved by this closeout.

## Phase 4.7 Gate: Non-production HumanInput Adapter Proposal Readiness Review

Phase 4.7 may review whether the Phase 4.6 HumanInput adapter proposal is clear, safe, constrained, and explicitly non-runtime enough before future adapter safety gate documentation.

GO only for:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- project tracking updates

NO-GO for:

- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

Required proof:

- fixture is valid JSON
- status is non-runtime readiness review
- review is docs/tests/fixtures only
- Phase 4.4 HumanInput fixture contract remains synthetic, inert, and non-runtime
- Phase 4.5 readiness review remains non-runtime
- Phase 4.6 adapter proposal remains non-runtime
- ready-for scope is limited to adapter safety gate docs or further non-runtime review
- tests pass

After merge:

- GO only for Phase 4.8 HumanInput Adapter Safety Gate Docs if Phase 4.7 recommends it

## Phase 4.8 Gate: HumanInput Adapter Safety Gate Docs

Phase 4.8 may define safety gate documentation for any future HumanInput adapter.

GO only for:

- HumanInput adapter safety gate documentation
- static safety gate fixture metadata
- static safety gate tests
- project tracking updates

NO-GO for:

- files under `lima/`
- live adapter code
- Sparkbot imports or wiring
- runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

Required proof:

- fixture is valid JSON
- status is non-runtime safety gate docs
- safety gate is docs/tests/fixtures only
- adapter output rule is HumanInput only
- blocked behavior list is explicit
- Phase 4.7 readiness review remains non-runtime
- tests pass

After merge:

- STOP for explicit operator approval before any next narrow non-production phase

## Phase 4.9 Gate: HumanInput Adapter Implementation Readiness Review

Phase 4.9 may review whether the HumanInput adapter boundary is ready for a future explicitly approved test-only adapter harness proposal while remaining not ready for live adapter code, production wiring, or runtime behavior.

GO only for:

- readiness review documentation
- static readiness review fixture metadata
- static readiness review tests
- project tracking updates

NO-GO for:

- files under `lima/`
- live adapter code
- test-only adapter harness code
- Sparkbot imports or wiring
- runtime behavior
- model calls
- tool execution
- terminal or PTY behavior
- robotics or physical-world behavior
- live auth/session/trust lookup
- real IntentCompiler
- real GuardianDecision
- approval, enforcement, execution, or audit persistence

Required proof:

- fixture is valid JSON
- status is non-runtime readiness review
- review is docs/tests/fixtures only
- no adapter or harness code is added
- Phase 4.4 HumanInput fixture contract remains synthetic, inert, and non-runtime
- Phase 4.8 safety gate remains non-runtime
- ready-for scope is limited to a future explicitly approved test-only adapter harness proposal or further non-runtime review
- tests pass

After merge:

- STOP for explicit operator approval before any next narrow non-production phase

## Phase 2.21: Guardian Request Test Design Review

No IntentEnvelope-to-Guardian-request fixtures until Phase 2.21 design review is merged.

After merge:

GO only for Phase 2.22 Guardian Request Test Fixtures.

NO-GO:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2.22: Guardian Request Test Fixtures

Guardian request test fixtures are allowed.

Still blocked:

- real GuardianDecision creation
- Guardian enforcement
- policy enforcement
- approval enforcement
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2.23: Guardian Request Fixture Readiness Review

No Guardian request fixture harness until Phase 2.23 readiness review is merged.

After merge:

GO only for Phase 2.24 Guardian Request Fixture Harness.

NO-GO:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2.24: Guardian Request Fixture Harness

Guardian request fixture harness is allowed for tests only.

Still blocked:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- real enforcement

## Phase 2.25: Guardian Request Harness Readiness Review

No Guardian-request-adjacent expansion until Phase 2.25 readiness review is merged.

After merge:

GO only for Phase 2.26 Guardian Request Safety Gate Docs.

NO-GO:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2.26: Guardian Request Safety Gate Docs

`docs/GUARDIAN_REQUEST_SAFETY_GATE.md` is now the standing gate for Guardian-request-adjacent work.

No Guardian-request-adjacent PR may merge without satisfying it.

Real GuardianDecision remains blocked.

## Phase 2.27: Guardian Request Safety Gate Readiness Review

Guardian-request safety-gate work may pause after Phase 2.27 if readiness decision approves.

After merge:

GO only for Phase 2.28 Fake GuardianDecision Test Design Review.

NO-GO:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement

## Phase 2: Extract Model Harness

Scope:

- Define the Intent Compiler boundary before extracting Harness execution paths so Sparkbot does not accidentally preserve raw chat-to-tool behavior.
- Extract model routing/fallback, tool catalogue, prompt cache, telemetry, and friendly error handling.
- Enforce tool-pack scoping.
- Preserve Sparkbot model behavior through parity tests.

Acceptance criteria:

- Public Harness APIs cannot execute tools without a Guardian decision or approval token.
- Shells declare allowed tool packs.
- Model calls are auditable events.
- Sparkbot model routing behavior is covered by parity tests.

## Phase 3: Extract Spine

Scope:

- Extract the process/task/event ledger, scheduler contracts, recurring jobs, audit writer, autonomous loop metadata, and lineage interfaces.
- Keep storage backend behind the persistence interface.

Acceptance criteria:

- Spine can append events and retrieve lineage through contracts.
- Approval state is represented in the ledger.
- Storage backend is replaceable.
- Sparkbot task/project/approval ledger behavior has parity coverage.

## Phase 4: Put Sparkbot On LIMA Runtime

Scope:

- Run Sparkbot as a shell on top of LIMA Runtime.
- Replace direct internal runtime calls with contract-backed adapters.
- Keep Sparkbot product behavior unchanged.

Acceptance criteria:

- Sparkbot parity tests pass.
- Tool policy decisions, pending approvals, model calls, audit events, memory events, and Spine events match current behavior.
- Operators retain existing approval and breakglass controls.

## Phase 5: Integrate Robo-OS As Guardian-Gated Driver

Scope:

- Treat LIMA Robo-OS as a driver/runtime layer.
- Register robotics capabilities, telemetry requirements, dry runs, and approval requirements.
- Use MCP for robot/device tool boundaries.

Acceptance criteria:

- Simulation and dry-run commands can be planned without physical execution.
- Medium/high/unknown physical-world commands require Guardian approval.
- Real hardware motion is blocked by default until approval workflow and audit evidence are complete.
- Emergency stop remains available and audited.

## Phase 6: Arc, LIMA AI Office, And SparkPit Shells

Scope:

- Integrate Arc / LIMA AI Office, SparkPit web systems, office bots, automation agents, and future robot shells as LIMA Runtime consumers.
- Each shell declares tool packs and permissions.

Acceptance criteria:

- Shells consume shared runtime contracts.
- Shell-specific permissions are enforced by Guardian.
- Tool packs are scoped per shell.
- Runtime audit and lineage remain consistent across shells.

## Extraction Risks

- Sparkbot Guardian improvements are moving faster than earlier Guardian Suite extraction work.
- Existing Guardian Suite code shows useful module boundaries but still has Sparkbot app coupling.
- Robo-OS has real physical-world execution surfaces; integration must default to dry-run, simulation, and explicit Guardian approval.
- Tool catalogues can grow beyond safe model context; tool-pack scoping is required.

## Phase 2.28 Gate: Fake GuardianDecision Test Design Review

No fake GuardianDecision fixtures until Phase 2.28 design review is merged.

After merge:

GO only for Phase 2.29 Fake GuardianDecision Test Fixtures.

NO-GO:

- real GuardianDecision creation
- real Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- production Sparkbot wiring
- real enforcement
