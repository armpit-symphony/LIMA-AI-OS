# LIMA Guardian Decision Authority Preview Audit

## Branch

`audit-lima-guardian-decision-authority-preview`

## Base Commit

`dac7f32ae9e8281aff47771a2ca98db73e0b1973`

## Audited Branch

`implement-lima-guardian-decision-authority-preview`

## Audited Branch Base Commit

`a5b1ee9395905a06ff14999b422919ce7a31c208`

## Audit Verdict

PASS.

The Guardian decision authority preview implementation is narrow, non-authoritative, dry-run only, and fail-closed. It
adds a useful preview surface for determining whether future `GuardianDecision` authority would be required, while
preserving the current rule that no real decision authority, approval enforcement, execution, dispatch, persistence,
model calls, tool execution, connector access, shell wiring, Robo-OS access, device control, robotics, drones, or
physical-world behavior exists.

The branch is ready for a public API metadata review lane. It is not ready for real GuardianDecision authority.

## Scope And File Safety

The audited implementation branch changed only:

- `lima/kernel/guardian_decision_authority.py`
- `lima/kernel/kernel.py`
- `tests/test_lima_guardian_decision_authority_preview.py`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_PREVIEW_IMPLEMENTATION_AUDIT.md`

This audit branch adds only:

- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_PREVIEW_AUDIT.md`

The audited implementation did not modify:

- `lima/__init__.py`
- `lima/kernel/__init__.py`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/support/`
- `pyproject.toml`
- package metadata
- public Sparkbot repository files
- Arc Bot repository files
- provider/model files
- adapter registry files
- storage/persistence files
- shell wiring files
- Robo-OS files

## Public API Review

The implementation adds one callable method:

```python
LimaKernel.preview_guardian_decision_authority(request)
```

It does not add a top-level `lima` export.

It does not add `GuardianDecisionAuthorityPreviewResult`, `GuardianDecisionAuthorityPreview`,
`GuardianDecisionAuthorityPreviewEvent`, or `preview_guardian_decision_authority(...)` to `lima.kernel.__all__`.

The result dataclasses are internal implementation-preview objects. They are reachable by direct module import for tests,
but they are not proof-public API.

`LimaKernel.preview_guardian_decision_authority(...)` should be reviewed in the next public API metadata lane before
Sparkbot or Arc proof branches treat it as an approved proof surface.

## Runtime Behavior Review

The method:

- accepts `KernelRequest` or mapping metadata
- coerces mapping metadata through the existing `KernelRequest` shape
- classifies whether a future decision would be required
- reviews optional decision-shaped preview metadata
- blocks unsafe status/scope/approval cases
- returns result-local events
- preserves dry-run-only metadata

It does not:

- call `LimaKernel.evaluate(...)`
- change existing `evaluate(...)` behavior
- create real `GuardianDecision`
- create runtime `IntentEnvelope`
- enforce approval
- record `ApprovalMetadata`
- dispatch work
- persist events
- call models
- execute tools
- access connectors
- wire Sparkbot
- wire Arc Bot
- wire Robo-OS
- perform live discovery
- touch devices or physical-world systems

## Classification Behavior Review

PASS.

Tests and code confirm:

- safe planning returns `authority_not_required`
- enabled consequential capability returns `authority_required`
- disabled capability blocks
- dangerous capability blocks
- execution-seeking request without decision-shaped metadata blocks
- unknown decision status blocks
- revoked or other non-eligible status blocks
- scope mismatch blocks
- approval-required preview metadata without approval reference blocks
- matching approved preview metadata still returns `authority_required`, not execution approval
- raw executable input blocks
- authority claims block
- runtime dependency presence blocks

The implementation intentionally avoids treating even a matching approved preview as executable. That is correct.

## Authority Boundary Review

PASS.

The implementation keeps:

- `decision_authority_created is False`
- `guardian_decision_created is False`
- `approval_enforced is False`
- `execution_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`

The preview result names possible future decision needs but never creates real authority.

The preview object is decision-requirement metadata, not a `GuardianDecision`.

## Non-Execution Invariant Review

PASS.

`GuardianDecisionAuthorityPreviewResult` preserves:

- `dry_run is True`
- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
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

The focused test suite asserts these invariants directly.

## Event And Redaction Review

PASS.

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

Tests confirm event metadata remains:

- `in_memory_only is True`
- `durable is False`
- `contains_secret is False`
- `contains_raw_prompt is False`
- `contains_unsafe_payload is False`

## Forbidden Import And Surface Review

PASS.

The test suite checks `lima/kernel/guardian_decision_authority.py` for forbidden imports and calls.

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

The module imports only dataclass/typing helpers, the existing lifecycle constants, and kernel plugin contracts.

## Test Coverage Review

Added tests cover:

- explicit `LimaKernel.preview_guardian_decision_authority(...)`
- safe planning authority-not-required behavior
- no public export expansion
- enabled consequential capability authority-required behavior
- disabled capability block
- dangerous capability block
- execution-seeking no-decision block
- unknown decision status block
- revoked/non-eligible status block
- actor scope mismatch block
- approval-required missing approval ref block
- matching approved preview remains non-executing and authority-required only
- raw input block
- authority claim block
- runtime dependency block
- redacted in-memory events
- non-execution invariants
- forbidden imports and calls
- forbidden Sparkbot/Arc/Robo/persistence/dispatch/execution strings

Coverage is sufficient for this preview-only slice.

## Risk And Gap Review

Remaining gaps are intentional:

- `preview_guardian_decision_authority(...)` is not classified in the public API manifest
- preview result objects are not public API
- no real GuardianDecision authority exists
- no approval enforcement exists
- no HumanInput bridge exists
- no runtime IntentEnvelope creation exists
- no event/spine persistence exists
- no consumer proof packet has been received from Sparkbot or Arc Bot
- no compatibility freeze exists

These are blockers to product use, not defects in this preview slice.

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests/test_lima_guardian_decision_authority_preview.py -p no:cacheprovider` - passed, 15 tests
- `python -m pytest -q tests/test_lima_guardian_lifecycle_preview.py -p no:cacheprovider` - passed, 13 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2863 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended audit report before commit

## Readiness Decision

Ready for the next design lane:

`design-lima-guardian-decision-authority-public-api-contract`

That lane should decide whether `LimaKernel.preview_guardian_decision_authority(...)` remains internal, becomes
`method_level_dry_run_candidate`, or stays out of consumer proof guidance until Guardian authority semantics mature.

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

`design-lima-guardian-decision-authority-public-api-contract`
