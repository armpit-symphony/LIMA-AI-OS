# LIMA Consumer Proof Public API Compatibility Freeze

## Design Status

This document defines the future public API compatibility freeze contract for Sparkbot and Arc Bot dry-run dependency
proof.

It is design-only. It does not start a compatibility freeze, receive proof packets, audit proof packets, modify
consumer repositories, modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata,
change exports, implement runtime behavior, wire shells, call models, execute tools, access connectors, persist data,
run schedulers, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control
drones, or touch physical-world systems.

Current freeze verdict:

`not_ready_for_freeze`

Reason:

- Sparkbot consumer-owned dry-run proof packet is missing.
- Arc Bot consumer-owned dry-run proof packet is missing.
- Sparkbot LIMA-side proof audit is missing.
- Arc Bot LIMA-side proof audit is missing.
- No evidence proves both proof audits passed as `pass_for_dry_run_dependency_proof`.

This design records what the freeze would mean after those inputs exist. It does not claim that the freeze exists now.

## Purpose

The future compatibility freeze will create a narrow LIMA dependency contract for Sparkbot and Arc Bot proof-stage use.

The freeze should answer:

- which proof-stage public imports are stable enough for dry-run consumer proof
- which non-execution result invariants are frozen
- which method-level dry-run candidates may be referenced as optional metadata
- which consumer proof packet audits justify the freeze
- which changes require a new compatibility review
- which claims remain forbidden after the freeze

The freeze is a dry-run dependency proof boundary only. It is not product readiness, live integration approval, or a
production API stability guarantee.

## Authoritative Source Artifacts

The future freeze must be derived from:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_PREREQUISITES.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/design/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- future Sparkbot proof packet
- future Arc Bot proof packet
- future Sparkbot LIMA-side proof audit
- future Arc Bot LIMA-side proof audit

If this freeze contract conflicts with any stricter source artifact, the stricter artifact controls.

## Freeze Entry Requirements

A future freeze may start only when all of these are true:

