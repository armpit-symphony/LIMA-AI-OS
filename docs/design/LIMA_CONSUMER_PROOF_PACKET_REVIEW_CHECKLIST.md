# LIMA Consumer Proof Packet Review Checklist

## Checklist Status

This checklist is for future LIMA-side human review of Sparkbot and Arc Bot consumer-owned dry-run proof packets.

It is docs-only. It does not audit real consumer proof packets, modify Sparkbot repositories, modify Arc Bot repositories, modify public release repositories, modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, create runtime behavior, wire shells, automate proof intake, call models, execute tools, access connectors, persist events, run schedulers, use browser/file/process/network APIs, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve production integration.

## Purpose

Use this checklist when the Sparkbot or Arc Bot repo team supplies a consumer-owned dry-run proof packet.

The checklist turns the proof results audit template into a step-by-step review flow so a LIMA reviewer can classify a packet consistently before any compatibility freeze is considered.

## Entry Conditions

Do not start review unless all are true:

- the user has supplied a proof packet or proof packet location
- the packet is from a consumer-owned branch
- Sparkbot branch is `sparkbot-lima-dry-run-boundary-proof` or Arc branch is `arc-lima-dry-run-boundary-proof`
- the packet is intended for dry-run proof only
- no request asks LIMA to modify the consumer repo
- no request asks LIMA to fetch, clone, scan, or inspect a consumer repo without explicit approval
- no request asks LIMA to run production routes, model calls, tool calls, connectors, storage, schedulers, live discovery, Robo-OS, devices, robots, drones, or physical-world behavior

If these are not true, stop and use `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`.

## Step 1: Intake Identity

Confirm the packet identifies:

- consumer repo
- consumer branch
- consumer team owner
- proof packet location
- LIMA repository URL
- LIMA commit or package version reviewed
- package name
- package version
- import method
- proof author or reviewer

If missing, classify as:

`needs_missing_evidence`

## Step 2: Redaction Gate

Before archiving or detailed review, check for:

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

If any appear, stop and classify as:

`needs_redaction_before_review`

Do not archive unredacted evidence.

## Step 3: Public API Import Review

Allowed proof-public imports:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Imports requiring follow-up:

- any `dry_run_candidate` import from `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`

Forbidden consumer imports:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

If forbidden imports appear, classify as:

`blocked_by_consumer_repo_boundary`

If unreviewed `dry_run_candidate` imports appear, classify as:

`requires_lima_design_followup`

## Step 4: Normalized Metadata Review

Confirm the packet shows:

- already-normalized intent or task metadata
- redacted shell identity
- redacted actor identity
- redacted session identity
- source surface metadata
- context refs only
- no raw natural-language parser in LIMA
- no raw prompt or raw office-task text sent to LIMA

If missing, classify as:

`needs_missing_evidence`

If raw input was sent to LIMA, classify as:

`blocked_by_runtime_boundary`

## Step 5: Capability Profile Review

Confirm a default-deny capability profile is present.

Expected disabled capabilities include:

- `model_calls`
- `memory_write`
- `task_state_write`
- `connector_read`
- `connector_write`
- `external_send`
- `file_write`
- `process_execute`
- `browser_control`
- `device_control`
- `robotics_actuation`
- `drone_actuation`
- `scheduler_run`
- `connection_attempt`
- `device_pairing`
- `credential_use`
- `physical_world_actuation`

If a capability is enabled, the packet must explain why it remains dry-run, synthetic, inert, and non-executing.

If capability evidence is missing, classify as:

`needs_missing_evidence`

If enabled capabilities imply execution or side effects, classify as:

`blocked_by_runtime_boundary`

## Step 6: Kernel Call Review

Confirm the packet shows:

- explicit `LimaKernel.evaluate(...)` call
- dry-run request
- redacted request evidence
- redacted `ExecutionResult` evidence
- no hidden adapter dispatch
- no runtime `IntentEnvelope` creation
- no real `GuardianDecision` authority
- no approval enforcement

Allowed result states:

- `proposed`
- `approval_required`
- `blocked`

If result evidence claims execution, dispatch, persistence, approval enforcement, model calls, connector access, device access, or physical-world behavior, classify as:

`blocked_by_runtime_boundary`

## Step 7: Optional Simulated Discovery Review

Complete this only if `SimulatedDiscoveryAdapter` is used.

Confirm:

- explicit adapter usage
- `dry_run is True`
- `simulated_only is True`
- synthetic surfaces only
- inert surfaces only
- surfaces are not connectable
- surfaces are not controllable
- live discovery executed is False
- scan occurred is False
- connection attempted is False
- pairing attempted is False
- credentials used is False
- session opened is False
- device control executed is False
- physical-world behavior occurred is False

If live discovery, scanning, connection, pairing, credential use, session opening, device access, Robo-OS access, robotics, drones, or physical-world behavior appears, classify as:

`blocked_by_runtime_boundary`

## Step 8: Non-Execution Invariant Review

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

Missing invariant evidence:

`needs_missing_evidence`

Contradictory invariant evidence:

`blocked_by_runtime_boundary`

## Step 9: Sparkbot-Specific Review

For Sparkbot packets, confirm:

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

If missing, classify as:

`needs_missing_evidence`

If contradicted, classify as:

`blocked_by_consumer_repo_boundary`

## Step 10: Arc Bot-Specific Review

For Arc Bot packets, confirm:

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

If missing, classify as:

`needs_missing_evidence`

If contradicted, classify as:

`blocked_by_consumer_repo_boundary`

## Step 11: Claim Boundary Review

The packet must not claim:

- production readiness
- live integration readiness
- model-call readiness
- tool-execution readiness
- connector readiness
- live discovery readiness
- device-control readiness
- Robo-OS readiness
- physical-world readiness
- compatibility freeze

If forbidden claims appear, classify as:

`blocked_by_claim_boundary`

## Step 12: Final Packet Status

Allowed statuses:

- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

Forbidden statuses:

- `approved_for_production`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_live_discovery`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_physical_world`

The only passing status is:

`pass_for_dry_run_dependency_proof`

That status does not mean production readiness.

## Step 13: Next Branch Decision

If both Sparkbot and Arc packets pass:

`design-lima-dry-run-consumer-compatibility-freeze`

If one packet passes and one is missing:

`revise-consumer-proof-evidence`

If redaction is missing:

`revise-consumer-proof-evidence`

If forbidden runtime behavior appears:

`design-lima-runtime-blocker-resolution`

If forbidden production claims appear:

`audit-production-readiness-blockers`

If consumer teams request API changes:

`design-lima-consumer-api-gap-response`

## Forbidden Reviewer Actions

The reviewer must not:

- modify consumer repos
- create or push consumer proof branches
- fetch, clone, scan, or inspect consumer repos without explicit approval
- automate proof intake
- archive unredacted evidence
- call models
- execute tools
- access connectors
- persist events
- run schedulers
- perform browser/file/process/network actions
- perform live discovery
- connect to devices
- pair devices
- use credentials
- invoke Robo-OS
- control devices, robots, drones, or physical-world systems

## Recommended Next Branch

If this checklist is accepted:

`audit-lima-consumer-proof-packet-review-checklist`

If proof packets are supplied first:

`audit-consumer-owned-proof-results`
