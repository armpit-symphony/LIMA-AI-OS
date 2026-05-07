# Sparkbot Entrypoint Inventory

## Purpose

This inventory identifies current Sparkbot entrypoints that may later adapt into LIMA Runtime. It does not migrate code, copy implementation, or define adapters. It exists to prevent accidental extraction of raw chat-to-tool shortcuts into the LIMA Kernel.

Sparkbot remains the spec. LIMA Runtime must preserve Sparkbot behavior through contracts, not preserve unsafe internal shortcuts. Future extraction must map current paths into:

`HumanInput -> IntentCompiler -> IntentEnvelope -> GuardianDecision -> Harness / Tool / Driver -> Spine / Audit event`

Inspected reference: Sparkbot `origin/main` at `f3c098056518dedec42f6452dec6e24ccdb1e309`. The local checkout was on `main` at `9f68de2d14e59391b9c65b5d7cd6c0da6d8d089f` and behind `origin/main` by one commit; this inventory uses fetched `origin/main` read-only.

Freshness check: the `9f68de2d14e59391b9c65b5d7cd6c0da6d8d089f..f3c098056518dedec42f6452dec6e24ccdb1e309` delta touched chat message/search routes, chat WebSocket cleanup, terminal WebSocket database cleanup, Guardian auth lockout cleanup, upload handling, and public safety tests/docs. No relevant delta changed the core `stream_chat_with_tools()` chat/model/tool coupling, voice-to-tool-aware-chat path, tool catalogue/executor shape, robotics bridge command path, MCP planning/approval shape, or raw PTY classification.

## Scope

This pass inspected current Sparkbot surfaces for:

- chat input
- voice/transcript input
- meeting / roundtable input
- SparkBud/workstation actions
- API routes
- WebSocket routes
- model harness calls
- tool catalogue / tool execution
- Guardian approval, breakglass, vault, policy, verifier, and token routing paths
- terminal/shell/PTY paths
- filesystem/browser/network paths
- task/spine/audit/event logging paths
- desktop/Tauri/local launcher paths
- docs/scripts that shape product behavior

No Sparkbot files were modified.

## Inventory Table

