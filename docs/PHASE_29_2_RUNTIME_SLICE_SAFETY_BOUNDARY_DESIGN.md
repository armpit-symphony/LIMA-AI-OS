# Phase 29.2 Runtime Slice Safety Boundary Design

Phase 29.2 defines the no-code safety boundary for the recommended future read-only runtime state inspection slice.

This phase is safety boundary design only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Future Slice Boundary

The future slice may only expose deterministic, local-only, read-only inspection of already-existing non-executing runtime candidate state.

The future slice may produce an inspectable, non-authoritative state snapshot that describes candidate safety flags, provenance presence, status category, and blocked/not-ready/needs-review signals.

The future slice must not mutate candidate state, create candidates from HumanInput, infer IntentEnvelope runtime behavior, preview GuardianDecision behavior, enforce approval, persist audit, dispatch work, execute tools, call external systems, or perform physical-world action.

## Future Eligible Runtime File Scope

The proposed future runtime implementation, if separately approved later, should be limited to:

- a possible new `lima/kernel/runtime_state.py`,
- and `lima/kernel/__init__.py` only if a safe public export is required.

The future slice should not modify `lima/kernel/intake_candidate.py`, `lima/kernel/candidate_status.py`, new live adapter modules, Sparkbot files, IntentCompiler runtime behavior, GuardianDecision runtime behavior, or any other `lima/` files.

## Required Safety Invariants

- Output is non-authoritative.
- Output is deterministic and local-only.
- `execution_allowed` remains false.
- `side_effects_allowed` remains false.
- `approval_state` is never approved.
- Unknown or malformed inspected state is reported as blocked, invalid, not-ready, or needs-review.
- Operator, admin, Phil, trusted, urgent, override, approve, or emergency wording does not change the inspection result.
- Phase 5 HumanInput runtime bridge remains gated.

## Continue

Continue only to Phase 29.3 future implementation eligibility matrix.
