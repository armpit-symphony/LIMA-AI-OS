# LIMA Consumer Readiness Matrix

## Purpose

This document compares the current LIMA-side readiness state for future Sparkbot and Arc Bot consumers.

The goal is to define exactly what is ready, what remains blocked, and what evidence must exist before either repo team begins a dry-run proof branch.

This branch is design-only. It does not modify `lima/`, tests, fixtures, examples, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, browser/network/file mutation surfaces, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Current LIMA Baseline

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
- Sparkbot/Arc normalized request fixtures
- shell-owned translator fixtures
- local synthetic external-consumer import proof
- Sparkbot-owned boundary design, audit, handoff fixtures, and fixture audit
- Arc-owned boundary design, audit, handoff fixtures, and fixture audit

LIMA currently does not provide:

- raw chat parsing
- raw office-task parsing
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
- scheduler/background execution
- Robo-OS access
- physical-world behavior

## Consumer Readiness Summary

| Consumer | LIMA-side boundary | Handoff fixtures | Ready for consumer-owned dry-run proof | Ready for production use |
| --- | --- | --- | --- | --- |
| Sparkbot | Ready as design/audit evidence | Ready as synthetic fixture/audit evidence | Conditionally ready after consumer-proof design is archived | No |
| Arc Bot | Ready as design/audit evidence | Ready as synthetic fixture/audit evidence | Conditionally ready after consumer-proof design is archived | No |

## Sparkbot Readiness

Sparkbot has:

- LIMA-side owned integration boundary design
- independent boundary audit
- LIMA-local handoff fixture implementation
- independent handoff fixture audit
- synthetic planning preview fixture
- synthetic simulated BLE discovery fixture
- external-send blocked fixture
- tests proving dry-run results and non-execution invariants

Sparkbot may later begin a repo-owned proof branch only if that branch is limited to:

- install/import proof
- normalized metadata construction in Sparkbot-owned code
- `LimaKernel.evaluate(...)` dry-run call
- optional explicit `SimulatedDiscoveryAdapter`
- `ExecutionResult` inspection
- evidence that no production route, model, tool, connector, storage, scheduler, external send, device, robot, drone, or physical-world action occurred

Recommended future Sparkbot branch:

`sparkbot-lima-dry-run-boundary-proof`

That branch belongs to the Sparkbot team, not this LIMA repo lane.

## Arc Readiness

Arc has:

- LIMA-side owned integration boundary design
- independent boundary audit
- LIMA-local handoff fixture implementation
- independent handoff fixture audit
- synthetic office-task preview fixture
- synthetic simulated BLE discovery fixture
- scheduler blocked fixture
- external customer communication blocked fixture
- tests proving dry-run results and non-execution invariants

Arc may later begin a repo-owned proof branch only if that branch is limited to:

- install/import proof
- normalized office-task metadata construction in Arc-owned code
- `LimaKernel.evaluate(...)` dry-run call
- optional explicit `SimulatedDiscoveryAdapter`
- `ExecutionResult` inspection
- evidence that no production route, scheduler/background worker, model, tool, connector, storage, external send, device, robot, drone, or physical-world action occurred

Recommended future Arc branch:

`arc-lima-dry-run-boundary-proof`

That branch belongs to the Arc team, not this LIMA repo lane.

## Shared Consumer Proof Preconditions

Before either consumer-owned proof branch starts, the owning repo team should archive:

- branch name
- LIMA package/import method
- exact LIMA commit or version
- normalized request fixture or local normalized request builder
- dry-run `ExecutionResult` sample
- non-execution invariant checklist
- proof no raw prompt or raw task text is sent to LIMA
- proof no production route is wired
- proof no model/tool/connector/storage action occurs
- proof no scheduler/background worker is triggered
- proof no external send occurs
- proof no device/robot/drone/physical-world action occurs
- rollback or disable plan for removing the proof

## Shared Allowed Input Shape

Consumer-owned proof branches may pass only:

- redacted shell identity
- redacted actor identity
- redacted session identity
- already-normalized intent or office-task metadata
- default-deny capability profile
- source surface metadata
- context refs, not dereferenced payloads
- synthetic/simulated discovery metadata
- redacted approval-boundary hints

## Shared Forbidden Inputs

Consumer-owned proof branches must not pass:

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
- customer record payloads
- regulated data payloads
- device serials
- physical location
- robot/drone command payloads

## Required Non-Execution Invariants

Every consumer proof result must preserve:

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

## Consumer Difference Matrix

| Area | Sparkbot proof posture | Arc proof posture |
| --- | --- | --- |
| Consumer role | Public/self-hosted workspace shell candidate | Guarded office-task consumer |
| Raw input | Must be normalized/redacted before LIMA | Must be normalized/redacted before LIMA |
| Planning preview | Proposed dry-run only | Proposed dry-run only |
| Simulated discovery | Explicit adapter, synthetic only | Explicit adapter, synthetic only |
| External send | Blocked or approval-shaped only, no execution | Blocked, no customer communication execution |
| Scheduler/background work | Forbidden | Explicitly blocked |
| Customer records | Must not send raw connector/customer records | Must not send customer record payloads |
| Browser/files/process | Forbidden | Forbidden |
| Connector access | Forbidden | Forbidden |
| Device/Robo-OS/physical world | Forbidden | Forbidden |
| Production readiness | No | No |

## Remaining LIMA Work Before Production Consumer Use

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
- consumer compatibility test matrix implementation
- consumer-owned proof branch design and audit in each owning repo
- rollback and disable strategy

## Explicitly Forbidden In This Matrix Lane

This branch does not approve:

- Sparkbot repo changes
- Arc Bot repo changes
- production shell wiring
- `lima/` runtime behavior changes
- provider/model calls
- tool execution
- connector access
- storage/persistence
- live adapters
- browser control
- network access
- file mutation
- scheduler/background work
- subprocesses
- threads
- credential storage
- external sends
- live discovery
- connection attempts
- device control
- Robo-OS access
- robot/drone/physical-world behavior

## Recommended Next LIMA Branch

The next LIMA-side branch after audit may be:

`audit-lima-consumer-readiness-matrix`

After that audit passes, the safest implementation-shaped LIMA branch is:

`implement-lima-consumer-readiness-checklist-fixtures`

That branch may only add:

- LIMA-local consumer readiness checklist fixture metadata
- tests validating Sparkbot and Arc checklist completeness
- tests proving forbidden repo/runtime surfaces remain absent from the fixtures
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

Sparkbot and Arc have enough LIMA-side evidence to plan consumer-owned dry-run proof branches, but not enough for production use. The next work should preserve the proof-only boundary and convert the readiness matrix into LIMA-local checklist fixtures before any repo team begins consumer-owned proof work.
