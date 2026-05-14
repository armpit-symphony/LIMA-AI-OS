# Phase 8.0 Implementation Design Review Charter

Phase 8.0 opens Phase 8 as a no-code implementation design review lane. It converts the Phase 7 no-code kernel runtime charter into a precise future implementation design package without modifying runtime code.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Source Context

- Phase 7.0 defined the smallest possible future runtime slice as a non-executing kernel intake-to-candidate coordinator.
- Phase 7.1 mapped future eligible and forbidden file surfaces.
- Phase 7.2 defined safety preconditions before runtime code.
- Phase 7.3 defined runtime implementation test-plan obligations.
- Phase 7.4 closed Phase 7 at an implementation decision gate.
- Phase 7.5 archived Phase 7 as no-code charter/planning only.

## Design Review Mission

Phase 8 must produce a future implementation design package that is exact enough for Phil to make a later runtime implementation approval decision. The design package must include:

- narrowest future runtime slice definition
- exact future file-touch map
- future runtime acceptance tests
- rollback expectations
- audit proof requirements
- implementation success and failure criteria
- explicit out-of-scope list
- final approval question

## Narrowest Future Runtime Slice

The only future runtime slice that Phase 8 may design is a non-executing kernel intake-to-candidate coordinator.

That future slice may be designed to accept already-typed, explicit input metadata and produce non-executable candidate metadata for later Guardian review. It must not parse natural language, call a model, call tools, execute commands, mutate files, access the network, open a browser, control robots, persist audit, enforce approvals, wire Sparkbot, create a real IntentEnvelope, or create a real GuardianDecision.

## Lane Boundaries

- Phase 5 HumanInput runtime bridge remains gated.
- Runtime implementation remains blocked.
- `lima/` changes remain blocked.
- `tests/support/` changes remain blocked.
- Sparkbot imports and wiring remain blocked.
- Live adapters remain blocked.
- IntentCompiler and GuardianDecision runtime behavior remain blocked.
- Approval enforcement, execution, audit persistence, shell/browser/network/file mutation/robotics/physical-world side effects remain blocked.

## Next Step

Phase 8.1 may map exact future runtime file touches as docs/tests/fixtures only. It must not modify those future runtime files.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