| Area | Current Sparkbot file/path | Current role | Entry type | Side-effect risk | Current Guardian involvement | Future LIMA mapping | Extraction concern | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REST chat messages | `backend/app/api/routes/chat/messages.py` | Stores chat messages through room-scoped HTTP routes. | HumanInput | low | Auth and membership checks; no LIMA `IntentEnvelope` boundary observed. | HumanInput adapter | Chat persistence must not become execution authorization. | POST creates human messages and may create bot messages for some flows. |
| Chat WebSocket | `backend/app/api/routes/chat/websocket.py` | Real-time room chat input, broadcast, and persistence. | HumanInput | medium | Auth and room membership checks; no typed intent boundary observed. | HumanInput adapter / Shell manifest | WebSocket message receipt should emit `HumanInput` before model or tool routing. | `origin/main` includes security/cleanup hardening; this remains a shell boundary candidate. |
| Voice message route | `backend/app/api/routes/chat/voice.py` | Audio transcription and streaming bot response. | HumanInput | high | File notes say transcribed text enters `stream_chat_with_tools()` so existing policy/tool/Guardian logic fires identically. | HumanInput adapter | Voice transcript must not bypass Intent Compiler; transcript confidence should be preserved. | Voice should normalize into same contract as text. |
| Voice transcription-only route | `backend/app/api/routes/chat/voice.py` | Returns transcript without immediately streaming tool-aware response. | HumanInput | low | Auth and membership checks. | HumanInput adapter | Useful future capture path if transcript confidence is attached. | Safer than immediate voice-to-stream path. |
| Model/tool streaming loop | `backend/app/api/routes/chat/llm.py` | Routes messages to model, selects tools, receives tool calls, applies Guardian policy, streams tool results. | ModelCall / ToolCall | high | Uses Token Guardian routing, policy decisions, pending approvals, verifier, executive guarded execution, audit logging. | Harness contract / GuardianDecision gate | High-priority extraction risk: raw message and model output are close to tool execution. | Current loop calls `guardian_suite.policy.decide_tool_use()` before guarded execution, but LIMA needs `IntentEnvelope` and durable `GuardianDecision` IDs before this layer. |
| Global operation prompt | `backend/app/api/routes/chat/llm.py` | Instructs model to use tools proactively for live data, shell, browser, Gmail, GitHub, Slack, calendar, and terminal tasks. | ModelCall | high | Prompt includes approval language for some write actions and secrets boundaries. | Harness policy context | Potential shortcut: prompt pressure can encourage model-to-tool execution before typed intent exists. | Needs future separation of user intent, planning, and execution authority. |
| Tool catalogue and executors | `backend/app/api/routes/chat/tools.py` | Defines tool manifests and dispatches tool names to implementation functions. | ToolCall | critical | Some tools call Guardian Vault or rely on Guardian policy decisions upstream. | ToolPack declaration / Tool contract | Large mixed catalogue can expose too many capabilities at once. | Includes browser, terminal, GitHub, Slack, Gmail, calendar, vault, memory, Task Guardian, and robot tools. |
| Browser tools | `backend/app/api/routes/chat/tools.py` | Opens/navigates browser sessions, snapshots pages, fills fields, clicks, saves/restores sessions. | DriverCommand | high | URL guardrails block localhost/private targets; execution appears tool-policy-gated upstream. | Driver contract / browser ToolPack | Interactive browser actions need explicit risk classes and approval policy. | Future adapter must distinguish read-only browse from form submission/click side effects. |
| Terminal tool | `backend/app/api/routes/chat/tools.py` | Sends text to a running terminal session through `terminal_send`. | ShellAction | critical | Expected to be gated by upstream Guardian policy; terminal itself is raw PTY. | Driver contract / terminal ToolPack / GuardianDecision gate | Terminal input is a high/critical side-effect surface and cannot inherit chat-to-terminal shortcuts. | Requires explicit high/critical risk handling and audit linkage. |
| Terminal HTTP/WebSocket API | `backend/app/api/routes/terminal.py` | Creates/list/deletes PTY sessions and streams terminal input/output. | ShellAction | critical | Route comments say command-level filtering is not enforced and this is a raw shell. | Driver contract / Shell manifest | Direct terminal route must remain shell-specific until LIMA has GuardianDecision-enforced terminal driver contracts. | `origin/main` hardens DB cleanup; raw PTY classification remains critical. |
| Terminal service | `backend/app/services/terminal_service.py` | Manages Windows ConPTY and POSIX PTY subprocess sessions. | SystemAction | critical | No command-level Guardian boundary observed inside service. | Driver contract | Runtime extraction must not move raw PTY management into kernel without gating. | Supports PowerShell/cmd/pwsh and POSIX shells. |
| MCP registry | `backend/app/services/mcp_registry.py` | Defines MCP manifests, health, policy explain plans, dry-run/approval metadata. | ToolPack declaration | medium | Builds policy simulations and approval requirements; notes that explain plan never executes tools. | ToolPack declaration / GuardianDecision candidate | Good reference for plan-before-execute boundary. | Should be adapted after Intent/Guardian decision contracts are durable. |
| MCP routes/runs | `backend/app/api/routes/chat/mcp.py`, `backend/app/services/mcp_runs.py` | Creates durable MCP explain plans and approval records; approve/deny routes do not execute tools. | ApprovalRequest / AuditEvent | medium | Approval requires Guardian operator identity; actions write audit logs. | GuardianDecision gate / Spine event | Good extraction candidate after Guardian decision ID contract. | Needs linkage to `IntentEnvelope.intent_id`. |
| Guardian breakglass and vault routes | `backend/app/api/routes/chat/guardian.py` | Operator-only breakglass and encrypted vault management. | ApprovalRequest / SystemAction | critical | Breakglass, operator checks, vault service, and audit logging are present. | Guardian control plane | Must not be treated as ordinary tools. | Vault writes/deletes require privileged breakglass mode in inspected route text. |
| Guardian services | `backend/app/services/guardian/*` | Policy, auth, executive guard, verifier, pending approvals, token routing, memory, vault, and Spine helpers. | ApprovalRequest / AuditEvent | high | Guardian is active across policy, approvals, verifier, vault, token routing, and memory. | Guardian contracts | Current services still have Sparkbot app coupling and local persistence assumptions. | `origin/main` includes auth lockout cleanup; extract only after entrypoints and decision IDs are contract-aligned. |
| Dashboard approvals | `backend/app/api/routes/chat/dashboard.py` | Surfaces pending approvals and executes approved tool callbacks. | ApprovalRequest / ToolCall | high | Reads pending approvals and uses guarded tool execution paths. | GuardianDecision UX / Shell | Approval UI must produce durable Guardian decisions, not just transient confirmation IDs. | Future LIMA shell adapter candidate. |
| Spine routes | `backend/app/api/routes/chat/spine.py` | Exposes task, event, handoff, approval, queue, and lineage views. | AuditEvent | low | Spine tracks approval states and task lineage. | Spine event | Must link future events to `HumanInput`, `IntentEnvelope`, and `GuardianDecision`. | Strong reference for audit/event shape. |
| Audit route and CRUD audit logs | `backend/app/api/routes/chat/audit.py`, `app.crud.create_audit_log` callers | Records policy decisions, tool runs, MCP actions, robotics actions, breakglass/vault actions. | AuditEvent | low | Many Guardian paths write audit logs. | Spine / Audit event | Missing LIMA-wide decision IDs and intent IDs in current pattern. | Extraction should unify audit lineage. |
| Robotics API | `backend/app/api/routes/chat/robotics.py` | Robot status, tool listing, command, and emergency stop endpoints. | DriverCommand | critical | Audits robotics commands; bridge classification blocks real-hardware motion unless approval handoff exists. | Driver contract / GuardianDecision gate | Robot actions must remain critical and Guardian-gated; emergency stop remains audited bypass. | Physical-world boundary must not be model-controlled. |
| LIMA robotics bridge | `backend/app/services/lima_robotics_bridge.py` | Resolves natural-language robot commands to MCP tool calls and risk classifications. | DriverCommand | critical | Real hardware motion is blocked until Guardian approval handoff; emergency stop bypasses approval and audits. | Driver contract | Potential shortcut: natural language is parsed directly to robot MCP tools inside Sparkbot. | Future LIMA must require typed intent before this bridge. |
| Workstation overview | `backend/app/api/routes/chat/workstation.py`, `frontend/src/pages/WorkstationPage.tsx` | Presents workstation actions and terminal/meeting surfaces. | ShellAction | high | Inherits backend Guardian coverage per feature. | Shell manifest | UI shell must declare tool packs rather than receive broad runtime authority. | Useful shell-specific boundary. |
| Frontend chat shell | `frontend/src/components/chat/*`, `frontend/src/lib/chat/*`, `frontend/src/pages/ChatPage.tsx` | Captures and displays chat messages, streams, WebSocket updates, and room state. | HumanInput | medium | Mostly frontend shell; backend owns policy. | Shell / HumanInput adapter | Must emit human inputs without embedding policy decisions in UI. | Future adapter should preserve UX. |
| Frontend terminal shell | `frontend/src/components/Terminal/XtermTerminal.tsx`, `frontend/src/hooks/useTerminalSession.ts` | Connects browser UI to terminal sessions. | ShellAction | critical | Backend terminal route provides raw PTY stream. | Shell / Driver adapter | Must not become a generic LIMA terminal driver without Guardian approval contract. | High-risk UI-to-system surface. |
| Meeting / roundtable docs and pages | `frontend/src/pages/MeetingRoomPage.tsx`, `frontend/src/lib/workstationMeeting.ts`, `docs/architecture/roundtable_meeting_flow_v1.6.60.md` | Meeting room workflows, transcripts, or roundtable product behavior. | HumanInput / SystemAction | medium | Needs verification per route and service. | HumanInput adapter / SystemService request | Meeting instructions may be human inputs or system service events depending on source. | Inventory marks as adapter-sensitive. |
| Bot bridge integrations | `backend/app/api/routes/chat/bot_integration.py`, `backend/app/services/telegram_bridge.py`, `discord_bridge.py`, `whatsapp_bridge.py`, `github_bridge.py` | External message ingestion or integration bridges. | HumanInput / SystemAction | high | Needs per-bridge verification. | HumanInput adapter / ToolPack | External send/receive flows require actor identity, shell ID, and policy scope. | Treat inbound messages as human or service input explicitly. |
| Dynamic skills | `backend/app/services/skills.py`, `backend/app/services/skill_executor.py` | Loads skill definitions/executors and runs skill tools. | ToolCall | high | Guardian coverage depends on caller path. | ToolPack declaration / Tool contract | Dynamic registry can become a capability firehose if not scoped. | Require tool pack manifests and GuardianDecision before execution. |
| Desktop/Tauri launcher | `src-tauri/src/main.rs`, `src-tauri/src/lib.rs`, `src-tauri/tauri.conf.json` | Local desktop shell and launcher surface. | ShellAction | medium | Needs verification by command. | Shell manifest | Desktop shell should declare local permissions and tool packs. | Do not extract launcher assumptions into kernel. |
| Product behavior docs/scripts | `docs/audits/*`, `docs/guardian-spine.md`, `docs/lima-robo-os-integration.md`, `scripts/*` | Document existing Guardian/Spine/robotics behavior and operational scripts. | Unknown | unknown | Documentation includes useful intended behavior; scripts need individual review before extraction. | Reference only | Docs can describe desired behavior that code only partially enforces. | Use as parity hints, not direct contract source. |

