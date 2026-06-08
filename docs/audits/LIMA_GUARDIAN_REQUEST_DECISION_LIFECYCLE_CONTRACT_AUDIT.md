# LIMA Guardian Request Decision Lifecycle Contract Audit

## Branch

`audit-lima-guardian-request-decision-lifecycle-contract`

## Base Commit

`c07a67b86690b938cbeec6212399af04aaa51b23`

## Audit Verdict

PASS.

The Guardian request decision lifecycle contract is a docs-only design that gives LIMA a clear next safety boundary before future Sparkbot and Arc Bot runtime use.

It preserves the distinction between:

- `KernelRequest` as shell-facing dry-run metadata
- `IntentEnvelope` candidate as structured intent metadata, not authority
- `GuardianRequest` as a request for review, not a decision
- `GuardianDecision` as future authority, not created in this branch
- `ApprovalMetadata` as evidence, not a replacement for GuardianDecision
- `ExecutionResult` as dry-run until future execution lanes are separately approved
- event/spine records as future audit surfaces, not persistence in this branch

The design is ready for the next implementation-shaped lane only if that lane remains non-authoritative and preview-only.

## Scope And File Safety

The audited design branch added only:

- `docs/design/LIMA_GUARDIAN_REQUEST_DECISION_LIFECYCLE_CONTRACT.md`
- `docs/audits/LIMA_GUARDIAN_REQUEST_DECISION_LIFECYCLE_CONTRACT_READINESS_REVIEW.md`

This audit branch adds only:

- `docs/audits/LIMA_GUARDIAN_REQUEST_DECISION_LIFECYCLE_CONTRACT_AUDIT.md`

The branch does not modify:

- `lima/`
- `tests/`
- `tests/support/`
- public Sparkbot repositories
- Arc Bot repositories
- package metadata
- public exports
- provider/model files
- adapter files
- storage/persistence files
- shell wiring files
- Robo-OS wiring files

No runtime behavior is added.

## Current Baseline Review

The design correctly describes the current LIMA baseline:

- `LimaKernel.evaluate(...)` accepts already-normalized metadata.
- Kernel results remain dry-run only.
- safe planning/drafting/text-preview metadata may be proposed.
- unknown, unsafe, disabled, consequential, connection, device, robot, drone, and physical-world categories block or require approval metadata without execution.
- `GuardianStubDecision` remains non-authoritative.
- events remain redacted and in-memory only.
- `SimulatedDiscoveryAdapter` remains deterministic, explicit, synthetic, inert, and dry-run only.

This matches the current non-executing proof posture.

## Lifecycle Boundary Review

The lifecycle sequence is appropriate:

```text
KernelRequest
  -> IntentEnvelope candidate
  -> GuardianRequest
  -> GuardianDecision
  -> ApprovalMetadata, if required later
  -> ExecutionResult
  -> Event or Spine record, if approved later
```

The sequence is useful because it prevents a common failure mode: shells or adapters treating normalized metadata as execution authority.

The design keeps every pre-decision object non-authoritative.

## IntentEnvelope Candidate Review

The design correctly states that an `IntentEnvelope` candidate is not:

- a command
- a tool call
- approval
- authorization
- execution permission
- persistence permission
- a real runtime record in this branch

Allowed candidate states are descriptive:

- `drafted`
- `needs_clarification`
- `ready_for_guardian_request`
- `blocked_before_guardian`

Forbidden candidate states correctly block authority claims:

- `approved`
- `authorized`
- `execution_allowed`
- `dispatch_allowed`
- `persisted`
- `sent`
- `completed`

This is safe for later preview-only implementation.

## GuardianRequest Review

The design preserves the existing Guardian request safety gate:

- Guardian request is not GuardianDecision.
- Guardian request is not approval.
- Guardian request is not enforcement.
- Guardian request cannot create approval.
- Guardian request cannot authorize execution.
- `requested_tool_packs` are requests only.
- `requested_tool_packs` are not `allowed_tool_packs`.
- `approval_requirement_ref` is descriptive only.
- `approval_requirement_ref` is not ApprovalMetadata.
- trust context is context only.
- privacy/redaction metadata is not enforcement.

Allowed request states are safe:

- `prepared`
- `needs_clarification`
- `ready_for_policy_review`
- `blocked_before_decision`
- `invalid`

Forbidden request states correctly prevent accidental authority:

- `approved`
- `approval_granted`
- `execution_allowed`
- `dispatch_allowed`
- `tool_packs_granted`
- `policy_enforced`

## GuardianDecision Review

The design correctly treats `GuardianDecision` as future authority only.

It does not implement decision creation. It does not authorize execution. It does not claim production Guardian behavior.

Allowed future statuses are consistent with existing Guardian decision vocabulary:

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

The design explicitly states that denied, blocked, escalated, expired, revoked, and superseded decisions are audit records only and not execution credentials.

## ApprovalMetadata Review

The design correctly states that `ApprovalMetadata` is future evidence only.

It is not:

- a substitute for GuardianDecision
- a tool execution token
- proof that execution happened
- allowed as runtime behavior in this design branch

It correctly requires future ApprovalMetadata to attach to a scoped GuardianDecision.

No approval enforcement is introduced.

## Fail-Closed Review

The design requires blocking when:

- identity context is missing
- normalized intent is missing
- raw prompt/chat/office-task text is supplied as executable intent
- source surface metadata indicates secrets or unsafe payloads
- capability is disabled
- action category is unknown
- requested tool pack is unknown or mismatched
- risk class is missing or contradictory
- provenance is missing for consequential actions
- approval-bypass wording appears
- owner/admin/operator wording attempts to bypass Guardian
- Guardian request tries to claim decision authority
- GuardianDecision is absent for future consequential execution
- GuardianDecision is expired, revoked, superseded, denied, blocked, or escalated
- required ApprovalMetadata is absent or scope-mismatched
- event metadata contains forbidden raw data
- downstream behavior requires unapproved model/tool/connector/storage/scheduler/browser/file/process/network/device/robot/drone/physical-world capability

This is the correct fail-closed stance.

## Sparkbot Boundary Review

The design keeps Sparkbot-owned work out of LIMA:

- raw chat handling
- local redaction before LIMA
- shell actor/session context
- source surface classification
- proof packet creation
- production route decisions

The design forbids LIMA from:

- parsing Sparkbot raw chat
- wiring Sparkbot routes
- calling Sparkbot tools or connectors
- writing Sparkbot memory or tasks
- sending Sparkbot messages
- persisting Sparkbot state
- approving Sparkbot actions before future Guardian lifecycle implementation

This preserves the public Sparkbot repo boundary and keeps Sparkbot as consumer-owned proof work.

## Arc Bot Boundary Review

The design keeps Arc Bot / LIMA Office-owned work out of LIMA:

- raw office-task handling
- local redaction before LIMA
- shell actor/session/tenant context
- customer data boundary controls
- proof packet creation
- production route decisions

The design forbids LIMA from:

- parsing raw customer requests
- ingesting raw customer records
- wiring Arc production routes
- mutating Arc tasks, projects, notes, forms, records, or files
- calling Arc connectors or office-system adapters
- triggering Arc schedulers or workers
- approving Arc actions before future Guardian lifecycle implementation

This preserves Arc Bot as a separate consumer-owned proof path.

## Event And Audit Boundary Review

The design does not add persistence.

It allows future event metadata fields only as design concepts and requires redaction of:

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
- raw Bluetooth MAC addresses
- raw IP or MAC addresses
- raw device serials
- precise physical location
- robot or drone command payloads

Durable event/spine persistence remains separately blocked.

## Future Implementation Readiness

The design is narrow enough for:

`implement-lima-guardian-lifecycle-preview-only`

That later branch may only:

- add typed non-authoritative lifecycle preview objects
- map `KernelRequest` metadata into a dry-run lifecycle preview
- prepare a GuardianRequest-shaped object without creating GuardianDecision authority
- return blocked or approval_required metadata
- preserve all non-execution invariants
- emit redacted in-memory events only
- add focused fail-closed tests

That later branch must not:

- enforce approvals
- approve execution
- dispatch work
- call models
- execute tools
- access connectors
- persist events
- wire Sparkbot or Arc Bot
- touch devices, Robo-OS, robotics, drones, or physical-world systems

## Forbidden Surfaces Checked

The design does not approve:

- runtime behavior in this branch
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

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended audit report before commit

## Readiness Decision

Ready for the next implementation-shaped lane:

`implement-lima-guardian-lifecycle-preview-only`

Not ready for:

- Sparkbot product integration
- Arc Bot product integration
- public Sparkbot release wiring
- live GuardianDecision authority
- approval enforcement
- model calls
- tool execution
- connector access
- persistence
- live discovery
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior
