# LIMA Dry-Run Consumer Compatibility Freeze Prerequisites

## Design Status

This document defines prerequisites for a future dry-run consumer compatibility freeze for Sparkbot and Arc Bot proof usage.

It is design-only. It does not freeze the API, audit real consumer proof packets, modify Sparkbot repositories, modify Arc Bot repositories, modify `lima/`, modify package metadata, change exports, create runtime behavior, wire shells, call models, execute tools, access connectors, persist events, run schedulers, perform browser/file/process/network actions, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

This document does not approve production integration.

## Purpose

The future freeze is intended to create a narrow, reviewable LIMA dependency posture that Sparkbot and Arc Bot can use for dry-run proof branches only.

The freeze must answer:

- which public imports are stable enough for dry-run proof use
- which result fields and invariants must not change without review
- which proof branches and archives demonstrate consumer compatibility
- which claims remain forbidden after the freeze
- which future changes require a new compatibility review

The freeze must not claim that LIMA is production-ready, live-integrated, model-call-ready, tool-execution-ready, connector-ready, Robo-OS-ready, or physical-world-ready.

## Freeze Is Not Production Readiness

A dry-run consumer compatibility freeze means only:

- Sparkbot and Arc Bot consumer-owned proof packets both passed LIMA-side audit
- the proof packets used exact LIMA commit/package/version references
- the proof packets used only approved proof-stage public imports
- the proof packets passed already-normalized redacted metadata only
- the proof packets called non-executing dry-run LIMA surfaces only
- every result preserved non-execution invariants
- no forbidden consumer, runtime, live, adapter, model, connector, or physical-world surfaces were used

It does not mean:

- production Sparkbot integration is approved
- Arc Bot integration is approved
- live HumanInput bridge behavior is approved
- raw natural-language parsing is approved
- runtime `IntentEnvelope` creation is approved
- real `GuardianDecision` authority is approved
- approval enforcement is approved
- provider/model routing is approved
- tool execution is approved
- connector access is approved
- storage or event-spine persistence is approved
- live discovery, connection, pairing, or credential use is approved
- Robo-OS, device, robot, drone, or physical-world behavior is approved

## Required Inputs Before Freeze Design Can Proceed

A later `design-lima-dry-run-consumer-compatibility-freeze` branch may start only after these inputs exist:

- Sparkbot proof packet from `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot proof packet from `arc-lima-dry-run-boundary-proof`
- LIMA-side audit report for the Sparkbot proof packet
- LIMA-side audit report for the Arc Bot proof packet
- both audits use `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- both audits return `pass_for_dry_run_dependency_proof`
- neither audit reports missing evidence
- neither audit reports redaction failures
- neither audit reports forbidden imports
- neither audit reports runtime boundary violations
- neither audit reports production or live integration claims

If either consumer proof packet is missing, the freeze must not proceed.

## Authoritative Reference Artifacts

Future freeze work must reference:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- Sparkbot consumer proof packet
- Arc Bot consumer proof packet
- Sparkbot LIMA-side proof results audit
- Arc Bot LIMA-side proof results audit

## Candidate Freeze Surface

The freeze candidate may include only the proof-stage public imports currently listed as `proof_public`:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

The freeze candidate must not promote `dry_run_candidate` imports without a separate design and audit.

The freeze candidate must not approve top-level runtime re-exports such as `from lima import LimaKernel`.

## Frozen Behavior Candidate

A future dry-run compatibility freeze may cover only:

- importability of `lima`
- importability of approved `lima.kernel` proof-public symbols
- construction of approved dry-run request/metadata objects
- `LimaKernel.evaluate(...)` with already-normalized metadata
- dry-run result status values: `proposed`, `approval_required`, `blocked`
- redacted in-memory event-style result metadata
- explicit `SimulatedDiscoveryAdapter` use for synthetic, inert, simulated-only previews
- non-execution invariant fields

The freeze must not cover or imply:

- raw prompt parsing
- live HumanInput ingestion
- runtime `IntentEnvelope` creation
- real Guardian decision authority
- approval enforcement
- model calls
- tool execution
- connector access
- storage/persistence
- scheduler/background work
- browser/file/process/network actions
- live discovery/scanning
- connection attempts
- pairing
- credential use or storage
- device control
- Robo-OS access
- robotics
- drones
- physical-world behavior

