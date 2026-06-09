# LIMA Consumer Proof Packet Audit Result Gate

## Design Status

This document defines a future LIMA-local gate for interpreting Sparkbot and Arc Bot consumer-owned dry-run proof packet
audit results.

It is design-only. It does not receive proof packets, archive proof packets, audit proof packets, accept proof packets,
create proof branches, inspect consumer repositories, modify consumer repositories, modify `lima/`, modify
`tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, implement runtime behavior,
wire shells, call models, execute tools, access connectors, persist data, run schedulers, perform live discovery,
connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve product or production integration.

## Purpose

The result gate answers one narrow future question:

Given one or two completed LIMA-side proof packet audit reports, what is the combined readiness state for Sparkbot and
Arc Bot dry-run dependency proof?

This gate exists so LIMA does not accidentally treat one passing packet, a missing packet, a redaction failure, a
runtime-boundary violation, or an over-claiming consumer report as public API compatibility freeze readiness.

## Relationship To Existing Artifacts

This result gate is derived from:

- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_RESULTS_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PUBLIC_API_COMPATIBILITY_FREEZE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_RELEASE_CANDIDATE_GATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_READINESS_RELEASE_CANDIDATE_GATE_STATIC_TESTS_AUDIT.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`

If this gate conflicts with any stricter source artifact, the stricter artifact controls.

## Current State

Current state remains:

| Area | State | Meaning |
| --- | --- | --- |
| Sparkbot proof packet | `not_received` | no Sparkbot packet is available to audit |
| Arc Bot proof packet | `not_received` | no Arc Bot packet is available to audit |
| Sparkbot proof audit | `not_started` | cannot start until redacted packet exists |
| Arc Bot proof audit | `not_started` | cannot start until redacted packet exists |
| Combined result gate | `not_ready_for_result_gate` | required audit inputs are missing |
| Public API compatibility freeze | `not_ready_for_freeze` | both proof audits must pass first |
| Product readiness | `not_production_ready` | live/product lanes remain blocked |

This design does not change those states.

## Required Inputs

The result gate may evaluate only completed, redacted, LIMA-side audit reports that use
`docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.

Required Sparkbot input:

- consumer repo: Sparkbot
- consumer branch: `sparkbot-lima-dry-run-boundary-proof`
- redacted proof packet reference
- LIMA commit or package version reviewed
- package name and package version
- public API import review
- normalized metadata review
- kernel dry-run review
- optional simulated discovery review, if used
- non-execution invariant review
- redaction review
- forbidden surface review
- consumer-specific findings
- audit status

Required Arc Bot input:

- consumer repo: Arc Bot / LIMA Office
- consumer branch: `arc-lima-dry-run-boundary-proof`
- redacted proof packet reference
- LIMA commit or package version reviewed
- package name and package version
- public API import review
- normalized metadata review
- kernel dry-run review
- optional simulated discovery review, if used
- non-execution invariant review
- redaction review
- forbidden surface review
- consumer-specific findings
- audit status

Missing audit input must keep the combined result at:

`not_ready_for_result_gate`

## Forbidden Inputs

The result gate must not process:

- raw proof packets
- unredacted proof packets
- raw prompts
- raw chat text
- raw office-task text
- raw customer records
- raw attachments
- connector payloads
- provider payloads
- tool arguments
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
- raw BLE identifiers
- raw IP addresses
- raw MAC addresses
- device serial numbers
- precise physical location
- robot command payloads
- drone command payloads
- physical-world actuator payloads
- live webhooks
- production route payloads
- automated event streams

If such material appears, the only safe state is:

`needs_redaction_before_result_gate`

Unredacted evidence must not be archived.

## Allowed Input Audit Statuses

Allowed per-consumer audit statuses are inherited from the proof results audit template:

- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

The only passing per-consumer audit status is:

`pass_for_dry_run_dependency_proof`

That status does not mean production readiness.

## Combined Result States

Allowed combined result states:

- `not_ready_for_result_gate`
- `needs_redaction_before_result_gate`
- `needs_missing_consumer_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `pass_for_dry_run_dual_consumer_proof`
- `not_ready_for_implementation`

Forbidden combined result states:

- `approved_for_production`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_storage`
- `approved_for_scheduler`
- `approved_for_live_discovery`
- `approved_for_connection`
- `approved_for_pairing`
- `approved_for_credential_use`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_robotics`
- `approved_for_drones`
- `approved_for_physical_world`
- `compatibility_frozen`

## Result Mapping

The combined result gate must map inputs as follows:

