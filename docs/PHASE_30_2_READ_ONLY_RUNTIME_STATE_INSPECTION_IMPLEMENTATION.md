# Phase 30.2 Read-Only Runtime State Inspection Implementation

Phase 30.2 implements the approved narrow read-only runtime state inspection slice.

This phase adds `lima/kernel/runtime_state.py` and a safe public export in `lima/kernel/__init__.py` following the existing kernel package convention. It does not modify `lima/kernel/intake_candidate.py`, does not modify `lima/kernel/candidate_status.py`, does not modify any other existing `lima/` files, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Runtime Behavior Added

`inspect_runtime_state` accepts caller-provided candidate-like metadata and returns a deterministic, local-only, read-only, non-authoritative snapshot dictionary.

The snapshot is advisory only and always reports:

- `execution_allowed` as false,
- `side_effects_allowed` as false,
- `approved` as false,
- `approval_state` as blocked,
- `dispatch_allowed` as false,
- `persistence_allowed` as false,
- Phase 5 HumanInput runtime bridge as gated,
- Sparkbot wiring as absent,
- live adapter as absent,
- IntentEnvelope creation as absent,
- GuardianDecision creation as absent.

Malformed, missing, unknown, suspicious, stale-like, replay-like, or bypass-wording state remains blocked, invalid, or not execution-ready.

## Export Rationale

`lima/kernel/__init__.py` was changed only to expose the new safe public inspection primitive through the existing kernel package pattern. Importing `lima.kernel` remains side-effect-free.

## Continue

Continue only to Phase 30.3 runtime state inspection boundary regression review.
