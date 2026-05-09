# Phase 1.9 Fake Pipeline Readiness Review

## Purpose

Review the fake Guardian pipeline and determine whether LIMA is ready to begin adapter-design work.

This review does not authorize production integration.
This review does not authorize real enforcement.
This review does not authorize Sparkbot runtime migration.

## Current Fake Pipeline

```text
ConsequentialActionRequest
  -> FakePolicyRiskEvaluator
  -> FakeGuardianDecisionEvaluator
  -> FakeApprovalRecorder when needed
  -> FakeSpineAuditRecorder
  -> FakeGuardianPipelineResult
```

The current fake pipeline is in-memory and test-only. It records contract-shaped decisions, approvals, and lineage evidence without executing or persisting anything.

The fake pipeline proves contract composition only. It is not production runtime.

Safety invariants:

- Fake decisions are not production authorization.
- `PolicyDecision` does not replace `GuardianDecision`.
- `ApprovalMetadata` is evidence, not execution.
- Spine records; it does not execute.

## What Is Proven

- Contracts can compose across policy, Guardian decision, approval, and Spine/Audit lineage boundaries.
- `PolicyDecision` can be produced from a request-derived `PolicyEvaluationContext`.
- `GuardianDecision` can be produced from `ConsequentialActionRequest`.
- `ApprovalMetadata` can be recorded when a fake Guardian decision requires confirmation, operator PIN, breakglass, or review.
- Spine/Audit lineage can be recorded in memory.
- Critical actions avoid auto-approval.
- Unknown actions are denied/escalated and auditable.
- Boundary tests block Sparkbot imports and unsafe provider methods.

## What Is Not Proven

- real Guardian enforcement
- real policy enforcement
- real approval enforcement
- real PIN verification
- real breakglass enforcement
- real audit persistence
- real redaction runtime
- real Sparkbot adapter behavior
- real model/tool/driver execution safety
- real terminal/PTY safety
- real Robo-OS physical action safety

## Readiness Decision

GO for first adapter-design branch only.

NO-GO for production adapter, real enforcement, real tool execution, real audit persistence, terminal/PTY, or Robo-OS physical action integration.

## Recommended Next Branch

Recommended next branch:

```text
phase-1-10-sparkbot-humaninput-adapter-design
```

Purpose:
Design, but do not implement production integration, how Sparkbot chat/voice/meeting entrypoints will become `HumanInput` records.

Phase 1.10 should be adapter-design/docs/tests only, not live Sparkbot wiring.

## Why HumanInput Adapter Design Comes Next

Before moving Guardian, Harness, or tool behavior, LIMA needs to define how Sparkbot entrypoints become `HumanInput` without preserving raw chat-to-tool shortcuts.

This aligns with:

- Intent Compiler Boundary
- GuardianDecision Contract
- Tool-Pack Scoping
- Runtime Boundary Map
- Sparkbot Entrypoint Inventory

## Adapter-Design Acceptance Criteria

For Phase 1.10, acceptance criteria should include:

- no Sparkbot code migration
- no production Sparkbot changes
- no tool execution
- no model execution
- no terminal/PTY
- no Robo-OS physical action
- no audit persistence
- design maps Sparkbot chat, voice, meeting, and operator inputs to `HumanInput`
- design preserves behavior without preserving raw chat-to-tool shortcuts
- privacy classes for text, voice, and future BCI are identified
- lineage IDs are planned but not persisted
- tests remain contract-shape only

## Still Blocked

- `stream_chat_with_tools` extraction
- Harness/tool execution extraction
- full-catalogue tool exposure
- terminal/PTY execution
- raw natural language to robot MCP commands
- live Sparkbot adapter
- real Guardian enforcement
- real policy enforcement
- real approval enforcement
- real audit persistence
- real redaction runtime
- vault/auth live adapters
- Robo-OS physical action integration

## Risk Register

| Risk | Severity | Current mitigation | Next action | Phase target |
| --- | --- | --- | --- | --- |
| Fake pipeline mistaken for production runtime | high | Phase 1.8 and this review state fake/test-only behavior | Keep production integration blocked in Phase 1.10 | Phase 1.9 |
| Adapter accidentally preserving raw chat-to-tool shortcut | critical | Intent Compiler Boundary and Runtime Boundary Map mark shortcut as unsafe | Design `HumanInput` adapter before Harness/tool work | Phase 1.10 |
| Sparkbot changes before adapter design | medium | Sparkbot remains parity source and prior inventories record commit context | Recheck Sparkbot before adapter-design PR | Phase 1.10 |
| Privacy/redaction not enforced yet | high | Redaction/privacy contracts block raw sensitive persistence | Keep Phase 1.10 design-only with privacy classification | Phase 1.10 |
| Lineage not persisted yet | high | Fake Spine/Audit recorder records lineage in memory only | Plan lineage IDs without storage implementation | Phase 1.10 |
| Critical action handling still fake | critical | Fake evaluators deny/require approval for critical-like actions | Do not begin execution or enforcement branches | Deferred |
| Guardian enforcement still fake | critical | Fake Guardian decision evaluator is test-only | Keep real enforcement blocked pending design | Deferred |
| Policy/approval enforcement still fake | critical | Fake policy and approval components record metadata only | Keep real enforcement blocked pending design | Deferred |

## Final Recommendation

Phase 1.9 recommends moving to Phase 1.10 Sparkbot HumanInput Adapter Design only.

No real runtime integration is approved.