## Raw Chat-to-Tool Shortcut Risk

Potential shortcut areas found during inspection:

- `backend/app/api/routes/chat/llm.py` appears to keep raw user messages, model routing, model tool-call handling, Guardian policy decisions, and tool execution close together in `stream_chat_with_tools()`. It does call Guardian policy before guarded execution, but LIMA must insert `HumanInput -> IntentEnvelope -> GuardianDecision` before this layer.
- `backend/app/api/routes/chat/voice.py` explicitly routes transcripts into the same tool-aware chat stream. That is good for consistent behavior, but future LIMA must preserve transcript confidence and treat voice as `HumanInput`, not as already-authorized text.
- `backend/app/api/routes/chat/tools.py` centralizes a large tool catalogue and dispatcher. Needs verification for per-tool Guardian decisions and future tool-pack scoping before extraction.
- `backend/app/api/routes/terminal.py` and `backend/app/services/terminal_service.py` expose raw PTY behavior. Route comments state command-level filtering is not enforced. This must remain outside kernel execution until a GuardianDecision-gated driver boundary exists.
- `backend/app/services/lima_robotics_bridge.py` parses natural language into robot MCP tool commands. The inspected bridge blocks real-hardware motion without approval handoff, but future LIMA must require typed intent before robot command resolution.

