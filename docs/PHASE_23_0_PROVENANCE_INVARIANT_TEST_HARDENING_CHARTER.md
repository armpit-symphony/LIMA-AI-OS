# Phase 23.0 Provenance Invariant Test Hardening Charter

Phase 23.0 opens a test-only hardening lane for provenance and candidate invariants.

This phase does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, call shell, browser, network, file mutation, robotics, external services, or physical-world systems, and does not start background workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Approved Lane

Phase 23 may add deterministic offline tests and synthetic fixtures for existing non-executing candidate APIs.

Allowed:

- `tests/test_phase_23_*.py`
- `tests/fixtures/runtime_extraction/phase_23_*.json`
- `docs/PHASE_23_*.md`
- required roadmap/state documentation updates

## Hardening Goals

- valid provenance remains preserved
- missing provenance fails closed
- malformed provenance fails closed
- suspicious provenance fails closed
- stale or replayed candidates remain blocked or invalid
- approval-bypass wording cannot change safety outcomes
- `execution_allowed` remains false
- `side_effects_allowed` remains false
- `approval_state` never becomes approved
- Phase 5 HumanInput runtime bridge remains gated
- Sparkbot, HumanInput bridge, live adapter, execution, dispatch, approval enforcement, and audit persistence surfaces remain absent

## Gate

Phase 23.1 may add candidate provenance regression tests only. Runtime expansion remains blocked.
