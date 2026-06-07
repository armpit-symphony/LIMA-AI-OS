# LIMA Discovery Adapter Interface

## Purpose

The discovery adapter interface is a future boundary between `LimaKernel` connection intent classification and any discovery provider.

This branch is design-only. It does not implement simulated discovery, live discovery, scanning, connection attempts, pairing, credential use, sockets, OS network APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT/Matter/mDNS APIs, IoT adapters, Robo-OS adapters, Sparkbot wiring, Arc Bot wiring, background workers, subprocesses, threads, schedulers, persistence, storage, device control, robot/drone control, or physical-world behavior.

The interface must preserve:

- discovery is not connection
- connection is not control
- control is not actuation

## Adapter Tiers

| Tier | Allowed future behavior | Default state now | Risk tier | Required capability | Guardian requirement | HumanInput requirement | Event requirement | Redaction requirement | Can be implemented next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `metadata_only_adapter` | Describe static adapter metadata and supported synthetic surfaces. No discovery. | proposed/design-only | low | `connection_discovery` | Guardian classification before any use | not required for static docs | redacted metadata event only | no raw endpoint values | No; keep as design until simulated path exists |
| `simulated_discovery_adapter` | Return deterministic synthetic/inert discovery surfaces from synthetic request metadata. | eligible after independent audit | low/medium | domain-specific `*_discovery` or `connection_discovery` | Guardian classification required | approval not required for inert fixtures, unless policy marks risk higher | redacted in-memory simulation events | synthetic-only values, no secrets | Yes, only future eligible tier |
| `read_only_local_discovery_adapter` | Future local read-only discovery such as local interfaces or local service metadata. | blocked | medium/high | `network_discovery` or domain-specific discovery | Guardian review required | explicit approval required | redacted event with no raw scan payloads | no raw SSIDs, MAC/IPs, serials, location | No |
| `authenticated_discovery_adapter` | Future credential-ref based discovery against approved systems. | blocked | high | `credential_use` plus domain discovery | Guardian review required | explicit approval required | redacted event with credential_ref only | credential_ref only, never raw credentials | No |
| `physical_endpoint_discovery_adapter` | Future endpoint discovery involving robots, drones, devices, sensors, or physical-world systems. | blocked | critical | `robotics_endpoint_discovery`, `drone_endpoint_discovery`, `device_discovery` | Guardian review required | explicit approval required | physical endpoint event with safety/privacy metadata | no telemetry, location, commands, or identifiers unless approved | No |

Only `simulated_discovery_adapter` may be eligible for the next implementation branch. All live/local/authenticated/physical endpoint adapters remain blocked.

## Proposed Future Protocol Shapes

These are protocol-style design shapes only. They are not implemented in this branch.

```python
# PSEUDO-CODE ONLY. Not implemented.
class DiscoveryAdapterProtocol(Protocol):
    def manifest(self) -> DiscoveryAdapterManifest: ...
    def classify(self, request: DiscoveryAdapterRequest) -> DiscoveryAdapterResult: ...
    def simulate(self, request: DiscoveryAdapterRequest) -> DiscoveryAdapterResult: ...
```

```python
# PSEUDO-CODE ONLY. Not implemented.
@dataclass(frozen=True)
class DiscoveryAdapterManifest:
    adapter_id: str
    adapter_type: str
    adapter_version: str
    supported_connection_types: tuple[str, ...]
    supported_discovery_modes: tuple[str, ...]
    required_capabilities: tuple[str, ...]
    supports_simulation: bool
    supports_live_discovery: bool
    supports_connection_attempt: bool
    supports_pairing: bool
    supports_credentials: bool
    supports_physical_world: bool
    risk_tier: str
    requires_guardian: bool
    requires_human_approval: bool
    redaction_policy: DiscoveryAdapterRedactionPolicy
```

```python
# PSEUDO-CODE ONLY. Not implemented.
@dataclass(frozen=True)
class DiscoveryAdapterCapability:
    capability_name: str
    connection_type: str
    discovery_mode: str
    risk_tier: str
    requires_guardian: bool
    requires_human_approval: bool
    dry_run_only: bool
```

```python
# PSEUDO-CODE ONLY. Not implemented.
@dataclass(frozen=True)
class DiscoveryAdapterRequest:
    request_id: str
    actor_id: str
    shell_id: str
    session_id: str | None
    source_surface: Mapping[str, Any]
    target_hint: str | None
    discovery_mode: str
    dry_run: bool
    simulated_only: bool
    credential_ref: str | None
```

`credential_ref` is reference-only. Raw credentials are never accepted.

```python
# PSEUDO-CODE ONLY. Not implemented.
@dataclass(frozen=True)
class DiscoveryAdapterResult:
    request_id: str
    adapter_id: str
    adapter_type: str
    state: str
    dry_run: bool
    simulated_only: bool
    redacted_summary: str
    event_refs: tuple[str, ...]
    blocked_reason: str | None
    surfaces: tuple[DiscoveryAdapterSurface, ...]
```

```python
# PSEUDO-CODE ONLY. Not implemented.
@dataclass(frozen=True)
class DiscoveryAdapterSurface:
    surface_id: str
    connection_type: str
    discovery_mode: str
    redacted_label: str
    risk_tier: str
    simulated: bool
    connectable: bool
    controllable: bool
    physical_world: bool
```

```python
# PSEUDO-CODE ONLY. Not implemented.
@dataclass(frozen=True)
class DiscoveryAdapterError:
    error_code: str
    blocked_reason: str
    redacted_summary: str
    event_refs: tuple[str, ...]
```

