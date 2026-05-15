# Phase 13.0 Threat-Derived Test Planning Charter

Phase 13.0 opens Phase 13 as a docs/tests/fixtures-only threat-model-derived test planning lane.

This phase is planning only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Source Threats

Phase 13 converts the Phase 12.2 threats into future test requirements:

- candidate status mistaken for approval
- candidate validation mistaken for GuardianDecision behavior
- HumanInput runtime bridge pressure
- Sparkbot boundary planning drifting into wiring
- Robo-OS planning drifting into driver behavior
- operator, admin, Phil, or trusted wording bypass attempts
- shell, browser, network, file, robotics, or physical-world escalation
- audit persistence implied before approval
- static tests mistaken for complete runtime proof

## Planning Outputs

Phase 13 should produce:

- static forbidden-pattern test requirements
- runtime contract test requirements
- threat fixture matrix
- future acceptance gate / closeout

## Standing Boundary

Phase 5 HumanInput runtime bridge remains gated. Phase 13 does not approve runtime implementation or integration work.

## Next Step

Phase 13.1 should define static forbidden-pattern test requirements.
