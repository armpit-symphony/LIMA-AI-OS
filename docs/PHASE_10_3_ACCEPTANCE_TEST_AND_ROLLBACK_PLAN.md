# Phase 10.3 Acceptance Test and Rollback Plan

Phase 10.3 defines acceptance-test and rollback/audit-proof requirements for a possible Phase 11 candidate validation and status normalization runtime slice. It does not implement that slice.

This phase does not modify `lima/`, does not modify `tests/support/`, does not change helper behavior, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add live adapters, does not implement HumanInput runtime bridge behavior, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Required Future Acceptance Tests

A future Phase 11 implementation may proceed only if its tests prove:

- valid Phase 9-style candidates validate without gaining authority
- candidates missing `execution_allowed` are rejected or marked blocked
- candidates missing `side_effects_allowed` are rejected or marked blocked
- candidates with `execution_allowed: true` are rejected or marked blocked
- candidates with `side_effects_allowed: true` are rejected or marked blocked
- candidates with `approval_state: approved` are rejected or marked blocked
- candidate status normalization only emits `proposed`, `needs_review`, or `blocked`
- unknown, malformed, stale, replayed, or incomplete candidates are blocked or not ready
- provenance is preserved
- blocked/not-ready candidates carry an explicit reason
- operator/admin/Phil/trusted wording does not bypass safety
- no HumanInput runtime bridge behavior exists
- no Sparkbot import or wiring exists
- no live adapter exists
- no IntentCompiler or GuardianDecision runtime behavior changes
- no approval enforcement, execution, dispatch, audit persistence, shell, browser, network, file mutation, robotics, or physical-world side effects are reachable

## Rollback Plan

If a future Phase 11 implementation fails validation or touches forbidden scope, rollback must:

1. Revert the Phase 11 merge commit.
2. Confirm only the Phase 10.2 eligible runtime files were affected.
3. Confirm `lima/kernel/intake_candidate.py` still produces non-executing candidates.
4. Confirm imports remain side-effect-free.
5. Re-run targeted Phase 9, Phase 10, and Phase 11 tests.
6. Re-run the full suite.
7. Re-run `python -m compileall lima`.
8. Re-run `git diff --check`.
9. Document the failure mode and rollback evidence before retrying.

No database migrations, background workers, queues, daemons, external services, or filesystem side effects are expected or allowed, so rollback must remain a source-only Git revert.

## Audit Proof Requirements

Phase 11 audit proof must include:

- exact runtime files changed
- proof that no files outside the Phase 10.2 map changed
- validation output
- full-suite output
- compileall output
- diff-check output
- side-effect review
- import review
- confirmation that Phase 5 HumanInput runtime bridge remains gated
- confirmation that approval, execution, dispatch, audit persistence, and physical-world behavior remain absent

## Next Step

Phase 10.4 should close the Phase 10 design lane and preserve the exact Phase 11 approval question for Phil.
