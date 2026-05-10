# Phase 2.1 Fixture Harness Coverage Review

## Purpose

Review whether the Phase 2.0 non-production fixture harness covers enough Sparkbot-shaped payloads before any further harness expansion.

This review does not implement production wiring.
This review does not authorize model/tool execution.
This review does not modify Sparkbot.

## Sparkbot Reference Check

| Repo | Branch | Commit | Checked surfaces | Modified? yes/no | Adapter-relevant changes since Phase 2.0 |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `4a08838ba500fec4ef85c163b3249a2db80da9d6` | Chat REST/WebSocket, `stream_chat_with_tools`, chat model routing, voice/transcript, meeting/roundtable, SparkBud, Workstation, operator/terminal input, MCP explain-plan/run approval, robotics natural-language surfaces, frontend chat input, auth/session/user context, Token Guardian/model routing, and Guardian autonomous-turn pacing. | No tracked Sparkbot modifications by this task; local checkout has an untracked `scripts/file_v1_6_72_proposals.py`. | Sparkbot moved from `4da833858428e076645cac8fca942205e80bcc6e` to `4a08838ba500fec4ef85c163b3249a2db80da9d6` (`v1.6.72`). Changes add autonomous-turn pacing around chat/meeting model dispatch, new operator Spine APIs for autonomous pauses, Guardian sidecar data-dir behavior, and frontend Spine UI for paused/backing-off agents. Existing chat/voice/meeting/operator/MCP/robot fixture request shapes did not require immediate replacement, but model-routing/Token Guardian and autonomous-turn pacing context is now more important coverage. |

## Current Fixture Categories

| Category | Fixture file | Harness exercises it? | Maps to HumanInput? | Goes through fake pipeline? | Non-executing / safety notes |
| --- | --- | --- | --- | --- | --- |
| chat payloads | `tests/fixtures/sparkbot_payloads/chat_payloads.json` | Yes | Yes, `HumanInputSource.TEXT` | Yes | Unknown action defaults to denied; fixture mirror only. |
| voice/transcript payloads | `tests/fixtures/sparkbot_payloads/voice_payloads.json` | Yes | Yes, `HumanInputSource.VOICE` | Yes | Voice recognition is explicitly not performed. |
| meeting payloads | `tests/fixtures/sparkbot_payloads/meeting_payloads.json` | Yes | Yes, `HumanInputSource.TEXT` | Yes | Meeting/room refs are preserved as metadata only. |
| operator payloads | `tests/fixtures/sparkbot_payloads/operator_payloads.json` | Yes | Yes, `HumanInputSource.CONSOLE` | Yes | Terminal-shaped fixtures are critical and non-executing. |
| MCP approval payloads | `tests/fixtures/sparkbot_payloads/mcp_approval_payloads.json` | Yes | Yes, `HumanInputSource.CONSOLE` | Yes | Tool-call records are high risk and non-executing; no tool is run. |
| robot request payloads | `tests/fixtures/sparkbot_payloads/robot_request_payloads.json` | Yes | Yes, `HumanInputSource.CONSOLE` | Yes | Robot records are safety-critical and non-executing; no physical action occurs. |

## Coverage Assessment

| Surface | Fixture coverage | Harness coverage | Risk level | Gap | Recommended action |
| --- | --- | --- | --- | --- | --- |
| chat | Partial | Covered for stream and WebSocket-shaped examples | High | Frontend chat send body and message-type variants are not first-class fixtures. | Add frontend chat fixture examples. |
| voice/transcript | Partial | Covered for transcript refs and confidence | High | No hands-free loop, TTS, or alternate voice control shape. | Add only if current Sparkbot payload shape requires it. |
| meeting/roundtable | Partial | Covered for kickoff and artifact examples | High | Autonomous turn pacing and meeting heartbeat context are not mirrored. | Add meeting/autonomous-turn fixture context. |
| operator/console | Partial | Covered for terminal session and terminal WebSocket input | Critical | Current coverage proves non-execution, not broader operator/admin context. | Keep critical and expand only with synthetic refs. |
| MCP approval | Partial | Covered as high-risk non-executing fake tool call records | Critical | Approval run/request lifecycle variants are not fully mirrored. | Add more MCP approval lifecycle fixtures if needed. |
| robot request | Partial | Covered as safety-critical non-executing fake robot records | Critical | No robot status/telemetry or dry-run-result fixture mirror. | Add only non-executing safety metadata fixtures. |
| frontend chat | Undercovered | Not separate from backend chat fixtures | High | `frontend/src/lib/chat/api.ts` body shape is not explicitly mirrored. | Add frontend chat fixture. |
| Workstation | Undercovered | Meeting launch is partially covered | High | Workstation station context and launch state are not mirrored. | Add Workstation fixture coverage. |
| SparkBud | Not covered | Not covered | Medium | SparkBud launch/prompt routes are unrepresented. | Add SparkBud fixture coverage. |
| auth/session context | Undercovered | Passive `actor_ref` / `session_ref` only | Critical | No fixture for current user/session/operator context as passive refs. | Add passive auth/session context fixtures only. |
| Token Guardian / model routing context | Not covered | Not covered | High | Sparkbot v1.6.72 reinforces routing/pacing context; no fixture mirrors Token Guardian shadow/live routing metadata or autonomous-turn pacing notes. | Add model-routing/Token Guardian context fixtures as passive metadata only. |

## What Is Covered

- neutral fixture loading
- adapter conversion to `HumanInput`
- bridge to fake pipeline
- fake lineage recording
- critical/unknown non-auto-approval
- MCP/robot non-executing posture
- no Sparkbot imports
- no execution/persistence

## What Is Not Covered

- live Sparkbot payload extraction
- real route/WebSocket data
- production adapter wiring
- model/tool execution
- real auth/session verification
- real trusted device enforcement
- real autonomy enforcement
- audit persistence
- redaction runtime
- live robot/MCP execution
- `stream_chat_with_tools` safety

## Gap Decision

GO for Phase 2.2 Fixture Coverage Expansion.

Recommended branch:

`phase-2-2-fixture-coverage-expansion`

Purpose:
Add missing fixture coverage for frontend chat, Workstation, SparkBud, passive auth/session context, and model-routing/Token Guardian/autonomous-turn pacing context if currently undercovered.

NO-GO for production Sparkbot adapter wiring.

## Still Blocked

- production Sparkbot wiring
- live route/WebSocket adapter
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

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| Fixture coverage gaps | High | Phase 2.0 tests cover six fixture categories through the fake harness. | Add focused fixture expansion before harness expansion. |
| Sparkbot payload drift | High | Drift metadata and Sparkbot origin/main checks are required. | Recheck Sparkbot before Phase 2.2 and update fixture reviewed commit. |
| Frontend payload mismatch | High | Backend chat/WebSocket fixtures exist. | Add frontend chat send-body fixture. |
| Workstation/SparkBud undercoverage | Medium | Meeting launch fixture partially covers Workstation. | Add Workstation station and SparkBud prompt fixtures. |
| MCP/robot fixture misunderstood as execution readiness | Critical | Phase 2.0 tests assert non-executing and non-auto-approval behavior. | Keep fixture expansion non-executing and documented. |
| Fake harness mistaken for production | Critical | Docs state fake harness is not production runtime. | Keep production adapter blocked. |
| Identity/session references mistaken for authority | Critical | `actor_ref` and `session_ref` remain passive refs. | Add passive context fixtures without live lookup. |

## Final Decision

GO for Phase 2.2 Fixture Coverage Expansion.

NO-GO for production Sparkbot adapter wiring.