```python
# PSEUDO-CODE ONLY. Not implemented.
@dataclass(frozen=True)
class DiscoveryAdapterRedactionPolicy:
    redact_passwords: bool
    redact_raw_credentials: bool
    redact_tokens: bool
    redact_headers: bool
    redact_pairing_codes: bool
    redact_private_ssids: bool
    redact_bluetooth_macs: bool
    redact_ip_mac_addresses: bool
    redact_serial_numbers: bool
    redact_scan_dumps: bool
    redact_precise_location: bool
    redact_robot_drone_commands: bool
```

## Adapter Lifecycle

Future lifecycle stages:

- `registered`
- `capability_declared`
- `request_classified`
- `guardian_reviewed`
- `human_approval_required`
- `simulated`
- `blocked`
- `disabled`
- `retired`

This branch implements none of these stages. The stages define future state names only.

## Fail-Closed Rules

Future adapter policy must fail closed:

- unknown adapter blocks
- adapter without manifest blocks
- adapter with live discovery enabled blocks unless separately approved
- adapter requiring credentials blocks unless credential-ref support is separately approved
- adapter supporting pairing blocks unless pairing support is separately approved
- adapter supporting physical-world behavior blocks unless physical endpoint policy is separately approved
- adapter that returns raw secrets blocks
- adapter that returns raw scan dumps blocks
- adapter that tries to connect blocks
- adapter that opens sockets blocks
- adapter that starts background workers blocks
- adapter that imports OS/Bluetooth/USB/IoT protocol libraries in a disallowed lane blocks

## Event and Redaction Contract

Future adapter event types:

- `discovery_adapter_registered`
- `discovery_adapter_manifest_loaded`
- `discovery_adapter_request_classified`
- `discovery_adapter_simulation_requested`
- `discovery_adapter_simulation_completed`
- `discovery_adapter_live_discovery_blocked`
- `discovery_adapter_connection_blocked`
- `discovery_adapter_pairing_blocked`
- `discovery_adapter_physical_endpoint_blocked`
- `discovery_adapter_redaction_failed`

Events must not log:

- passwords
- raw credentials
- tokens
- headers
- pairing codes
- raw SSIDs marked private/sensitive
- raw Bluetooth MACs
- raw IP/MAC addresses
- raw serial numbers
- raw scan dumps
- precise physical location
- robot/drone command payloads

Events remain redacted and in-memory only until a separate event/spine persistence contract and implementation is approved.

## Simulated Adapter Future Lane

Next possible implementation branch:

`implement-lima-simulated-discovery-adapter-only`

That branch may only implement a deterministic in-process simulated adapter that:

- accepts synthetic/inert request metadata
- returns synthetic/inert discovery surfaces
- never scans
- never opens sockets
- never calls OS APIs
- never imports Bluetooth/USB/serial/MQTT/Matter/mDNS libraries
- never connects
- never pairs
- never uses credentials
- never controls devices
- never touches physical-world systems
- emits redacted in-memory events only
- preserves dry-run non-execution invariants

No live/local/authenticated/physical endpoint adapter is eligible for that branch.

## Integration Boundary

### `LimaKernel`

Future integration must happen after kernel classification returns a safe dry-run state. The adapter must not bypass `LimaKernel` classification.

### `CapabilityProfile`

Future adapters must declare required capabilities and must not self-authorize. Disabled capabilities block.

### Connection Intent Classification

The classifier remains the first gate. Adapter results cannot turn `blocked` into `proposed` or `approval_required`.

### Guardian Policy

Guardian review is mandatory before any live/local/authenticated/physical endpoint adapter. Simulated adapter work may still carry Guardian stub metadata but cannot create real authority.

### HumanInput Approval Bridge

HumanInput approval is required before future live discovery, credential use, pairing, connection, control, or physical endpoint behavior. This branch does not implement a bridge.

### Event/Spine Logging

Future adapter events are redacted and in-memory only until a durable Spine/event contract is separately approved.

### Sparkbot Workstation

Future Sparkbot Workstation integration may consume redacted simulated adapter results only after shell adapter design. This branch does not wire Sparkbot.

### Arc Bot Shell

Future Arc Bot shell integration may request simulated discovery metadata only after shell adapter design. This branch does not wire Arc Bot.

### LIMA-Robo-OS

Future Robo-OS endpoint discovery is a physical endpoint boundary and remains blocked until physical endpoint policy, dry-run semantics, emergency-stop semantics, and Guardian/HumanInput approval requirements are separately approved. This branch does not wire Robo-OS.

## Example Pseudo-Flow

Pseudo-flow only:

```text
1. Kernel receives simulated Bluetooth discovery request metadata.
2. Connection intent classification returns proposed or approval_required.
3. Future simulated adapter manifest is checked.
4. Future simulated adapter returns synthetic surfaces.
5. Redacted in-memory event is emitted.
6. No scan, connect, pair, credential use, control, or actuation occurs.
```

Pseudo-code only:

```python
# PSEUDO-CODE ONLY. Not implemented.
request = DiscoveryAdapterRequest(
    request_id="req-sim-ble-001",
    actor_id="actor-ref",
    shell_id="test-shell",
    session_id="session-ref",
    source_surface={"surface": "test_fixture"},
    target_hint="synthetic_ble_fixture",
    discovery_mode="simulated",
    dry_run=True,
    simulated_only=True,
    credential_ref=None,
)

manifest = adapter.manifest()
result = adapter.simulate(request)
# result contains synthetic surfaces only.
# no scan/connect/pair/control occurs.
```

## Design Verdict

The adapter interface is ready for independent audit.

It is not approval to implement simulated discovery yet. It is not approval for live discovery, scanning, connection attempts, pairing, credentials, sockets, OS APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT/Matter/mDNS APIs, IoT adapters, Robo-OS adapters, Sparkbot wiring, Arc Bot wiring, background work, storage, device control, robot/drone control, or physical-world behavior.
