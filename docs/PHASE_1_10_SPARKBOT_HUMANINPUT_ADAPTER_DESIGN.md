# Phase 1.10 Sparkbot HumanInput Adapter Design

## Purpose

Design how Sparkbot input surfaces should map into LIMA `HumanInput` records.

This phase does not implement adapters.
This phase does not modify Sparkbot.
This phase does not execute models or tools.
This phase does not wire production behavior.

Phase 1.10 is an adapter-design gate only. It preserves Sparkbot as the behavior spec while blocking raw chat-to-tool shortcuts from becoming LIMA Runtime primitives.

## Reference Commit Inspected

| Repo | Branch | Commit | Inspected paths | Modified? | Notes |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `origin/main` | `b59041d2946e8c121e76ab9af47d1fbea4bd90cb` | `backend/app/api/routes/chat/messages.py`, `backend/app/api/routes/chat/websocket.py`, `backend/app/api/routes/chat/voice.py`, `backend/app/api/routes/chat/llm.py`, `backend/app/api/routes/chat/mcp.py`, `backend/app/api/routes/chat/robotics.py`, `backend/app/api/routes/chat/workstation.py`, `backend/app/api/routes/terminal.py`, `backend/app/services/terminal_service.py`, `frontend/src/components/chat/ChatInput.tsx`, `frontend/src/pages/ChatPage.tsx`, `frontend/src/pages/MeetingRoomPage.tsx`, `frontend/src/pages/SparkBudPage.tsx`, `frontend/src/pages/WorkstationPage.tsx`, `frontend/src/lib/workstationMeeting.ts`, `frontend/src/lib/sparkbudLaunch.ts`, `frontend/src/lib/mcpRegistry.ts` | No | Latest inspected commit is v1.6.67-era `origin/main`. Input surfaces were inspected read-only. The local Sparkbot checkout remained clean. |

## HumanInput Boundary

Future adapter chain:

```text
Sparkbot input surface
  -> HumanInput
  -> IntentCompiler
  -> IntentEnvelope
  -> GuardianDecision
  -> ToolPackScope / Policy / Approval
  -> Execution later
  -> Spine/Audit lineage later
```

Raw Sparkbot messages must not directly become tool execution.

The future adapter must convert a Sparkbot input surface into `HumanInput` first. The Intent Compiler translates human control input into typed intent. Guardian decides what can proceed. Harness, tool, driver, terminal, MCP, and robot execution remain later phases and require a `GuardianDecision.decision_id`.

## Sparkbot Input Surface Inventory

