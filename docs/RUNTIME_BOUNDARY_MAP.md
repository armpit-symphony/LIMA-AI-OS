# Runtime Boundary Map

## Purpose

This map translates current Sparkbot, LIMA Guardian Suite, and LIMA Robo-OS surfaces into future LIMA Runtime boundaries.

It does not migrate code. It does not authorize extraction. It identifies what can later become runtime contracts, shell adapters, drivers, services, or do-not-extract-yet areas.

Sparkbot remains the parity source. LIMA Runtime must preserve user-facing behavior through contracts, not preserve unsafe internal shortcuts. Robo-OS is a Guardian-gated driver/runtime integration, not a competing brain.

## Reference Commits Inspected

| Repo | Branch | Commit | Inspection notes | Modified? |
| --- | --- | --- | --- | --- |
| Sparkbot | `origin/main` | `129eab05b37b5d3fb6b078b4218b0dca7f6d993b` | Inspected read-only through fetched `origin/main`. Local worktree stayed on `main` and was behind origin. Recent delta touched model/provider save paths and `llm.py`; core chat/tool coupling still requires boundary gates. | No |
| LIMA-Guardian-Suite | `origin/main` | `0559d9a6ce7e3dc401185a6732a6c8fa123db477` | Inspected read-only through fetched `origin/main`. Local checkout has pre-existing untracked cache/data and is ahead one local commit; this pass used `origin/main` only. | No by this pass |
| LIMA-Robo-OS | `origin/main` | `d6f8edc7423e72343d0e4778fb7555b96beed288` | Inspected read-only through fetched `origin/main`. Local status has a pre-existing Git LFS clean/filter issue on `data/.lfs/unitree_go2_bigoffice.tar.gz`; this pass used `origin/main` only. | No by this pass |

## Classification Types

SHELL_ADAPTER:

- UI/product shell, frontend, Tauri, desktop launcher, Workstation, SparkPit web surfaces.

HUMAN_INPUT_ADAPTER:

- Chat, voice transcript, console/operator commands, meeting prompts, future mobile/gesture input.

INTENT_BOUNDARY:

- Anything that should become `HumanInput -> IntentEnvelope -> GuardianDecision`.

GUARDIAN_CONTRACT:

- Policy, auth, vault, approval, breakglass, verifier, permission, risk, decision logic.

HARNESS_CONTRACT:

- Model routing, fallback, completion, prompt cache, model telemetry, selected tools, tool planning.

TOOL_PACK_CANDIDATE:

- Any tool or skill that must be grouped into deny-by-default packs.

POLICY_CANDIDATE:

- Risk/approval/pack policy logic.

APPROVAL_CANDIDATE:

- Operator PIN, confirmation, breakglass, approval evidence.

SPINE_AUDIT_CANDIDATE:

- Task ledger, events, audit, lineage, project/task status, scheduled/autonomous records.

PRIVACY_REDACTION_CANDIDATE:

- Secrets, prompts, transcripts, tool args/results, terminal output, sensor data, memory refs.

DRIVER_CANDIDATE:

- Robo-OS, browser, filesystem, network, terminal, sensors, robot/device integrations.

SYSTEM_SERVICE:

- Skills runtime, comms, voice, meeting manager, task/project services.

PERSISTENCE_CANDIDATE:

- SQLite, Postgres, vault DB, task DB, memory DB, audit store.

DO_NOT_EXTRACT_YET:

- Code that violates Phase 0 gates, mixes shell/runtime/execution, exposes full tool catalogue, or lacks `decision_id`/privacy lineage.

DEPRECATED_OR_UNSAFE_SHORTCUT:

- Raw chat-to-tool, direct terminal execution, direct robot command from natural language, direct model/tool execution without `GuardianDecision`.

UNKNOWN:

- Needs more inspection.

## Boundary Matrix

