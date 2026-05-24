# Phase 43.0 Universal Contract Fixture Hardening Charter

Phase 43.0 opens the Universal Contract Fixture Hardening lane recommended by Phase 42.4.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, `tests/support/`, Sparkbot, runtime behavior, helper behavior, Sparkbot wiring, Arc Bot implementation, HumanInput bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, shell/browser/network/file mutation, robotics, physical-world action, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Purpose

Phase 42 defined universal LIMA AI OS contract vocabulary for model-, consumer-, and embodiment-agnostic planning. Phase 43 hardens that vocabulary with inert fixtures and tests so future consumers cannot imply authority from profile metadata.

Phase 43.0 is the charter only. It authorizes only docs/tests/fixtures planning and prepares the fixture categories for later Phase 43 slices.

## Fixture Categories To Harden

Phase 43 should cover representative safe, risky, embodied, and adversarial profiles:

- Arc Bot office task profile
- Sparkbot reference profile
- generic automation agent profile
- coding agent profile
- research agent profile
- browser action profile
- shell action profile
- file mutation profile
- network/API action profile
- scheduled/background work profile
- IoT device action profile
- drone action profile
- humanoid action profile
- robot motion profile
- emergency stop profile
- malicious consumer profile trying to grant approval
- malicious embodiment profile trying to allow execution
- malformed profile data
- unknown model/provider data
- nested bypass wording

## Required Fixture Invariants

Every Phase 43 fixture must remain:

- preview-only
- non-authoritative
- safe by default
- local-only
- deterministic
- non-executing
- side-effect free
- approval-free
- dispatch-free
- persistence-free
- adapter-inactive
- Sparkbot-wiring inactive
- Arc Bot implementation inactive
- robotics inactive
- physical-world inactive

Profile metadata may describe approval posture, risk, evidence requirements, simulation posture, or adapter requirements. It must not grant approval, execute, dispatch, persist, mutate, call adapters, start background work, or touch physical-world systems.

## Allowed Phase 43.0 Work

- Phase 43.0 charter documentation
- Phase 43.0 inert fixture metadata
- Phase 43.0 tests proving the charter boundary
- README, roadmap, decision, extraction-plan, and current-state updates

## Blocked Work

- runtime implementation
- `lima/` changes
- `tests/support/` changes
- Sparkbot wiring
- Arc Bot implementation
- live adapters
- real approval enforcement
- execution, dispatch, persistence, mutation, or external calls
- shell/browser/network/file mutation
- robotics, hardware control, or physical-world behavior
- background workers, queues, daemons, subprocesses, threads, database writes, or hidden side effects
- live/customer connectors or production deployment claims

## Phase 43.1 Recommendation

If continuing under docs/tests/fixtures-only autopilot, Phase 43.1 should add the inert universal contract profile fixture corpus. It should not modify runtime behavior or create any live adapter, approval, dispatch, persistence, robotics, or physical-world path.
