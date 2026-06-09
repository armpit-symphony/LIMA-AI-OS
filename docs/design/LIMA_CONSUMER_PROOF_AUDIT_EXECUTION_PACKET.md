# LIMA Consumer Proof Audit Execution Packet

## Design Status

This document designs a future LIMA-local, human-authored audit execution packet for recording the outcome of one
Sparkbot or Arc Bot dry-run consumer proof packet review.

It is design-only. It does not receive proof packets, archive proof packets, execute audits, automate evaluation,
accept proof packets, send responses, create proof branches, inspect consumer repositories, modify consumer
repositories, modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public
exports, implement runtime behavior, wire shells, call models, execute tools, access connectors, persist data, run
schedulers, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones,
or touch physical-world systems.

It does not approve product or production integration.

## Purpose

The audit execution packet answers one narrow future question:

When a human LIMA reviewer has manually evaluated a redacted Sparkbot or Arc Bot proof packet against the evaluation
contract, what reference-only packet shape should record that review outcome so it can later feed the dual-consumer
result gate?

This packet is not:

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

This design is derived from:

- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_EVALUATION_CONTRACT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_PACKET_EVALUATION_CONTRACT_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_PACKET_EVALUATION_CONTRACT_STATIC_TESTS_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_AUDIT_RESULT_GATE.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_PROOF_EVIDENCE_INDEX.md`
- `docs/design/LIMA_CONSUMER_PROOF_GAP_RESPONSE_PLAYBOOK.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`

If this design conflicts with any stricter source artifact, the stricter artifact controls.

## Current Missing Inputs

This design cannot be used yet because the required consumer proof packets and audits are missing:

| Input | Current State |
| --- | --- |
| Sparkbot proof packet | `not_received` |
| Arc Bot proof packet | `not_received` |
| Sparkbot LIMA-side proof audit | `not_started` |
| Arc Bot LIMA-side proof audit | `not_started` |
| dual consumer result gate | `not_ready_for_result_gate` |
| compatibility freeze | `not_ready_for_freeze` |
| product readiness | `not_production_ready` |

The packet design records the shape for a future manual audit result only. It does not create, fetch, request, receive,
store, archive, or evaluate any proof packet.

## Packet Preconditions

A future audit execution packet may be written only when all are true:

- a consumer team has supplied a redacted proof packet reference
- the proof packet is human-reviewed, not automatically ingested
- the proof packet claims to follow `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- the reviewer has evaluated it against `docs/design/LIMA_CONSUMER_PROOF_PACKET_EVALUATION_CONTRACT.md`
- the reviewer has not copied raw proof evidence into the LIMA repo
- the reviewer has not inspected or modified the consumer repository unless explicitly approved in a separate user task
- the review remains dry-run dependency proof only

If any precondition is missing, the audit execution packet must use a fail-closed status and must not feed the result
gate as a passing input.

## Packet Identity

A future packet should include:

```yaml
audit_execution_packet_id:
branch:
base_commit:
lima_reviewer:
review_date:
consumer_repo:
consumer_branch:
consumer_team_owner:
proof_packet_reference:
proof_packet_owner:
proof_packet_supplied_by:
lima_commit_or_package_version_reviewed:
package_name:
package_version:
evaluation_contract_version:
proof_archive_template_version:
```

The `proof_packet_reference` must be a redacted reference only. It must not embed raw proof content.

## Review Area Shape

Each review area should use this minimal shape:

```yaml
status:
evidence_refs:
redacted_summary:
missing_evidence:
boundary_findings:
redaction_findings:
recommended_human_action:
```

Allowed review-area statuses:

- `pass`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_applicable`

Forbidden review-area statuses:

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
- `dependency_use_approved`
- `product_ready`
- `production_ready`

## Required Review Areas

A future packet must include these review areas:

- `preflight_review`
- `public_api_import_review`
- `package_version_pin_review`
- `normalized_metadata_review`
- `capability_profile_review`
- `kernel_call_review`
- `simulated_discovery_review`
- `non_execution_invariant_review`
- `redaction_review`
- `forbidden_surface_review`
- `consumer_specific_review`
- `rollback_or_disable_plan_review`
- `claim_boundary_review`

Every review area must contain redacted summaries and references only.

## Public API Review Requirements

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

Forbidden import evidence maps the packet to `blocked_by_consumer_repo_boundary`.

## Runtime Review Requirements

The audit packet must record whether the proof showed:

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

Any execution, dispatch, persistence, model call, connector access, device access, or physical-world behavior maps the
packet to `blocked_by_runtime_boundary`.

## Simulated Discovery Review Requirements

If simulated discovery was not used, the area may be `not_applicable`.

If `SimulatedDiscoveryAdapter` was used, the audit packet must record whether evidence showed:

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

Live discovery, scanning, connection, pairing, credential use, device access, Robo-OS access, robotics, drones, or
physical-world behavior maps the packet to `blocked_by_runtime_boundary`.

## Non-Execution Invariant Requirements

The packet must record evidence for:

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

Missing invariant evidence maps the packet to `needs_missing_evidence`.

Contradictory invariant evidence maps the packet to `blocked_by_runtime_boundary`.

## Redaction Requirements

The packet must not contain:

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

If any appears, the packet status must be `needs_redaction_before_review`, and the sensitive content must not be copied
into the LIMA repo.

## Consumer-Specific Requirements

Sparkbot packets must record review of evidence that:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

Arc Bot packets must record review of evidence that:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

Missing consumer-specific evidence maps the packet to `needs_missing_evidence`.

Contradictory consumer-specific evidence maps the packet to `blocked_by_consumer_repo_boundary` unless it also proves
runtime execution, in which case `blocked_by_runtime_boundary` controls.

## Overall Packet Status

Allowed overall statuses:

- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

Forbidden overall statuses:

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

That status is only valid for one consumer packet and does not mean production readiness, dependency-use approval, live
integration readiness, result gate pass, or compatibility freeze readiness.

## Status Precedence

When multiple findings exist, choose the strictest applicable status:

1. `needs_redaction_before_review`
2. `blocked_by_runtime_boundary`
3. `blocked_by_consumer_repo_boundary`
4. `blocked_by_claim_boundary`
5. `needs_missing_evidence`
6. `requires_lima_design_followup`
7. `requires_lima_audit_followup`
8. `not_ready_for_implementation`
9. `pass_for_dry_run_dependency_proof`

`pass_for_dry_run_dependency_proof` may be used only when every required review area passes, optional simulated
discovery is either not applicable or safe, and no forbidden status is present.

## Result Gate Boundary

This packet does not run the dual-consumer result gate.

A future result gate may read two completed, redacted audit execution packets only if:

- one packet is for Sparkbot
- one packet is for Arc Bot
- both packets have status `pass_for_dry_run_dependency_proof`
- both packets reviewed the same LIMA commit or explicitly compatible package version
- both packets preserve proof-public imports only
- both packets preserve non-execution invariants
- both packets are redacted/reference-only

If either packet is missing or not passing, the combined result remains fail-closed per
`docs/design/LIMA_CONSUMER_PROOF_PACKET_AUDIT_RESULT_GATE.md`.

## Output Shape

A future audit execution packet should include:

```yaml
audit_execution_packet_id:
branch:
base_commit:
lima_reviewer:
review_date:
consumer_repo:
consumer_branch:
consumer_team_owner:
proof_packet_reference:
lima_commit_or_package_version_reviewed:
package_name:
package_version:
review_areas:
overall_status:
missing_evidence:
boundary_findings:
redaction_findings:
consumer_specific_findings:
compatibility_freeze_state: not_ready_for_freeze
product_readiness: not_production_ready
recommended_next_branch:
```

The packet must contain redacted summaries and evidence references only.

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

If one packet passes and the other is missing:

- recommended next branch: none in LIMA until the other consumer packet is supplied
- owner: consumer repo team for the missing packet

If both Sparkbot and Arc Bot packets later pass:

- recommended next branch: `design-lima-dry-run-consumer-compatibility-freeze`
- owner: LIMA repo team
- still design-only unless separately approved

## Forbidden Actions

This design must not trigger:

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

- `tests/fixtures/consumer_proof_audit_execution_packet/audit_execution_packet.json`
- `tests/test_lima_consumer_proof_audit_execution_packet_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_AUDIT_EXECUTION_PACKET_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

That branch must remain static. It must not receive proof packets, inspect consumer repos, modify `lima/`, change public
exports, add runtime behavior, add persistence, send responses, execute audits, run the result gate, or approve a freeze.

## Readiness Decision

PASS for design of a future human-authored audit execution packet shape.

NOT READY for proof packet receipt, proof packet archive, proof packet audit execution, result gate execution,
compatibility freeze, Sparkbot or Arc dependency-use claims, product use, or production use.

The only safe current status remains:

`lima_local_prerequisites_closed_waiting_on_consumer_proof`

## Recommended Next Branch

`audit-lima-consumer-proof-audit-execution-packet`
