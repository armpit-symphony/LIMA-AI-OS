# LIMA Simulated Discovery Adapter Implementation Audit

## Branch

`implement-lima-simulated-discovery-adapter-only`

## Base commit

`629fccda83f3e33f931300427c2122e9539e5911`

## Files Changed

- `lima/kernel/discovery.py`
- `lima/kernel/__init__.py`
- `tests/test_lima_simulated_discovery_adapter.py`
- `docs/audits/LIMA_SIMULATED_DISCOVERY_ADAPTER_IMPLEMENTATION_AUDIT.md`

## Public Imports Exposed

New public imports are exposed only from `lima.kernel`:

- `DiscoveryAdapterManifest`
- `DiscoveryAdapterRequest`
- `DiscoveryAdapterSurface`
- `DiscoveryAdapterResult`
- `SimulatedDiscoveryAdapter`

Top-level `lima` remains unchanged.

## Adapter API Summary

The implementation adds a deterministic in-process simulated adapter:

- `SimulatedDiscoveryAdapter.manifest`
- `SimulatedDiscoveryAdapter.simulate(request)`

The adapter accepts `DiscoveryAdapterRequest` or mapping-shaped synthetic metadata. It is not invoked automatically by `LimaKernel.evaluate(...)`, and there is no live adapter registry, hidden dispatch, scheduler, worker, or background execution.

## Synthetic Surface Behavior

Allowed simulated connection types return one deterministic synthetic surface:

- `wifi` -> `simulated-wifi-preview`
- `ble` -> `simulated-ble-preview`
- `lan` -> `simulated-lan-preview`
- `iot` -> `simulated-iot-preview`

Returned surfaces are explicitly marked:

- `synthetic: true`
- `inert: true`
- `simulated: true`
- `connectable: false`
- `controllable: false`
- `physical_world: false`

No real discovery, scan data, SSID, MAC address, IP address, serial number, physical location, credential, pairing code, device endpoint, or provider payload is returned.

## Rejection Behavior

The adapter blocks:

- `dry_run=False`
- `simulated_only=False`
- live discovery modes
- unsupported connection types
- connection attempts
- pairing requests
- credential refs
- raw credential-like fields
- robot, drone, device-control, or physical-world actuator paths

Blocked results return no surfaces and preserve the same non-execution invariants as proposed simulated results.

## Non-Execution Invariants

Every result preserves:

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

## Event/Redaction Behavior

The adapter returns redacted in-memory event-style metadata only. Events are result-local dataclass values, not durable records.

Events are marked:

- `durable: false`
- `in_memory_only: true`
- `contains_secret: false`
- `contains_raw_scan_dump: false`
- `contains_physical_location: false`

Events and results do not echo raw target hints, raw metadata payloads, raw credentials, tokens, headers, pairing codes, scan dumps, serial numbers, or physical locations.

## Forbidden Surfaces Checked

The implementation does not introduce:

- live scanning
- live discovery
- connection attempts
- pairing
- credential use or storage
- sockets or OS network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- IoT adapters
- Robo-OS adapters
- Sparkbot wiring
- Arc Bot wiring
- storage/persistence
- provider/model calls
- real Guardian enforcement
- real HumanInput bridge
- approval enforcement
- background workers
- subprocesses
- threads
- scheduler
- device control
- robot/drone control
- physical-world behavior

Focused tests statically check the new module for forbidden imports, calls, and wiring strings.

## Tests Added

Added `tests/test_lima_simulated_discovery_adapter.py` covering:

- public imports from `lima.kernel`
- deterministic fake surfaces for synthetic dry-run requests
- synthetic/inert/simulated surface flags
- rejection of non-simulated requests
- rejection of `dry_run=False`
- rejection of live discovery modes
- rejection of connection attempts
- rejection of pairing
- rejection of credential refs
- rejection of raw password/token/key/header-like fields
- rejection of robot/drone/physical-world control metadata
- rejection of unsupported connection types
- redacted in-memory event-style metadata
- non-execution invariants
- forbidden imports/calls/wiring checks

## Validation Result

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2460 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only intended branch changes before staging.

## Remaining Blockers Before Any Live Discovery

Before any live discovery can be considered, LIMA still needs separately approved design and audit lanes for:

- adapter registration and manifest policy
- Guardian classification for live/local/authenticated discovery
- HumanInput approval bridge semantics
- credential-ref-only handling without raw credential exposure
- redaction failure handling
- event/spine persistence policy
- socket/API/library allowlist policy
- Robo-OS and physical endpoint safety policy
- emergency-stop and simulation-first physical-world semantics

This branch is not ready for live discovery, scanning, connection attempts, pairing, credential use, device sessions, Robo-OS access, robotics, drones, or physical-world behavior.

## Recommended Next Branch

`audit-lima-simulated-discovery-adapter`
