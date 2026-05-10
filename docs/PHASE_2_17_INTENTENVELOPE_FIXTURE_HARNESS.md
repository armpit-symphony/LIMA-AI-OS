# Phase 2.17 IntentEnvelope Fixture Harness

## Purpose

Create a test-only fixture harness for IntentEnvelope-shaped fixtures.

This validates explicit typed metadata and expected envelope shapes without implementing real IntentCompiler.

## Harness Path

```text
IntentEnvelope fixture file
  -> fixture loader
  -> explicit metadata validator
  -> expected envelope shape validator
  -> IntentEnvelopeFixtureReport
```

## Non-Goals

- no real IntentCompiler
- no natural-language inference
- no raw_text parsing
- no model calls
- no tool execution
- no GuardianDecision creation
- no production behavior
- no Sparkbot imports
- no audit persistence

## raw_text Rule

`raw_text` is inert fixture text only.

The harness must never parse `raw_text` to infer intent.

## Explicit Metadata Rule

Only `explicit_metadata` drives expected envelope validation.

The harness validates fixture shape and required explicit metadata fields. It does not translate, clarify, revise, approve, authorize, execute, persist, or enforce policy.

## IntentEnvelope Is Not Authorization

IntentEnvelope fixtures do not approve action.

Safety-critical fixtures require later Guardian/policy/approval review.

Guardian remains mandatory before any consequential behavior.

## Acceptance Criteria

- harness helper exists under `tests/helpers`
- tests load all intent fixtures
- typed fixtures validate explicit metadata
- invalid/clarification fixtures stay non-valid
- safety-critical fixtures remain non-authorizing
- `raw_text` remains inert
- no runtime behavior added
