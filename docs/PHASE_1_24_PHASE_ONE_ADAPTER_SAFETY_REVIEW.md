# Phase 1.24 Phase One Adapter Safety Review

## Purpose

Review Phase 1 adapter safety work and decide whether Phase 1 can close or whether more pre-Phase-2 hardening is required.

This review does not implement runtime behavior.
This review does not authorize production adapter wiring.
This review does not authorize model/tool execution.

## Sparkbot Reference Check

| Repo | Branch | Commit | Checked surfaces | Modified? yes/no | Adapter-relevant changes since prior check |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `4da833858428e076645cac8fca942205e80bcc6e` | Chat REST/WebSocket, `stream_chat_with_tools`, chat model routing, voice/transcript, meeting/roundtable, SparkBud, Workstation, operator/terminal input, MCP explain-plan/run approval, robotics natural-language surfaces, frontend chat input, auth/session/user context, and Token Guardian reporting/config surfaces related to chat/model routing. | No | No movement since the Phase 1.22 drift check. Sparkbot `origin/main` remains at `4da833858428e076645cac8fca942205e80bcc6e`; the local Sparkbot checkout was clean at review time. Existing v1.6.71 movement remains documented in Phase 1.22 and does not require another fixture/drift pass before Phase 2.0. |

## What Phase 1 Adapter Work Has Proven

- Sparkbot input can be represented as neutral payloads.
- Neutral payloads can convert to HumanInput.
- Adapter returns HumanInput only.
- HumanInput can flow into a fake pipeline via a separate test-only bridge.
- Fake AuthContext/trust fixtures can be carried passively.
- Payload fixture mirrors exist.
- Payload drift metadata exists.
- Adapter boundary tests block unsafe imports/methods.
- Production adapter remains blocked.
- Raw chat-to-tool shortcut remains blocked.

## What Phase 1 Adapter Work Has Not Proven

- production Sparkbot route integration
- live WebSocket integration
- verified identity/session resolution
- trusted device enforcement
- owner autonomy enforcement
- real IntentCompiler
- real Guardian enforcement
- real policy enforcement
- real approval enforcement
- real audit persistence
- real redaction runtime
- model/tool execution safety
- `stream_chat_with_tools` safety
- terminal/PTY safety
- Robo-OS physical action safety

## Adapter Boundary Status

Current allowed adapter methods:

- `adapt_chat_payload`
- `adapt_voice_payload`
- `adapt_meeting_payload`
- `adapt_operator_payload`

Current forbidden import coverage blocks Sparkbot runtime modules, FastAPI/WebSocket route layers, Sparkbot route/CRUD/model/service modules, model/tool execution paths, terminal/PTY/subprocess, filesystem/env/socket/network clients, persistence clients, payment/cloud/robotics/container orchestration clients, and model-provider clients.

Current forbidden method coverage blocks execution, model/tool calls, route wiring, persistence, terminal/driver/robot, IntentCompiler, GuardianDecision, approval, policy, auth, trust, autonomy, and secret methods.

Current return boundary:

- SparkbotHumanInputAdapter returns HumanInput only.
- It does not return IntentEnvelope, GuardianDecision, ApprovalMetadata, PolicyDecision, SpineEvent, or ConsequentialActionRequest.

## Fixture / Drift Status

Fixture categories:

- chat payloads
- voice/transcript payloads
- meeting payloads
- operator payloads
- MCP approval payloads
- robot request payloads

Sparkbot commit reviewed:

- `4da833858428e076645cac8fca942205e80bcc6e`

Drift metadata status:

- Fixture objects include `shape_version`, `reviewed_at`, `reviewed_against`, `drift_status`, and `drift_notes`.
- Existing fixture drift status remains current for the reviewed commit.

Dirty local worktree rule:

- Dirty local Sparkbot files are not a source of truth.
- Reviews must use Sparkbot `origin/main`, `git show origin/main:path`, an explicit reviewed commit, or a clean temporary checkout.

Fixtures are mirrors, not runtime or authority.

## Identity / Trust / Autonomy Status

- References are not authority.
- `actor_ref` is not verified identity.
- `session_ref` is not verified session.
- `trusted_context_ref` is not trusted-device proof.
- `autonomy_notes` are passive.
- Privacy metadata is not redaction enforcement.

## Readiness Decision

GO to close Phase 1 adapter safety work and define Phase 2.0 as a non-production adapter package / fixture harness only.

NO-GO for production Sparkbot adapter wiring.

## Recommended Phase 2 Start

Recommended branch:

`phase-2-0-nonproduction-adapter-fixture-harness`

Purpose:
Create a non-production fixture harness that runs LIMA-owned Sparkbot payload fixtures through:

```text
payload fixture
  -> SparkbotHumanInputAdapter
  -> HumanInput
  -> HumanInputFakePipelineBridge
  -> FakeGuardianPipeline
  -> fake lineage
```

Allowed:

- fixture-only harness
- no Sparkbot imports
- no live routes
- no production wiring
- no model/tool execution
- no persistence
- no real enforcement

## Phase 2.0 Acceptance Criteria

- uses LIMA-owned fixtures only
- adapter remains HumanInput-only
- bridge remains separate
- fake pipeline only
- critical/unknown requests do not auto-approve
- no Sparkbot imports
- no `stream_chat_with_tools`
- no `execute_tool`
- no model/harness calls
- no terminal/PTY
- no Robo-OS physical action
- no audit persistence
- no redaction runtime
- tests pass

## Still Blocked

- production Sparkbot wiring
- live route integration
- live WebSocket adapter
- `stream_chat_with_tools` extraction
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
- real IntentCompiler
- real Guardian/policy/approval enforcement

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| Production wiring creep | Critical | Adapter boundary tests block route/runtime imports and behavior-bearing methods. | Keep Phase 2.0 fixture-only. |
| Fake harness mistaken for production | High | Fake pipeline and bridge are documented as test-only and non-production. | Keep harness non-production and clearly named. |
| Fixture drift | High | Payload fixture mirrors carry drift metadata and reviewed commit references. | Recheck Sparkbot `origin/main` before Phase 2.0 and any later adapter work. |
| Sparkbot origin moving | High | Sparkbot is checked read-only at review gates. | Repeat freshness checks before fixture harness work. |
| Identity refs mistaken for authority | Critical | Phase 1.17-1.19 document and test passive references. | Keep Phase 2.0 fixture refs passive. |
| Autonomy metadata mistaken for enforcement | High | Autonomy notes are passive and boundary tests block enforcement methods. | Defer enforcement to a future explicit phase. |
| Privacy metadata mistaken for redaction | High | Privacy/redaction metadata is documented as descriptive only. | Keep redaction runtime blocked. |
| `stream_chat_with_tools` shortcut leakage | Critical | Direct shortcut extraction is blocked in docs and tests. | Continue blocking symbol imports and direct paths. |

## Final Decision

GO for Phase 2.0 Non-production Adapter Fixture Harness.

NO-GO for production Sparkbot adapter wiring, `stream_chat_with_tools`, model/tool execution, terminal/PTY, Robo-OS physical action, live auth/session lookup, trusted device/autonomy enforcement, audit persistence, redaction runtime, or real Guardian/policy/approval enforcement.
