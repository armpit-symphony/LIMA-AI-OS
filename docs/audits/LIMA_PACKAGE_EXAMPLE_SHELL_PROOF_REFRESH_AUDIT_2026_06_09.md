# LIMA Package Example Shell Proof Refresh Audit - 2026-06-09

## Branch

`audit-lima-package-example-shell-proof-refresh-2026-06-09`

## Base Commit

`729179b06c3e579b7ab1f44782b3a939434b1b3d`

## Audit Verdict

PASS.

PASS for current package/example-shell proof refresh.

The local minimal example shell still proves a dependency-shaped, dry-run-only LIMA consumer path from the current repo
tip. This refresh does not modify the example shell, runtime code, package metadata, public exports, tests, Sparkbot,
Arc Bot, Robo-OS, provider/model code, storage, persistence, adapters, or any live integration surface.

## Files Changed

This branch adds only:

- `docs/audits/LIMA_PACKAGE_EXAMPLE_SHELL_PROOF_REFRESH_AUDIT_2026_06_09.md`

## Current Proof Surface Verified

The refresh verified these existing files:

- `examples/minimal_shell/example_shell.py`
- `examples/minimal_shell/README.md`
- `tests/test_lima_package_example_shell_contract.py`
- `tests/test_lima_external_consumer_install_verification.py`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `README.md`
- `docs/CURRENT_PROJECT_STATE.md`

The current example shell remains local, inert, deterministic, and shell-shaped.

## Package And Import Status

PASS.

Verified by focused tests and source review:

- `import lima` works.
- `from lima.kernel import LimaKernel` works.
- package metadata remains `lima-runtime`.
- package version remains `0.0.1`.
- package discovery remains `include = ["lima*"]`.
- top-level runtime exports from `lima` remain unapproved.
- proof-public runtime imports remain under `lima.kernel`.

No package metadata, top-level exports, public manifest exports, or packaging behavior changed in this branch.

## Example Shell Behavior

PASS.

`python -m examples.minimal_shell.example_shell` passed and emitted two redacted dry-run summaries:

- planning preview:
  - `request_id`: `example-planning-001`
  - `state`: `proposed`
  - `reason_code`: `text_preview_or_planning_proposed`
  - `dry_run`: `True`
  - `redacted_audit_summary`: `proposed:planning:text_preview_or_planning_proposed`
- simulated BLE discovery preview:
  - `request_id`: `example-simulated-discovery-001`
  - `state`: `proposed`
  - `reason_code`: `simulated_connection_discovery_proposed:ble_discovery`
  - `dry_run`: `True`
  - `redacted_audit_summary`: `proposed:ble_discovery:simulated_connection_discovery_proposed:ble_discovery`
  - synthetic surface: `simulated-ble-preview`

The example shell constructs already-normalized `KernelRequest` metadata. It does not parse raw natural language,
ingest live HumanInput, create real `IntentEnvelope` records, create real `GuardianDecision` authority, enforce
approval, call models, execute tools, persist data, access connectors, scan, connect, pair, use credentials, invoke
Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

## Simulated Discovery Refresh

PASS.

The simulated discovery path remains explicit:

`LimaKernel().evaluate(request, simulated_discovery_adapter=SimulatedDiscoveryAdapter())`

The returned surface remains synthetic and inert:

- `surface_id`: `simulated-ble-preview`
- `connection_type`: `ble`
- `synthetic`: `True`
- `inert`: `True`
- `simulated`: `True`
- `connectable`: `False`
- `controllable`: `False`
- `physical_world`: `False`

No auto-dispatch, registry behavior, live discovery, scanning, socket usage, OS network API usage, Bluetooth/BLE API
usage, USB/serial API usage, MQTT/Matter/mDNS usage, pairing, credential use, session opening, device control,
robotics, drones, or physical-world behavior exists in this proof.

## Non-Execution Invariants

PASS.

The example shell and focused tests preserve these result invariants:

- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `dry_run is True`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `live_discovery_executed is False`
- `connection_attempted is False`
- `pairing_attempted is False`
- `credentials_used is False`
- `session_opened is False`
- `device_control_executed is False`
- `physical_world_allowed is False`
- `physical_world_executed is False`
- `guardian_decision_created is False`
- `approval_enforced is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `robo_os_wiring_active is False`
- `adapter_active is False`
- `tool_execution_allowed is False`
- `driver_execution_allowed is False`
- `scheduler_active is False`
- `external_calls_allowed is False`

## Forbidden Surface Review

PASS.

This branch does not add or modify:

- `lima/` runtime files
- tests or test fixtures
- examples
- package metadata
- public exports
- public Sparkbot repository files
- Arc Bot repository files
- consumer proof branches
- provider/model implementation
- storage/persistence implementation
- Guardian enforcement
- HumanInput bridge behavior
- Sparkbot wiring
- Arc Bot wiring
- Robo-OS wiring
- adapter expansion
- tool execution
- browser/file/process/network actions
- live discovery
- scanning
- connection attempts
- pairing
- credential use
- sockets
- background workers
- schedulers
- device control
- robotics
- drones
- physical-world behavior

## Consumer Readiness Decision

PASS for local dependency-shape proof.

The current repo has a working local example shell proving that a caller can import LIMA, construct normalized metadata,
call `LimaKernel.evaluate(...)`, and receive dry-run non-executing results.

This is not enough to claim Sparkbot or Arc Bot readiness. Sparkbot and Arc Bot still need consumer-owned proof packets
from their repo teams, and those packets must pass LIMA-side redaction review and proof-result audit before result gate
or compatibility freeze work.

## Validation Result

PASS.

Validation commands run:

- `python -m examples.minimal_shell.example_shell` - passed, emitted redacted dry-run summaries only
- `python -m pytest -q tests/test_lima_package_example_shell_contract.py -p no:cacheprovider` - passed, 9 tests
- `python -m pytest -q tests/test_lima_external_consumer_install_verification.py -p no:cacheprovider` - passed, 7 tests
- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 3078 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only this audit report before commit

## Recommended Next Branch

If the operator explicitly confirms manual delivery and no proof packets are supplied:

`record-lima-consumer-proof-delivery-confirmation-status`

If Sparkbot or Arc Bot proof packets are supplied:

`audit-consumer-owned-proof-results`

If neither input is supplied:

remain in waiting state and do not claim Sparkbot/Arc readiness.
