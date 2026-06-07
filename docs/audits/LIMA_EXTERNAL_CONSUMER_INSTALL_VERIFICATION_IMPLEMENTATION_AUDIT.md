# LIMA External Consumer Install Verification Implementation Audit

## Branch

`implement-lima-external-consumer-import-proof`

## Base Commit

`736222038cc7b7b771c3be3400b2c616a052900e`

## Files Changed

- `tests/fixtures/external_consumer_install/README.md`
- `tests/fixtures/external_consumer_install/consumer_metadata.json`
- `tests/fixtures/external_consumer_install/synthetic_consumer.py`
- `tests/test_lima_external_consumer_install_verification.py`
- `docs/audits/LIMA_EXTERNAL_CONSUMER_INSTALL_VERIFICATION_IMPLEMENTATION_AUDIT.md`

No `lima/` runtime files, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector files, browser/network/file mutation surfaces, scheduler/background workers, Robo-OS files, device control files, robotics, drones, or physical-world files were modified.

## Verification Mode

Implemented Mode A only:

- subprocess-free import verification
- no `pip install`
- no package build
- no virtual environment creation
- no dependency downloads
- no registry access
- no package publishing

## Fixture Summary

Added a synthetic external consumer fixture:

- `consumer_metadata.json`
- `synthetic_consumer.py`

The synthetic consumer imports only LIMA public APIs and performs dry-run evaluations:

- planning preview through `LimaKernel`
- explicit simulated discovery through `SimulatedDiscoveryAdapter`

## Public Import Proof

Tests verify:

- package metadata remains `lima-runtime`
- package version remains `0.0.1`
- package discovery remains `include = ["lima*"]`
- `import lima` works
- `from lima.kernel import LimaKernel` works
- synthetic external consumer imports only `lima`

## Non-Execution Guarantees

Tests assert evaluated results preserve:

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

## Forbidden Surfaces Checked

The implementation does not add:

- public Sparkbot repo changes
- Arc Bot repo changes
- production shell wiring
- raw HumanInput bridge
- raw chat parsing in LIMA
- `lima/` runtime behavior
- package publishing
- dependency downloads
- package build automation
- editable install automation
- provider/model calls
- storage/persistence
- real Guardian enforcement
- real approval enforcement
- live adapters
- tool execution
- connector access
- browser control
- file mutation outside test fixtures
- network calls
- socket APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- scheduler/background workers
- subprocesses/threads
- device control
- robot/drone control
- physical-world behavior
- credentials or secret storage

## Tests Added

Added `tests/test_lima_external_consumer_install_verification.py` covering:

- package metadata and public imports
- Mode A local-only metadata
- synthetic consumer import allowlist
- forbidden source marker scan
- dry-run planning preview
- explicit simulated discovery with synthetic surfaces
- normalized metadata construction
- non-execution invariants

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests/test_lima_external_consumer_install_verification.py -p no:cacheprovider` - passed, 7 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2506 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except intended external consumer import-proof files before commit

## Remaining Blockers Before Sparkbot/Arc Use

LIMA now has a stronger dependency-shape proof, but is still not ready for public Sparkbot or Arc production integration.

Remaining blockers:

- independent audit of this external consumer import proof
- clean install verification mode design if editable/wheel proof is needed
- Sparkbot-owned integration design
- Arc-owned integration design
- live HumanInput bridge design
- IntentEnvelope runtime creation design
- real Guardian request/decision lifecycle design
- approval enforcement design
- provider/model boundary design
- event/spine persistence design

## Recommended Next Branch

`audit-lima-external-consumer-import-proof`

After that audit passes, the next design lane should be:

`design-lima-sparkbot-owned-integration-boundary`
