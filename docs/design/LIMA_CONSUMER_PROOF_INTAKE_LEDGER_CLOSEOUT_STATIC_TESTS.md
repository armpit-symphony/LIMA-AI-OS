# LIMA Consumer Proof Intake Ledger Closeout Static Tests

## Design Status

This document designs a later fixture-backed static test slice for the Sparkbot / Arc Bot proof-packet intake ledger closeout.

It is design-only. It does not add tests, fixtures, runtime behavior, proof intake automation, storage, persistence, public exports, package metadata, shell wiring, consumer repository changes, proof packet receipt claims, proof archive claims, proof audit claims, compatibility freeze claims, or product-readiness claims.

It does not modify `lima/`, `tests/support/`, `pyproject.toml`, Sparkbot, Arc Bot, LIMA-Robo-OS, provider/model surfaces, adapters, tools, connectors, schedulers, browser/file/process/network behavior, live discovery, connection attempts, pairing, credential use, device control, robotics, drones, or physical-world behavior.

## Purpose

The later static tests should lock the closeout document into a machine-checkable LIMA-local state:

- LIMA-local intake materials are prepared.
- Sparkbot and Arc Bot proof packets are still missing.
- LIMA-local materials are preparation only, not consumer proof.
- Proof-public imports remain aligned with the public API manifest fixture.
- Non-execution invariants remain aligned with the public API manifest fixture.
- Compatibility freeze and product readiness remain blocked.
- Consumer repository boundaries remain explicit.
- Runtime, storage, shell, connector, live discovery, Robo-OS, device, robot, drone, and physical-world behavior remain forbidden.

## Source Artifacts

The later static tests should reference and check the stricter-source rule across:

- `docs/design/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT.md`
- `docs/audits/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT_READINESS_REVIEW.md`
- `docs/audits/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE_STATIC_TESTS_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW.md`
- `docs/audits/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW_STATIC_TESTS_AUDIT.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`

If the later fixture conflicts with any source artifact, the stricter source artifact must control.

## Allowed Later Files

A later implementation branch may touch only:

- `tests/fixtures/consumer_proof_intake_ledger_closeout/consumer_proof_intake_ledger_closeout.json`
- `tests/test_lima_consumer_proof_intake_ledger_closeout_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_LEDGER_CLOSEOUT_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

The independent audit branch after that may touch only:

- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_LEDGER_CLOSEOUT_STATIC_TESTS_AUDIT.md`

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

- proof packet receipt
- proof packet archive
- proof packet audit
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
- `closeout_path`
- `readiness_review_path`
- `audit_path`
- `static_tests_audit_path`
- `public_api_manifest_fixture_path`
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
- `compatibility_freeze_started`
- `automated_intake_added`
- `storage_or_persistence_added`
- `runtime_wiring_added`
- `production_readiness_claimed`

All behavior and claim booleans above must remain `false`.

## Static Test Coverage

The later static tests should verify:

- fixture metadata remains static and non-runtime
- closeout, readiness review, audit, static-test audit, and public API manifest fixture paths exist
- source artifacts are referenced and stricter source controls
- closeout verdict remains `intake_ledger_ready_waiting_for_consumer_packets`
- Sparkbot packet remains `not_received`
- Arc Bot packet remains `not_received`
- Sparkbot proof audit remains `not_started`
- Arc Bot proof audit remains `not_started`
- Sparkbot redaction review remains `not_checked` / `not_started`
- Arc Bot redaction review remains `not_checked` / `not_started`
- compatibility freeze remains `blocked`
- product readiness remains `not_production_ready`
- LIMA-local materials are preparation only and not proof that Sparkbot or Arc Bot can use LIMA
- required consumer packet fields remain present
- public proof imports match `tests/fixtures/public_api/lima_public_api_manifest.json`
- `LimaKernel.preview_guardian_lifecycle(...)` remains a method-level candidate only
- lifecycle preview result dataclasses, `dry_run_candidate` imports, internal namespaces, and top-level runtime re-exports are not promoted as proof-public imports
- forbidden consumer imports remain blocked
- non-execution invariants are listed and match the public API manifest fixture
- redaction blockers remain listed and fail-closed
- Sparkbot-specific missing evidence remains listed
- Arc Bot-specific missing evidence remains listed
- manual intake closeout flow remains manual and non-automated
- compatibility freeze remains blocked until both packets and audits pass and a freeze branch is separately designed and audited
- forbidden closeout claims remain listed
- reviewer forbidden actions remain listed
- the later static-test implementation audit bounds files and forbidden surfaces
- the later static-test implementation recommends independent audit before any next proof lane

