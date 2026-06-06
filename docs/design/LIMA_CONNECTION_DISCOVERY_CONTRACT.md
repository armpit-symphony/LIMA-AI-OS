# LIMA Connection Discovery Contract

## Purpose

This document defines the future LIMA connection discovery contract for WiFi, Bluetooth, LAN, IoT, USB, serial, BLE, MQTT, Matter, mDNS, local devices, Robo-OS endpoints, and other connection surfaces.

This branch is design-only. It does not implement scanning, discovery, connection attempts, pairing, sockets, OS network APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT, Matter, mDNS, IoT adapters, Robo-OS adapters, Sparkbot wiring, Arc Bot wiring, background workers, subprocesses, threads, schedulers, external calls, credential storage, device behavior, robot behavior, drone behavior, or physical-world behavior.

## Core Invariant

Discovery is not connection. Connection is not control. Control is not actuation.

Definitions:

- Discovery: metadata-only proposal that a future shell or operator may want to inspect available connection surfaces.
- Connection: a future operation that attempts to establish a live channel to a network, endpoint, adapter, service, bus, device, robot, drone, or physical-world system.
- Control: a future operation that sends commands or mutates state over an established connection.
- Actuation: a future physical-world effect, including robot movement, drone behavior, device control, hardware IO, or environmental action.

The minimal kernel must not collapse these levels. Each level requires a stricter Guardian classification and HumanInput approval boundary than the prior level.

## Required Future Flow

Future connection discovery work must follow this sequence:

```text
Request -> Classify -> Capability Check -> Discovery Proposal -> Guardian Review -> HumanInput Approval -> Dry Run -> Live Connection Later Only If Separately Approved
```

This branch defines that flow only. It does not implement any step.

## Boundary Levels

### Level 0: Request Metadata

The caller may provide already-normalized metadata describing a possible discovery need.

Allowed future metadata fields:

- `request_id`
- `shell_id`
- `actor_id`
- `session_id`
- `surface`
- `discovery_domain`
- `requested_scope`
- `target_ref`
- `privacy_class`
- `risk_class`
- `source_refs`

Forbidden metadata:

- credentials
- passwords
- tokens
- headers
- raw scan payloads
- raw adapter payloads
- raw hardware identifiers when privacy-sensitive
- raw sensor data
- unsafe commands
- connection strings with secrets

### Level 1: Classification

Future kernel classification may label metadata as one of:

- `discovery_proposal`
- `connection_attempt`
- `control_request`
- `actuation_request`
- `unknown_connection_surface`

Expected classification behavior:

- `discovery_proposal` may be `proposed` only if it remains metadata-only and dry-run.
- `connection_attempt` must be `approval_required` or `blocked`.
- `control_request` must be `approval_required` or `blocked`.
- `actuation_request` must be `blocked` until a separate physical-world safety lane exists.
- unknown surfaces must be `blocked`.

### Level 2: Capability Check

Future capability profile names:

- `connection_discovery`
- `connection_attempt`
- `credential_use`
- `device_enumeration`
- `network_scan`
- `bluetooth_scan`
- `usb_serial_probe`
- `iot_protocol_probe`
- `robo_os_endpoint_probe`
- `device_control`
- `robotics_actuation`
- `drone_actuation`

Default behavior:

- `connection_discovery`: proposed/dry-run metadata only after Guardian review design exists.
- `connection_attempt`: approval_required or blocked.
- `credential_use`: blocked until credential contract exists.
- `device_enumeration`: approval_required or blocked.
- `network_scan`: blocked until a separate non-executing classifier is approved.
- `bluetooth_scan`: blocked.
- `usb_serial_probe`: blocked.
- `iot_protocol_probe`: blocked.
- `robo_os_endpoint_probe`: blocked.
- `device_control`: blocked.
- `robotics_actuation`: blocked.
- `drone_actuation`: blocked.

### Level 3: Discovery Proposal

A future discovery proposal is a redacted statement of intent, not a scan result.

Allowed proposal output:

- proposed domain, such as `wifi`, `bluetooth`, `lan`, `usb`, `serial`, `iot`, `robo_os`
- requested scope
- risk class
- approval requirement
- privacy warning
- dry-run state
- no execution claims

Forbidden proposal output:

- live device lists
- live SSIDs
- MAC addresses
- IP scans
- BLE advertisements
- serial port enumeration
- USB descriptor dumps
- MQTT broker probes
- Matter fabric data
- mDNS service responses
- Robo-OS endpoint calls
- credentials
- connection handles
- control handles

