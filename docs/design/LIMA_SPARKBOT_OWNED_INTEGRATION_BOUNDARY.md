# LIMA Sparkbot-Owned Integration Boundary

## Purpose

This document defines the LIMA-side boundary for a future Sparkbot-owned integration lane.

The goal is to make the next handoff precise without touching the public Sparkbot repository:

- what LIMA can offer today
- what Sparkbot may test later in its own branch
- what remains forbidden
- what evidence Sparkbot must produce before any production wiring
- what LIMA must still implement before real runtime use

This branch is design-only. It does not modify `lima/`, public Sparkbot, Arc Bot repositories, tests, fixtures, package metadata, provider/model files, storage/persistence files, live adapter files, connector behavior, browser/network/file mutation surfaces, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Current LIMA Readiness Baseline

LIMA currently provides:

- importable `lima`
- importable `lima.kernel`
- `LimaKernel`
- `KernelRequest`
- `CapabilityProfile`
- `ExecutionResult`
- `SimulatedDiscoveryAdapter`
- non-executing dry-run evaluation
- explicit simulated discovery path
- package metadata for `lima-runtime`
- local minimal shell proof
- Sparkbot/Arc normalized metadata fixtures
- shell-owned translator fixtures
- local synthetic external-consumer import proof

LIMA currently does not provide:

- raw chat parsing
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real `GuardianDecision` authority
- approval enforcement
- model/provider calls
- tool execution
- connector access
- storage/persistence
- event spine persistence
- production shell wiring
- live discovery
- network/device access
- Robo-OS access
- physical-world behavior

## Ownership Rule

Sparkbot integration must be Sparkbot-owned.

LIMA may provide:

- stable public imports
- normalized request contracts
- fixture examples
- dry-run kernel results
- non-execution invariant expectations
- handoff notes
- compatibility tests inside LIMA

LIMA must not:

- edit public Sparkbot files from this repo lane
- import Sparkbot internals
- depend on Sparkbot application modules
- wire Sparkbot routes
- parse Sparkbot chat text
- call Sparkbot tools/connectors/storage
- create Sparkbot tasks
- send Sparkbot messages
- mutate Sparkbot state
- claim Sparkbot product readiness

## Future Sparkbot-Owned Branch Shape

Future Sparkbot repo work, when separately approved by that repo team, should begin with a branch such as:

`sparkbot-lima-dry-run-boundary-proof`

That branch should only prove:

- Sparkbot can install or import LIMA as a dependency candidate
- Sparkbot can construct already-normalized metadata locally
- Sparkbot can call `LimaKernel.evaluate(...)` in dry-run mode
- Sparkbot can optionally pass explicit `SimulatedDiscoveryAdapter`
- Sparkbot can inspect `ExecutionResult`
- non-execution invariants remain safe
- no production route is wired
- no model/tool/connector/storage/device action occurs

This future branch belongs to the Sparkbot team, not this LIMA branch.

## Allowed Future Sparkbot Consumer Inputs

Sparkbot may later send only:

- redacted shell identity
- redacted actor identity
- redacted session identity
- already-normalized intent metadata
- default-deny capability profile
- source surface metadata
- context refs, not dereferenced payloads
- synthetic/simulated discovery metadata

Sparkbot must not send:

- raw chat text
- raw prompt text
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- headers
- cookies
- tokens
- unsafe command bodies
- live scan dumps
- device serials
- physical location
- robot/drone command payloads

## Future Sparkbot Dry-Run Flow

```text
Sparkbot receives user interaction
Sparkbot locally classifies and redacts input
Sparkbot builds normalized metadata
Sparkbot builds default-deny capability profile
Sparkbot calls LimaKernel.evaluate(...)
LIMA returns proposed, approval_required, or blocked
Sparkbot displays or records redacted dry-run result
No production route, model call, tool call, connector access, send, persistence, or physical action occurs
```

## Required Sparkbot-Side Evidence

A future Sparkbot-owned proof should produce:

- branch name
- LIMA package/import method
- exact LIMA commit or version
- normalized request fixture used
- dry-run `ExecutionResult` sample
- non-execution invariant checklist
- proof no raw chat was sent to LIMA
- proof no production route was wired
- proof no model/tool/connector/storage action occurred
- proof no background worker or scheduler was triggered
- proof no external send occurred
- proof no device/robot/drone/physical-world action occurred

## LIMA-Side Acceptance Expectations

Any future Sparkbot dry-run result must preserve:

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

## Explicitly Forbidden Sparkbot Integration Surfaces

Until separately designed, implemented, and audited, Sparkbot must not use LIMA for:

- raw chat execution
- prompt parsing in LIMA
- production route handling
- background agent loops
- model calls
- provider routing
- tool execution
- connector reads/writes
- memory writes
- task state writes
- file writes
- browser control
- process execution
- external sends
- approval enforcement
- real Guardian decisions
- persistence
- scheduler execution
- live discovery
- network access
- device control
- Robo-OS access
- robot/drone/physical-world behavior

## Required LIMA Work Before Production Sparkbot Use

Before Sparkbot can use LIMA as a production runtime layer, LIMA still needs:

- audited install/package verification beyond Mode A if needed
- stable public API versioning policy
- real Guardian request/decision lifecycle
- approval-required flow design
- approval enforcement implementation
- HumanInput bridge contract and implementation
- IntentEnvelope runtime creation contract and implementation
- provider/model boundary design and implementation
- tool execution boundary design
- connector boundary design
- event/spine persistence design
- storage interface implementation
- consumer compatibility test matrix
- Sparkbot-owned integration design and audit
- rollback and disable strategy

## Handoff Notes for Sparkbot Team

Archive-ready message:

- LIMA has reached local dependency-shape proof, not production integration readiness.
- A future Sparkbot branch should be dry-run only.
- Sparkbot must own local normalization/redaction before LIMA sees metadata.
- Do not send raw chat text to LIMA.
- Do not wire production routes yet.
- Do not expect LIMA to call models, tools, connectors, storage, or send messages.
- The first Sparkbot proof should be normalized metadata in, dry-run `ExecutionResult` out.

## Future LIMA Branch

The next LIMA-side branch after audit may be:

`implement-lima-sparkbot-boundary-handoff-fixtures`

That branch may only add:

- Sparkbot handoff fixture metadata inside LIMA tests
- tests validating handoff checklist shape
- tests proving no Sparkbot imports are introduced
- tests proving dry-run invariants remain expected
- implementation audit report

That branch must not:

- touch public Sparkbot
- implement Sparkbot integration
- modify `lima/` runtime behavior
- add model/provider calls
- add tool execution
- add connector access
- add persistence
- add shell wiring
- add network/browser/file mutation
- add schedulers/workers/subprocesses
- add Robo-OS or physical-world behavior

## Design Verdict

This design is ready for independent audit.

It does not approve public Sparkbot repo work, production Sparkbot integration, raw chat parsing in LIMA, live HumanInput, runtime `IntentEnvelope` creation, real Guardian decisions, approval enforcement, provider/model calls, tool execution, persistence, connector access, live discovery, Robo-OS access, or physical-world behavior.
