# LIMA Kernel Simulated Discovery Wiring

## Purpose

This document designs a future explicit bridge from `LimaKernel.evaluate(...)` to `SimulatedDiscoveryAdapter.simulate(...)`.

This branch is design-only. It does not implement kernel wiring, adapter registry behavior, auto-dispatch, live discovery, scanning, connection attempts, pairing, credential use, sockets, OS APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT/Matter/mDNS APIs, IoT adapters, Robo-OS adapters, Sparkbot wiring, Arc Bot wiring, storage, persistence, background workers, subprocesses, threads, schedulers, device control, robot/drone control, or physical-world behavior.

The future bridge must remain:

- opt-in
- explicit
- dry-run only
- simulated only
- synthetic/inert only
- non-executing
- local/in-process only
- no live registry
- no hidden adapter dispatch

The purpose is not to make LIMA discover networks or devices. The purpose is to prove that an already-classified, simulated-only discovery request can be mapped through the kernel to an inert adapter result while preserving every non-execution invariant.

## Wiring Model

Future implementation may choose one of two explicit wiring shapes.

Option A: constructor dependency injection:

```python
# PSEUDO-CODE ONLY. Not implemented in this branch.
kernel = LimaKernel(simulated_discovery_adapter=SimulatedDiscoveryAdapter())
result = kernel.evaluate(kernel_request)
```

Option B: method-level explicit dependency:

```python
# PSEUDO-CODE ONLY. Not implemented in this branch.
result = kernel.evaluate(
    kernel_request,
    simulated_discovery_adapter=SimulatedDiscoveryAdapter(),
)
```

Option B is narrower because it makes adapter use explicit at the call site. Option A is acceptable only if the constructor argument is named for simulated discovery only and does not become a generic registry, provider catalogue, plugin loader, or hidden adapter bus.

The adapter may be invoked only when all of the following are true:

- request metadata explicitly includes `discovery_mode="simulated"`
- request metadata explicitly includes `simulated_only=True`
- request metadata explicitly includes `dry_run=True`
- connection/discovery classification result is `proposed`, or a future explicitly approved simulation-only state
- requested capability is enabled
- no credentials are present
- no credential refs are present unless a separate credential-ref-only contract later permits them for simulation-only metadata
- no pairing request is present
- no connection attempt is present
- no session-opening request is present
- no physical-world endpoint is present
- no robot/drone endpoint or control intent is present
- no live discovery mode is present
- no auto-connect or try-everything wording is present

If the adapter is absent and the request only asks for classification, the kernel returns the existing classification-only `ExecutionResult`.

If the adapter is absent and the request explicitly demands simulated surfaces, the kernel must return `blocked`.

If the adapter is present but the request metadata is not strictly simulated, the kernel must return `blocked`.

If the adapter returns unsafe data, the kernel must block or redact the adapter payload and return a dry-run blocked result.

## Request/Result Mapping

The future kernel wiring may map from `KernelRequest` to `DiscoveryAdapterRequest` only after Guardian/classification checks pass.

### `KernelRequest` to `DiscoveryAdapterRequest`

Mapping rules:

- `KernelRequest.request_id` -> `DiscoveryAdapterRequest.request_id`
- `KernelRequest.actor_id` -> `DiscoveryAdapterRequest.actor_id`
- `KernelRequest.shell_id` -> `DiscoveryAdapterRequest.shell_id`
- `KernelRequest.session_id` -> `DiscoveryAdapterRequest.session_id`
- `KernelRequest.source_surface` -> redacted `DiscoveryAdapterRequest.source_surface`
- `normalized_intent.connection_type` -> `DiscoveryAdapterRequest.connection_type`
- `normalized_intent.discovery_mode` -> `DiscoveryAdapterRequest.discovery_mode`
- `normalized_intent.target_hint` -> redacted or synthetic `DiscoveryAdapterRequest.target_hint`
- `normalized_intent.dry_run` -> `DiscoveryAdapterRequest.dry_run`
- `normalized_intent.simulated_only` -> `DiscoveryAdapterRequest.simulated_only`
- no raw credentials -> `DiscoveryAdapterRequest.credential_ref=None`
- safe synthetic metadata only -> `DiscoveryAdapterRequest.metadata`

