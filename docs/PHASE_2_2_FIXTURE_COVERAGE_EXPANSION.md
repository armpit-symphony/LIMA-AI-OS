# Phase 2.2 Fixture Coverage Expansion

## Purpose

Expand LIMA-owned synthetic Sparkbot payload fixtures to cover gaps found in Phase 2.1.

This phase does not implement production Sparkbot wiring, live routes, model calls, tool execution, persistence, redaction runtime, or real Guardian/policy/approval enforcement.

## Sparkbot Reference Check

| Repo | Branch | Commit | Checked surfaces | Modified? yes/no | Movement since Phase 2.1 |
| --- | --- | --- | --- | --- | --- |
| Sparkbot | `main` / `origin/main` | `4a08838ba500fec4ef85c163b3249a2db80da9d6` | Frontend chat body/message variants, Workstation station/launch context, SparkBud prompt/launch context, auth/session context, Token Guardian/model-routing/autonomous-turn pacing context. | No tracked Sparkbot modifications by this task; local checkout still has untracked `scripts/file_v1_6_72_proposals.py`. | No movement since Phase 2.1. Fixture expansion used Sparkbot `origin/main` / explicit commit inspection, not dirty local files. |

## New Fixture Categories

- `frontend_chat_payloads.json`: frontend chat body/message variants, including `body`, `message`, `content`, `reply_to_id`, and `confirm_id` examples.
- `workstation_payloads.json`: Workstation station and launch-context references.
- `sparkbud_payloads.json`: SparkBud prompt and launch-draft context.
- `auth_session_context_payloads.json`: passive `actor_ref`, `session_ref`, `trusted_context_ref`, `identity_confidence_ref`, and `autonomy_context_ref`.
- `model_routing_context_payloads.json`: Token Guardian / model-routing / autonomous-turn pacing context.

## Fixture Rules

- synthetic only
- no secrets
- no real user data
- no Sparkbot imports
- no production wiring
- no execution
- fixtures are mirrors, not authority

## Passive Metadata Rules

- auth/session refs are not verified identity/session
- `trusted_context_ref` is not trusted-device proof
- autonomy metadata is not enforcement
- model-routing/token budget metadata does not call models or route anything
- autonomous pacing metadata does not start autonomous execution

## Harness Handling

Compatible text-like fixtures flow through:

```text
fixture -> SparkbotHumanInputAdapter -> HumanInput -> HumanInputFakePipelineBridge -> FakeGuardianPipeline
```

Workstation context remains console-shaped and non-executing.

Unsupported categories may be marked `unsupported_nonexecuting` in later phases. Unsupported does not mean failure when documented and tested; it means the fixture mirror is present but no execution path is opened.

MCP, robot, model-routing, and autonomous pacing fixtures remain non-executing.

## Acceptance Criteria

- new fixture files exist
- fixture metadata complete
- drift metadata present
- no secrets
- fixture tests updated
- harness tests updated
- production adapter remains blocked

## Final Decision

GO for review of expanded fixture coverage.

NO-GO for production Sparkbot adapter wiring, live routes, `stream_chat_with_tools`, `execute_tool`, model/tool execution, terminal/PTY, Robo-OS physical action, live auth/session lookup, trusted device/autonomy enforcement, audit persistence, redaction runtime, or real IntentCompiler / Guardian / policy / approval enforcement.
