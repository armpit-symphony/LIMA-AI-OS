# LIMA Consumer Proof Intake Response Ledger Update Gate Static Tests

## Design Status

This document designs a later fixture-backed static test slice for the LIMA consumer proof intake response ledger update gate.

It is design-only. It does not add tests, fixtures, runtime behavior, proof packet intake automation, proof packet receipt, proof packet archive, proof packet audit, response sending, receipt ledger persistence, compatibility freeze, package metadata changes, public exports, shell wiring, consumer repository changes, or product-readiness claims.

It does not modify `lima/`, `tests/support/`, `pyproject.toml`, Sparkbot, Arc Bot, LIMA-Robo-OS, provider/model surfaces, adapters, tools, connectors, schedulers, browser/file/process/network behavior, live discovery, connection attempts, pairing, credential use, device control, robotics, drones, or physical-world behavior.

## Purpose

The later static tests should lock the gate into a machine-checkable LIMA-local state:

- the gate remains docs-only and manual
- response-to-ledger mapping remains fail-closed
- Sparkbot and Arc Bot proof packets remain missing until supplied by their repo teams
- intake response alone does not prove packet receipt, proof archive acceptance, proof audit, compatibility freeze, product readiness, or production readiness
- ledger update rules remain human-maintained document records only
- response packet rules remain human-reviewed records only
- redaction-before-archive and redaction-before-audit remain required
- non-execution invariants remain required for accepted packets
- consumer repo ownership remains explicit
- compatibility freeze remains blocked until both proof audits pass
- runtime, storage, shell, connector, live discovery, Robo-OS, device, robot, drone, and physical-world behavior remain forbidden

## Source Artifacts

The later static tests should reference and check the stricter-source rule across:

- `docs/design/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_LEDGER_UPDATE_GATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_LEDGER_UPDATE_GATE_READINESS_REVIEW.md`
- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_LEDGER_UPDATE_GATE_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_RECEIPT_RESPONSE_EXAMPLES.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE.md`

If the later fixture conflicts with any source artifact, the stricter source artifact must control.

## Allowed Later Files

A later implementation branch may touch only:

- `tests/fixtures/consumer_proof_intake_response_ledger_update_gate/consumer_proof_intake_response_ledger_update_gate.json`
- `tests/test_lima_consumer_proof_intake_response_ledger_update_gate_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_LEDGER_UPDATE_GATE_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

The independent audit branch after that may touch only:

- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_LEDGER_UPDATE_GATE_STATIC_TESTS_AUDIT.md`

## Forbidden Files And Surfaces

The later implementation branch must not modify:

- `lima/`
- `tests/support/`
- `pyproject.toml`
- package metadata
- public exports
- public Sparkbot repository
- Sparkbot R&D repository
- Arc Bot repository
- consumer proof branches
- adapter implementation files
- provider/model files
- storage/persistence files
- shell wiring files
- Robo-OS files

The later implementation branch must not add or claim:

- proof packet receipt automation
- proof packet archive automation
- proof packet audit
- response sending
- receipt ledger persistence
- compatibility freeze
- Sparkbot readiness
- Arc Bot readiness
- public Sparkbot readiness
- product readiness
- production readiness
- runtime behavior
- shell wiring
- storage
- persistence
- provider/model calls
- tool execution
- connector access
- scheduler/background work
- browser/file/process/network behavior
- live discovery
- connection attempts
- pairing
- credential use or storage
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Fixture Shape

The later fixture should be static metadata only.

Required fixture metadata:

- `schema_version`
- `fixture_scope`
- `gate_path`
- `readiness_review_path`
- `audit_path`
- `static_tests_design_path`
- `static_tests_design_audit_path`
- `static_tests_audit_path`
- `runtime_behavior_changed`
- `lima_runtime_files_touched`
- `tests_support_touched`
- `pyproject_modified`
- `package_metadata_changed`
- `public_exports_changed`
- `public_sparkbot_repo_touched`
- `arc_bot_repo_touched`
- `consumer_repo_scanned`
- `consumer_proof_packet_received`
- `consumer_proof_packet_archived`
- `consumer_proof_packet_audited`
- `response_sending_added`
- `ledger_persistence_added`
- `compatibility_freeze_started`
- `automated_intake_added`
- `storage_or_persistence_added`
- `runtime_wiring_added`
- `production_readiness_claimed`

All behavior and claim booleans above must remain `false`.

## Static Test Coverage

The later static tests should verify:

- fixture metadata remains static and non-runtime
- gate, readiness review, audit, static-test design audit, implementation audit, and source paths exist
- source artifacts are referenced and stricter source controls
- current proof state remains Sparkbot `not_received`, Arc Bot `not_received`, proof audits `not_started`, compatibility freeze `blocked`, and product readiness `not_production_ready`
- allowed gate inputs remain human-supplied and redacted
- forbidden gate inputs remain blocked
- pre-update entry conditions remain present and fail-closed
- response-to-ledger mapping includes every allowed response status
- response-to-ledger mapping does not allow production/live/model/tool/connector/storage/live-discovery/Robo-OS/device/robot/drone/physical-world approval or compatibility freeze
- manual ledger update fields remain present
- manual response packet fields remain present
- `production_readiness` remains `not_production_ready`
- redaction blockers remain listed and map to `needs_redaction_before_review`
- raw sensitive evidence must not be stored in ledger records
- non-execution invariants remain listed
- missing invariant evidence maps to `needs_missing_evidence`
- contradictory execution evidence maps to `blocked_by_runtime_boundary`
- Sparkbot-specific archive gate remains present
- Arc Bot-specific archive gate remains present
- branch recommendation rules remain safe
- compatibility freeze remains blocked until both proof audits pass
- intake response or ledger update alone never unfreezes compatibility
- forbidden status values remain listed
- forbidden gate behavior remains listed
- reviewer forbidden actions remain listed
- allowed later static-test implementation files remain bounded
- forbidden later surfaces remain listed
- independent audit is recommended before any implementation branch

## Response-To-Ledger Mapping To Lock

The later static tests should lock these response-to-ledger mappings:

- `accepted_for_archive` -> `redacted`, `accepted_for_archive`, `ready_for_lima_side_audit`
- `needs_redaction_before_review` -> `needs_redaction_before_review`, `needs_missing_evidence`, `needs_redaction_before_review`
- `needs_missing_evidence` -> `not_checked` or `redacted`, `needs_missing_evidence`, `needs_missing_evidence`
- `blocked_by_claim_boundary` -> `not_checked` or `redacted`, `blocked_by_claim_boundary`, `blocked_by_claim_boundary`
- `blocked_by_runtime_boundary` -> `not_checked` or `redacted`, `blocked_by_runtime_boundary`, `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary` -> `not_checked` or `redacted`, `blocked_by_consumer_repo_boundary`, `blocked_by_consumer_repo_boundary`
- `requires_followup_design` -> `not_checked` or `redacted`, `requires_lima_design_followup`, `requires_lima_design_followup`
- `requires_followup_audit` -> `redacted`, `requires_lima_audit_followup`, `ready_for_lima_side_audit`
- `not_ready_for_implementation` -> `not_checked` or `redacted`, `requires_lima_design_followup`, `not_ready_for_implementation`

## Manual Ledger Fields To Lock

The later tests should require:

- `receipt_id`
- `received_date`
- `received_by`
- `consumer_repo`
- `consumer_branch`
- `consumer_team_owner`
- `packet_location`
- `packet_kind`
- `lima_commit_or_package_version`
- `package_name`
- `package_version`
- `redaction_status`
- `intake_status`
- `audit_status`
- `accepted_evidence_refs`
- `missing_evidence`
- `boundary_findings`
- `forbidden_claim_findings`
- `recommended_next_branch`
- `production_readiness`
- `reviewer_notes`

## Manual Response Fields To Lock

The later tests should require:

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

## Non-Execution Invariants

The later static tests must require the gate to preserve:

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

## Redaction Blockers

The later static tests must require the gate to block archive or audit for:

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

Unsafe packets must remain classified as:

`needs_redaction_before_review`

## Compatibility Freeze Gate

The later static tests should keep compatibility freeze `blocked` unless:

- Sparkbot packet is received
- Arc Bot packet is received
- both packets pass redaction checks
- Sparkbot proof audit passes as `pass_for_dry_run_dependency_proof`
- Arc Bot proof audit passes as `pass_for_dry_run_dependency_proof`
- no missing evidence blockers remain
- no forbidden import blockers remain
- no runtime boundary blockers remain
- no consumer repo boundary blockers remain
- no production/live-readiness claim blockers remain
- a compatibility freeze branch is separately designed and audited

The tests must verify that an intake response or ledger update alone never unfreezes compatibility.

## Recommended Next Branch

After this design branch:

`audit-lima-consumer-proof-intake-response-ledger-update-gate-static-tests`

After that audit passes:

`implement-lima-consumer-proof-intake-response-ledger-update-gate-static-tests`
