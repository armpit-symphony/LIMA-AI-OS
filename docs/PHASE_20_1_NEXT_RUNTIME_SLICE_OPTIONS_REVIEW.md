# Phase 20.1 Next Runtime Slice Options Review

Phase 20.1 compares the candidate next-slice options and recommends exactly one future runtime slice without implementing it.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `candidate_status.py` or `intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not approve execution, does not enforce approval, does not dispatch, does not persist audit, and does not add shell, browser, network, file mutation, robotics, or physical-world behavior.

## Options Review

| Option | Candidate Slice | Safety Fit | Decision |
| --- | --- | --- | --- |
| A | candidate provenance hardening | Strong fit: provenance is already required, non-executing, and audit-relevant | Recommended |
| B | candidate lifecycle metadata | Useful, but could drift toward state-machine semantics | Defer |
| C | replay/staleness marker normalization | Useful, but already has basic handling and can be folded into provenance acceptance tests | Defer |
| D | candidate error taxonomy | Useful, but less urgent than provenance consistency | Defer |
| E | no runtime work; pause and preserve | Always acceptable if Phil prefers no runtime lane | Keep available |
| F | Sparkbot integration boundary planning instead of runtime work | Separate integration lane, not the next candidate runtime slice | Defer |

## Recommendation

Recommend a future Phase 21 runtime slice limited to candidate provenance hardening.

The future slice should only normalize and validate provenance metadata for existing non-executing candidates. It must not create a HumanInput runtime bridge, must not approve, execute, dispatch, persist, call external services, wire Sparkbot, or add live adapters.

## Gate

Phase 20.1 does not approve Phase 21. Phase 20.2 must map exact future files before any approval question can be preserved.
