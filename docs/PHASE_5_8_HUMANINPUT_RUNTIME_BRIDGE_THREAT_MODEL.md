# Phase 5.8 HumanInput Runtime Bridge Threat Model

Phase 5.8 threat-models a future HumanInput to IntentEnvelope runtime bridge. It is docs/tests/fixtures only.

This phase does not implement a runtime bridge, does not add live adapter code, does not modify `lima/`, does not modify `tests/support/`, does not change the Phase 5.4 helper, does not wire Sparkbot, does not implement real IntentCompiler behavior, does not implement real GuardianDecision behavior, does not enforce approval, does not execute, and does not persist audit.

## Threats

- Prompt injection: HumanInput text attempts to override system policy or Guardian review.
- Operator impersonation: input claims to be Phil, admin, trusted, or an operator to bypass review.
- Trust bypass: passive trust/autonomy references are treated as permission.
- Accidental execution: candidate metadata is treated as executable command state.
- Side-effect escalation: shell, browser, network, file mutation, robotics, or physical-world requests are normalized without approval-required status.
- Audit gaps: candidate lineage lacks source, actor, session, timestamp, redaction, or retention context.
- Approval confusion: proposed, denied, approval-required, and ready-for-review states are collapsed into approval.
- Helper classifier misuse: Phase 5.4 test-only keyword classifier is reused as runtime logic.
- Unsafe test-code reuse: `tests/support/` helpers are imported from production runtime paths.
- Malformed input: missing, empty, partial, or invalid records produce candidates.
- Replayed input: stale or duplicate HumanInput is accepted without lineage review.
- Ambiguous commands: unclear requests are treated as low-risk or executable.

## Mitigations

- Treat every HumanInput record as intent context only.
- Require provenance before candidate creation.
- Default all candidates to non-executable and side-effect denied.
- Require approval-required or blocked status for side-effect-bearing categories.
- Keep risk tier and approval state as metadata until GuardianDecision enforcement is explicitly approved.
- Reject operator/admin/Phil/trusted wording as approval bypass.
- Keep Phase 5.4 helper and classifier test-only.
- Block production imports from `tests/support/`.
- Require future runtime design and threat-model review before implementation.
- Require future runtime tests to cover malformed, replayed, stale, ambiguous, and side-effect-bearing requests.

## Residual Risk

The threat model is static and cannot prove runtime safety. Any future implementation must include runtime design review, semantic tests, Guardian gate integration review, audit design, and explicit operator approval before live behavior.

## Next Gate

Phase 5.9 may continue with a docs/tests/fixtures-only boundary validation matrix. Runtime implementation remains blocked.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