The mapper must not pass raw prompts, raw provider payloads, raw scan data, raw SSIDs marked private/sensitive, raw Bluetooth MACs, raw IP/MAC addresses, serial numbers, physical location, headers, tokens, passwords, pairing codes, or robot/drone command payloads.

### `DiscoveryAdapterResult` to `ExecutionResult`

The future kernel result must remain an `ExecutionResult`.

Adapter surfaces may be copied only into redacted result metadata, for example:

```python
# PSEUDO-CODE ONLY. Not implemented in this branch.
metadata={
    "simulated_discovery": {
        "adapter_id": adapter_result.adapter_id,
        "state": adapter_result.state,
        "surfaces": [
            {
                "surface_id": surface.surface_id,
                "connection_type": surface.connection_type,
                "synthetic": surface.synthetic,
                "inert": surface.inert,
                "simulated": surface.simulated,
                "connectable": False,
                "controllable": False,
                "physical_world": False,
            }
        ],
    }
}
```

The kernel must not convert adapter results into execution authority. Adapter `proposed` means only that synthetic surfaces were generated for preview.

All returned `ExecutionResult` values must preserve:

- `executable: false`
- `execution_allowed: false`
- `side_effects_allowed: false`
- `dispatch_allowed: false`
- `persistence_allowed: false`
- `dry_run: true`
- `simulated_only: true` if represented in metadata
- `live_discovery_executed: false`
- `connection_attempted: false`
- `pairing_attempted: false`
- `credentials_used: false`
- `session_opened: false`
- `device_control_executed: false`
- `physical_world_executed: false`
- `adapter_active: false` unless explicitly redefined later as `simulated_adapter_used` without execution authority

## Event Behavior

Future event behavior:

- kernel emits a classification event
- adapter emits or returns simulation event metadata
- kernel merges event refs into result metadata or warnings
- all merged refs are redacted
- events remain in-memory only
- no durable persistence
- no raw scan data
- no device/network secrets
- no physical endpoint details without redaction

The kernel must treat adapter event metadata as untrusted. If an adapter event contains raw credential-like data, live discovery markers, connection/session/pairing markers, physical-world markers, robot/drone command payloads, or raw scan dumps, the kernel blocks and returns a redaction failure reason.

The kernel must not send adapter events to a Spine ledger, database, file, queue, external telemetry sink, shell websocket, or network endpoint until separate event/spine persistence design and approval exist.

## Fail-Closed Rules

The future wiring must block when:

- adapter is missing but request demands simulated surfaces
- adapter is present but manifest is invalid
- adapter manifest reports live discovery support for this lane
- adapter manifest reports connection attempt support for this lane
- adapter manifest reports pairing support for this lane
- adapter manifest reports credential support for this lane
- adapter manifest reports physical-world support for this lane
- adapter result contains raw credential-like data
- adapter result contains live discovery markers
- adapter result contains connection markers
- adapter result contains session markers
- adapter result contains pairing markers
- adapter result contains physical-world markers
- adapter result contains robot/drone control markers
- adapter result contains raw scan dumps
- request asks for auto-connect
- request asks to "try everything"
- request uses a live discovery mode
- request includes credential refs or raw credentials
- request includes pairing intent
- request includes session intent
- request includes control/action intent
- request includes physical-world endpoint intent
- adapter raises an exception
- adapter returns an error state
- requested capability is disabled
- classification returns `blocked`

Adapter results cannot turn a blocked kernel classification into `proposed`. Guardian/classification remains the first gate.

## No Registry Rule

Future wiring must not introduce:

- global adapter registry
- plugin auto-loading
- dynamic import
- scanning for adapters
- background adapter discovery
- live connector lookup
- environment-based adapter activation
- shell-driven hidden adapter activation
- file-system adapter discovery
- network adapter discovery
- package entry-point loading
- remote manifest loading

