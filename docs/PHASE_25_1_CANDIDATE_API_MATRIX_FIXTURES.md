# Phase 25.1 Candidate API Matrix Fixtures

Phase 25.1 adds synthetic fixtures for the cross-API candidate invariant matrix.

This phase is test/docs/fixtures-only fixture work. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Fixture Coverage

The matrix fixture covers:

- valid low-risk intake
- unknown candidate status
- suspicious provenance
- bypass wording with risky action metadata
- stale candidate
- replayed candidate
- malformed HumanInput-like intake rejection
- shell/browser/network/file/robotics/physical-world attempt categories

## Gate

Phase 25.2 may add cross-API non-execution invariant tests using these fixtures. Runtime expansion remains blocked.
