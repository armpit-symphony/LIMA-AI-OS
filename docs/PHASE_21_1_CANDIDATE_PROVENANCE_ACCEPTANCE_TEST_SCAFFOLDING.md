# Phase 21.1 Candidate Provenance Acceptance Test Scaffolding

Phase 21.1 adds test-only acceptance coverage for candidate provenance hardening before runtime implementation.

This phase does not modify runtime files. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not approve execution, does not enforce approval, does not dispatch, does not persist audit, and does not add shell, browser, network, file mutation, robotics, or physical-world behavior.

## Acceptance Coverage

The Phase 21.1 tests cover:

- valid non-executing candidates preserve provenance
- missing provenance is rejected or invalid
- empty provenance is rejected or invalid
- non-mapping provenance is rejected or invalid
- suspicious provenance wording does not bypass safety
- stale and replayed candidates remain blocked or invalid
- `execution_allowed` remains false
- `side_effects_allowed` remains false
- `approval_state` is never approved
- no Sparkbot wiring, HumanInput runtime bridge, live adapter, execution, dispatch, approval enforcement, audit persistence, shell, browser, network, file mutation, robotics, or physical-world behavior is reachable
- only Phase 21 approved runtime files may be touched by the later implementation phase

## Gate

Phase 21.1 does not implement provenance hardening. Phase 21.2 may touch only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`.
