# LIMA Dry-Run Consumer Compatibility Freeze Input Matrix

## Design Status

This matrix defines the human-reviewed input inventory required before LIMA can design a dry-run consumer compatibility freeze for Sparkbot and Arc Bot.

It is design-only. It does not audit real consumer proof packets, modify Sparkbot repositories, modify Arc Bot repositories, modify public release repositories, modify `lima/`, modify `pyproject.toml`, change package metadata, change public exports, create runtime behavior, wire shells, automate intake, call models, execute tools, access connectors, persist events, run schedulers, use browser/file/process/network APIs, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

This matrix does not approve production integration.

## Purpose

The freeze prerequisites document defines when a future dry-run consumer compatibility freeze may be designed. This input matrix makes those prerequisites operational by listing:

- each required input
- owner
- source artifact
- expected evidence
- current status
- blocker status
- required LIMA response

The matrix is intentionally static and human-reviewed. It must not become an automated proof intake system without a separate design, audit, and explicit implementation approval.

## Current Matrix Verdict

`not_ready_for_freeze`

Reason:

- Sparkbot consumer-owned dry-run proof packet is not present in this LIMA branch.
- Arc Bot consumer-owned dry-run proof packet is not present in this LIMA branch.
- LIMA-side audit reports for those proof packets do not exist yet.
- No evidence proves that both consumer proof packets passed `pass_for_dry_run_dependency_proof`.

The correct next LIMA action remains waiting for consumer-owned proof packets or preparing human-reviewed intake materials. It is not a compatibility freeze.

## Authoritative References

This matrix is derived from:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITES.md`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITES_READINESS_REVIEW.md`

## Status Values

Allowed input status values:

- `present`
- `missing`
- `needs_redaction`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `accepted_for_dry_run_freeze_input`

Forbidden input status values:

- `production_ready`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_live_discovery`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_physical_world`

Only `accepted_for_dry_run_freeze_input` may count toward a future freeze design.

## Required Input Matrix

| Input ID | Required Input | Owner | Source Artifact | Expected Evidence | Current Status | LIMA Response |
| --- | --- | --- | --- | --- | --- | --- |
| `sparkbot_packet` | Sparkbot dry-run proof packet | Sparkbot repo team | `sparkbot-lima-dry-run-boundary-proof` | Redacted proof archive using LIMA proof template | `missing` | Wait for consumer-owned packet |
| `arc_packet` | Arc Bot dry-run proof packet | Arc Bot repo team | `arc-lima-dry-run-boundary-proof` | Redacted proof archive using LIMA proof template | `missing` | Wait for consumer-owned packet |
| `sparkbot_audit` | LIMA-side Sparkbot proof audit | LIMA reviewer | future audit report using results audit template | `pass_for_dry_run_dependency_proof` or blocker status | `missing` | Cannot create until packet exists |
| `arc_audit` | LIMA-side Arc proof audit | LIMA reviewer | future audit report using results audit template | `pass_for_dry_run_dependency_proof` or blocker status | `missing` | Cannot create until packet exists |
| `public_api_manifest` | Public API manifest | LIMA repo | `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md` | Proof-public import list and forbidden surfaces | `present` | Reference during packet audit |
| `proof_archive_template` | Proof archive template | LIMA repo | `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md` | Required packet structure | `present` | Reference during packet audit |
| `intake_response_template` | Intake response template | LIMA repo | `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md` | Human-reviewed response statuses | `present` | Reference for feedback to consumer teams |
| `results_audit_template` | Proof results audit template | LIMA repo | `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md` | Required LIMA-side audit report shape | `present` | Use for future packet audits |
| `handoff_artifact` | Consumer proof handoff artifact | LIMA repo | `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md` | Repo-team instructions and boundaries | `present` | Use as consumer-team note |
| `delivery_note` | Consumer proof delivery note | LIMA repo | `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md` | Archive-ready delivery language | `present` | Use as operator handoff note |
| `freeze_prerequisites` | Freeze prerequisites design | LIMA repo | `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITES.md` | Freeze input and blocker requirements | `present` | Reference before freeze design |
| `freeze_prereq_review` | Freeze prerequisite readiness review | LIMA repo | `docs/audits/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITES_READINESS_REVIEW.md` | PASS for prerequisite design, not freeze | `present` | Reference before freeze design |