The only allowed future dependency is an explicit in-process simulated adapter object supplied directly by code under test or by an approved shell-facing call path after design review.

## Future Pseudo-Flow

Allowed simulated pseudo-flow:

```text
1. Kernel receives normalized simulated Bluetooth metadata preview request.
2. Kernel classifies request as connection discovery.
3. Capability check passes for simulation-only discovery.
4. Kernel verifies dry_run=True and simulated_only=True.
5. Kernel verifies no credential, pairing, session, connection, control, robot, drone, or physical-world intent.
6. Kernel builds DiscoveryAdapterRequest.
7. Explicit SimulatedDiscoveryAdapter.simulate(...) runs.
8. Adapter returns synthetic surfaces only.
9. Kernel validates/redacts adapter result.
10. Kernel returns ExecutionResult with dry-run metadata.
11. No scan, connect, pair, credential use, control, actuation, persistence, dispatch, or external call occurs.
```

Pseudo-code only:

```python
# PSEUDO-CODE ONLY. Not implemented in this branch.
classification = kernel.evaluate(kernel_request)
if classification.state == "proposed" and request_is_strictly_simulated(kernel_request):
    adapter_request = build_discovery_adapter_request(kernel_request)
    adapter_result = explicit_simulated_adapter.simulate(adapter_request)
    result = merge_simulated_result(classification, adapter_result)
```

Blocked pseudo-flow: real Bluetooth scan:

```text
Request asks for discovery_mode="scan" or "live".
Kernel blocks before adapter invocation.
No Bluetooth API is imported or called.
```

Blocked pseudo-flow: connect to WiFi:

```text
Request includes connect/auto-connect/session intent.
Kernel blocks.
Adapter is not invoked.
No connection attempt occurs.
```

Blocked pseudo-flow: pair device:

```text
Request includes pair/pairing intent.
Kernel blocks.
Adapter is not invoked.
No pairing occurs.
```

Blocked pseudo-flow: credential present:

```text
Request includes credential_ref or raw password/token/key/header field.
Kernel blocks.
Adapter is not invoked.
No credential is used or stored.
```

Blocked pseudo-flow: robot or drone:

```text
Request asks to find/connect to robot or drone endpoint.
Kernel blocks as physical endpoint intent.
Adapter is not invoked.
No device, robot, drone, or physical-world behavior occurs.
```

Blocked pseudo-flow: auto-connect:

```text
Request asks to auto-connect to anything.
Kernel blocks.
Adapter is not invoked.
No connection or session opens.
```

## Later Implementation Branch

Next possible implementation branch:

`implement-lima-kernel-simulated-discovery-wiring`

That branch may only:

- add an explicit optional simulated adapter dependency or method argument
- map `KernelRequest` to `DiscoveryAdapterRequest`
- call `SimulatedDiscoveryAdapter.simulate(...)` only for strict simulated dry-run metadata
- return adapter synthetic surfaces inside dry-run result metadata
- preserve all non-execution invariants
- add tests for explicit simulated path
- add tests for blocked unsafe paths

That branch must not:

- add live adapter registry
- add auto-dispatch beyond explicit simulated path
- add live discovery
- scan
- connect
- pair
- use credentials
- import socket/network/Bluetooth/USB/serial/MQTT/Matter/mDNS APIs
- wire Robo-OS
- wire Sparkbot
- wire Arc Bot
- persist data
- run background work
- control devices
- touch physical-world systems

## Design Verdict

This design is ready for independent audit.

It is not approval to implement wiring yet. It is not approval for kernel auto-dispatch, adapter registries, live discovery, scanning, connection attempts, pairing, credentials, sockets, OS APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT/Matter/mDNS APIs, IoT adapters, Robo-OS access, Sparkbot wiring, Arc Bot wiring, persistence, background work, device control, robotics, drones, or physical-world behavior.
