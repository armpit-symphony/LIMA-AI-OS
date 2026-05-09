# Phase 1.11 HumanInput Adapter Contract

## Purpose

Define non-executing adapter contracts for mapping Sparkbot input surfaces to LIMA `HumanInput` records.

This phase does not implement adapters.
This phase does not modify Sparkbot.
This phase does not wire production routes.
This phase does not execute models or tools.

## Contract Scope

`HumanInputAdapterSurface` identifies the Sparkbot-style surface being mapped:

- `CHAT_MESSAGE`
- `VOICE_TRANSCRIPT`
- `MEETING_PROMPT`
- `SPARKBUD_PROMPT`
- `WORKSTATION_COMMAND`
- `OPERATOR_CONSOLE`
- `TERMINAL_REQUEST`
- `APPROVAL_RESPONSE`
- `MCP_REQUEST`
- `ROBOT_REQUEST`
- `FRONTEND_CHAT`
- `UNKNOWN`

`HumanInputAdapterMapping` records a single design-time mapping from a source surface to a future `HumanInput` shape. It carries the source path/name, target HumanInput source type, actor/session/shell/source references, privacy class, redaction class, shortcut risks, notes, and metadata.

`HumanInputAdapterDesign` groups mappings for a source system and records blocked shortcuts, lineage notes, privacy notes, creation metadata, and design metadata.

`AdapterDesignProtocol` is describe-only:

- `describe_mappings() -> Sequence[HumanInputAdapterMapping]`
- `describe_design() -> HumanInputAdapterDesign`

## Design-Only Rule

Adapter contracts describe mappings only.

They do not:

- read live Sparkbot messages
- call models
- execute tools
- open terminal/PTY
- call Robo-OS
- persist audit data
- enforce Guardian decisions
- bypass IntentCompiler

These contracts do not transform live Sparkbot messages. They exist so future adapter work targets stable LIMA contract shapes before any production integration exists.

## Required Mapping Fields

Every future adapter mapping should identify:

- source surface
- source path/name
- HumanInput source type
- actor reference
- shell reference
- session reference
- source reference
- privacy class
- redaction class
- shortcut risks
- lineage notes

Mappings should also preserve room, meeting, message, operator, terminal session, MCP run, robot, and frontend source references when available, but only as references. Raw sensitive content should use `content_ref`, `transcript_ref`, or equivalent references once implementation begins.

## Blocked Shortcuts

Adapter mappings must explicitly block:

- raw chat-to-tool shortcut
- `stream_chat_with_tools` direct extraction
- model-generated tool calls before `GuardianDecision`
- full-catalogue tool exposure
- terminal/PTY direct execution
- raw natural language to robot MCP command
- direct approval/breakglass bypass

Sparkbot remains the spec for behavior. LIMA Runtime does not preserve unsafe shortcut internals as kernel primitives.

## Sparkbot Mapping Examples

| Sparkbot surface | Future mapping |
| --- | --- |
| chat message route / WebSocket | `HumanInputSource.TEXT` with actor, shell, room, and message references |
| voice transcript | `HumanInputSource.VOICE` with transcript reference and confidence metadata |
| meeting / roundtable prompt | `HumanInputSource.TEXT` with meeting and room references |
| SparkBud prompt | `HumanInputSource.TEXT` with specialist/agent actor metadata as a bot reference |
| Workstation command | `HumanInputSource.CONSOLE` or `HumanInputSource.TEXT` depending on whether the surface is a control or freeform prompt |
| operator console | `HumanInputSource.CONSOLE` with operator and shell references |
| terminal request | `HumanInputSource.CONSOLE` with critical risk notes and no PTY execution |
| MCP explain-plan/run approval | `HumanInputSource.CONSOLE` for operator controls or approval response mapping for approval inputs |
| robotics natural language request | `HumanInputSource.TEXT` with safety-critical notes and robot/source references |
| frontend chat input | `HumanInputSource.TEXT` with frontend source metadata and room/session references |

## Privacy Defaults

- chat text: `PrivacyClass.PRIVATE`
- voice transcript: `PrivacyClass.PRIVATE` or `PrivacyClass.BIOMETRIC` depending on audio handling
- meeting transcript: `PrivacyClass.CONFIDENTIAL`
- terminal/operator command: `PrivacyClass.CONFIDENTIAL` and `RedactionClass.REFERENCE_ONLY`
- robot/physical-world request: `PrivacyClass.SAFETY_CRITICAL`
- future BCI/thought-adjacent: `PrivacyClass.BIOMETRIC` and confirm-only

## Acceptance Criteria

- adapter contracts exist
- `AdapterDesignProtocol` is describe-only
- no adapt/execute/live methods exist
- no Sparkbot imports
- no runtime behavior
- raw chat-to-tool shortcut remains blocked
- tests validate contract shape only
