# Phase 26.2 Remaining Cross-API Gap Review

Phase 26.2 records remaining cross-API candidate invariant gaps after the Phase 25 test-only hardening package.

This phase is gap review only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Remaining Gaps

Phase 25 provides strong deterministic offline regression coverage, but several gaps remain as future planning inputs only.

- A broader property-style or matrix-generated fixture sweep could reduce duplication and expose edge combinations without changing runtime behavior.
- Static forbidden-pattern scans could be consolidated around a shared checklist in a future test-only lane, without modifying `tests/support/`.
- Import-boundary regression checks could be widened for Sparkbot, HumanInput bridge, live adapter, IntentCompiler, and GuardianDecision boundaries.
- Provenance traceability could receive a fixture index that maps risky examples back to their threat category.
- The project still needs a conservative decision on whether to pause, add more test-only hardening, or design a future narrow runtime slice.

## Not Approved

The gap list does not approve runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, or physical-world behavior.

Phase 5 HumanInput runtime bridge remains gated.

## Continue

Continue only to Phase 26.3 next-lane decision matrix.
