# Phase 25.0 Cross-API Candidate Invariant Matrix Charter

Phase 25.0 opens a test-only hardening lane for a cross-API candidate invariant matrix.

This phase is test/docs/fixtures-only charter work. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Matrix Purpose

The Phase 25 matrix protects existing candidate-facing APIs from regression:

- intake candidate construction
- candidate status normalization
- candidate validation
- provenance hardening behavior

Every matrix case must preserve the same candidate invariants:

- `execution_allowed` remains false
- `side_effects_allowed` remains false
- `approval_state` never becomes approved
- provenance is preserved or safely rejected, blocked, invalid, or needs review
- malformed input remains safe
- unknown status remains safe
- suspicious provenance remains safe
- bypass wording does not change safety outcome

## Gate

Phase 25.1 may add synthetic matrix fixtures only. Runtime expansion remains blocked.
