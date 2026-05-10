# Phase 1.20 Real Adapter Readiness Review

## Purpose

Review whether LIMA is ready for any real Sparkbot adapter implementation.

This review does not implement production wiring.
This review does not modify Sparkbot.
This review does not authorize model/tool execution.

## Sparkbot Reference Check

| Repo | Branch | Commit | Checked paths/surfaces | Modified? yes/no | Adapter-relevant changes since prior check |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `f7d5ee2054794ea7156ffb51a009c058cb7757e6` | Chat REST/WebSocket, `stream_chat_with_tools`, chat model routing, voice/transcript, meeting/roundtable, SparkBud, Workstation, operator/terminal input, MCP explain-plan/run approval, robotics natural-language surfaces, frontend chat input, auth/session/user context, Token Guardian reporting/config checks, Command Center / Spine / Guardian frontend client paths, and `docs/capabilities.md`. Representative diff paths since the prior `da9506151f7c45910ddf4788ed50dd989b668c4c` check include `docs/capabilities.md`, `frontend/src/lib/spine.ts`, `frontend/src/routes/_layout/index.tsx`, release notes, downloader docs, package/version metadata, and Tauri config. | No | Sparkbot moved from v1.6.69 to v1.6.70. The movement is mainly Command Center Inspector / Spine / Guardian frontend API routing: `spineGet`, `guardianFetch`, `roomsFetch`, dashboard summary, and dashboard approval actions moved from raw `fetch` to `apiFetch` for Tauri desktop origin handling and chat-token bearer injection. No backend chat, WebSocket, voice, meeting, Workstation, MCP, terminal, robotics, or `stream_chat_with_tools` files changed in the inspected diff. The movement still affects operator-facing Guardian/Spine visibility and reinforces the need to mirror payload and UI-context fixtures before live adapter work. |

Sparkbot was fetched read-only. The local Sparkbot checkout remained on `main`, tracking `origin/main`, with no modified files reported.

## What Is Ready

- neutral payload-to-HumanInput skeleton
- describe-only adapter contracts
- fake pipeline contract proof
- fake AuthContext/trust fixture tests
- owner autonomy policy
- blocked shortcut documentation
- boundary tests

## What Is Not Ready

- production route wiring
- live Sparkbot request object adaptation
- verified identity/session mapping
- trusted device enforcement
- autonomy enforcement
- real IntentCompiler
- real Guardian/policy/approval enforcement
- audit persistence
- redaction runtime
- model/tool execution
- terminal/PTY
- Robo-OS physical action

## Readiness Decision

NO-GO for production Sparkbot adapter wiring.

GO only for Phase 1.21 non-production Sparkbot payload fixture mirror.

Reason:
Phase 1.19 proved that fake AuthContext/trust references can be carried passively through adapter fixture tests. It did not prove that live Sparkbot request, WebSocket, UI session, Guardian/Spine, or chat/model-routing surfaces are stable enough for production wiring. Sparkbot moved again after the prior check, and the latest movement touched Command Center / Spine / Guardian frontend API routing. That is not live adapter surface implementation, but it is close enough to operator-facing context and Guardian visibility that LIMA should first mirror current Sparkbot payload and context shapes in LIMA-owned fixtures.

## Why Production Adapter Remains Blocked

- actor/session/trust refs remain metadata, not verified authority
- no live AuthContext resolution exists
- no real redaction enforcement exists
- no audit persistence exists
- fake pipeline is not production runtime
- `stream_chat_with_tools` remains blocked
- Sparkbot chat/model and operator-facing Guardian/Spine surfaces have moved and require stable fixture mirroring before live integration

## Possible Safe Next Branch Options

Option A:
`phase-1-21-sparkbot-payload-fixture-mirror`

Purpose:
Create LIMA-owned test fixtures mirroring the shape of Sparkbot chat/voice/meeting/operator payloads based on latest Sparkbot inspection, without importing Sparkbot.

Option B:
`phase-1-21-adapter-boundary-hardening`

Purpose:
Add stronger tests preventing Sparkbot route/request imports, `stream_chat_with_tools`, `execute_tool`, WebSocket, FastAPI, terminal/PTY, and runtime modules from entering adapters.

Option C:
`phase-1-21-identity-session-contract-fixtures`

Purpose:
Add more fake identity/session/trust fixture coverage before real adapter work.

Recommended next branch:
`phase-1-21-sparkbot-payload-fixture-mirror`

Rationale:
Sparkbot moved recently. The backend adapter-critical files did not change, but Command Center / Spine / Guardian frontend API routing and capability docs did. The safest next step is to build LIMA-owned payload/context fixtures from the current Sparkbot inspection before any real adapter decision.

## Phase 1.21 Allowed Scope

- test fixtures only
- no Sparkbot imports
- no production wiring
- mirror payload shape using LIMA-owned dataclasses or JSON fixtures
- update adapter tests if needed
- no behavior change

## Still Blocked

- production Sparkbot wiring
- live route integration
- WebSocket adapter
- `stream_chat_with_tools`
- `execute_tool`
- model/harness calls
- tool execution
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device enforcement
- autonomy enforcement
- audit persistence
- redaction runtime
- real enforcement

## Risk Register

| Risk | Severity | Mitigation | Next action |
| --- | --- | --- | --- |
| Sparkbot payload shape drift | High | Keep Sparkbot as the spec and recheck `origin/main` before adapter work. | Build LIMA-owned payload fixture mirror from current Sparkbot shapes. |
| Accidental Sparkbot imports | High | Existing boundary tests block Sparkbot/backend imports in LIMA adapter paths. | Add fixture mirror tests without importing Sparkbot. |
| Production wiring creep | High | Keep adapter work behind explicit readiness gates and docs decisions. | Keep Phase 1.21 test-only. |
| `stream_chat_with_tools` shortcut leakage | Critical | Raw chat-to-tool shortcuts remain blocked in docs and tests. | Continue blocking direct extraction and symbol imports. |
| Identity/session references mistaken for authority | High | Phase 1.17-1.19 document and test references as passive. | Keep fixtures explicit that refs do not verify identity/session. |
| Fake pipeline mistaken for production | High | Bridge remains separate, fake-only, and non-production. | Do not connect adapter to fake pipeline outside tests. |
| Privacy metadata mistaken for redaction enforcement | High | Privacy metadata is documented as a hint only. | Defer real redaction runtime until reviewed. |

## Final Decision

GO for Phase 1.21 Sparkbot payload fixture mirror.

NO-GO for production Sparkbot adapter implementation.
