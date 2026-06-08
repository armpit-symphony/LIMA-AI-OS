# LIMA Guardian Request Decision Lifecycle Contract

## Purpose

This document defines the next design-only contract for moving LIMA from dry-run kernel classification toward a real Guardian-gated runtime boundary for future Sparkbot and Arc Bot use.

The contract describes how future LIMA runtime objects may relate:

```text
KernelRequest
  -> IntentEnvelope candidate
  -> GuardianRequest
  -> GuardianDecision
  -> ApprovalMetadata, if required later
  -> ExecutionResult
  -> Event or Spine record, if approved later
```

This branch is design-only. It does not implement runtime behavior, modify `lima/`, modify `tests/support/`, create a live Guardian request bridge, create real `IntentEnvelope` records, create real `GuardianDecision` authority, enforce approvals, dispatch work, persist audit events, call models, execute tools, access connectors, wire Sparkbot, wire Arc Bot, wire Robo-OS, perform discovery, connect to devices, or touch physical-world systems.

## Current Baseline

LIMA currently supports a non-executing proof surface:

- `LimaKernel.evaluate(...)` accepts already-normalized metadata.
- Results remain dry-run only.
- Safe planning/drafting/text-preview metadata may be `proposed`.
- Unknown, unsafe, disabled, consequential, connection, device, robot, drone, and physical-world categories block or require approval metadata without execution.
- `GuardianStubDecision` is non-authoritative.
- Events are redacted and in-memory only.
- `SimulatedDiscoveryAdapter` is deterministic, explicit, synthetic, inert, and dry-run only.

Current Guardian-related evidence already states:

- Guardian request is not GuardianDecision.
- Guardian request is not approval.
- Guardian request is not enforcement.
- GuardianDecision is the future mandatory authority boundary for consequential behavior.
- ApprovalMetadata is evidence, not a replacement for GuardianDecision.
- Fake GuardianDecision fixtures are test-only and non-authorizing.

## Lifecycle Objects

### KernelRequest

`KernelRequest` is the current shell-facing dry-run input shape.

It may contain:

- request ID
- shell ID
- actor ID
- session ID
- already-normalized intent metadata
- capability profile
- source surface metadata
- context refs
- optional synthetic discovery metadata

It must not contain:

- raw chat text as executable intent
- raw office-task text as executable intent
- raw prompts
- raw provider payloads
- raw tool arguments
- raw connector records
- credentials, headers, tokens, cookies, passwords, pairing codes, or secrets
- live scan dumps
- raw device identifiers
- precise physical location
- robot or drone command payloads

### IntentEnvelope Candidate

An `IntentEnvelope` candidate is future structured intent metadata derived from shell-owned normalization.

It is not:

- a command
- a tool call
- approval
- authorization
- execution permission
- persistence permission
- a real runtime record in this design branch

Future candidate fields may include:

- `intent_id`
- `request_id`
- `actor_id`
- `shell_id`
- `session_id`
- `tenant_ref`
- `source_surface`
- `intent_kind`
- `action_category`
- `requested_capability`
- `risk_class`
- `confidence`
- `summary_redacted`
- `evidence_refs`
- `context_refs`
- `requested_tool_packs`
- `redaction_policy_ref`
- `provenance`
- `candidate_state`

Allowed candidate states:

- `drafted`
- `needs_clarification`
- `ready_for_guardian_request`
- `blocked_before_guardian`

Forbidden candidate states:

- `approved`
- `authorized`
- `execution_allowed`
- `dispatch_allowed`
- `persisted`
- `sent`
- `completed`

### GuardianRequest

A `GuardianRequest` is a future request-for-review object.

It asks Guardian to classify, deny, or require approval for a scoped action. It is not a decision and grants no authority.

Future fields may include:

- `guardian_request_id`
- `intent_id`
- `request_id`
- `actor_id`
- `shell_id`
- `session_id`
- `tenant_ref`
- `action_type`
- `requested_capability`
- `requested_tool_packs`
- `target_ref`
- `risk_class`
- `consequence_class`
- `policy_context_ref`
- `trust_context_ref`
- `redaction_context_ref`
- `approval_requirement_ref`
- `evidence_refs`
- `source_surface`
- `dry_run`
- `created_at`

