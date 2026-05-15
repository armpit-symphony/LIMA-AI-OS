# Phase 11.3 Candidate Validation Runtime Implementation

Phase 11.3 implements candidate validation for existing non-executing intake candidates.

This phase stays inside the Phase 10.2 eligible file map:

- `lima/kernel/candidate_status.py`
- `lima/kernel/__init__.py`

This phase does not modify runtime files outside the Phase 10.2 eligible list, does not modify `tests/support/`, does not change helper behavior, does not create HumanInput runtime bridge behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Runtime Behavior Added

`validate_candidate` validates already-created intake candidate metadata and returns a fail-closed candidate dictionary.

It:

- requires the Phase 9 candidate shape
- requires provenance
- rejects missing safety fields
- rejects `executable: true`
- rejects `execution_allowed: true`
- rejects `side_effects_allowed: true`
- rejects `approval_state: approved`
- rejects `approved: true`
- treats stale or replayed markers as invalid
- preserves non-executing flags as false
- preserves the Phase 5 HumanInput runtime bridge gate
- uses candidate status normalization before returning

## What Phase 11.3 Does Not Add

- no HumanInput runtime bridge
- no Sparkbot wiring
- no live adapter
- no IntentCompiler runtime behavior
- no GuardianDecision runtime behavior
- no approval enforcement
- no execution
- no dispatch
- no audit persistence
- no shell, browser, network, file mutation, robotics, or physical-world action

## Next Step

Phase 11.4 may review the runtime slice before Phase 11.5 archive closeout.
