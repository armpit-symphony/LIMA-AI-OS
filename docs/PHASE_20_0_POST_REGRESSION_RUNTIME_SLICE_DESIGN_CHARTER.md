# Phase 20.0 Post-Regression Runtime Slice Design Charter

Phase 20.0 opens Phase 20 as a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice.

This phase uses Phase 18 regression coverage and Phase 19 audit findings as inputs. It does not implement runtime code, does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `candidate_status.py` or `intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not approve execution, does not enforce approval, does not dispatch, does not persist audit, and does not add shell, browser, network, file mutation, robotics, or physical-world behavior.

## Design Inputs

- Phase 18 candidate API regression tests.
- Phase 18 acceptance-boundary fixtures.
- Phase 18 forbidden integration regression tests.
- Phase 19 regression coverage review.
- Phase 19 remaining regression gap review.
- Phase 19 next-lane decision matrix.
- Phase 19 archive closeout.

## Candidate Slice Options

- Option A: candidate provenance hardening.
- Option B: candidate lifecycle metadata.
- Option C: replay/staleness marker normalization.
- Option D: candidate error taxonomy.
- Option E: no runtime work; pause and preserve.
- Option F: Sparkbot integration boundary planning instead of runtime work.

## Phase 20 Design Outputs

Phase 20 may recommend one next runtime slice or recommend no runtime work. It must produce:

- exact future file-touch map
- future acceptance-test requirements
- rollback and audit proof requirements
- Phase 21 decision gate

## Gate

Phase 20.0 does not approve Phase 21 and does not approve runtime implementation. The Phase 5 HumanInput runtime bridge remains gated.
