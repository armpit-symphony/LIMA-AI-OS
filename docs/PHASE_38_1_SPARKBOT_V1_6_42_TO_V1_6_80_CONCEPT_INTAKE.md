# Phase 38.1 Sparkbot v1.6.42-to-v1.6.80 Concept Intake

Phase 38.1 records the operating concepts Sparkbot added or clarified between the v1.6.42 baseline and v1.6.80.

This phase is docs/tests/fixtures-only. Sparkbot remains read-only reference material. LIMA does not copy Sparkbot implementation code, wire Sparkbot, change `lima/`, change `tests/support/`, approve, execute, dispatch, persist, mutate files, call external services, or connect to robotics/physical-world systems.

## Baseline

Sparkbot v1.6.42 focused on operational persistence:

- Computer Control checkbox persistence.
- Model stack and provider setting persistence across workers.
- Startup loading of saved settings from `data/.env`.

That baseline matters to LIMA because it shows early owner configuration persistence, but it does not by itself define a full operating substrate.

## v1.6.80 Direction

Sparkbot v1.6.80 is now a local-first/self-hosted assistant and governed agent OS surface. The concepts LIMA should absorb are planning concepts, not runtime permissions.

Concepts identified:

- local-first desktop/server operation
- Command Center as unified operator hub
- owner-local posture for routine local/server/browser/terminal/SSH/communication reads
- strict Security posture as owner-enabled guardrail mode
- confirmation/PIN/break-glass posture for risky writes, sends, browser writes, service control, Vault reveal/write paths, and critical admin actions
- policy simulation and explain-plan before risky automation
- persistent approval inbox and approval state
- agent identity metadata: owner, purpose, scopes, allowed tools, expiration, risk tier, kill switch
- run timeline, audit hash, redacted arguments, connector health, and eval evidence
- Guardian Spine as canonical task/event/approval ledger
- memory lifecycle metadata: source, confidence, verification state, redaction state, pending approval
- Token Guardian honest live/shadow posture and subscription provider support, including Codex subscription routing
- Round Table orchestration, meeting manager behavior, and task-linked project rooms
- MCP registry and LIMA Robo OS manifests
- LIMA Robotics OS positioning with replay/simulation default
- real hardware motion blocked by default
- emergency stop as audited safety surface
- Sparkbot as command center and LIMA as future safety/runtime substrate

## LIMA Inclusion Rule

LIMA may absorb these concepts as metadata vocabulary, preview invariants, fixtures, and roadmap language.

LIMA must not inherit Sparkbot's owner-local execution behavior at runtime in Phase 38. In current LIMA, these concepts stay preview/planning only:

- `execution_allowed=false`
- `approval_granted=false`
- `dispatch_allowed=false`
- `persistence_allowed=false`
- `side_effects_allowed=false`
- HumanInput bridge inactive
- Sparkbot wiring inactive
- live adapter inactive
- external calls inactive
- robotics/physical-world behavior inactive

## Concepts To Carry Forward

Carry these concept groups into Phase 38.2 vocabulary review:

- consumer identity
- operator posture
- action class
- risk tier
- approval posture
- dry-run posture
- run state
- agent identity
- memory trust
- connector health
- robotics posture
- audit surface

## Continue

Continue only to Phase 38.2 LIMA consumer boundary vocabulary review.
