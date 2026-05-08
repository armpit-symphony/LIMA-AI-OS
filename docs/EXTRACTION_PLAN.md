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
