# Phase 35.3 Phase 36 Eligibility And Test Plan Matrix

Phase 35.3 defines the eligibility criteria, acceptance-test requirements, rollback/audit proof, stop conditions, and exact approval question for a possible future Phase 36 candidate preview helper.

This phase does not approve implementation. It does not modify `lima/`, does not modify `tests/support/`, and does not add runtime behavior.

## Phase 36 Eligibility Criteria

A future Phase 36 implementation is eligible only if it remains:

- deterministic
- local-only
- side-effect free
- read-only
- non-authoritative
- non-executing
- caller-provided-data only
- inspectable
- safe by default
- safe under missing, malformed, unknown, suspicious, nested, or bypass-worded input
- fully testable without `tests/support/` changes
- revertible by removing only Phase 36 files and an optional safe export

It must avoid filesystem reads or writes, environment reads, network calls, shell calls, browser calls, database access, background workers, queues, daemons, subprocesses, threads, approval enforcement, execution, dispatch, persistence, audit persistence, HumanInput runtime bridge behavior, Sparkbot wiring, live adapters, robotics, and physical-world behavior.

## Phase 36 Acceptance-Test Requirements

Future Phase 36 acceptance tests must prove:

- benign caller-provided data yields inspectable, non-authoritative preview output
- missing input yields safe blocked, invalid, or needs-review preview output
- malformed input yields safe blocked, invalid, or needs-review preview output
- unknown values remain safe
- suspicious nested metadata remains safe
- bypass wording does not change authority or safety outcome
- `execution_allowed` remains false
- `side_effects_allowed` remains false
- approval remains false or blocked
- dispatch remains false or blocked
- persistence remains false or blocked
- Phase 5 HumanInput runtime bridge remains gated
- Sparkbot wiring/imports remain absent
- live adapters remain absent
- shell/browser/network/file mutation, robotics, physical-world behavior, external calls, background workers, queues, daemons, subprocesses, threads, database writes, and hidden side effects remain absent
- only the approved future runtime files changed
- `tests/support/` did not change

## Rollback And Audit Proof

Future Phase 36 rollback must be simple:

- remove `lima/kernel/candidate_preview.py`
- remove the `lima/kernel/__init__.py` safe export if it was added
- remove Phase 36 docs/tests/fixtures

Audit proof must include:

- `git diff --name-only` against pre-Phase-36 main
- explicit report on whether `lima/kernel/__init__.py` changed and why
- forbidden-import and forbidden-behavior scan
- targeted Phase 36 tests
- all Phase 36 tests so far
- full suite
- `python -m compileall lima`
- `git diff --check`
- clean synced status

## Stop Conditions

Stop before implementation if Phase 36 would require:

- changes to `lima/kernel/runtime_state.py`
- changes to `lima/kernel/intake_candidate.py`
- changes to `lima/kernel/candidate_status.py`
- changes to any other `lima/` file outside the approved candidate preview scope
- `tests/support/` changes
- HumanInput runtime bridge behavior
- Sparkbot wiring/imports
- live adapters
- IntentCompiler runtime behavior
- GuardianDecision runtime behavior
- approval enforcement
- execution
- dispatch
- persistence or audit persistence
- shell/browser/network/file mutation
- robotics or physical-world behavior
- external service calls
- workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects
- a real product or safety decision from Phil

## Exact Phase 36 Approval Question

Do you approve Phase 36 as a narrow runtime implementation slice limited to a non-executing, local-only, read-only, non-authoritative candidate preview helper that accepts only caller-provided data and emits inspectable safe preview output, touching only a possible new `lima/kernel/candidate_preview.py` and `lima/kernel/__init__.py` only if a safe public export is required by existing package convention, plus Phase 36 docs/tests/fixtures, requiring the Phase 35.3 acceptance tests and rollback/audit proof, and still forbidding changes to `lima/kernel/runtime_state.py`, `lima/kernel/intake_candidate.py`, `lima/kernel/candidate_status.py`, all other `lima/` files, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, physical-world action, external service calls, background workers, queues, daemons, subprocesses, threads, database writes, and hidden side effects?

## Continue

Continue only to Phase 35.4 Phase 35 design review archive and closeout.
