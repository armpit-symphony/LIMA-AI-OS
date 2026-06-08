# LIMA Consumer Proof Readiness Closeout Package Static Tests

## Design Status

This document designs a later fixture-backed static test slice for the LIMA consumer proof readiness closeout package.

It is design-only. It does not add tests, fixtures, runtime behavior, proof packet intake automation, proof packet receipt, proof packet archive, proof packet audit, receipt ledger persistence, compatibility freeze, package metadata changes, public exports, shell wiring, consumer repository changes, or product-readiness claims.

It does not modify `lima/`, `tests/support/`, `pyproject.toml`, Sparkbot, Arc Bot, LIMA-Robo-OS, provider/model surfaces, adapters, tools, connectors, schedulers, browser/file/process/network behavior, live discovery, connection attempts, pairing, credential use, device control, robotics, drones, or physical-world behavior.

## Purpose

The later static tests should lock the closeout package into a machine-checkable LIMA-local state:

- the package remains an operator-facing index and delivery wrapper, not a source of truth
- LIMA is ready only for consumer-owned dry-run proof handoff
- Sparkbot and Arc Bot proof packets are still missing until supplied by their repo teams
- proof packet receipt, archive, audit, compatibility freeze, and product readiness remain blocked
- proof-public imports remain aligned with the public API manifest fixture
- non-execution invariants remain aligned with the public API manifest fixture
- Sparkbot and Arc Bot consumer repository boundaries remain explicit
- runtime, storage, shell, connector, live discovery, Robo-OS, device, robot, drone, and physical-world behavior remain forbidden

## Source Artifacts

The later static tests should reference and check the stricter-source rule across:

- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE_READINESS_REVIEW.md`
- `docs/audits/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE_AUDIT.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_STATUS_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_RECEIPT_RESPONSE_EXAMPLES.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/design/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW.md`
- `docs/design/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_INTAKE_LEDGER_CLOSEOUT_STATIC_TESTS.md`

If the later fixture conflicts with any source artifact, the stricter source artifact must control.

## Allowed Later Files

A later implementation branch may touch only:

- `tests/fixtures/consumer_proof_readiness_closeout_package/consumer_proof_readiness_closeout_package.json`
- `tests/test_lima_consumer_proof_readiness_closeout_package_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`

The independent audit branch after that may touch only:

- `docs/audits/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE_STATIC_TESTS_AUDIT.md`

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
- `package_path`
- `readiness_review_path`
- `audit_path`
- `static_tests_design_path`
- `static_tests_design_audit_path`
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
- package design, readiness review, audit, static-test design audit, static-test implementation audit, and public API manifest fixture paths exist
- source artifacts are referenced and stricter source controls
- package verdict remains `ready_for_consumer_owned_dry_run_proof_handoff_only`
- the latest LIMA-local reference commit remains a local preparation checkpoint only
- Sparkbot packet remains `not_received`
- Arc Bot packet remains `not_received`
- Sparkbot proof audit remains `not_started`
- Arc Bot proof audit remains `not_started`
- compatibility freeze remains `blocked`
- product readiness remains `not_production_ready`
- required package contents remain listed
- required audit and static-test evidence references remain listed
- Sparkbot consumer branch remains `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot consumer branch remains `arc-lima-dry-run-boundary-proof`
- delivery warning remains proof-only and forbids production routes, raw sensitive data, model calls, tool calls, connectors, storage, schedulers, external sends, browsers, files, processes, networks, devices, Robo-OS, robots, drones, and physical-world systems
- allowed proof shape remains consumer-owned, redacted, normalized, explicit, dry-run, and non-authoritative
- required consumer proof packet fields remain present
- Sparkbot evidence requirements remain present
- Arc Bot evidence requirements remain present
- proof-public imports match `tests/fixtures/public_api/lima_public_api_manifest.json`
- `LimaKernel.preview_guardian_lifecycle(...)` remains a method-level dry-run candidate only
- lifecycle preview result dataclasses, `dry_run_candidate` imports, internal namespaces, and top-level runtime re-exports are not promoted as proof-public imports
- forbidden consumer imports remain blocked
- non-execution invariants are listed and match the public API manifest fixture
- redaction blockers remain listed and fail-closed
- manual intake path remains manual and non-automated
- compatibility freeze remains blocked until both packets and audits pass and a freeze branch is separately designed and audited
- forbidden package claims remain listed
- forbidden package actions remain listed
- the later static-test implementation audit bounds files and forbidden surfaces
- the later static-test implementation recommends independent audit before any next proof lane

