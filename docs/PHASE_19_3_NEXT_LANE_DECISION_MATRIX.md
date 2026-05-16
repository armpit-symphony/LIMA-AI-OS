# Phase 19.3 Next-Lane Decision Matrix

Phase 19.3 compares the approved Phase 20 options after the Phase 18 regression hardening audit and remaining-gap review.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `candidate_status.py` or `intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not approve execution, does not enforce approval, does not dispatch, does not persist audit, and does not add shell, browser, network, file mutation, robotics, or physical-world behavior.

## Decision Matrix

| Option | Direction | Fit After Phase 18 | Boundary Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A | no-code design lane for next narrow runtime slice | Strong: Phase 18 hardened existing candidate boundaries and Phase 19 captured remaining gaps | Low if docs/tests/fixtures-only | Recommended |
| B | additional test-only regression hardening | Safe, but likely incremental after Phase 18 unless a specific gap is prioritized | Low | Keep available |
| C | Sparkbot integration boundary planning | Useful, but it opens a separate integration surface | Medium planning risk | Defer until runtime candidate lane decision is settled |
| D | Robo-OS / physical-world boundary planning | Important, but physical-world planning deserves a separate Guardian-gated lane | Medium-to-high planning risk | Defer |
| E | pause and preserve current runtime/test state | Safest preservation option | Lowest | Acceptable if Phil wants no additional lane now |

## Recommended Phase 20 Direction

Recommend Phase 20 as a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice.

That recommendation does not approve runtime implementation. Phase 20 would only define a possible future runtime slice, exact future file-touch scope, acceptance gates, rollback proof, and explicit stop conditions.

## Phase 20 Approval Boundary

Phase 20 must still require explicit Phil approval and must forbid runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior changes, GuardianDecision runtime behavior changes, approval enforcement, execution, dispatch, audit persistence, shell, browser, network, file mutation, robotics, and physical-world action.
