# LIMA Guardian Request Decision Lifecycle Contract Readiness Review

## Branch

`design-lima-guardian-request-decision-lifecycle-contract`

## Base Commit

`6f2a02cdf261b714073e22c9d85f48b6e0cd6183`

## Review Verdict

READY FOR INDEPENDENT AUDIT.

The design is narrow enough for a later non-authoritative Guardian lifecycle preview implementation. It preserves the current LIMA posture: dry-run, fail-closed, redacted, and non-executing.

It does not approve Sparkbot or Arc Bot product use. It does not approve runtime GuardianDecision authority, approval enforcement, model calls, tool execution, connector access, persistence, shell wiring, live discovery, Robo-OS, device control, robotics, drones, or physical-world behavior.

## Scope Review

This design branch adds only:

- `docs/design/LIMA_GUARDIAN_REQUEST_DECISION_LIFECYCLE_CONTRACT.md`
- `docs/audits/LIMA_GUARDIAN_REQUEST_DECISION_LIFECYCLE_CONTRACT_READINESS_REVIEW.md`

It does not modify:

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

## Boundary Preservation

The design preserves the required boundary sequence:

```text
KernelRequest
  -> IntentEnvelope candidate
  -> GuardianRequest
  -> GuardianDecision
  -> ApprovalMetadata, if required later
  -> ExecutionResult
  -> Event or Spine record, if approved later
```

It also preserves these distinctions:

- `KernelRequest` is shell-facing dry-run metadata.
- `IntentEnvelope` candidate is structured intent metadata, not authority.
- `GuardianRequest` is a request for review, not a decision.
- `GuardianDecision` is future authority, not created here.
- `ApprovalMetadata` is evidence, not a replacement for GuardianDecision.
- `ExecutionResult` remains dry-run until execution lanes are separately approved.
- Event/spine persistence remains future work.

## Fail-Closed Review

The design requires blocking for:

- missing actor/shell/session/tenant context where required
- missing normalized intent
- raw prompt/chat/office-task text supplied as executable intent
- unsafe source-surface metadata
- disabled capabilities
- unknown action categories
- unknown requested tool packs
- tool pack mismatch
- missing or contradictory risk class
- missing provenance for consequential actions
- approval-bypass wording
- owner/admin/operator bypass wording
- Guardian request attempting to claim decision authority
- absent GuardianDecision for future consequential execution
- expired, revoked, superseded, denied, blocked, or escalated decision state
- missing or mismatched ApprovalMetadata when required later
- forbidden raw data in event metadata
- downstream model/tool/connector/storage/scheduler/browser/file/process/network/device/robot/drone/physical behavior that lacks separate approval

This is aligned with Guardian always and fail-closed runtime design.

## Sparkbot Boundary Review

The design keeps Sparkbot-owned responsibilities outside this LIMA branch:

- raw chat handling
- local redaction
- source surface classification
- actor/session/shell context
- proof packet creation
- production route ownership

It forbids LIMA from:

- parsing Sparkbot raw chat
- wiring Sparkbot routes
- calling Sparkbot tools or connectors
- writing Sparkbot memory/tasks
- sending Sparkbot messages
- persisting Sparkbot state
- approving Sparkbot actions before future Guardian lifecycle implementation

This preserves the public Sparkbot repo boundary.

## Arc Bot Boundary Review

The design keeps Arc Bot / LIMA Office-owned responsibilities outside this LIMA branch:

- raw office-task handling
- local redaction
- customer data controls
- actor/session/tenant context
- proof packet creation
- production route ownership

It forbids LIMA from:

- parsing raw customer requests
- ingesting raw customer records
- wiring Arc production routes
- mutating Arc tasks, projects, notes, forms, records, or files
- calling Arc connectors or office-system adapters
- triggering Arc schedulers or workers
- approving Arc actions before future Guardian lifecycle implementation

This preserves the Arc repo boundary.

## Event And Redaction Review

The design keeps event behavior non-durable and future-only.

It forbids event metadata from carrying:

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

## Implementation Readiness

The design is narrow enough for a later implementation branch:

`implement-lima-guardian-lifecycle-preview-only`

That later branch should be limited to:

- typed non-authoritative lifecycle preview objects
- mapping already-normalized `KernelRequest` metadata into dry-run lifecycle preview metadata
- preparing a GuardianRequest-shaped object without creating GuardianDecision authority
- returning blocked or approval_required metadata
- preserving current non-execution invariants
- redacted in-memory events only
- focused fail-closed tests

## Forbidden Surfaces

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

## Validation Plan

Required validation for this design branch:

- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git status --short --branch`

## Readiness Decision

Ready for:

`audit-lima-guardian-request-decision-lifecycle-contract`

Not ready for:

- implementation until independent audit passes
- Sparkbot or Arc Bot product integration
- public Sparkbot release wiring
- live GuardianDecision authority
- approval enforcement
- model/tool/connector execution
- persistence
- live discovery
- Robo-OS/device/robot/drone/physical-world behavior
