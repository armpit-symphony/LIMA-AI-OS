# Fake GuardianDecision Safety Gate

## Purpose

Define the standing safety gate for fake GuardianDecision-adjacent work in LIMA-AI-OS.

This gate protects the boundary between fake/test decision artifacts and real production GuardianDecision authority.

## Scope

This gate applies to any PR touching:

- `tests/helpers/fake_guardiandecision_fixture_harness.py`
- `tests/fixtures/fake_guardian_decisions/`
- `tests/test_fake_guardiandecision_*.py`
- `docs/GUARDIAN_DECISION_CONTRACT.md`
- `docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md`
- fake GuardianDecision phase docs
- any future fake decision helper, fixture, report, or harness

## Core Invariants

- Fake GuardianDecision is test-only.
- Fake GuardianDecision is not real GuardianDecision.
- Fake GuardianDecision is not production authorization.
- Fake GuardianDecision is not approval.
- Fake GuardianDecision is not enforcement.
- Fake GuardianDecision is not execution.
- `allow_test_only` is not production allow.
- `deny_test_only` is test-only denial shape.
- `needs_approval_test_only` is not approval granted.
- `approval_ref` is not ApprovalMetadata.
- `requires_approval` is not approval granted.
- `blocked_test_only` must remain non-executing.
- safety-critical fake decisions must not auto-approve.
- expired/revoked/superseded fake decisions are not executable.
- requested/tool_pack refs are not granted tool access.
- owner autonomy metadata cannot approve by itself.
- trusted context metadata cannot approve by itself.
- privacy/redaction metadata is not enforcement.
- fake harness is not real Guardian.
- real GuardianDecision remains blocked.
- ApprovalMetadata remains separate evidence only.
- Spine/Audit records; it does not execute.
- Human safety and law override owner command.

## Required Checks Before Merge

Required commands:

```text
python3 -m compileall lima
python3 -m pytest -q
git diff --check
```

Required tests:

- `tests/test_fake_guardiandecision_test_fixtures.py`
- `tests/test_fake_guardiandecision_fixture_harness.py`
- `tests/test_guardian_request_fixture_harness.py`
- `tests/test_guardian_request_test_fixtures.py`
- `tests/test_contract_imports.py`
- `tests/test_adapter_boundaries.py`

## Required Fixture Rules

- fixtures are synthetic
- no secrets
- no real user data
- fake decision statuses must be test-only
- `expected_fake_guardian_decision` must not imply production authority
- `allow_test_only` must say not production authorization
- `needs_approval_test_only` must not imply approval granted
- `approval_ref` must remain reference-only
- no ApprovalMetadata expected/created
- no GuardianDecision expected/created
- no audit persistence expected/created
- no execution expected/created
- safety-critical fixtures require later Guardian/policy/approval review
- expired/revoked/superseded fixtures are non-executable

## Required Harness Rules

- harness is test-only
- harness validates fixture shape only
- harness validates test-only statuses only
- harness must not create real GuardianDecision
- harness must not enforce policy
- harness must not record ApprovalMetadata
- harness must not approve actions
- harness must not execute tools
- harness must not call models
- harness must not persist audit data
- harness must not call Sparkbot
- harness must not infer from `raw_text`

## Forbidden Behaviors

- real GuardianDecision creation
- Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- real IntentCompiler
- natural-language inference
- `raw_text` parsing
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device enforcement
- autonomy enforcement
- redaction runtime
- production GuardianDecision behavior

## PR Blocking Conditions

A PR must not merge if:

- fake GuardianDecision is treated as real GuardianDecision
- fake GuardianDecision is treated as production authorization
- `allow_test_only` is treated as production allow
- `needs_approval_test_only` is treated as approval granted
- `approval_ref` becomes ApprovalMetadata
- ApprovalMetadata is recorded
- safety-critical fake decision auto-approves
- expired/revoked/superseded fake decision becomes executable
- owner autonomy metadata grants approval
- trusted context metadata grants approval
- requested/tool_pack refs are granted tool access
- audit persistence is added
- execution appears
- required fake GuardianDecision fixture tests fail
- required fake GuardianDecision harness tests fail

## Manual Review Requirements

Manual review required for:

- new fake GuardianDecision fields
- new `decision_status` values
- changes to allow/deny/blocked/approval semantics
- new fake decision fixture categories
- safety-critical decision changes
- `approval_ref` semantics
- `policy_refs` semantics
- `tool_pack_refs` semantics
- owner autonomy / trusted context metadata
- lifecycle decision semantics: expired/revoked/superseded
- any GuardianDecision-related code
- any request to move toward real GuardianDecision or enforcement

## Current Status

Current allowed work:

- synthetic fake GuardianDecision fixtures
- fake GuardianDecision fixture harness
- safety gate docs
- test-only review artifacts
- fake decision shape validation

Current blocked work:

- real GuardianDecision
- enforcement
- approval
- ApprovalMetadata recording
- execution
- audit persistence
- production GuardianDecision behavior

## Exit Criteria for Real GuardianDecision Discussion

Future real GuardianDecision discussion requires:

- explicit readiness review
- policy enforcement design
- approval enforcement design
- audit lineage design
- redaction/privacy enforcement design
- owner autonomy enforcement design
- tool-pack execution gate design
- fake-to-real migration plan
- rollback/kill switch
- security review
- Phil/operator approval
