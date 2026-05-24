# Phase 46.0 Static Acceptance-Test Implementation-Plan Template

Phase 46.0 opens a docs/tests/fixtures-only static implementation-plan template lane for future typed bridge acceptance-test implementation planning.

This phase does not implement runtime bridge behavior. This phase does not create a runtime test harness. This phase does not add executable acceptance tests for a runtime bridge. This phase does not modify `lima/` or `tests/support/` behavior.

## Mission

Define the static template a future explicitly approved phase could use before implementing typed IntentEnvelope / Guardian request bridge acceptance tests.

The template covers:

- what future acceptance-test implementation would need to prove
- what files might be eligible in a future approved implementation phase
- what files remain forbidden
- what validation and rollback gates are mandatory
- what runtime boundaries must stay blocked
- what Phil approval gates are required before any actual implementation

## Future Acceptance-Test Proof Requirements

A future approved acceptance-test implementation phase would need to prove:

- source request metadata is accepted only as deterministic input metadata
- typed IntentEnvelope candidate metadata is non-authoritative
- Guardian request metadata is not GuardianDecision authority
- expected bridge states remain non-executing unless a separate runtime design/audit gate approves otherwise
- GuardianDecision metadata remains absent, pending, or blocked until real Guardian policy membrane work is explicitly approved
- malicious approval claims fail closed
- forged GuardianDecision claims fail closed
- missing actor, tenant, or lineage metadata fails closed
- background scheduling, adapter, external-call, model/tool/driver-call, persistence, dispatch, execution, robotics, and physical-world claims fail closed
- runtime/support boundary checks prove no unapproved `lima/` or `tests/support/` scope is changed

## Future Eligible File Scope

Only after separate Phil approval, a future acceptance-test implementation phase may be eligible to touch:

- new static test files under `tests/` that validate inert fixture or plan metadata
- new inert JSON fixtures under `tests/fixtures/runtime_extraction/`
- phase documentation under `docs/`
- project-tracking updates in README/current-state/roadmap/decision/extraction-plan files

Future eligibility does not approve runtime implementation.

## Forbidden File Scope

Phase 46.0 keeps the following forbidden for this lane and for any future phase unless Phil explicitly approves a separate design/audit gate:

- `lima/` runtime behavior changes
- `tests/support/` helper behavior changes
- runtime test harness creation or activation
- actual acceptance-test harness behavior
- Sparkbot wiring
- Arc Bot implementation
- HumanInput bridge behavior
- live adapters
- real IntentCompiler behavior
- real Guardian request runtime behavior
- GuardianDecision creation
- approval enforcement
- execution, dispatch, or persistence
- external calls
- model/tool/driver calls
- shell/browser/network/file mutation
- robotics, hardware control, or physical-world behavior
- background workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects

## Mandatory Validation Gate

Any future phase that uses this template must run at minimum:

- Python version check
- JSON fixture validation for the phase fixture
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git status --short`

The future phase must stop and report before merge/tag if validation fails.

## Mandatory Rollback Gate

A future approved implementation-plan or test implementation phase must define rollback before merge:

- list every changed file
- confirm the diff is limited to the approved file scope
- confirm no `lima/` path changed unless the explicit phase approval allowed it
- confirm no `tests/support/` path changed unless the explicit phase approval allowed it
- confirm no hidden side effect, external call, runtime worker, or persistence path was introduced
- keep merge/tag blocked until Phil approves after an independent audit

## Phil Approval Gates

Phil approval is required before:

- implementing actual acceptance tests
- creating any runtime test harness
- modifying `lima/`
- modifying `tests/support/`
- adding real typed bridge behavior
- adding real IntentCompiler behavior
- adding real Guardian request runtime behavior
- creating GuardianDecision records
- adding approval enforcement
- adding execution, dispatch, persistence, model/tool/driver calls, external calls, robotics, hardware control, physical-world behavior, background work, subprocesses, threads, database writes, or hidden side effects
- merge or tag

## Boundary Result

Phase 46.0 is a static implementation-plan template only.

No runtime implementation is recommended by Phase 46.0.
No next runtime implementation is approved by Phase 46.0.
No `lima/` file changed.
No `tests/support` file changed.

## Recommended Next Direction

Stop at review for Phase 46.0. If Phil approves, Phase 46.1 may add docs/tests/fixtures-only static dry-run planning or archive/readiness review. Runtime implementation remains blocked.