Required rules:

- `requested_tool_packs` are requests only.
- `requested_tool_packs` are not `allowed_tool_packs`.
- `approval_requirement_ref` is descriptive only.
- `approval_requirement_ref` is not ApprovalMetadata.
- `trust_context_ref` is context only.
- privacy/redaction metadata is not enforcement.
- Guardian request cannot create approval.
- Guardian request cannot authorize execution.

Allowed request states:

- `prepared`
- `needs_clarification`
- `ready_for_policy_review`
- `blocked_before_decision`
- `invalid`

Forbidden request states:

- `approved`
- `approval_granted`
- `execution_allowed`
- `dispatch_allowed`
- `tool_packs_granted`
- `policy_enforced`

### GuardianDecision

`GuardianDecision` is the future authority record.

This design does not implement it. It defines the boundary a later branch must preserve.

Future fields may include:

- `decision_id`
- `guardian_request_id`
- `intent_id`
- `request_id`
- `actor_id`
- `shell_id`
- `session_id`
- `action_type`
- `target_ref`
- `risk_class`
- `decision_status`
- `allowed_tool_packs`
- `constraints`
- `policy_version`
- `expires_at`
- `revoked_at`
- `supersedes_decision_id`
- `approval_requirement`
- `approval_ref`
- `evidence_refs`
- `redacted_summary`

Allowed decision statuses:

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

Only a future approved Guardian implementation may create real `GuardianDecision` authority.

Denied, blocked, escalated, expired, revoked, and superseded decisions are audit records only. They are not execution credentials.

### ApprovalMetadata

`ApprovalMetadata` is future evidence that a required human/operator approval step occurred.

It is not:

- a substitute for GuardianDecision
- a tool execution token
- proof that execution happened
- allowed to appear in this design branch as runtime behavior

Future fields may include:

- `approval_id`
- `decision_id`
- `approver_ref`
- `approval_level`
- `approval_method`
- `approved_scope`
- `constraints`
- `expires_at`
- `evidence_refs`
- `redacted_summary`

ApprovalMetadata must always attach to a scoped GuardianDecision.

## Future Flow

The future non-executing lifecycle should be:

```text
Shell creates redacted normalized metadata
KernelRequest receives metadata
Kernel validates capability profile and source surface
Kernel proposes IntentEnvelope candidate
Kernel prepares GuardianRequest
Guardian classifies request
Guardian returns denied / blocked / needs_approval / approved metadata
Kernel returns dry-run ExecutionResult
No dispatch occurs until separate execution lanes exist
```

The future executing lifecycle, not approved here, would require:

```text
GuardianDecision approved within scope
ApprovalMetadata present when required
Decision not expired, revoked, or superseded
Capability profile still permits requested category
Tool pack or driver scope still matches
Execution service separately approved
Audit/spine event writer separately approved
Rollback/disable path available
```

This branch does not approve that executing lifecycle.

## Fail-Closed Rules

Future implementation must block when:

- required identity fields are missing
- request lacks actor, shell, session, or tenant/workspace context where required
- normalized intent is missing
- raw prompt/chat/office-task text is supplied as executable intent
- source surface indicates secrets or unsafe payloads
- requested capability is disabled
- action category is unknown
- requested tool pack is unknown
- requested tool pack is not in capability profile
- risk class is missing or contradictory
- provenance is missing for consequential actions
- approval-bypass wording appears
- owner/admin/operator wording attempts to bypass Guardian
- Guardian request tries to claim decision authority
- GuardianDecision is absent for consequential execution
- GuardianDecision is expired, revoked, superseded, denied, blocked, or escalated
- ApprovalMetadata is required but absent
- ApprovalMetadata does not match decision scope
- event or audit metadata contains forbidden raw data
- downstream execution would require model, tool, connector, storage, scheduler, browser, file, process, network, device, robot, drone, or physical-world behavior not separately approved

## Risk Classes

Future Guardian lifecycle design should preserve these rough classes:

