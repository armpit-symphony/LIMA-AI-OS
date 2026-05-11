# Phase 2.26 Guardian Request Safety Gate Docs

## Purpose

Create `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` as the standing gate for Guardian-request-adjacent work.

## What Was Consolidated

- request-vs-decision boundary
- request-vs-approval boundary
- fixture rules
- harness rules
- requested tool pack rules
- approval/autonomy reference rules
- forbidden behaviors
- PR blockers
- manual review requirements

## Decision

Guardian Request Safety Gate is now the standing review gate for Guardian-request-adjacent work.

Real GuardianDecision remains blocked.

## Non-Goals

- no real GuardianDecision
- no enforcement
- no approval
- no execution
- no audit persistence
- no production wiring

## Acceptance Criteria

- `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` exists
- tests validate safety gate doc
- no runtime behavior added
- real GuardianDecision remains blocked
- tests pass
