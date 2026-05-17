# Phase 40.3 Arc Bot Candidate Preview Fixture Plan

Phase 40.3 defines the fixture targets for a future docs/tests/fixtures-only Arc Bot-shaped `candidate_preview` hardening lane.

Sparkbot v1.6.80 remains reference evidence only. Arc Bot / LIMA AI Office remains the primary guarded task-oriented consumer. This plan does not implement Arc Bot, wire Sparkbot, change `candidate_preview`, modify `lima/`, modify `tests/support/`, create a HumanInput bridge, enable live adapters, enforce approvals, execute, dispatch, persist, mutate files, call external systems, create background work, or touch robotics or physical-world behavior.

## Fixture Targets

Phase 41 should use caller-provided synthetic task metadata only. Each case must remain preview-only, non-authoritative, non-executing, and safe by default.

| Fixture | Purpose | Expected Posture |
| --- | --- | --- |
| `draft_email_no_send` | Owner asks Arc Bot to draft an email but not send it. | Preview-only, non-authoritative, no dispatch. |
| `external_email_send_request` | Owner asks Arc Bot to send an external email. | Blocked or awaiting approval; no dispatch. |
| `calendar_write_request` | Office task requires a calendar write. | Approval posture; no connector write. |
| `file_mutation_request` | Office task requires file mutation. | Blocked; no file mutation. |
| `low_confidence_memory_fact` | Low-confidence memory fact requires pending approval. | Pending approval label only; no memory storage. |
| `connector_missing_secret` | Connector cannot proceed because secrets/setup are missing. | Blocked setup posture; no secret access. |
| `agent_identity_kill_switch` | Agent identity metadata has `kill_switch=true`. | Blocked or inert identity posture. |
| `scheduled_task_requires_approval` | Scheduled work request requires approval. | Planned or awaiting approval; no worker or queue. |
| `admin_breakglass_request` | Admin action requires block/PIN/breakglass posture. | Blocked or breakglass-required label only. |
| `robotics_physical_world_request` | Physical-world or robotics request appears. | Rejected or deferred; no hardware path. |
| `sparkbot_only_behavior_rejected` | Sparkbot-only workstation behavior appears in Arc context. | Rejected from Arc defaults. |
| `strict_security_default_posture` | Arc Bot uses strict default posture. | Preview-only strict posture. |
| `explain_plan_only_risky_request` | Risky request asks for explain-plan only. | Explain-plan preview only; no action. |

## Required Invariants

Every planned fixture must preserve:

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
- `non_authoritative=true`
- `preview_only=true`
- `safe_by_default=true`

## Phase 41 Recommendation

If Phase 40 closes cleanly, continue automatically into Phase 41 as docs/tests/fixtures-only Arc Bot-shaped `candidate_preview` hardening. Phase 41 must not modify runtime code, `lima/`, `tests/support/`, Sparkbot, Arc Bot implementation, HumanInput bridge behavior, live adapters, execution, approvals, dispatch, persistence, mutation, external calls, background work, robotics, or physical-world behavior.