No direct shortcut is asserted as production-unsafe without runtime testing. These are potential shortcut patterns that need verification before extraction.

## Guardian Coverage Notes

- Guardian policy is active in `backend/app/api/routes/chat/llm.py` through `guardian_suite.policy.decide_tool_use()` before tool execution.
- Guarded execution is routed through `guardian_suite.executive.exec_with_guard()` in the chat tool loop.
- Pending approvals are stored through `guardian_suite.pending_approvals` and surfaced through chat/dashboard flows.
- Breakglass and vault routes are operator-focused and audit sensitive. Vault add/delete routes require breakglass privileged mode in inspected route text.
- MCP explain-plan and run approval routes already distinguish planning, approval request, approval, denial, and audit without executing tools.
- Robotics commands emit audit logs, and the bridge blocks real-hardware motion until approval handoff exists.
- Future LIMA extraction must attach durable `GuardianDecision.decision_id` values to policy decisions, approvals, tool/driver calls, and Spine events.

## Tool-Pack Scoping Notes

Sparkbot appears to expose these future tool packs:

- `comms`: Gmail, Slack, email, messaging bridges, calendar sends.
- `robo`: LIMA robot command, robotics status, emergency stop, MCP robot tools.
- `system`: service status/logs, local machine checks, terminal-adjacent operations.
- `browser`: browser open/navigate/snapshot/fill/click/save/restore.
- `files`: uploads, drive tools, local file-like operations that need deeper inspection.
- `memory`: memory recall, Guardian memory, fact promotion.
- `admin`: breakglass, vault writes/deletes, service management, credentials/security actions.
- `meeting`: meeting room and roundtable flows.
- `terminal`: PTY sessions and terminal send.
- `model`: model routing, Token Guardian, model settings, stream generation.
- `unknown`: dynamic skills and scripts requiring per-skill classification.

