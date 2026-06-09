# LIMA Consumer Proof Packet Request

## Design Status

This document designs a LIMA-local request contract for asking Sparkbot and Arc Bot / LIMA Office repo teams to produce
consumer-owned dry-run proof packets.

It is design-only. It does not send requests, deliver artifacts, create proof packets, receive proof packets, archive
proof packets, audit proof packets, update ledgers, persist state, start compatibility freeze, inspect consumer
repositories, create consumer branches, modify consumer repositories, modify `lima/`, modify `tests/support/`, modify
`pyproject.toml`, change package metadata, change public exports, wire shells, call models, execute tools, access
connectors, use storage, run schedulers, perform browser/file/process/network actions, perform live discovery, connect,
pair, use credentials, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve Sparkbot dependency use, Arc Bot dependency use, public Sparkbot release readiness, product
readiness, production readiness, live integration, compatibility freeze, model calls, tool execution, connector access,
storage/persistence, schedulers, live discovery, Robo-OS, device control, robotics, drones, or physical-world behavior.

## Purpose

The request contract answers one narrow question:

How should LIMA ask the Sparkbot and Arc Bot repo teams for redacted, consumer-owned dry-run proof packets without
automating delivery, inspecting consumer repos, or claiming product readiness?

This request contract is not:

- an external send
- a proof packet
- a proof branch
- a proof packet receiver
- a proof archive
- an intake service
- an automated evaluator
- an audit execution packet
- a result gate
- a compatibility freeze
- a product-readiness decision
- a runtime integration surface

Current state remains:

`lima_local_prerequisites_closed_waiting_on_consumer_proof`

Current freeze state remains:

`not_ready_for_freeze`

Current product state remains:

`not_production_ready`

## Relationship To Existing Artifacts

This design is derived from:

- `docs/handoffs/LIMA_CONSUMER_PROOF_OPERATOR_DELIVERY_REQUEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_STATUS_RECORD.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_EVALUATION_CONTRACT.md`
- `docs/design/LIMA_CONSUMER_PROOF_AUDIT_EXECUTION_PACKET.md`
- `docs/audits/LIMA_CONSUMER_PROOF_AUDIT_EXECUTION_PACKET_STATIC_TESTS_AUDIT.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_PROOF_EVIDENCE_INDEX.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_AUDIT_RESULT_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_GAP_RESPONSE_PLAYBOOK.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`

If this request contract conflicts with any stricter source artifact, the stricter artifact controls.

## Current Missing Inputs

The request exists because both consumer proof packets are still missing.

| Input | Current State |
| --- | --- |
| Sparkbot proof packet | `not_received` |
| Arc Bot proof packet | `not_received` |
| Sparkbot LIMA-side proof audit | `not_started` |
| Arc Bot LIMA-side proof audit | `not_started` |
| dual consumer result gate | `not_ready_for_result_gate` |
| compatibility freeze | `not_ready_for_freeze` |
| product readiness | `not_production_ready` |

This design does not change those states. It only defines the request that an operator may manually deliver outside the
LIMA repo if approved.

## Request Delivery Boundary

Delivery must remain manual and operator-controlled.

Allowed in this contract:

- prepare LIMA-local request text
- identify LIMA-local docs to include in an operator-delivered packet
- name the consumer-owned proof branches
- define returned proof evidence requirements
- define redaction and non-execution requirements
- define what LIMA must do after a packet is supplied

Forbidden in this contract:

- automated sending
- webhooks
- emails
- chat sends
- issue creation
- PR creation
- consumer branch creation
- consumer repo fetch, clone, scan, or inspection
- proof packet receipt
- proof packet archive
- proof packet audit execution
- result gate execution
- compatibility freeze
- runtime behavior

## Request Packet Shape

A future request packet should be a human-readable, copy-ready, LIMA-local artifact with this shape:

```yaml
request_id:
request_branch:
request_base_commit:
request_prepared_by:
request_date:
delivery_mode: manual_operator_delivery_only
current_lima_commit:
current_lima_branch:
package_name:
package_version_if_any:
target_consumers:
  - sparkbot
  - arc_bot
proof_stage_status: waiting_for_consumer_owned_dry_run_proof
product_readiness: not_production_ready
compatibility_freeze_state: not_ready_for_freeze
included_artifacts:
consumer_branch_requests:
returned_evidence_requirements:
forbidden_surfaces:
redaction_requirements:
non_execution_invariants:
next_step_after_delivery:
```

The request packet must contain instructions and references only. It must not contain raw proof evidence, consumer
payloads, credentials, secrets, tokens, headers, connector records, provider payloads, tool arguments, live scan data,
device identifiers, physical location, robot/drone payloads, or physical-world actuator payloads.

## Manual Delivery Warning

Every manually delivered request must include this warning:

```text
This is a proof-only LIMA request.
Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads,
provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads
to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, devices, Robo-OS,
or physical-world systems.
The first proof is normalized metadata in and dry-run ExecutionResult out.
```

## Artifacts To Include

The operator may manually include references to these LIMA-local artifacts:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_OPERATOR_DELIVERY_REQUEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_STATUS_RECORD.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_EVALUATION_CONTRACT.md`
- `docs/design/LIMA_CONSUMER_PROOF_AUDIT_EXECUTION_PACKET.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_PROOF_EVIDENCE_INDEX.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_AUDIT_RESULT_GATE.md`

The operator must not include raw proof packet contents because no proof packet has been supplied yet.

## Sparkbot Team Request

Manual request text for the Sparkbot repo team:

```text
Please create `sparkbot-lima-dry-run-boundary-proof` in the Sparkbot repo.

