# Phase 2.6 Fixture Regression CI Gate Docs

## Purpose

Document the fixture regression harness as a standing safety gate for future adapter-adjacent work.

This phase does not add production wiring.
This phase does not implement CI infrastructure.
This phase defines required checks and review gates.

## When This Gate Applies

The fixture regression gate must run before any PR that touches:

- `lima/adapters/`
- `lima/guardian/fixture_harness.py`
- `lima/guardian/humaninput_pipeline_fakes.py`
- `tests/fixtures/sparkbot_payloads/`
- adapter fixture tests
- payload drift metadata
- HumanInput adapter contracts
- Sparkbot payload mirror docs
- any adapter-adjacent runtime boundary

## Required Commands

Run:

```powershell
python -m compileall lima
python -m pytest -q
git diff --check
```

These tests must pass:

- `tests/test_adapter_boundaries.py`
- `tests/test_sparkbot_payload_fixture_mirror.py`
- `tests/test_nonproduction_adapter_fixture_harness.py`
- `tests/test_fixture_regression_harness.py`
- `tests/test_sparkbot_humaninput_adapter_skeleton.py`
- `tests/test_humaninput_fake_pipeline_bridge.py`

## Required Review Checks

- no Sparkbot imports
- no production route wiring
- no `stream_chat_with_tools`
- no `execute_tool`
- no model/tool/driver execution
- no terminal/PTY
- no Robo-OS physical action
- no live auth/session lookup
- no trusted device/autonomy enforcement
- no audit persistence
- no redaction runtime
- no real enforcement
- fixtures are synthetic/no secrets
- drift metadata is current
- unsupported categories are explicit
- critical/unknown paths do not auto-approve
- MCP/robot fixtures remain non-executing

## PR Blocking Conditions

A PR must not merge if:

- fixture regression fails
- adapter boundary tests fail
- Sparkbot imports are introduced
- production wiring appears
- model/tool execution appears
- critical/unknown paths auto-approve
- unsupported categories pass silently
- drift metadata is stale without review
- fixtures contain secrets/real user data
- robot/MCP fixtures imply execution readiness

## Manual Review Requirements

Manual review is still required for:

- Sparkbot origin/main drift
- payload shape changes
- new fixture categories
- new adapter methods
- identity/session/trust metadata changes
- owner autonomy metadata changes
- robot/MCP-related fixture changes
- model-routing/Token Guardian fixture changes

## Non-production Reminder

Fixture regression is not production runtime.

It does not prove:

- live Sparkbot adapter safety
- real auth/session verification
- real redaction
- real Guardian enforcement
- real tool/model execution safety
- robot physical safety

## Acceptance Criteria

- CI gate doc exists
- required tests listed
- blocking conditions listed
- manual review requirements listed
- production adapter remains blocked
- no runtime behavior added
