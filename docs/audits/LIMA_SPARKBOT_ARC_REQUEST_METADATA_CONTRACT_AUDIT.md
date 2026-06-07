# LIMA Sparkbot and Arc Request Metadata Contract Audit

## Branch

`audit-lima-sparkbot-arc-request-metadata-contract`

## Base Commit

`15b8e0c73aab3c898df4e1dc02bea62e1e26b5f5`

## Audit Scope

This independent audit reviews the design-only Sparkbot/Arc normalized request metadata contract before any fixture implementation begins.

This audit branch does not implement behavior. It does not modify `lima/`, tests, examples, package metadata, public Sparkbot files, Arc Bot files, provider/model files, storage/persistence files, live adapter files, connector behavior, network access, browser control, file mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Audit Verdict

PASS.

The metadata contract is narrow, dependency-facing, and safe for a later fixture-only implementation branch:

`implement-lima-sparkbot-arc-request-fixtures`

It is not ready for public Sparkbot integration, Arc Bot integration, live HumanInput, IntentEnvelope runtime creation, Guardian enforcement, approval enforcement, provider/model calls, tool execution, persistence, connector access, live discovery, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## 1. Scope and File Safety

The design branch added only:

- `docs/design/LIMA_SPARKBOT_ARC_REQUEST_METADATA_CONTRACT.md`
- `docs/audits/LIMA_SPARKBOT_ARC_REQUEST_METADATA_CONTRACT_READINESS_REVIEW.md`

Confirmed untouched by the design branch:

- `lima/`
- `tests/`
- `examples/`
- `pyproject.toml`
- public Sparkbot repository
- Arc Bot repository surfaces
- provider/model implementation
- storage/persistence implementation
- live adapter implementation
- shell wiring
- connector behavior
- browser/network/file mutation surfaces
- scheduler/background worker surfaces
- Robo-OS/device/robot/drone/physical-world surfaces

Audit finding:

- PASS. The branch stayed docs-only and did not alter runtime behavior.

## 2. Normalized Metadata Boundary

The design requires Sparkbot and Arc to normalize request metadata before calling LIMA. It explicitly rejects:

- raw chat text as executable intent
- raw prompt text
- raw provider request/response payloads
- raw tool arguments
- raw connector records
- secrets, tokens, headers, cookies, credentials, or pairing codes
- unsafe command payloads
- live network/device scan dumps
- device serial numbers or physical location details
- robot/drone command payloads

Audit finding:

- PASS. The contract preserves "normalized metadata in, dry-run result out."

## 3. Mapping to Current Kernel Contract

The design maps future consumer metadata into existing `KernelRequest` fields:

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

The design does not require `lima/` runtime changes for the next fixture lane.

Audit finding:

- PASS. The proposed mapping is compatible with the current minimal kernel surface.

## 4. Required Metadata Review

The design identifies required future fields:

- `schema_version`
- `request_id`
- `shell.shell_id`
- `shell.shell_type`
- `actor.actor_id`
- `actor.actor_type`
- `session.session_id`
- `normalized_intent.action_category`
- `normalized_intent.risk_class`
- `normalized_intent.execution_mode`
- `capability_profile.profile_id`
- `source_surface.surface`
- `source_surface.privacy_class`

Missing required fields are specified to block in a later implementation.

Audit finding:

- PASS. The future contract is specific enough for fixture validation.

## 5. Capability Profile Review

The design requires default-deny capability profiles and keeps the following false by default:

- `model_calls`
- `memory_write`
- `task_state_write`
- `connector_read`
- `connector_write`
- `external_send`
- `file_write`
- `process_execute`
- `browser_control`
- `device_control`
- `robotics_actuation`
- `drone_actuation`
- `scheduler_run`
- `connection_attempt`
- `device_pairing`
- `credential_use`
- `iot_control`
- `physical_world_actuation`

Discovery capabilities may be enabled only for dry-run metadata classification or explicit simulated adapter paths. Live discovery remains out of scope.

Audit finding:

- PASS. Capability posture remains fail-closed.

## 6. Output and Non-Execution Invariant Review

The design requires future Sparkbot/Arc contract tests to assert dry-run invariants:

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

- PASS. The design preserves current non-execution semantics.

## 7. Sparkbot Boundary Review

The design does not authorize touching the public Sparkbot repository.

It explicitly blocks Sparkbot use of LIMA for:

- raw chat execution
- production route wiring
- model calls
- tool execution
- connector access
- message sending
- file/browser/network actions
- persistence
- approval enforcement

Audit finding:

- PASS. Public Sparkbot remains out of scope.

## 8. Arc Bot Boundary Review

The design does not authorize touching Arc Bot repositories.

It explicitly blocks Arc use of LIMA for:

- live employee/customer workflow execution
- autonomous office actions
- external sends
- file mutation
- production connector reads/writes
- scheduled jobs
- workstation/device control
- Robo-OS access

Audit finding:

- PASS. Arc Bot remains a future consumer boundary only.

## 9. Guardian Boundary Review

The design keeps current Guardian output as non-authoritative stub metadata. It does not approve:

- real GuardianDecision creation
- approval enforcement
- execution authority
- bypass paths
- live policy enforcement

Audit finding:

- PASS. Guardian remains the future syscall gate and is not weakened.

## 10. Fixture Implementation Readiness

The next implementation-shaped branch may be:

`implement-lima-sparkbot-arc-request-fixtures`

That branch should be limited to:

- synthetic Sparkbot-shaped normalized request fixtures
- synthetic Arc-shaped normalized request fixtures
- focused tests mapping those fixtures into existing `KernelRequest`
- dry-run result invariant checks
- an implementation audit report

Audit finding:

- PASS. This is a narrow, non-executing next lane.

## 11. Allowed Later Files

Allowed later files:

- `tests/fixtures/sparkbot_arc_request_metadata/`
- `tests/test_lima_sparkbot_arc_request_fixtures.py`
- `docs/audits/LIMA_SPARKBOT_ARC_REQUEST_FIXTURES_IMPLEMENTATION_AUDIT.md`
- optional docs notes under `docs/design/` only if they clarify fixture scope

Any `lima/` runtime change requires separate approval.

## 12. Forbidden Later Surfaces

The fixture branch must not add:

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
- device control
- robot/drone control
- physical-world behavior
- credentials or secret storage

Audit finding:

- PASS. Forbidden surfaces remain explicit.

## Handoff Notes for Sparkbot and Arc Teams

Archive-ready message:

- LIMA now has a proposed normalized request metadata contract for future Sparkbot and Arc consumers.
- The first supported consumer shape is normalized metadata in, default-deny capability profile in, dry-run `ExecutionResult` out.
- Do not send raw chat text into LIMA for execution.
- Do not expect LIMA to call models, tools, connectors, storage, networks, browsers, files, devices, robots, or drones.
- Do not wire public Sparkbot or Arc production paths yet.
- The next useful review is fixture-based comparison against Sparkbot and Arc normalized task/action shapes.

## Validation Result

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2488 tests
- `git diff --check` - passed
- `git status --short --branch` - clean except this audit report before commit

## Recommended Next Branch

`implement-lima-sparkbot-arc-request-fixtures`

That branch must remain fixture-only and non-executing.
