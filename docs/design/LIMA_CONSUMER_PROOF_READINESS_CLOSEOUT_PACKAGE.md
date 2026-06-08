# LIMA Consumer Proof Readiness Closeout Package

## Package Status

This document designs the current LIMA-local readiness closeout package for Sparkbot and Arc Bot consumer-owned dry-run proof work.

It is docs-only. It does not create proof packets, receive proof packets, archive evidence, update the receipt ledger, audit real proof results, inspect consumer repositories, modify consumer repositories, create consumer branches, modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, implement intake automation, implement storage, implement runtime behavior, wire shells, call models, execute tools, access connectors, run schedulers, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve production integration.

## Purpose

The closeout package is the operator-facing index of all LIMA-local materials that are ready to give Sparkbot and Arc Bot teams before they create their own proof packets.

It has three jobs:

- consolidate the current package, readiness closeout, intake ledger closeout, public API, templates, and audits into one package index
- keep the current state explicit: LIMA is ready for consumer-owned dry-run proof handoff only
- prevent the handoff package from being mistaken for Sparkbot readiness, Arc Bot readiness, compatibility freeze, product readiness, live integration, or runtime expansion

## Current Package Verdict

`ready_for_consumer_owned_dry_run_proof_handoff_only`

Meaning:

- LIMA can hand proof-only instructions and templates to Sparkbot and Arc Bot repo teams through the operator.
- Sparkbot proof packet is still `not_received`.
- Arc Bot proof packet is still `not_received`.
- Sparkbot proof audit is still `not_started`.
- Arc Bot proof audit is still `not_started`.
- compatibility freeze remains `blocked`.
- product readiness remains `not_production_ready`.

## Latest LIMA-Local Reference Commit

Use this LIMA commit as the current LIMA-local closeout package reference unless a later audited branch supersedes it:

`d9228cebf72289b18cd8c7887ff44363878c8887`

That commit is the independent audit of the fixture-backed Sparkbot / Arc proof-packet intake ledger closeout static tests.

This commit is not proof that Sparkbot or Arc Bot can use LIMA. It is only the latest audited LIMA-local preparation checkpoint.

## Relationship To Existing Artifacts

This package is an index and delivery wrapper. It does not replace the source artifacts.

Use these source artifacts:

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

If this package conflicts with a source artifact, the stricter source artifact controls.

## Required Package Contents

The operator-facing package should include these LIMA-local documents:

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

The package should include these LIMA-local audit and static-test evidence references:

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

## Current Evidence State

The package must report:

| Evidence Area | Current Status | Meaning |
| --- | --- | --- |
| Sparkbot proof packet | `not_received` | Sparkbot repo team has not supplied a redacted packet |
| Arc Bot proof packet | `not_received` | Arc Bot / LIMA Office repo team has not supplied a redacted packet |
| Sparkbot redaction review | `not_started` | cannot begin until packet exists |
| Arc Bot redaction review | `not_started` | cannot begin until packet exists |
| Sparkbot proof audit | `not_started` | cannot begin until packet passes redaction |
| Arc Bot proof audit | `not_started` | cannot begin until packet passes redaction |
| Compatibility freeze | `blocked` | both proof audits must pass first |
| Product readiness | `not_production_ready` | live/product lanes remain out of scope |

## Consumer-Owned Branches

Sparkbot team branch:

`sparkbot-lima-dry-run-boundary-proof`

Arc Bot / LIMA Office team branch:

`arc-lima-dry-run-boundary-proof`

These branches must be created and owned by consumer repo teams.

The LIMA repo lane must not create, edit, push, fetch, clone, scan, or inspect those branches unless the user supplies approved proof artifacts or explicitly instructs a read-only reference review.

## Delivery Warning

Use this warning when handing the package to consumer teams:

```text
This is a proof-only LIMA handoff package.
Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads, provider payloads, tool arguments, live scan dumps, device identifiers, physical location, robot payloads, drone payloads, or physical-world command payloads to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, browsers, files, processes, networks, devices, Robo-OS, robots, drones, or physical-world systems.
The first proof is already-normalized metadata in and dry-run ExecutionResult out.
```

