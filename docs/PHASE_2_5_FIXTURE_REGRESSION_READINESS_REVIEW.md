# Phase 2.5 Fixture Regression Readiness Review

## Purpose

Review whether the Phase 2.4 fixture regression harness is ready to become a standing safety gate for future adapter work.

This review does not implement production wiring.
This review does not authorize execution.
This review does not modify Sparkbot.

## Sparkbot Reference Check

| Repo | Branch | Commit | Checked surfaces | Modified? | Fixture-relevant changes since Phase 2.4 |
| --- | --- | --- | --- | --- | --- |
| `armpit-symphony/Sparkbot` | `origin/main` | `92128daef23f6ef0434972d9cb5edf83213f80da` | chat/WebSocket, `stream_chat_with_tools`, chat model routing, voice/transcript, meeting/roundtable, SparkBud, Workstation, operator/terminal input, MCP explain-plan/run approval, robotics natural-language surfaces, frontend chat input, auth/session/user context, Token Guardian reporting/config | Yes, local worktree has dirty files; origin/main was used as source of truth | None. `origin/main` did not move from the Phase 2.4 baseline. |

Local Sparkbot dirty files observed during this review:

- `backend/app/api/routes/chat/tools.py`
- `backend/tests/api/routes/test_chat_server_ops.py`
- `scripts/file_v1_6_72_proposals.py`

These local files were not used as fixture authority and were not modified by this review.

## Current Regression Harness Status

| Metric | Value |
| --- | --- |
| Fixture count | 19 |
| Executed count | 19 |
| `unsupported_nonexecuting` count | 0 |
| Failed count | 0 |

Fixture categories covered:

- chat payloads
- frontend chat payloads
- voice/transcript payloads
- meeting payloads
- operator payloads
- Workstation payloads
- SparkBud payloads
- passive auth/session context payloads
- model-routing / Token Guardian / autonomous pacing payloads
- MCP approval payloads
- robot request payloads

Status summary:

- All fixtures are LIMA-owned synthetic mirrors.
- Critical and unknown paths avoid auto-approval.
- MCP and robot fixtures remain non-executing.
- Model-routing metadata remains passive and does not call models.
- Auth/session refs remain passive and do not verify authority.
- `unsupported_nonexecuting` is `0` because all current fixture categories have a safe non-production harness path, not because unsupported categories are hidden.

## What The Harness Proves

- LIMA-owned fixture files can load.
- Fixtures have required metadata.
- Fixtures are synthetic and contain no obvious secrets.
- Compatible fixtures flow through `AdapterFixtureHarness`.
- Compatible fixtures flow through `SparkbotHumanInputAdapter -> HumanInput -> HumanInputFakePipelineBridge -> FakeGuardianPipeline`.
- Fake lineage is produced.
- Unsupported categories cannot pass silently.
- Critical and unknown paths do not auto-approve.
- Boundary tests protect adapter imports and methods.

## What The Harness Does Not Prove

- production Sparkbot adapter safety
- live route/WebSocket behavior
- real Sparkbot request object shape
- real auth/session verification
- trusted device enforcement
- owner autonomy enforcement
- real IntentCompiler behavior
- real Guardian/policy/approval enforcement
- model/tool execution safety
- terminal/PTY safety
- Robo-OS physical action safety
- audit persistence
- redaction runtime

## Safety Gate Decision

GO to make fixture regression a required precondition for future adapter expansion.

NO-GO for production Sparkbot adapter wiring.

The regression harness is strong enough to act as a standing safety gate for fixture-backed adapter-adjacent work because it exercises every current LIMA-owned fixture, keeps unsupported handling explicit, and verifies the core non-execution posture. It remains insufficient as proof of production runtime safety.

## Proposed Future Gate

Before any future adapter expansion or adapter-adjacent PR:

- fixture regression tests must pass
- adapter boundary tests must pass
- payload drift metadata must be current
- Sparkbot origin/main must be rechecked if adapter-relevant
- production wiring remains blocked unless separately approved

## Recommended Next Branch

Recommended branch:

`phase-2-6-fixture-regression-ci-gate-docs`

Purpose:

Document the fixture regression harness as a standing safety gate and add any lightweight test marker or README guidance needed.

Alternative if new gaps appear before Phase 2.6:

`phase-2-6-fixture-regression-gap-hardening`

## Still Blocked

- production Sparkbot wiring
- live routes/WebSocket adapter
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
| Fixture regression harness mistaken for production | High | Docs and helper mark it test-only and non-production | Phase 2.6 should document it as a safety gate, not runtime |
| Fixture drift | High | Drift metadata and Sparkbot origin/main checks | Keep origin/main rechecks before adapter-adjacent work |
| Sparkbot origin moving | Medium | Phase reviews record inspected commits | Recheck origin/main when payload surfaces are relevant |
| Unsupported category hidden by tests | High | Unknown surfaces produce `unsupported_nonexecuting` with a reason | Keep unsupported counts visible in regression reporting |
| MCP/robot fixtures mistaken for execution readiness | High | Tests assert no auto-approval and non-executing metadata | Keep MCP/robot language explicit in docs and tests |
| Identity refs mistaken for authority | High | Auth/session fixtures remain passive | Keep live auth/session lookup blocked |
| Autonomy/privacy metadata mistaken for enforcement | High | Metadata remains passive and no redaction runtime exists | Keep real enforcement and persistence blocked |

## Final Decision

GO for Phase 2.6 Fixture Regression CI Gate Docs.

NO-GO for production Sparkbot adapter wiring.
