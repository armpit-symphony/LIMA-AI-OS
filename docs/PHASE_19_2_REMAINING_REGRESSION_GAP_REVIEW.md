# Phase 19.2 Remaining Regression Gap Review

Phase 19.2 identifies remaining gaps after the Phase 18 test-only regression hardening package and Phase 19.1 coverage review.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `candidate_status.py` or `intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not approve execution, does not enforce approval, does not dispatch, does not persist audit, and does not add shell, browser, network, file mutation, robotics, or physical-world behavior.

## Remaining Gaps

- The regression package proves current non-executing candidate invariants, but it does not define a new runtime slice.
- Static forbidden-pattern tests are useful tripwires, but they are not runtime monitors or Guardian enforcement.
- Synthetic fixtures cover risky examples, but they do not exercise live adapters, external services, Sparkbot integration, HumanInput runtime input, or physical-world drivers.
- Candidate APIs remain intentionally non-executing and cannot validate future integration behavior until a separately approved design lane defines it.
- Phase 5 HumanInput runtime bridge behavior remains gated and should not be folded into candidate regression work.
- Sparkbot and Robo-OS integration boundaries remain planning topics, not implementation topics.

## Gap Treatment

- Runtime expansion should not proceed directly from Phase 19.
- A future no-code design lane may define the next narrow runtime slice if Phil approves it.
- Additional test-only hardening remains a safe option if the project wants more regression depth before design.
- Sparkbot and Robo-OS planning remain separate boundary lanes and should not be mixed into runtime candidate API work.

## Gate

Phase 19.2 does not approve Phase 20 and does not approve runtime expansion. Phase 19.3 should compare the Phase 20 options and recommend the safest next lane.
