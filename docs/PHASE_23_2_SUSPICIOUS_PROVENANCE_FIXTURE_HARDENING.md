# Phase 23.2 Suspicious Provenance Fixture Hardening

Phase 23.2 adds synthetic fixtures and deterministic tests for suspicious provenance authority claims.

This phase is test-only hardening. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Fixture Coverage

The fixtures cover suspicious authority claims in:

- provenance values
- provenance keys
- nested provenance mappings
- provenance lists
- risky shell/browser/network/file/robotics attempts represented as synthetic metadata

Every case must remain blocked or invalid and must preserve non-executing invariants.

## Gate

Phase 23.3 may add explicit bypass-wording provenance tests only. Runtime expansion remains blocked.
