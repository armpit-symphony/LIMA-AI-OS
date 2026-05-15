# Phase 17.3 Next-Lane Decision Matrix

Phase 17.3 compares the safe Phase 18 options after the Phase 16 acceptance implementation and Phase 17 audit work.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Options

| Option | Lane | Risk | Recommendation |
| --- | --- | --- | --- |
| A | No-code design lane for the next narrow runtime slice | Medium | Viable after regression hardening or if Phil wants runtime-design planning next |
| B | Test-only regression hardening lane | Lowest | Recommended next because it improves confidence without runtime expansion |
| C | Sparkbot integration boundary planning | Medium-high | Defer until runtime slice boundaries and regression tests are stronger |
| D | Robo-OS / physical-world boundary planning | High | Defer; physical-world boundaries require separate safety doctrine |
| E | Pause and preserve current runtime/test state | Lowest operational risk | Acceptable if no new lane is desired |

## Recommended Phase 18 Direction

Option B is the safest active next lane: a docs/tests/fixtures-only and tests-only regression hardening lane for existing non-executing candidate APIs and acceptance-gate boundaries.

This recommendation does not approve runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, or physical-world behavior.

## Phase 18 Gate

Phase 18 requires explicit Phil approval. If approved, the recommended scope is test-only regression hardening before any runtime expansion.
