# Phase 43.2 Universal Contract Profile Regression Tests

Phase 43.2 adds regression tests over the Phase 43.1 universal contract profile fixture corpus using the existing `candidate_preview` helper.

This phase does not modify `candidate_preview.py`, `lima/`, `tests/support/`, Sparkbot, Arc Bot implementation, HumanInput bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Regression Intent

The tests prove universal profile metadata remains:

- deterministic
- read-only
- local-only
- non-authoritative
- safe by default
- non-executing
- side-effect free
- approval-free
- dispatch-free
- persistence-free
- bridge-inactive
- adapter-inactive
- Sparkbot-wiring inactive
- external-call inactive
- robotics inactive
- physical-world inactive

## Conservative Blocking Note

The existing helper may block some safe planning fixtures more conservatively than their planning label because profile metadata contains words such as operator, approval, browser, network, shell, file, Sparkbot, robot, emergency, or override. Conservative blocking is acceptable for Phase 43.2 because these tests are safety regression tests, not product readiness tests.

## Continue

Continue only to Phase 43.3 docs/tests/fixtures-only hardening gap and next-lane review. No runtime implementation is approved.
