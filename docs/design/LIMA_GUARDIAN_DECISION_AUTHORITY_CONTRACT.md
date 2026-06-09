# LIMA Guardian Decision Authority Contract

## Purpose

This document defines the future Guardian decision authority boundary for LIMA Runtime.

The goal is to make the next product-critical boundary explicit before implementation: `GuardianDecision` is the first
object that may later carry authority, but this branch does not create it, enforce it, persist it, approve execution, or
dispatch work.

This branch is design-only. It does not modify `lima/`, tests, package metadata, public exports, Sparkbot, Arc Bot,
providers, adapters, storage, persistence, HumanInput, shell wiring, live discovery, Robo-OS, devices, robotics, drones,
or physical-world behavior.

## Current Baseline

Current LIMA source-backed behavior:

- `LimaKernel.evaluate(...)` accepts already-normalized metadata and returns dry-run `ExecutionResult` objects.
- `LimaKernel.preview_guardian_lifecycle(...)` returns non-authoritative lifecycle preview metadata.
- `GuardianStubDecision` is non-authoritative.
- `GuardianLifecyclePreviewResult.guardian_decision_created` remains `False`.
- `GuardianLifecyclePreviewResult.approval_enforced` remains `False`.
- events are redacted and in-memory/result-local only.
- `SimulatedDiscoveryAdapter` is explicit, deterministic, synthetic, inert, and dry-run only.

Current public API posture:

- `from lima.kernel import LimaKernel` is proof-public.
- `LimaKernel.preview_guardian_lifecycle(...)` is a `method_level_dry_run_candidate`.
- lifecycle preview result dataclasses are not proof-public imports.
- top-level `lima` does not export runtime APIs.

## Authority Definition

A future `GuardianDecision` is an authority record only if all of these are true:

- it is created by an approved Guardian decision service
- it is bound to one `GuardianRequest`
- it is bound to one normalized intent or intent candidate
- it has a scoped action category
- it has explicit status
- it has explicit constraints
- it has policy version/provenance
- it has expiry or revocation semantics
- it is redacted for audit output
- it is separately checked by an approved execution boundary before any side effect

Anything else is not authority.

Non-authority objects include:

- `KernelRequest`
- normalized shell metadata
- `IntentEnvelope` candidate
- `GuardianRequest`
- `GuardianStubDecision`
- `GuardianLifecyclePreviewResult`
- `ApprovalMetadata`
- redacted event metadata
- proof packet evidence
- compatibility freeze metadata

These objects may inform a decision later. They must not authorize execution.

## Future Decision Object Shape

A future authority object may be shaped as:

```text
GuardianDecision
  decision_id
  guardian_request_id
  intent_id
  request_id
  actor_id
  shell_id
  session_id
  tenant_ref
  action_category
  requested_capability
  decision_status
  consequence_class
  risk_class
  allowed_tool_packs
  denied_tool_packs
  constraints
  approval_requirement
  approval_ref
  policy_version
  policy_refs
  evidence_refs
  redacted_summary
  created_at
  expires_at
  revoked_at
  supersedes_decision_id
  dry_run
```

The first implementation must not expose this as execution authority. The first implementation lane should be
non-executing metadata only unless a later audited branch explicitly approves authority creation.

## Decision Status Contract

Allowed future statuses:

- `approved`
- `denied`
- `blocked`
- `needs_clarification`
- `needs_human_confirmation`
- `needs_operator_pin`
- `needs_breakglass`
- `escalated`
- `expired`
- `revoked`
- `superseded`

Execution may never be inferred from status alone.

Only a non-expired, non-revoked, non-superseded `approved` decision with matching scope, matching capability profile,
matching approval evidence when required, and a separately approved execution boundary may later become eligible for
execution.

Denied, blocked, escalated, expired, revoked, and superseded decisions are audit records only.

Unknown status must block.

## Authority Scope Rules

Every future decision must be scoped by:

- actor
- shell
- session
- tenant/workspace where applicable
- action category
- requested capability
- target reference where applicable
- allowed tool packs or driver packs
- risk/consequence class
- expiry/revocation window
- approval requirement

Scope may only narrow downstream. It must never widen downstream.

Examples:

- a decision for `connector_read` must not permit `connector_write`
- a decision for `external_send` must not permit file writes or process execution
- a decision for simulated discovery must not permit live discovery
- a decision for one actor/session must not authorize another actor/session
- a decision for planning text must not authorize model calls, tools, connectors, files, browsers, devices, or sends
- a decision for a dry-run path must not authorize live execution

## Approval Relationship

Approval is separate from Guardian decision authority.

Future `ApprovalMetadata` may only be evidence that a human/operator approval step occurred. It is not:

- a decision
- a policy result
- a tool token
- an execution credential
- a replacement for Guardian

Approval evidence must bind to a scoped decision and must not widen that decision.

Approval enforcement is not implemented in this branch.

## Fail-Closed Rules

