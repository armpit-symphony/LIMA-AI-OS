# Phase 21.3 Candidate Provenance Regression Review

Phase 21.3 reviews the Phase 21.2 candidate provenance hardening runtime slice and adds regression-only documentation, fixtures, and tests.

This phase does not modify runtime files. It does not modify `lima/`, does not modify `tests/support/`, does not expand candidate provenance behavior, does not modify `lima/kernel/__init__.py`, does not add runtime modules, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not approve execution, does not enforce approval, does not dispatch, does not persist audit, and does not add shell, browser, network, file mutation, robotics, external-service, or physical-world behavior.

## Regression Findings

The Phase 21.2 runtime slice remains narrow:

- candidate construction rejects malformed provenance keys and missing provenance values
- candidate validation marks malformed or suspicious provenance invalid
- candidate status normalization blocks suspicious provenance authority claims
- valid provenance remains preserved
- non-executing invariants remain forced
- stale and replayed candidates remain blocked or invalid
- Phase 5 HumanInput runtime bridge remains gated

## Remaining Limits

The slice still does not create a live HumanInput bridge, approval enforcement, execution path, dispatch path, audit persistence layer, Sparkbot wiring, live adapter, IntentCompiler behavior, or GuardianDecision behavior.

## Gate

Phase 21.4 may proceed as a readiness review only. No runtime scope expansion is approved.
