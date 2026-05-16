# Phase 29.3 Future Implementation Eligibility Matrix

Phase 29.3 defines the no-code eligibility matrix for a possible future read-only runtime state inspection implementation slice.

This phase is eligibility design only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Future Slice Recommendation

The recommended future runtime slice is read-only runtime state inspection.

The future slice may only inspect already-existing non-executing candidate state and return deterministic, local-only, non-authoritative snapshot metadata. It must not create candidates, mutate candidates, compile intents, preview GuardianDecision behavior, enforce approval, persist audit, dispatch work, execute tools, or call external systems.

## Future Eligible Runtime Files

If Phil explicitly approves a later implementation phase, the future runtime file scope should be limited to:

- a possible new `lima/kernel/runtime_state.py`,
- `lima/kernel/__init__.py` only if a safe public export is required.

No other runtime files are eligible under this design. `lima/kernel/intake_candidate.py`, `lima/kernel/candidate_status.py`, all other `lima/` files, new live adapter modules, Sparkbot files, IntentCompiler behavior, and GuardianDecision behavior remain forbidden.

## Eligibility Criteria

A future implementation phase is eligible only if all of the following are true:

- Phil explicitly approves the runtime implementation scope.
- The approved scope names exact runtime files before edits begin.
- Tests are written before runtime edits and cover the read-only inspection contract.
- The implementation remains deterministic, local-only, read-only, non-authoritative, and side-effect-free.
- The implementation operates only on already-existing non-executing candidate state.
- The output preserves `execution_allowed` as false, `side_effects_allowed` as false, and never reports `approval_state` as approved.
- Missing, malformed, unknown, suspicious, stale, or replayed inspected state is surfaced as blocked, invalid, not-ready, or needs-review.
- Operator, admin, Phil, trusted, urgent, override, approve, or emergency wording does not change inspection output.
- Rollback can remove the future runtime file and safe export without changing existing candidate behavior.
- Audit proof shows no forbidden imports, calls, persistence, dispatch, execution, background work, or external side effects.
- Phase 5 HumanInput runtime bridge remains gated.

## Required Future Acceptance Tests

Before any future implementation lands, acceptance tests must prove:

- valid non-executing candidate state produces a non-authoritative read-only snapshot,
- malformed candidate state is reported blocked, invalid, not-ready, or needs-review,
- unknown status or missing provenance does not become executable or approved,
- stale, replayed, suspicious, or bypass-wording state does not change safety outcome,
- `execution_allowed` remains false,
- `side_effects_allowed` remains false,
- `approval_state` is never approved,
- no mutation of input candidate state occurs,
- no Sparkbot import or wiring exists,
- no HumanInput runtime bridge exists,
- no live adapter exists,
- no execution, dispatch, approval enforcement, audit persistence, shell, browser, network, file mutation, robotics, physical-world action, external service call, background worker, queue, daemon, subprocess, thread, database write, or hidden side effect is reachable.

## Future Phase 30 Approval Question

Do you approve Phase 30 as a narrow runtime implementation slice limited to read-only runtime state inspection, touching only a possible new `lima/kernel/runtime_state.py` and `lima/kernel/__init__.py` only if a safe public export is required, requiring Phase 29.3 acceptance tests, rollback plan, and audit proof, and still forbidding `lima/kernel/intake_candidate.py`, `lima/kernel/candidate_status.py`, all other `lima/` files, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, physical-world action, external service calls, background workers, queues, daemons, subprocesses, threads, database writes, and hidden side effects?

## Continue

Continue only to Phase 29.4 Phase 29 no-code design review archive / closeout.