- Sparkbot proof packet exists from `sparkbot-lima-dry-run-boundary-proof`.
- Arc Bot proof packet exists from `arc-lima-dry-run-boundary-proof`.
- Sparkbot packet passed the consumer proof acceptance gate.
- Arc Bot packet passed the consumer proof acceptance gate.
- Sparkbot packet passed redaction review.
- Arc Bot packet passed redaction review.
- Sparkbot LIMA-side proof audit exists.
- Arc Bot LIMA-side proof audit exists.
- Both proof audits use `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.
- Both proof audits return `pass_for_dry_run_dependency_proof`.
- Neither audit reports missing evidence.
- Neither audit reports forbidden imports.
- Neither audit reports runtime boundary violations.
- Neither audit reports consumer repo boundary violations.
- Neither audit reports production, live integration, model/tool/connector, Robo-OS, device, robotics, drone, or
  physical-world readiness claims.
- The public API manifest has not drifted since the proof audits, or drift has been separately reviewed.

If any requirement is missing, stale, contradictory, or unredacted, freeze status must remain:

`not_ready_for_freeze`

## Frozen Proof-Public Import Set

The future freeze may cover only current proof-public imports:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

The freeze must not approve top-level runtime re-exports such as:

- `from lima import LimaKernel`

The freeze must not promote `dry_run_candidate` imports without a separate design and audit.

## Method-Level Dry-Run Candidate Handling

The public API manifest currently records these method-level dry-run candidates on proof-public `LimaKernel`:

- `LimaKernel.preview_guardian_lifecycle(...)`
- `LimaKernel.preview_guardian_decision_authority(...)`

The future freeze may reference these only as optional non-authoritative metadata surfaces.

The freeze must not:

- make either method required consumer proof evidence
- export preview result dataclasses
- treat preview metadata as real Guardian authority
- treat preview metadata as approval enforcement
- treat preview metadata as execution permission

Result dataclasses remain internal unless a separate public API promotion design and audit approve otherwise.

## Frozen Dry-Run Behavior

The future freeze may cover only:

- package import proof
- proof-public `lima.kernel` imports
- construction of already-normalized dry-run metadata
- `LimaKernel.evaluate(...)` dry-run calls
- result statuses `proposed`, `approval_required`, and `blocked`
- redacted in-memory/result-local event metadata
- explicit `SimulatedDiscoveryAdapter` use for synthetic, inert, simulated-only requests
- optional method-level Guardian lifecycle and decision-authority previews as non-authoritative metadata
- non-execution invariant fields listed below

The freeze must not cover:

- raw natural-language parsing
- live HumanInput ingestion
- runtime `IntentEnvelope` authority creation
- real `GuardianDecision` authority
- approval enforcement
- provider/model calls
- tool execution
- connector access
- memory or task-state writes
- storage or event-spine persistence
- scheduler/background work
- browser/file/process/network actions
- live discovery/scanning
- connection attempts
- pairing
- credential use or storage
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Frozen Non-Execution Invariants

Every frozen proof-stage result must preserve:

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

Missing or contradictory invariant evidence blocks the freeze.

## Consumer Proof Evidence Required

Sparkbot proof evidence must show:

- exact LIMA commit or package version
- package name and version
- proof-public imports only
- redacted already-normalized Sparkbot metadata
- default-deny capability profile
- explicit `LimaKernel.evaluate(...)` dry-run call
- optional explicit synthetic `SimulatedDiscoveryAdapter` use only
- optional method-level preview evidence only
- no raw chat text sent to LIMA
- no public Sparkbot production route wired
- no Sparkbot task, message, connector, tool, provider, memory, storage, scheduler, external-send, browser, file,
  process, network, Robo-OS, device, robot, drone, or physical-world behavior invoked through LIMA
- complete non-execution invariant evidence

Arc Bot proof evidence must show:

- exact LIMA commit or package version
- package name and version
- proof-public imports only
- redacted already-normalized office-task metadata
- default-deny capability profile
- explicit `LimaKernel.evaluate(...)` dry-run call
- optional explicit synthetic `SimulatedDiscoveryAdapter` use only
- optional method-level preview evidence only
- no raw office-task text, customer record payload, connector payload, credential, provider payload, or tool payload sent
  to LIMA
- no Arc production route wired
- no Arc task, project, note, form, record, customer file, connector, tool, provider, memory, storage, scheduler,
  office-system adapter, external-send, browser, file, process, network, Robo-OS, device, robot, drone, or physical-world
  behavior invoked through LIMA
- complete non-execution invariant evidence

## Redaction Freeze Gate

The freeze must block if any proof evidence contains:

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

Unredacted evidence must not be archived as freeze evidence.

## Change-Control Rules

After a future freeze exists, a new compatibility review is required before:

- removing or renaming any frozen proof-public import
- changing package name, package version, or Python requirement used by proof branches
- changing `LimaKernel.evaluate(...)` dry-run result status semantics
- removing required non-execution invariant fields
- changing invariant defaults
- promoting any `dry_run_candidate` import
- promoting method-level preview result dataclasses
- adding top-level runtime exports
- adding hidden dispatch, registry behavior, dynamic plugin loading, or adapter auto-loading
- adding model calls, tool execution, connector access, storage, persistence, live discovery, connection, pairing,
  credential use, Robo-OS access, device control, robotics, drones, or physical-world behavior to the proof path

## Rollback And Unfreeze Rules

The future freeze must be revoked or reopened if:

- consumer proof evidence is later found to be unredacted
- consumer proof used forbidden imports
- consumer proof wired production routes
- consumer proof invoked runtime, live, model, tool, connector, storage, scheduler, live discovery, Robo-OS, device,
  robot, drone, or physical-world behavior through LIMA
- LIMA breaks frozen proof-public imports
- LIMA weakens required non-execution invariants
- LIMA introduces hidden dispatch, adapter auto-loading, live discovery, model calls, tool execution, connector access,
  persistence, or physical-world behavior into the proof path

## Forbidden Claims

The future freeze must not be described as:

- production-ready
- Sparkbot integrated
- Arc Bot integrated
- public Sparkbot release ready
- product-use ready
- live HumanInput ready
- raw natural-language execution ready
- real GuardianDecision ready
- approval enforcement ready
- model/provider routing ready
- tool execution ready
- connector ready
- storage ready
- event spine persistence ready
- live discovery ready
- connection/pairing ready
- Robo-OS ready
- device/robot/drone/physical-world ready

## Future Implementation Boundary

A later implementation or static-test branch may add only:

- static fixture metadata for the freeze contract
- static tests that check required references, import lists, invariants, blockers, and forbidden claims
- an implementation audit report

It must not modify:

- `lima/`
- `tests/support/`
- `pyproject.toml`
- package metadata
- public Sparkbot repository files
- Arc Bot repository files
- runtime behavior
- provider/model code
- adapter implementation
- storage/persistence code
- shell wiring
- Robo-OS wiring

## Current Readiness Decision

Current status remains:

`not_ready_for_freeze`

This design is ready for independent audit, not implementation and not product use.

## Recommended Next Branch

`audit-lima-consumer-proof-public-api-compatibility-freeze`
