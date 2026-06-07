# LIMA Sparkbot and Arc Request Fixtures Audit

## Branch

`audit-lima-sparkbot-arc-request-fixtures`

## Base Commit

`eed3c312c50427b8deefc666ba3e11e4825d1351`

## Audit Scope

This independent audit reviews the Sparkbot/Arc synthetic request fixture implementation before any shell-owned translator design begins.

This audit branch does not implement behavior. It does not modify `lima/`, tests, fixtures, examples, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Audit Verdict

PASS.

The fixture implementation is narrow, synthetic, redacted, and non-executing. It is ready for the next design lane after validation passes:

`design-lima-shell-owned-request-translator-contract`

It is not ready for public Sparkbot integration, Arc Bot integration, live HumanInput, runtime IntentEnvelope creation, Guardian enforcement, approval enforcement, provider/model calls, tool execution, persistence, live connector access, live discovery, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## 1. Scope and File Safety

The implementation branch added only:

- `tests/fixtures/sparkbot_arc_request_metadata/README.md`
- `tests/fixtures/sparkbot_arc_request_metadata/sparkbot_normalized_request_fixtures.json`
- `tests/fixtures/sparkbot_arc_request_metadata/arc_normalized_request_fixtures.json`
- `tests/test_lima_sparkbot_arc_request_fixtures.py`
- `docs/audits/LIMA_SPARKBOT_ARC_REQUEST_FIXTURES_IMPLEMENTATION_AUDIT.md`

Confirmed untouched:

- `lima/`
- `pyproject.toml`
- `examples/`
- public Sparkbot repository
- Arc Bot repository surfaces
- provider/model implementation
- storage/persistence implementation
- live adapters
- shell wiring
- connector implementation
- browser/network/file mutation surfaces
- scheduler/background worker surfaces
- Robo-OS/device/robot/drone/physical-world surfaces

Audit finding:

- PASS. The implementation stayed within the approved fixture-only file map.

## 2. Fixture Content Review

The fixtures are synthetic and redacted.

Sparkbot-shaped fixture cases:

- planning preview returns `proposed`
- simulated BLE discovery preview returns `proposed`
- external-send request returns `blocked`

Arc-shaped fixture cases:

- office task preview returns `proposed`
- scheduler request returns `blocked`
- device-control request returns `blocked`

Audit finding:

- PASS. The fixtures represent normalized metadata, not live shell input or integration payloads.

## 3. Metadata Contract Review

The tests verify required contract metadata:

- `schema_version`
- `request_id`
- `shell`
- `actor`
- `session`
- `normalized_intent`
- `capability_profile`
- `source_surface`
- `context_refs`

The tests also verify:

- `execution_mode == "dry_run"`
- source surfaces do not claim raw prompts, secrets, or unsafe payloads
- fixture documents are synthetic normalized metadata only

Audit finding:

- PASS. Fixture data exercises the contract without adding runtime schema enforcement.

## 4. Mapping Review

The tests map fixtures into the existing `KernelRequest` contract:

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

This mapping exists only inside tests and does not add shell-owned translator code to `lima/`.

Audit finding:

- PASS. Mapping proves compatibility without implementing production translation behavior.

## 5. Kernel Evaluation Review

The tests evaluate fixtures with the current non-executing `LimaKernel`.

Observed expected behavior:

- planning requests are proposed
- simulated discovery requires explicit `SimulatedDiscoveryAdapter`
- disabled external send blocks
- disabled scheduler blocks
- enabled device-control metadata still blocks at the physical/device boundary

Audit finding:

- PASS. Results are dry-run classifications, not executed actions.

## 6. Non-Execution Invariants

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

Audit finding:

- PASS. Runtime invariants remain safe.

## 7. Sensitive Payload Review

The tests scan fixture values for raw sensitive markers including:

- API keys
- authorization material
- bearer tokens
- cookies
- passwords
- pairing codes
- raw chat
- raw prompts
- raw provider data
- secrets
- tokens

Audit finding:

- PASS. Fixtures remain synthetic/redacted.

## 8. Forbidden Surface Review

The fixture implementation does not add:

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

Audit finding:

- PASS. Forbidden surfaces remain absent.

## 9. Readiness Decision

Ready for:

- `design-lima-shell-owned-request-translator-contract`

Not ready for:

- public Sparkbot repo work
- Arc Bot repo work
- production shell wiring
- runtime request translator implementation
- live HumanInput
- IntentEnvelope runtime creation
- Guardian enforcement
- approval enforcement
- model/provider calls
- tool execution
- persistence
- connector access
- live discovery
- Robo-OS access
- device, robot, drone, or physical-world behavior

## Handoff Notes for Sparkbot and Arc Teams

Archive-ready message:

- LIMA now has synthetic Sparkbot-shaped and Arc-shaped normalized metadata fixtures.
- The fixtures prove current `KernelRequest` compatibility for normalized metadata and dry-run results.
- The fixtures are not integration approval.
- Do not send raw chat text, prompts, credentials, connector payloads, or live command bodies into LIMA.
- Do not wire public Sparkbot or Arc production paths yet.
- The next cross-team design work is a shell-owned request translator contract.

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests/test_lima_sparkbot_arc_request_fixtures.py -p no:cacheprovider` - passed, 5 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2493 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except this audit report before commit

## Recommended Next Branch

`design-lima-shell-owned-request-translator-contract`
