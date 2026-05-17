# Phase 41.3 Arc Bot Hardening Gap And Next-Lane Review

Phase 41.3 reviews the Phase 41 Arc Bot-shaped `candidate_preview` hardening results.

This phase does not modify `candidate_preview.py`, `lima/`, `tests/support/`, Sparkbot, Arc Bot implementation, HumanInput bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, mutation, external calls, background work, robotics, or physical-world behavior.

## Evidence Reviewed

- Phase 41.0 opened the test-only hardening charter.
- Phase 41.1 added synthetic Arc Bot / LIMA Office fixture data.
- Phase 41.2 exercised the existing `candidate_preview` helper against those fixtures.

## Findings

- Benign draft-only email preview remains proposed, non-authoritative, non-executing, and inert.
- Risky external write, calendar write, file mutation, memory persistence, scheduled work, admin, Sparkbot-only, robotics, physical-world, and explain-plan cases remain blocked.
- Connector missing secret/setup remains blocked.
- Strict-security posture is conservatively blocked because caller-provided planning keys containing `operator` are treated as suspicious claim evidence.
- This conservative blocking is acceptable and safer than review-only output.

## Gaps

No concrete runtime gap was found.

No runtime change, `lima/` change, `tests/support/` change, Sparkbot wiring, HumanInput bridge behavior, live adapter behavior, approval enforcement, execution, dispatch, persistence, mutation, external call, background work, robotics, or physical-world behavior is needed.

## Recommended Next Lane

Phase 41.4 should archive the completed test-only hardening lane.

After Phase 41.4, the safest next direction is a docs/tests/fixtures-only audit/archive or no-code design-review lane, not runtime implementation.
