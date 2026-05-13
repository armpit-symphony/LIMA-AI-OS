# Phase 6.0 Post-Phase-5 Roadmap Reorientation

Phase 6.0 starts broader LIMA OS roadmap planning after the Phase 5 HumanInput bridge design lane archive. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, and does not persist audit.

## Reorientation

Phase 5 closed the HumanInput to IntentEnvelope design lane as planning/specification work. The safest next architectural lane is not runtime bridge implementation. The safest next lane is broader LIMA kernel lifecycle planning so later runtime work has a clearer operating model.

## Future Lanes To Separate

- kernel lifecycle planning
- IntentEnvelope lifecycle
- GuardianDecision lifecycle
- approval boundary model
- audit, spine, and memory relationship
- Sparkbot integration boundary
- Robo-OS and physical-world boundary
- runtime bridge prerequisites

## Runtime Bridge Prerequisites

Before any runtime bridge can be approved, the repo needs clear lifecycle boundaries for the kernel, IntentEnvelope, GuardianDecision, approval states, audit/spine/memory relationships, Sparkbot integration, and physical-world consumers.

## Next Gate

Phase 6.1 may continue as docs/tests/fixtures-only LIMA Kernel Lifecycle Planning. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
