# Phase 1.21 Sparkbot Payload Fixture Mirror

## Purpose

Mirror current Sparkbot input payload shapes into LIMA-owned synthetic fixtures.

This helps detect payload shape drift without importing Sparkbot or wiring live routes.

This phase does not implement production adapter work, live route wiring, model calls, tool calls, terminal/PTY access, robotics execution, live auth/session lookup, trusted device enforcement, autonomy enforcement, audit persistence, redaction runtime, or real Guardian/policy/approval enforcement.

## Sparkbot Reference Commit

| Repo | Branch | Commit | Checked paths | Modified? yes/no | Adapter-relevant notes |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `f7d5ee2054794ea7156ffb51a009c058cb7757e6` | `backend/app/schemas/chat.py`, `backend/app/api/routes/chat/rooms.py`, `backend/app/api/routes/chat/websocket.py`, `backend/app/api/routes/chat/voice.py`, `backend/app/api/routes/chat/mcp.py`, `backend/app/api/routes/chat/robotics.py`, `backend/app/api/routes/terminal.py`, `frontend/src/pages/SparkbotDmPage.tsx`, `frontend/src/lib/workstationMeeting.ts`, `frontend/src/lib/mcpRegistry.ts`, `frontend/src/types/terminal.ts`, and Workstation session/context snippets. | Yes, local checkout only | `origin/main` did not move since Phase 1.20 and remains at `f7d5ee2`. The local Sparkbot worktree had pre-existing changes in chat/Spine/Guardian/frontend files plus untracked correction-lock files; LIMA did not modify Sparkbot. Fixture shapes are synthetic LIMA-owned mirrors based on `origin/main` / the checked commit, not uncommitted local dirty files or copied production request objects. |

## Fixture Rules

- synthetic data only
- no secrets
- no real user messages
- no tokens
- no private data
- no Sparkbot imports
- no route wiring
- no execution
- no model/tool calls
- fixtures are not authority
- production adapter remains blocked

## Fixture Categories

- chat payloads
- voice/transcript payloads
- meeting payloads
- operator payloads
- MCP approval payloads
- robot request payloads

Robot request payloads are safety-critical mirrors. They remain blocked, non-executing fixtures and do not call drivers, execute MCP tools, or trigger physical-world action.

## How Fixtures Are Used

Fixtures are used to test LIMA-owned adapter skeletons.

They are not production contracts.
They are not authority.
They do not verify identity/session/trust.
They do not imply runtime wiring.

The fixture tests may adapt supported shapes through `SparkbotHumanInputAdapter`, but the adapter still returns `HumanInput` only. It does not create `IntentEnvelope`, `GuardianDecision`, `ApprovalMetadata`, `PolicyDecision`, `SpineEvent`, or any execution path.

## Drift Policy

Before any real adapter work:

- re-run Sparkbot inspection
- compare payload fixture mirror with current Sparkbot shapes
- update fixtures if needed
- do not wire production routes until reviewed

## Acceptance Criteria

- fixture files exist
- fixtures use synthetic data only
- Sparkbot commit recorded
- no Sparkbot imports
- adapter tests use or can use fixtures
- no runtime behavior added