## Proof Shape For Consumer Teams

The only allowed proof shape is:

```text
consumer-owned branch
redacted already-normalized metadata in
default-deny capability profile
explicit LimaKernel.evaluate(...) dry-run call
optional explicit SimulatedDiscoveryAdapter for synthetic preview only
optional LimaKernel.preview_guardian_lifecycle(...) as non-authoritative metadata only
dry-run ExecutionResult out
redacted proof packet
repo-team-owned proof verdict
LIMA-side proof audit later
```

Consumer teams must not use this package as permission to wire production routes, run live integrations, access connectors, invoke models, execute tools, persist data, schedule work, scan networks, connect to devices, use credentials, invoke Robo-OS, control devices, or touch physical-world systems.

## Required Proof Packet Evidence

Each consumer proof packet must include:

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

## Sparkbot Evidence Requirements

Sparkbot proof packet must show:

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

## Arc Bot Evidence Requirements

Arc Bot proof packet must show:

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

## Proof-Public Imports

Consumer dry-run proof branches may use only:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Optional method-level dry-run candidate:

- `LimaKernel.preview_guardian_lifecycle(...)`

Consumer proof branches must not rely on:

- top-level runtime re-exports such as `from lima import LimaKernel`
- standalone lifecycle preview result dataclass imports
- unreviewed `dry_run_candidate` imports
- internal namespaces such as `lima.io.*`, `lima.persistence.*`, `lima.harness.*`, `lima.guardian.*`, `lima.spine.*`, `lima.services.*`, `lima.shells.*`, or `lima.adapters.*`

## Required Non-Execution Invariants

Every archived proof result must preserve:

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

## Redaction Boundary

Proof packets must not include:

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

If any of these appear, the packet must be classified as:

`needs_redaction_before_review`

Do not archive unredacted evidence.

## Manual Intake Path After Packets Arrive

When a consumer team returns a packet or question:

1. Do not ingest it automatically.
2. Confirm packet source and consumer-owned branch.
3. Confirm the packet is dry-run proof only.
4. Check for redaction issues before archiving.
5. If redaction is unsafe, respond using `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`.
6. If the packet is clean enough to audit, audit it using `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.
7. Audit Sparkbot and Arc Bot packets separately.
8. If either packet is missing or blocked, do not freeze compatibility.
9. If both Sparkbot and Arc Bot packets pass as `pass_for_dry_run_dependency_proof`, design a dry-run consumer compatibility freeze in a separate branch.

This package does not automate intake, redaction, archive, ledger update, response sending, or audit.

## Compatibility Freeze Status

Current freeze status:

`blocked`

Current missing evidence:

- Sparkbot proof packet from `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot proof packet from `arc-lima-dry-run-boundary-proof`
- LIMA-side Sparkbot proof results audit
- LIMA-side Arc Bot proof results audit
- both audits passing as `pass_for_dry_run_dependency_proof`
- no redaction blockers
- no missing evidence blockers
- no forbidden import blockers
- no runtime boundary blockers
- no consumer repo boundary blockers
- no production/live-readiness claim blockers

## Forbidden Package Claims

This package must not be described as:

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

## Forbidden Package Actions

This package must not trigger:

- consumer repository edits
- public Sparkbot repository changes
- Arc Bot repository changes
- creation or pushing of consumer proof branches by LIMA
- fetching, cloning, scanning, or inspecting consumer repositories without explicit approval
- automated proof intake
- proof archive crawling
- redaction scanning
- raw evidence storage
- receipt ledger persistence
- event spine persistence
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

## Validation Evidence To Report With Package

The package should report the latest validation run from this branch:

- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git status --short --branch`

## Recommended Next Branch

If this package design is accepted:

`audit-lima-consumer-proof-readiness-closeout-package`

If Sparkbot or Arc Bot proof packets are supplied first:

`audit-consumer-owned-proof-results`
