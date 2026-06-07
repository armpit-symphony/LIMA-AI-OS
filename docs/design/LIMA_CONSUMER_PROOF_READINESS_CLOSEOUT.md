# LIMA Consumer Proof Readiness Closeout

## Closeout Status

This document closes the current LIMA-local consumer proof preparation lane.

It is docs-only. It does not audit real consumer proof packets, modify Sparkbot repositories, modify Arc Bot repositories, modify public release repositories, modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, create runtime behavior, wire shells, automate proof intake, call models, execute tools, access connectors, persist events, run schedulers, use browser/file/process/network APIs, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve production integration.

## Purpose

This closeout records what LIMA has prepared for future Sparkbot and Arc Bot consumer-owned dry-run proof work, what is ready to hand off, what remains blocked, and what the next branch must be when consumer proof packets arrive.

It exists to prevent three unsafe outcomes:

- claiming Sparkbot or Arc Bot readiness without proof packets
- starting a dry-run compatibility freeze before both proof packets pass audit
- drifting from LIMA-local proof preparation into consumer repo wiring or runtime behavior

## Current Readiness Verdict

`ready_for_consumer_owned_dry_run_proof_handoff_only`

LIMA is ready to give Sparkbot and Arc Bot repo teams the dry-run proof instructions and audit templates.

LIMA is not ready for:

- dry-run consumer compatibility freeze
- production Sparkbot integration
- Arc Bot integration
- consumer repo modifications
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real Guardian decision authority
- approval enforcement
- provider/model calls
- tool execution
- connector access
- storage/persistence
- scheduler/background work
- live discovery
- connection attempts
- pairing
- credential use
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Completed LIMA-Local Proof Preparation Artifacts

The current lane has prepared these LIMA-local artifacts:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITES.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `tests/fixtures/dry_run_consumer_compatibility_freeze_input_matrix/freeze_input_matrix.json`
- `tests/test_lima_dry_run_consumer_compatibility_freeze_input_matrix.py`

These artifacts are enough to tell consumer teams what proof packets must contain and how LIMA will review them.

They are not proof packets.

They do not prove consumer compatibility.

They do not freeze the API.

## What LIMA Can Hand Off Now

LIMA can hand off:

- current proof-stage public API manifest
- Sparkbot-owned proof branch name: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot-owned proof branch name: `arc-lima-dry-run-boundary-proof`
- consumer proof archive template
- consumer proof intake response template
- consumer proof results audit template
- consumer proof handoff artifact
- consumer proof delivery note
- dry-run compatibility freeze prerequisites
- freeze input matrix
- static matrix tests proving the current stop condition

The handoff message must say:

```text
LIMA is ready for consumer-owned dry-run proof only.
Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads, provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, devices, Robo-OS, or physical-world systems.
The first proof is normalized metadata in and dry-run ExecutionResult out.
```

## Required Consumer-Owned Proof Branches

Sparkbot team:

`sparkbot-lima-dry-run-boundary-proof`

Arc Bot team:

`arc-lima-dry-run-boundary-proof`

These branches must be created and owned in the consumer repositories by those repo teams.

The LIMA repo must not create, edit, push, fetch, clone, scan, or inspect those branches unless the user supplies approved proof artifacts or explicitly instructs a read-only reference review.

## Required Proof Packet Evidence

Each consumer proof packet must include:

- consumer repo
- consumer branch
- consumer team owner
- exact LIMA repository URL
- exact LIMA commit or package version
- package name
- package version
- import method
- public imports used
- proof archive location
- redacted already-normalized metadata
- default-deny capability profile
- explicit `LimaKernel.evaluate(...)` call
- dry-run `ExecutionResult` evidence
- optional explicit simulated discovery evidence if used
- non-execution invariant evidence
- forbidden surface attestation
- redaction attestation
- rollback or disable plan
- final proof verdict

## Required Sparkbot-Specific Evidence

Sparkbot proof packet must show:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Required Arc Bot-Specific Evidence

Arc Bot proof packet must show:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Proof-Public Imports

Consumer dry-run proof branches may use only:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Consumer proof branches must not rely on:

- top-level runtime re-exports such as `from lima import LimaKernel`
- `dry_run_candidate` imports without review
- internal namespaces such as `lima.io.*`, `lima.persistence.*`, `lima.harness.*`, `lima.guardian.*`, `lima.spine.*`, `lima.services.*`, `lima.shells.*`, or `lima.adapters.*`

## Required Non-Execution Invariants

Every accepted proof packet must preserve:

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

## Redaction Boundary

LIMA must not accept or archive proof evidence containing:

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

Any packet containing those materials must be classified as `needs_redaction`.

## Freeze Stop Condition

The compatibility freeze remains blocked while any of these are missing:

- Sparkbot proof packet from `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot proof packet from `arc-lima-dry-run-boundary-proof`
- LIMA-side Sparkbot proof results audit
- LIMA-side Arc Bot proof results audit
- both audits passing as `pass_for_dry_run_dependency_proof`
- no redaction blockers
- no missing evidence blockers
- no forbidden import blockers
- no runtime boundary blockers
- no production/live-claim blockers

Current status:

`not_ready_for_freeze`

## Forbidden Next Actions

Do not proceed to:

- compatibility freeze
- production integration
- Sparkbot route wiring
- Arc Bot route wiring
- consumer repository edits from this LIMA lane
- automated proof intake
- proof archive crawling
- public repository scanning
- runtime behavior expansion
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real Guardian decision authority
- approval enforcement
- provider/model routing
- model calls
- tool execution
- connector access
- storage/persistence
- event-spine persistence
- scheduler/background workers
- browser/file/process/network actions
- live discovery
- connection attempts
- pairing
- credential use or storage
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Allowed Next Actions

Allowed next actions:

- deliver the handoff note to consumer repo teams through the user
- wait for consumer-owned proof packets
- audit supplied consumer proof packets using `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- answer consumer-team questions using the intake response template
- create LIMA-local docs-only clarifications if a proof blocker reveals ambiguity

## Recommended Next Branch

If consumer proof packets are available:

`audit-consumer-owned-proof-results`

If consumer teams request clarification before proof packets:

`revise-consumer-proof-handoff-clarifications`

If LIMA must continue locally without packets:

`audit-lima-consumer-proof-readiness-closeout`