| Current repo | Current path / surface | Current role | Boundary classification | Future LIMA location | Required contracts before extraction | Risk level | Extraction status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sparkbot | `backend/app/api/routes/chat/messages.py` | Stores room chat messages. | HUMAN_INPUT_ADAPTER | Sparkbot shell adapter | HumanInput, privacy metadata, audit lineage | medium | ready_for_adapter_design | Chat persistence is input evidence, not execution authority. |
| Sparkbot | `backend/app/api/routes/chat/websocket.py` | Real-time room chat input and broadcast. | HUMAN_INPUT_ADAPTER | Sparkbot shell adapter | HumanInput, IntentEnvelope, lineage | medium | ready_for_adapter_design | WebSocket messages should emit `HumanInput` before model/tool routing. |
| Sparkbot | `backend/app/api/routes/chat/voice.py` | Audio transcription and tool-aware bot response path. | HUMAN_INPUT_ADAPTER / PRIVACY_REDACTION_CANDIDATE | Voice service adapter | HumanInput, transcript_ref, transcript confidence, privacy classes, IntentEnvelope | high | needs_privacy_review | Voice must normalize like text and carry transcript confidence; raw transcript persistence needs redaction review. |
| Sparkbot | `backend/app/api/routes/chat/llm.py::stream_chat_with_tools` | Chat, model routing, selected tools, Guardian policy, pending approvals, and tool execution are close together. | DEPRECATED_OR_UNSAFE_SHORTCUT | Split between Sparkbot adapter, Intent boundary, Harness, ToolPack, Guardian, Spine | HumanInput, IntentEnvelope, GuardianDecision, ToolPackScope, ApprovalMetadata, lineage, redaction/privacy | critical | do_not_extract_yet | Direct extraction would preserve raw chat/model/tool coupling. Preserve behavior through gated adapters. |
| Sparkbot | `backend/app/api/routes/chat/llm.py::_select_tool_definitions` | Chooses tool definitions for the model context. | HARNESS_CONTRACT / TOOL_PACK_CANDIDATE | LIMA Harness tool shortlist | ShellToolScope, ToolExposureDecision, ToolPackRiskPolicy, decision_id | high | needs_pack_classification | Harness must receive selected tools only, never the full catalogue. |
| Sparkbot | `backend/app/api/routes/chat/model.py` | Model settings, provider routing, agent config, model telemetry endpoints. | HARNESS_CONTRACT / POLICY_CANDIDATE | LIMA Harness plus Sparkbot settings adapter | GuardianDecision for consequential model calls, model_context_ref, lineage | high | needs_contract_review | Recent provider changes are Sparkbot behavior evidence, not kernel implementation. |
| Sparkbot | `backend/app/api/routes/chat/tools.py` | Broad static tool catalogue and dispatcher. | TOOL_PACK_CANDIDATE | ToolPack manifests and driver/tool adapters | ToolPack scoping, risk policy, decision_id, selected_tools audit, privacy classes | critical | needs_pack_classification | Full-catalogue exposure is do-not-extract-yet. |
| Sparkbot | `backend/skills/`, `backend/app/services/skills.py`, `backend/app/services/skill_executor.py` | Dynamic skills and fallback execution registry. | TOOL_PACK_CANDIDATE / SYSTEM_SERVICE | Skills service plus ToolPack manifests | Dynamic skill policy, unknown denied by default, exposure_id, execution_id | high | needs_pack_classification | `SPARKBOT_SKILLS_DIR`, `_register_extra()`, and fallback names cannot self-authorize. |
| Sparkbot | `backend/app/services/mcp_registry.py` | MCP manifests, health, explain plans, dry-run/approval metadata. | TOOL_PACK_CANDIDATE / POLICY_CANDIDATE | Driver/tool registry contract | ToolPack manifest, GuardianDecision, ApprovalMetadata, lineage | medium | ready_for_adapter_design | Good plan-before-execute reference if kept contract-level. |
| Sparkbot | `backend/app/api/routes/chat/mcp.py`, `backend/app/services/mcp_runs.py` | Durable MCP explain-plan and approval state. | APPROVAL_CANDIDATE / SPINE_AUDIT_CANDIDATE | Approval and Spine adapter | GuardianDecision, ApprovalMetadata, lineage, privacy metadata | medium | ready_for_adapter_design | Approve/deny routes do not execute tools in inspected path. |
| Sparkbot | `backend/app/api/routes/chat/guardian.py` | Breakglass and vault endpoints. | GUARDIAN_CONTRACT / APPROVAL_CANDIDATE / PRIVACY_REDACTION_CANDIDATE | Guardian control plane with Sparkbot adapter | GuardianDecision, ApprovalMetadata, secret_ref, breakglass scope, audit lineage | critical | needs_contract_review | Vault writes/deletes are privileged; raw secrets must not enter audit. |
| Sparkbot | `backend/app/services/guardian/*` | Policy, auth, executive guard, verifier, pending approvals, token routing, memory, vault, Spine helpers. | GUARDIAN_CONTRACT | Guardian core plus Sparkbot adapter | Decoupled imports, GuardianDecision, ApprovalMetadata, PrivacyProtocol, lineage | high | needs_contract_review | Useful source of truth but currently tied to Sparkbot app/persistence assumptions. |
| Sparkbot | `backend/app/api/routes/chat/dashboard.py` | Dashboard approvals and approved callback execution. | SHELL_ADAPTER / APPROVAL_CANDIDATE | Sparkbot approval UX adapter | ApprovalMetadata, GuardianDecision, selected_tools, lineage | high | needs_decision_gate | Approval UI must produce durable decision/approval evidence before callbacks execute. |
| Sparkbot | `backend/app/api/routes/chat/spine.py` | Task, event, queue, handoff, approval, and lineage views. | SPINE_AUDIT_CANDIDATE | Spine adapter/read model | AuditLineageRecord, SpineEvent, privacy fields | medium | ready_for_adapter_design | Strong reference for audit views; storage implementation remains future work. |
| Sparkbot | `backend/app/api/routes/chat/audit.py`, `app.crud.create_audit_log` callers | Audit log writes and views. | SPINE_AUDIT_CANDIDATE / PRIVACY_REDACTION_CANDIDATE | Audit adapter | decision_id, lineage_id, redaction/privacy refs | high | needs_lineage_mapping | Raw prompts/tool output/terminal output must be referenced or summarized. |
| Sparkbot | `backend/app/api/routes/terminal.py`, `backend/app/services/terminal_service.py` | Raw terminal/PTY sessions and streams. | DRIVER_CANDIDATE / DEPRECATED_OR_UNSAFE_SHORTCUT | Terminal driver adapter | critical risk, decision_id, ApprovalMetadata, redaction-safe output, lineage | critical | do_not_extract_yet | Route comments indicate raw shell behavior; no kernel extraction until gated. |
| Sparkbot | `terminal_send` in `backend/app/api/routes/chat/tools.py` | Model-reachable terminal send tool. | DRIVER_CANDIDATE / DO_NOT_EXTRACT_YET | Terminal ToolPack plus driver | ToolPack scoping, critical approval, decision_id, terminal output refs | critical | do_not_extract_yet | Must not survive as chat-to-terminal shortcut. |
| Sparkbot | Browser tools in `backend/app/api/routes/chat/tools.py` | Browser open/navigate/snapshot/click/form/session actions. | DRIVER_CANDIDATE / TOOL_PACK_CANDIDATE | Browser driver ToolPack | browser pack risk policy, decision_id, privacy refs, selected_tools | high | needs_pack_classification | Split read-only snapshot from state-changing click/form actions. |
| Sparkbot | File/network/comms/calendar tools in `tools.py` and `backend/skills/*` | Drive, OneDrive, uploads, external APIs, email, Slack, Gmail, calendar, contacts. | TOOL_PACK_CANDIDATE / DRIVER_CANDIDATE | Files/network/comms/calendar ToolPacks | action-level risk, approval metadata, evidence refs, privacy refs | high | needs_pack_classification | Mixed read/write packs must be classified per action. |
| Sparkbot | `backend/app/api/routes/chat/robotics.py` | Robot status, tool listing, command, emergency stop. | DRIVER_CANDIDATE / SPINE_AUDIT_CANDIDATE | Robo-OS driver adapter | typed intent, GuardianDecision, ApprovalMetadata, robot action lineage, safety/privacy | critical | needs_decision_gate | Physical-world paths require explicit safety gates; emergency stop stays audited. |
| Sparkbot | `backend/app/services/lima_robotics_bridge.py` | Natural-language robot command to MCP tool planning. | DEPRECATED_OR_UNSAFE_SHORTCUT / DRIVER_CANDIDATE | Robo-OS driver planning adapter | IntentEnvelope before command planning, GuardianDecision, dry-run metadata, robot lineage | critical | do_not_extract_yet | Raw natural language to robot MCP command path must not become kernel behavior. |
| Sparkbot | Meeting / roundtable paths: `MeetingRoomPage.tsx`, `workstationMeeting.ts`, `docs/architecture/roundtable_meeting_flow_v1.6.60.md` | Meeting UX, meeting prompts, roundtable behavior, artifacts. | HUMAN_INPUT_ADAPTER / SYSTEM_SERVICE | Meeting system service plus shell adapter | HumanInput vs SystemService classification, transcript_ref, privacy, lineage | medium | needs_contract_review | Meeting prompts can be human input or service events depending source. |
| Sparkbot | SparkBud / Workstation: `frontend/src/pages/WorkstationPage.tsx`, `backend/app/api/routes/chat/workstation.py` | Workstation shell, MCP control plane, approvals, terminal/meeting surfaces. | SHELL_ADAPTER | Sparkbot shell manifest and adapters | ShellManifest, tool-pack declarations, ApprovalMetadata, privacy metadata | high | ready_for_adapter_design | Shell can preserve UX while runtime owns policy. |
| Sparkbot | Frontend chat shell: `frontend/src/components/chat/*`, `frontend/src/pages/ChatPage.tsx` | Chat UI and stream rendering. | SHELL_ADAPTER / HUMAN_INPUT_ADAPTER | Sparkbot shell adapter | HumanInput, ShellManifest, privacy metadata | medium | ready_for_adapter_design | UI should not own runtime policy. |
| Sparkbot | Desktop/Tauri: `src-tauri/src/main.rs`, `src-tauri/tauri.conf.json`, local launcher surfaces | Desktop shell and local runtime launcher. | SHELL_ADAPTER | Sparkbot desktop shell manifest | ShellManifest, local permission declaration, tool packs | medium | ready_for_adapter_design | Do not extract launcher assumptions into kernel. |
| Sparkbot | Bot bridges: Telegram, Discord, WhatsApp, GitHub bridge services/routes | External message ingress and send surfaces. | HUMAN_INPUT_ADAPTER / TOOL_PACK_CANDIDATE | Comms service adapter | actor identity, shell_id, comms policy, approval metadata | high | needs_contract_review | Inbound vs outbound action must be separated. |
| LIMA-Guardian-Suite | `app/services/guardian/auth.py` | PIN verification and privileged sessions, imports Sparkbot `ChatUser`. | GUARDIAN_CONTRACT / APPROVAL_CANDIDATE | Guardian auth contract plus Sparkbot adapter | ApprovalMetadata, privacy rules, decoupled identity adapter | critical | needs_contract_review | Sparkbot app/model coupling must be removed before extraction. |
| LIMA-Guardian-Suite | `app/services/guardian/policy.py` | Tool policy decisions including vault and breakglass requirements. | POLICY_CANDIDATE / GUARDIAN_CONTRACT | Guardian policy core | GuardianDecision, ToolPackRiskPolicy, PolicyDecision | high | needs_contract_review | Useful policy source; must not execute or expand tool scope. |
| LIMA-Guardian-Suite | `app/services/guardian/pending_approvals.py` | SQLite pending approval storage. | APPROVAL_CANDIDATE / PERSISTENCE_CANDIDATE | Approval protocol plus persistence interface | ApprovalMetadata, StorageProtocol, expiry/revocation, lineage | high | needs_contract_review | Storage implementation is not extracted in Phase 0. |
| LIMA-Guardian-Suite | `app/services/guardian/vault.py`, `guardian/vault.py` | Vault DB and encrypted secret operations. | GUARDIAN_CONTRACT / PRIVACY_REDACTION_CANDIDATE / PERSISTENCE_CANDIDATE | Guardian vault contract plus secret_ref adapter | secret_ref only, no raw audit secrets, ApprovalMetadata, breakglass | critical | needs_privacy_review | Raw secret values must never become audit payloads. |
| LIMA-Guardian-Suite | `app/services/guardian/task_guardian.py` | Scheduled tasks, internal tool execution, audit, verifier. | SPINE_AUDIT_CANDIDATE / SYSTEM_SERVICE / DO_NOT_EXTRACT_YET | Task service plus Spine adapter | decision inheritance, approval renewal, exposure_id, execution_id, lineage | high | needs_lineage_mapping | Imports Sparkbot CRUD/models and executes internal tools; cannot extract directly. |
| LIMA-Guardian-Suite | `app/services/guardian/meeting_recorder.py` | Meeting transcript notes and LLM call, imports Sparkbot CRUD/models. | SYSTEM_SERVICE / PRIVACY_REDACTION_CANDIDATE | Meeting service adapter | transcript_ref, model_context_ref, privacy, decoupled persistence | high | needs_privacy_review | Raw transcripts/model prompts need redaction handling before persistence. |
| LIMA-Guardian-Suite | `app/services/guardian/token_guardian.py`, `tokenguardian/*` | Model routing, usage monitoring, token policy. | HARNESS_CONTRACT / POLICY_CANDIDATE | Harness routing policy | GuardianDecision for costly/private calls, telemetry lineage | medium | ready_for_adapter_design | Good candidate for contract-backed model routing after decoupling. |
| LIMA-Guardian-Suite | `app/services/guardian/verifier.py` | Verifies high-risk tool/task runs. | GUARDIAN_CONTRACT / POLICY_CANDIDATE | Guardian verifier contract | GuardianDecision, ApprovalMetadata, ToolPackRiskPolicy | high | needs_contract_review | Verifier should produce policy evidence, not execute. |
| LIMA-Guardian-Suite | `guardian/*` standalone modules | Earlier standalone Guardian, memory, token, task, vault modules. | UNKNOWN / GUARDIAN_CONTRACT | Reference only until reviewed | Contract parity review, privacy rules, storage boundary | unknown | unknown | Older shape may lag Sparkbot behavior. |
| LIMA-Robo-OS | `AGENTS.md`, `README.md` CLI/MCP surfaces | Agentic robot runtime, CLI, MCP tools, direct skill calls, hardware/simulation runs. | DRIVER_CANDIDATE / SHELL_ADAPTER | Robo shell and driver integration | ShellManifest, ToolPack scoping, GuardianDecision, ApprovalMetadata, safety/privacy | critical | needs_decision_gate | Current CLI/MCP can call skills; LIMA must gate physical actions. |
| LIMA-Robo-OS | `lima/agents/mcp/*` | MCP server/client/adapters exposing skills as tools. | DRIVER_CANDIDATE / TOOL_PACK_CANDIDATE | MCP driver/tool boundary | ToolPack manifests, selected_tools, decision_id, lineage | high | needs_pack_classification | MCP is the right boundary but not authorization by itself. |
| LIMA-Robo-OS | `lima/agents/agent.py`, `lima/agents/*` | LLM agent modules, prompts, tool planning. | HARNESS_CONTRACT / DO_NOT_EXTRACT_YET | Harness reference only | no full catalogue, decision_id, prompt privacy refs | high | needs_decision_gate | In-process agent behavior cannot bypass Guardian. |
| LIMA-Robo-OS | `lima/robot/unitree/unitree_skill_container.py` | Go2 robot skills: relative movement and sport commands. | DRIVER_CANDIDATE / TOOL_PACK_CANDIDATE | Robo driver ToolPack | typed intent, GuardianDecision, ApprovalMetadata, dry-run/sim, robot lineage | critical | needs_approval_metadata | Movement/manipulation is physical-world critical risk. |
| LIMA-Robo-OS | `lima/control/*` | Control tasks, hardware interface, tick loop, teleop, trajectories. | DRIVER_CANDIDATE | Robo driver runtime | safety constraints, decision_id, approval metadata, telemetry evidence | critical | needs_decision_gate | Driver capabilities can be wrapped later; no direct kernel extraction. |
| LIMA-Robo-OS | `lima/robot/unitree/go2/*`, `lima/robot/unitree/g1/*`, `lima/robot/unitree/*connection*` | Unitree hardware/sim/replay connections. | DRIVER_CANDIDATE | Robo-OS driver adapter | dry-run/simulation metadata, hardware capability manifest, safety/privacy | critical | needs_approval_metadata | Real hardware motion must remain blocked until approvals and audit are complete. |
| LIMA-Robo-OS | `lima/perception/*`, `lima/msgs/sensor_msgs/*`, `lima/robot/unitree/type/lidar.py`, odometry/map modules | Camera, lidar, odometry, sensor streams, maps, temporal memory. | DRIVER_CANDIDATE / PRIVACY_REDACTION_CANDIDATE | Sensor driver adapter and privacy boundary | sensor_ref, SAFETY_CRITICAL/BIOMETRIC classes, retention/visibility rules | high | needs_privacy_review | Sensor data may include biometric/private physical-world context. |
| LIMA-Robo-OS | `lima/perception/experimental/temporal_memory/*` | Persistent visual/temporal memory, raw VLM logs, SQLite/JSONL. | PRIVACY_REDACTION_CANDIDATE / PERSISTENCE_CANDIDATE | Future memory/sensor adapter | redaction/privacy, model_context_ref, sensor_ref, StorageProtocol | high | needs_privacy_review | Raw VLM/sensor memory cannot be logged without privacy review. |
| LIMA-Robo-OS | `docker/navigation/*`, `.github/workflows/*`, `bin/*` | Navigation stacks, hardware env, build/deploy/test tooling. | SYSTEM_SERVICE / DRIVER_CANDIDATE | Deployment/runtime ops reference | deploy policy, terminal/system pack policy, no production wiring | critical | do_not_extract_yet | Ops scripts are not runtime contracts. |

