# LIMA Consumer Proof Archive Template

## Purpose

This document defines a LIMA-side template for the evidence packet that Sparkbot and Arc Bot repo teams should archive when they run consumer-owned dry-run proof branches.

This is design-only. It does not implement a template generator, modify `lima/`, touch Sparkbot or Arc repositories, create consumer wiring, call models, execute tools, access connectors, persist events, schedule work, scan networks, connect to devices, use credentials, invoke Robo-OS, or touch physical-world systems.

## Intended Consumers

The template is for future repo-owned proof branches:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot: `arc-lima-dry-run-boundary-proof`

Each consumer repo team owns its proof branch, fills out its archive packet, and keeps any consumer code changes in that repo.

## Archive Packet Goal

The packet should prove only this narrow claim:

```text
This consumer repo can import the current LIMA dependency candidate and call the non-executing dry-run kernel surface with already-normalized redacted metadata, while preserving all non-execution invariants.
```

The packet must not claim:

- production readiness
- route integration readiness
- model/provider readiness
- tool execution readiness
- connector readiness
- storage/persistence readiness
- approval enforcement readiness
- live discovery readiness
- network/device readiness
- Robo-OS readiness
- robot/drone/physical-world readiness

## Required Archive Sections

Each consumer proof archive should include:

1. Branch and owner
2. LIMA dependency reference
3. Consumer proof scope
4. Input evidence
5. Capability profile evidence
6. Kernel call evidence
7. Optional simulated discovery evidence
8. Dry-run result evidence
9. Non-execution invariant checklist
10. Forbidden surface checklist
11. Redaction and sensitive-data checklist
12. Consumer-specific evidence
13. Rollback or disable plan
14. Open blockers
15. Final proof verdict

## Section 1: Branch And Owner

Required fields:

- `consumer_repo`
- `consumer_branch`
- `consumer_team_owner`
- `proof_date`
- `proof_author`
- `reviewer`
- `lima_handoff_artifact`
- `lima_handoff_audit`

Expected branch values:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot: `arc-lima-dry-run-boundary-proof`

## Section 2: LIMA Dependency Reference

Required fields:

- `lima_repo`
- `lima_commit`
- `lima_branch_or_tag`
- `lima_package_version_if_any`
- `import_method`
- `public_imports_used`

Allowed public imports for this proof stage:

- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import SimulatedDiscoveryAdapter`

No consumer proof should import LIMA internals outside the approved public boundary.

## Section 3: Consumer Proof Scope

Required fields:

- `proof_goal`
- `proof_is_dry_run_only`
- `production_routes_touched`
- `consumer_state_mutated`
- `external_side_effects_observed`
- `runtime_claims_made`

Expected values:

- `proof_is_dry_run_only: true`
- `production_routes_touched: false`
- `consumer_state_mutated: false`
- `external_side_effects_observed: false`
- `runtime_claims_made: false`

## Section 4: Input Evidence

Required fields:

- `normalized_metadata_builder_or_fixture`
- `source_surface_metadata`
- `shell_id_redacted`
- `actor_id_redacted`
- `session_id_redacted`
- `context_refs_only`
- `raw_input_excluded`
- `sensitive_payloads_excluded`

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

## Section 5: Capability Profile Evidence

The packet must include the capability profile used for the proof.

Required expected false values:

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

If a consumer proof enables any simulated-only discovery capability, the packet must explain why it remains synthetic, inert, dry-run only, and non-executing.

## Section 6: Kernel Call Evidence

Required fields:

- `kernel_entrypoint`
- `request_type`
- `evaluate_called`
- `dry_run_requested`
- `raw_language_parser_used`
- `humaninput_bridge_used`
- `intent_envelope_created`
- `guardian_authority_created`

Expected values:

- `kernel_entrypoint: LimaKernel.evaluate`
- `evaluate_called: true`
- `dry_run_requested: true`
- `raw_language_parser_used: false`
- `humaninput_bridge_used: false`
- `intent_envelope_created: false`
- `guardian_authority_created: false`

The packet may include a redacted code excerpt or fixture reference, but it must not include raw prompts, customer records, credentials, or live connector payloads.

## Section 7: Optional Simulated Discovery Evidence

This section is optional.

It is required only if the consumer proof explicitly uses `SimulatedDiscoveryAdapter`.

Required fields:

- `simulated_adapter_used`
- `simulated_only`
- `dry_run`
- `synthetic_surfaces_only`
- `live_discovery_executed`
- `connection_attempted`
- `pairing_attempted`
- `credentials_used`
- `session_opened`
- `device_control_executed`
- `physical_world_executed`

Expected values:

- `simulated_adapter_used: true`
- `simulated_only: true`
- `dry_run: true`
- `synthetic_surfaces_only: true`
- `live_discovery_executed: false`
- `connection_attempted: false`
- `pairing_attempted: false`
- `credentials_used: false`
- `session_opened: false`
- `device_control_executed: false`
- `physical_world_executed: false`

The proof must not scan, discover, connect, pair, use credentials, open sockets, call OS network APIs, call Bluetooth/BLE APIs, call USB/serial APIs, call MQTT/Matter/mDNS APIs, or touch devices.

## Section 8: Dry-Run Result Evidence

Required fields:

- `result_status`
- `guardian_stub_summary`
- `event_refs`
- `redacted_audit_summary`
- `execution_result_sample_redacted`

Allowed result states:

- `proposed`
- `approval_required`
- `blocked`

The packet must not archive a result that claims execution, dispatch, persistence, approval enforcement, model calls, connector access, device access, or physical-world behavior occurred.

## Section 9: Non-Execution Invariant Checklist

Every proof archive must include these values:

- `executable: false`
- `execution_allowed: false`
- `side_effects_allowed: false`
- `dispatch_allowed: false`
- `persistence_allowed: false`
- `dry_run: true`
- `model_calls_allowed: false`
- `model_calls_executed: false`
- `live_discovery_executed: false`
- `connection_attempted: false`
- `pairing_attempted: false`
- `credentials_used: false`
- `session_opened: false`
- `device_control_executed: false`
- `physical_world_allowed: false`
- `physical_world_executed: false`
- `guardian_decision_created: false`
- `approval_enforced: false`
- `humaninput_bridge_active: false`
- `sparkbot_wiring_active: false`
- `robo_os_wiring_active: false`
- `adapter_active: false`
- `tool_execution_allowed: false`
- `driver_execution_allowed: false`
- `scheduler_active: false`
- `external_calls_allowed: false`

## Section 10: Forbidden Surface Checklist

The packet must include yes/no evidence that the proof did not touch:

- production route wiring
- raw natural-language execution
- raw prompt parsing in LIMA
- runtime `IntentEnvelope` creation
- live HumanInput bridge
- real Guardian decisions
- approval enforcement
- provider routing
- model calls
- tool execution
- connector reads or writes
- memory writes
- task state writes
- storage or persistence
- event spine persistence
- scheduler or background workers
- queues, daemons, subprocesses, or threads
- external sends
- browser actions
- file mutation
- process execution
- network actions
- live discovery
- scanning
- WiFi connection attempts
- Bluetooth or BLE connection attempts
- USB or serial connection attempts
- MQTT, Matter, or mDNS calls
- pairing
- credential use or storage
- device control
- Robo-OS access
- robotics
- drones
- physical-world behavior

## Section 11: Redaction And Sensitive-Data Checklist

The packet must confirm no archive evidence contains:

- raw prompts
- raw chat text
- raw office-task text
- raw customer records
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- headers
- cookies
- tokens
- passwords
- pairing codes
- private SSIDs
- raw Bluetooth MAC addresses
- raw IP or MAC addresses
- device serial numbers
- precise physical location
- robot or drone command payloads

If any item is present, the proof fails and must be redacted before archive.

## Section 12: Consumer-Specific Evidence

### Sparkbot

Sparkbot proof archive must include:

- proof no raw chat text was sent to LIMA
- proof no public Sparkbot production route was wired
- proof no Sparkbot task was created or mutated
- proof no Sparkbot message was sent or mutated
- proof no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

### Arc Bot

Arc Bot proof archive must include:

- proof no raw office-task text was sent to LIMA
- proof no customer record payload was sent to LIMA
- proof no customer communication was sent
- proof no Arc production route was wired
- proof no Arc task, project, note, form, record, or customer file was created or mutated
- proof no Arc scheduler or background worker was triggered
- proof no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

## Section 13: Rollback Or Disable Plan

Required fields:

- `proof_branch_disable_step`
- `dependency_revert_step`
- `feature_flag_or_import_gate_if_any`
- `owner_to_contact`
- `evidence_archive_location`

The rollback plan must not depend on live LIMA services because no live LIMA service is approved in this proof stage.

## Section 14: Open Blockers

Each proof archive must carry forward the current LIMA blockers:

- stable public API versioning policy
- stronger install/package verification if needed
- real Guardian request and decision lifecycle
- approval-required flow design
- approval enforcement implementation
- HumanInput bridge contract and implementation
- runtime `IntentEnvelope` creation contract and implementation
- provider/model boundary design and implementation
- tool execution boundary design and implementation
- connector boundary design and implementation
- scheduler/background-work boundary design and implementation
- event/spine persistence design
- storage interface implementation
- consumer-owned proof branch audit in each repo

## Section 15: Final Proof Verdict

Allowed verdicts:

- `pass_for_dry_run_proof_only`
- `needs_redaction`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_missing_evidence`

Forbidden verdicts:

- `production_ready`
- `ready_for_live_integration`
- `ready_for_model_calls`
- `ready_for_tool_execution`
- `ready_for_connector_access`
- `ready_for_live_discovery`
- `ready_for_device_control`
- `ready_for_robo_os`
- `ready_for_physical_world`

## Example Archive Skeleton

```yaml
proof_packet:
  consumer_repo: sparkbot-or-arc
  consumer_branch: sparkbot-lima-dry-run-boundary-proof-or-arc-lima-dry-run-boundary-proof
  lima_commit: exact-commit-required
  import_method: local-package-or-dependency-candidate
  proof_is_dry_run_only: true
  production_routes_touched: false
  consumer_state_mutated: false
  external_side_effects_observed: false
  normalized_metadata_builder_or_fixture: redacted-reference-only
  raw_input_excluded: true
  sensitive_payloads_excluded: true
  kernel_entrypoint: LimaKernel.evaluate
  dry_run_requested: true
  raw_language_parser_used: false
  humaninput_bridge_used: false
  intent_envelope_created: false
  guardian_authority_created: false
  result_status: proposed-or-approval_required-or-blocked
  non_execution_invariants:
    executable: false
    execution_allowed: false
    side_effects_allowed: false
    dispatch_allowed: false
    persistence_allowed: false
    dry_run: true
    model_calls_executed: false
    physical_world_executed: false
  final_verdict: pass_for_dry_run_proof_only
```

## Recommended Next Branch

`audit-lima-consumer-proof-archive-template`

That branch should independently audit this design before any fixture or template-file implementation.
