# LIMA Guardian Decision Authority Preview Implementation Audit

## Branch

`implement-lima-guardian-decision-authority-preview`

## Base Commit

`a5b1ee9395905a06ff14999b422919ce7a31c208`

## Files Changed

- `lima/kernel/guardian_decision_authority.py`
- `lima/kernel/kernel.py`
- `tests/test_lima_guardian_decision_authority_preview.py`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_PREVIEW_IMPLEMENTATION_AUDIT.md`

## Implementation Verdict

PASS for a narrow non-executing preview slice.

This branch adds a non-authoritative Guardian decision authority preview surface. It classifies whether a future
`GuardianDecision` would be required, reviews provided decision-shaped preview metadata for fail-closed status/scope/
approval blockers, emits redacted in-memory/result-local event metadata, and preserves all non-execution invariants.

It does not create real `GuardianDecision` authority, enforce approval, approve execution, dispatch work, persist
events, call models, execute tools, access connectors, wire Sparkbot, wire Arc Bot, wire Robo-OS, touch devices, or
perform physical-world behavior.

## New Callable API

One explicit method was added:

```python
LimaKernel.preview_guardian_decision_authority(request)
```

The method accepts:

- `KernelRequest`
- mapping coercible to `KernelRequest`

The method returns an internal `GuardianDecisionAuthorityPreviewResult`.

No new top-level `lima` export is added. No new `lima.kernel.__all__` export is added. The result dataclasses remain
internal implementation-preview objects and are not proof-public API.

## Internal Preview Objects

The new module defines:

- `GuardianDecisionAuthorityPreview`
- `GuardianDecisionAuthorityPreviewEvent`
- `GuardianDecisionAuthorityPreviewResult`
- `preview_guardian_decision_authority(...)`

These are internal preview implementation details. They grant no authority.

## Classification Behavior

The preview returns:

- `authority_not_required` for safe low-risk planning/drafting/text-preview metadata
- `authority_required` for enabled consequential capabilities such as model calls or external sends
- `blocked` for disabled capabilities
- `blocked` for dangerous capabilities
- `blocked` when an execution-seeking request has no decision-shaped metadata
- `blocked` for unknown decision statuses
- `blocked` for denied, blocked, expired, revoked, superseded, or escalated decision statuses
- `blocked` for scope mismatch
- `blocked` for approval-required preview metadata without an approval reference
- `authority_required` for matching approved decision-shaped preview metadata, while still creating no authority

The branch intentionally does not treat a matching approved preview as executable.

## Non-Execution Guarantees

All preview results preserve:

- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `dry_run is True`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `guardian_decision_created is False`
- `decision_authority_created is False`
- `approval_enforced is False`
- `approval_metadata_recorded is False`
- `tool_execution_allowed is False`
- `connector_access_allowed is False`
- `storage_persistence_allowed is False`
- `event_spine_persistence_allowed is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `arc_bot_wiring_active is False`
- `robo_os_wiring_active is False`
- `live_discovery_executed is False`
- `connection_attempted is False`
- `pairing_attempted is False`
- `credentials_used is False`
- `session_opened is False`
- `device_control_executed is False`
- `physical_world_allowed is False`
- `physical_world_executed is False`

## Event And Redaction Behavior

Events are result-local preview objects only.

They remain:

- in-memory only
- durable false
- redacted summary only
- no raw prompt
- no secret marker
- no unsafe payload marker

No file, database, queue, worker, scheduler, event-spine, socket, or external persistence is introduced.

## Public API Boundary

This branch intentionally does not modify:

- `lima/__init__.py`
- `lima/kernel/__init__.py`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- package metadata

`LimaKernel.preview_guardian_decision_authority(...)` is callable through the proof-public `LimaKernel` class, but it is
not yet classified in the public API manifest. A later public API metadata review should decide whether it remains
internal, becomes method-level dry-run candidate metadata, or stays implementation-preview only.

## Tests Added

Added focused tests for:

- explicit `LimaKernel.preview_guardian_decision_authority(...)`
- no public export expansion
- safe planning returning `authority_not_required`
- enabled consequential capability returning `authority_required`
- disabled capability block
- dangerous capability block
- execution-seeking request without decision block
- unknown decision status block
- revoked/non-eligible status block
- actor scope mismatch block
- approval-required without approval reference block
- matching approved preview remaining non-executing and authority-required only
- raw input block
- authority claim block
- runtime dependency block
- redacted in-memory events
- forbidden imports/calls
- forbidden Sparkbot/Arc/Robo/persistence/dispatch/execution strings

## Forbidden Surfaces Checked

No new usage was introduced for:

- real GuardianDecision authority
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
- `python -m pytest -q tests/test_lima_guardian_decision_authority_preview.py -p no:cacheprovider` - passed, 15 tests
- `python -m pytest -q tests/test_lima_guardian_lifecycle_preview.py -p no:cacheprovider` - passed, 13 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2863 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended implementation, test, and audit files before commit

## Remaining Blockers Before Sparkbot And Arc Product Use

- Sparkbot consumer-owned dry-run proof packet is still missing.
- Arc Bot consumer-owned dry-run proof packet is still missing.
- dry-run consumer compatibility freeze remains blocked.
- real GuardianDecision authority is still not implemented.
- approval enforcement is still not implemented.
- HumanInput bridge is still not implemented.
- runtime `IntentEnvelope` creation is still not implemented.
- provider/model routing is still not implemented.
- tool/connector/storage/event-spine execution lanes remain blocked.
- Sparkbot and Arc integration remain consumer-repo-owned and unproven.

## Recommended Next Branch

`audit-lima-guardian-decision-authority-preview`
