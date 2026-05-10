# Phase 2.3 Harness Coverage Readiness Review

## Purpose

Review expanded fixture coverage and decide whether LIMA is ready for a repeatable fixture regression harness.

This review does not implement production wiring.
This review does not authorize execution.
This review does not modify Sparkbot.

## Sparkbot Reference Check

| Repo | Branch | Commit | Checked surfaces | Modified? yes/no | Adapter-relevant changes since Phase 2.2 |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `92128daef23f6ef0434972d9cb5edf83213f80da` | Chat/WebSocket, `stream_chat_with_tools`, chat model routing, voice/transcript, meeting/roundtable, SparkBud, Workstation, operator/terminal input, MCP explain-plan/run approval, robotics natural-language surfaces, frontend chat input, auth/session/user context, Token Guardian reporting/config, and Guardian policy changes related to execution gating. | No Sparkbot modifications by this LIMA task. The local checkout has untracked `scripts/file_v1_6_72_proposals.py`; previously reported `backend/app/services/guardian/policy.py` and `backend/tests/services/test_guardian_policy.py` changes are now present in Sparkbot `origin/main` as v1.6.73. | Sparkbot moved from `4a08838ba500fec4ef85c163b3249a2db80da9d6` to `92128daef23f6ef0434972d9cb5edf83213f80da`. The movement changes break-glass execution-gate policy behavior and related tests, not LIMA fixture payload shapes. Review used Sparkbot `origin/main`, not dirty local files. |

## Current Coverage Inventory

| Category | Fixture file | Harness support status | Expected HumanInput source | Fake pipeline coverage | Risk / safety notes | Non-executing posture documented? |
| --- | --- | --- | --- | --- | --- | --- |
| Chat payloads | `tests/fixtures/sparkbot_payloads/chat_payloads.json` | Supported | `text` | Yes | Unknown action is denied in fake pipeline. | Yes |
| Frontend chat payloads | `tests/fixtures/sparkbot_payloads/frontend_chat_payloads.json` | Supported | `text` | Yes | Body/message variants stay synthetic. | Yes |
| Voice/transcript payloads | `tests/fixtures/sparkbot_payloads/voice_payloads.json` | Supported | `voice` | Yes | No voice recognition or biometric verification. | Yes |
| Meeting payloads | `tests/fixtures/sparkbot_payloads/meeting_payloads.json` | Supported | `text` | Yes | Meeting refs are metadata only. | Yes |
| Operator payloads | `tests/fixtures/sparkbot_payloads/operator_payloads.json` | Supported | `console` | Yes | Terminal-shaped records are critical and non-executing. | Yes |
| Workstation payloads | `tests/fixtures/sparkbot_payloads/workstation_payloads.json` | Supported as console context | `console` | Yes | Station/launch refs do not launch production runtime. | Yes |
| SparkBud payloads | `tests/fixtures/sparkbot_payloads/sparkbud_payloads.json` | Supported as text context | `text` | Yes | Prompt/launch refs do not launch specialists. | Yes |
| Passive auth/session context payloads | `tests/fixtures/sparkbot_payloads/auth_session_context_payloads.json` | Supported as text context | `text` | Yes | References are not authority. | Yes |
| Model-routing / Token Guardian / autonomous pacing payloads | `tests/fixtures/sparkbot_payloads/model_routing_context_payloads.json` | Supported as text context | `text` | Yes | Routing metadata does not call models or start autonomous turns. | Yes |
| MCP approval payloads | `tests/fixtures/sparkbot_payloads/mcp_approval_payloads.json` | Supported as high-risk console context | `console` | Yes | Tool-call records are non-executing. | Yes |
| Robot request payloads | `tests/fixtures/sparkbot_payloads/robot_request_payloads.json` | Supported as safety-critical console context | `console` | Yes | Robot records are safety-critical and perform no physical action. | Yes |

## Coverage Readiness Matrix

