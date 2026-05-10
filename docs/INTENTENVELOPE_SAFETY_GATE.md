# IntentEnvelope Safety Gate

## Purpose

Define the standing safety gate for all IntentEnvelope-adjacent work in LIMA-AI-OS.

This gate protects the boundary between HumanInput and GuardianDecision.

## Scope

This gate applies to any PR touching:

- `lima/contracts/intent.py`
- any future IntentCompiler code
- `tests/helpers/intent_envelope_fixture_harness.py`
- `tests/fixtures/intent_envelopes/`
- `tests/test_intent_envelope_*.py`
- `docs/INTENT_COMPILER_BOUNDARY.md`
- IntentEnvelope-related extraction/runtime docs
- any HumanInput-to-IntentEnvelope bridge or harness

## Core Invariants

- HumanInput is not IntentEnvelope.
- IntentEnvelope is not authorization.
- GuardianDecision remains mandatory before consequential behavior.
- `raw_text` is inert unless a future explicitly approved real IntentCompiler phase exists.
- Explicit typed metadata is required for test IntentEnvelope fixtures.
- No hidden parser.
- No heuristic free-text interpretation.
- No model call.
- No tool execution.
- No GuardianDecision creation from adapter.
- Adapter remains HumanInput-only.
- Owner autonomy metadata is passive.
- References are not authority.
- Safety-critical intent requires later Guardian/policy/approval review.

## Required Checks Before Merge

Required commands:

```text
python -m compileall lima
python -m pytest -q
git diff --check
```

Required tests:

- `tests/test_intent_envelope_test_fixtures.py`
- `tests/test_intent_envelope_fixture_harness.py`
- `tests/test_contract_imports.py`
- `tests/test_adapter_boundaries.py`

## Required Fixture Rules

- fixtures are synthetic
- no secrets
- no real user data
- `raw_text` is inert
- valid fixtures require `explicit_metadata`
- invalid fixtures must not imply envelope creation
- clarification fixtures must remain `clarification_needed`
- safety-critical fixtures must mention later Guardian/policy/approval review
- no GuardianDecision expected/created

## Forbidden Behaviors

- real IntentCompiler implementation
- natural-language inference
- `raw_text` parsing
- model calls
- hidden parser
- heuristic free-text interpretation
- tool execution
- GuardianDecision creation
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device/autonomy enforcement
- audit persistence
- redaction runtime
- real Guardian / policy / approval enforcement

## PR Blocking Conditions

A PR must not merge if:

- `raw_text` is parsed or interpreted
- IntentEnvelope is treated as authorization
- GuardianDecision is created from adapter
- model/tool execution appears
- real IntentCompiler behavior appears without approved phase
- safety-critical fixture implies approval
- owner autonomy metadata grants approval/risk reduction
- references are treated as authority
- required intent fixture tests fail

## Manual Review Requirements

Manual review required for:

- new IntentEnvelope fields
- changes to IntentEnvelope status/risk/approval metadata
- new intent fixture categories
- any IntentCompiler-related code
- any HumanInput-to-IntentEnvelope bridge
- any natural-language handling
- safety-critical intent changes
- owner autonomy intent metadata
- requested tool pack metadata
- `evidence_refs` / `lineage_id` semantics

## Current Status

Current allowed work:

- synthetic fixtures
- fixture harness
- safety gate docs
- test-only report/review artifacts
- explicit metadata validation

Current blocked work:

- real IntentCompiler
- natural-language inference
- execution
- GuardianDecision creation
- production wiring

## Exit Criteria for Real IntentCompiler Discussion

Future real IntentCompiler discussion requires:

- explicit readiness review
- model/no-model decision
- natural-language inference safety design
- clarification UX design
- redaction/privacy design
- Guardian/policy/approval integration design
- audit lineage design
- eval tests
- rollback/kill switch
- Phil/operator approval
