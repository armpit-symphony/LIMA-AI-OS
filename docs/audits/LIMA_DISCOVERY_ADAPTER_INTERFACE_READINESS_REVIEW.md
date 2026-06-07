# LIMA Discovery Adapter Interface Readiness Review

## Branch

`design-lima-discovery-adapter-interface`

## Base commit

`3a6b8a34bb29cd565ba716766748f432d14d592b`

## Scope

This readiness review evaluates `docs/design/LIMA_DISCOVERY_ADAPTER_INTERFACE.md`.

This branch is design-only. It does not modify `lima/`, `tests/`, `tests/support/`, adapter implementation files, provider/model implementation, storage/persistence, network code, Bluetooth/BLE code, USB/serial code, MQTT/Matter/mDNS code, IoT adapters, Robo-OS adapters, Sparkbot wiring, Arc Bot wiring, background workers, subprocesses, threads, schedulers, credential storage, connection attempts, pairing, device control, robot/drone control, or physical-world behavior.

## Readiness Verdict

PASS for design readiness.

The design is ready for independent audit in `audit-lima-discovery-adapter-interface`. It is not approval to implement simulated discovery yet.

## Does this design preserve discovery vs connection vs control vs actuation boundaries?

Yes.

The design preserves the invariant:

- discovery is not connection
- connection is not control
- control is not actuation

It defines adapter tiers so simulated discovery remains separate from live/local/authenticated/physical endpoint discovery, and it keeps connection, control, and actuation out of the simulated adapter lane.

## Does it avoid implementing adapters?

Yes.

The document defines protocol-style shapes only. No adapter classes, modules, tests/support helpers, provider code, or runtime adapter behavior are added.

## Does it avoid scanning/connection/pairing/credentials?

Yes.

The design explicitly forbids scanning, live discovery, connection attempts, pairing, credential use, and credential storage. It only allows a future deterministic simulated adapter after independent audit.

## Does it avoid sockets, OS APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT/Matter/mDNS APIs?

Yes.

The branch is documentation only and the design states that the future simulated adapter must never open sockets, call OS APIs, import Bluetooth/USB/serial/MQTT/Matter/mDNS libraries, connect, pair, or use credentials.

## Does it avoid Robo-OS/Sparkbot/Arc wiring?

Yes.

Sparkbot Workstation, Arc Bot shell, and LIMA-Robo-OS are discussed only as future integration boundaries. No wiring is added, and Robo-OS endpoint discovery remains a blocked physical endpoint boundary.

## Does it keep live/local/authenticated/physical endpoint adapters blocked?

Yes.

Only `simulated_discovery_adapter` is marked eligible for a later implementation branch.

Blocked tiers:

- `metadata_only_adapter` as implementation target in the next branch
- `read_only_local_discovery_adapter`
- `authenticated_discovery_adapter`
- `physical_endpoint_discovery_adapter`

## Is only a simulated adapter eligible for the next implementation?

Yes.

The design states that `implement-lima-simulated-discovery-adapter-only` may only implement a deterministic in-process simulated adapter using synthetic/inert request metadata and synthetic/inert surfaces.

## Is the simulated adapter lane narrow enough?

Yes.

The future lane is constrained to:

- synthetic/inert request metadata
- deterministic in-process simulated results
- synthetic/inert discovery surfaces
- redacted in-memory events only
- dry-run non-execution invariants

It forbids:

- scanning
- sockets
- OS APIs
- Bluetooth/USB/serial/MQTT/Matter/mDNS imports
- connection
- pairing
- credential use
- device control
- physical-world behavior

## Exact files allowed in the next implementation branch

For `implement-lima-simulated-discovery-adapter-only`, allowed files should be limited to:

- `lima/kernel/discovery_adapter.py`
- `lima/kernel/plugin_contract.py` only if small contract dataclasses are required
- `lima/kernel/kernel.py` only if the adapter is invoked behind existing dry-run classification
- `lima/kernel/__init__.py` only if safe exports are required
- `tests/test_lima_simulated_discovery_adapter.py`
- `docs/audits/LIMA_SIMULATED_DISCOVERY_ADAPTER_IMPLEMENTATION_AUDIT.md`

Optional docs-only file if needed:

- `docs/design/LIMA_DISCOVERY_ADAPTER_INTERFACE.md`

No other files should be touched unless the operator explicitly approves an amended file map.

## Exact surfaces that remain forbidden

Forbidden source areas:

- `tests/support/**`
- `lima/adapters/**`
- `lima/harness/**`
- `lima/io/**`
- `lima/packs/**`
- `lima/persistence/**`
- `lima/services/**`
- `lima/shells/**`
- `lima/spine/**`
- provider/model implementation files
- storage/persistence files
- Sparkbot files
- Arc Bot files
- Robo-OS files
- frontend/UI files

Forbidden behavior:

- simulated discovery implementation before independent audit
- live discovery
- scanning
- connection attempts
- pairing
- credential use
- credential storage
- sockets/network code
- OS network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- IoT adapters
- Robo-OS adapters
- Sparkbot wiring
- Arc Bot wiring
- background workers
- subprocesses
- threads
- schedulers
- storage/persistence
- provider/model calls
- device control
- robot/drone control
- physical-world behavior

## Validation Result

Validation performed on this branch:

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2433 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only the two intended docs files before staging.

## Recommended Next Branch

`audit-lima-discovery-adapter-interface`

Do not proceed directly to simulated adapter implementation until the adapter interface design is independently audited.
