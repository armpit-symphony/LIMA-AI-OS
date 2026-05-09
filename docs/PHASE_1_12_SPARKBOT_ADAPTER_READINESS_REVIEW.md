# Phase 1.12 Sparkbot Adapter Readiness Review

## Purpose

Review whether LIMA is ready to create a first non-production Sparkbot HumanInput adapter skeleton.

This review does not implement adapters.
This review does not modify Sparkbot.
This review does not authorize production wiring.
This review does not authorize model/tool execution.

This review includes the Phase 1.12A Owner Autonomy & Safety Policy. Owner autonomy is now part of the adapter context, but only as passive metadata until a later reviewed phase.

## Sparkbot Reference Commit

| Repo | Branch | Commit | Inspected paths | Modified? | Notes |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `b59041d2946e8c121e76ab9af47d1fbea4bd90cb` | `backend/app/api/routes/chat/messages.py`, `backend/app/api/routes/chat/websocket.py`, `backend/app/api/routes/chat/voice.py`, `backend/app/api/routes/chat/llm.py`, `backend/app/api/routes/chat/tools.py`, `backend/app/api/routes/chat/mcp.py`, `backend/app/services/mcp_registry.py`, `backend/app/services/mcp_runs.py`, `backend/app/api/routes/chat/robotics.py`, `backend/app/services/lima_robotics_bridge.py`, `backend/app/api/routes/terminal.py`, `backend/app/services/terminal_service.py`, `frontend/src/pages/WorkstationPage.tsx`, `frontend/src/pages/MeetingRoomPage.tsx`, `frontend/src/lib/workstationMeeting.ts`, `frontend/src/lib/sparkbudLaunch.ts`, `frontend/src/components/chat/ChatInput.tsx`, `frontend/src/pages/ChatPage.tsx`, `docs/architecture/roundtable_meeting_flow_v1.6.60.md`, `docs/capabilities.md` | No | Sparkbot was fetched, checked out on `main`, fast-forward checked, and inspected read-only. The local Sparkbot worktree remained clean. Adapter-relevant surfaces remain chat/REST, chat WebSocket, voice transcript, meeting/roundtable, SparkBud, Workstation, terminal/operator, MCP explain-plan/approval, robotics natural-language/control, and frontend chat. |

## Current Adapter Contract State

Phase 1.10 designed the Sparkbot HumanInput adapter boundary.

Phase 1.11 created describe-only adapter contracts.

Phase 1.12A added owner-defined autonomy and safety policy.

`AdapterDesignProtocol` is describe-only.

No live adapter implementation exists.

Sparkbot input must become `HumanInput` before `IntentEnvelope`, `GuardianDecision`, planning, tool exposure, execution, or audit lineage. `stream_chat_with_tools` remains a do-not-extract direct path because it is close to model routing, tool calls, approval handling, and execution.

## Owner Autonomy Context

The future adapter must support owner-defined autonomy, not approval fatigue.

However, Phase 1.13 skeleton must not implement autonomy behavior yet.

It may carry metadata needed later:

- actor_ref
- shell_id
- session_ref
- trusted device/session hints
- privacy class
- risk notes
- autonomy policy notes

But it must not decide approval, risk, autonomy, or execution.

Owner-autonomy metadata is evidence for later Guardian and policy review. It is not permission. Guardian remains mandatory. Human safety, law, configured safety policy, and privacy constraints override owner command.

## Readiness Decision

GO for Phase 1.13 non-production Sparkbot HumanInput adapter skeleton using neutral payloads.

NO-GO for:

- production Sparkbot wiring
- live route integration
- model execution
- tool execution
- `stream_chat_with_tools` extraction
- terminal/PTY execution
- Robo-OS physical action
- audit persistence
- redaction runtime
- Guardian/policy/approval enforcement
- autonomy enforcement

## First Allowed Adapter Skeleton

Recommended next branch:

`phase-1-13-sparkbot-humaninput-adapter-skeleton`

Allowed scope:

- create a non-production, test-only adapter skeleton in LIMA
- adapter accepts neutral dataclass-style input payloads, not live Sparkbot objects
- adapter returns HumanInput contract objects
- may include owner-autonomy metadata fields as passive metadata only
- no Sparkbot imports
- no route wiring
- no model calls
- no tool calls
- no persistence
- no terminal/PTY
- no external services
- no autonomy decision logic

Recommended skeleton:

- `lima/adapters/sparkbot_humaninput.py`
- class `SparkbotHumanInputAdapter`
- methods may adapt explicit neutral payload dataclasses into `HumanInput`:
  - `adapt_chat_payload`
  - `adapt_voice_payload`
  - `adapt_meeting_payload`
  - `adapt_operator_payload`

These methods must accept neutral payloads defined in LIMA, not Sparkbot request objects.

## Safe Input Payloads

These payloads are proposed for the next phase only. They are not implemented in this review.

### SparkbotChatInputPayload

- message_id
- actor_ref
- shell_id
- session_ref
- text_ref or text
- source_ref
- trusted_context_ref optional
- autonomy_notes optional
- metadata

### SparkbotVoiceInputPayload

- transcript_ref
- actor_ref
- shell_id
- session_ref
- confidence
- trusted_context_ref optional
- autonomy_notes optional
- metadata

### SparkbotMeetingInputPayload

- meeting_id
- room_id
- prompt_ref or prompt
- actor_ref
- shell_id
- trusted_context_ref optional
- autonomy_notes optional
- metadata

### SparkbotOperatorInputPayload

- command_ref or command
- actor_ref
- shell_id
- session_ref
- trusted_context_ref optional
- autonomy_notes optional
- metadata

## Required Guardrails for Phase 1.13

- no Sparkbot imports
- no FastAPI route imports
- no WebSocket imports
- no `stream_chat_with_tools` import
- no `execute_tool` import
- no model/harness imports
- no terminal/PTY imports
- no robot/Robo-OS imports
- no persistence
- no env vars
- no DB
- no external services
- no production route wiring
- no raw chat-to-tool shortcut
- no autonomy enforcement
- no approval decisions
- no GuardianDecision creation
- adapter returns HumanInput only

## Mapping Requirements

Phase 1.13 skeleton must map:

- chat payload -> HumanInput source TEXT
- voice payload -> HumanInput source VOICE
- meeting payload -> HumanInput source TEXT
- operator payload -> HumanInput source CONSOLE

It must include:

- input_id
- source
- actor_id or actor_ref mapping
- shell_id
- raw_text or content_ref
- confidence where applicable
- metadata
- privacy metadata where available
- passive trusted/autonomy metadata only

The skeleton must not create `IntentEnvelope`, `GuardianDecision`, `ApprovalMetadata`, `PolicyDecision`, `ToolExposureDecision`, `SpineEvent`, or persistent audit records.

## Privacy Requirements

Before implementation:

- chat text defaults PRIVATE
- voice transcript defaults PRIVATE / BIOMETRIC depending data
- meeting prompt defaults CONFIDENTIAL
- operator/terminal-like command defaults CONFIDENTIAL and REFERENCE_ONLY
- robot/physical request remains blocked

Phase 1.13 may carry privacy metadata but must not persist anything.

## Still Blocked

- `stream_chat_with_tools` direct extraction
- Sparkbot route wiring
- live WebSocket adapter
- live frontend adapter
- model execution
- tool execution
- terminal/PTY
- Robo-OS physical action
- audit persistence
- redaction runtime
- Guardian/policy/approval enforcement
- autonomy enforcement
- live auth/vault adapters
- production deploy integration

## Acceptance Criteria for Phase 1.13

- non-production adapter skeleton only
- no Sparkbot imports
- neutral payload dataclasses only
- returns HumanInput
- no IntentEnvelope creation
- no GuardianDecision creation
- no model/tool execution
- no autonomy decisions
- no persistence
- no production wiring
- tests prove chat/voice/meeting/operator payloads map to HumanInput
- tests prove forbidden imports/methods are absent

## Risk Register

| Risk | Severity | Mitigation | Next action |
| --- | --- | --- | --- |
| Adapter accidentally imports Sparkbot route/request objects | High | Use neutral LIMA-owned payload dataclasses only; add tests blocking `app.`/FastAPI/WebSocket imports in adapter module. | Phase 1.13 tests should scan adapter imports and source text. |
| Adapter accidentally calls `stream_chat_with_tools` | Critical | Explicitly forbid import/call; adapter returns `HumanInput` only. | Phase 1.13 tests should block `stream_chat_with_tools`. |
| Adapter preserves raw chat-to-tool shortcut | Critical | Require `HumanInput` as the only output and block `IntentEnvelope`, `GuardianDecision`, model, tool, and Harness creation. | Keep shortcut block in tests and docs. |
| Autonomy metadata mistaken for autonomy enforcement | High | Treat trusted/autonomy fields as passive metadata only. No approval/risk/autonomy decisions in adapter. | Phase 1.13 should name fields `*_notes` or refs, not policy decisions. |
| Identity/session mapping still approximate | Medium | Carry `actor_ref`, `shell_id`, `session_ref`, and `source_ref` without claiming auth authority. | Later identity/session review before production wiring. |
| Privacy metadata still design-level | Medium | Apply conservative defaults and avoid persistence. | Later redaction runtime review before audit storage. |
| Lineage not persisted | Medium | Carry source refs and input IDs only; no Spine writes. | Later lineage emission design before persistence. |
| Future production wiring risk | High | Keep Phase 1.13 non-production and test-only; route wiring remains no-go. | Require separate production adapter readiness review. |

## Review Summary

Phase 1.12 finds LIMA ready to create a first non-production Sparkbot HumanInput adapter skeleton, but only under strict guardrails.

The allowed skeleton is a boundary proof. It may translate neutral payload dataclasses into `HumanInput` records and carry passive privacy/trusted-context/autonomy metadata. It must not import Sparkbot, wire routes, call models or tools, create Guardian decisions, enforce autonomy, persist audit data, or touch terminal/robot execution.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