## Sparkbot Packet Acceptance Inputs

The Sparkbot packet must include evidence for:

- consumer repo
- consumer branch
- consumer team owner
- exact LIMA repository URL
- exact LIMA commit or package version
- package name
- package version
- import method
- public imports used
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

Sparkbot-specific required evidence:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

Current Sparkbot packet status:

`missing`

## Arc Bot Packet Acceptance Inputs

The Arc Bot packet must include evidence for:

- consumer repo
- consumer branch
- consumer team owner
- exact LIMA repository URL
- exact LIMA commit or package version
- package name
- package version
- import method
- public imports used
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

Arc-specific required evidence:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

Current Arc packet status:

`missing`

## Public API Freeze Candidate Inputs

A future freeze may consider only current `proof_public` imports:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

The future freeze must not promote `dry_run_candidate` imports unless a separate design and audit explicitly approve that promotion.

The future freeze must not approve top-level runtime re-exports such as:

- `from lima import LimaKernel`

## Required Non-Execution Inputs

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

Missing invariant evidence maps to `needs_missing_evidence`.

Contradictory invariant evidence maps to `blocked_by_runtime_boundary`.

## Redaction Inputs

The matrix cannot accept a proof packet if any evidence includes:

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

If any of these appear, status must be `needs_redaction`.

## Freeze-Blocking Inputs

The future freeze must remain blocked if:

- either consumer proof packet is missing
- either LIMA-side packet audit is missing
- either packet audit lacks `pass_for_dry_run_dependency_proof`
- either packet audit has missing evidence
- either packet audit has redaction issues
- either packet audit uses forbidden imports
- either packet audit reports runtime boundary violations
- either packet audit reports production or live integration claims
- either consumer branch wires production routes
- either consumer branch invokes models, tools, connectors, storage, schedulers, browser/file/process/network APIs, live discovery, Robo-OS, devices, robots, drones, or physical-world systems through LIMA
- LIMA public API manifest changes before the freeze branch without review

## Human Review Workflow

Future human workflow:

1. Consumer team submits proof packet location and branch.
2. LIMA reviewer checks redaction before archiving.
3. LIMA reviewer audits packet using `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.
4. LIMA reviewer records packet status in this matrix model.
5. If both packets are accepted, a future freeze design branch may start.
6. If either packet is blocked, LIMA sends a human-reviewed intake response to the consumer team.

This workflow is not automated by this branch.

## Forbidden Automation

This matrix must not be used to justify:

- automatic proof packet intake
- scanning consumer repositories
- pulling public Sparkbot branches
- writing Arc Bot branches
- crawling proof archives
- opening network connections
- reading live customer systems
- parsing raw prompts
- invoking LIMA runtime behavior
- invoking models, tools, connectors, storage, or schedulers
- invoking live discovery or device APIs
- invoking Robo-OS
- controlling devices, robots, drones, or physical-world systems

## Allowed Later Matrix Implementation

A later implementation branch may add static fixture and test coverage for this matrix only if explicitly approved.

Allowed later files:

- `tests/fixtures/dry_run_consumer_compatibility_freeze_input_matrix/*.json`
- `tests/test_lima_dry_run_consumer_compatibility_freeze_input_matrix.py`
- `docs/audits/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX_IMPLEMENTATION_AUDIT.md`

The later implementation must remain static and must not inspect real consumer repositories or proof archives.

## Forbidden Later Implementation Surfaces

Forbidden later implementation surfaces:

- `lima/`
- `tests/support/`
- `pyproject.toml`
- package metadata
- public Sparkbot repository files
- Arc Bot repository files
- adapter implementation
- provider/model implementation
- storage/persistence implementation
- shell wiring
- Robo-OS wiring
- runtime behavior
- production integration
- automated intake
- model calls
- tool execution
- connector access
- scheduler/background work
- browser/file/process/network behavior
- live discovery
- scanning
- connection attempts
- pairing
- credential use or storage
- device control
- robotics
- drones
- physical-world behavior

## Recommended Next Branch

If this design is accepted:

`audit-lima-dry-run-consumer-compatibility-freeze-input-matrix`

If consumer proof packets arrive before that audit:

`audit-consumer-owned-proof-results`
