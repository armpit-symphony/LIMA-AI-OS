# Phase 38.2 LIMA Consumer Boundary Vocabulary Review

Phase 38.2 defines Sparkbot-shaped vocabulary that LIMA can use in planning, preview fixtures, and future contract discussions.

This is not runtime implementation. These names do not approve, execute, dispatch, persist, bridge HumanInput, wire Sparkbot, activate adapters, call external services, mutate files, connect to MCP, or control robotics/physical-world systems.

## Consumer Boundary Vocabulary

| Field | Allowed planning values | LIMA meaning in Phase 38 |
| --- | --- | --- |
| `consumer_kind` | `sparkbot`, `arc_office`, `guardian_suite`, `robotics_os` | Future shell/consumer identity only. |
| `operator_posture` | `owner_local`, `strict_security`, `breakglass_active`, `simulation_only` | Preview posture only; does not change runtime permissions. |
| `action_class` | `read`, `internal_write`, `external_write`, `execute`, `admin`, `robot_motion`, `secret_use` | Requested action category for risk preview only. |
| `risk_tier` | `low`, `medium`, `high`, `critical` | Planning risk label only. |
| `approval_posture` | `not_required`, `confirmation_required`, `pin_required`, `breakglass_required`, `blocked` | Required future approval shape only; no approval is granted. |
| `dry_run_posture` | `native_dry_run`, `explain_plan_required`, `simulation_only`, `unavailable` | Preview/simulation posture only; no tool call happens. |
| `run_state` | `planned`, `awaiting_approval`, `ready`, `blocked`, `completed`, `failed` | Inspectable state label only; `ready` is not permission to execute. |
| `agent_identity` | `owner`, `purpose`, `scopes`, `allowed_tools`, `expires_at`, `risk_tier`, `kill_switch` | Agent metadata shape only; no agent routing or wiring. |
| `memory_trust` | `source`, `confidence`, `verification_state`, `redaction_state`, `pending_approval` | Memory trust shape only; no memory storage implementation. |
| `connector_health` | `configured`, `missing_secrets`, `disabled`, `demo_ready`, `bridge_needed` | Connector readiness label only; no connector access. |
| `robotics_posture` | `no_hardware`, `replay`, `simulation`, `real_hardware_blocked`, `emergency_stop_available` | Robotics planning label only; no hardware call. |
| `audit_surface` | `policy_decision`, `run_timeline`, `audit_hash`, `redacted_args`, `evidence_ref` | Audit evidence vocabulary only; no audit persistence. |

## Vocabulary Invariants

Every vocabulary record remains safe by default:

- `execution_allowed=false`
- `side_effects_allowed=false`
- `approval_granted=false`
- `dispatch_allowed=false`
- `persistence_allowed=false`
- `humaninput_bridge_active=false`
- `sparkbot_wiring_active=false`
- `live_adapter_active=false`
- `external_calls_active=false`
- `robotics_physical_world_active=false`

## Owner-Local Versus Strict Security

Sparkbot owner-local mode is a product posture that can allow routine reads in Sparkbot.

LIMA Phase 38 treats `owner_local` as a planning label only. It does not allow LIMA to read a host, run commands, inspect a browser, access SSH, read files, call networks, execute tools, or perform local/server actions.

`strict_security` means a future consumer wants stricter guardrail semantics, but Phase 38 still does not enforce approvals or execute anything.

## Explain-Plan And Dry-Run Representation

Policy simulation and explain-plan concepts become preview metadata:

- `dry_run_posture=explain_plan_required` means future work should explain a plan before any action is considered.
- `dry_run_posture=simulation_only` means robotics or MCP-shaped actions must remain replay/simulation-only unless a future phase explicitly approves more.
- `approval_posture=blocked` is the safe default for critical or real-hardware shaped requests.

## Continue

Continue only to Phase 38.3 Sparkbot-to-LIMA gap and risk matrix.
