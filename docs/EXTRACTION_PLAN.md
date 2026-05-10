# Extraction Plan

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
