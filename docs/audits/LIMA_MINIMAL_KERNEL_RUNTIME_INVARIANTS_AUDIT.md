# LIMA Minimal Kernel Runtime Invariants Audit

## Branch

`harden-lima-minimal-kernel-runtime-invariants`

## Base commit

`01e762394f5ed70f6aca1379826785396dd969bb`

## Scope

This branch audits and hardens the minimal non-executing `LimaKernel` runtime slice. It does not add live WiFi, Bluetooth, IoT, Robo-OS, device, network, connection discovery, provider/model routing, storage, persistence, approval enforcement, shell wiring, adapter behavior, background work, or physical-world behavior.

## Files changed

- `lima/kernel/kernel.py`
- `tests/test_lima_minimal_kernel_runtime.py`
- `docs/audits/LIMA_MINIMAL_KERNEL_RUNTIME_INVARIANTS_AUDIT.md`

## Import confirmation

`from lima.kernel import LimaKernel` is covered by `tests/test_lima_minimal_kernel_runtime.py`.

The public import remains scoped to `lima.kernel`. Top-level `lima` export behavior is unchanged.

## Dry-run invariant confirmation

The test helper `_assert_non_execution_invariants(...)` confirms every covered `LimaKernel.evaluate(...)` result preserves:

- `executable=False`
- `execution_allowed=False`
- `side_effects_allowed=False`
- `dispatch_allowed=False`
- `persistence_allowed=False`
- `dry_run=True`
- `model_calls_executed=False`
- `physical_world_executed=False`
- `model_calls_allowed=False`
- `physical_world_allowed=False`
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

## Hardened capability behavior

Tests cover:

- approval-bypass wording blocks
- unknown actions block
- disabled capabilities block
- `model_call` returns `approval_required` without model execution
- `connector_read` returns `approval_required` without connector access
- `connector_write` returns `approval_required` without connector mutation
- `external_send` returns `approval_required` without sending
- `file_write` returns `approval_required` without file mutation
- `process_execute` blocks
- `browser_control` returns `approval_required` without browser control
- `device_control` blocks
- `robotics_actuation` blocks
- `drone_actuation` blocks
- `scheduler_run` returns `approval_required` without scheduler/background work

The expected behavior is metadata-only: `blocked` or `approval_required`, never execution.

## Connection/discovery hardening

This branch adds explicit fail-closed detection for connection/discovery wording in already-normalized metadata. These terms now block until a separate design-only connection discovery contract exists:

- WiFi
- Bluetooth
- IoT
- LAN
- BLE
- serial
- USB
- MQTT
- Matter
- mDNS
- pairing
- scan
- discovery/discover
- connect/connection/auto-connect

The branch does not implement discovery. It does not scan, pair, connect, auto-connect, open ports, access networks, use credentials, use sockets, or call adapters.

## Event behavior

Existing tests confirm in-memory events remain:

- local to the `LimaKernel` instance
- redacted
- `in_memory_only=True`
- `durable=False`
- free of raw secrets, credentials, unsafe command payloads, and raw prompts

This branch adds no persistence, file writes, database writes, event flushing, workers, queues, daemons, subprocesses, threads, sockets, scans, adapters, or external calls.

## Forbidden surfaces checked

Static tests continue to check new minimal kernel modules for forbidden imports/calls and forbidden coupling strings, including:

- Sparkbot backend wiring
- Robo-OS wiring
- persistence/SQLite
- request/network packages
- sockets
- subprocesses
- threads
- dispatch/execution calls
- scan/connect calls
- adapter construction
- file opening

No forbidden file areas were modified.

## Validation result

Validation performed on this branch:

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2407 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only intended branch changes before staging.

## Remaining blockers

The minimal kernel is still intentionally non-executing. Remaining blockers before true connection/device/runtime behavior:

- no connection discovery contract yet
- no Guardian-classified discovery request shape
- no HumanInput approval flow for discovery/connection
- no credential handling contract
- no provider/model registry
- no persistent Spine/event ledger
- no shell integration examples
- no Robo-OS adapter contract implementation
- no emergency-stop semantics implementation
- no real approval enforcement

## Recommended next branch

`design-lima-connection-discovery-contract`

That branch must remain design-only and define how LIMA will eventually discover WiFi, Bluetooth, LAN, IoT, USB, serial, BLE, MQTT, Matter, mDNS, local devices, Robo-OS endpoints, and other connection surfaces without connecting automatically.

Discovery should remain proposed/dry-run/read-only until separately approved. Connection attempts, pairing, credential use, device control, IoT commands, robotics, drones, and physical-world behavior must require Guardian classification and explicit HumanInput approval.
