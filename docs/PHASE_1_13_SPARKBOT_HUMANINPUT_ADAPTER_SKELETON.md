# Phase 1.13 Sparkbot HumanInput Adapter Skeleton

## Purpose

Create a non-production LIMA adapter skeleton that converts neutral Sparkbot-style payloads into HumanInput records.

This skeleton does not import Sparkbot.
This skeleton does not wire routes.
This skeleton does not execute models/tools.
This skeleton does not create IntentEnvelope or GuardianDecision.

## Payloads

- `SparkbotChatInputPayload`: carries message, actor, shell, session, text or text reference, source reference, trusted context reference, passive autonomy notes, and metadata.
- `SparkbotVoiceInputPayload`: carries transcript reference, actor, shell, session, confidence, trusted context reference, passive autonomy notes, and metadata.
- `SparkbotMeetingInputPayload`: carries meeting, room, actor, shell, prompt or prompt reference, trusted context reference, passive autonomy notes, and metadata.
- `SparkbotOperatorInputPayload`: carries operator command or command reference, actor, shell, session, trusted context reference, passive autonomy notes, and metadata.

These payloads are LIMA-owned neutral records. They are not Sparkbot request objects.

## Adapter Methods

- `adapt_chat_payload`
- `adapt_voice_payload`
- `adapt_meeting_payload`
- `adapt_operator_payload`

Each method accepts a neutral payload and returns a `HumanInput` contract object.

## Guardrails

- no Sparkbot imports
- no FastAPI/WebSocket imports
- no stream_chat_with_tools
- no execute_tool
- no model/harness calls
- no tool execution
- no terminal/PTY
- no robot/Robo-OS
- no persistence
- no env vars
- no DB
- no external services
- no production wiring
- no autonomy enforcement
- no approval decisions
- no IntentEnvelope or GuardianDecision creation
- no ApprovalMetadata, PolicyDecision, or SpineEvent creation

## Owner Autonomy Metadata

`trusted_context_ref` and `autonomy_notes` are passive metadata only.

They do not authorize action.
They do not enforce autonomy.
They do not replace Guardian.

Owner-defined autonomy remains a future policy and Guardian concern. The skeleton only preserves context that later policy review may evaluate.

## Raw Chat-to-Tool Block

This adapter stops at HumanInput.

Any model/tool planning must happen later after IntentCompiler, IntentEnvelope, GuardianDecision, ToolPackScope, and policy.

The skeleton does not preserve any raw chat-to-tool shortcut and does not provide a direct path from chat, voice, meeting, or operator input to tools.

## Acceptance Criteria

- neutral payload dataclasses exist
- adapter returns HumanInput
- no Sparkbot imports
- no execution methods
- no route wiring
- no model/tool calls
- no persistence
- no decision, approval, policy, or spine event creation
- tests prove mappings
- tests prove forbidden imports/methods absent