## Phase Gate Checklist

Before extracting chat/tool path:

- HumanInput contract
- IntentEnvelope contract
- `GuardianDecision.decision_id`
- ToolPack scoping
- ToolPack risk policy
- Approval metadata for high/critical
- Spine/Audit lineage
- Redaction/privacy

Before extracting terminal/PTY:

- critical risk classification
- decision_id
- approval metadata
- redaction-safe output handling
- lineage events
- no raw secrets in audit

Before extracting Robo-OS:

- typed intent
- GuardianDecision
- approval metadata
- dry-run/simulation metadata where available
- safety/privacy defaults
- robot action lineage
- sensor redaction/privacy

Before extracting model harness:

- selected_tools only
- no full catalogue
- decision_id for consequential calls
- prompt/context privacy refs
- model telemetry lineage

Before extracting dynamic skills:

- pack classification
- risk policy
- unknown denied by default
- exposure_id
- execution_id
- selected_tools audit

Before extracting Guardian Suite:

- remove Sparkbot app/crud/model coupling
- preserve GuardianDecision contract
- preserve ApprovalMetadata contract
- preserve Vault/Auth privacy rules
- verify no runtime bypass

## Do-Not-Extract-Yet List

- `stream_chat_with_tools` as direct extraction target
- raw chat-to-tool shortcut
- full-catalogue tool exposure
- terminal/PTY direct execution path
- raw natural language to robot MCP command path
- dynamic `SPARKBOT_SKILLS_DIR` without pack classification
- `execute_tool` fallback names without classification
- audit logging of raw secrets/prompts/tool outputs/terminal output
- Guardian Suite modules that import Sparkbot `app.crud`, `app.models`, or route services without adapters
- Robo-OS direct MCP/skill calls that can move hardware without `GuardianDecision` and approval metadata

