# LIMA Connection Intent Classification Implementation Audit

## Branch

`implement-lima-connection-intent-classification`

## Base commit

`f410415a597ec7dda6c67b81daec4cbe9007ec74`

## Files changed

- `lima/kernel/kernel.py`
- `lima/kernel/plugin_contract.py`
- `tests/test_lima_minimal_kernel_runtime.py`
- `tests/test_lima_connection_intent_classification.py`
- `docs/audits/LIMA_CONNECTION_INTENT_CLASSIFICATION_IMPLEMENTATION_AUDIT.md`

## Classification behavior summary

This branch teaches the minimal `LimaKernel` to classify already-normalized connection/discovery intent metadata into dry-run results only.

Supported result states remain:

- `proposed`
- `approval_required`
- `blocked`

Classification behavior:

- passive local metadata preview with enabled capability can return `proposed`
- simulated discovery can return `proposed` or `approval_required`
- read-only local discovery returns `approval_required` unless it is passive/simulated and low-risk
- authenticated or sensitive discovery returns `approval_required` or `blocked`
- unauthenticated network scan returns `blocked`
- disabled capability returns `blocked`
- unknown connection type returns `blocked`
- connection attempt returns `blocked`
- device pairing returns `blocked`
- credential use returns `blocked`
- connector/device session request returns `blocked`
- IoT control returns `blocked`
- device control returns `blocked`
- robot/drone endpoint discovery returns `blocked`
- physical-world actuation returns `blocked`
- auto-connect wording returns `blocked`
- try-everything wording returns `blocked`

No scan, discovery execution, connection, pairing, credential use, session open, device control, model call, provider call, adapter call, or physical-world behavior is performed.

## Capability names added/recognized

Added to `CapabilityProfile`:

- `connection_discovery`
- `network_discovery`
- `wifi_discovery`
- `bluetooth_discovery`
- `ble_discovery`
- `lan_discovery`
- `usb_discovery`
- `serial_discovery`
- `iot_discovery`
- `mdns_discovery`
- `mqtt_discovery`
- `matter_discovery`
- `device_discovery`
- `robotics_endpoint_discovery`
- `drone_endpoint_discovery`
- `connection_attempt`
- `device_pairing`
- `credential_use`
- `iot_control`
- `physical_world_actuation`

Existing capabilities also remain recognized:

- `device_control`
- `robotics_actuation`
- `drone_actuation`

## Event behavior

Connection classification emits redacted in-memory events only.

New event names used by the classifier:

- `connection_discovery_requested`
- `connection_discovery_proposed`
- `connection_discovery_blocked`
- `connection_attempt_requested`
- `connection_attempt_blocked`
- `device_pairing_requested`
- `device_pairing_blocked`
- `physical_endpoint_detected`
- `physical_endpoint_blocked`

Events remain local to the `LimaKernel` instance. No durable persistence, file write, database write, queue, worker, thread, subprocess, scheduler, socket, adapter call, or external call is added.

## Redaction behavior

Events and result summaries use state/category/reason metadata only. Tests assert event output does not include raw credential, token, header, IP-like, or pairing-code text from caller summaries.

Forbidden event/result content remains:

- passwords
- tokens
- headers
- raw SSIDs marked private/sensitive
- raw Bluetooth MACs
- raw IP/MAC addresses
- pairing codes
- credentials
- raw scan dumps
- device serial numbers
- physical location
- robot/device command payloads

## Non-execution guarantees

All tested results preserve:

- `executable=False`
- `execution_allowed=False`
- `side_effects_allowed=False`
- `dispatch_allowed=False`
- `persistence_allowed=False`
- `dry_run=True`
- `model_calls_executed=False`
- `live_discovery_executed=False`
- `connection_attempted=False`
- `pairing_attempted=False`
- `credentials_used=False`
- `session_opened=False`
- `device_control_executed=False`
- `physical_world_executed=False`
- `tool_execution_allowed=False`
- `driver_execution_allowed=False`
- `scheduler_active=False`
- `external_calls_allowed=False`

The branch does not add live scanning, live discovery, connection attempts, pairing, credential use/storage, sockets, OS network APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT/Matter/mDNS implementation, IoT adapters, Robo-OS adapters, Sparkbot wiring, Arc Bot wiring, storage/persistence, provider/model calls, real Guardian enforcement, HumanInput bridge, approval enforcement, background workers, subprocesses, threads, schedulers, device control, robot/drone control, or physical-world behavior.

## Forbidden surfaces checked

Tests statically inspect the kernel modules for forbidden imports/calls covering:

- sockets
- subprocesses
- threads
- persistence/SQLite
- network request libraries
- Bluetooth/BLE libraries
- USB/serial libraries
- MQTT/Matter/mDNS libraries
- provider/model libraries
- background/concurrency modules
- direct `scan`, `discover`, `connect`, `pair`, `open`, `socket`, `eval`, and `exec` calls

String checks also guard against Sparkbot, Arc Bot, Robo-OS, adapter, MQTT, serial, socket, subprocess, thread, and persistence wiring strings in the minimal kernel modules.

## Tests added

Added `tests/test_lima_connection_intent_classification.py`.

Coverage includes:

- safe passive metadata preview with enabled capability returns `proposed` and dry-run only
- simulated WiFi discovery returns safe dry-run result
- WiFi discovery with disabled capability blocks
- Bluetooth/BLE discovery remains dry-run only and does not call APIs
- LAN scan blocks
- USB/serial discovery never executes
- MQTT/Matter/mDNS discovery never executes
- connection attempt blocks
- device pairing blocks
- credential wording blocks
- auto-connect blocks
- try-everything blocks
- unknown connection type blocks
- IoT control blocks
- device control blocks
- robot/drone endpoint discovery blocks
- physical-world actuation blocks
- event output is redacted and in-memory only
- no forbidden live API imports/calls are introduced
- no Sparkbot, Arc Bot, Robo-OS, adapter, persistence, or external-call wiring strings are introduced

Hardened `tests/test_lima_minimal_kernel_runtime.py` to assert new optional non-execution fields remain false.

## Validation result

Validation performed on this branch:

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2433 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only intended branch changes before staging.

## Remaining blockers before simulated discovery adapter

Before any simulated discovery adapter is considered, LIMA still needs:

- independent audit of this classification slice
- a fixture matrix for discovery vs connection vs control vs actuation
- redaction hardening for SSIDs, MAC/IP-like values, serial numbers, pairing codes, and location metadata
- Guardian request shape for discovery review
- HumanInput approval wording and evidence requirements
- dry-run adapter contract that proves it cannot call live APIs
- explicit operator approval for any adapter-like work

Live discovery, scanning, connection, pairing, credential use, device access, network access, Robo-OS access, and physical-world behavior remain blocked.

## Recommended next branch

`audit-lima-connection-intent-classification`

Do not proceed directly to simulated discovery until the classification slice is independently audited.
