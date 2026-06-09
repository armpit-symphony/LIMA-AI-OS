# LIMA Consumer Proof Operator Delivery Static Tests Design

## Branch

`design-lima-consumer-proof-operator-delivery-static-tests`

## Base Commit

`a2994f54f2ba6e986c29836faa037c6a154177b2`

## Design Status

This document designs a later fixture-backed static test slice for the LIMA consumer proof operator-delivery gate.

It is design-only. It does not add tests, fixtures, runtime behavior, automated sending, proof packet receipt, proof
packet archive, proof packet audit, response sending, ledger persistence, compatibility freeze, package metadata
changes, public exports, shell wiring, consumer repository changes, consumer branch creation, or product-readiness
claims.

It does not modify `lima/`, `tests/support/`, `pyproject.toml`, Sparkbot, Arc Bot, LIMA-Robo-OS, provider/model
surfaces, adapters, tools, connectors, schedulers, browser/file/process/network behavior, live discovery, connection
attempts, pairing, credential use, device control, robotics, drones, or physical-world behavior.

## Purpose

The later static tests should lock the operator-delivery design into a machine-checkable LIMA-local state:

- operator delivery remains manual and outside the branch
- no automated delivery or external send is introduced
- no proof packets are created, received, archived, audited, or accepted
- Sparkbot and Arc proof branches remain consumer-owned
- Sparkbot and Arc proof packets remain missing until supplied by their repo teams
- the manual delivery request remains proof-only and dry-run-only
- redaction boundaries remain explicit
- non-execution invariants remain required
- compatibility freeze remains blocked
- product readiness remains `not_production_ready`
- runtime, storage, shell, connector, live discovery, Robo-OS, device, robot, drone, and physical-world behavior remain forbidden

## Source Artifacts

The later fixture and tests should reference and check the stricter-source rule across:

- `docs/design/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE_OPERATOR_DELIVERY.md`
- `docs/audits/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE_OPERATOR_DELIVERY_READINESS_REVIEW.md`
- `docs/audits/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE_OPERATOR_DELIVERY_AUDIT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
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

If the later fixture conflicts with any source artifact, the stricter source artifact must control.

## Allowed Later Files

A later implementation branch may touch only:

- `tests/fixtures/consumer_proof_operator_delivery/consumer_proof_operator_delivery.json`
- `tests/test_lima_consumer_proof_operator_delivery_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_OPERATOR_DELIVERY_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

The independent audit branch after that may touch only:

- `docs/audits/LIMA_CONSUMER_PROOF_OPERATOR_DELIVERY_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`

## Fixture Shape

The later fixture should be static metadata only.

Required fixture metadata:

- `schema_version`
- `fixture_scope`
- `operator_delivery_design_path`
- `operator_delivery_readiness_review_path`
- `operator_delivery_audit_path`
- `static_tests_design_path`
- `static_tests_readiness_review_path`
- `static_tests_design_audit_path`
- `static_tests_audit_path`
- `independent_audit_path`
- `operator_delivery_verdict`
- `current_state`
- `manual_delivery_artifacts`
- `manual_delivery_warning`
- `sparkbot_operator_request`
- `arc_bot_operator_request`
- `required_returned_evidence`
- `non_execution_invariants`
- `redaction_blockers`
- `delivery_controls`
- `forbidden_claims`
- `forbidden_actions`
- `allowed_later_files`
- `forbidden_later_surfaces`
- `recommended_next_branch`

All behavior and claim booleans must remain `false`:

- `automated_delivery_added`
- `external_send_added`
- `proof_packet_created`
- `proof_packet_received`
- `proof_packet_archived`
- `proof_packet_audited`
- `response_sending_added`
- `ledger_persistence_added`
- `compatibility_freeze_started`
- `consumer_repo_scanned`
- `consumer_repo_modified`
- `consumer_branch_created_by_lima`
- `runtime_behavior_changed`
- `lima_runtime_files_touched`
- `tests_support_touched`
- `pyproject_modified`
- `package_metadata_changed`
- `public_exports_changed`
- `storage_or_persistence_added`
- `runtime_wiring_added`
- `production_readiness_claimed`

## Static Test Coverage

The later static tests should verify:

- fixture metadata remains static and non-runtime
- operator-delivery design, readiness review, audit, static-test design/audit, implementation audit, and source paths exist
- source artifacts are referenced and stricter-source controls
- operator-delivery verdict remains `ready_for_manual_operator_delivery_request_only`
- delivery remains manual and outside the branch
- no automated delivery, external send, or response sending is represented
- no proof packet creation, receipt, archive, audit, or acceptance is represented
- Sparkbot branch remains `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot branch remains `arc-lima-dry-run-boundary-proof`
- consumer branches remain repo-team-owned
- LIMA repo does not create or inspect consumer branches
- manual delivery artifacts remain LIMA-local documentation and templates only
- raw proof packet contents and sensitive data remain forbidden delivery inputs
- manual delivery warning remains proof-only and dry-run-only
- Sparkbot request remains dry-run-only and forbids production routes, raw chat, connectors, models, tools, storage, schedulers, live discovery, Robo-OS, devices, robots, drones, and physical-world behavior
- Arc request remains dry-run-only and forbids production office routes, raw office-task text, customer records, connectors, models, tools, storage, schedulers, live discovery, Robo-OS, devices, robots, drones, and physical-world behavior
- required returned evidence remains listed
- `pass_for_dry_run_dependency_proof` remains non-production
- non-execution invariants remain listed
- missing evidence maps to `needs_missing_evidence`
- contradictory execution evidence maps to `blocked_by_runtime_boundary`
- returned proof must be redacted before archive or audit
- proof archive and audit happen only in later approved branches
- Sparkbot and Arc packets are audited separately
- compatibility freeze remains blocked until both proof audits pass
- production readiness remains blocked
- forbidden claims remain listed
- forbidden actions remain listed
- allowed later static-test implementation files remain bounded
- forbidden later surfaces remain listed
- independent audit is recommended after implementation

## Current State To Lock

The later static tests should lock:

- operator-delivery verdict: `ready_for_manual_operator_delivery_request_only`
- delivery status: `manual_operator_delivery_request_only`
- Sparkbot proof packet: `not_received`
- Arc Bot proof packet: `not_received`
- Sparkbot proof branch owner: `Sparkbot repo team`
- Arc Bot proof branch owner: `Arc Bot / LIMA Office repo team`
- proof archive status: `not_started`
- proof audit status: `not_started`
- compatibility freeze: `blocked`
- product readiness: `not_production_ready`

## Non-Execution Invariants

The later static tests must require:

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

The later static tests must require the delivery request to block:

- raw proof packet contents
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

Unsafe returned packets must remain classified as:

`needs_redaction_before_review`

## Forbidden Claims To Lock

The later static tests must keep these claims forbidden:

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

## Forbidden Actions To Lock

The later static tests must keep these actions forbidden:

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

## Recommended Next Branch

After this design branch:

`audit-lima-consumer-proof-operator-delivery-static-tests`

After that audit passes:

`implement-lima-consumer-proof-operator-delivery-static-tests`
