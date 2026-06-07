# LIMA Consumer Proof Handoff Package

## Package Status

This is the archive-ready LIMA-local handoff package index for Sparkbot and Arc Bot consumer-owned dry-run proof work.

It is docs-only. It does not audit real consumer proof packets, modify Sparkbot repositories, modify Arc Bot repositories, modify public release repositories, modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, create runtime behavior, wire shells, automate proof intake, call models, execute tools, access connectors, persist events, run schedulers, use browser/file/process/network APIs, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

This package does not approve production integration.

## Handoff Verdict

`ready_for_consumer_owned_dry_run_proof_handoff_only`

LIMA may hand this package to Sparkbot and Arc Bot repo teams through the operator so those teams can prepare their own proof branches and proof packets.

LIMA is not ready for:

- dry-run consumer compatibility freeze
- production Sparkbot integration
- Arc Bot integration
- consumer repo modifications from this LIMA lane
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real Guardian decision authority
- approval enforcement
- provider/model calls
- tool execution
- connector access
- storage/persistence
- scheduler/background work
- live discovery
- connection attempts
- pairing
- credential use
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Consumer-Owned Branches

Sparkbot team branch:

`sparkbot-lima-dry-run-boundary-proof`

Arc Bot team branch:

`arc-lima-dry-run-boundary-proof`

These branches must be created and owned by the consumer repo teams.

The LIMA repo lane must not create, edit, push, fetch, clone, scan, or inspect those branches unless the user supplies approved proof artifacts or explicitly instructs a read-only reference review.

## Package Contents

Archive and deliver these LIMA-local artifacts:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITES.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT.md`
- `tests/fixtures/dry_run_consumer_compatibility_freeze_input_matrix/freeze_input_matrix.json`
- `tests/test_lima_dry_run_consumer_compatibility_freeze_input_matrix.py`

Supporting audits to archive with the package:

- `docs/audits/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_DELIVERY_NOTE_FINAL_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE_IMPLEMENTATION_FINAL_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE_AUDIT.md`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITES_READINESS_REVIEW.md`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX_AUDIT.md`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX_STATIC_TESTS_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_AUDIT.md`

## Required Delivery Warning

Use this warning when delivering the package:

```text
This is a proof-only LIMA handoff package.
Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads, provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, devices, Robo-OS, or physical-world systems.
The first proof is normalized metadata in and dry-run ExecutionResult out.
```

## Proof Shape For Consumer Teams

The allowed proof shape is:

```text
consumer-owned branch
already-normalized redacted metadata in
default-deny capability profile
LimaKernel.evaluate(...) dry-run call
optional explicit SimulatedDiscoveryAdapter for synthetic preview only
dry-run ExecutionResult out
archive proof packet
stop at repo-team audit
```

Consumer teams must not use this package as permission to wire production routes, run live integrations, access connectors, invoke models, execute tools, persist data, schedule work, scan networks, connect to devices, use credentials, invoke Robo-OS, or touch physical-world systems.

## Required Proof Packet Evidence

Each consumer proof packet must include:

- consumer repo
- consumer branch
- consumer team owner
- exact LIMA repository URL
- exact LIMA commit or package version
- package name
- package version
- import method
- public imports used
- proof archive location
- redacted already-normalized metadata
- default-deny capability profile
- explicit `LimaKernel.evaluate(...)` call
- dry-run `ExecutionResult` evidence
- optional explicit simulated discovery evidence if used
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
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Arc Bot Evidence Requirements

Arc Bot proof packet must show:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA
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

Consumer proof branches must not rely on:

- top-level runtime re-exports such as `from lima import LimaKernel`
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

If any of these appear, the packet must be classified as `needs_redaction`.

## LIMA Intake Response Path

When a consumer team returns a packet or question:

1. Do not ingest it automatically.
2. Check for redaction issues before archiving.
3. If redaction is unsafe, respond using `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`.
4. If the packet is clean, audit it using `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.
5. If both Sparkbot and Arc Bot packets pass, only then design a dry-run consumer compatibility freeze.
6. If either packet is missing or blocked, do not freeze compatibility.

## Current Freeze Status

`not_ready_for_freeze`

Current missing evidence:

- Sparkbot proof packet from `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot proof packet from `arc-lima-dry-run-boundary-proof`
- LIMA-side Sparkbot proof results audit
- LIMA-side Arc Bot proof results audit
- both audits passing as `pass_for_dry_run_dependency_proof`

## Forbidden Package Claims

This package must not be described as:

- production-ready
- Sparkbot integrated
- Arc Bot integrated
- compatibility frozen
- live integration approved
- model-call ready
- tool-execution ready
- connector-ready
- storage-ready
- scheduler-ready
- live-discovery ready
- Robo-OS ready
- device-control ready
- robotics-ready
- drone-ready
- physical-world ready

## Validation Evidence To Report With Package

Latest package-preparation validation:

- `python -m compileall lima`
- `python -m pytest -q tests/test_lima_dry_run_consumer_compatibility_freeze_input_matrix.py -p no:cacheprovider`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git status --short --branch`

## Recommended Next Branch

If this package is accepted:

`audit-lima-consumer-proof-handoff-package`

If proof packets are supplied first:

`audit-consumer-owned-proof-results`
