# LIMA Arc-Owned Integration Boundary

## Purpose

This document defines the LIMA-side boundary for a future Arc Bot / LIMA AI Office integration lane.

The goal is to make the Arc handoff precise without touching Arc Bot repositories or public Sparkbot:

- what LIMA can offer today
- what Arc may test later in its own branch
- how Arc differs from Sparkbot as a guarded office-task consumer
- what remains forbidden
- what evidence Arc must produce before any production wiring
- what LIMA must still implement before real office-runtime use

This branch is design-only. It does not modify `lima/`, tests, fixtures, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, browser/network/file mutation surfaces, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

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
- Sparkbot boundary handoff fixtures

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

## Arc Role

Arc Bot / LIMA AI Office should be treated as a guarded office-task consumer.

Arc is not:

- a Sparkbot clone
- a personal workstation shell
- a browser automation surface
- a terminal or code execution surface
- a connector executor
- an approval executor
- a dispatch system
- a scheduler runtime
- an audit persistence system
- a Robo-OS driver
- a robotics or physical-world controller

Arc's first useful relationship to LIMA is normalized, redacted office-task metadata in and dry-run `ExecutionResult` out.

## Ownership Rule

Arc integration must be Arc-owned.

LIMA may provide:

- stable public imports
- normalized request contracts
- fixture examples
- dry-run kernel results
- non-execution invariant expectations
- handoff notes
- compatibility tests inside LIMA

LIMA must not:

- edit Arc Bot repository files from this repo lane
- edit public Sparkbot repository files from this repo lane
- import Arc Bot internals
- import Sparkbot internals
- depend on Arc application modules
- wire Arc routes
- parse Arc chat or office-task text
- call Arc tools/connectors/storage
- create Arc tasks
- schedule Arc work
- send Arc messages
- mutate Arc state
- claim Arc product readiness

## Arc Default Posture

Arc defaults stricter than Sparkbot.

Arc future requests should assume:

- external writes require approval posture and must not execute in LIMA today
- connector reads and writes require Guardian classification and are unavailable today
- memory writes and task-state writes are unavailable today
- scheduled work is planned or blocked, not run in the background
- secrets and credentials remain blocked
- admin actions remain blocked
- file/browser/process actions remain blocked
- network, live discovery, and device-control actions remain blocked
- physical-world, robotics, drones, and Robo-OS actions remain blocked
- Sparkbot-only workstation affordances are not inherited by Arc

## Future Arc-Owned Branch Shape

Future Arc repo work, when separately approved by that repo team, should begin with a branch such as:

`arc-lima-dry-run-boundary-proof`

That branch should only prove:

- Arc can install or import LIMA as a dependency candidate
- Arc can construct already-normalized office-task metadata locally
- Arc can call `LimaKernel.evaluate(...)` in dry-run mode
- Arc can optionally pass explicit `SimulatedDiscoveryAdapter` for synthetic preview metadata only
- Arc can inspect `ExecutionResult`
- non-execution invariants remain safe
- no production route is wired
- no scheduler/background job is triggered
- no model/tool/connector/storage/device action occurs

This future branch belongs to the Arc team, not this LIMA branch.

## Allowed Future Arc Consumer Inputs

Arc may later send only:

- redacted shell identity
- redacted actor identity
- redacted session identity
- already-normalized office-task metadata
- task candidate metadata
- default-deny capability profile
- source surface metadata
- context refs, not dereferenced payloads
- synthetic/simulated discovery metadata
- redacted approval-boundary hints

Arc must not send:

- raw chat text
- raw office-task text
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
- customer records
- unredacted HR, finance, legal, medical, or regulated data
- device serials
- physical location
- robot/drone command payloads

## Future Arc Dry-Run Flow

```text
Arc receives office-task interaction
Arc locally classifies and redacts input
Arc builds normalized office-task metadata
Arc builds default-deny capability profile
Arc calls LimaKernel.evaluate(...)
LIMA returns proposed, approval_required, or blocked
Arc displays or records redacted dry-run result
No production route, model call, tool call, connector access, scheduler run, send, persistence, or physical action occurs
```

