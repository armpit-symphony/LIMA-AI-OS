# Pipeline Composition Safety Gate

This is the standing non-runtime safety gate for any future LIMA Kernel pipeline composition work.

It does not define an executable pipeline. It is not a harness. It does not authorize a test-only harness. It does not approve runtime integration. It exists to prevent Phase 3 fixture maps, relationship metadata, report artifacts, and doctrine references from being mistaken for working runtime behavior.

## Scope

This gate applies before any future work that attempts to compose these non-production fixture families:

- Sparkbot-shaped payload or HumanInput-adjacent fixtures.
- IntentEnvelope fixtures.
- Guardian request fixtures.
- Fake GuardianDecision fixtures.
- Report/map artifact fixtures.

## Required Preconditions

Before any future test-only composition harness can be proposed, a readiness review must confirm:

- Phase 3.6 is merged and tagged.
- Source fixtures remain synthetic and LIMA-owned.
- Every referenced relationship remains `non_runtime: true`.
- Stage maps remain descriptive and do not define execution order.
- Relationship maps remain descriptive and do not prove compatibility.
- Readiness findings remain non-authoritative and non-executing.
- Doctrine references remain context only.
- No source fixture contains secrets, credentials, tokens, hostnames, live URLs, model prompts, tool calls, shell commands, deployment commands, or private operational data.
- Unsupported categories are explicit and cannot silently pass.
- Critical, unknown, destructive, secret, payment, deployment, admin, robot, drone, IoT, and physical-world scenarios cannot auto-approve.
- A separate design review approves any proposed test-only harness before it exists.

## Required Blockers

This gate blocks:

- executable pipeline
- runtime composition
- production Sparkbot integration
- Sparkbot imports or wiring
- real IntentCompiler
- real GuardianDecision
- model calls
- tool execution
- terminal or PTY execution
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

## Future Harness Conditions

A future test-only harness remains blocked unless a later readiness review explicitly approves it.

If approved later, that harness must:

- live under `tests/` only
- use synthetic LIMA-owned fixtures only
- avoid importing Sparkbot
- avoid importing production routes
- avoid model calls
- avoid tool execution
- avoid filesystem, browser, network, terminal, robot, drone, IoT, or physical-world actions
- report unsupported categories explicitly
- fail closed on critical and unknown risk
- never create real approvals or Guardian decisions
- never persist audit events
- never become a production adapter

## Phase 3.7 Decision

Phase 3.7 is documentation, fixtures, and tests only.

It is ready for a Phase 3.8 Pipeline Composition Safety Gate Readiness Review.

It is not ready for a test-only composition harness, executable pipeline, runtime composition, production integration, shell implementation, robot control, approval, execution, enforcement, or audit persistence.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
