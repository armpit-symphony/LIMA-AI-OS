# Phase 23.3 Bypass-Wording Provenance Tests

Phase 23.3 adds deterministic test-only coverage for dangerous bypass wording in provenance and request metadata.

This phase is test-only hardening. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Coverage

The Phase 23.3 tests cover bypass wording for:

- Phil
- operator
- admin
- trusted
- urgent
- override
- approve
- emergency

The tests verify that bypass wording does not turn a candidate into an approved, executable, side-effect-capable, dispatchable, or persisted action. Authority claims embedded in provenance fail closed. Emergency wording attached to risky requests remains non-executing and requires review.

## Gate

Phase 23.4 may review Phase 23.0 through Phase 23.3 readiness only. Runtime expansion remains blocked.
