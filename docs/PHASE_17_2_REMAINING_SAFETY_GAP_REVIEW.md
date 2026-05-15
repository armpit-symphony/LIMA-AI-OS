# Phase 17.2 Remaining Safety Gap Review

Phase 17.2 reviews the remaining safety gaps after the Phase 16 test-only acceptance implementation.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Remaining Gaps

- Future runtime file coverage remains narrow and must be re-evaluated for each approved runtime slice.
- Static forbidden-pattern checks are not a substitute for runtime policy enforcement.
- Existing contract tests cover current non-executing candidate APIs, not future runtime behavior.
- Synthetic threat fixtures are inert and do not represent live integration traffic.
- Approval semantics remain non-enforcing and must not be inferred from HumanInput, operator wording, Phil wording, admin wording, or trusted wording.
- Audit persistence remains unimplemented and must not be simulated as live persistence.
- Sparkbot integration, HumanInput runtime bridge behavior, live adapters, and Robo-OS / physical-world boundaries remain separate future lanes.

## Gaps That Block Runtime Expansion

Runtime expansion remains blocked until a later explicitly approved lane defines:

- exact runtime file-touch scope
- acceptance tests for the next slice
- rollback and audit proof
- forbidden behavior checks for the expanded scope
- clear decision ownership for approval semantics
- continued Phase 5 HumanInput runtime bridge gating

## Conclusion

Phase 16 acceptance coverage is useful, but it does not remove the need for a separate next-lane decision. Phase 17.3 should compare the safest next-lane options before Phase 17 closes.
