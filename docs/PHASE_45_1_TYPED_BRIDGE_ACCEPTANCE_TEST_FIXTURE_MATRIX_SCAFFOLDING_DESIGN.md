# Phase 45.1 Typed Bridge Acceptance Test Fixture Matrix / Scaffolding Design

Phase 45.1 opens docs/tests/fixtures-only no-code acceptance-test fixture matrix and scaffolding design for a future typed IntentEnvelope / Guardian request bridge runtime slice.

This phase does not implement runtime bridge behavior. This phase does not create a runtime test harness. This phase does not create GuardianDecision records, approval enforcement, execution, dispatch, persistence, model/tool/driver calls, adapter calls, external calls, shell/browser/network/file mutation, robotics, physical-world behavior, background work, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Mission

Map Phase 45.0 required future acceptance-test families into inert fixture matrix/scaffolding metadata:

source request metadata -> typed IntentEnvelope candidate metadata -> Guardian request metadata -> future GuardianDecision metadata -> still no execution.

The matrix design exists to lock expected future test coverage shape before any runtime bridge implementation or runtime harness scope is considered.

## Fixture Matrix Scope

Phase 45.1 may define:

- matrix row identifiers for future positive shape checks
- matrix row identifiers for fail-closed negative/bypass checks
- expected bridge state categories for future tests
- expected GuardianDecision metadata state categories for future tests
- expected blocked claim categories for future tests
- required non-authoritative control flag expectations for future tests

Phase 45.1 may not define or execute runtime behavior.

## Required Matrix Coverage

The fixture matrix/scaffolding design must include future rows for:

- source request metadata shape validation across HumanInput, shell, bot, and automation sources
- typed IntentEnvelope candidate metadata shape validation
- Guardian request metadata shape validation
- GuardianDecision metadata boundary validation limited to absent/pending/blocked
- malicious approval claim fail-closed behavior
- forged GuardianDecision claim fail-closed behavior
- missing identity or lineage fail-closed behavior
- background scheduling/dispatch claim fail-closed behavior
- adapter or external-call claim fail-closed behavior
- model/tool/driver-call claim fail-closed behavior
- robotics/physical-world claim fail-closed behavior
- runtime/support path boundary checks (`lima/` and `tests/support`)

## Boundary Result

Phase 45.1 remains acceptance-test fixture matrix/scaffolding design only.

No runtime bridge behavior was added.
No runtime test harness was created.
No `lima/` file changed.
No `tests/support` file changed.

## Recommended Next Direction

Stop at review for Phase 45.1. If Phil approves, Phase 45.2 may add docs/tests/fixtures-only acceptance-test matrix readiness review. Runtime implementation remains blocked.
