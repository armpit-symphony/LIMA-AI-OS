# Phase 35.2 Second-Slice Safety And Scope Comparison

Phase 35.2 compares the Phase 35.1 candidate second runtime slices by safety, usefulness, file scope, testability, rollback simplicity, and risk.

This phase is docs/tests/fixtures-only design review. It does not modify `lima/`, does not modify `tests/support/`, and does not approve Phase 36 implementation.

## Comparison Summary

| Option | Safety | Usefulness | Scope Clarity | Testability | Rollback | Result |
| --- | --- | --- | --- | --- | --- | --- |
| A: test-only continuation | Highest | Medium | Clear | High | Simple | Safe fallback, but not a runtime slice. |
| B: second read-only inspection helper | High | Low to medium | Moderate | High | Simple | Duplicates some Phase 30 value. |
| C: non-executing candidate preview helper | High if tightly bounded | High | Clear if limited to new helper plus optional export | High | Simple | Recommended future Phase 36 candidate if approved. |
| D: candidate status wrapper | Medium | Medium | Weak | Medium | Moderate | Not recommended because it risks touching existing status behavior. |
| E: GuardianDecision preview planning | Medium to low | Medium | Weak | Medium | Moderate | Planning-only; too authority-adjacent for implementation now. |
| F: HumanInput bridge planning | Low for implementation | High later | Weak | Medium | Hard | Planning-only; bridge behavior remains gated. |
| G: Sparkbot boundary planning | Low for implementation | High later | Weak | Medium | Hard | Planning-only; Sparkbot wiring remains forbidden. |
| H: pause/preserve | Highest | Low | Clear | High | Simple | Safe fallback if Phase 36 is not approved. |

## Recommended Future Candidate

Option C remains the recommended future Phase 36 implementation candidate if Phil approves it later.

The candidate must be:

- deterministic
- local-only
- side-effect free
- read-only
- non-authoritative
- non-executing
- caller-provided-data only
- safe under missing, malformed, unknown, suspicious, nested, or bypass-worded input

## Exact Future File Scope Under Review

If Phase 36 implementation is approved later, the proposed runtime file scope should be limited to:

- `lima/kernel/candidate_preview.py`
- `lima/kernel/__init__.py` only if a safe public export is required by existing package convention

Phase 36 should not touch:

- `lima/kernel/runtime_state.py`
- `lima/kernel/intake_candidate.py`
- `lima/kernel/candidate_status.py`
- any other `lima/` file
- `tests/support/`

## Explicit Forbidden Behaviors

The future candidate remains ineligible if it requires HumanInput bridge behavior, Sparkbot wiring, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, persistence, audit persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external service calls, workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Continue

Continue only to Phase 35.3 Phase 36 eligibility and test plan matrix.
