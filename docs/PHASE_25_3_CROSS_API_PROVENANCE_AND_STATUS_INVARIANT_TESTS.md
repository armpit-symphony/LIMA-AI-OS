# Phase 25.3 Cross-API Provenance and Status Invariant Tests

Phase 25.3 adds deterministic offline tests for provenance and status invariants across existing candidate-facing APIs.

This phase is test/docs/fixtures-only hardening. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Assertions

The tests assert:

- valid provenance is preserved
- suspicious provenance is blocked or invalid
- unknown status is blocked
- stale and replayed candidates are invalid or blocked
- bypass wording does not make risky requests approved
- malformed HumanInput-like intake remains rejected
- status normalization and validation never approve, execute, dispatch, persist, or create bridge records

## Gate

Phase 25.4 may perform a cross-API boundary readiness review only. Runtime expansion remains blocked.