| Sparkbot surface | Current path / file | Current role | Input type | Future `HumanInput.source` | Actor / shell mapping | Privacy class | Redaction class | Risk notes | Adapter notes | Do-not-preserve shortcut risks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Chat message REST route | `backend/app/api/routes/chat/messages.py::create_room_message` | Creates room messages and may trigger inline bot response | `chat_text` | `TEXT` | `actor_id` from current chat user; `shell_id` candidate `sparkbot-chat`; `session_id` from room/session; `message_id` from created message | `PRIVATE` by default | `SUMMARY_ONLY`, or `REFERENCE_ONLY` when sensitive | User text may contain secrets, commands, file paths, URLs, or task instructions | Future adapter emits `HumanInput` with `content_ref`/`source_ref` and no model/tool call | Existing inline bot response path must not become a LIMA adapter shortcut |
| Chat WebSocket | `backend/app/api/routes/chat/websocket.py::websocket_main`, `websocket_chat` | Real-time room message input and broadcast | `chat_text` | `TEXT` | `actor_id` from authenticated user; `shell_id` candidate `sparkbot-chat-ws`; `session_id` and `room_id` from WebSocket scope; `client_msg_id` when present | `PRIVATE` by default | `SUMMARY_ONLY`, or `REFERENCE_ONLY` when sensitive | Real-time chat can contain operational commands | Future adapter treats WebSocket message payloads as HumanInput only | WebSocket messages must not directly invoke model/tool execution |
| Frontend chat input | `frontend/src/components/chat/ChatInput.tsx`, `frontend/src/pages/ChatPage.tsx` | Captures user text and posts to chat APIs | `chat_text` | `TEXT` | `actor_id` from current UI session; `shell_id` candidate `sparkbot-frontend-chat`; `session_id`/`room_id` from selected room | `PRIVATE` by default | `SUMMARY_ONLY`, or `REFERENCE_ONLY` when sensitive | Browser UI cannot decide policy or tool scope | UI may provide source metadata and client message IDs only | Frontend controls must not become execution authority |
| `stream_chat_with_tools` | `backend/app/api/routes/chat/llm.py::stream_chat_with_tools` | Current model/tool streaming loop with selected tools and tool nudges | `unknown` design surface; user content arrives from prior chat/voice paths | `UNKNOWN` until adapted upstream, then `TEXT` or `VOICE` | Not a HumanInput source; it is a later model/Harness concern after intent and Guardian | Depends on upstream input; treat as `PRIVATE` or stricter | `REFERENCE_ONLY` for prompts/tool args/results until redaction exists | Critical shortcut risk: current path is near model calls and tool planning | Do not extract as a direct adapter. Split future planning/execution behind IntentEnvelope and GuardianDecision | Raw chat-to-tool and full tool catalogue exposure must not be preserved |
| Voice transcript route | `backend/app/api/routes/chat/voice.py::voice_message`, `transcribe_only` | Transcribes audio, saves transcript as human message, and can stream through chat tools | `voice_transcript` | `VOICE` | `actor_id` from current chat user; `shell_id` candidate `sparkbot-voice`; `session_id`/`room_id`; `message_id`; `transcript_ref` preferred | `PRIVATE`; `BIOMETRIC` if audio/voiceprint is retained or analyzed | `REFERENCE_ONLY` preferred; `SUMMARY_ONLY` if transcript summary is enough | Voice may contain biometric data, private speech, secrets, or commands | Future adapter emits transcript-derived HumanInput and confidence metadata; raw audio/transcript persistence remains separate review | Voice transcript must not directly enter `stream_chat_with_tools` |
| Meeting / roundtable owner prompt | `frontend/src/pages/MeetingRoomPage.tsx`, `frontend/src/lib/workstationMeeting.ts::launchMeetingRoom`, `launchProjectMeetingRoom` | Starts or redirects autonomous meeting rooms and seeds kickoff prompts | `meeting_prompt` | `TEXT` | `actor_id` from room owner/current user; `shell_id` candidate `sparkbot-meeting`; `session_id`/`room_id`; `meeting_id` from room metadata | `CONFIDENTIAL` by default | `SUMMARY_ONLY` or `REFERENCE_ONLY` | Meeting prompts may include project details, plans, approvals, blockers, or private context | Future adapter distinguishes owner input from generated meeting protocol text | Autonomous meeting prompts must not become self-executing tasks |
| SparkBud prompt / launch brief | `frontend/src/lib/sparkbudLaunch.ts`, `frontend/src/pages/SparkBudPage.tsx`, `frontend/src/pages/WorkstationPage.tsx` | Builds specialist launch prompts and opens chat-ready agent contexts | `SparkBud prompt` | `TEXT` | `actor_id` from launching user; `shell_id` candidate `sparkbud`; `session_id` from target chat/room; agent handle as bot actor ref | `PRIVATE` by default | `SUMMARY_ONLY` | Specialist prompts may encode task intent and agent role constraints | Future adapter records the human launch brief as HumanInput before any agent prompt expansion | SparkBud launch text must not bypass IntentCompiler or Guardian |
| Workstation command/control | `frontend/src/pages/WorkstationPage.tsx`, `backend/app/api/routes/chat/workstation.py` | Workstation UI surfaces desks, meetings, MCP panel, terminal panel, and operator controls | `Workstation command` | `CONSOLE` for command-style controls; `TEXT` for freeform prompts | `actor_id` from current user; `shell_id` candidate `sparkbot-workstation`; station ID/panel kind as metadata | `CONFIDENTIAL` by default | `REFERENCE_ONLY` for operational commands | Workstation can point at terminal, computer control, MCP, meetings, and robot surfaces | Future adapter maps UI command intent to HumanInput and shell metadata only | Workstation buttons must not become direct runtime operations |
| Terminal / operator commands | `backend/app/api/routes/terminal.py`, `backend/app/services/terminal_service.py`, `frontend/src/pages/WorkstationPage.tsx` | Creates live terminal sessions and streams PTY input/output | `terminal_request` / `operator_console` | `CONSOLE` | `actor_id` from authenticated operator; `shell_id` candidate `sparkbot-terminal`; `session_id` from terminal session; terminal ID as source ref | `CONFIDENTIAL` | `REFERENCE_ONLY` | Critical: terminal input/output may contain secrets, host state, destructive commands, and raw logs | Future adapter may describe terminal requests as HumanInput; no PTY execution in this phase | Raw PTY input must not be extracted as a LIMA driver path without GuardianDecision and approval |
| MCP explain-plan request | `backend/app/api/routes/chat/mcp.py::mcp_explain_plan`, `frontend/src/lib/mcpRegistry.ts`, `frontend/src/pages/WorkstationPage.tsx` | Creates no-execution MCP explain-plan/run records | `MCP request` | `CONSOLE` | `actor_id` from current user; `shell_id` candidate `sparkbot-mcp-panel`; `session_id`/`room_id`; `run_id`/manifest ID | `CONFIDENTIAL` for operator requests; `SAFETY_CRITICAL` for robot manifests | `REFERENCE_ONLY` | MCP manifests include terminal send, external send, secret use, and robot motion categories | Future adapter records operator request as HumanInput and later maps to IntentEnvelope/tool-pack policy | Explain-plan must not become implicit tool execution |
| MCP approval response | `backend/app/api/routes/chat/mcp.py::mcp_run_request_approval`, `mcp_run_approve`, `mcp_run_deny`, `frontend/src/lib/mcpRegistry.ts` | Records request/approve/deny state for planned MCP runs | `approval_response` | `CONSOLE` | `actor_id` from operator; `shell_id` candidate `sparkbot-mcp-approval`; `run_id` and `approval_id` as refs | `CONFIDENTIAL` | `REFERENCE_ONLY` | Approval response is evidence, not execution authority | Future adapter records approval response input separately from policy/approval contracts | Approval click must not authorize execution without GuardianDecision and scoped ApprovalMetadata |
| Robotics command route | `backend/app/api/routes/chat/robotics.py`, `backend/app/services/lima_robotics_bridge.py`, `frontend/src/lib/mcpRegistry.ts` | Sends robot command contracts to LIMA robotics bridge; includes dry-run and emergency stop surfaces | `robot_request` | `TEXT` for natural language requests; `CONSOLE` for operator controls | `actor_id` from current user; `shell_id` candidate `sparkbot-robo`; `robot_id` and MCP tool name as refs | `SAFETY_CRITICAL`; `BIOMETRIC` if person/sensor data is involved | `REFERENCE_ONLY` | Critical physical-world risk; sensor data and motion commands need explicit review | Future adapter emits HumanInput and requires typed intent, dry-run/simulation planning, GuardianDecision, and approval before motion | Raw natural language to robot MCP command is blocked |
| Meeting task/operator action controls | `frontend/src/pages/MeetingRoomPage.tsx`, `frontend/src/lib/workstationMeeting.ts` | Owner/operator can run task meeting flows, interrupt, redirect, or request task run from meeting sidebar | `operator_console` / `meeting_prompt` | `CONSOLE` for controls; `TEXT` for owner prompts | `actor_id` from meeting owner/operator; `shell_id` candidate `sparkbot-meeting-operator`; `room_id`, `meeting_id`, task ID refs | `CONFIDENTIAL` | `REFERENCE_ONLY` | Meeting controls can touch task, approval, and project state | Future adapter captures the operator action as HumanInput and later links to policy/approval lineage | Meeting sidebar actions must not become direct task/tool execution |
| Unknown or newly added input surface | Any future Sparkbot route, bridge, frontend control, plugin, or robotics surface not classified above | Unreviewed input | `unknown` | `UNKNOWN` at design level; must map to a concrete `HumanInputSource` before implementation | Actor/shell/session mapping required before use | `UNKNOWN`, promote to stricter class before persistence | `REFERENCE_ONLY` until reviewed | Unknown surfaces are deny-by-default | Future adapter design must classify before wiring | Unknown input cannot execute or plan tools |

