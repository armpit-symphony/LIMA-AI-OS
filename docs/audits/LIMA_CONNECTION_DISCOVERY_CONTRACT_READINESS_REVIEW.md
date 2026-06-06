# LIMA Connection Discovery Contract Readiness Review

## Branch

`design-lima-connection-discovery-contract`

## Base commit

`82eaaf10c21f31b33230307ee39ffe52d9a1f202`

## Scope

This readiness review evaluates `docs/design/LIMA_CONNECTION_DISCOVERY_CONTRACT.md`.

This branch is design-only. It does not modify `lima/`, `tests/`, `tests/support/`, adapters, shell code, provider code, storage code, Robo-OS code, or runtime behavior.

## Readiness verdict

The design is ready for a later non-executing kernel classification slice. It is not approval for live discovery, scanning, connection, pairing, credential use, device control, robotics, drones, or physical-world behavior.

The design is narrow enough because it preserves the central invariant:

Discovery is not connection. Connection is not control. Control is not actuation.

## Does the design preserve the distinction between discovery, connection, and control?

Yes.

The design defines separate levels:

- discovery proposal as metadata-only
- connection attempt as a stricter future operation
- control request as a command/mutation boundary
- actuation request as a physical-world boundary

It requires each level to pass stricter Guardian classification and HumanInput approval before any later live behavior could be considered.

## Does it prevent live scanning/connection in this branch?

Yes.

The branch adds documentation only. It does not implement scanning, discovery, connection attempts, pairing, sockets, OS APIs, protocol adapters, or endpoint calls.

The design explicitly forbids live SSID scans, IP scans, BLE scans, serial/USB probing, MQTT/Matter/mDNS calls, Robo-OS endpoint calls, and connection handles.

## Does it preserve fail-closed behavior?

Yes.

The design requires:

- unknown surfaces to block
- connection attempts to be approval_required or blocked
- control requests to be approval_required or blocked
- actuation requests to block
- credential use to block until a credential contract exists
- discovery to remain proposed/dry-run/read-only until separately approved

## Does it avoid sockets, Bluetooth APIs, USB/serial APIs, IoT APIs, Robo-OS wiring, adapters, and background workers?

Yes.

The branch does not add code and the design explicitly forbids:

- sockets
- OS network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS implementation
- IoT adapters
- Robo-OS adapters
- Sparkbot wiring
- Arc Bot wiring
- background workers
- subprocesses
- threads
- schedulers
- external calls

## Does it avoid credential capture/logging?

Yes.

The design forbids credentials, passwords, tokens, headers, connection strings with secrets, and raw credential-bearing payloads in request metadata, events, proposals, and dry-run results.

Credential use remains blocked until a separate credential handling contract exists.

## Does it keep physical-world behavior blocked?

Yes.

The design keeps device control, robot behavior, drone behavior, hardware IO, and physical-world actuation blocked. It requires a separate physical-world safety lane before any such behavior could be considered.

## Is it narrow enough for a later non-executing kernel classification slice?

Yes.

The next implementation can be limited to classification of already-normalized metadata into:

- `proposed`
- `approval_required`
- `blocked`

That later branch must remain non-executing and must not scan, discover, connect, pair, call APIs, or touch devices/networks.

## Exact files allowed in the later implementation branch

For `implement-lima-connection-intent-classification`, allowed files should be limited to:

- `lima/kernel/kernel.py`
- `lima/kernel/plugin_contract.py`
- `lima/kernel/__init__.py` only if safe exports are required
- `tests/test_lima_connection_intent_classification.py`
- `docs/audits/LIMA_CONNECTION_INTENT_CLASSIFICATION_AUDIT.md`

Optional docs-only file if needed:

- `docs/design/LIMA_CONNECTION_DISCOVERY_CONTRACT.md`

No other files should be touched unless the operator explicitly approves an amended file map before work begins.

## Exact files/surfaces that remain forbidden

Forbidden source areas:

- `lima/adapters/**`
- `lima/guardian/**`
- `lima/harness/**`
- `lima/io/**`
- `lima/packs/**`
- `lima/persistence/**`
- `lima/services/**`
- `lima/shells/**`
- `lima/spine/**`
- `tests/support/**`
- Sparkbot files
- Arc Bot files
- Robo-OS files
- frontend/UI files

Forbidden runtime surfaces:

- scanning
- discovery execution
- connection attempts
- pairing
- sockets
- OS network APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS implementation
- IoT adapters
- Robo-OS adapters
- provider/model calls
- storage/persistence
- credential storage
- Guardian enforcement
- approval enforcement
- HumanInput live bridge
- Sparkbot wiring
- Arc Bot wiring
- tool execution
- driver execution
- shell/browser/network/file mutation
- background workers
- queues
- daemons
- subprocesses
- threads
- scheduler
- external calls
- device control
- robotics actuation
- drone actuation
- physical-world behavior

Forbidden event/result content:

- credentials
- passwords
- tokens
- headers
- raw scan payloads
- raw adapter payloads
- raw network responses
- raw Bluetooth/BLE advertisements
- raw USB/serial descriptors
- MQTT payloads
- Matter fabric data
- mDNS responses
- unsafe commands
- robot/device command payloads
- physical-world telemetry

## Validation result

Validation performed on this branch:

- `python -m compileall lima` passed.
- `python -m pytest -q tests -p no:cacheprovider` passed: 2407 tests.
- `git diff --check` passed.
- `git status --short --branch` showed only the two intended docs files before staging.

## Recommended next branch

`implement-lima-connection-intent-classification`

That branch must remain non-executing. It should only teach the kernel to classify connection/discovery intent metadata into `proposed`, `approval_required`, or `blocked` results. It must not scan, discover, connect, pair, call APIs, or touch devices/networks.
