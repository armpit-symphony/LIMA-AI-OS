# LIMA Simulated Discovery Adapter Audit

## Branch

`audit-lima-simulated-discovery-adapter`

## Base commit

`616431799df4410d7982f571553852ac02608cde`

## Scope

This audit reviews the deterministic simulated discovery adapter implementation before any kernel-to-adapter wiring, adapter registry, or additional adapter work begins.

This branch does not implement behavior. It does not modify `lima/`, tests, adapter implementation files, provider/model files, storage/persistence files, Sparkbot wiring, Arc Bot wiring, Robo-OS wiring, runtime behavior, or physical-world behavior.

## Audit Verdict

PASS.

The simulated discovery adapter remains deterministic, explicit, in-process, synthetic/inert, result-local, redacted, and non-executing. It is ready for the next design lane, `design-lima-kernel-simulated-discovery-wiring`.

It is not ready for kernel auto-dispatch implementation until the wiring design is complete and reviewed. It is not ready for live discovery, scanning, connection attempts, pairing, credential use, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## 1. Public API Status

`from lima.kernel import SimulatedDiscoveryAdapter` works through `lima/kernel/__init__.py`.

The following simulated adapter contracts are safely exported from `lima.kernel`:

- `DiscoveryAdapterManifest`
- `DiscoveryAdapterRequest`
- `DiscoveryAdapterSurface`
- `DiscoveryAdapterResult`
- `SimulatedDiscoveryAdapter`

Top-level `lima` remains unchanged and still exposes only:

- `contracts`

No unsafe public exports were added. `DiscoveryAdapterEvent` remains internal to `lima.kernel.discovery` and is not re-exported from `lima.kernel`.

## 2. Adapter Behavior

`SimulatedDiscoveryAdapter.simulate(...)` is deterministic:

- identical synthetic dry-run requests return identical result dictionaries
- event refs are deterministic result-local refs
- synthetic surface IDs are fixed by connection type

Accepted successful request shape:

- metadata-only request object or mapping
- `dry_run=True`
- `simulated_only=True`
- simulated discovery mode
- supported synthetic connection type: `wifi`, `ble`, `lan`, or `iot`

Returned surfaces are synthetic/inert only:

- `simulated-wifi-preview`
- `simulated-ble-preview`
- `simulated-lan-preview`
- `simulated-iot-preview`

Each returned surface is marked:

- `synthetic: true`
- `inert: true`
- `simulated: true`
- `connectable: false`
- `controllable: false`
- `physical_world: false`

The adapter rejects:

- live discovery modes
- connection attempts
- pairing
- credential refs
- raw credential-like fields
- unsupported connection types
- robot/drone/physical-world requests

The adapter does not open sessions, perform discovery, scan, pair, connect, or control devices.

## 3. Non-Execution Invariants

All proposed and blocked adapter results preserve:

- `executable: false`
- `execution_allowed: false`
- `side_effects_allowed: false`
- `dispatch_allowed: false`
- `persistence_allowed: false`
- `dry_run: true`
- `simulated_only: true`
- `live_discovery_executed: false`
- `connection_attempted: false`
- `pairing_attempted: false`
- `credentials_used: false`
- `session_opened: false`
- `device_control_executed: false`
- `physical_world_executed: false`

Audit finding:

- PASS. The result dataclass defaults enforce non-execution posture, and tests assert the invariants across success and rejection paths.

## 4. Event/Redaction Behavior

Event-style metadata is result-local only. The adapter does not write events to disk, database, queue, scheduler, service, socket, or external sink.

Events are marked:

- `durable: false`
- `in_memory_only: true`
- `contains_secret: false`
- `contains_raw_scan_dump: false`
- `contains_physical_location: false`

Result and event payloads do not echo raw request metadata or raw target hints. Tests confirm credential-like target content is not echoed in result dictionaries.

The implementation does not log:

- raw scan dumps
- passwords
- raw credentials
- tokens
- headers
- pairing codes
- raw SSIDs marked private/sensitive
- raw Bluetooth MACs
- raw IP/MAC addresses
- raw serial numbers
- physical location
- robot/drone command payloads

Audit finding:

- PASS. Redaction is conservative for this simulated-only lane because raw request payloads are not reflected in returned summaries or events.

## 5. Forbidden Imports/Surfaces

The simulated adapter module imports only:

- `dataclasses`
- `typing`

No usage was found in `lima/kernel/discovery.py` for:

- socket/network APIs
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

Audit finding:

- PASS. Focused tests statically check the module for forbidden imports, forbidden calls, and live/shell wiring strings.

## 6. Kernel Integration Boundary

No `LimaKernel.evaluate(...)` auto-dispatch was added.

No hidden adapter registry was added.

No background adapter dispatch exists.

The simulated adapter remains manually callable and explicit only:

- caller instantiates `SimulatedDiscoveryAdapter`
- caller calls `simulate(...)`
- adapter returns a dry-run result

Audit finding:

- PASS. `lima/kernel/kernel.py` does not import or call `SimulatedDiscoveryAdapter`.

## 7. Test Coverage

`tests/test_lima_simulated_discovery_adapter.py` covers:

- public imports from `lima.kernel`
- successful deterministic simulated discovery
- fake WiFi/BLE/LAN/IoT-style surfaces as synthetic/inert only
- rejection of non-simulated requests
- rejection of `dry_run=False`
- rejection of live discovery modes
- rejection of connection attempts
- rejection of pairing
- rejection of credential refs
- rejection of raw credential fields
- rejection of unsupported types
- rejection of robot/drone/physical-world requests
- non-execution invariants
- redacted/result-local event metadata
- forbidden imports/surfaces

Audit finding:

- PASS. Coverage matches the required simulated-only lane. It does not test live discovery because live discovery remains forbidden.

## 8. Readiness Decision

Ready for:

- `design-lima-kernel-simulated-discovery-wiring`

Not ready for:

- kernel auto-dispatch implementation
- adapter registry implementation
- live discovery
- scanning
- connection attempts
- pairing
- credential use
- sockets
- OS APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- IoT adapters
- Robo-OS access
- Sparkbot wiring
- Arc Bot wiring
- device control
- robotics
- drones
- physical-world behavior

PASS condition:

- The adapter is purely simulated/inert/non-executing, and no live discovery or connection surfaces exist.

## Key Findings

- Public imports are narrow and shell-facing through `lima.kernel`.
- Top-level `lima` remains unchanged.
- The adapter returns deterministic synthetic surfaces only.
- Rejection behavior is fail-closed for live modes, connection, pairing, credentials, unsupported types, and physical-world requests.
- Results preserve dry-run non-execution invariants.
- Events are result-local, redacted, and non-durable.
- There is no kernel auto-dispatch, hidden adapter registry, background dispatch, or live adapter behavior.

## Validation Result

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2460 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only `docs/audits/LIMA_SIMULATED_DISCOVERY_ADAPTER_AUDIT.md` before staging.

## Recommended Next Branch

`design-lima-kernel-simulated-discovery-wiring`

The next branch must be design-only and should define how `LimaKernel` may explicitly route already-classified simulated discovery requests to the simulated adapter later, without auto-dispatch, live discovery, connection attempts, pairing, credentials, sockets, Robo-OS access, device control, robotics, drones, or physical-world behavior.
