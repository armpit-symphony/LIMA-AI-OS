# Phase 12.3 Next Lane Recommendation Matrix

Phase 12.3 records a machine-checkable recommendation matrix for the next safe lane after Phase 12.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Recommendation Matrix

| Option | Lane | Recommendation | Reason |
| --- | --- | --- | --- |
| A | Pause and preserve | Safe fallback | Lowest risk, but does not reduce known safety gaps |
| B | Future runtime slice design | Defer | Needs threat-model-derived tests first |
| C | Sparkbot boundary planning | Defer | Important, but boundary drift risk remains high |
| D | Robo-OS / physical-world planning | Defer | Highest physical-world risk; needs stronger safety test plan first |
| E | Threat-model-derived test planning | Recommended next | Reduces risk before runtime, Sparkbot, or Robo-OS lanes |

## Recommended Next Lane

The recommended next lane is a docs/tests/fixtures-only threat-model-derived test planning lane. It should convert Phase 12.2 threats into static, contract, fixture, and future acceptance-test requirements before any runtime expansion or integration planning.

## Explicit Non-Recommendations

Phase 12.3 does not recommend:

- runtime implementation
- Sparkbot wiring
- HumanInput runtime bridge behavior
- Robo-OS driver behavior
- live adapter integration
- approval enforcement
- execution
- dispatch
- audit persistence
- shell, browser, network, file mutation, robotics, or physical-world action

## Next Step

Phase 12.4 should close Phase 12 at a decision gate and preserve the exact next approval question for Phil.
