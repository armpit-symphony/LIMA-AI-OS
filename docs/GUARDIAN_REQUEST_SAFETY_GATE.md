# Guardian Request Safety Gate

## Purpose

Define the standing safety gate for Guardian-request-adjacent work in LIMA-AI-OS.

This gate protects the boundary between IntentEnvelope and GuardianDecision.

## Scope

This gate applies to any PR touching:

- `lima/contracts/guardian.py`
- any future Guardian request helper
- `tests/helpers/guardian_request_fixture_harness.py`
- `tests/fixtures/guardian_requests/`
- `tests/test_guardian_request_*.py`
- `docs/GUARDIAN_DECISION_CONTRACT.md`
- Guardian request / decision / enforcement extraction docs
- any IntentEnvelope-to-Guardian-request bridge or harness

## Core Invariants

- Guardian request is not GuardianDecision.
- Guardian request is not approval.
- Guardian request is not enforcement.
- Guardian request is not execution.
- `requested_tool_packs` are requests only.
- `requested_tool_packs` are not `allowed_tool_packs`.
- `requested_tool_packs` are not `granted_tool_packs`.
- `approval_requirement_ref` is descriptive only.
- `approval_requirement_ref` is not ApprovalMetadata.
- `autonomy_context_ref` is passive only.
- privacy/redaction metadata is not enforcement.
- GuardianDecision remains mandatory before consequential behavior.
- ApprovalMetadata remains evidence only.
- no ApprovalMetadata recording is allowed in Guardian request fixtures or harnesses.
- Spine/Audit lineage records; it does not execute.
- Owner autonomy metadata does not approve or lower risk by itself.
- Human safety and law override owner command.

## Required Checks Before Merge

Required commands:

```text
python -m compileall lima
python -m pytest -q
git diff --check
```

Required tests:

- `tests/test_guardian_request_test_fixtures.py`
- `tests/test_guardian_request_fixture_harness.py`
- `tests/test_contract_imports.py`
- `tests/test_adapter_boundaries.py`
- `tests/test_intent_envelope_fixture_harness.py`

## Required Fixture Rules

- fixtures are synthetic
- no secrets
- no real user data
- `explicit_request` must describe request shape only
- `expected_guardian_request` must not imply decision or approval
- `requested_tool_packs` must not be granted/allowed
- `approval_requirement_ref` must remain descriptive
- `autonomy_context_ref` must remain passive
- privacy/redaction metadata must remain non-enforcing
- safety-critical requests require later Guardian/policy/approval review
- no GuardianDecision expected/created
- no ApprovalMetadata expected/created
- no audit persistence expected/created
- no execution expected/created

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
- production Guardian request behavior

## PR Blocking Conditions

A PR must not merge if:

- Guardian request is treated as GuardianDecision
- Guardian request is treated as approval
- `requested_tool_packs` become granted/allowed tools
- `approval_requirement_ref` becomes ApprovalMetadata
- `autonomy_context_ref` authorizes action
- privacy/redaction metadata enforces access/redaction
- safety-critical request implies approval
- `approval_required` request implies `approval_granted`
- GuardianDecision is created
- ApprovalMetadata is recorded
- audit persistence is added
- execution appears
- required Guardian request fixture tests fail

## Manual Review Requirements

Manual review required for:

- new Guardian request fields
- new request fixture categories
- new risk/action types
- `requested_tool_packs` semantics
- `approval_requirement_ref` semantics
- `autonomy_context_ref` semantics
- privacy/redaction metadata changes
- safety-critical request changes
- any GuardianDecision-related code
- any policy/approval/enforcement-adjacent code
- any request to move toward real Guardian enforcement

## Current Status

Current allowed work:

- synthetic Guardian request fixtures
- Guardian request fixture harness
- safety gate docs
- test-only review artifacts
- explicit request shape validation

Current blocked work:

- real GuardianDecision
- enforcement
- approval
- ApprovalMetadata recording
- execution
- audit persistence
- production Guardian request behavior

## Exit Criteria for Real GuardianDecision Discussion

Future real GuardianDecision discussion requires:

- explicit readiness review
- policy enforcement design
- approval enforcement design
- audit lineage design
- redaction/privacy enforcement design
- owner autonomy enforcement design
- tool-pack execution gate design
- rollback/kill switch
- security review
- Phil/operator approval