## Required Packet Fields To Lock

The later fixture and tests should lock the closeout requirement that each consumer packet include:

- consumer repo
- consumer branch
- consumer team owner
- LIMA repository URL
- exact LIMA commit or package version
- package name
- package version
- public imports used
- proof archive location
- import method
- normalized metadata evidence
- capability profile evidence
- explicit `LimaKernel.evaluate(...)` evidence
- dry-run `ExecutionResult` evidence
- optional simulated discovery evidence if used
- optional Guardian lifecycle preview evidence if used
- non-execution invariant evidence
- forbidden surface attestation
- redaction attestation
- rollback or disable plan
- final proof verdict

## Proof-Public API Boundary

The later static tests must match proof-public imports from the public API manifest fixture:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

The only method-level dry-run candidate in this lane is:

- `LimaKernel.preview_guardian_lifecycle(...)`

The later static tests must keep these forbidden consumer imports blocked:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Non-Execution Invariants

The later static tests must require the closeout to preserve:

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

The later static tests must require the closeout to block archiving or audit for:

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

## Consumer Boundary Evidence To Lock

Sparkbot-specific missing evidence must remain listed until supplied by the Sparkbot repo team:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector was invoked by LIMA
- no Sparkbot tool was invoked by LIMA
- no Sparkbot provider was invoked by LIMA
- no Sparkbot memory was invoked by LIMA
- no Sparkbot storage was invoked by LIMA
- no Sparkbot scheduler was invoked by LIMA
- no live terminal, browser, file, network, connector, model, scheduler, or external send behavior was introduced through LIMA

Arc Bot-specific missing evidence must remain listed until supplied by the Arc Bot / LIMA Office repo team:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector was invoked by LIMA
- no Arc tool was invoked by LIMA
- no Arc provider was invoked by LIMA
- no Arc memory was invoked by LIMA
- no Arc storage was invoked by LIMA
- no office-system adapter was invoked by LIMA
- no live office connector, customer system, file, browser, process, network, scheduler, model, or external send behavior was introduced through LIMA

## Manual Closeout Flow

The later static tests should lock the flow as manual:

1. Confirm packet source and consumer-owned branch.
2. Check redaction before archive or audit.
3. Update the receipt ledger manually.
4. Send human-reviewed intake response if packet is missing evidence or blocked.
5. Audit packet using `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.
6. Record audit status.
7. Repeat separately for Sparkbot and Arc Bot.
8. Start compatibility freeze design only if both proof audits pass as `pass_for_dry_run_dependency_proof`.

The later static tests must not automate this flow.

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

## Implementation Branch Boundary

The later implementation branch may only add fixture-backed static tests and an implementation audit for the closeout.

It must not:

- receive proof packets
- archive proof packets
- audit proof packets
- update a receipt ledger as evidence
- claim proof has passed
- start compatibility freeze
- claim Sparkbot or Arc Bot dependency use
- claim public Sparkbot readiness
- claim product or production readiness
- implement runtime behavior
- inspect or modify consumer repositories

## Recommended Next Branch

After this design branch:

`audit-lima-consumer-proof-intake-ledger-closeout-static-tests`

After that audit passes:

`implement-lima-consumer-proof-intake-ledger-closeout-static-tests`
