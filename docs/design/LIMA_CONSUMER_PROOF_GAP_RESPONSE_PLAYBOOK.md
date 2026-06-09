# LIMA Consumer Proof Gap Response Playbook

## Design Status

This document designs a LIMA-local, human-reviewed playbook for responding to gaps in future Sparkbot and Arc Bot
dry-run consumer proof packets.

It is design-only. It does not receive proof packets, archive proof packets, audit proof packets, accept proof packets,
send responses, create proof branches, inspect consumer repositories, modify consumer repositories, modify `lima/`,
modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, implement runtime
behavior, wire shells, call models, execute tools, access connectors, persist data, run schedulers, perform live
discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world
systems.

It does not approve product or production integration.

## Purpose

The playbook answers one narrow future question:

When a consumer-owned Sparkbot or Arc Bot proof packet is missing, incomplete, unredacted, over-claiming, or blocked by
runtime/consumer-boundary concerns, how should the LIMA reviewer classify the gap and recommend the next safe human
action?

The playbook is not:

- a proof packet
- an intake service
- a response sender
- an audit report
- a result gate
- a compatibility freeze
- a consumer repo scanner
- a runtime integration surface
- a production-readiness decision

Current state remains:

`lima_local_prerequisites_closed_waiting_on_consumer_proof`

Current freeze state remains:

`not_ready_for_freeze`

Current product state remains:

`not_production_ready`

## Relationship To Existing Artifacts

This playbook is derived from:

- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_PROOF_EVIDENCE_INDEX.md`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_PROOF_EVIDENCE_INDEX_AUDIT.md`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_PROOF_EVIDENCE_INDEX_STATIC_TESTS_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_AUDIT_RESULT_GATE.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITE_CLOSEOUT.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`

If this playbook conflicts with any stricter source artifact, the stricter artifact controls.

## Current Missing Inputs

The playbook starts from the current missing-proof state:

| Area | Current State |
| --- | --- |
| Sparkbot proof packet | `not_received` |
| Arc Bot proof packet | `not_received` |
| Sparkbot LIMA-side proof audit | `not_started` |
| Arc Bot LIMA-side proof audit | `not_started` |
| dual consumer result gate | `not_ready_for_result_gate` |
| compatibility freeze | `not_ready_for_freeze` |
| product readiness | `not_production_ready` |

This design does not change those states.

## Gap Categories

Allowed gap categories:

- `missing_packet`
- `missing_required_field`
- `missing_lima_commit_or_version`
- `missing_package_name_or_version`
- `missing_public_import_evidence`
- `missing_normalized_metadata_evidence`
- `missing_capability_profile_evidence`
- `missing_kernel_call_evidence`
- `missing_dry_run_result_evidence`
- `missing_simulated_discovery_evidence`
- `missing_non_execution_invariants`
- `missing_forbidden_surface_attestation`
- `missing_redaction_attestation`
- `missing_consumer_specific_evidence`
- `missing_rollback_or_disable_plan`
- `redaction_failure`
- `forbidden_public_import`
- `unreviewed_dry_run_candidate_import`
- `runtime_boundary_violation`
- `consumer_repo_boundary_violation`
- `forbidden_product_or_production_claim`
- `consumer_question`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`

Forbidden gap categories:

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
- `product_ready`
- `production_ready`

## Response Statuses

Allowed response statuses:

