# Phase 1.4 Guardian Decision Fake Evaluator

## Purpose

Define a fake, in-memory Guardian decision evaluator for contract tests.

It turns `ConsequentialActionRequest` into `GuardianDecision` without executing anything.

## Non-Goals

- no real Guardian enforcement
- no production policy
- no tool execution
- no model calls
- no driver calls
- no auth enforcement
- no approval enforcement
- no breakglass enforcement
- no Sparkbot integration
- no Guardian Suite implementation copied

## Fake Evaluator Rules

- low risk may approve
- medium risk may approve or require confirmation depending fake config
- high risk requires confirmation or review
- critical risk requires operator PIN or breakglass-style decision status
- terminal, robot, payment, deploy, and secret access requests are critical-like paths
- unknown action is denied or escalated

These are deterministic test rules only. They are not production policy.

## Decision Records

The fake evaluator records `GuardianDecision` metadata in memory only.

Decision records are useful for tests and future adapter shape.

## Safety Rules

- Fake decisions do not authorize real execution.
- Fake decisions do not replace `ApprovalMetadata`.
- Fake decisions do not replace `ToolPackRiskPolicy`.
- Fake decisions do not execute tools.
- Fake decisions must still carry `decision_id`.

## Future Path

Future real Guardian evaluator must be implemented separately after:

- policy enforcement design
- approval enforcement design
- audit lineage emission
- redaction/privacy implementation
- Sparkbot adapter review
