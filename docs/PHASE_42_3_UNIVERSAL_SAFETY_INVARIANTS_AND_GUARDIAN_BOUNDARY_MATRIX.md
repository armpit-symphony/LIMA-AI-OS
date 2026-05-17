# Phase 42.3 Universal Safety Invariants And Guardian Boundary Matrix

Phase 42.3 records universal safety invariants and Guardian boundary rules for LIMA AI OS profile/contract planning.

This phase is docs/tests/fixtures-only. It does not implement Guardian behavior, approval enforcement, execution, dispatch, persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external calls, background work, adapters, MCP calls, database writes, or hidden side effects.

## Universal Safety Invariants

Every Phase 42 planning artifact must preserve:

- `preview_only=true`
- `non_authoritative=true`
- `safe_by_default=true`
- `execution_allowed=false`
- `side_effects_allowed=false`
- `approval_granted=false`
- `dispatch_allowed=false`
- `persistence_allowed=false`
- `humaninput_bridge_active=false`
- `sparkbot_wiring_active=false`
- `live_adapter_active=false`
- `external_calls_allowed=false`
- `robotics_allowed=false`
- `physical_world_allowed=false`
- `lima_grants_approval=false`

Consumer profile vocabulary cannot grant runtime authority.

## Guardian Boundary

Guardian or a future policy membrane owns real approval state.

LIMA AI OS in Phase 42 may describe:

- requested action class
- risk tier
- approval posture
- dry-run posture
- blocked/deferred reasons
- evidence references
- simulation references
- adapter boundary requirements

LIMA AI OS in Phase 42 cannot:

- approve
- execute
- dispatch
- persist
- mutate
- call external systems
- activate Sparkbot wiring
- activate HumanInput bridge behavior
- activate live adapters
- call robotics or physical-world systems
- start background workers
- create hidden side effects

## Boundary Matrix

| Action class | Phase 42 posture | Guardian / policy membrane requirement |
| --- | --- | --- |
| `read` | preview-only | future policy may allow depending on profile |
| `internal_write` | described only | explicit future approval required |
| `external_write` | blocked or approval-postured | Guardian-owned confirmation required |
| `execute` | blocked | explicit future implementation and Guardian approval required |
| `admin` | blocked or breakglass-postured | Guardian-owned PIN/breakglass required |
| `secret_use` | blocked or redacted | Guardian/Vault-owned approval required |
| `scheduled_work` | planned only | no worker/queue until future approval |
| `robot_motion` | blocked/deferred | Guardian + hardware adapter + emergency-stop contract required |
| `physical_world_action` | blocked/deferred | Guardian + embodiment policy + emergency-stop contract required |
| `iot_device_action` | blocked/deferred | Guardian + device adapter contract required |
| `human_proximity_action` | blocked/deferred | Guardian + safety policy + emergency-stop contract required |
| `emergency_stop` | descriptive posture only | future emergency-stop path must be audited and explicitly approved |

## Robotics / IoT Boundary

Robotics, drones, humanoids, IoT devices, and physical-world actuators are long-term LIMA AI OS targets. In this lane they remain profile vocabulary and blocked/deferred action classes. No MCP calls, hardware calls, adapters, drivers, movement, actuation, or physical-world behavior are introduced.
