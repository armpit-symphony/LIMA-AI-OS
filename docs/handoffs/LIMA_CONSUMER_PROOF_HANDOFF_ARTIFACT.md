# LIMA Consumer Proof Handoff Artifact

## Purpose

This is the LIMA-local, archive-ready handoff note for Sparkbot and Arc Bot repo teams.

It gives each team a bounded dry-run proof plan for importing LIMA and calling the current non-executing kernel surface from their own repository. It does not authorize this LIMA lane to touch public Sparkbot, Arc Bot, production routes, live connectors, tools, models, storage, devices, Robo-OS, robotics, drones, or physical-world systems.

## Current Status

LIMA is ready for consumer-owned dry-run proof planning only.

LIMA is not production-ready for Sparkbot or Arc Bot. The first proof is normalized metadata in and dry-run `ExecutionResult` out.

## Owning Branches

Sparkbot team branch:

`sparkbot-lima-dry-run-boundary-proof`

Arc Bot team branch:

`arc-lima-dry-run-boundary-proof`

Each branch must be created and owned in its consumer repository by that repo team. This LIMA branch must not modify either repository.

## Shared Proof Steps

Each consumer repo team should:

1. Create the consumer-owned proof branch.
2. Record the exact LIMA commit, package version, or import method.
3. Build redacted already-normalized intent or task metadata locally.
4. Build a default-deny `CapabilityProfile`.
5. Call `LimaKernel.evaluate(...)` in dry-run mode.
6. Optionally pass an explicit `SimulatedDiscoveryAdapter` only for synthetic preview metadata.
7. Archive the dry-run `ExecutionResult` sample.
8. Archive the non-execution invariant checklist.
9. Archive evidence that no production route was wired.
10. Archive evidence that no model, tool, connector, storage, scheduler, external send, device, robot, drone, or physical-world action occurred.
11. Archive a rollback or disable plan.
12. Stop at the proof report.

## Sparkbot Evidence Requirements

The Sparkbot-owned proof branch must archive:

- proof no raw chat text was sent to LIMA
- proof no public Sparkbot production route was wired
- proof no Sparkbot task was created or mutated
- proof no Sparkbot message was sent or mutated
- proof no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA
- proof any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Arc Bot Evidence Requirements

The Arc-owned proof branch must archive:

- proof no raw office-task text was sent to LIMA
- proof no customer record payload was sent to LIMA
- proof no customer communication was sent
- proof no Arc production route was wired
- proof no Arc task, project, note, form, record, or customer file was created or mutated
- proof no Arc scheduler or background worker was triggered
- proof no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA
- proof any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Allowed Inputs

Consumer proof calls may pass only:

- redacted shell identity
- redacted actor identity
- redacted session identity
- already-normalized intent metadata
- already-normalized office-task metadata
- default-deny capability profile
- source surface metadata
- context references only
- synthetic or simulated discovery metadata
- redacted approval-boundary hints

## Forbidden Inputs

Consumer proof calls must not pass:

- raw prompts
- raw chat text
- raw office-task text
- raw customer records
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- headers
- cookies
- tokens
- passwords
- pairing codes
- unsafe command bodies
- live scan dumps
- private SSIDs
- raw Bluetooth MAC addresses
- raw IP or MAC addresses
- device serial numbers
- precise physical location
- robot or drone command payloads

## Required Result Invariants

Every archived proof result must preserve:

- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `dry_run is True`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `live_discovery_executed is False`
- `connection_attempted is False`
- `pairing_attempted is False`
- `credentials_used is False`
- `session_opened is False`
- `device_control_executed is False`
- `physical_world_allowed is False`
- `physical_world_executed is False`
- `guardian_decision_created is False`
- `approval_enforced is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `robo_os_wiring_active is False`
- `adapter_active is False`
- `tool_execution_allowed is False`
- `driver_execution_allowed is False`
- `scheduler_active is False`
- `external_calls_allowed is False`

## Forbidden Surfaces

The proof branches must not implement or trigger:

- production Sparkbot integration
- production Arc Bot integration
- public Sparkbot repo changes from this LIMA lane
- Arc Bot repo changes from this LIMA lane
- Sparkbot route wiring
- Arc route wiring
- raw natural-language parsing in LIMA
- runtime `IntentEnvelope` creation
- live HumanInput bridge
- real Guardian decisions
- approval enforcement
- provider routing
- model calls
- tool execution
- connector reads or writes
- memory writes
- task state writes
- storage or persistence
- event spine persistence
- scheduler or background workers
- queues, daemons, subprocesses, or threads
- external sends
- browser actions
- file mutation
- process execution
- network actions
- live discovery
- scanning
- WiFi connection attempts
- Bluetooth or BLE connection attempts
- USB or serial connection attempts
- MQTT, Matter, or mDNS calls
- pairing
- credential use or storage
- device control
- Robo-OS access
- robotics
- drones
- physical-world behavior

## Consumer Proof Pseudo-Flow

```text
Consumer repo branch starts.
Consumer imports the LIMA dependency candidate.
Consumer builds redacted normalized metadata locally.
Consumer builds default-deny capability profile.
Consumer calls LimaKernel.evaluate(...).
Optional: consumer passes explicit SimulatedDiscoveryAdapter for synthetic preview only.
Consumer inspects dry-run ExecutionResult.
Consumer archives result sample and invariant checklist.
Consumer archives proof no forbidden surface was reached.
Consumer branch stops at proof report.
```

## Handoff Note

```text
LIMA has reached local dependency-shape and dry-run proof readiness for consumer-owned proof branches only.

Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads, provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, devices, Robo-OS, or physical-world systems.

The first proof is normalized metadata in and dry-run ExecutionResult out.
The proof branch must archive the exact LIMA version or commit and non-execution evidence.
```

## Remaining Blockers Before Product Use

Sparkbot and Arc Bot cannot use LIMA as a production runtime until later approved branches complete:

- stable public API versioning policy
- stronger install/package verification if Mode A local import is not enough
- real Guardian request and decision lifecycle
- approval-required flow design
- approval enforcement implementation
- HumanInput bridge contract and implementation
- runtime `IntentEnvelope` creation contract and implementation
- provider/model boundary design and implementation
- tool execution boundary design and implementation
- connector boundary design and implementation
- scheduler/background-work boundary design and implementation
- event/spine persistence design
- storage interface implementation
- consumer-owned proof branch design and audit in each repo
- rollback and disable strategy

## Recommended Next LIMA Branch

`audit-lima-consumer-proof-handoff-artifact`

That branch should independently audit this handoff artifact before either consumer team treats it as an archive-ready repo-team note.
