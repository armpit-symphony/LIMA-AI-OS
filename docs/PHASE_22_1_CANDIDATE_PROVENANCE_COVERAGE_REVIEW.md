# Phase 22.1 Candidate Provenance Coverage Review

Phase 22.1 reviews the coverage added around the Phase 21 candidate provenance hardening slice.

This phase is docs/tests/fixtures only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Covered Areas

Phase 21 and earlier acceptance gates cover:

- exact approved runtime file scope
- valid provenance preservation
- malformed provenance rejection or invalidation
- suspicious authority wording blocked or invalid
- non-executing candidate invariants
- stale and replayed candidates blocked or invalid
- no Sparkbot wiring
- no HumanInput runtime bridge
- no live adapter
- no approval enforcement, execution, dispatch, or audit persistence

## Coverage Limits

The current coverage is strong for the existing candidate APIs, but additional test-only hardening could still add:

- broader nested provenance fixture cases
- regression cases for authority wording inside lists and nested mappings
- matrix coverage for candidate construction, status normalization, and validation side by side
- static guardrails for accidental future runtime expansion

## Gate

Phase 22.1 does not recommend runtime expansion. Coverage findings feed the Phase 22.2 safety gap review.
