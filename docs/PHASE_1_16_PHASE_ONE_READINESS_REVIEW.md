# Phase 1.16 Phase One Readiness Review

## Purpose

Review Phase 1 progress and decide whether LIMA is ready for any real adapter implementation.

This review does not implement runtime behavior.
This review does not authorize production wiring.
This review does not authorize model/tool execution or real enforcement.

## Sparkbot Reference Check

| Repo | Branch | Commit | Checked paths | Modified? yes/no | Adapter-relevant changes since prior check |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `da9506151f7c45910ddf4788ed50dd989b668c4c` | `backend/app/api/routes/chat/messages.py`, `backend/app/api/routes/chat/websocket.py`, `backend/app/api/routes/chat/voice.py`, `backend/app/api/routes/chat/llm.py`, `backend/app/api/routes/chat/model.py`, `backend/app/api/routes/chat/tools.py`, `backend/app/api/routes/chat/mcp.py`, `backend/app/services/mcp_registry.py`, `backend/app/services/mcp_runs.py`, `backend/app/services/guardian/token_guardian.py`, `backend/app/api/routes/chat/robotics.py`, `backend/app/services/lima_robotics_bridge.py`, `backend/app/api/routes/terminal.py`, `backend/app/services/terminal_service.py`, `frontend/src/pages/WorkstationPage.tsx`, `frontend/src/pages/MeetingRoomPage.tsx`, `frontend/src/lib/workstationMeeting.ts`, `frontend/src/lib/sparkbudLaunch.ts`, `frontend/src/components/chat/ChatInput.tsx`, `frontend/src/pages/ChatPage.tsx`, `docs/architecture/roundtable_meeting_flow_v1.6.60.md`, `docs/capabilities.md` | No | Yes. Since the prior adapter review commit `b59041d2946e8c121e76ab9af47d1fbea4bd90cb`, Sparkbot moved through `v1.6.68` and `v1.6.69`. The relevant movement touches `backend/app/api/routes/chat/llm.py`, `backend/app/api/routes/chat/model.py`, `backend/app/services/guardian/token_guardian.py`, and `docs/capabilities.md`. The change adjusts Token Guardian bypass/reporting behavior inside `stream_chat_with_tools`, model version fallback, Token Guardian model configuration checks, and Spine event logging. This reinforces that chat/model/Guardian surfaces are still moving and must remain reference material, not production adapter code. |

Sparkbot was fetched read-only. The local Sparkbot checkout remained on `main`, tracking `origin/main`, with no modified files reported.

## What Phase 1 Has Proven

- Vault/Auth contracts exist.
- Provider boundary tests protect against Sparkbot internals.
- Fake Auth/Vault/Breakglass providers work in memory.
- Fake GuardianDecision evaluator exists.
- Fake Policy/Risk evaluator exists.
- Fake Approval recorder exists.
- Fake Spine/Audit recorder exists.
- Fake Guardian pipeline composes contracts.
- Sparkbot HumanInput adapter skeleton converts neutral payloads to HumanInput.
- HumanInput fake bridge can connect HumanInput to fake pipeline.
- Critical/unknown requests do not auto-approve in fake tests.
- Raw chat-to-tool shortcuts remain blocked.

## What Phase 1 Has Not Proven

- live Sparkbot adapter safety
- identity/session authenticity
- trusted device validation
- owner autonomy enforcement
- real IntentCompiler behavior
- real Guardian enforcement
- real policy enforcement
- real approval enforcement
- real audit persistence
- real redaction runtime
- model/tool execution safety
- terminal/PTY safety
- Robo-OS physical action safety
- production route wiring

## Readiness Decision

Decision: READY for Phase 1.17 Identity / Session / Trust Context Mapping Review.

Decision: NOT READY for production Sparkbot adapter implementation.

The next blocker is not code shape; it is verified identity/session/trusted-context mapping. The adapter skeleton currently carries `actor_ref`, `session_ref`, and `trusted_context_ref` as neutral metadata only. Before real adapter work, LIMA must define how those references map to `AuthContext`, trusted devices, owner autonomy, and privacy/redaction.

## Recommended Next Branch

`phase-1-17-identity-session-trust-context-review`

Purpose: Review and design how `actor_ref`, `session_ref`, `trusted_context_ref`, device/session confidence, and owner-autonomy hints should map into LIMA `AuthContext` / `HumanInput` metadata before any real Sparkbot adapter implementation.

## Why Not Production Adapter Yet

Production adapter is still blocked because:

- `actor_ref` is not verified identity
- `session_ref` is not verified session
- `trusted_context_ref` is passive metadata only
- `autonomy_notes` are passive metadata only
- privacy/redaction defaults are not enforced
- no audit persistence exists
- fake pipeline is not production runtime
- `stream_chat_with_tools` remains blocked

## Phase 1.17 Allowed Scope

Allowed:

- docs/design/tests only
- identity/session/trust mapping review
- AuthContext mapping proposal
- trusted device/session metadata proposal
- owner-autonomy metadata mapping proposal
- privacy/redaction mapping proposal
- no runtime implementation

NO-GO:

- live Sparkbot route wiring
- live auth/session lookup
- PIN verification
- facial/voice recognition implementation
- trusted device enforcement
- autonomy enforcement
- model/tool execution
- `stream_chat_with_tools`
- production adapter
- audit persistence

## Updated Phase 1 Roadmap Recommendation

Phase 1.17:
Identity / Session / Trust Context Mapping Review

Phase 1.18:
HumanInput AuthContext Contract Extension, if needed

Phase 1.19:
Non-production Sparkbot adapter fixture tests with fake AuthContext only

Phase 1.20:
Real adapter readiness review

Defer:

- production wiring
- model/tool execution
- real enforcement
- terminal/PTY
- Robo-OS physical action
- audit persistence

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| Fake bridge mistaken for production path | High | Bridge is documented and tested as separate from adapter and fake-pipeline-only. | Keep production wiring blocked and require Phase 1.17 identity/session review before adapter work. |
| `actor_ref` mistaken for verified identity | Critical | Adapter carries neutral metadata only. | Define mapping from Sparkbot actor evidence to LIMA `AuthContext`. |
| `trusted_context_ref` mistaken for trusted device | High | Trusted context remains passive metadata. | Define trusted device/session confidence fields before implementation. |
| `autonomy_notes` mistaken for autonomy enforcement | High | Owner autonomy notes are explicitly passive. | Map autonomy hints to future Guardian-owned policy evidence only. |
| Privacy metadata mistaken for redaction enforcement | High | Redaction/privacy contracts exist, but no runtime is implemented. | Define privacy mapping and keep audit persistence blocked. |
| Sparkbot changes before real adapter work | Medium | Sparkbot origin/main is rechecked during readiness reviews. | Recheck Sparkbot again before Phase 1.17 and any adapter fixture branch. |
| Raw chat-to-tool shortcut leakage | Critical | Adapter stops at HumanInput; bridge uses explicit test metadata only. | Keep `HumanInput -> IntentEnvelope -> GuardianDecision` as the only allowed production direction. |
| `stream_chat_with_tools` direct path | Critical | Marked do-not-extract-yet across boundary docs. | Continue to block direct extraction until intent, identity, Guardian, policy, approval, lineage, and privacy gates are designed. |

## Final Decision

GO for Phase 1.17 Identity / Session / Trust Context Mapping Review.

NO-GO for production Sparkbot adapter implementation, live auth/session lookup, model/tool execution, real enforcement, audit persistence, terminal/PTY, Robo-OS physical action, or `stream_chat_with_tools` extraction.
