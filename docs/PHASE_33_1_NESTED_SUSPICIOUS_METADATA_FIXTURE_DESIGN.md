# Phase 33.1 Nested Suspicious Metadata Fixture Design

Phase 33.1 adds synthetic caller-provided fixture data for nested suspicious metadata around the existing read-only `runtime_state` inspection slice.

This phase is test-only fixture design. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, and does not add Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, execution, approval enforcement, dispatch, audit persistence, shell/browser/network/file mutation, robotics, physical-world action, external service calls, background workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects.

## Fixture Coverage

The Phase 33.1 fixture set covers:

- nested authority wording using `Phil`, `operator`, `admin`, `trusted`, `urgent`, `override`, `approve`, and `emergency`
- nested Sparkbot wiring claims
- nested HumanInput bridge activation claims
- nested live adapter activation claims
- nested shell/browser/network/file mutation claims
- nested robotics and physical-world action claims
- nested external service, subprocess, thread, queue, daemon, and database-write claims
- malformed nested metadata values
- unknown nested statuses and values

## Expected Safety Outcome

The fixtures are caller-provided data only. They must not create authority, approval, execution, dispatch, persistence, bridge behavior, adapter behavior, Sparkbot wiring, robotics, physical-world action, external calls, or hidden side effects.

Phase 33.2 will use these fixtures in regression tests against the existing `inspect_runtime_state` API without changing runtime code.

## Continue

Continue only to Phase 33.2 runtime state nested metadata regression tests.
