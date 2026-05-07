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
