# LIMA Dry-Run Consumer Proof Evidence Index

## Design Status

This document designs a future LIMA-local evidence index for Sparkbot and Arc Bot dry-run consumer proof artifacts.

It is design-only. It does not receive proof packets, archive proof packets, audit proof packets, accept proof packets,
create proof branches, inspect consumer repositories, modify consumer repositories, modify `lima/`, modify
`tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, implement runtime behavior,
wire shells, call models, execute tools, access connectors, persist data, run schedulers, perform live discovery,
connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve product or production integration.

## Purpose

The evidence index answers one future bookkeeping question:

When Sparkbot and Arc Bot proof packets are supplied by their owning teams, what minimal redacted reference metadata
must LIMA record so reviewers can find the packet, audit it, and feed the result gate without treating the packet as
accepted or compatibility-freeze ready?

The evidence index is not:

- a proof packet
- a proof archive
- an intake service
- an audit report
- a result gate
- a compatibility freeze
- a product-readiness record
- a persistence layer
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

- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_AUDIT_RESULT_GATE.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITE_CLOSEOUT.md`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITE_CLOSEOUT_STATIC_TESTS_AUDIT.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`

If this design conflicts with any stricter source artifact, the stricter artifact controls.

## Current Missing Inputs

The index must start empty because no consumer-owned proof packet has been supplied.

| Input | Current State | Required Before Result Gate |
| --- | --- | --- |
| Sparkbot proof packet reference | `not_received` | yes |
| Arc Bot proof packet reference | `not_received` | yes |
| Sparkbot proof packet redaction confirmation | `not_started` | yes |
| Arc Bot proof packet redaction confirmation | `not_started` | yes |
| Sparkbot LIMA-side proof audit | `not_started` | yes |
| Arc Bot LIMA-side proof audit | `not_started` | yes |
| dual consumer result gate | `not_ready_for_result_gate` | yes |
| compatibility freeze | `not_ready_for_freeze` | yes |
| product readiness | `not_production_ready` | yes |

The evidence index cannot make any of these states pass. It can only point to future redacted evidence after the user
supplies it or explicitly approves review of it.

## Index Entry Shape

A future index entry should be a human-authored, redacted metadata record with this shape:

```yaml
evidence_index_id:
consumer_repo:
consumer_branch:
consumer_team_owner:
proof_packet_reference:
proof_packet_owner:
proof_packet_supplied_by:
proof_packet_received_state:
redaction_state:
lima_commit_or_version_claimed:
package_name_claimed:
package_version_claimed:
public_imports_claimed:
normalized_metadata_evidence_ref:
capability_profile_evidence_ref:
kernel_call_evidence_ref:
dry_run_result_evidence_ref:
simulated_discovery_evidence_ref:
non_execution_invariant_evidence_ref:
forbidden_surface_attestation_ref:
consumer_specific_evidence_ref:
rollback_or_disable_plan_ref:
lima_side_audit_state:
lima_side_audit_report_ref:
result_gate_input_state:
compatibility_freeze_state:
product_readiness:
redacted_summary:
missing_evidence:
boundary_findings:
recommended_next_branch:
```

The index must store references and redacted summaries only. It must not store raw proof evidence.

## Allowed Index Entry Values

Allowed `consumer_repo` values:

- `sparkbot`
- `arc_bot`

Allowed `consumer_branch` values:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot / LIMA Office: `arc-lima-dry-run-boundary-proof`

Allowed `proof_packet_received_state` values:

- `not_received`
- `received_redacted_reference_only`
- `received_needs_redaction`
- `received_missing_required_fields`
- `rejected_for_claim_boundary`
- `rejected_for_consumer_repo_boundary`

Allowed `redaction_state` values:

- `not_started`
- `redacted_reference_only`
- `needs_redaction_before_review`
- `redaction_failed`

Allowed `lima_side_audit_state` values:

- `not_started`
- `ready_for_human_audit`
- `audit_in_progress`
- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

Allowed `result_gate_input_state` values:

- `not_ready_for_result_gate`
- `ready_for_result_gate`
- `needs_redaction_before_result_gate`
- `needs_missing_consumer_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`

Required `compatibility_freeze_state` value until both audits pass:

- `not_ready_for_freeze`

Required `product_readiness` value:

- `not_production_ready`

## Forbidden Index Values

The index must never use:

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
- `public_sparkbot_release_ready`
- `product_ready`
- `production_ready`

## Redaction Boundary

Index entries must not contain:

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

If an incoming artifact includes any of these, the index may record only:

`needs_redaction_before_review`

It must not copy the sensitive content into the LIMA repo.

## Public API Evidence Boundary

The index may reference only proof-public import evidence:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

The index must flag as boundary findings:

- `from lima import LimaKernel`
- unreviewed `dry_run_candidate` imports
- standalone preview result dataclass imports
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

## Non-Execution Evidence Boundary

The index may point to future redacted evidence only if it preserves:

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

Missing evidence must keep the entry at `needs_missing_evidence` or `not_ready_for_result_gate`.

Contradictory evidence must become `blocked_by_runtime_boundary`.

## Consumer-Specific Evidence Boundary

Sparkbot evidence references must prove:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

Arc Bot evidence references must prove:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

If consumer-specific evidence is missing, the index state must remain `needs_missing_evidence`.

## Lifecycle

Future index entries may move through these human-reviewed states:

1. `not_received`
2. `received_redacted_reference_only`
3. `ready_for_human_audit`
4. `audit_in_progress`
5. `pass_for_dry_run_dependency_proof` or a fail-closed audit status
6. `ready_for_result_gate` only if both consumer entries have passing audits

The lifecycle must not include automated polling, background scanning, repository inspection, webhooks, file watchers,
model review, scheduler work, or durable persistence unless separately designed and approved.

## Example Empty Index

This branch may describe an empty index only:

```yaml
entries:
  sparkbot:
    consumer_repo: sparkbot
    consumer_branch: sparkbot-lima-dry-run-boundary-proof
    proof_packet_received_state: not_received
    redaction_state: not_started
    lima_side_audit_state: not_started
    result_gate_input_state: not_ready_for_result_gate
    compatibility_freeze_state: not_ready_for_freeze
    product_readiness: not_production_ready
  arc_bot:
    consumer_repo: arc_bot
    consumer_branch: arc-lima-dry-run-boundary-proof
    proof_packet_received_state: not_received
    redaction_state: not_started
    lima_side_audit_state: not_started
    result_gate_input_state: not_ready_for_result_gate
    compatibility_freeze_state: not_ready_for_freeze
    product_readiness: not_production_ready
```

This is not a received proof packet and not an archive.

## Forbidden Actions

This evidence index design must not trigger:

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

## Later Implementation Boundary

A later static implementation branch may add only:

- `tests/fixtures/dry_run_consumer_proof_evidence_index/evidence_index.json`
- `tests/test_lima_dry_run_consumer_proof_evidence_index_static.py`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_PROOF_EVIDENCE_INDEX_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

That branch must remain static. It must not receive or archive proof packets, inspect consumer repos, modify `lima/`,
change public exports, add runtime behavior, add persistence, or approve a freeze.

## Readiness Decision

PASS for design of a future static evidence index.

NOT READY for compatibility freeze.

NOT READY for Sparkbot or Arc dependency-use claims.

NOT READY for product or production use.

The only safe current status remains:

`lima_local_prerequisites_closed_waiting_on_consumer_proof`

## Recommended Next Branch

`audit-lima-dry-run-consumer-proof-evidence-index`
