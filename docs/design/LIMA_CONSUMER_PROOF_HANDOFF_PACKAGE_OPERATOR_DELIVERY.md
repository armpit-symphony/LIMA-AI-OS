# LIMA Consumer Proof Handoff Package Operator Delivery

## Branch

`design-lima-consumer-proof-handoff-package-operator-delivery`

## Base Commit

`15a2b186c1950ddb1a4d66723f5132becd4ca63f`

## Design Status

This document designs how the operator may deliver the existing LIMA-local consumer proof handoff package to the
Sparkbot and Arc Bot repo teams.

It is design-only. It does not send messages, create proof packets, receive proof packets, archive proof packets,
audit proof packets, update ledgers, persist state, start compatibility freeze, inspect consumer repositories, create
consumer branches, modify consumer repositories, modify `lima/`, modify `tests/support/`, change package metadata,
change public exports, wire shells, call models, execute tools, access connectors, use storage, run schedulers, perform
browser/file/process/network actions, perform live discovery, connect, pair, use credentials, invoke Robo-OS, control
devices, control robots, control drones, or touch physical-world systems.

This design does not approve Sparkbot dependency use, Arc Bot dependency use, product readiness, production readiness,
or public Sparkbot release readiness.

## Purpose

The operator-delivery lane answers one narrow question:

Can the LIMA-local proof package be converted into a controlled operator handoff request that the user can manually
deliver to the Sparkbot and Arc Bot teams?

The only allowed verdict is:

`ready_for_manual_operator_delivery_request_only`

That means:

- the LIMA repo may tell the operator what to deliver
- delivery is manual and outside this branch
- Sparkbot and Arc proof branches remain consumer-owned
- Sparkbot and Arc proof packets remain missing until returned by their repo teams
- LIMA does not receive, archive, audit, or accept proof in this branch
- compatibility freeze remains blocked
- product readiness remains `not_production_ready`

## Source Artifacts

The operator delivery request is derived from:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_STATIC_TESTS.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_STATIC_TESTS_AUDIT.md`
- `tests/fixtures/consumer_proof_ledger_package_readiness_gate/consumer_proof_ledger_package_readiness_gate.json`
- `tests/test_lima_consumer_proof_ledger_package_readiness_gate_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`

If this design conflicts with a source artifact, the stricter source artifact controls.

## Operator Delivery Scope

The operator may manually deliver:

- the handoff package index
- the handoff artifact
- the delivery note
- the Sparkbot / Arc dry-run proof delivery brief
- the proof archive template
- the intake response template
- the proof results audit template
- the public API manifest
- the package-readiness gate and static-test audit summary
- the current LIMA commit or package candidate selected by the operator

The operator must not deliver:

- raw proof packet contents
- raw chat text
- raw office-task text
- customer records
- connector payloads
- provider payloads
- tool arguments
- credentials
- headers
- cookies
- tokens
- passwords
- pairing codes
- live scan dumps
- private SSIDs
- raw Bluetooth identifiers
- raw IP or MAC addresses
- device serial numbers
- precise physical location
- robot command payloads
- drone command payloads
- physical-world actuator payloads

## Manual Delivery Packet

The manual operator request should include this exact boundary:

```text
This is a proof-only LIMA handoff package.
Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads,
provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads
to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, devices, Robo-OS,
or physical-world systems.
The first proof is normalized metadata in and dry-run ExecutionResult out.
```

## Sparkbot Operator Request

The operator may manually ask the Sparkbot team:

```text
Please create `sparkbot-lima-dry-run-boundary-proof` in the Sparkbot repo.

Use the current audited LIMA commit or package candidate supplied with this request.
Use only proof-stage LIMA imports.
Build redacted already-normalized Sparkbot intent metadata locally.
Call `LimaKernel.evaluate(...)` with a default-deny capability profile.
Optionally pass `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata.
Optionally call `LimaKernel.preview_guardian_lifecycle(...)` as non-authoritative preview metadata only.

Return a redacted proof packet using `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`.

Do not wire public routes, mutate Sparkbot tasks/messages, invoke Sparkbot connectors/tools/providers/memory/storage/
schedulers, send raw chat text or prompts to LIMA, call models, execute tools, access storage, run browser/file/process/
network actions, perform live discovery, connect, pair, use credentials, invoke Robo-OS, control devices, control robots,
control drones, or touch physical-world systems through LIMA.
```

