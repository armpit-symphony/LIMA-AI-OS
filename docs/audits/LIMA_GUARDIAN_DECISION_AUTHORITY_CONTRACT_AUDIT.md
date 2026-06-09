# LIMA Guardian Decision Authority Contract Audit

## Branch

`audit-lima-guardian-decision-authority-contract`

## Base Commit

`1c31f2fda0b97c58f328769cfcc17895edc1f32c`

## Audited Branch

`design-lima-guardian-decision-authority-contract`

## Audited Branch Base Commit

`200e45569f2890a11d4fc4c3ec090983e894fe00`

## Audit Verdict

PASS.

The Guardian decision authority contract is docs-only, conservative, and aligned with LIMA's current non-executing
runtime posture. It defines the future `GuardianDecision` authority boundary without creating real authority, approval
enforcement, dispatch, persistence, provider/model routing, tool execution, connector access, shell wiring, live
discovery, Robo-OS access, device control, robotics, drones, or physical-world behavior.

The design is ready for the next implementation-shaped lane only if that lane remains preview-only and
non-authoritative.

## Scope And File Safety

The audited design branch added only:

- `docs/design/LIMA_GUARDIAN_DECISION_AUTHORITY_CONTRACT.md`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_CONTRACT_READINESS_REVIEW.md`

This audit branch adds only:

- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_CONTRACT_AUDIT.md`

The audited branch did not modify:

- `lima/`
- `tests/`
- `tests/support/`
- `pyproject.toml`
- package metadata
- public exports
- public Sparkbot repository files
- Arc Bot repository files
- provider/model files
- adapter files
- storage/persistence files
- shell wiring files
- Robo-OS files

No runtime behavior was added.

## Current Baseline Review

The design accurately describes the current baseline:

- `LimaKernel.evaluate(...)` is dry-run only for already-normalized metadata.
- `LimaKernel.preview_guardian_lifecycle(...)` is non-authoritative lifecycle preview metadata.
- `GuardianStubDecision` is non-authoritative.
- lifecycle preview result objects preserve `guardian_decision_created is False`.
- lifecycle preview result objects preserve `approval_enforced is False`.
- events remain redacted and in-memory/result-local only.
- `SimulatedDiscoveryAdapter` remains explicit, deterministic, synthetic, inert, and dry-run only.

This is consistent with current source and the public API manifest.

## Public API Review

The design does not change public API posture.

Confirmed current posture remains:

- `from lima.kernel import LimaKernel` is proof-public.
- `LimaKernel.preview_guardian_lifecycle(...)` is `method_level_dry_run_candidate`.
- lifecycle preview result dataclasses are not proof-public imports.
- top-level `lima` does not export runtime APIs.
- no `GuardianDecision` authority object is exported by this branch.

This is the right boundary for a design-only authority contract.

## Authority Separation Review

PASS.

The design correctly states that future authority requires an approved Guardian decision service, one bound
`GuardianRequest`, one bound intent or intent candidate, scoped action category, explicit status, constraints, policy
provenance, expiry/revocation semantics, redacted audit output, and a separate execution-boundary check before side
effects.

The design correctly marks these as non-authority:

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

This prevents the next implementation from confusing metadata with permission.

## Decision Status Review

PASS.

Allowed future statuses are explicit:

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

The design correctly says execution may never be inferred from status alone. It also correctly states that denied,
blocked, escalated, expired, revoked, and superseded decisions are audit records only.

Unknown status defaults to blocked.

## Scope Rules Review

PASS.

The design requires future decisions to be scoped by actor, shell, session, tenant/workspace where applicable, action
category, capability, target reference, allowed tool/driver packs, risk/consequence class, expiry/revocation window, and
approval requirement.

It also states that scope may only narrow downstream and must never widen.

The examples are correct:

- `connector_read` does not imply `connector_write`
- `external_send` does not imply file writes or process execution
- simulated discovery does not imply live discovery
- one actor/session does not authorize another
- planning text does not authorize models, tools, connectors, files, browsers, devices, or sends
- dry-run does not authorize live execution

## Approval Relationship Review

PASS.

The design keeps approval separate from decision authority. It correctly says future `ApprovalMetadata` is evidence only
and not a decision, policy result, tool token, execution credential, or Guardian replacement.

Approval evidence must bind to a scoped decision and must not widen that decision.

No approval enforcement is introduced.

## Fail-Closed Review

PASS.

The design requires blocking for:

- missing decision on execution-seeking actions
- missing decision identity fields
- missing request or intent binding
- unknown or ineligible decision status
- expired, revoked, or superseded decision
- scope, capability, target, tool-pack, driver-pack, or approval mismatch
- disabled capabilities
- stale/revoked/overbroad approval evidence
- raw sensitive event or audit metadata
- approval-bypass wording
- owner/admin/operator override attempts without policy support
- execute, dispatch, persist, send, connect, pair, scan, mutate, or actuation attempts through unapproved lanes
- downstream calls to models, tools, connectors, storage, schedulers, browsers, files, processes, networks, devices,
  Robo-OS, robots, drones, or physical-world systems without a separately approved execution boundary

Unknown blocks. This matches LIMA's fail-closed doctrine.

## Non-Execution Invariant Review

PASS.

The contract preserves the current proof invariant set:

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
- `guardian_decision_created is False` unless a later audited branch explicitly creates non-executing decision records
- `approval_enforced is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `robo_os_wiring_active is False`
- `adapter_active is False`
- `tool_execution_allowed is False`
- `driver_execution_allowed is False`
- `scheduler_active is False`
- `external_calls_allowed is False`

The exception language is acceptable only because it still requires a later audited branch and limits any future record
to non-executing decision-shaped metadata. It does not approve real authority in this branch.

## Event And Redaction Review

PASS.

The design defines future event names only and implements none:

- `guardian_decision_requested`
- `guardian_decision_prepared`
- `guardian_decision_blocked`
- `guardian_decision_denied`
- `guardian_decision_approval_required`
- `guardian_decision_expired`
- `guardian_decision_revoked`
- `guardian_decision_scope_mismatch`

The design blocks raw prompts, raw chat text, raw office-task text, raw customer records, raw provider payloads, raw tool
arguments, raw connector records, credentials, headers, cookies, tokens, passwords, API keys, pairing codes, unsafe
command payloads, live scan dumps, private SSIDs, raw network/device identifiers, precise physical location,
robot/drone command payloads, and physical-world actuator payloads.

Durable persistence remains separately blocked.

## Sparkbot Boundary Review

PASS.

The design keeps Sparkbot as a consumer shell and leaves the public Sparkbot repo untouched.

It forbids:

- public Sparkbot repo changes
- Sparkbot route wiring
- Sparkbot model/tool/connector/memory/storage/scheduler/browser/file/process/network/send behavior
- treating Sparkbot proof packets as production integration approval

This preserves the consumer-owned proof model.

## Arc Bot Boundary Review

PASS.

The design keeps Arc Bot / LIMA Office as a consumer shell and does not touch Arc repositories.

It forbids:

- Arc route wiring
- office-system adapter calls
- customer record/task/note/form/file mutation
- scheduler/worker triggers
- customer communications
- treating Arc proof packets as production integration approval

This preserves the Arc consumer-owned proof model.

## Robo-OS And Physical-World Review

PASS.

The design does not authorize:

- Robo-OS access
- device control
- robotics actuation
- drone actuation
- physical-world behavior
- live discovery
- connection attempts
- pairing
- credential use

It also correctly says future physical-world decisions require stricter policy, dry-run/simulation, explicit HumanInput
approval, emergency stop handling, telemetry, and a separately audited driver execution boundary.

## Implementation Readiness

Ready for a future preview-only lane:

`implement-lima-guardian-decision-authority-preview`

That branch should be limited to:

- non-executing decision-authority preview metadata or dataclasses
- required-decision classification
- missing/invalid authority blockers
- status/scope/approval mismatch blockers
- dry-run-only results
- redacted in-memory/result-local events
- focused fail-closed tests

It must not:

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

## Forbidden Surfaces Checked

No forbidden surface is introduced or approved by this audit.

Still blocked:

- runtime authority creation
- approval enforcement
- execution approval
- dispatch
- persistence
- event spine persistence
- provider/model routing
- model calls
- tool execution
- connector access
- memory writes
- task-state writes
- live HumanInput bridge
- raw natural-language parsing
- Sparkbot wiring
- Arc Bot wiring
- Robo-OS wiring
- live adapters
- browser/file/process/network mutation
- sockets
- live discovery
- scanning
- connection attempts
- pairing
- credential use or storage
- scheduler/background workers
- queues, daemons, subprocesses, or threads
- device control
- robotics
- drones
- physical-world behavior

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests/test_lima_guardian_lifecycle_preview.py -p no:cacheprovider` - passed, 13 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2848 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended audit report before commit

## Readiness Decision

Ready for:

`implement-lima-guardian-decision-authority-preview`

Not ready for:

- Sparkbot product integration
- Arc Bot product integration
- public Sparkbot release wiring
- real GuardianDecision authority
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

## Recommended Next Branch

`implement-lima-guardian-decision-authority-preview`
