# Phase 22.3 Next-Lane Decision Matrix

Phase 22.3 compares the approved Phase 22 next-lane options and recommends exactly one Phase 23 direction.

This phase is docs/tests/fixtures only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Decision Matrix

| Option | Direction | Recommendation |
| --- | --- | --- |
| A | no-code design for another narrow runtime slice | defer |
| B | test-only hardening for provenance/candidate invariants | recommend |
| C | Sparkbot integration boundary planning | defer |
| D | Robo-OS / physical-world boundary planning | defer |
| E | pause and preserve current runtime state | acceptable fallback |

## Recommended Phase 23 Direction

Phase 23 should be a test-only hardening lane for provenance and candidate invariants.

This is the safest next direction because it addresses the remaining Phase 22.2 gaps without runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot integration, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, audit persistence, or physical-world behavior.

## Phase 23 Approval Question

Do you approve Phase 23 as a test-only hardening lane for provenance and candidate invariants, limited to `tests/test_phase_23_*.py`, `tests/fixtures/runtime_extraction/phase_23_*.json`, `docs/PHASE_23_*.md`, and required roadmap/state docs only, while still forbidding runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, IntentCompiler runtime behavior, GuardianDecision runtime behavior, approval enforcement, execution, dispatch, audit persistence, shell/browser/network/file mutation, robotics, physical-world action, external service calls, background workers, queues, daemons, subprocesses, threads, database writes, and hidden side effects?
