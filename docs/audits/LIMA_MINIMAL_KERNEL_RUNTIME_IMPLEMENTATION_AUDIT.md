# LIMA Minimal Kernel Runtime Implementation Audit

## Branch

`implement-lima-minimal-kernel-runtime`

## Base commit

`1076efce44a268a744d8dbbf52a6bedbcbb46c2b`

## Files changed

- `lima/kernel/plugin_contract.py`
- `lima/kernel/kernel.py`
- `lima/kernel/__init__.py`
- `tests/test_lima_minimal_kernel_runtime.py`
- `docs/audits/LIMA_MINIMAL_KERNEL_RUNTIME_IMPLEMENTATION_AUDIT.md`

## Public imports exposed

New imports exposed from `lima.kernel`:

- `CapabilityProfile`
- `ExecutionResult`
- `GuardianStubDecision`
- `KernelEvent`
- `KernelRequest`
- `LimaKernel`

Top-level `lima` was not changed. `lima.__all__` remains limited to `["contracts"]`.

## New callable APIs

New callable API:

- `LimaKernel.evaluate(request)`

Accepted request types:

- `KernelRequest`
- mapping shaped like `KernelRequest`

The callable API accepts only already-normalized intent/task metadata. It does not parse raw natural language, ingest live HumanInput, create real IntentEnvelope records, create GuardianDecision authority, call models, call providers, execute tools, dispatch actions, or persist events.

Read-only inspection API:

- `LimaKernel.events`

This returns a tuple of redacted in-memory `KernelEvent` records held by that kernel instance only.

## Non-execution guarantees

Every `ExecutionResult` returned by the minimal kernel preserves these invariants:

- `executable=False`
- `execution_allowed=False`
- `side_effects_allowed=False`
- `dry_run=True`
- `dispatch_allowed=False`
- `persistence_allowed=False`
- `model_calls_allowed=False`
- `model_calls_executed=False`
- `physical_world_allowed=False`
- `physical_world_executed=False`
- `guardian_decision_created=False`
- `approval_enforced=False`
- `humaninput_bridge_active=False`
- `sparkbot_wiring_active=False`
- `robo_os_wiring_active=False`
- `adapter_active=False`
- `tool_execution_allowed=False`
- `driver_execution_allowed=False`
- `scheduler_active=False`
- `external_calls_allowed=False`

The implementation does not add provider/model adapters, storage backends, durable persistence, Guardian enforcement, approval enforcement, HumanInput runtime bridge, Sparkbot wiring, Arc Bot wiring, Robo-OS wiring, live adapters, tool execution, driver execution, scheduler/background work, shell/browser/network/file mutation, robotics, drones, devices, physical-world behavior, external sends, or secret storage.

## Capability gate behavior

Safe categories:

- `informational`
- `planning`
- `drafting`
- `text_preview`

These return `proposed` only when no authority-bypass wording or forbidden runtime dependency is present.

Approval-required capabilities when explicitly enabled:

- `model_calls`
- `memory_write`
- `task_state_write`
- `connector_read`
- `connector_write`
- `external_send`
- `file_write`
- `browser_control`
- `scheduler_run`

These return `approval_required`; they still do not execute and do not enforce approval.

Blocked capabilities:

- `process_execute`
- `device_control`
- `robotics_actuation`
- `drone_actuation`

These return `blocked`, even when enabled in the caller-provided profile.

Disabled capability behavior:

- If a request asks for a capability that is disabled in `CapabilityProfile`, the result is `blocked`.

Unknown behavior:

- Unknown action categories return `blocked`.
- Unknown capability names return `blocked`.
- Authority, approval, bypass, dispatch, persistence, execution, breakglass, or override wording in caller metadata returns `blocked`.

## Guardian stub behavior

The minimal Guardian stub is non-authoritative and fail-closed.

It can return:

- `proposed`
- `approval_required`
- `blocked`

It does not:

- create real GuardianDecision records
- approve execution
- enforce approval
- verify PINs
- open breakglass
- access Vault/Auth/Trust providers
- route providers
- persist policy decisions

`GuardianStubDecision.decision_ref` is always `None` in this implementation.

## Event behavior

The kernel emits redacted in-memory events only.

Current emitted event types:

- `kernel.request_received`
- `kernel.guardian_stub_evaluated`

Event guarantees:

- local instance memory only
- no durable persistence
- no database writes
- no file writes
- no scheduler, queue, worker, daemon, subprocess, or thread
- no raw prompt storage
- no raw provider payloads
- no secrets, tokens, headers, credentials, unsafe command payloads, raw tool args/results, raw terminal output, raw browser/network payloads, raw sensor payloads, or robot/device command payloads

Event summaries contain only redacted state/category/reason metadata.

## Tests added

Added `tests/test_lima_minimal_kernel_runtime.py`.

Coverage includes:

- `from lima.kernel import LimaKernel`
- safe normalized planning request returns `proposed` and dry-run/non-executable
- unknown action category blocks
- approval-bypass wording blocks
- disabled capability blocks
- `model_call` does not call a model and does not create authority
- file/process/browser/network/external_send/scheduler/robotics/drone/device requests do not execute
- event output is redacted and in-memory only
- result preserves non-execution invariants
- runtime dependency injection fails closed
- mapping-shaped request support without HumanInput bridge
- no forbidden imports/calls in new kernel modules
- no Sparkbot, Robo-OS, persistence, dispatch, adapter, or tool execution wiring in new kernel modules

## Forbidden surfaces checked

Static tests check the new kernel modules for forbidden imports/calls and forbidden coupling strings related to:

- Sparkbot backend coupling
- Robo-OS wiring
- SQLite/persistence
- network request packages
- subprocess/threading
- dispatch/execution calls
- adapter construction
- file opening

The implementation did not modify forbidden source areas outside `lima/kernel/`.

## Validation result

Validation performed on this branch:

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2391 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only intended branch changes before staging.

## Remaining blockers to true plug-and-play status

This branch proves a minimal importable kernel object and dry-run fail-closed evaluation surface. It is still not true plug-and-play AI OS runtime status.

Remaining blockers:

- no real Guardian enforcement
- no real GuardianDecision authority
- no approval UX or approval enforcement
- no provider/model registry
- no model routing
- no prompt assembly
- no storage or durable Spine ledger
- no HumanInput runtime bridge
- no IntentCompiler runtime
- no shell manifests wired from Sparkbot, Arc Bot, Robo-OS, or other shells
- no adapters
- no tool packs exposed to a model
- no connector/tool/driver execution
- no scheduler/background runtime
- no Robo-OS adapter
- no physical-world safety runtime
- no external package/example shell proving install-and-call behavior from another repository

## Recommended next branch

Recommended next branch:

`harden-lima-minimal-kernel-runtime-invariants`

Goal:

- add more negative tests and fixture cases around malformed metadata, authority claims, capability drift, redaction, event invariants, and import-boundary regressions before expanding runtime behavior

Implementation expansion into providers, storage, real Guardian enforcement, HumanInput bridge, shell wiring, Robo-OS wiring, or physical-world behavior should remain blocked until this minimal kernel surface is hardened and reviewed.