| Sparkbot Audit | Arc Bot Audit | Combined Result |
| --- | --- | --- |
| missing | missing | `not_ready_for_result_gate` |
| pass | missing | `needs_missing_consumer_evidence` |
| missing | pass | `needs_missing_consumer_evidence` |
| redaction blocker | any | `needs_redaction_before_result_gate` |
| any | redaction blocker | `needs_redaction_before_result_gate` |
| missing evidence | any non-redaction | `needs_missing_consumer_evidence` |
| any non-redaction | missing evidence | `needs_missing_consumer_evidence` |
| runtime boundary block | any non-redaction | `blocked_by_runtime_boundary` |
| any non-redaction | runtime boundary block | `blocked_by_runtime_boundary` |
| consumer repo boundary block | any non-redaction/runtime | `blocked_by_consumer_repo_boundary` |
| any non-redaction/runtime | consumer repo boundary block | `blocked_by_consumer_repo_boundary` |
| claim boundary block | any non-redaction/runtime/repo | `blocked_by_claim_boundary` |
| any non-redaction/runtime/repo | claim boundary block | `blocked_by_claim_boundary` |
| design follow-up | any non-blocking | `requires_lima_design_followup` |
| any non-blocking | design follow-up | `requires_lima_design_followup` |
| audit follow-up | any non-blocking | `requires_lima_audit_followup` |
| any non-blocking | audit follow-up | `requires_lima_audit_followup` |
| pass | pass | `pass_for_dry_run_dual_consumer_proof` |

Redaction blockers outrank all other statuses. Runtime boundary blockers outrank consumer repo, claim, design, and audit
follow-up statuses.

## Pass Criteria

The combined result may be:

`pass_for_dry_run_dual_consumer_proof`

only when all are true:

- Sparkbot LIMA-side proof audit exists
- Arc Bot LIMA-side proof audit exists
- both audits used `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- both audits reviewed the same LIMA commit or an explicitly compatible package version
- both audits reviewed only redacted evidence
- both audits status `pass_for_dry_run_dependency_proof`
- both audits confirm proof-public imports only
- both audits confirm already-normalized metadata only
- both audits confirm explicit `LimaKernel.evaluate(...)` dry-run call
- both audits confirm optional simulated discovery was explicit, synthetic, inert, and dry-run only, if used
- both audits confirm all non-execution invariants
- both audits confirm no forbidden Sparkbot or Arc repo boundary behavior
- both audits confirm no production, live integration, model/tool/connector/storage/scheduler, live discovery,
  connection, pairing, credential, Robo-OS, device, robotics, drone, or physical-world readiness claims

This pass state means only that LIMA may design a dry-run public API compatibility freeze next.

It does not approve:

- Sparkbot product integration
- Arc Bot product integration
- public Sparkbot release readiness
- live integration
- production use
- model calls
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

## Fail-Closed Rules

The result gate must fail closed when:

- either consumer audit is missing
- either packet is unredacted
- either packet is stale against the reviewed LIMA commit/version
- either packet uses forbidden imports
- either packet uses unreviewed `dry_run_candidate` imports without a design follow-up
- either packet omits required non-execution invariant evidence
- either packet contradicts non-execution invariant evidence
- either packet sends raw chat or office-task text to LIMA
- either packet wires production routes
- either packet invokes consumer tasks, messages, records, connectors, tools, providers, memory, storage, schedulers,
  office-system adapters, or external sends through LIMA
- either packet shows model calls, tool execution, connector access, persistence, scheduler/background work,
  browser/file/process/network behavior, live discovery, connection, pairing, credential use, Robo-OS access, device
  control, robotics, drones, or physical-world behavior
- either packet claims product readiness, production readiness, live integration readiness, compatibility freeze, or
  public Sparkbot readiness

## Compatibility Freeze Boundary

The result gate does not start a compatibility freeze.

If the combined result is:

`pass_for_dry_run_dual_consumer_proof`

then the next branch may be:

`design-lima-dry-run-consumer-compatibility-freeze`

That future branch must still be design-only unless separately approved. It must not modify `lima/`, package metadata,
consumer repositories, runtime behavior, shell wiring, model/tool/connector/storage behavior, live discovery, Robo-OS,
devices, robotics, drones, or physical-world behavior.

If the combined result is anything else, compatibility freeze remains:

`not_ready_for_freeze`

## Output Shape

A future result gate report should include:

- branch
- base commit
- Sparkbot audit report path
- Arc Bot audit report path
- LIMA commit or package version reviewed
- package name and version
- Sparkbot audit status
- Arc Bot audit status
- redaction review
- public API import review
- non-execution invariant review
- forbidden surface review
- combined result state
- compatibility freeze readiness
- product readiness
- missing evidence
- required follow-up
- recommended next branch

## Forbidden Actions

This gate must not trigger:

- proof packet receipt
- proof packet archive
- proof packet audit
- automated intake
- response sending
- compatibility freeze
- package version bump
- public export change
- consumer repo edits
- public Sparkbot repo changes
- Arc Bot repo changes
- consumer branch creation
- consumer repo fetch, clone, scan, or inspection without explicit approval
- `lima/` modifications
- `tests/support/` modifications
- runtime behavior
- shell wiring
- model calls
- tool execution
- connector access
- storage/persistence
- event spine persistence
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

## Current Readiness Decision

Current state:

`not_ready_for_result_gate`

Reason:

- Sparkbot proof packet is missing.
- Arc Bot proof packet is missing.
- Sparkbot LIMA-side proof audit is missing.
- Arc Bot LIMA-side proof audit is missing.
- No combined result can be computed from missing inputs.

## Recommended Next Branch

`audit-lima-consumer-proof-packet-audit-result-gate`
