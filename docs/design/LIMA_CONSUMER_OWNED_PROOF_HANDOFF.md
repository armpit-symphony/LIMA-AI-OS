# LIMA Consumer-Owned Proof Handoff

## Purpose

This document defines the LIMA-side handoff package for future Sparkbot-owned and Arc-owned dry-run proof branches.

The goal is to give each consumer repo team exact instructions for proving LIMA can be imported and called as a dry-run dependency without allowing this LIMA repo lane to touch either consumer repo.

This branch is design-only. It does not modify `lima/`, tests, fixtures, examples, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, browser/network/file mutation surfaces, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Current Handoff Evidence

LIMA-side evidence now includes:

- Sparkbot-owned integration boundary design
- Sparkbot-owned integration boundary audit
- Sparkbot boundary handoff fixtures
- Sparkbot boundary handoff fixtures audit
- Arc-owned integration boundary design
- Arc-owned integration boundary audit
- Arc boundary handoff fixtures
- Arc boundary handoff fixtures audit
- consumer readiness matrix
- consumer readiness matrix audit
- consumer readiness checklist fixtures
- consumer readiness checklist fixtures audit

This is enough to hand off proof instructions to repo teams. It is not enough to claim production readiness.

## Handoff Rule

Consumer proof branches must be owned by their repo teams.

LIMA may provide:

- public imports and package metadata
- normalized metadata expectations
- dry-run result expectations
- checklist fixtures
- non-execution invariants
- forbidden-surface requirements
- handoff notes

LIMA must not:

- edit public Sparkbot repository files
- edit Arc Bot repository files
- import consumer internals
- wire consumer routes
- parse raw consumer input
- call consumer tools/connectors/storage
- create or mutate consumer tasks
- send consumer messages
- schedule consumer work
- claim consumer product readiness

## Sparkbot-Owned Proof Branch

Recommended branch in the Sparkbot repo:

`sparkbot-lima-dry-run-boundary-proof`

Allowed proof scope:

- install or import LIMA as a dependency candidate
- build already-normalized metadata in Sparkbot-owned code
- call `LimaKernel.evaluate(...)` in dry-run mode
- optionally pass an explicit `SimulatedDiscoveryAdapter`
- inspect `ExecutionResult`
- archive the dry-run result and invariant checklist
- prove no production route was wired
- prove no raw chat text was sent to LIMA
- prove no Sparkbot task or message mutation occurred

Forbidden in that proof:

- production route wiring
- raw chat execution
- prompt parsing in LIMA
- model calls
- provider routing
- tool execution
- connector reads/writes
- memory writes
- task state writes
- storage/persistence
- browser/file/process/network actions
- scheduler/background work
- external sends
- approval enforcement
- real Guardian decisions
- live discovery
- device control
- Robo-OS access
- robot/drone/physical-world behavior

## Arc-Owned Proof Branch

Recommended branch in the Arc repo:

`arc-lima-dry-run-boundary-proof`

Allowed proof scope:

- install or import LIMA as a dependency candidate
- build already-normalized office-task metadata in Arc-owned code
- call `LimaKernel.evaluate(...)` in dry-run mode
- optionally pass an explicit `SimulatedDiscoveryAdapter`
- inspect `ExecutionResult`
- archive the dry-run result and invariant checklist
- prove no production route was wired
- prove no raw office-task text was sent to LIMA
- prove no customer record payload was sent to LIMA
- prove no scheduler or background worker was triggered
- prove no customer communication was sent

Forbidden in that proof:

- production route wiring
- raw office-task execution
- prompt parsing in LIMA
- customer record mutation
- model calls
- provider routing
- tool execution
- connector reads/writes
- memory writes
- task state writes
- storage/persistence
- browser/file/process/network actions
- scheduler/background work
- external sends
- approval enforcement
- real Guardian decisions
- live discovery
- device control
- Robo-OS access
- robot/drone/physical-world behavior

## Required Proof Evidence

Each consumer-owned proof branch must archive:

- branch name
- owning repository
- exact LIMA commit or package version
- LIMA package/import method
- normalized request fixture or builder
- source surface metadata
- default-deny capability profile
- dry-run `ExecutionResult` sample
- non-execution invariant checklist
- proof no raw prompt or task text was passed to LIMA
- proof no production route was wired
- proof no model/tool/connector/storage action occurred
- proof no scheduler/background worker was triggered
- proof no external send occurred
- proof no device/robot/drone/physical-world action occurred
- rollback or disable plan

## Required Result Invariants

Every proof result must preserve:

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

## Consumer Proof Pseudo-Flow

```text
Consumer repo branch starts
Consumer imports LIMA dependency candidate
Consumer builds redacted normalized metadata locally
Consumer builds default-deny capability profile
Consumer calls LimaKernel.evaluate(...)
Optional: Consumer passes explicit SimulatedDiscoveryAdapter for synthetic preview only
Consumer inspects dry-run ExecutionResult
Consumer archives result sample and invariant checklist
No production route, model call, tool call, connector access, storage write, scheduler run, send, device access, or physical-world action occurs
Consumer branch stops at proof report
```

## LIMA-Side Handoff Package

LIMA should provide the following archive-ready note to consumer repo teams:

```text
LIMA has reached local dependency-shape and dry-run proof readiness for consumer-owned proof branches only.

Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads, provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, devices, Robo-OS, or physical-world systems.

The first proof is normalized metadata in and dry-run ExecutionResult out.
The proof branch must archive the exact LIMA version or commit and non-execution evidence.
```

## Not Approved

This handoff does not approve:

- public Sparkbot repo changes from this LIMA lane
- Arc Bot repo changes from this LIMA lane
- production Sparkbot integration
- production Arc integration
- runtime `IntentEnvelope` creation
- live HumanInput bridge
- real Guardian decisions
- approval enforcement
- provider/model calls
- tool execution
- connector access
- storage/persistence
- event spine persistence
- scheduler/background execution
- live discovery
- connection attempts
- browser/network/file mutation
- device control
- Robo-OS access
- robotics
- drones
- physical-world behavior

## Remaining LIMA Work Before Production Use

Before Sparkbot or Arc can use LIMA as a production runtime layer, LIMA still needs:

- stable public API versioning policy
- stronger package/install verification beyond local Mode A if needed
- real Guardian request/decision lifecycle
- approval-required flow design
- approval enforcement implementation
- HumanInput bridge contract and implementation
- runtime `IntentEnvelope` creation contract and implementation
- provider/model boundary design and implementation
- tool execution boundary design
- connector boundary design
- scheduler/background-work boundary design
- event/spine persistence design
- storage interface implementation
- consumer-owned proof branch design and audit in each repo
- rollback and disable strategy

## Recommended Next LIMA Branch

The next LIMA-side branch after audit may be:

`audit-lima-consumer-owned-proof-handoff`

After that audit passes, the next LIMA-side implementation branch may be:

`implement-lima-consumer-proof-handoff-artifact`

That branch may only add:

- one LIMA-local handoff artifact file for Sparkbot and Arc teams
- tests validating the artifact contains required proof steps and forbidden surfaces
- implementation audit report

That branch must not:

- touch public Sparkbot
- touch Arc Bot repositories
- implement consumer integration
- modify `lima/` runtime behavior
- add model/provider calls
- add tool execution
- add connector access
- add persistence
- add shell wiring
- add scheduler/background work
- add network/browser/file mutation
- add Robo-OS or physical-world behavior

## Design Verdict

This design is ready for independent audit.

It provides proof-branch handoff instructions for consumer repo teams, but it does not authorize LIMA to touch those repos or claim production readiness.
