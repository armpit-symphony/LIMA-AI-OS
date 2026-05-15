# Phase 11.2 Candidate Status Normalization Runtime Implementation

Phase 11.2 implements candidate status normalization for existing non-executing intake candidates.

This is the first Phase 11 runtime implementation touch. It stays inside the Phase 10.2 eligible file map:

- `lima/kernel/candidate_status.py`
- `lima/kernel/__init__.py`

This phase does not modify runtime files outside the Phase 10.2 eligible list, does not modify `tests/support/`, does not change helper behavior, does not create HumanInput runtime bridge behavior, does not wire Sparkbot, does not add live adapters, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Runtime Behavior Added

`lima/kernel/candidate_status.py` adds pure in-process candidate status normalization for already-created intake candidates.

It:

- copies candidate metadata into a new dictionary
- emits only `proposed`, `needs_review`, or `blocked` as `candidate_status`
- forces `executable` false
- forces `execution_allowed` false
- forces `side_effects_allowed` false
- forces `approved` false
- never preserves `approval_state: approved`
- preserves provenance
- blocks unknown, stale, replayed, execution-enabled, side-effect-enabled, or approved candidate states
- preserves the Phase 5 HumanInput runtime bridge gate

## Static Test Adjustment

Phase 10.5 and Phase 11.0 contained historical pre-implementation assertions that `lima/kernel/candidate_status.py` was absent. Phase 11.2 is the explicitly approved phase that creates that eligible runtime file, so those tests now assert their phase fixtures instead of current filesystem absence.

This mirrors the earlier accepted Phase 8.1 warning: static pre-implementation tests must not fail after an explicitly approved eligible runtime file is created.

## What Phase 11.2 Does Not Add

- no candidate validation yet beyond status safety normalization
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

Phase 11.3 may implement candidate validation within the Phase 10.2 file-touch map.
