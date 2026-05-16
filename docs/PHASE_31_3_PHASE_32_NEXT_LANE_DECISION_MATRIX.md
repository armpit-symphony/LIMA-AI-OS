# Phase 31.3 Phase 32 Next-Lane Decision Matrix

Phase 31.3 evaluates Phase 32 options after the completed Phase 30 read-only runtime state inspection slice.

This phase is next-lane decision metadata only. It does not implement new runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Options Evaluated

Option A: docs/tests/fixtures-only design review for the next narrow runtime slice.

Result: recommended. Phase 30 is stable and bounded, but another runtime implementation should not be automatic. A design review can evaluate the next smallest candidate and preserve explicit approval boundaries.

Option B: additional test-only hardening around runtime_state if a concrete gap exists.

Result: fallback only. Phase 31.2 found no blocking safety regression. Test-only hardening remains appropriate if Phase 32 identifies a concrete fixture or regression gap.

Option C: second narrow read-only runtime slice only if Phase 31 proves eligibility.

Result: not recommended as the immediate default. Phase 31 proves Phase 30 is bounded, but a new implementation still needs design review and explicit Phil approval.

Option D: HumanInput bridge boundary planning only, no implementation.

Result: valid but not recommended as the immediate default. The Phase 5 runtime bridge remains gated, and bridge planning should stay separate from runtime_state audit closeout.

Option E: Sparkbot integration boundary planning only, no implementation.

Result: valid but not recommended as the immediate default. Sparkbot remains unwired; integration boundary planning should be explicit and separate.

Option F: pause and preserve state if Phase 30 introduced unresolved risk.

Result: not required. Phase 30 introduced no unresolved risk requiring an automatic pause.

## Recommended Phase 32 Direction

Recommend Phase 32 as a docs/tests/fixtures-only design review for the next narrow runtime slice.

Phase 32 should not implement runtime code. It should evaluate whether any future slice is safe, define eligibility criteria, list exact allowed and forbidden file scope, define acceptance tests and rollback/audit proof, and end with an explicit Phase 33 approval question.

## Exact Phase 32 Approval Question

Do you approve Phase 32 as a docs/tests/fixtures-only design review for the next narrow runtime slice after the completed Phase 30 read-only runtime state inspection slice, with no new runtime implementation, no new `lima/` changes, no `tests/support/` changes, no Sparkbot wiring, no HumanInput runtime bridge behavior, no live adapters, no IntentCompiler runtime behavior, no GuardianDecision runtime behavior, no approval enforcement, no execution, no dispatch, no audit persistence, no shell/browser/network/file mutation, no robotics, no physical-world action, no external service calls, no background workers, no queues, no daemons, no subprocesses, no threads, no database writes, and no hidden side effects?

## Continue

Continue only to Phase 31.4 Phase 31 runtime slice audit archive / closeout.
