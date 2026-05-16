# Phase 20.2 Exact File-Touch Map For Candidate Slice

Phase 20.2 defines the exact future runtime file-touch map for the Phase 20.1 recommended candidate provenance hardening slice.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `candidate_status.py` or `intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not approve execution, does not enforce approval, does not dispatch, does not persist audit, and does not add shell, browser, network, file mutation, robotics, or physical-world behavior.

## Future Eligible Runtime Files

If Phil later approves Phase 21 candidate provenance hardening, the only eligible runtime files are:

- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`

## Future Forbidden Runtime Files

The future Phase 21 slice must not touch:

- `lima/kernel/__init__.py`
- any new `lima/kernel/candidate_provenance.py`
- any other `lima/` file
- any `tests/support/` file
- any Sparkbot file
- any live adapter, IntentCompiler, GuardianDecision, approval, execution, dispatch, audit persistence, shell, browser, network, file mutation, robotics, or physical-world file

## Future Touch Intent

`lima/kernel/intake_candidate.py` may only define provenance shape requirements for candidate construction and keep every candidate non-executing.

`lima/kernel/candidate_status.py` may only validate or normalize provenance metadata for existing non-executing candidates and keep validation/status normalization fail-closed.

## Gate

Phase 20.2 does not approve Phase 21. Phase 20.3 must define acceptance tests and rollback/audit proof before any implementation approval question is preserved.
