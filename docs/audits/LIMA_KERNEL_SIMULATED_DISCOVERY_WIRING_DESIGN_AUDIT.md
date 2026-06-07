# LIMA Kernel Simulated Discovery Wiring Design Audit

## Branch

`audit-lima-kernel-simulated-discovery-wiring-design`

## Base commit

`a9eeccee89849af2f1bd044afe92071d422f5126`

## Scope

This audit reviews the design-only kernel simulated discovery wiring branch before any implementation begins.

This branch does not implement behavior. It does not modify `lima/`, tests/support, adapter implementation files, provider/model implementation files, storage/persistence files, Sparkbot wiring, Arc Bot wiring, Robo-OS wiring, runtime behavior, or physical-world behavior.

## Audit Verdict

PASS.

The design keeps future kernel-to-simulated-adapter use explicit, opt-in, dry-run, simulated-only, synthetic/inert, local/in-process, redacted, and non-executing. It is ready for the next implementation branch only if that branch remains limited to explicit simulated adapter wiring and preserves all fail-closed boundaries.

It is not ready for live discovery, scanning, connection attempts, pairing, credential use, sockets/network APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT/Matter/mDNS APIs, Robo-OS/Sparkbot/Arc wiring, persistence, background work, device control, robotics, drones, or physical-world behavior.

## 1. Scope and File Safety

The design branch added only:

- `docs/design/LIMA_KERNEL_SIMULATED_DISCOVERY_WIRING.md`
- `docs/audits/LIMA_KERNEL_SIMULATED_DISCOVERY_WIRING_READINESS_REVIEW.md`

Confirmed untouched by the design branch:

- `lima/`
- `tests/support/`
- adapter implementation files
- provider/model files
- storage/persistence files
- shell wiring files
- Sparkbot, Arc Bot, and Robo-OS wiring files

Audit finding:

- PASS. The design branch avoided runtime behavior and implementation files.

## 2. Explicit Wiring Model

The design requires future wiring to remain:

- explicit opt-in
- dry-run only
- simulated only
- synthetic/inert only
- local/in-process only
- no live registry
- no global plugin auto-loading
- no hidden adapter dispatch
- no dynamic import
- no environment-based adapter activation
- no shell-driven hidden adapter activation

Allowed future shapes are limited to:

- explicit constructor dependency injection named for simulated discovery only
- method-level explicit adapter argument

Audit finding:

- PASS. The design prefers method-level explicit dependency and restricts constructor injection so it cannot become a registry, provider catalogue, plugin loader, or hidden adapter bus.

## 3. Invocation Gates

The design requires future adapter invocation only when:

- `discovery_mode="simulated"`
- `simulated_only=True`
- `dry_run=True`
- classification result is eligible for a simulation-only path
- required capability is enabled
- no credentials are present
- no credential refs are present unless a later credential-ref-only contract separately approves them
- no pairing is present
- no connection attempt is present
- no session-opening request is present
- no physical-world endpoint is present
- no robot/drone endpoint or control intent is present
- no live discovery mode is present
- no auto-connect or try-everything wording is present

Audit finding:

- PASS. Adapter invocation is gated behind kernel classification and strict simulated metadata.

## 4. Request/Result Mapping

The design preserves mapping between:

- `KernelRequest`
- `ExecutionResult`
- `DiscoveryAdapterRequest`
- `DiscoveryAdapterResult`

The design maps kernel request identity and context into adapter request metadata only after classification passes:

- request ID
- actor ID
- shell ID
- session ID
- redacted source surface
- connection type
- discovery mode
- redacted or synthetic target hint
- dry-run flag
- simulated-only flag
- no raw credentials
- safe synthetic metadata only

The design maps adapter surfaces back into redacted `ExecutionResult.metadata` only. It does not allow adapter results to become execution authority.

The design preserves:

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

- PASS. The mapping is narrow and preserves non-execution invariants.

## 5. Event/Redaction Behavior

The design confirms:

- classification event remains in-memory
- adapter simulation metadata remains in-memory/result-local
- kernel result merges/redacts event refs
- no durable persistence
- no raw scan data
- no passwords
- no raw credentials
- no tokens
- no headers
- no pairing codes
- no raw SSIDs marked private/sensitive
- no raw Bluetooth MACs
- no raw IP/MAC addresses
- no raw serial numbers
- no physical location
- no robot/drone command payloads

The design requires the kernel to treat adapter event metadata as untrusted and block/redact on unsafe content.

Audit finding:

- PASS. Event behavior remains redacted, in-memory only, and non-durable.

## 6. Fail-Closed Rules

The design requires blocking for:

- missing adapter when request demands simulated surfaces
- invalid adapter manifest
- unsafe adapter result
- raw credential-like data
- live discovery markers
- connection markers
- session markers
- pairing markers
- physical-world markers
- robot/drone control markers
- raw scan dumps
- auto-connect
- "try everything"
- live discovery mode
- credential refs or raw credentials
- pairing intent
- session intent
- control/action intent
- physical-world endpoint intent
- adapter exception
- adapter error state
- disabled capability
- blocked classification result

Audit finding:

- PASS. Adapter results cannot turn blocked classification into proposed. Guardian/classification remains the first gate.

## 7. Forbidden Surfaces

The design does not approve:

- live discovery
- scanning
- connection attempts
- pairing
- credential use
- credential storage
- sockets/network code
- Bluetooth/BLE code
- USB/serial code
- MQTT/Matter/mDNS code
- IoT adapters
- Robo-OS adapters
- Sparkbot wiring
- Arc Bot wiring
- background workers
- subprocesses
- threads
- scheduler
- storage/persistence
- provider/model calls
- device control
- robot/drone control
- physical-world behavior

Audit finding:

- PASS. Forbidden surfaces remain explicitly blocked.

## 8. Implementation Readiness

The next branch may be:

`implement-lima-kernel-simulated-discovery-wiring`

PASS is conditional on that branch being limited to:

- explicit optional simulated adapter dependency or explicit method argument
- mapping `KernelRequest` to `DiscoveryAdapterRequest`
- returning adapter synthetic surfaces inside dry-run result metadata
- preserving all non-execution invariants
- tests for explicit simulated path
- tests for blocked unsafe paths

Still forbidden in that branch:

- live adapter registry
- hidden dispatch
- live discovery
- scanning
- connection
- pairing
- credentials
- sockets/network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- Robo-OS wiring
- Sparkbot wiring
- Arc Bot wiring
- persistence
- background work
- device control
- physical-world behavior

Audit finding:

- PASS for implementation readiness, with strict file and scope constraints from the readiness review.

## Key Findings

- The design branch was docs-only.
- Runtime code remained untouched.
- The wiring model is explicit and opt-in.
- No global registry, plugin auto-loading, dynamic import, environment activation, shell hidden activation, or background dispatch is approved.
- Invocation requires strict simulated dry-run metadata and eligible classification.
- Request/result mapping preserves dry-run non-execution invariants.
- Event metadata remains redacted, in-memory only, and result-local.
- Fail-closed rules cover missing adapters, invalid manifests, unsafe results, credentials, live markers, connection/session/pairing markers, physical markers, auto-connect, try-everything, adapter errors, and disabled capabilities.

## Validation Result

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2460 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only `docs/audits/LIMA_KERNEL_SIMULATED_DISCOVERY_WIRING_DESIGN_AUDIT.md` before staging.

## Recommended Next Branch

`implement-lima-kernel-simulated-discovery-wiring`

That branch must remain non-executing and explicit-only. It must not introduce live discovery, scanning, connection attempts, pairing, credentials, sockets/network APIs, Bluetooth/BLE APIs, USB/serial APIs, MQTT/Matter/mDNS APIs, Robo-OS/Sparkbot/Arc wiring, persistence, background work, device control, robotics, drones, or physical-world behavior.
