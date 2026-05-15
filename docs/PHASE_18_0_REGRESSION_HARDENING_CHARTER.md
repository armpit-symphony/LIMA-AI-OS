# Phase 18.0 Regression Hardening Charter

Phase 18.0 opens Phase 18 as a test-only regression hardening lane for existing non-executing candidate APIs and acceptance-gate boundaries.

This phase is limited to docs, tests, and synthetic fixtures. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Regression Hardening Scope

Phase 18 may add regression tests and synthetic fixtures under `tests/` and `tests/fixtures/runtime_extraction/` only.

The lane protects:

- existing non-executing candidate APIs
- acceptance-gate boundaries from Phase 16
- Phase 5 HumanInput runtime bridge gating
- absence of Sparkbot wiring and live adapters
- absence of approval enforcement, execution, dispatch, audit persistence, and physical-world behavior

## Planned Phase 18 Work

- Phase 18.1: candidate API regression tests
- Phase 18.2: acceptance boundary regression fixtures
- Phase 18.3: forbidden integration regression tests
- Phase 18.4: regression hardening readiness review
- Phase 18.5: Phase 18 archive / closeout

## Gate

Phase 18.0 does not approve runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot integration, HumanInput runtime bridge behavior, live adapters, execution, approval enforcement, dispatch, audit persistence, or physical-world behavior.
