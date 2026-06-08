# LIMA Guardian Lifecycle Preview Audit

## Branch

`audit-lima-guardian-lifecycle-preview-only`

## Base Commit

`573b81a022a28599722f11968e0b354343717b66`

## Audit Verdict

PASS.

The Guardian lifecycle preview implementation is narrow, explicit, non-authoritative, and dry-run only.

It gives `LimaKernel` a callable lifecycle preview surface without creating real `IntentEnvelope` records, real `GuardianDecision` authority, approval enforcement, dispatch, persistence, model calls, tool execution, connector access, Sparkbot wiring, Arc Bot wiring, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Scope And File Safety

The implementation branch changed only:

- `lima/kernel/guardian_lifecycle.py`
- `lima/kernel/kernel.py`
- `tests/test_lima_guardian_lifecycle_preview.py`
- `docs/audits/LIMA_GUARDIAN_LIFECYCLE_PREVIEW_IMPLEMENTATION_AUDIT.md`

This audit branch adds only:

- `docs/audits/LIMA_GUARDIAN_LIFECYCLE_PREVIEW_AUDIT.md`

The implementation did not modify:

- `lima/kernel/__init__.py`
- top-level `lima/__init__.py`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/support/`
- public Sparkbot repository files
- Arc Bot repository files
- provider/model implementation files
- adapter implementation files outside the existing simulated adapter surface
- storage/persistence files
- shell wiring files
- Robo-OS wiring files

## Public API Review

The implementation adds one explicit method:

```python
LimaKernel.preview_guardian_lifecycle(request)
```

It does not add new symbols to `lima.kernel.__all__`.

It does not add top-level runtime exports from `lima`.

The preview result/dataclass objects remain internal implementation-preview symbols reachable by module import, not proof-public API. That is appropriate until a later public API review decides whether to expose them.

## Runtime Behavior Review

The preview path:

- accepts a `KernelRequest` or mapping coercible to `KernelRequest`
- returns `GuardianLifecyclePreviewResult`
- prepares `IntentEnvelopeCandidatePreview`
- prepares `GuardianRequestPreview`
- returns result-local redacted events
- blocks unsafe input fail-closed
- returns `approval_required` for enabled consequential capabilities
- returns `proposed` for safe low-risk planning/drafting/text preview

It does not:

- call `LimaKernel.evaluate(...)`
- modify existing `evaluate(...)` behavior
- create real `IntentEnvelope`
- create real `GuardianRequest` authority
- create real `GuardianDecision`
- record `ApprovalMetadata`
- enforce approval
- dispatch work
- call models
- execute tools
- access connectors
- persist events
- wire shells
- start workers
- perform live discovery
- touch devices or physical-world systems

## Guardian Boundary Review

The implementation correctly preserves:

- `IntentEnvelopeCandidatePreview` is metadata, not authority.
- `GuardianRequestPreview` is a request-shaped preview, not a decision.
- `decision_ref` remains `None`.
- `approval_ref` remains `None`.
- `guardian_decision_created` remains `False`.
- `approval_enforced` remains `False`.
- requested tool packs do not become allowed tool packs.
- dangerous capabilities block even when enabled.
- runtime dependency injection blocks the preview.

This matches the lifecycle contract and current Guardian safety gates.

## Fail-Closed Behavior Review

Tests and code confirm fail-closed behavior for:

- unknown actions
- raw chat or raw office-task metadata fields
- authority/approval/dispatch claims
- disabled capabilities
- dangerous capabilities
- unallowed requested tool packs
- injected provider registry
- unsafe source-surface metadata by implementation path

The preview does not treat structured action names such as `process_execute` as approval-bypass wording; it reaches the intended dangerous-capability block.

## Non-Execution Invariant Review

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

The invariant coverage is explicit in `tests/test_lima_guardian_lifecycle_preview.py`.

## Event And Redaction Review

Preview events are result-local and in-memory only.

They do not persist to:

- files
- SQLite or database storage
- event spine
- queues
- workers
- schedulers
- sockets
- shell/browser/network surfaces
- external services

Credential-like evidence references are dropped from preview evidence refs.

Events expose redacted summaries only and carry:

- `durable is False`
- `in_memory_only is True`
- `contains_secret is False`
- `contains_raw_prompt is False`
- `contains_unsafe_payload is False`

## Forbidden Import And Surface Review

The test suite checks `lima/kernel/guardian_lifecycle.py` for forbidden imports and calls.

No new usage was introduced for:

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

## Test Coverage Review

Added tests cover:

- explicit `LimaKernel.preview_guardian_lifecycle(...)`
- successful safe planning preview
- mapping request coercion
- no public export expansion
- unknown action block
- raw chat/office-task block
- authority claim block
- disabled capability block
- enabled consequential capability returns `approval_required` only
- dangerous capability block
- requested tool-pack mismatch block
- runtime dependency block
- redacted in-memory events
- non-execution invariants
- forbidden imports and calls
- forbidden Sparkbot/Arc/Robo/persistence/dispatch/execution strings

Coverage is sufficient for this preview-only slice.

## Risk And Gap Review

Remaining gaps are intentional:

- preview result objects are not public API yet
- no real Guardian request runtime exists
- no real GuardianDecision authority exists
- no approval enforcement exists
- no event/spine persistence exists
- no consumer proof packet has been received from Sparkbot or Arc Bot
- no compatibility freeze exists

These are blockers to product use, not defects in this slice.

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended audit report before commit

## Readiness Decision

Ready for the next design lane:

`design-lima-guardian-lifecycle-public-api-contract`

That lane should decide whether lifecycle preview objects remain internal, become `dry_run_candidate`, or become proof-public API later.

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
