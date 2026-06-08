# LIMA Consumer Proof Acceptance Gate

## Gate Status

This document defines the LIMA-side acceptance gate for future Sparkbot and Arc Bot consumer-owned dry-run proof packets.

It is design-only. It does not receive proof packets, archive evidence, update ledgers, audit real proof results, inspect consumer repositories, modify consumer repositories, create consumer branches, modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, implement intake automation, implement storage, implement runtime behavior, wire shells, call models, execute tools, access connectors, run schedulers, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve production integration.

## Purpose

The acceptance gate exists so LIMA reviewers cannot accidentally treat a partial, unsafe, unredacted, or over-claiming consumer proof packet as readiness evidence.

It defines:

- entry conditions before a packet can be reviewed
- mandatory redaction gates
- public API gates
- normalized metadata gates
- dry-run kernel gates
- optional simulated discovery gates
- optional Guardian lifecycle preview gates
- consumer-specific evidence gates
- pass/fail status rules
- compatibility freeze stop conditions

## Relationship To Existing Artifacts

This gate uses these source artifacts:

- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`

If this gate conflicts with a source artifact, the stricter source artifact controls.

## Required Entry Conditions

Do not start acceptance review unless all are true:

- the user supplies a proof packet or proof packet location
- the packet is from a consumer-owned branch
- Sparkbot branch is `sparkbot-lima-dry-run-boundary-proof` or Arc branch is `arc-lima-dry-run-boundary-proof`
- the packet is explicitly dry-run proof only
- the packet names the exact LIMA commit or package version used
- the packet names the package name and package version used
- the packet includes redaction attestation
- the packet includes non-execution invariant evidence
- no request asks LIMA to modify a consumer repo
- no request asks LIMA to fetch, clone, scan, or inspect a consumer repo without explicit approval
- no request asks LIMA to run production routes, model calls, tool calls, connectors, storage, schedulers, live discovery, Robo-OS, devices, robots, drones, or physical-world behavior

If any entry condition is missing, acceptance status must be:

`not_ready_for_acceptance_review`

Recommended response:

`needs_missing_evidence`

## Redaction Gate

Before archiving or detailed proof review, reject evidence containing:

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

If any redaction blocker appears, acceptance status must be:

`rejected_redaction_blocker`

Recommended response:

`needs_redaction_before_review`

Do not archive unredacted evidence.

## Public API Gate

Consumer proof branches may use only:

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

Consumer proof branches must not import lifecycle preview result dataclasses as public API.

Consumer proof branches must not import:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

If forbidden imports appear, acceptance status must be:

`rejected_forbidden_imports`

Recommended response:

`blocked_by_consumer_repo_boundary`

If unreviewed `dry_run_candidate` imports appear, acceptance status must be:

`requires_api_followup`

Recommended response:

`requires_lima_design_followup`

## Normalized Metadata Gate

Accepted packets must prove:

- metadata was already normalized before LIMA received it
- LIMA did not parse raw natural language
- LIMA did not ingest live HumanInput
- LIMA did not receive raw chat text
- LIMA did not receive raw office-task text
- shell ID, actor ID, and session ID are redacted or synthetic
- context references are refs or summaries only
- source surface metadata is redacted

If normalized metadata evidence is missing, acceptance status must be:

`rejected_missing_normalized_metadata`

Recommended response:

`needs_missing_evidence`

If raw input was sent to LIMA, acceptance status must be:

`rejected_raw_input_boundary`

Recommended response:

`blocked_by_runtime_boundary`

## Kernel Dry-Run Gate

Accepted packets must prove:

- `LimaKernel.evaluate(...)` was called explicitly
- request metadata was dry-run
- no hidden adapter dispatch occurred
- no runtime `IntentEnvelope` authority was created
- no real `GuardianDecision` authority was created
- no approval enforcement occurred
- result status was one of `proposed`, `approval_required`, or `blocked`
- `ExecutionResult` evidence is redacted

If the result claims execution, dispatch, persistence, approval enforcement, model calls, connector access, device access, or physical-world behavior, acceptance status must be:

`rejected_runtime_boundary`

Recommended response:

`blocked_by_runtime_boundary`

## Optional Simulated Discovery Gate

Complete this gate only if the packet used `SimulatedDiscoveryAdapter`.

Accepted packets must prove:

- adapter was passed explicitly
- `dry_run is True`
- `simulated_only is True`
- discovery mode was `simulated`
- surfaces are synthetic
- surfaces are inert
- surfaces are not connectable
- surfaces are not controllable
- live discovery executed is False
- scanning occurred is False
- connection attempted is False
- pairing attempted is False
- credentials used is False
- session opened is False
- device control executed is False
- physical-world behavior occurred is False

If live discovery, scanning, connection, pairing, credential use, session opening, device access, Robo-OS access, robotics, drones, or physical-world behavior appears, acceptance status must be:

`rejected_simulated_discovery_boundary`

Recommended response:

`blocked_by_runtime_boundary`

## Optional Guardian Lifecycle Preview Gate

Complete this gate only if the packet used `LimaKernel.preview_guardian_lifecycle(...)`.

Accepted packets must prove:

- method was called through proof-public `LimaKernel`
- lifecycle preview was optional, not required for proof acceptance
- preview input was already-normalized `KernelRequest` metadata or equivalent redacted mapping
- preview output was treated as metadata only
- lifecycle preview result dataclasses were not imported as public API
- no runtime `IntentEnvelope` authority was created
- no real `GuardianDecision` authority was created
- no approval enforcement occurred
- no execution was approved
- events remained redacted and in-memory/result-local only

If lifecycle preview output is treated as real Guardian authority, acceptance status must be:

`rejected_guardian_authority_boundary`

Recommended response:

`blocked_by_runtime_boundary`

## Required Non-Execution Invariant Gate

Accepted packets must prove every invariant:

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

If invariant evidence is missing, acceptance status must be:

`rejected_missing_invariants`

Recommended response:

`needs_missing_evidence`

If invariant evidence is contradicted, acceptance status must be:

`rejected_runtime_boundary`

Recommended response:

`blocked_by_runtime_boundary`

## Sparkbot-Specific Gate

Sparkbot packet acceptance requires evidence that:

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

Missing evidence maps to:

`rejected_missing_sparkbot_evidence`

Contradictory evidence maps to:

`rejected_consumer_repo_boundary`

## Arc Bot-Specific Gate

Arc Bot packet acceptance requires evidence that:

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

Missing evidence maps to:

`rejected_missing_arc_evidence`

Contradictory evidence maps to:

`rejected_consumer_repo_boundary`

## Claim Boundary Gate

Reject packets that claim:

- production readiness
- live integration readiness
- model-call readiness
- tool-execution readiness
- connector readiness
- storage readiness
- scheduler readiness
- live discovery readiness
- connection readiness
- device-control readiness
- Robo-OS readiness
- robotics readiness
- drone readiness
- physical-world readiness
- compatibility freeze

Forbidden claims map to:

`rejected_claim_boundary`

Recommended response:

`blocked_by_claim_boundary`

## Acceptance Status Values

Allowed acceptance statuses:

- `accepted_for_dry_run_proof_audit`
- `not_ready_for_acceptance_review`
- `rejected_redaction_blocker`
- `rejected_forbidden_imports`
- `requires_api_followup`
- `rejected_missing_normalized_metadata`
- `rejected_raw_input_boundary`
- `rejected_runtime_boundary`
- `rejected_simulated_discovery_boundary`
- `rejected_guardian_authority_boundary`
- `rejected_missing_invariants`
- `rejected_missing_sparkbot_evidence`
- `rejected_missing_arc_evidence`
- `rejected_consumer_repo_boundary`
- `rejected_claim_boundary`

Forbidden acceptance statuses:

- `accepted_for_production`
- `accepted_for_live_integration`
- `accepted_for_model_calls`
- `accepted_for_tool_execution`
- `accepted_for_connector_access`
- `accepted_for_live_discovery`
- `accepted_for_device_control`
- `accepted_for_robo_os`
- `accepted_for_physical_world`
- `compatibility_frozen`

`accepted_for_dry_run_proof_audit` only means the packet is safe enough to audit using the proof results audit template. It does not mean the packet passed.

## Compatibility Freeze Rule

Do not design a dry-run compatibility freeze unless all are true:

- Sparkbot packet is accepted for audit
- Arc Bot packet is accepted for audit
- Sparkbot proof audit passes as `pass_for_dry_run_dependency_proof`
- Arc Bot proof audit passes as `pass_for_dry_run_dependency_proof`
- no redaction blockers remain
- no missing evidence blockers remain
- no forbidden import blockers remain
- no runtime boundary blockers remain
- no consumer repo boundary blockers remain
- no claim boundary blockers remain

Until then, freeze status remains:

`blocked`

## Reviewer Forbidden Actions

Reviewers must not:

- modify consumer repositories
- create or push consumer proof branches
- fetch, clone, scan, or inspect consumer repositories without explicit approval
- automate proof intake
- archive unredacted evidence
- run redaction scanners
- persist proof packet contents
- call models
- execute tools
- access connectors
- run schedulers
- perform browser/file/process/network actions
- perform live discovery
- connect to devices
- pair devices
- use credentials
- invoke Robo-OS
- control devices, robots, drones, or physical-world systems

## Recommended Next Branch

If this design is accepted:

`audit-lima-consumer-proof-acceptance-gate`

If proof packets are supplied first:

`audit-consumer-owned-proof-results`