| Category | Fixture present | Harness exercised | Fake pipeline exercised | Passive metadata checked | Non-executing safety checked | Gap | Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chat | Yes | Yes | Yes | Basic refs | Yes | No regression-wide runner yet | Include in Phase 2.4 regression run |
| Frontend chat | Yes | Yes | Yes | Basic refs | Yes | No aggregate drift summary | Include in Phase 2.4 regression run |
| Voice/transcript | Yes | Yes | Yes | Confidence/transcript refs | Yes | No live voice-loop coverage | Keep fixture-only; live voice remains blocked |
| Meeting/roundtable | Yes | Yes | Yes | Meeting/room refs | Yes | No live autonomous meeting extraction | Keep fixture-only; include in regression run |
| Operator/console | Yes | Yes | Yes | Session refs | Yes | No live terminal adapter | Keep terminal non-executing |
| Workstation | Yes | Yes | Yes | Station/launch refs | Yes | No live Workstation capture | Keep launch context synthetic |
| SparkBud | Yes | Yes | Yes | Source refs | Yes | No production specialist launch | Keep prompt context synthetic |
| Auth/session context | Yes | Yes | Yes | Explicit passive refs | Yes | No live AuthContext resolution | Keep refs passive |
| Model routing / Token Guardian / autonomous pacing | Yes | Yes | Yes | Routing and pacing refs | Yes | No model-routing execution safety | Keep metadata passive |
| MCP approval | Yes | Yes | Yes | Run/manifest refs | Yes | No real approval lifecycle | Keep non-executing |
| Robot request | Yes | Yes | Yes | Robot refs | Yes | No dry-run telemetry fixture | Add later only if non-executing |

## What Is Ready

- fixture metadata shape is validated
- drift metadata exists
- synthetic/no-secret checks exist
- core payload categories exist
- expanded categories exist
- harness can safely handle supported categories
- unsupported/non-executing handling exists if needed, and no current category needs hidden unsupported handling
- boundary tests protect adapters
- production adapter remains blocked

## What Is Not Ready

- live Sparkbot payload extraction
- real route/WebSocket data
- production adapter wiring
- live route/WebSocket integration
- live frontend payload capture
- real Sparkbot adapter
- model/tool execution
- real auth/session verification
- real trusted device enforcement
- real autonomy enforcement
- live robot/MCP execution
- `stream_chat_with_tools` safety
- terminal/PTY
- Robo-OS physical action
- audit persistence
- redaction runtime

## Readiness Decision

GO for Phase 2.4 Fixture Regression Harness.

Recommended branch:

`phase-2-4-fixture-regression-harness`

Purpose:
Create a test-only regression harness that loads every fixture file and runs compatible fixtures through the non-production harness, while marking unsupported/non-executing categories clearly.

NO-GO for production Sparkbot adapter wiring.

## Phase 2.4 Allowed Scope

Phase 2.4 may:

- add a fixture regression runner/test helper
- load all LIMA-owned fixture files
- run compatible categories through `AdapterFixtureHarness`
- report unsupported_nonexecuting categories
- assert no critical/unknown auto-approval
- assert no Sparkbot imports
- assert no execution/persistence

Phase 2.4 must not:

- import Sparkbot
- wire live routes
- call models/tools
- persist data
- execute terminal/robot actions
- implement real enforcement

## Still Blocked

- production Sparkbot wiring
- live WebSocket adapter
- `stream_chat_with_tools`
- `execute_tool`
- model/harness calls
- tool execution
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
| Fixture regression harness mistaken for production | Critical | Docs label harness non-production and fake-only. | Phase 2.4 must keep runner test-only. |
| Unsupported categories hidden by passing tests | High | Current categories are exercised; docs require explicit unsupported handling if added. | Phase 2.4 must report unsupported_nonexecuting status. |
| Fixture drift | High | Drift metadata and Sparkbot origin/main checks exist. | Recheck Sparkbot before each fixture update. |
| Sparkbot origin moving | High | Phase reviews record exact origin/main commit. | Continue freshness checks before regression runs. |
| Model-routing metadata mistaken for model routing | Critical | Phase 2.2 tests assert no model calls. | Regression harness must assert metadata remains passive. |
| Auth/session refs mistaken for authority | Critical | Passive context tests deny authority. | Keep no live AuthContext lookup. |
| MCP/robot fixtures mistaken for execution readiness | Critical | MCP/robot tests assert non-execution and no auto-approval. | Regression harness must keep safety-critical checks. |

## Final Decision

GO for Phase 2.4 Fixture Regression Harness.

NO-GO for production Sparkbot adapter wiring.
