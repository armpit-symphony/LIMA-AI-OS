# Phase 6.1 LIMA Kernel Lifecycle Planning

Phase 6.1 defines a planning-only lifecycle map for the LIMA Kernel. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, and does not persist audit.

## Kernel Lifecycle Stages

1. Shell intake receives operator-originated context.
2. Boundary normalization produces typed non-executable boundary records.
3. Intent candidate formation prepares non-executable IntentEnvelope candidate metadata.
4. Guardian review classifies risk, required approval, and allowed handoff.
5. GuardianDecision records approve, deny, block, or request more review.
6. Spine/audit/memory handoff records lineage and retention intent after a valid decision.
7. Driver/tool handoff remains blocked until Guardian has approved a later executable path.

## Lifecycle Rules

- HumanInput is intent context, not execution permission.
- IntentEnvelope candidates are non-executable until a future approved runtime phase.
- GuardianDecision is the only future authority boundary for approval semantics.
- Audit/spine/memory relationships must be designed before persistence is implemented.
- Sparkbot remains a reference shell, not the kernel.
- Robo-OS and physical-world consumers remain gated driver-plane surfaces.

## Next Gate

Phase 6.2 may map IntentEnvelope and GuardianDecision lifecycle boundaries as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