Firehose risk: `backend/app/api/routes/chat/tools.py` aggregates many tools in one catalogue. LIMA should scope manifests by shell, actor, risk class, room policy, and declared tool pack before the model sees available tools.

## Future Adapter Requirements

- Chat messages become `HumanInput`.
- Voice transcripts become `HumanInput` with transcript confidence and source metadata.
- Meeting manager instructions become `HumanInput` or `SystemService` requests depending on source.
- Model-generated tool plans must not execute directly.
- Tool execution requires `IntentEnvelope` and `GuardianDecision`.
- Terminal/PTY actions require high/critical risk handling.
- File/network/browser actions require explicit risk class and approval policy.
- Robot/Robo-OS actions require critical risk handling, dry-run when possible, and Guardian approval for physical-world execution.
- Audit events must link `HumanInput.input_id -> IntentEnvelope.intent_id -> GuardianDecision.decision_id -> action event`.
- Sparkbot parity must be behavioral, not architectural shortcut preservation.
- External bridge messages must declare actor identity, shell ID, source system, and permission scope.
- Dynamic skills must become declared tool packs before the Harness can expose them.

## Extraction Blockers

- Mixed chat/model/tool responsibilities in `stream_chat_with_tools()` need a contract boundary before Harness extraction.
- Current policy decisions appear to be logged, but a durable LIMA `GuardianDecision.decision_id` chain is not yet the common execution token.
- Terminal/PTY routes expose raw shell behavior and cannot be extracted into runtime drivers without high/critical Guardian gates.
- Tool catalogue ownership is broad and centralized; future extraction needs per-shell tool-pack manifests.
- Voice transcripts route into chat execution without a distinct typed-intent artifact.
- Robotics bridge contains natural-language-to-MCP command resolution; future LIMA must place Intent Compiler before robot driver planning.
- Guardian, Spine, and audit services still appear tied to Sparkbot app modules and persistence.
- Meeting/workstation boundaries need source classification so system events are not confused with human commands.

## Recommended Next Step

Recommended next branch: `phase-0-7-guardian-decision-id-contract`.

Goal: define the durable `GuardianDecision.decision_id` and approval token linkage required before Guardian, Harness, Driver, Tool, Spine, or Sparkbot adapter extraction.

## Phase 0.7 Follow-Up

The unresolved risks from Phase 0.6 are carried into the GuardianDecision contract. Each risky entrypoint must later be mapped to `decision_id` before extraction, especially `stream_chat_with_tools()`, voice transcript routing, terminal/PTY routes, robotics bridge command planning, and broad tool catalogue execution.
