# Phase 39.1 Sparkbot-Shaped Candidate Preview Fixtures

Phase 39.1 adds deterministic offline fixtures that represent Sparkbot-shaped caller-provided candidate preview inputs.

This phase is fixtures/docs/tests only. The fixtures are inert JSON data. They do not call Sparkbot, import Sparkbot, execute tools, approve actions, dispatch runs, persist audit, connect to MCP, mutate files, call external services, or touch robotics/physical-world systems.

## Fixture Cases

The fixture file includes:

- owner-local routine read request
- strict-security risky write request
- breakglass-required Vault request
- MCP explain-plan request
- Robo OS simulation request
- real-hardware robot-motion request
- agent identity with `kill_switch=true`
- low-confidence memory write requiring pending approval

## Expected Preview Outcome

Every fixture must remain safe under existing `candidate_preview` behavior:

- preview is non-authoritative
- execution remains disallowed
- side effects remain disallowed
- approval remains not granted
- dispatch remains disallowed
- persistence remains disallowed
- HumanInput bridge remains gated/inactive
- Sparkbot wiring remains inactive
- live adapter remains inactive
- external calls remain disallowed
- robotics and physical-world behavior remain disallowed

## Continue

Continue only to Phase 39.2 runtime candidate preview Sparkbot-shaped regression tests.