Use the current audited LIMA proof-stage commit supplied by the operator.
Use only proof-public LIMA imports.
Build redacted already-normalized Sparkbot intent metadata locally.
Call `LimaKernel.evaluate(...)` with a default-deny capability profile.
Optionally use `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata.
Return a redacted proof packet using `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`.

Do not wire public routes, mutate Sparkbot tasks/messages, invoke Sparkbot connectors/tools/providers/memory/storage/
schedulers, send raw chat text or prompts to LIMA, call models, execute tools, access storage, run browser/file/process/
network actions, perform live discovery, connect, pair, use credentials, invoke Robo-OS, control devices, control robots,
control drones, or touch physical-world systems through LIMA.
```

## Arc Bot / LIMA Office Team Request

Manual request text for the Arc Bot / LIMA Office repo team:

```text
Please create `arc-lima-dry-run-boundary-proof` in the Arc Bot / LIMA Office repo.

Use the current audited LIMA proof-stage commit supplied by the operator.
Use only proof-public LIMA imports.
Build redacted already-normalized Arc office-task metadata locally.
Call `LimaKernel.evaluate(...)` with a default-deny capability profile.
Optionally use `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata.
Return a redacted proof packet using `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`.

Do not wire production office routes, mutate Arc tasks/projects/notes/forms/records/customer files, trigger schedulers
or background workers, invoke Arc connectors/tools/providers/memory/storage/office-system adapters, send raw office-task
text or customer records to LIMA, call models, execute tools, access storage, run browser/file/process/network actions,
perform live discovery, connect, pair, use credentials, invoke Robo-OS, control devices, control robots, control drones,
or touch physical-world systems through LIMA.
```

## Proof-Public Imports

Consumer proof branches may use only:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Consumer proof branches must not rely on:

- `from lima import LimaKernel`
- unreviewed `dry_run_candidate` imports
- internal namespace imports
- top-level runtime re-exports
- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Returned Proof Packet Requirements

Each consumer team should return a redacted proof packet containing:

- consumer repo
- consumer branch
- consumer team owner
- exact LIMA repository URL
- exact LIMA commit, branch, tag, package version, or import method
- package name and package version if installable package testing was used
- public imports used
- redacted already-normalized metadata evidence
- default-deny capability profile evidence
- explicit `LimaKernel.evaluate(...)` dry-run call evidence
- optional `SimulatedDiscoveryAdapter` evidence if used
- dry-run `ExecutionResult` sample
- full non-execution invariant evidence
- redaction attestation
- forbidden surface attestation
- consumer-specific evidence
- rollback or disable plan
- repo-team proof verdict

Allowed repo-team proof verdict:

`pass_for_dry_run_dependency_proof`

That verdict does not mean product readiness, production readiness, live integration readiness, dependency-use approval,
or compatibility freeze readiness.

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

## Redaction Requirements

The request must tell consumer teams not to return:

- raw prompts
- raw chat text
- raw office-task text
- raw customer records
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- API keys
- secrets
- headers
- cookies
- tokens
- passwords
- pairing codes
- unsafe command bodies
- live scan dumps
- private SSIDs
- raw Bluetooth MAC addresses
- raw BLE identifiers
- raw IP addresses
- raw MAC addresses
- device serial numbers
- precise physical location
- robot command payloads
- drone command payloads
- physical-world actuator payloads

If any of these appear, the packet must be redacted before LIMA-side review.

## Consumer-Specific Requirements

Sparkbot proof packets must show:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

Arc Bot proof packets must show:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

## After Manual Delivery

If the operator manually delivers the request and no packet is supplied:

- LIMA remains `lima_local_prerequisites_closed_waiting_on_consumer_proof`
- Sparkbot proof packet remains `not_received`
- Arc Bot proof packet remains `not_received`
- compatibility freeze remains `not_ready_for_freeze`
- product readiness remains `not_production_ready`

If a proof packet is supplied:

- do not process it in this branch
- perform redaction review before archive or audit
- audit Sparkbot and Arc packets separately
- use `docs/design/LIMA_CONSUMER_PROOF_PACKET_EVALUATION_CONTRACT.md`
- record human review using `docs/design/LIMA_CONSUMER_PROOF_AUDIT_EXECUTION_PACKET.md`
- keep result gate blocked until both proof audits pass

## Forbidden Actions

This request contract must not trigger:

- automated sending
- external sends
- proof packet creation
- proof packet receipt
- proof packet archive
- proof packet audit execution
- automated intake
- automated evaluation
- response sending
- result gate execution
- compatibility freeze
- package version bump
- public export change
- consumer repo edits
- public Sparkbot repo changes
- Arc Bot repo changes
- consumer branch creation
- consumer repo fetch, clone, scan, or inspection without explicit approval
- `lima/` modifications
- `tests/support/` modifications
- runtime behavior
- shell wiring
- model calls
- tool execution
- connector access
- storage/persistence
- event spine persistence
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

## Later Static Implementation Boundary

A later static implementation branch may add only:

- `tests/fixtures/consumer_proof_packet_request/consumer_proof_packet_request.json`
- `tests/test_lima_consumer_proof_packet_request_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_PACKET_REQUEST_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

That branch must remain static. It must not send requests, receive proof packets, inspect consumer repos, modify `lima/`,
change public exports, add runtime behavior, add persistence, send responses, execute audits, run the result gate, or
approve a freeze.

## Readiness Decision

PASS for design of a LIMA-local, manual-operator consumer proof packet request contract.

NOT READY for automated delivery, proof packet receipt, proof packet archive, proof packet audit execution, result gate
execution, compatibility freeze, Sparkbot dependency-use claims, Arc Bot dependency-use claims, product use, or
production use.

The only safe current status remains:

`lima_local_prerequisites_closed_waiting_on_consumer_proof`

## Recommended Next Branch

`audit-lima-consumer-proof-packet-request`
