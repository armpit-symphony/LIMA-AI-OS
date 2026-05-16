# Phase 21.2 Candidate Provenance Hardening Runtime Implementation

Phase 21.2 implements the approved narrow runtime slice for candidate provenance hardening.

This phase touches only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py` as runtime files. It does not modify `lima/kernel/__init__.py`, does not add runtime modules, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, call shell, browser, network, filesystem mutation, robotics, external services, or physical-world systems, and does not start background workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Runtime Change

The implementation hardens provenance metadata for existing non-executing candidates only:

- candidate construction rejects malformed provenance keys and missing provenance values
- status normalization blocks malformed or suspicious provenance
- validation marks malformed or suspicious provenance invalid
- valid provenance remains preserved
- non-executing candidate guarantees remain forced

## Safety Guarantees

- `execution_allowed` remains false
- `side_effects_allowed` remains false
- `approval_state` is never approved
- suspicious operator/admin/Phil/trusted/urgent/override/approve provenance wording cannot bypass safety
- stale or replayed candidates remain blocked or invalid
- Phase 5 HumanInput runtime bridge remains gated

## Gate

Phase 21.2 does not expand runtime scope. Phase 21.3 must review the runtime slice as regression-only documentation, fixtures, and tests unless a later explicit approval changes scope.