## Required Non-Execution Invariants

The freeze must preserve these required values for proof-stage consumer use:

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

Any future compatibility freeze must treat missing or contradictory invariant evidence as a blocker.

## Consumer Proof Packet Requirements

Each consumer proof packet must show:

- exact LIMA commit or package version
- package name and package version used
- import method used
- public imports used
- redacted already-normalized metadata
- default-deny capability profile
- explicit dry-run kernel call
- dry-run result evidence
- optional simulated discovery evidence if used
- non-execution invariant evidence
- redaction attestation
- forbidden surface attestation
- rollback or disable plan
- final proof verdict

Sparkbot evidence must also show:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task or message was created or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

Arc Bot evidence must also show:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

## Redaction Requirements

The future freeze must not archive, bless, or depend on proof evidence containing:

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

If any proof packet includes these materials, the compatibility freeze must stop until the consumer team resubmits redacted evidence.

## Version And Change-Control Requirements

A future freeze must record:

- frozen LIMA commit
- frozen branch or tag, if any
- package name
- package version
- Python requirement
- approved proof-public imports
- allowed dry-run result states
- required invariant fields
- consumer proof packet locations
- consumer audit report locations
- freeze owner
- rollback or unfreeze criteria

The future freeze must require a new compatibility review before:

- removing an approved proof-public import
- renaming an approved proof-public symbol
- changing a required result field name
- changing a required invariant default
- changing dry-run result status values
- promoting a `dry_run_candidate` import to proof-public
- adding top-level runtime re-exports
- adding adapter registry behavior
- adding hidden dispatch
- adding any live behavior or external side effect

## Rollback And Unfreeze Criteria

The future freeze must be revoked or reopened if:

- a consumer proof packet is later found to include unredacted sensitive data
- a consumer proof packet used forbidden imports
- a proof result claimed execution or side effects
- a consumer branch wired production routes
- a LIMA runtime change breaks approved proof-public imports
- a LIMA runtime change weakens non-execution invariants
- a LIMA change introduces hidden dispatch, adapter auto-loading, live discovery, model calls, tool execution, connector access, persistence, or physical-world behavior into the proof path

## Allowed Future Freeze Branch Scope

A later `design-lima-dry-run-consumer-compatibility-freeze` branch may add only:

- a freeze design doc
- a freeze readiness review or audit doc
- optional static fixture metadata if needed to represent freeze inputs
- optional static tests that verify the freeze doc references required artifacts and forbids production claims

It must not modify:

- `lima/`
- `pyproject.toml`
- package metadata
- Sparkbot repositories
- Arc Bot repositories
- runtime implementation
- adapters
- provider/model code
- storage/persistence code
- shell wiring
- Robo-OS wiring

## Forbidden Surfaces

This prerequisite document does not authorize:

- production Sparkbot integration
- production Arc Bot integration
- consumer repo edits from this LIMA lane
- public release repo edits
- raw natural-language ingestion
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real Guardian decision authority
- approval enforcement
- provider/model routing
- model calls
- tool execution
- connector reads or writes
- memory writes
- task state writes
- storage or persistence
- event spine persistence
- scheduler/background workers
- queues, daemons, subprocesses, or threads
- external sends
- browser actions
- file mutation
- process execution
- network actions
- sockets
- live discovery
- scanning
- connection attempts
- pairing
- credential use or storage
- OS network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT, Matter, or mDNS APIs
- IoT adapters
- Robo-OS adapters
- Sparkbot wiring
- Arc Bot wiring
- device control
- robotics
- drones
- physical-world behavior

## Readiness Decision Rule

The future freeze can be designed only after both consumer-owned dry-run proof packets pass LIMA-side audits.

Until then, the correct status is:

`not_ready_for_freeze`

## Recommended Next Branch

If both proof packets have passed:

`design-lima-dry-run-consumer-compatibility-freeze`

If proof packets have not been supplied:

`audit-consumer-owned-proof-results`

If LIMA must continue locally before proof packets arrive:

`design-lima-dry-run-consumer-compatibility-freeze-input-matrix`
