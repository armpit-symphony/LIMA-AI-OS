# Phase 41.2 Arc Bot Candidate Preview Regression Tests

Phase 41.2 adds regression tests over the Phase 41.1 Arc Bot / LIMA Office fixture corpus using the existing `candidate_preview` helper.

This phase does not modify `candidate_preview.py`, `lima/`, `tests/support/`, Sparkbot, Arc Bot implementation, HumanInput bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Regression Intent

The tests prove that Arc Bot-shaped office task metadata remains:

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
- robotics and physical-world inactive

## Conservative Blocking Note

The existing helper may block some fixtures more conservatively than their planning label. For example, planning keys such as `operator_posture` or `dry_run_posture` are caller-provided strings and may trigger suspicious claim detection. This is acceptable for Phase 41 because it is safer than review-only output and does not require runtime changes.

## Continue

Continue only to Phase 41.3 Arc Bot hardening gap and next-lane review.
