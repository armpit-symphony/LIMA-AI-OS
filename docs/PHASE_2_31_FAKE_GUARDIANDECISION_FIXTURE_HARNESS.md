# Phase 2.31 Fake GuardianDecision Fixture Harness

## Purpose

Create a test-only fixture harness for fake GuardianDecision-shaped fixtures.

This validates fake decision fields and test-only statuses without creating real GuardianDecision or enforcing anything.

## Harness Path

```text
Fake GuardianDecision fixture file
  -> fixture loader
  -> fake decision shape validator
  -> test-only status validator
  -> FakeGuardianDecisionFixtureReport
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

- Fake GuardianDecision is not real GuardianDecision.
- Fake GuardianDecision is not production authorization.
- `allow_test_only` is not production allow.
- `approval_ref` is not ApprovalMetadata.
- `requires_approval` is not approval granted.
- safety-critical fake decisions do not auto-approve.
- expired/revoked/superseded fixtures are not executable.

## Safety-Critical Rules

Safety-critical fake decision fixtures are non-authorizing.

Robot, terminal, secret, payment, deploy, admin, filesystem delete, and destructive decisions require later Guardian/policy/approval review.

Human safety and law override owner command.

## Acceptance Criteria

- harness helper exists under tests/helpers
- tests load all fake GuardianDecision fixtures
- fake decision shapes validate
- all statuses are test-only
- `allow_test_only` remains non-production
- needs_approval remains non-approving
- safety-critical fixtures remain non-authorizing
- expired/revoked/superseded remain non-executable
- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- tests pass
