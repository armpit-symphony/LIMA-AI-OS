# LIMA Consumer Proof Ledger Package Readiness Gate Static Tests Design

## Branch

`design-lima-consumer-proof-ledger-package-readiness-gate-static-tests`

## Base Commit

`927c22130abdd4719707644df9879133e6d64211`

## Design Status

This branch defines a design for later fixture-backed static tests for the LIMA consumer proof ledger
package readiness gate. It is design-only and does not add tests, fixtures, runtime behavior, proof
packet intake automation, proof packet receipt, proof packet archive, proof packet audit, response sending,
ledger persistence, compatibility freeze, package metadata changes, public exports, shell wiring,
consumer repository changes, or product-readiness claims.

It does not modify `lima/`, `tests/support/`, `pyproject.toml`, Sparkbot, Arc Bot, LIMA-Robo-OS,
provider/model surfaces, adapters, tools, connectors, storage, browser/file/process/network behavior,
live discovery, connection attempts, pairing, credential use, device control, robotics, drones, or physical-world
behavior.

## Goal

The later static-test implementation should lock the existing package-readiness gate as
**docs-only LIMA-local readiness to request consumer proof packets**, not as proof that Sparkbot or Arc Bot
has accepted LIMA.

## Source Artifacts

The later fixture and tests should be validated against and constrained by:

- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_READINESS_REVIEW.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_READINESS_REVIEW.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_STATUS_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`

If any later fixture conflicts with source artifacts, the stricter source artifact remains authoritative.

## Allowed Later Files

A later implementation branch may add only:

- `tests/fixtures/consumer_proof_ledger_package_readiness_gate/consumer_proof_ledger_package_readiness_gate.json`
- `tests/test_lima_consumer_proof_ledger_package_readiness_gate_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

An independent audit branch after that may add only:

- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`

## Fixture Shape

The fixture must be static metadata only.

Required top-level fields:

- `schema_version`
- `fixture_scope`
- `gate_design_path`
- `gate_audit_path`
- `audit_readiness_review_path`
- `static_tests_design_path`
- `static_tests_readiness_review_path`
- `static_tests_audit_path`
- `package_readiness_gates_path`
- `package_state`
- `redaction_policy`
- `non_execution_invariants`
- `sparkbot_requirements`
- `arc_bot_requirements`
- `prohibited_runtime_behaviors`
- `consumer_boundary`
- `compatibility_freeze`
- `forbidden_claims`
- `forbidden_actions`
- `allowed_later_files`
- `forbidden_later_surfaces`
- `recommended_next_branch`

Required `package_readiness_gates_path` entries:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_STATUS_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_RECEIPT_RESPONSE_EXAMPLES.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/design/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW.md`
- `docs/design/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT.md`

All behavior and claim booleans in the fixture must remain `false`:

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

## Static Test Coverage

The later static tests should verify:

- fixture is static metadata (no runtime fields, no live payloads)
- gate design, audit, readiness review, and implementation-audit paths exist and are local
- source artifacts are referenced and stricter-source control is applied
- gate verdict remains `ready_for_operator_handoff_request_only`
- proof shape remains:
  - Sparkbot/Arc branch ownership unchanged
  - dry-run-only expectation
  - no model/tool/execution/storage/connector/discovery/connection/credential/Robo-OS/device/robot/drone/physical claims
- Sparkbot packet remains `not_received`
- Arc Bot packet remains `not_received`
- Sparkbot and Arc redaction reviews remain `not_started`
- Sparkbot and Arc proof audits remain `not_started`
- compatibility freeze remains `blocked`
- product readiness remains `not_production_ready`
- redaction blockers remain present:
  - raw prompts, raw text, customer records, credentials, provider payloads, tool args, identifiers, tokens,
    credentials, serials, locations, and physical command payloads
- all non-execution invariants remain `false` for execution fields and `true` for dry-run fields:
  - `executable`, `execution_allowed`, `side_effects_allowed`, `dispatch_allowed`, `persistence_allowed`,
    `model_calls_allowed`, `model_calls_executed`, `live_discovery_executed`, `connection_attempted`,
    `pairing_attempted`, `credentials_used`, `session_opened`, `device_control_executed`, `physical_world_allowed`,
    `physical_world_executed`
  - `dry_run`
- forbidden claims and actions remain listed and present
- in-memory/manual-only interpretation remains required
- no fixture path references consumer repositories, network endpoints, credentials, or storage backends
- implementation-file and forbidden-surface boundaries are explicit
- implementation branch must be explicitly static-test only
- independent audit branch is required before any implementation

## Forbidden Runtime/Proof Surface

The static-test design and future implementation must still block:

- proof packet receipt
- proof packet archive
- proof packet audit
- automated response sending
- ledger persistence
- compatibility freeze
- runtime behavior
- shell wiring
- storage and persistence
- provider/model calls
- tool execution
- connector access
- scheduler/background work
- browser/file/process/network behavior
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
- Robo-OS
- device control
- robotics
- drones
- physical-world behavior

## Current State to Lock

The later static tests should encode the current state:

- LIMA proof package: `prepared_for_handoff_request`
- Sparkbot proof packet: `not_received`
- Arc Bot proof packet: `not_received`
- Sparkbot redaction review: `not_started`
- Arc Bot redaction review: `not_started`
- Sparkbot proof audit: `not_started`
- Arc Bot proof audit: `not_started`
- compatibility freeze: `blocked`
- production readiness: `not_production_ready`

## Recommended Next Branch

`audit-lima-consumer-proof-ledger-package-readiness-gate-static-tests`