## Required Arc-Side Evidence

A future Arc-owned proof should produce:

- branch name
- LIMA package/import method
- exact LIMA commit or version
- normalized office-task request fixture used
- dry-run `ExecutionResult` sample
- non-execution invariant checklist
- proof no raw office-task text was sent to LIMA
- proof no customer record payload was sent to LIMA
- proof no production route was wired
- proof no scheduler/background worker was triggered
- proof no model/tool/connector/storage action occurred
- proof no external send occurred
- proof no device/robot/drone/physical-world action occurred

## LIMA-Side Acceptance Expectations

Any future Arc dry-run result must preserve:

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

## Explicitly Forbidden Arc Integration Surfaces

Until separately designed, implemented, and audited, Arc must not use LIMA for:

- raw office-task execution
- prompt parsing in LIMA
- customer record mutation
- production route handling
- background agent loops
- scheduled job execution
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
- live discovery
- network access
- device control
- Robo-OS access
- robot/drone/physical-world behavior

## Arc-Specific Risk Notes

Arc is likely closer than Sparkbot to customer office operations. That makes conservative gating more important, not less.

Arc-specific risk classes that must remain blocked or approval-required until later contracts exist:

- external customer communications
- calendar or scheduling changes
- ticket status changes
- CRM/customer record changes
- document/file mutation
- connector setup or credential use
- admin or IT remediation actions
- background recurring work
- regulated or sensitive customer data access
- device or local office network actions

This design does not approve any of those behaviors.

## Required LIMA Work Before Production Arc Use

Before Arc can use LIMA as a production runtime layer, LIMA still needs:

- audited install/package verification beyond Mode A if needed
- stable public API versioning policy
- real Guardian request/decision lifecycle
- approval-required flow design
- approval enforcement implementation
- HumanInput bridge contract and implementation
- `IntentEnvelope` runtime creation contract and implementation
- provider/model boundary design and implementation
- tool execution boundary design
- connector boundary design
- scheduler/background-work boundary design
- event/spine persistence design
- storage interface implementation
- consumer compatibility test matrix
- Arc-owned integration design and audit
- rollback and disable strategy

## Handoff Notes for Arc Team

Archive-ready message:

- LIMA has reached local dependency-shape proof, not production Arc integration readiness.
- A future Arc branch should be dry-run only.
- Arc must own local normalization/redaction before LIMA sees metadata.
- Do not send raw office-task text or customer records to LIMA.
- Do not wire production routes yet.
- Do not expect LIMA to call models, tools, connectors, storage, schedulers, or send messages.
- The first Arc proof should be normalized office-task metadata in, dry-run `ExecutionResult` out.

## Future LIMA Branch

The next LIMA-side branch after audit may be:

`implement-lima-arc-boundary-handoff-fixtures`

That branch may only add:

- Arc handoff fixture metadata inside LIMA tests
- tests validating Arc handoff checklist shape
- tests proving no Arc imports are introduced
- tests proving dry-run invariants remain expected
- implementation audit report

That branch must not:

- touch Arc Bot repositories
- touch public Sparkbot
- implement Arc integration
- modify `lima/` runtime behavior
- add model/provider calls
- add tool execution
- add connector access
- add persistence
- add shell wiring
- add scheduler/background work
- add network/browser/file mutation
- add schedulers/workers/subprocesses
- add Robo-OS or physical-world behavior

## Design Verdict

This design is ready for independent audit.

It does not approve Arc repo work, public Sparkbot repo work, production Arc integration, raw office-task parsing in LIMA, live HumanInput, runtime `IntentEnvelope` creation, real Guardian decisions, approval enforcement, provider/model calls, tool execution, persistence, connector access, live discovery, scheduler execution, Robo-OS access, or physical-world behavior.