Future authority handling must block when:

- no decision exists for an execution-seeking action
- decision is missing required identity fields
- decision is missing request or intent binding
- decision status is unknown
- decision status is not eligible
- decision is expired
- decision is revoked
- decision is superseded
- decision scope does not match the requested action
- decision capability does not match the requested capability
- decision target does not match the requested target
- requested tool pack or driver pack is outside decision scope
- capability profile disables the requested action
- approval is required but absent
- approval evidence is stale, revoked, mismatched, or overbroad
- event/audit metadata contains raw sensitive data
- request contains approval-bypass wording
- request attempts owner/admin/operator override without policy support
- request asks to execute, dispatch, persist, send, connect, pair, scan, mutate, or actuate through an unapproved lane
- downstream behavior would call models, tools, connectors, storage, schedulers, browsers, files, processes, networks,
  devices, Robo-OS, robots, drones, or physical-world systems without a separately approved execution boundary

Unknown must block.

## Non-Execution Invariants

This contract does not change the current required proof invariants:

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
- `guardian_decision_created is False` unless a later audited implementation explicitly creates non-executing decision
  records
- `approval_enforced is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `robo_os_wiring_active is False`
- `adapter_active is False`
- `tool_execution_allowed is False`
- `driver_execution_allowed is False`
- `scheduler_active is False`
- `external_calls_allowed is False`

If a later non-executing implementation creates decision-shaped records, it must not change execution invariants.

## Event And Redaction Contract

Future decision-authority events may include:

- `guardian_decision_requested`
- `guardian_decision_prepared`
- `guardian_decision_blocked`
- `guardian_decision_denied`
- `guardian_decision_approval_required`
- `guardian_decision_expired`
- `guardian_decision_revoked`
- `guardian_decision_scope_mismatch`

This branch implements none of these events.

Future event metadata must not contain:

- raw prompts
- raw chat text
- raw office-task text
- raw customer records
- raw provider payloads
- raw tool arguments
- raw connector records
- credentials
- headers
- cookies
- tokens
- passwords
- API keys
- pairing codes
- unsafe command payloads
- live scan dumps
- private SSIDs
- raw Bluetooth MACs
- raw IP or MAC addresses
- raw serial numbers
- precise physical location
- robot/drone command payloads
- physical-world actuator payloads

Durable persistence requires a separate storage/spine contract and audit.

## Sparkbot Boundary

Sparkbot remains a consumer shell, not a LIMA implementation source in this branch.

Sparkbot must continue to own:

- raw chat handling
- redaction before LIMA
- local actor/session/source-surface metadata
- consumer-owned proof packet generation
- production route decisions
- public release changes

LIMA must not:

- touch the public Sparkbot repo
- wire Sparkbot routes
- call Sparkbot models, tools, connectors, memory, storage, scheduler, browser, file, process, network, or sends
- treat Sparkbot proof packets as production integration approval

## Arc Bot Boundary

Arc Bot / LIMA Office remains a consumer shell, not a LIMA implementation source in this branch.

Arc must continue to own:

- raw office-task handling
- customer-data redaction before LIMA
- tenant/actor/session/source-surface metadata
- consumer-owned proof packet generation
- office workflow integration decisions

LIMA must not:

- touch Arc Bot repos
- wire Arc routes
- call Arc office-system adapters
- mutate customer records, tasks, notes, forms, or files
- trigger Arc schedulers/workers
- send customer communications
- treat Arc proof packets as production integration approval

## Robo-OS And Physical-World Boundary

Robo-OS is a future gated driver plane.

This contract does not authorize:

- Robo-OS access
- device control
- robotics actuation
- drone actuation
- physical-world behavior
- live discovery
- connection attempts
- pairing
- credential use

Any future physical-world decision must require stricter policy, simulation/dry-run semantics, explicit HumanInput
approval, emergency stop handling, telemetry, and a separately audited driver execution boundary.

## Future Implementation Lane

If this design passes audit, the next possible implementation-shaped lane may be:

`implement-lima-guardian-decision-authority-preview`

That branch may only:

- add non-executing decision-authority preview metadata or dataclasses
- classify whether a future `GuardianDecision` would be required
- identify missing/invalid authority blockers
- preserve `guardian_decision_created is False` unless explicitly approved as non-authoritative preview metadata
- keep approval enforcement absent
- keep dispatch and persistence absent
- return dry-run-only result metadata
- add focused tests for fail-closed status/scope/approval mismatch behavior

That branch must not:

- create real `GuardianDecision` authority
- enforce approval
- approve execution
- dispatch work
- persist events
- call models
- execute tools
- access connectors
- wire Sparkbot
- wire Arc Bot
- wire Robo-OS
- touch browser/file/process/network surfaces
- perform live discovery, connection, pairing, credential use, device control, robotics, drones, or physical-world behavior

## Recommended Next Branch

`audit-lima-guardian-decision-authority-contract`
