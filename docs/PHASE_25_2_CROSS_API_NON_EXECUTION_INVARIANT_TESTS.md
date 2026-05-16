# Phase 25.2 Cross-API Non-Execution Invariant Tests

Phase 25.2 adds deterministic offline tests proving existing candidate-facing APIs preserve non-execution invariants across the Phase 25 matrix fixtures.

This phase is test/docs/fixtures-only hardening. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Assertions

For every constructible matrix candidate:

- candidate construction remains non-executing
- candidate status normalization remains non-executing
- candidate validation remains non-executing
- `execution_allowed` remains false
- `side_effects_allowed` remains false
- `approval_state` never becomes approved
- Phase 5 HumanInput runtime bridge remains gated

Malformed HumanInput-like intake remains rejected before candidate construction.

## Gate

Phase 25.3 may add provenance and status invariant tests only. Runtime expansion remains blocked.