Current `HumanInputSource` contract values are `TEXT`, `VOICE`, `CONSOLE`, `GESTURE`, and `FUTURE_BCI`. `UNKNOWN` above is a design-level hold state for unclassified surfaces; implementation must map to a real contract value or reject the surface.

## Actor and Shell Mapping

Phase 1.10 only designs mapping. It does not implement identity lookup.

Actor ID source candidates:

- Sparkbot `current_user.id` for authenticated chat, voice, WebSocket, MCP, Workstation, terminal, and robotics routes.
- Frontend local session or authenticated user context for UI-only draft surfaces.
- Meeting owner/current user for meeting kickoff, redirect, task, and approval prompts.
- Operator user ID for terminal, MCP approval, breakglass-style, and command-console controls.
- Agent/bot actor references for SparkBud specialists, invite agents, meeting participants, and generated bot messages. Bot actors should not be treated as human approvers.

Shell ID candidates:

- `sparkbot-chat`
- `sparkbot-chat-ws`
- `sparkbot-frontend-chat`
- `sparkbot-voice`
- `sparkbot-meeting`
- `sparkbot-workstation`
- `sparkbud`
- `sparkbot-terminal`
- `sparkbot-mcp-panel`
- `sparkbot-mcp-approval`
- `sparkbot-robo`

Session and source mapping candidates:

- `session_id`: chat session, browser session, room session, terminal session, or future shell session.
- `room_id`: Sparkbot chat room UUID.
- `meeting_id`: Workstation/meeting room ID or meeting metadata ID.
- `message_id`: Sparkbot chat message ID or client message ID.
- `operator_id`: authenticated operator/current user ID when an input is an approval or console action.
- `source_ref`: stable reference to Sparkbot route, frontend component, WebSocket client message, MCP run ID, terminal session ID, robot ID, or meeting artifact.

