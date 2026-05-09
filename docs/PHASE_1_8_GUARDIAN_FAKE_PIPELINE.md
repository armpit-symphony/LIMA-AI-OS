# Phase 1.8 Guardian Fake Pipeline

## Purpose

Create a fake, in-memory Guardian pipeline for contract tests.

It proves `PolicyDecision`, `GuardianDecision`, `ApprovalMetadata`, and Spine/Audit lineage contracts fit together.

It does not enforce policy.
It does not authorize execution.
It does not execute tools, models, or drivers.
It does not persist audit data.
It does not integrate with Sparkbot.

## Pipeline

```text
ConsequentialActionRequest
  -> FakePolicyRiskEvaluator
  -> FakeGuardianDecisionEvaluator
  -> FakeApprovalRecorder when needed
  -> FakeSpineAuditRecorder
  -> FakeGuardianPipelineResult
```

The fake pipeline records policy, Guardian, approval, and lineage metadata in memory only.

## Non-Goals

- no real Guardian enforcement
- no real policy enforcement
- no real approval enforcement
- no tool execution
- no model calls
- no driver calls
- no Sparkbot adapter
- no Guardian Suite implementation copied
- no audit persistence
- no DB/storage
- no raw sensitive data persistence
- no production use

## Safety Rules

- Fake decisions are not production authorization.
- `PolicyDecision` does not replace `GuardianDecision`.
- `ApprovalMetadata` is evidence, not execution.
- Spine records; it does not execute.
- Critical actions do not auto-approve.
- Unknown actions remain denied/escalated.
- No raw prompts, transcripts, tool outputs, terminal output, secrets, or sensor data are stored.

## Future Path

Real pipeline work remains blocked until:

- Guardian enforcement design
- policy enforcement design
- approval enforcement design
- redaction/privacy implementation
- lineage emission design
- Sparkbot adapter review
- tool-pack runtime enforcement design
