# Phase 7.2 Kernel Runtime Safety Preconditions

Phase 7.2 defines the safety preconditions that must be satisfied before any future kernel runtime implementation can be approved. It is docs/tests/fixtures only.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Required Test Preconditions

- Targeted tests for every future modified or created runtime file.
- Negative tests for missing typed input.
- Negative tests for raw natural-language parsing attempts.
- Negative tests for execution, approval enforcement, audit persistence, and side effects.
- Import-boundary tests proving no Sparkbot coupling.
- Full suite passing before merge.

## Rollback Preconditions

- The future runtime slice must be independently revertible.
- No irreversible migration is allowed.
- No persistent schema change is allowed.
- No external side effect is allowed.
- The old docs/tests/fixtures-only state must remain recoverable.

## Audit Proof Preconditions

- Future runtime candidate output must carry provenance metadata.
- Future runtime candidate output must carry explicit non-executable markers.
- Future runtime candidate output must identify which Guardian review boundary would be required later.
- Audit proof remains test evidence only until audit persistence is separately approved.

## Input / Output Shape Preconditions

- Input must be typed, explicit, synthetic or test-vetted metadata.
- Input must fail closed if required fields are missing.
- Output must be non-executable candidate metadata.
- Output must not include approval, execution permission, driver handoff, or persistence authority.

## Safety Gate Preconditions

- Phase 5 runtime bridge gate remains active.
- Phase 7.1 eligible/forbidden file map must be honored.
- GuardianDecision remains future authority.
- Approval enforcement remains blocked.
- Execution remains blocked.
- Sparkbot wiring remains blocked.
- Physical-world behavior remains blocked.

## Next Gate

Phase 7.3 may define a runtime implementation test plan as docs/tests/fixtures only. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
