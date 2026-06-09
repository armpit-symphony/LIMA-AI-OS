# LIMA Consumer Proof Packet Evaluation Contract

## Design Status

This document designs a future LIMA-local, human-reviewed evaluation contract for one supplied Sparkbot or Arc Bot
dry-run consumer proof packet.

It is design-only. It does not receive proof packets, archive proof packets, audit proof packets, accept proof packets,
send responses, create proof branches, inspect consumer repositories, modify consumer repositories, modify `lima/`,
modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, implement runtime
behavior, wire shells, call models, execute tools, access connectors, persist data, run schedulers, perform live
discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world
systems.

It does not approve product or production integration.

## Purpose

The evaluation contract answers one narrow future question:

When a consumer-owned Sparkbot or Arc Bot proof packet has been supplied as a redacted reference, what exact LIMA-side
checks must a human reviewer perform before the packet can produce a single proof-audit status?

This contract is not:

- a proof packet
- an intake service
- an archive service
- an automated evaluator
- a response sender
- a result gate
- a compatibility freeze
- a product-readiness decision
- a consumer repo scanner
- a runtime integration surface

Current state remains:

`lima_local_prerequisites_closed_waiting_on_consumer_proof`

Current freeze state remains:

`not_ready_for_freeze`

Current product state remains:

`not_production_ready`

## Relationship To Existing Artifacts

This contract is derived from:

- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_PROOF_EVIDENCE_INDEX.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_AUDIT_RESULT_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_GAP_RESPONSE_PLAYBOOK.md`
- `docs/audits/LIMA_CONSUMER_PROOF_GAP_RESPONSE_PLAYBOOK_STATIC_TESTS_AUDIT.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`

If this contract conflicts with any stricter source artifact, the stricter artifact controls.

## Current Missing Inputs

This contract cannot be applied yet because both consumer proof packets are missing:

| Input | Current State |
| --- | --- |
| Sparkbot proof packet | `not_received` |
| Arc Bot proof packet | `not_received` |
| Sparkbot LIMA-side proof audit | `not_started` |
| Arc Bot LIMA-side proof audit | `not_started` |
| dual consumer result gate | `not_ready_for_result_gate` |
| compatibility freeze | `not_ready_for_freeze` |
| product readiness | `not_production_ready` |

The contract defines how to evaluate a future supplied packet only. It does not create, fetch, request, or store that
packet.

## Evaluation Inputs

A future evaluation may review only a human-supplied, redacted reference packet that claims to follow
`docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`.

Required packet identity:

- `consumer_repo`
- `consumer_branch`
- `consumer_team_owner`
- `proof_packet_reference`
- `proof_packet_owner`
- `proof_packet_supplied_by`
- `lima_commit_or_package_version`
- `package_name`
- `package_version`
- `import_method`
- `public_imports_used`

Required evidence references:

- `normalized_metadata_evidence`
- `capability_profile_evidence`
- `kernel_call_evidence`
- `dry_run_result_evidence`
- `simulated_discovery_evidence`, if simulated discovery was used
- `non_execution_invariant_evidence`
- `forbidden_surface_attestation`
- `redaction_attestation`
- `consumer_specific_evidence`
- `rollback_or_disable_plan`
- `final_proof_verdict`

The evaluator may record redacted summaries and references only. The evaluator must not copy raw proof evidence into
the LIMA repo.

## Preflight Gate

Before evaluating proof content, the reviewer must classify the packet preflight state.

Allowed preflight states:

- `not_received`
- `received_redacted_reference_only`
- `received_needs_redaction`
- `received_missing_required_fields`
- `rejected_for_claim_boundary`
- `rejected_for_consumer_repo_boundary`

Preflight mapping:

| Condition | Preflight State | Audit Status |
| --- | --- | --- |
| no packet supplied | `not_received` | `needs_missing_evidence` |
| packet reference supplied and redacted | `received_redacted_reference_only` | continue evaluation |
| packet contains unredacted sensitive content | `received_needs_redaction` | `needs_redaction_before_review` |
| required identity or evidence fields missing | `received_missing_required_fields` | `needs_missing_evidence` |
| packet claims product, production, live integration, freeze, or dependency-use approval | `rejected_for_claim_boundary` | `blocked_by_claim_boundary` |
| packet requires consumer repo inspection, branch creation, or repo mutation by LIMA | `rejected_for_consumer_repo_boundary` | `blocked_by_consumer_repo_boundary` |

If the preflight state is anything except `received_redacted_reference_only`, evaluation stops.

## Public API Evaluation

Allowed proof-public imports:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Imports requiring design follow-up:

- unreviewed `dry_run_candidate` imports from `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`

Forbidden consumer imports:

- `from lima import LimaKernel`
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

Evaluation outcomes:

- proof-public imports only -> continue evaluation
- unreviewed `dry_run_candidate` import -> `requires_lima_design_followup`
- forbidden import -> `blocked_by_consumer_repo_boundary`
- missing import evidence -> `needs_missing_evidence`

This contract does not change public exports.

## Normalized Metadata Evaluation

The packet must show already-normalized metadata only.

Allowed input evidence:

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

Forbidden input evidence:

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

Missing normalized metadata evidence maps to `needs_missing_evidence`.

Raw or sensitive input evidence maps to `needs_redaction_before_review` unless it also proves runtime execution, in
which case it maps to `blocked_by_runtime_boundary`.

## Capability Profile Evaluation

The packet must show a default-deny capability profile unless a simulated-only discovery capability is enabled and
explained as synthetic, inert, dry-run only, and non-executing.

Required default-deny capability evidence:

- `model_calls: false`
- `memory_write: false`
- `task_state_write: false`
- `connector_read: false`
- `connector_write: false`
- `external_send: false`
- `file_write: false`
- `process_execute: false`
- `browser_control: false`
- `device_control: false`
- `robotics_actuation: false`
- `drone_actuation: false`
- `scheduler_run: false`
- `connection_attempt: false`
- `device_pairing: false`
- `credential_use: false`
- `physical_world_actuation: false`

Missing capability evidence maps to `needs_missing_evidence`.

Any enabled consequential, live, device, robot, drone, physical-world, model, connector, tool, process, browser,
file-write, scheduler, external-send, pairing, credential, or connection capability without a dry-run proof boundary maps
to `blocked_by_runtime_boundary`.

## Kernel Call Evaluation

The packet must show an explicit dry-run kernel call:

- `LimaKernel.evaluate(...)` called explicitly
- request is already-normalized
- dry run requested
- no raw natural-language parser in LIMA
- no live HumanInput bridge
- no runtime `IntentEnvelope` creation
- no real `GuardianDecision` authority
- no approval enforcement
- no hidden adapter dispatch
- redacted result evidence returned

Allowed result states:

- `proposed`
- `approval_required`
- `blocked`

Missing kernel-call evidence maps to `needs_missing_evidence`.

Any result state or packet claim that execution, dispatch, persistence, approval enforcement, model calls, connector
access, device access, or physical-world behavior occurred maps to `blocked_by_runtime_boundary`.

## Simulated Discovery Evaluation

If `SimulatedDiscoveryAdapter` is not used, the packet may mark simulated discovery evidence as not applicable.

If it is used, the packet must show:

- explicit adapter usage
- no kernel hidden auto-dispatch
- `dry_run is True`
- `simulated_only is True`
- synthetic surfaces only
- inert surfaces only
- surfaces are not connectable
- surfaces are not controllable
- live discovery executed is False
- scan occurred is False
- connection attempted is False
- pairing attempted is False
- credentials used is False
- session opened is False
- device control executed is False
- physical-world behavior occurred is False

If live discovery, scanning, connection, pairing, credential use, device access, Robo-OS access, robotics, drones, or
physical-world behavior appears, classify as `blocked_by_runtime_boundary`.

## Non-Execution Invariant Evaluation

Every accepted packet must show:

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

Missing invariant evidence maps to `needs_missing_evidence`.

Contradictory invariant evidence maps to `blocked_by_runtime_boundary`.

## Redaction Evaluation

Classify as `needs_redaction_before_review` if the packet includes:

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

LIMA must not archive unredacted consumer evidence.

## Consumer-Specific Evaluation

Sparkbot packets must prove:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

Arc Bot packets must prove:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

Missing consumer-specific evidence maps to `needs_missing_evidence`.

Contradictory consumer-specific evidence maps to `blocked_by_consumer_repo_boundary` unless it also proves runtime
execution, in which case `blocked_by_runtime_boundary` controls.

## Audit Status Contract

Allowed audit statuses:

- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

Forbidden audit statuses:

- `approved_for_production`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_storage`
- `approved_for_scheduler`
- `approved_for_live_discovery`
- `approved_for_connection`
- `approved_for_pairing`
- `approved_for_credential_use`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_robotics`
- `approved_for_drones`
- `approved_for_physical_world`
- `compatibility_frozen`
- `sparkbot_integrated`
- `arc_bot_integrated`
- `dependency_use_approved`
- `product_ready`
- `production_ready`

The only passing status is:

`pass_for_dry_run_dependency_proof`

That status does not mean production readiness, live integration readiness, dependency-use approval, or compatibility
freeze readiness.

## Evaluation Precedence

When multiple findings exist, the reviewer must choose the strictest applicable status:

1. `needs_redaction_before_review`
2. `blocked_by_runtime_boundary`
3. `blocked_by_consumer_repo_boundary`
4. `blocked_by_claim_boundary`
5. `needs_missing_evidence`
6. `requires_lima_design_followup`
7. `requires_lima_audit_followup`
8. `not_ready_for_implementation`
9. `pass_for_dry_run_dependency_proof`

Redaction blockers stop review until the packet is corrected. Runtime execution evidence blocks before consumer-boundary
or claim-boundary remediation. A pass can occur only when every required review area passes and no forbidden status is
present.

## Evaluation Output Shape

A future human-authored evaluation report should include:

```yaml
evaluation_id:
branch:
base_commit:
consumer_repo:
consumer_branch:
consumer_team_owner:
proof_packet_reference:
lima_commit_or_package_version:
package_name:
package_version:
preflight_state:
public_api_import_review:
normalized_metadata_review:
capability_profile_review:
kernel_call_review:
simulated_discovery_review:
non_execution_invariant_review:
redaction_review:
forbidden_surface_review:
consumer_specific_review:
missing_evidence:
boundary_findings:
redaction_findings:
audit_status:
compatibility_freeze_state: not_ready_for_freeze
product_readiness: not_production_ready
recommended_next_branch:
```

The report must contain redacted summaries and references only.

## Recommended Branch Rules

If a packet is missing:

- recommended next branch: none in LIMA until packet is supplied
- recommended human action: ask the consumer team for a redacted proof packet

If a packet has missing evidence:

- recommended next branch: `revise-consumer-proof-evidence`
- owner: consumer repo team

If a packet has redaction failure:

- recommended next branch: `revise-consumer-proof-evidence`
- owner: consumer repo team

If a packet has a LIMA API design question:

- recommended next branch: `design-lima-consumer-api-gap-response`
- owner: LIMA repo team

If a packet has a LIMA audit question:

- recommended next branch: `audit-lima-consumer-proof-gap-response`
- owner: LIMA repo team

If a packet claims product or production readiness:

- recommended next branch: `audit-production-readiness-blockers`
- owner: LIMA repo team

If a packet passes:

- recommended next branch: wait for the other consumer packet audit, or feed both passing audits into
  `design-lima-dry-run-consumer-compatibility-freeze`
- owner: LIMA repo team
- still design-only unless separately approved

## Forbidden Actions

This evaluation contract must not trigger:

- proof packet receipt
- proof packet archive
- proof packet audit
- automated intake
- response sending
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

- `tests/fixtures/consumer_proof_packet_evaluation_contract/evaluation_contract.json`
- `tests/test_lima_consumer_proof_packet_evaluation_contract_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_PACKET_EVALUATION_CONTRACT_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

That branch must remain static. It must not receive proof packets, inspect consumer repos, modify `lima/`, change public
exports, add runtime behavior, add persistence, send responses, or approve a freeze.

## Readiness Decision

PASS for design of a future human-reviewed consumer proof packet evaluation contract.

NOT READY for proof packet receipt, proof packet audit, result gate, compatibility freeze, Sparkbot or Arc
dependency-use claims, product use, or production use.

The only safe current status remains:

`lima_local_prerequisites_closed_waiting_on_consumer_proof`

## Recommended Next Branch

`audit-lima-consumer-proof-packet-evaluation-contract`