## Package Contents To Lock

The later fixture and tests should lock the required package contents:

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
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_RECEIPT_RESPONSE_EXAMPLES.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/design/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW.md`
- `docs/design/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_INTAKE_LEDGER_CLOSEOUT_STATIC_TESTS.md`

The later fixture and tests should also lock the required audit/static-test evidence references:

- `docs/audits/LIMA_CONSUMER_PROOF_STATUS_PACKAGE_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_STATUS_PACKAGE_STATIC_TESTS_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE_STATIC_TESTS_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW_STATIC_TESTS_AUDIT.md`
- `docs/audits/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_LEDGER_CLOSEOUT_STATIC_TESTS_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_LEDGER_CLOSEOUT_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`

## Required Packet Fields To Lock

The later fixture and tests should lock the package requirement that each consumer packet include:

- consumer repo
- consumer branch
- consumer team owner
- LIMA repository URL
- exact LIMA commit or package version
- package name
- package version
- import method
- public imports used
- proof archive location
- redacted already-normalized metadata evidence
- capability profile evidence
- explicit `LimaKernel.evaluate(...)` call evidence
- dry-run `ExecutionResult` evidence
- optional explicit simulated discovery evidence if used
- optional `LimaKernel.preview_guardian_lifecycle(...)` evidence if used
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

- top-level runtime re-exports such as `from lima import LimaKernel`
- standalone lifecycle preview result dataclass imports
- unreviewed `dry_run_candidate` imports
- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Non-Execution Invariants

The later static tests must require the package to preserve:

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

The later static tests must require the package to block packets containing:

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

The later static tests must not automate redaction or archive unredacted evidence.

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
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

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
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Manual Intake Path

The later static tests should lock the flow as manual:

1. Do not ingest packets automatically.
2. Confirm packet source and consumer-owned branch.
3. Confirm the packet is dry-run proof only.
4. Check for redaction issues before archiving.
5. If redaction is unsafe, respond using `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`.
6. If the packet is clean enough to audit, audit it using `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.
7. Audit Sparkbot and Arc Bot packets separately.
8. If either packet is missing or blocked, do not freeze compatibility.
9. If both packets pass as `pass_for_dry_run_dependency_proof`, design a dry-run consumer compatibility freeze in a separate branch.

The later static tests must not automate this flow.

## Compatibility Freeze Gate

The later static tests should keep compatibility freeze `blocked` unless:

- Sparkbot proof packet from `sparkbot-lima-dry-run-boundary-proof` is received
- Arc Bot proof packet from `arc-lima-dry-run-boundary-proof` is received
- LIMA-side Sparkbot proof results audit passes
- LIMA-side Arc Bot proof results audit passes
- both audits pass as `pass_for_dry_run_dependency_proof`
- no redaction blockers remain
- no missing evidence blockers remain
- no forbidden import blockers remain
- no runtime boundary blockers remain
- no consumer repo boundary blockers remain
- no production/live-readiness claim blockers remain
- a compatibility freeze branch is separately designed and audited

## Implementation Branch Boundary

The later implementation branch may only add fixture-backed static tests and an implementation audit for the closeout package.

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

`audit-lima-consumer-proof-readiness-closeout-package-static-tests`

After that audit passes:

`implement-lima-consumer-proof-readiness-closeout-package-static-tests`
