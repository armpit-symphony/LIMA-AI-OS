# Phase 37.3 Next-Lane Decision Matrix

Phase 37.3 evaluates the safest next lane after the Phase 36 candidate preview runtime slice and Phase 37 audit evidence.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, `tests/support/`, or stale prior-phase tests.

## Decision Matrix

| Option | Candidate next lane | Result |
| --- | --- | --- |
| A | Additional docs/tests/fixtures-only audit/archive of Phase 37 | Not needed beyond Phase 37.4 closeout. |
| B | Additional test-only hardening around `candidate_preview` | Not recommended now because Phase 37.2 found no concrete gap. |
| C | No-code design review for a third narrow runtime slice | Deferred. A third runtime slice is not justified immediately after Phase 36 without a concrete need. |
| D | HumanInput bridge boundary planning only | Deferred. The Phase 5 runtime bridge remains gated, and no bridge planning is needed to close this lane. |
| E | Sparkbot integration boundary planning only | Deferred. Sparkbot wiring remains forbidden, and no integration planning is needed to close this lane. |
| F | Pause and preserve current state | Recommended after Phase 37.4. |
| G | Request Phil approval for future runtime implementation | Not recommended. No evidence supports immediate runtime implementation. |

## Recommendation

After Phase 37.4, pause and preserve the current runtime/test state.

Reason:

- Phase 36 implemented the approved candidate preview helper cleanly.
- Phase 37 found no regression.
- Phase 37 found no blocking gap.
- Phase 37 found no immediate test-only hardening need.
- No new runtime implementation is justified.
- No `lima/`, `tests/support/`, stale prior-phase test, bridge, adapter, Sparkbot, execution, dispatch, persistence, external-call, robotics, or physical-world scope is needed.

## Operator Implication

Because the recommended next direction is pause/preserve rather than another phase, no Phil approval question is required at Phase 37.4 unless a future task asks to restart work.

## Continue

Continue only to Phase 37.4 candidate preview audit archive and closeout.