Generated bot messages, meeting heartbeat outputs, model responses, and tool results are not human input. They may become evidence or lineage records later, but not `HumanInput` records.

## Privacy / Redaction Defaults

Chat text:

- Default `PrivacyClass.PRIVATE`.
- Use `RedactionClass.SUMMARY_ONLY` for ordinary private chat.
- Use `RedactionClass.REFERENCE_ONLY` when content may contain secrets, credentials, file paths, private documents, health/legal/financial data, or operational instructions.

Voice transcript:

- Default `PrivacyClass.PRIVATE` for transcript text.
- Use `PrivacyClass.BIOMETRIC` if raw audio, voiceprints, speaker identity features, or person-identifying voice metadata are retained or analyzed.
- Prefer `transcript_ref` over raw transcript persistence.
- Prefer `RedactionClass.REFERENCE_ONLY` for raw transcript content until redaction runtime exists.

Meeting transcript:

- Default `PrivacyClass.CONFIDENTIAL`.
- Prefer transcript references, summaries, meeting artifact references, and redacted excerpts over raw transcript persistence.
- Use `RedactionClass.SUMMARY_ONLY` for meeting notes and `REFERENCE_ONLY` for raw transcript content.

Terminal/operator command:

- Default `PrivacyClass.CONFIDENTIAL`.
- Default `RedactionClass.REFERENCE_ONLY`.
- Commands and terminal output may contain secrets, host paths, credentials, service state, and destructive intent.

Robot/physical-world request:

- Default `PrivacyClass.SAFETY_CRITICAL`.
- Add `PrivacyClass.BIOMETRIC` handling if sensor data, person images, voice, gait, face, location, or other person data is involved.
- Use `RedactionClass.REFERENCE_ONLY` unless a reviewed redaction policy allows a summary.

Future BCI/thought-adjacent input:

- Default `PrivacyClass.BIOMETRIC`.
- Confirmation-only.
- Never direct approval.
- Never direct control.
- Never direct execution.

## Raw Chat-to-Tool Shortcut Block

`stream_chat_with_tools` must not be extracted as a direct adapter.

Chat text must first become `HumanInput`.

Model/tool planning must happen after `IntentEnvelope` and `GuardianDecision`.

Tool execution requires `GuardianDecision.decision_id`.

Full tool catalogue exposure remains blocked.

Sparkbot parity means preserving user-facing behavior through governed boundaries, not preserving raw chat-to-tool internals.

## Adapter Contract Sketch

Future non-production adapter interface in prose:

```text
SparkbotHumanInputAdapter
  describe_supported_surfaces() -> adapter surface metadata
  adapt_chat_message(...) -> HumanInput or design-level equivalent
  adapt_voice_transcript(...) -> HumanInput or design-level equivalent
  adapt_meeting_prompt(...) -> HumanInput or design-level equivalent
  adapt_workstation_command(...) -> HumanInput or design-level equivalent
  adapt_operator_console(...) -> HumanInput or design-level equivalent
  adapt_approval_response(...) -> HumanInput or design-level equivalent
```

The future adapter should be describe/adapt only. It must not execute, call models, call tools, call drivers, open terminal sessions, approve actions, persist audit data, or mutate Sparkbot production state.

Phase 1.10 intentionally does not add adapter code. The existing `HumanInput` contract is sufficient for this design gate.

## Lineage Planning

Future adapter implementation should plan, but not persist in Phase 1.10:

- `input_id`: LIMA HumanInput identifier.
- `session_id`: shell/chat/terminal/meeting session identifier.
- `shell_id`: source shell or panel identifier.
- `actor_id`: authenticated human actor or operator.
- `message_id`: Sparkbot message/client message ID when available.
- `room_id`: Sparkbot room UUID.
- `meeting_id`: Workstation/meeting room identifier.
- `source_ref`: Sparkbot route/component/run/session reference.
- `content_ref`: reference to source content when raw content should not be persisted inline.
- `lineage_id`: planned future audit chain identifier.

Lineage IDs are planned but not persisted in this phase.

## Acceptance Criteria

- Sparkbot input surfaces are inventoried.
- Each surface has a future `HumanInput` mapping or a blocked/unclassified hold state.
- Privacy/redaction defaults are identified.
- Raw chat-to-tool shortcut is explicitly blocked.
- No Sparkbot code is modified.
- No adapter implementation is added.
- No tool/model execution is added.
- No terminal/PTY execution is added.
- No Robo-OS physical action is added.
- No audit persistence is added.
- Tests remain contract/docs shape only.
