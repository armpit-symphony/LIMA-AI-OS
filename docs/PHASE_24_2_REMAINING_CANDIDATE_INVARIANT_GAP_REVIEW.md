# Phase 24.2 Remaining Candidate Invariant Gap Review

Phase 24.2 identifies remaining provenance and candidate-invariant gaps after the Phase 23 test-only hardening package.

This phase is docs/tests/fixtures-only gap review. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Remaining Gaps

The following gaps remain planning inputs only:

- broader provenance fixture matrix for nested mixed safe/unsafe metadata
- cross-API regression matrix spanning candidate construction, status normalization, and validation
- explicit static import/call pattern review for future candidate-slice work
- future test-only replay/staleness matrix with more timestamp and lineage combinations
- future no-code design for whether another narrow runtime slice is warranted

## Non-Gaps

The following are not approved by this review:

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot integration
- HumanInput runtime bridge behavior
- live adapters
- approval enforcement
- execution, dispatch, audit persistence, or physical-world behavior

## Gate

Phase 24.3 may evaluate next-lane options only. Runtime expansion remains blocked.