- `low`: text-only preview, planning, drafting, classification, metadata review
- `medium`: internal state proposal, task draft, limited connector-read proposal, memory-write proposal
- `high`: external communication, connector write, file write, browser action, authenticated connector action, privileged data access, expensive model/tool use
- `critical`: process execution, terminal/PTY, production systems, credential/security changes, destructive actions, payment/legal/regulatory actions, device control, Robo-OS, robotics, drones, physical-world actuation

Unknown risk must default to blocked.

## Sparkbot Boundary

Sparkbot may later supply only redacted, already-normalized metadata to LIMA.

Sparkbot must own:

- raw chat handling
- local redaction before LIMA
- shell actor/session context
- source surface classification
- proof packet creation
- production route decisions

LIMA must not:

- parse Sparkbot raw chat
- wire Sparkbot routes
- call Sparkbot tools
- call Sparkbot connectors
- write Sparkbot memory or tasks
- send Sparkbot messages
- persist Sparkbot state
- approve Sparkbot actions without future Guardian lifecycle implementation

## Arc Bot Boundary

Arc Bot / LIMA Office may later supply only redacted, already-normalized office-task metadata to LIMA.

Arc must own:

- raw office-task handling
- local redaction before LIMA
- shell actor/session/tenant context
- customer data boundary controls
- proof packet creation
- production route decisions

LIMA must not:

- parse raw customer requests
- ingest raw customer records
- wire Arc production routes
- mutate Arc tasks, projects, notes, forms, records, or files
- call Arc connectors or office-system adapters
- trigger Arc schedulers or workers
- approve Arc actions without future Guardian lifecycle implementation

## Event And Audit Boundary

This design does not add persistence.

Future event metadata may include:

- `event_id`
- `request_id`
- `intent_id`
- `guardian_request_id`
- `decision_id`, if a real decision exists later
- `actor_id`
- `shell_id`
- `session_id`
- `event_type`
- `state`
- `risk_class`
- `redacted_summary`
- `evidence_refs`

Events must not include:

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
- pairing codes
- unsafe command payloads
- live scan dumps
- private SSIDs
- raw Bluetooth MACs
- raw IP or MAC addresses
- raw device serials
- precise physical location
- robot or drone command payloads

Durable event/spine persistence requires a separate design and implementation lane.

## Future API Shape

Future implementation may add narrow dataclasses or protocols such as:

- `IntentEnvelopeCandidate`
- `GuardianRequest`
- `GuardianDecisionLifecycleState`
- `GuardianDecisionAuthority`
- `ApprovalRequirement`
- `GuardianLifecycleResult`

These must remain scoped and non-executing in the first implementation branch.

The first implementation branch should not create real execution authority. It should only map already-normalized kernel metadata into a non-authoritative lifecycle preview or request candidate and preserve dry-run result invariants.

## Forbidden Implementation In This Branch

This branch must not add:

- runtime behavior
- `lima/` changes
- `tests/support/` changes
- live Guardian request bridge
- real IntentEnvelope creation
- real GuardianDecision creation
- approval enforcement
- ApprovalMetadata recording
- dispatch
- model calls
- tool execution
- connector access
- memory writes
- task state writes
- storage or persistence
- event spine persistence
- shell wiring
- Sparkbot wiring
- Arc Bot wiring
- live HumanInput bridge
- browser/file/process/network mutation
- live discovery
- connection attempts
- pairing
- credential use
- scheduler/background work
- queues, workers, daemons, subprocesses, or threads
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Future Implementation Branch

If this design passes audit, the next possible implementation-shaped branch may be:

`implement-lima-guardian-lifecycle-preview-only`

That branch may only:

- add typed non-authoritative lifecycle preview objects
- map `KernelRequest` metadata into a dry-run lifecycle preview
- prepare a GuardianRequest-shaped object without creating GuardianDecision authority
- return blocked or approval_required metadata
- preserve all non-execution invariants
- emit redacted in-memory events only
- add focused tests for fail-closed lifecycle behavior

That branch must not:

- enforce approvals
- approve execution
- dispatch work
- call models
- execute tools
- access connectors
- persist events
- wire Sparkbot or Arc Bot
- touch devices, Robo-OS, robotics, drones, or physical-world systems

## Recommended Next Branch

`audit-lima-guardian-request-decision-lifecycle-contract`