## Future Adapter Plan

1. Sparkbot chat adapter emits HumanInput.
2. IntentCompiler creates IntentEnvelope.
3. Guardian evaluates ConsequentialActionRequest.
4. ApprovalMetadata attaches if required.
5. ToolPackScope produces ToolExposureDecision.
6. Harness receives selected_tools only.
7. Execution emits Spine/Audit events with privacy metadata.
8. Sparkbot preserves user-facing behavior without preserving unsafe internal shortcuts.

## Ready For Adapter Design

- Sparkbot chat message and WebSocket surfaces as `HumanInput` adapters.
- Sparkbot frontend chat, Workstation, and desktop/Tauri surfaces as shell adapters.
- Sparkbot MCP explain-plan/run approval surfaces as approval/audit adapter references.
- Sparkbot Spine view surfaces as audit/read-model references.
- Guardian Suite token routing as Harness policy reference after decoupling.

## Unresolved Risks

- Sparkbot `origin/main` moved beyond prior inventories and should be rechecked before Phase 1 extraction.
- Guardian Suite still has Sparkbot app/model/CRUD coupling and local persistence assumptions.
- Robo-OS worktree has a local Git LFS status issue; this map inspected `origin/main` but did not clean or modify the repo.
- Robo-OS exposes direct CLI/MCP/skill paths for robot actions; LIMA must add Guardian gates before using those paths.
- Privacy implementation is intentionally absent; no audit persistence should store raw prompts, transcripts, tool outputs, terminal output, or sensor data.

## Recommended Next Step

Recommended next branch: `phase-0-15-extraction-readiness-review`.

Goal: perform a final Phase 0 readiness review and produce a Phase 1 extraction order.
