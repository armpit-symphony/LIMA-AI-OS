# LIMA Guardian Lifecycle Preview Implementation Audit

## Branch

`implement-lima-guardian-lifecycle-preview-only`

## Base Commit

`7ce3a5fddb158e1a201f44d92f5021eb4de56101`

## Implementation Verdict

PASS for a narrow non-authoritative Guardian lifecycle preview implementation.

This branch adds a dry-run preview path only. It does not create real `IntentEnvelope` records, real `GuardianRequest` runtime authority, real `GuardianDecision` authority, approval enforcement, dispatch, model calls, tool execution, connector access, persistence, shell wiring, live discovery, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Files Changed

- `lima/kernel/guardian_lifecycle.py`
- `lima/kernel/kernel.py`
- `tests/test_lima_guardian_lifecycle_preview.py`
- `docs/audits/LIMA_GUARDIAN_LIFECYCLE_PREVIEW_IMPLEMENTATION_AUDIT.md`

No public Sparkbot repository files or Arc Bot repository files were touched.

## Callable API Added

Added explicit method:

```python
LimaKernel.preview_guardian_lifecycle(request)
```

The method accepts:

- `KernelRequest`
- mapping-shaped request metadata that can be coerced into `KernelRequest`

The method returns:

- `GuardianLifecyclePreviewResult`

The new result object is intentionally not exported from `lima.kernel.__all__` in this branch. This avoids expanding proof-public API surface before a later public API review.

## New Internal Preview Objects

Added non-authoritative frozen dataclasses:

- `IntentEnvelopeCandidatePreview`
- `GuardianRequestPreview`
- `GuardianLifecyclePreviewEvent`
- `GuardianLifecyclePreviewResult`

These objects are preview metadata only. They are not runtime records, not authority, not approval, not dispatch permission, and not persistence.

## Behavior Summary

Safe planning/drafting/text-preview metadata may return:

`proposed`

Consequential enabled capabilities may return:

`approval_required`

Unknown, unsafe, disabled, dangerous, raw-input, authority-claim, unsafe source-surface, blocked dependency, and tool-pack mismatch paths return:

`blocked`

The lifecycle preview prepares:

- an `IntentEnvelopeCandidatePreview`
- a `GuardianRequestPreview`
- redacted in-memory event metadata

It never prepares:

- real `IntentEnvelope`
- real `GuardianDecision`
- real `ApprovalMetadata`
- execution dispatch
- persistent audit/spine records

## Fail-Closed Checks

The implementation blocks:

- raw chat text and raw office-task fields
- authority/approval/dispatch claims
- unsafe source surfaces
- disabled capabilities
- dangerous capabilities such as process, device, robot, drone, and physical-world action
- requested tool packs not allowed by the capability profile
- runtime dependency injection such as provider registry, storage, HumanInput bridge, or driver registry
- unknown action categories

## Non-Execution Guarantees

`GuardianLifecyclePreviewResult` preserves:

- `dry_run is True`
- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `guardian_decision_created is False`
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

The preview returns result-local event metadata only.

Events are:

- redacted
- in-memory only
- non-durable
- not written to a database or file
- not emitted to a queue, worker, scheduler, webhook, socket, shell, browser, or external service

Evidence refs containing credential-like markers are dropped from the preview.

## Public API Status

No top-level `lima` export was added.

No new symbol was added to `lima.kernel.__all__`.

The public API manifest remains unchanged. The new preview objects are implementation-preview internals until a later public API review decides otherwise.

## Tests Added

Added `tests/test_lima_guardian_lifecycle_preview.py`.

The tests cover:

- explicit `LimaKernel.preview_guardian_lifecycle(...)` method
- safe planning preview
- mapping request coercion
- no `lima.kernel.__all__` expansion
- unknown action block
- raw chat/office-task block
- authority claim block
- disabled capability block
- consequential enabled capability returns approval_required only
- dangerous capability block
- requested tool pack mismatch block
- runtime dependency block
- redacted in-memory events
- non-execution invariants
- forbidden imports and calls
- forbidden Sparkbot/Arc/Robo/persistence/dispatch/execution strings

## Forbidden Surfaces Checked

Checked no new usage of:

- sockets/network APIs
- OS network APIs
- Bluetooth/BLE libraries
- USB/serial libraries
- MQTT/Matter/mDNS libraries
- subprocess
- threading/background workers
- scheduler
- filesystem mutation/persistence
- database/storage backends
- provider/model calls
- Sparkbot imports
- Arc Bot imports
- Robo-OS imports
- live adapters
- device/robot/drone control
- physical-world code

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2698 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only intended implementation files before commit

## Remaining Blockers Before Sparkbot And Arc Product Use

Still blocked:

- consumer-owned Sparkbot dry-run proof packet
- consumer-owned Arc Bot dry-run proof packet
- proof packet redaction review
- proof packet audits
- compatibility freeze
- public API review for lifecycle preview symbols
- real Guardian request/decision runtime implementation
- approval enforcement
- HumanInput bridge
- runtime `IntentEnvelope` creation
- provider/model boundary
- tool execution boundary
- connector boundary
- scheduler/background-work boundary
- event/spine persistence
- storage interface
- Sparkbot/Arc repo-owned integration work

## Recommended Next Branch

`audit-lima-guardian-lifecycle-preview-only`
