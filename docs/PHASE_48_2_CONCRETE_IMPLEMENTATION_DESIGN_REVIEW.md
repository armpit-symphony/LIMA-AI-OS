# Phase 48.2 Concrete Implementation Design Review

Phase 48.2 designs the first possible concrete implementation lane after the Phase 48.1 implementation gate readiness review.

This phase is docs/tests/fixtures-only.
This phase is not implementation.
This phase is not runtime implementation.
This phase is not `tests/support` implementation.
This phase does not create executable acceptance tests.
This phase does not create or activate a runtime test harness.
This phase does not modify `lima/`.
This phase does not modify `tests/support/`.
This phase does not modify Sparkbot Shell.

## V1 Product Direction Captured

Phase 48.2 now also records the current V1 product-readiness target in `docs/V1_PRODUCT_READINESS_TARGET.md`.

That target clarifies:

- first shell consumers are `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`
- Sparkbot remains the R&D shell behavior reference
- live/actual approval, real `GuardianDecision`, provider/model routing, haptic intent support, and first-shell response-state parity are acceptable future V1 product capabilities
- deleting or editing anything must require operator approval in LIMA-AI-OS and shells
- haptic rendering remains shell-owned; LIMA may define future haptic intent metadata only

This does not approve implementation in Phase 48.2. It gives the next design/readiness lane a clearer V1 target.

## Reviewed Phase

- Phase 48.1 implementation gate readiness review.

## Proposed First Implementation Lane

Suggested future lane:

- `first_concrete_typed_bridge_acceptance_test_design`

Candidate status:

- `design_only`

Implementation approved:

- false

The candidate future lane would create executable proof only if Phil separately approves it later. Its intent would be to prove typed bridge contract shape without runtime authority, preserve non-authoritative preview posture, avoid runtime side effects, avoid Sparkbot Shell live wiring, and avoid robotics, IoT, or physical-world behavior.

## Candidate Future Allowed File Scope

These file names are candidate future names only. Phase 48.2 does not create them.

- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_preview_only_positive.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_approval_bypass.json`
- `tests/fixtures/runtime_extraction/typed_bridge_acceptance_fail_closed_runtime_claim.json`
- `tests/test_typed_bridge_acceptance_preview_only.py`

The first concrete lane should try to stay under docs/tests/fixtures-only scope. It should avoid `lima/` and `tests/support/` unless a later Phil approval packet explicitly names those paths.

## Candidate Future Forbidden File Scope

The future lane must continue to forbid:

- `lima/`
- `tests/support/`
- Sparkbot Shell paths
- `adapters/`
- `drivers/`
- `persistence/`
- runtime dispatch paths
- robotics, IoT, drone, humanoid, or physical-world paths
- shell, browser, network, or file mutation paths
- background workers, queues, daemons, subprocesses, threads, or database writes

## Candidate Future Behavior Boundaries

The future lane must continue to forbid:

- real IntentCompiler behavior
- GuardianDecision creation
- approval enforcement
- execution, dispatch, or persistence
- model, tool, driver, or external calls
- Sparkbot runtime integration
- Guardian approval or enforcement claims
- robotics or physical-world behavior
- hidden side effects

## Sparkbot Shell Implication

Sparkbot Shell can safely depend on LIMA vocabulary only as non-authoritative mock/display-only preview guidance.

Sparkbot Shell can prepare UI language for:

- consumer profile
- embodiment profile
- approval posture
- evidence references
- preview state
- blocked state

Sparkbot Shell must not claim:

- LIMA runtime integration
- Guardian approval or enforcement
- dispatch, execution, persistence, adapter calls, robotics control, or IoT control through LIMA

Sparkbot Shell files must not change in Phase 48.2.

## Required Future Approval Packet

Before any candidate implementation lane begins, the approval packet must include:

- explicit Phil approval
- exact allowed file list
- exact forbidden file list
- rollback plan
- validation checklist
- independent pre-merge audit
- post-merge verification plan
- active-allowance scan
- hidden side-effect scan
- confirmation that runtime, `lima/`, `tests/support`, and Sparkbot Shell changes remain absent unless explicitly approved

## Stop Conditions

Stop the future lane if any of these occur:

- unapproved `lima/` change
- unapproved `tests/support` change
- Sparkbot Shell file change
- runtime behavior
- runtime harness creation or activation
- executable acceptance tests created in Phase 48.2
- GuardianDecision creation
- approval enforcement
- execution, dispatch, or persistence
- model, tool, driver, or external calls
- robotics or physical-world behavior
- active implementation approval flag set true
- failed validation
- dirty worktree
- base or tag mismatch

## Boundary Result

Phase 48.2 confirms:

- no runtime bridge behavior
- no runtime test harness creation or activation
- no actual acceptance-test harness behavior
- no executable runtime bridge acceptance tests
- no `lima/` changes
- no `tests/support/` changes
- no Sparkbot Shell changes
- no Sparkbot wiring
- no HumanInput bridge behavior
- no real IntentCompiler behavior
- no real Guardian request runtime behavior
- no GuardianDecision creation
- no approval enforcement
- no execution, dispatch, or persistence
- no model/tool/driver calls
- no external calls
- no shell/browser/network/file mutation
- no robotics or physical-world behavior
- no hidden side effects

## Recommended Next Lane

- Default: `phase_48_3_docs_tests_fixtures_only_design_readiness_review`.
- Acceptable alternative: `pause_preserve`.

Runtime implementation remains blocked. Any implementation lane still requires separate explicit Phil approval after this design review.