## Arc Bot Operator Request

The operator may manually ask the Arc Bot / LIMA Office team:

```text
Please create `arc-lima-dry-run-boundary-proof` in the Arc Bot / LIMA Office repo.

Use the current audited LIMA commit or package candidate supplied with this request.
Use only proof-stage LIMA imports.
Build redacted already-normalized Arc office-task metadata locally.
Call `LimaKernel.evaluate(...)` with a default-deny capability profile.
Optionally pass `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata.
Optionally call `LimaKernel.preview_guardian_lifecycle(...)` as non-authoritative preview metadata only.

Return a redacted proof packet using `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`.

Do not wire production office routes, mutate Arc tasks/projects/notes/forms/records/customer files, trigger schedulers
or background workers, invoke Arc connectors/tools/providers/memory/storage/office-system adapters, send raw office-task
text or customer records to LIMA, call models, execute tools, access storage, run browser/file/process/network actions,
perform live discovery, connect, pair, use credentials, invoke Robo-OS, control devices, control robots, control drones,
or touch physical-world systems through LIMA.
```

## Required Returned Evidence

Each consumer team should return a redacted proof packet containing:

- consumer repo
- consumer branch
- consumer team owner
- exact LIMA repository URL
- exact LIMA commit, tag, package version, or import method
- public imports used
- redacted already-normalized metadata evidence
- default-deny capability profile evidence
- explicit `LimaKernel.evaluate(...)` dry-run call evidence
- optional `SimulatedDiscoveryAdapter` evidence if used
- optional `LimaKernel.preview_guardian_lifecycle(...)` evidence if used
- dry-run `ExecutionResult` sample
- full non-execution invariant evidence
- redaction attestation
- forbidden surface attestation
- rollback or disable plan
- repo-team proof verdict

Allowed proof verdict:

`pass_for_dry_run_dependency_proof`

That verdict does not mean production readiness.

## Required Non-Execution Invariants

Every returned proof packet must include evidence that:

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

Missing evidence remains `needs_missing_evidence`.

Contradictory execution evidence remains `blocked_by_runtime_boundary`.

## Delivery Controls

The operator delivery request must preserve:

- consumer branches are repo-team owned
- LIMA repo does not create or inspect consumer branches
- proof packets are not accepted in this branch
- returned proof must be redacted before archive or audit
- proof archive and proof audit happen only in later approved branches
- Sparkbot and Arc packets are audited separately
- compatibility freeze starts only after both proof audits pass
- production readiness remains blocked

## Forbidden Claims

This operator delivery design must not be described as:

- production-ready
- Sparkbot integrated
- Arc Bot integrated
- public Sparkbot ready
- compatibility frozen
- live integration approved
- model-call ready
- tool-execution ready
- connector-ready
- storage-ready
- scheduler-ready
- live-discovery ready
- connection-ready
- pairing-ready
- credential-use ready
- Robo-OS ready
- device-control ready
- robotics-ready
- drone-ready
- physical-world ready

## Forbidden Actions

This operator delivery design must not trigger:

- automated sending
- proof packet receipt
- proof packet archive
- proof packet audit
- response sending
- ledger persistence
- compatibility freeze
- consumer repository edits
- public Sparkbot repository changes
- Arc Bot repository changes
- creation or pushing of consumer proof branches by LIMA
- fetching, cloning, scanning, or inspecting consumer repositories without explicit approval
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
- scheduler/background workers
- browser/file/process/network actions
- live discovery
- connection attempts
- pairing
- credential use or storage
- sockets
- OS network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- IoT adapters
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Next-Step Rule

If the operator manually delivers the request and no consumer packet is supplied:

- LIMA remains waiting
- no compatibility freeze may start
- no product-readiness claim may be made

If Sparkbot or Arc Bot supplies a packet:

- do not process it in this branch
- start `audit-consumer-owned-proof-results`
- check redaction before archive or audit
- audit Sparkbot and Arc packets separately

## Recommended Next Branch

If this design is accepted:

`audit-lima-consumer-proof-handoff-package-operator-delivery`

If Sparkbot or Arc Bot proof packets are supplied first:

`audit-consumer-owned-proof-results`
