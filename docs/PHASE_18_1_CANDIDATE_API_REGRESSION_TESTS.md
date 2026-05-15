# Phase 18.1 Candidate API Regression Tests

Phase 18.1 adds test-only regression coverage for existing non-executing candidate APIs.

This phase adds tests, docs, and synthetic fixture metadata only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Regression Coverage

The Phase 18.1 tests protect existing APIs:

- `lima.kernel.build_intake_candidate`
- `lima.kernel.normalize_candidate_status`
- `lima.kernel.validate_candidate`

The tests assert that candidates remain non-executable after construction, status normalization, and validation; authority-bearing fields fail closed; stale and replayed candidates stay blocked or invalid; provenance is preserved; and dangerous operator wording cannot bypass safety.

## Boundary

These tests exercise existing runtime APIs but do not modify runtime code. Phase 5 HumanInput runtime bridge behavior remains gated.