### Level 4: Guardian Review

Guardian must classify discovery separately from connection, control, and actuation.

Future Guardian review must answer:

- Is this discovery-only?
- Is a live scan implied?
- Is credential use implied?
- Is pairing implied?
- Is device control implied?
- Is physical-world behavior implied?
- Is the target environment private, customer-owned, regulated, safety-critical, or unknown?
- Does the actor/session/shell have permission to request this category?

This branch does not implement Guardian review.

### Level 5: HumanInput Approval

HumanInput approval is required before any future live discovery or connection attempt.

Approval must be explicit about:

- domain
- scope
- target environment
- whether credentials may be used
- whether pairing may be attempted
- whether devices may be touched
- whether the operation is dry-run only
- retention/redaction expectations

This branch does not implement HumanInput approval or approval enforcement.

### Level 6: Dry Run

Future dry-run behavior may describe what would be checked, but must not scan or connect.

Allowed dry-run result:

- checklist of intended checks
- requested permissions
- privacy impact summary
- Guardian constraints
- operator approval requirement
- redacted event references

Forbidden dry-run result:

- live scan output
- network calls
- socket operations
- Bluetooth/BLE API calls
- USB/serial API calls
- MQTT/Matter/mDNS calls
- Robo-OS calls
- credentials
- connection handles
- control handles

### Level 7: Live Connection Later Only If Separately Approved

Live connection is explicitly out of scope for this branch and any immediate classification-only implementation branch.

Future live connection requires a separate branch, threat model, Guardian classification, HumanInput approval, credential handling contract, redaction contract, rollback plan, and explicit operator approval.

## Domain Notes

### WiFi and LAN

Design-only. No SSID scans, IP scans, ARP, DNS, mDNS, sockets, pings, routing table reads, interface enumeration, or OS network APIs.

### Bluetooth and BLE

Design-only. No adapter enumeration, BLE scans, pairing, service discovery, GATT calls, or Bluetooth APIs.

### USB and Serial

Design-only. No port enumeration, device descriptor reads, serial open, USB probing, driver calls, or OS device APIs.

### MQTT, Matter, mDNS, and IoT

Design-only. No broker probing, subscription, publish, fabric lookup, pairing, service discovery, multicast, endpoint calls, or protocol adapters.

### Robo-OS Endpoints

Design-only. No Robo-OS imports, adapters, MCP calls, endpoint probing, simulator calls, robot telemetry calls, emergency-stop implementation, or driver behavior.

### Devices, Robots, Drones, and Physical-World Systems

Design-only. Device control, robotics actuation, drone actuation, and physical-world behavior remain blocked.

## Event and Privacy Rules

Future connection discovery events must be redacted and in-memory until a separate persistence contract exists.

Forbidden event content:

- credentials
- tokens
- headers
- raw scan payloads
- raw provider payloads
- unsafe command payloads
- raw network responses
- raw Bluetooth/BLE advertisements
- raw USB/serial descriptors
- MQTT payloads
- Matter fabric data
- mDNS responses
- robot/device command payloads
- physical-world telemetry unless a separate privacy contract approves it

## Pseudo-Flow

Pseudo-code only:

```python
# PSEUDO-CODE ONLY. Not implemented.
request = KernelRequest(
    request_id="req-discovery-001",
    shell_id="arc-office",
    actor_id="operator-ref",
    normalized_intent={
        "action_category": "connection_discovery",
        "discovery_domain": "wifi",
        "requested_scope": "office_network_metadata_only",
    },
    capability_profile=CapabilityProfile(connection_discovery=True),
)

result = kernel.evaluate(request)
# Future classification-only behavior may return proposed or approval_required.
# It must not scan, connect, pair, call APIs, use credentials, or touch devices.
```

This pseudo-code is not executable against the current runtime because this branch does not add `connection_discovery` runtime behavior.

## First Later Implementation Candidate

Recommended later implementation branch:

`implement-lima-connection-intent-classification`

Allowed scope for that later branch:

- classify already-normalized connection/discovery intent metadata
- return `proposed`, `approval_required`, or `blocked`
- keep all results dry-run and non-executing
- add tests for discovery, connection, control, and actuation distinctions

Forbidden in that later branch:

- scanning
- discovery
- connection attempts
- pairing
- sockets
- OS network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS implementation
- IoT adapters
- Robo-OS adapters
- Sparkbot or Arc Bot wiring
- background workers
- subprocesses
- threads
- scheduler
- external calls
- credential storage
- device, robot, drone, or physical-world behavior
