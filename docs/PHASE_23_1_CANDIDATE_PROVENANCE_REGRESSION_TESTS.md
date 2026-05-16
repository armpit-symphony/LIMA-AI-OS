# Phase 23.1 Candidate Provenance Regression Tests

Phase 23.1 adds deterministic offline regression tests for existing candidate provenance behavior.

This phase is test-only hardening. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Regression Coverage

The tests assert:

- valid provenance is preserved through candidate construction, status normalization, and validation
- missing provenance is rejected or invalid
- malformed provenance is rejected or invalid
- stale and replayed candidates remain blocked or invalid
- non-executing invariants remain preserved
- Phase 5 HumanInput runtime bridge remains gated

## Gate

Phase 23.2 may add broader synthetic suspicious provenance fixtures only. Runtime expansion remains blocked.
