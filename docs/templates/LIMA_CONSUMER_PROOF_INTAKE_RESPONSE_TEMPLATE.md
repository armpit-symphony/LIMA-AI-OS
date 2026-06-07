# LIMA Consumer Proof Intake Response Template

## Template Status

This template is for human-reviewed LIMA-side responses to consumer-owned dry-run proof packets only.

It does not implement an intake service, parser, webhook, bot, ticket workflow, storage system, scheduler, background worker, notification sender, model call, connector, adapter, shell wiring, runtime behavior, live discovery, connection attempt, device behavior, Robo-OS behavior, robotics, drones, or physical-world behavior.

It does not approve production integration.

## 1. Intake Scope

- Intake response ID:
- LIMA reviewer:
- Review date:
- Consumer repo:
- Consumer branch:
- Consumer team owner:
- LIMA commit or version:
- Proof archive location:
- Intake source:

Expected consumer-owned proof branches:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot: `arc-lima-dry-run-boundary-proof`

The proof branch remains owned by the consumer repo team. The LIMA repo may archive and respond to proof evidence, but it must not modify Sparkbot or Arc Bot repo files.

## 2. Allowed Intake Sources

Allowed sources:

- Sparkbot repo team proof report
- Arc Bot / LIMA AI Office repo team proof report
- Spark Pit Labs internal archive note
- human-written repo-team question about the proof package
- human-written blocker summary
- human-written redaction issue summary

Forbidden sources:

- live webhooks
- production route payloads
- raw chat exports
- raw office-task exports
- customer record dumps
- connector payload dumps
- provider payload dumps
- tool argument dumps
- credentials
- headers
- cookies
- tokens
- live scan dumps
- device identifiers
- physical location
- robot/drone command payloads

## 3. Intake Packet Checklist

Required intake packet fields:

- `consumer_repo`
- `consumer_branch`
- `consumer_team_owner`
- `lima_commit_or_version`
- `proof_archive_location`
- `proof_verdict`
- `question_or_blocker_summary`
- `redaction_confirmed`
- `non_execution_invariants_confirmed`
- `forbidden_surfaces_confirmed_absent`
- `requested_lima_response`
- `recommended_next_action_from_consumer_team`

If any required field is missing, use response status `needs_missing_evidence`.

## 4. Incoming Proof Verdict Review

Allowed incoming proof verdicts:

- `pass_for_dry_run_proof_only`
- `needs_redaction`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_missing_evidence`
- `question_only`

Forbidden incoming proof verdicts:

- `production_ready`
- `ready_for_live_integration`
- `ready_for_model_calls`
- `ready_for_tool_execution`
- `ready_for_connector_access`
- `ready_for_live_discovery`
- `ready_for_device_control`
- `ready_for_robo_os`
- `ready_for_physical_world`

If the packet uses a forbidden verdict, classify it as `blocked_by_claim_boundary` and request a corrected proof packet.

## 5. LIMA Response Status Review

Allowed LIMA-side response statuses:

- `accepted_for_archive`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_claim_boundary`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `requires_followup_design`
- `requires_followup_audit`
- `not_ready_for_implementation`

Forbidden LIMA-side response statuses:

- `approved_for_production`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_live_discovery`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_physical_world`

## 6. LIMA Response Packet Checklist

Required response packet fields:

- `response_id`
- `consumer_repo`
- `consumer_branch`
- `lima_reviewer`
- `response_status`
- `summary`
- `accepted_evidence_refs`
- `missing_evidence`
- `redaction_findings`
- `boundary_findings`
- `forbidden_claim_findings`
- `recommended_next_branch`
- `production_readiness`

Required production readiness value:

- `production_readiness: not_production_ready`

## 7. Redaction Review

Set response status to `needs_redaction_before_review` if evidence includes:

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

Do not archive unredacted evidence in this LIMA repo.

## 8. Non-Execution Invariant Review

Every accepted proof packet must show:

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

If any invariant is missing, use response status `needs_missing_evidence`.

If any invariant contradicts non-execution, use response status `blocked_by_runtime_boundary`.

## 9. Boundary Finding Categories

Allowed boundary finding categories:

- `missing_lima_commit`
- `missing_import_method`
- `missing_normalized_metadata_evidence`
- `missing_capability_profile_evidence`
- `missing_execution_result_sample`
- `missing_non_execution_invariants`
- `missing_forbidden_surface_attestation`
- `redaction_failure`
- `forbidden_production_claim`
- `forbidden_runtime_claim`
- `consumer_repo_boundary_unclear`
- `sparkbot_specific_evidence_missing`
- `arc_specific_evidence_missing`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`

## 10. Next Branch Recommendation Rules

If intake is clean and proof-only:

- recommended next branch may be `audit-consumer-owned-proof-results`

If intake has missing evidence:

- recommended next branch should be `revise-consumer-proof-evidence`

If intake raises a LIMA design question:

- recommended next branch should be `design-lima-consumer-proof-question-response`

If intake raises a runtime blocker:

- recommended next branch should be `design-lima-runtime-blocker-resolution`

If intake requests production integration:

- response must be `blocked_by_claim_boundary`
- recommended next branch should be `audit-production-readiness-blockers`

## 11. Forbidden Surface Confirmation

This template does not authorize:

- modifying `lima/`
- modifying public Sparkbot repository files
- modifying Arc Bot repository files
- consumer integration implementation
- route wiring
- raw natural-language ingestion
- runtime `IntentEnvelope` creation
- live HumanInput bridge
- real Guardian decision authority
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
- connection attempts
- pairing
- credential use or storage
- sockets
- OS network APIs
- Bluetooth or BLE APIs
- USB or serial APIs
- MQTT, Matter, or mDNS APIs
- IoT adapters
- Robo-OS adapters
- Sparkbot wiring
- Arc Bot wiring
- device control
- robotics
- drones
- physical-world behavior

## 12. Example Intake Packet

```yaml
consumer_repo: sparkbot
consumer_branch: sparkbot-lima-dry-run-boundary-proof
consumer_team_owner: sparkbot-repo-team
lima_commit_or_version: exact-lima-commit
proof_archive_location: repo-team-owned-proof-report
proof_verdict: pass_for_dry_run_proof_only
question_or_blocker_summary: none
redaction_confirmed: true
non_execution_invariants_confirmed: true
forbidden_surfaces_confirmed_absent: true
requested_lima_response: accepted_for_archive
recommended_next_action_from_consumer_team: audit proof results
```

## 13. Example LIMA Response Packet

```yaml
response_id: lima-consumer-proof-response-001
consumer_repo: sparkbot
consumer_branch: sparkbot-lima-dry-run-boundary-proof
lima_reviewer: lima-runtime-team
response_status: accepted_for_archive
summary: proof packet accepted as dry-run evidence only
accepted_evidence_refs:
  - repo-team-owned-proof-report
missing_evidence: []
redaction_findings: []
boundary_findings: []
forbidden_claim_findings: []
recommended_next_branch: audit-consumer-owned-proof-results
production_readiness: not_production_ready
```

## 14. Remaining Product Blockers

This intake response template does not remove the current blockers to product use:

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

## 15. Final Response Verdict

- Response status:
- Recommended next branch:
- Production readiness: `not_production_ready`
- Reviewer notes:
