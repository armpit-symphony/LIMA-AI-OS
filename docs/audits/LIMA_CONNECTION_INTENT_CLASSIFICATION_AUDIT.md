# LIMA Connection Intent Classification Audit

## Branch

`audit-lima-connection-intent-classification`

## Base commit

`3b1c411cc81685a29a1f8c9a49376e54ef5f5c79`

## Scope

This audit reviews the connection intent classification runtime slice before any simulated discovery adapter work begins.

No new behavior is implemented by this branch. This branch does not modify `lima/`, `tests/`, `tests/support/`, adapters, providers, storage, Sparkbot wiring, Arc Bot wiring, Robo-OS wiring, or runtime behavior.

## Audit verdict

PASS.

The connection intent classification slice remains non-executing, fail-closed, redacted, in-memory only, and safe for a later adapter interface design lane.

The branch is ready for adapter interface design. It is not ready for simulated discovery implementation until adapter interface design is complete. It is not ready for live discovery, scanning, connection attempts, pairing, credential use, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## 1. Public API status

`from lima.kernel import LimaKernel` works.

Direct verification performed:

- `import lima`
- `from lima.kernel import LimaKernel`
- `lima.__all__ == ["contracts"]`
- `LimaKernel.__name__ == "LimaKernel"`

Top-level `lima` remained unchanged. `lima.__all__` still exposes only `contracts`.

Recognized connection/discovery capability names:

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
- `device_control`
- `robotics_actuation`
- `drone_actuation`
- `physical_world_actuation`

Unsafe public exports added:

- None observed at top-level `lima`.
- `lima.kernel` exports remain kernel-scoped and non-executing.

## 2. Classification behavior

Observed behavior from source and tests:

| Case | Expected classification | Audit finding |
| --- | --- | --- |
| passive/local metadata preview | `proposed` if capability enabled and no live/sensitive/credential/pairing/session/control/physical claim | Covered and passing |
| simulated discovery | `proposed` or `approval_required`, dry-run only | Covered and passing |
| WiFi discovery | disabled capability blocks; simulated enabled case remains dry-run | Covered and passing |
| Bluetooth/BLE discovery | `proposed` or `approval_required`, no API calls | Covered and passing |
| LAN/network scan | `blocked` for live scan wording | Covered and passing |
| USB/serial discovery | `approval_required` or `blocked`, never executes | Covered and passing |
| MQTT/Matter/mDNS discovery | `approval_required` or `blocked`, never executes | Covered and passing |
| generic IoT discovery | capability recognized; safe path remains metadata-only | Covered by capability classification |
| connection attempt | `blocked` | Covered and passing |
| device pairing | `blocked` | Covered and passing |
| credential use | `blocked` | Covered and passing |
| connector/device session | `blocked` | Covered through session wording classifier |
| IoT control | `blocked` | Covered and passing |
| device control | `blocked` | Covered and passing |
| robot/drone endpoint discovery | `blocked` | Covered and passing |
| physical-world actuation | `blocked` | Covered and passing |
| auto-connect wording | `blocked` | Covered and passing |
| try-everything wording | `blocked` | Covered and passing |
| unknown connection type | `blocked` | Covered and passing |
| disabled capability | `blocked` | Covered and passing |

No live discovery, scan, connection, pairing, credential use, session open, device control, robot/drone control, or physical-world behavior is present.

## 3. Non-execution invariants

Tests verify connection/discovery results preserve:

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

Audit finding:

- PASS. The result model is explicit and tests cover these invariants for connection/discovery cases.

## 4. Event/redaction behavior

Events are in-memory only.

Observed connection event names:

- `connection_discovery_requested`
- `connection_discovery_proposed`
- `connection_discovery_blocked`
- `connection_attempt_requested`
- `connection_attempt_blocked`
- `device_pairing_requested`
- `device_pairing_blocked`
- `physical_endpoint_detected`
- `physical_endpoint_blocked`

Tests confirm:

- events are local to the `LimaKernel` instance
- events report `in_memory_only=True`
- events report `durable=False`
- events do not include password text
- events do not include token text
- events do not include IP-like test text
- events do not include pairing-code test text
- events do not include unsafe raw command payload text through existing redaction tests

Audit finding:

- PASS for current metadata-only event summaries.
- Events use state/category/reason metadata, not raw scan output or live discovery payloads.

No durable persistence exists. No database/file event store exists.

## 5. Forbidden imports/surfaces

Static tests inspect kernel modules for forbidden imports/calls covering:

- socket/network APIs
- Bluetooth/BLE libraries
- USB/serial libraries
- MQTT/Matter/mDNS libraries
- subprocess
- threading/background worker modules
- filesystem open calls
- database/storage backends
- provider/model libraries
- direct scan/discover/connect/pair/open/socket calls

String tests guard against:

- Sparkbot backend strings
- Arc Bot strings
- Robo-OS adapter strings
- adapter construction strings
- request/network package strings
- serial/MQTT/mDNS implementation strings
- persistence strings
- subprocess/threading/socket strings

Audit finding:

- PASS. The new source uses classification constants and string matching only. No live imports, API calls, adapters, sockets, persistence, subprocesses, threads, or external calls are introduced.

## 6. Test coverage

Tests confirm:

- safe passive metadata preview
- simulated discovery
- disabled capability block
- broad network scan block
- connection attempt block
- pairing block
- raw credential wording block
- auto-connect block
- try-everything block
- unknown type block
- robot/drone endpoint block
- physical-world block
- redacted/in-memory events
- forbidden imports/surfaces

Primary test file:

- `tests/test_lima_connection_intent_classification.py`

Supporting invariant test file:

- `tests/test_lima_minimal_kernel_runtime.py`

Audit finding:

- PASS. Coverage is sufficient for a classification slice audit.

## 7. Readiness decision

Ready for next design lane:

`design-lima-discovery-adapter-interface`

Not ready for:

- simulated discovery implementation
- live discovery
- scanning
- connection attempts
- pairing
- credential use
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Validation result

Validation performed on this branch:

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2433 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only the intended audit report before staging.

## Recommended next branch

`design-lima-discovery-adapter-interface`

Do not proceed to simulated discovery implementation until the adapter interface is designed and reviewed.

Safe path:

```text
audit-lima-connection-intent-classification
-> design-lima-discovery-adapter-interface
-> audit-lima-discovery-adapter-interface
-> implement-lima-simulated-discovery-adapter-only
```
