# LIMA Consumer Proof Intake Response

## Purpose

This document designs the LIMA-side intake and response format for questions, proof packets, blockers, redaction issues, and audit results returned by Sparkbot and Arc Bot repo teams after they run their own consumer-owned dry-run proof branches.

This branch is design-only. It does not implement an intake service, parser, webhook, bot, ticket workflow, storage system, scheduler, background worker, notification sender, model call, connector, adapter, shell wiring, or runtime behavior.

## Scope Boundary

The intake response process is human-reviewed and documentation-first.

It may define:

- intake categories
- required metadata
- redaction expectations
- response statuses
- escalation categories
- LIMA-side archival expectations
- next-branch recommendations

It must not:

- modify Sparkbot repositories
- modify Arc Bot repositories
- modify `lima/`
- ingest raw chat or raw office-task text
- ingest customer records
- ingest credentials
- ingest connector/provider/tool payloads
- automate triage
- call models
- create runtime `IntentEnvelope` records
- create real Guardian decisions
- enforce approval
- persist events
- schedule work
- send messages
- call browser/file/process/network APIs
- perform live discovery
- connect to devices
- invoke Robo-OS
- control devices, robots, drones, or physical-world systems

## Intake Sources

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

## Intake Packet Shape

Each intake packet should include:

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

Expected branches:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot: `arc-lima-dry-run-boundary-proof`

## Allowed Proof Verdicts

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

If a consumer packet uses a forbidden verdict, the LIMA-side response must classify the packet as `blocked_by_claim_boundary` and request correction.

## LIMA Response Statuses

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

## Response Packet Shape

Each LIMA response should include:

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

Required `production_readiness` value:

`not_production_ready`

## Redaction Review

LIMA-side intake response must reject or return for redaction if evidence includes:

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

Response status should be:

`needs_redaction_before_review`

## Non-Execution Review

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

If any invariant is missing, response status should be:

`needs_missing_evidence`

If any invariant contradicts non-execution, response status should be:

`blocked_by_runtime_boundary`

## Boundary Finding Categories

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

## Recommended Next Branch Rules

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

## Example Intake Packet

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

## Example LIMA Response Packet

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

## Implementation Readiness

The next implementation-shaped branch may be:

`implement-lima-consumer-proof-intake-response-template`

That branch may add:

- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `tests/fixtures/consumer_proof_intake_response/consumer_proof_intake_response.json`
- `tests/test_lima_consumer_proof_intake_response_template.py`
- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE_IMPLEMENTATION_AUDIT.md`

It must remain docs/tests/fixtures-only and must not modify `lima/`, consumer repositories, runtime behavior, providers, tools, connectors, storage, schedulers, browser/file/process/network actions, device behavior, Robo-OS, robotics, drones, or physical-world systems.

## Recommended Next Branch

`audit-lima-consumer-proof-intake-response-design`

That branch should independently audit this design before any intake response template is implemented.