- `waiting_for_consumer_packet`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`
- `ready_for_human_audit`

Forbidden response statuses:

- `accepted_for_production`
- `accepted_for_live_integration`
- `accepted_for_model_calls`
- `accepted_for_tool_execution`
- `accepted_for_connector_access`
- `accepted_for_storage`
- `accepted_for_scheduler`
- `accepted_for_live_discovery`
- `accepted_for_connection`
- `accepted_for_pairing`
- `accepted_for_credential_use`
- `accepted_for_device_control`
- `accepted_for_robo_os`
- `accepted_for_robotics`
- `accepted_for_drones`
- `accepted_for_physical_world`
- `compatibility_freeze_started`
- `dependency_use_approved`
- `product_ready`
- `production_ready`

## Gap To Response Mapping

The LIMA reviewer should map gaps as follows:

| Gap Category | Response Status | Recommended Human Action |
| --- | --- | --- |
| `missing_packet` | `waiting_for_consumer_packet` | ask consumer team to supply a redacted proof packet |
| `missing_required_field` | `needs_missing_evidence` | request a corrected proof packet with required fields |
| `missing_lima_commit_or_version` | `needs_missing_evidence` | request exact LIMA commit, branch, tag, or package version |
| `missing_package_name_or_version` | `needs_missing_evidence` | request package name and package version evidence |
| `missing_public_import_evidence` | `needs_missing_evidence` | request proof-public import evidence |
| `missing_normalized_metadata_evidence` | `needs_missing_evidence` | request already-normalized metadata evidence |
| `missing_capability_profile_evidence` | `needs_missing_evidence` | request capability profile evidence |
| `missing_kernel_call_evidence` | `needs_missing_evidence` | request explicit `LimaKernel.evaluate(...)` dry-run call evidence |
| `missing_dry_run_result_evidence` | `needs_missing_evidence` | request redacted `ExecutionResult` evidence |
| `missing_simulated_discovery_evidence` | `needs_missing_evidence` | request explicit simulated-only evidence if simulated discovery was used |
| `missing_non_execution_invariants` | `needs_missing_evidence` | request full non-execution invariant evidence |
| `missing_forbidden_surface_attestation` | `needs_missing_evidence` | request forbidden-surface absence attestation |
| `missing_redaction_attestation` | `needs_redaction_before_review` | request redaction attestation before review |
| `missing_consumer_specific_evidence` | `needs_missing_evidence` | request Sparkbot-specific or Arc-specific evidence |
| `missing_rollback_or_disable_plan` | `needs_missing_evidence` | request rollback or disable plan |
| `redaction_failure` | `needs_redaction_before_review` | reject unredacted evidence and request a redacted packet |
| `forbidden_public_import` | `blocked_by_consumer_repo_boundary` | request proof rewritten against proof-public imports only |
| `unreviewed_dry_run_candidate_import` | `requires_lima_design_followup` | open design follow-up before accepting that surface |
| `runtime_boundary_violation` | `blocked_by_runtime_boundary` | stop proof review and request non-executing evidence only |
| `consumer_repo_boundary_violation` | `blocked_by_consumer_repo_boundary` | keep ownership with consumer team and request corrected packet |
| `forbidden_product_or_production_claim` | `blocked_by_claim_boundary` | request corrected language and remove product/live claims |
| `consumer_question` | `requires_lima_design_followup` | answer via design-only clarification |
| `requires_lima_design_followup` | `requires_lima_design_followup` | create a design-only LIMA follow-up branch |
| `requires_lima_audit_followup` | `requires_lima_audit_followup` | create an audit-only LIMA follow-up branch |

No mapping may produce product readiness, production readiness, live integration approval, compatibility freeze, or
runtime approval.

## Response Packet Shape

A future human-authored response should use this minimal shape:

```yaml
response_id:
consumer_repo:
consumer_branch:
lima_reviewer:
lima_commit_or_version:
gap_categories:
response_status:
redaction_findings:
missing_evidence:
runtime_boundary_findings:
consumer_repo_boundary_findings:
claim_boundary_findings:
recommended_human_action:
recommended_next_branch:
compatibility_freeze_state: not_ready_for_freeze
product_readiness: not_production_ready
```

The response packet must contain redacted summaries only. It must not contain raw proof evidence.

## Public API Gap Rules

Allowed proof-public imports remain:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

If a packet uses any of these, the response should be `blocked_by_consumer_repo_boundary` unless an explicit design
follow-up exists:

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

If a packet uses an unreviewed `dry_run_candidate` import, the response should be `requires_lima_design_followup`.

## Non-Execution Gap Rules

If any required invariant is missing, use:

`needs_missing_evidence`

If any required invariant is contradicted, use:

`blocked_by_runtime_boundary`

Required invariant evidence:

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

## Redaction Gap Rules

If any of the following appear, use:

`needs_redaction_before_review`

Do not copy the sensitive content into the LIMA repo:

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

## Consumer-Specific Gap Rules

Sparkbot proof gaps include missing evidence that:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

Arc Bot proof gaps include missing evidence that:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

Missing consumer-specific evidence should map to `needs_missing_evidence`.

## Recommended Branch Rules

If proof packet is missing:

- recommended next branch: none in LIMA until packet is supplied
- recommended human action: ask the consumer team for a redacted proof packet

If proof packet has missing evidence:

- recommended next branch: `revise-consumer-proof-evidence`
- owner: consumer repo team

If proof packet has redaction failure:

- recommended next branch: `revise-consumer-proof-evidence`
- owner: consumer repo team

If proof packet has a LIMA API design question:

- recommended next branch: `design-lima-consumer-api-gap-response`
- owner: LIMA repo team

If proof packet has a LIMA audit question:

- recommended next branch: `audit-lima-consumer-proof-gap-response`
- owner: LIMA repo team

If proof packet claims product or production readiness:

- recommended next branch: `audit-production-readiness-blockers`
- owner: LIMA repo team
- response status: `blocked_by_claim_boundary`

If both consumer packets later pass LIMA-side audits:

- recommended next branch: `design-lima-dry-run-consumer-compatibility-freeze`
- owner: LIMA repo team
- still design-only unless separately approved

## Forbidden Actions

This playbook must not trigger:

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

- `tests/fixtures/consumer_proof_gap_response_playbook/gap_response_playbook.json`
- `tests/test_lima_consumer_proof_gap_response_playbook_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_GAP_RESPONSE_PLAYBOOK_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

That branch must remain static. It must not receive proof packets, inspect consumer repos, modify `lima/`, change public
exports, add runtime behavior, add persistence, send responses, or approve a freeze.

## Readiness Decision

PASS for design of a human-reviewed gap response playbook.

NOT READY for compatibility freeze.

NOT READY for Sparkbot or Arc dependency-use claims.

NOT READY for product or production use.

The only safe current status remains:

`lima_local_prerequisites_closed_waiting_on_consumer_proof`

## Recommended Next Branch

`audit-lima-consumer-proof-gap-response-playbook`
