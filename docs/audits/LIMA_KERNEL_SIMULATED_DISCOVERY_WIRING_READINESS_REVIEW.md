# LIMA Kernel Simulated Discovery Wiring Readiness Review

## Branch

`design-lima-kernel-simulated-discovery-wiring`

## Base commit

`36bdffc6e610034c3c60bcea6d5d5060674c2278`

## Scope

This readiness review evaluates the design-only kernel-to-simulated-adapter wiring contract before any implementation branch.

This branch does not modify `lima/`, tests, tests/support, adapter implementation files, provider/model implementation, storage/persistence files, socket/network code, Bluetooth/BLE code, USB/serial code, MQTT/Matter/mDNS code, IoT adapters, Robo-OS adapters, Sparkbot wiring, Arc Bot wiring, background workers, subprocesses, threads, schedulers, credential storage, connection attempts, pairing, device control, robot/drone control, or physical-world behavior.

## Readiness Verdict

PASS for independent audit.

The design is narrow enough to proceed to:

`audit-lima-kernel-simulated-discovery-wiring-design`

It is not ready for implementation until that independent audit passes. It is not ready for live discovery, scanning, connection attempts, pairing, credential use, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Explicit and Opt-In Adapter Use

Question: Does the design keep adapter use explicit and opt-in?

Answer: Yes.

The design allows only:

- explicit constructor injection named for simulated discovery only
- or explicit method-level simulated adapter argument

The readiness preference is method-level explicit dependency because it makes adapter use visible at the call site. Constructor injection remains acceptable only if it cannot become a registry, plugin loader, or hidden adapter bus.

## No Global Registry or Dynamic Plugin Behavior

Question: Does it avoid global registry/dynamic plugin behavior?

Answer: Yes.

The design explicitly forbids:

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

## No Auto-Dispatch or Hidden Activation

Question: Does it avoid auto-dispatch and hidden activation?

Answer: Yes.

Adapter invocation is allowed only when strict simulated metadata is present and classification has already returned a safe simulated path. If the adapter is absent, classification-only results remain valid unless the request explicitly demands simulated surfaces, in which case the kernel blocks.

No hidden adapter dispatch, scheduler, background worker, shell trigger, registry lookup, or environment-based activation is permitted.

## Dry-Run and Non-Execution Invariants

Question: Does it preserve dry-run/simulated-only/non-execution invariants?

Answer: Yes.

The design requires all mapped `ExecutionResult` values to preserve:

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

The design also states that adapter `proposed` means only synthetic preview, never execution authority.

## Event Redaction and In-Memory Behavior

Question: Does it preserve event redaction and in-memory-only behavior?

Answer: Yes.

The design requires:

- kernel classification event remains redacted
- adapter simulation event metadata remains redacted
- merged event refs remain in-memory only
- no durable persistence
- no raw scan data
- no device/network secrets
- no physical endpoint details without redaction
- no event writes to Spine, database, file, queue, shell websocket, network endpoint, or external telemetry sink

Adapter event metadata is treated as untrusted. Unsafe event content forces blocking/redaction failure.

## Blocking Live and Physical Requests

Question: Does it block live discovery, connection, pairing, credentials, robot/drone/physical-world requests?

Answer: Yes.

The design requires blocking when requests include:

- live discovery mode
- scan/probe/enumerate intent
- connect or auto-connect intent
- try-everything intent
- pairing intent
- session intent
- credential refs
- raw credentials
- control/action intent
- physical-world endpoint intent
- robot/drone endpoint or control intent

It also requires blocking when adapter results contain any equivalent unsafe markers.

## Narrowness for Later Implementation

Question: Is it narrow enough for a later implementation branch?

Answer: Yes.

The allowed implementation path is limited to explicit simulated wiring only:

- inject or pass a simulated adapter explicitly
- map `KernelRequest` to `DiscoveryAdapterRequest`
- call `SimulatedDiscoveryAdapter.simulate(...)` only for strict simulated dry-run metadata
- merge synthetic surfaces into dry-run metadata
- preserve non-execution invariants
- add tests for safe explicit simulated path and blocked unsafe paths

No live adapter tier is permitted.

## Exact Files Allowed in Later Implementation

The later implementation branch may touch only:

- `lima/kernel/kernel.py`
- `lima/kernel/plugin_contract.py` only if a typed metadata field is strictly required
- `lima/kernel/discovery.py` only if a minor typed adapter result/mapping adjustment is strictly required
- `lima/kernel/__init__.py` only if a safe public export changes
- `tests/test_lima_kernel_simulated_discovery_wiring.py`
- existing focused kernel/discovery tests only if needed to preserve invariants
- `docs/audits/LIMA_KERNEL_SIMULATED_DISCOVERY_WIRING_IMPLEMENTATION_AUDIT.md`

Any change outside those files requires separate approval before implementation starts.

## Exact Surfaces That Remain Forbidden

The later implementation branch must not add:

- live adapter registry
- global registry
- dynamic plugin loading
- auto-dispatch beyond explicit simulated path
- live discovery
- scanning
- connection attempts
- pairing
- credential use
- credential storage
- sockets
- OS network APIs
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
- file/browser/network mutation
- device control
- robot/drone control
- physical-world behavior

## Validation Result

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2460 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only the intended design and readiness review docs before staging.

## Recommended Next Branch

`audit-lima-kernel-simulated-discovery-wiring-design`

Do not proceed directly to implementation until this design is independently audited.
