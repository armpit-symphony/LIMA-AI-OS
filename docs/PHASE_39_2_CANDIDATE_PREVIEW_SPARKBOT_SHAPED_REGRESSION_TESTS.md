# Phase 39.2 Candidate Preview Sparkbot-Shaped Regression Tests

Phase 39.2 adds regression tests proving the existing `candidate_preview` helper remains safe for Sparkbot-shaped caller-provided inputs.

This phase is test/docs/fixtures only. It does not modify `lima/`, Sparkbot, `tests/support/`, helper behavior, runtime behavior, approval enforcement, execution, dispatch, persistence, audit persistence, shell/browser/network/file mutation, MCP connections, robotics, physical-world behavior, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Coverage

The tests cover:

- owner-local routine read request
- strict-security risky write request
- breakglass-required Vault request
- MCP explain-plan request
- Robo OS simulation request
- real-hardware robot-motion request
- agent identity with `kill_switch=true`
- low-confidence memory write requiring pending approval

## Result

Every Sparkbot-shaped fixture remains blocked and inert under the existing `candidate_preview` API.

The tests prove:

- deterministic output for repeated preview calls
- preview state remains blocked for each Sparkbot-shaped case
- expected blocked claims are present
- execution remains disallowed
- side effects remain disallowed
- approval remains not granted
- dispatch remains disallowed
- persistence remains disallowed
- Phase 5 HumanInput runtime bridge remains gated
- Sparkbot wiring remains inactive
- live adapters remain inactive
- external calls remain disallowed
- robotics and physical-world behavior remain disallowed

## Continue

Continue only to Phase 39.3 hardening gap and next-lane decision review.
