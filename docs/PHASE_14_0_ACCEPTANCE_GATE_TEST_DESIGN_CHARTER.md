# Phase 14.0 Acceptance-Gate Test Design Charter

Phase 14.0 opens Phase 14 as a docs/tests/fixtures-only acceptance-gate test design lane.

This phase is design only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add executable test helpers, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Source Requirements

Phase 14 converts Phase 13 requirements into concrete future test names and expected assertions:

- Phase 13.1 static forbidden-pattern requirements
- Phase 13.2 runtime contract requirements
- Phase 13.3 threat fixture matrix
- Phase 13.4 future acceptance gate requirements

## Design Outputs

Phase 14 should produce:

- static forbidden-pattern test design
- runtime contract test design
- threat fixture acceptance test design
- future runtime acceptance gate / closeout

## Standing Boundary

Phase 5 HumanInput runtime bridge remains gated. Runtime implementation and integration work remain unapproved.

## Next Step

Phase 14.1 should design concrete static forbidden-pattern test names and expected assertions.
