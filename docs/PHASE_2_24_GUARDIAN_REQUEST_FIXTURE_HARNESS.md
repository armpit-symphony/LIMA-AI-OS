# Phase 2.24 Guardian Request Fixture Harness

## Purpose

Create a test-only fixture harness for Guardian request-shaped fixtures.

This validates explicit Guardian request fields and expected request shapes without creating GuardianDecision or enforcing anything.

## Harness Path

```text
Guardian request fixture file
  -> fixture loader
  -> explicit request validator
  -> expected request shape validator
  -> GuardianRequestFixtureReport
```

## Non-Goals

- no real GuardianDecision
- no Guardian enforcement
- no policy enforcement
- no approval enforcement
- no ApprovalMetadata recording
- no action approval
- no tool execution
- no model calls
- no audit persistence
- no real IntentCompiler
- no natural-language inference
- no Sparkbot imports
- no production behavior

## Boundary Rules

- Guardian request is not GuardianDecision.
- Guardian request is not approval.
- `requested_tool_packs` are requests only.
- `approval_requirement_ref` is descriptive only.
- `autonomy_context_ref` is passive only.
- privacy/redaction metadata is not enforcement.

## Safety-Critical Rules

Safety-critical request fixtures are non-authorizing.

Terminal, robot, secret, payment, deploy, admin, filesystem delete, and destructive requests require later Guardian/policy/approval review.

## Acceptance Criteria

- harness helper exists under tests/helpers
- tests load all Guardian request fixtures
- valid fixtures validate request shape
- invalid fixtures stay non-valid
- safety-critical fixtures remain non-authorizing
- approval-required fixtures remain descriptive
- no GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass
