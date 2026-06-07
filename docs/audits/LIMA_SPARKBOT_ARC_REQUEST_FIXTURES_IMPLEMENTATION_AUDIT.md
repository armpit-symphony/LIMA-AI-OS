# LIMA Sparkbot and Arc Request Fixtures Implementation Audit

## Branch

`implement-lima-sparkbot-arc-request-fixtures`

## Base Commit

`51ad0634f515eb31394483edd2e5ab81724c06f6`

## Files Changed

- `tests/fixtures/sparkbot_arc_request_metadata/README.md`
- `tests/fixtures/sparkbot_arc_request_metadata/sparkbot_normalized_request_fixtures.json`
- `tests/fixtures/sparkbot_arc_request_metadata/arc_normalized_request_fixtures.json`
- `tests/test_lima_sparkbot_arc_request_fixtures.py`
- `docs/audits/LIMA_SPARKBOT_ARC_REQUEST_FIXTURES_IMPLEMENTATION_AUDIT.md`

No `lima/` runtime files, package metadata, example shell behavior, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector files, network/browser/file mutation surfaces, scheduler/background workers, Robo-OS files, device control files, robotics, drones, or physical-world files were modified.

## Fixture Summary

Added synthetic, redacted fixture documents:

- Sparkbot-shaped normalized metadata fixtures
- Arc-shaped normalized metadata fixtures

Fixture cases cover:

- Sparkbot planning preview proposed
- Sparkbot simulated BLE discovery preview proposed
- Sparkbot external-send request blocked by disabled capability
- Arc office task preview proposed
- Arc scheduler request blocked by disabled capability
- Arc device-control request blocked by physical/device boundary

All fixtures are synthetic and redacted. They contain no raw chat text, raw prompts, provider payloads, tool payloads, connector records, credentials, live scan dumps, device serials, physical location, robot command payloads, or drone command payloads.

## Mapping Behavior

The tests map each fixture into the current `KernelRequest` contract:

- `request_id`
- `shell_id`
- `actor_id`
- `session_id`
- `normalized_intent`
- `capability_profile`
- `actor_context`
- `shell_context`
- `session_context`
- `memory_refs`
- `source_surface`
- `metadata`

This mapping exists only in tests. It does not add runtime translation behavior to `lima/`.

## Kernel Evaluation Behavior

The fixtures are evaluated through the current non-executing `LimaKernel`:

- safe planning requests return `proposed`
- simulated discovery uses explicit `SimulatedDiscoveryAdapter`
- disabled consequential capabilities return `blocked`
- device-control metadata remains blocked

No public Sparkbot or Arc integration was added.

## Non-Execution Guarantees

Tests assert all evaluated results preserve:

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
- `lima/` runtime behavior
- provider/model calls
- storage/persistence
- real Guardian enforcement
- real approval enforcement
- live HumanInput bridge
- IntentEnvelope runtime creation
- live adapters
- tool execution
- connector access
- browser control
- file mutation
- network calls
- socket APIs
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- scheduler/background workers
- subprocesses/threads
- device control execution
- robot/drone control
- physical-world behavior
- credentials or secret storage

## Tests Added

Added `tests/test_lima_sparkbot_arc_request_fixtures.py` covering:

- fixture documents are synthetic normalized metadata only
- required contract metadata is present
- no raw sensitive payload markers are present
- fixtures map into `KernelRequest`
- fixtures evaluate through `LimaKernel` as dry-run results
- explicit simulated discovery returns synthetic surfaces only
- all non-execution invariants remain safe

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests/test_lima_sparkbot_arc_request_fixtures.py -p no:cacheprovider` - passed, 5 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2493 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except intended fixture implementation files before commit

## Remaining Blockers Before Sparkbot/Arc Use

LIMA is closer to future Sparkbot/Arc dependency readiness, but still not ready for production integration.

Remaining blockers:

- independent audit of these fixtures
- clean external consumer install verification
- real shell-owned translator design
- live HumanInput bridge design
- IntentEnvelope runtime creation design
- real Guardian request/decision lifecycle design
- approval enforcement design
- provider/model boundary design
- event/spine persistence design
- Sparkbot-owned integration branch later
- Arc-owned integration branch later

## Recommended Next Branch

`audit-lima-sparkbot-arc-request-fixtures`

After that audit passes, the next design lane should be:

`design-lima-shell-owned-request-translator-contract`
