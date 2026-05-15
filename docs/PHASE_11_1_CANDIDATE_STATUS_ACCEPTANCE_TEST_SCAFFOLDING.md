# Phase 11.1 Candidate Status Acceptance Test Scaffolding

Phase 11.1 converts the Phase 10.3 acceptance-test requirements into a concrete test plan for the Phase 11.2 and Phase 11.3 runtime implementation phases. It does not implement candidate status normalization or candidate validation.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not change helper behavior, does not add `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add live adapters, does not implement HumanInput runtime bridge behavior, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Runtime Acceptance Test Families

Phase 11.2 must add tests proving candidate status normalization:

- valid Phase 9-style candidates normalize to an allowed safe status
- allowed statuses are limited to `proposed`, `needs_review`, and `blocked`
- unknown status normalizes to `blocked` or `needs_review`
- approved status never survives normalization
- `execution_allowed` remains false
- `side_effects_allowed` remains false
- provenance is preserved

Phase 11.3 must add tests proving candidate validation:

- malformed candidates are rejected or marked invalid safely
- candidates missing `execution_allowed` fail closed
- candidates missing `side_effects_allowed` fail closed
- candidates with `execution_allowed: true` fail closed
- candidates with `side_effects_allowed: true` fail closed
- candidates with `approval_state: approved` fail closed
- stale or replayed candidates remain blocked or invalid when those markers are present
- validation cannot approve, execute, persist, or dispatch

Both implementation phases must prove:

- no Sparkbot import or wiring exists
- no HumanInput runtime bridge exists
- no live adapter exists
- no IntentCompiler runtime behavior changes
- no GuardianDecision runtime behavior changes
- no shell, browser, network, file mutation, robotics, or physical-world behavior is reachable
- only Phase 10.2 eligible runtime files are touched
- Phase 5 runtime bridge remains gated

## Next Step

Phase 11.2 may implement candidate status normalization within the Phase 10.2 file-touch map.
