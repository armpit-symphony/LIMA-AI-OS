# Adapter Safety Gate

## Purpose

Define the standing safety gate required before any adapter-adjacent work in LIMA-AI-OS.

This gate protects the HumanInput-first architecture and prevents production wiring creep.

## Scope

This gate applies to any PR touching:

- `lima/adapters/`
- `lima/guardian/fixture_harness.py`
- `lima/guardian/humaninput_pipeline_fakes.py`
- `tests/fixtures/sparkbot_payloads/`
- adapter fixture tests
- payload drift metadata
- fixture regression helpers
- fixture regression report helpers
- HumanInput adapter contracts
- Sparkbot payload mirror docs
- any adapter-adjacent runtime boundary

## Core Invariants

- Sparkbot input becomes HumanInput first.
- Adapter returns HumanInput only.
- Bridge remains separate from adapter.
- References are not authority.
- Fixtures are mirrors, not runtime.
- Fake pipeline is not production runtime.
- Regression report is not audit persistence.
- `gate_status` is not production approval.
- Production adapter remains NO-GO unless a future explicitly approved phase changes that.
- Guardian remains mandatory.
- Human safety and law override owner command.

## Required Checks Before Merge

Required commands:

```powershell
python -m compileall lima
python -m pytest -q
git diff --check
```

Required tests:

- `tests/test_adapter_boundaries.py`
- `tests/test_sparkbot_payload_fixture_mirror.py`
- `tests/test_nonproduction_adapter_fixture_harness.py`
- `tests/test_fixture_regression_harness.py`
- `tests/test_fixture_regression_report_artifact.py`
- `tests/test_fixture_regression_gate_docs.py`
- `tests/test_sparkbot_humaninput_adapter_skeleton.py`
- `tests/test_humaninput_fake_pipeline_bridge.py`

## Required Sparkbot Freshness Check

Before adapter-adjacent work, reviewers must:

- fetch Sparkbot `origin/main`
- record commit
- ignore dirty local Sparkbot files unless explicitly reviewing them
- document whether `origin/main` moved
- inspect adapter-relevant surfaces if moved
- never use dirty local files as source of truth

Adapter-relevant surfaces:

- chat/WebSocket
- `stream_chat_with_tools`
- chat model routing
- voice/transcript
- meeting/roundtable
- SparkBud
- Workstation
- operator/terminal input
- MCP explain-plan/run approval
- robotics natural-language surfaces
- frontend chat input
- auth/session/user context
- Token Guardian reporting/config if related to chat/model routing
- break-glass / Guardian changes if they affect adapter safety assumptions

## Forbidden Imports

- Sparkbot
- sparkbot
- backend.app
- app.crud
- app.models
- app.services
- app.api.routes
- FastAPI
- WebSocket
- APIRouter
- Request
- Depends
- ChatUser
- stream_chat_with_tools
- execute_tool
- terminal
- pty
- subprocess
- os.system
- requests
- httpx
- aiohttp
- sqlite
- sqlalchemy
- redis
- boto3
- stripe
- Robo
- robo
- LIMA-Robo-OS
- unitree
- docker
- kubernetes
- openai
- anthropic
- google.generativeai

## Forbidden Behaviors

- production Sparkbot route wiring
- live WebSocket adapter
- `stream_chat_with_tools` extraction
- `execute_tool` integration
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
- real Guardian enforcement
- real policy enforcement
- real approval enforcement
- file/DB/network side effects
- secret access
- payment/deploy/admin actions

## Required Fixture Rules

- fixtures are synthetic
- fixtures are LIMA-owned mirrors
- fixtures are not authority
- no real user data
- no secrets/tokens/API keys
- drift metadata required
- Sparkbot `origin/main` or explicit reviewed commit required
- dirty Sparkbot local worktree is not source of truth

## Required Regression Report Rules

- report must include gate fields
- report must show failed count/results
- report must show `unsupported_nonexecuting` count/results
- report must include `production_adapter_status`
- `production_adapter_status` defaults to blocked
- `gate_status` does not authorize production adapter work
- report is not audit persistence
- report is not production telemetry
- report is not Guardian evidence
- report is not production authorization
- report is not runtime state

## PR Blocking Conditions

A PR must not merge if:

- adapter boundary tests fail
- fixture regression fails
- payload drift metadata is stale without review
- Sparkbot imports are introduced
- production wiring appears
- model/tool execution appears
- terminal/PTY path appears
- robot/MCP fixtures imply execution readiness
- critical/unknown paths auto-approve
- unsupported categories pass silently
- fixtures contain secrets or real user data
- report `gate_status` hides failures
- references are treated as authority

## Manual Review Requirements

Manual review required for:

- new adapter methods
- new fixture categories
- payload shape changes
- Sparkbot `origin/main` movement
- identity/session/trust metadata changes
- owner autonomy metadata changes
- model-routing / Token Guardian fixture changes
- MCP/robot-related fixture changes
- any loosening of forbidden imports/behaviors
- any request to move toward production adapter wiring

## Current Production Adapter Status

Production adapter is NO-GO.

The only allowed current work is:

- synthetic fixtures
- fixture drift review
- fixture regression
- review artifacts
- documentation
- tests
- non-production harness work

## Exit Criteria for Future Production Adapter Discussion

Production adapter discussion may only reopen after a future explicit readiness review that addresses:

- stable Sparkbot payload surface
- verified identity/session mapping
- trusted device resolution
- owner autonomy enforcement design
- redaction/privacy enforcement
- real IntentCompiler design
- Guardian/policy/approval enforcement design
- audit persistence design
- rollback/kill switch
- security review
- Phil/operator approval
