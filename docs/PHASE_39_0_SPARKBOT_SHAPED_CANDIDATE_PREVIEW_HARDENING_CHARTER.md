# Phase 39.0 Sparkbot-Shaped Candidate Preview Hardening Charter

Phase 39.0 opens a test-only hardening lane for the existing `candidate_preview` runtime slice using Sparkbot-shaped caller-provided fixtures.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, Sparkbot, `tests/support/`, stale prior-phase tests, runtime behavior, helper behavior, approval enforcement, execution, dispatch, persistence, audit persistence, shell/browser/network/file mutation, MCP connections, robotics, physical-world behavior, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Starting Audit

Phase 38 audit result: PASS.

Phase 38 concluded:

- Sparkbot v1.6.80 alignment intake completed as docs/tests/fixtures-only.
- LIMA runtime files changed: no.
- Sparkbot files changed: no.
- `tests/support/` changed: no.
- Runtime behavior changed: no.
- Phase 5 HumanInput runtime bridge remains gated.
- Sparkbot wiring/imports remain absent.
- Execution, approval enforcement, dispatch, persistence, external calls, and robotics/physical-world behavior remain absent.

## Phase 39 Purpose

Phase 39 should prove the existing `candidate_preview` helper remains safe when it receives caller-provided data shaped like current Sparkbot operating concepts.

Required fixture cases:

- owner-local routine read request
- strict-security risky write request
- breakglass-required Vault request
- MCP explain-plan request
- Robo OS simulation request
- real-hardware robot-motion request
- agent identity with `kill_switch=true`
- low-confidence memory write requiring pending approval

## Required Outcome

For every Sparkbot-shaped fixture, the existing preview must remain:

- non-authoritative
- read-only
- local-only
- deterministic
- safe by default
- non-executing
- side-effect free
- approval-free
- dispatch-free
- persistence-free
- bridge-inactive
- Sparkbot-wiring-inactive
- live-adapter-inactive
- external-call-inactive
- robotics/physical-world-inactive

## Continue

Continue only to Phase 39.1 Sparkbot-shaped candidate preview fixtures.
