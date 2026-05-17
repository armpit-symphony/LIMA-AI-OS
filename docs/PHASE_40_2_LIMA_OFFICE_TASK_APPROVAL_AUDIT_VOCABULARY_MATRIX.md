# Phase 40.2 LIMA Office Task Approval Audit Vocabulary Matrix

Phase 40.2 records the Arc Bot / LIMA AI Office vocabulary that LIMA AI OS should understand for future guarded task-consumer planning.

Sparkbot v1.6.80 remains reference evidence only. Arc Bot / LIMA AI Office remains the primary guarded task-oriented office consumer. This matrix does not approve direct Sparkbot integration, Arc Bot implementation, HumanInput bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, robotics, physical-world behavior, external calls, background work, or any new `lima/` runtime change.

## Classification Matrix

| Concept | Classification | Arc Bot / LIMA Office Meaning |
| --- | --- | --- |
| `task_intake` | Adopt into LIMA AI OS planning vocabulary | A caller-provided office task request described as preview metadata only. |
| `task_classification` | Adopt into LIMA AI OS planning vocabulary | A non-authoritative risk and action-class label for task preview. |
| `operator_approval_boundary` | Adapt for Arc Bot / LIMA Office with stricter defaults | A planning label that marks external write, secret, admin, schedule, connector, or physical-world requests as requiring approval posture or block posture. |
| `explain_plan_required` | Adapt for Arc Bot / LIMA Office with stricter defaults | A planning flag that says a risky request needs policy simulation or explain-plan evidence before any future action path. |
| `run_state` | Adopt into LIMA AI OS planning vocabulary | One of `planned`, `awaiting_approval`, `ready`, `blocked`, `completed`, or `failed`, without runtime authority. |
| `audit_evidence_ref` | Adopt into LIMA AI OS planning vocabulary | A reference label for future evidence, not audit persistence. |
| `connector_health` | Adopt into LIMA AI OS planning vocabulary | `configured`, `missing_secrets`, `disabled`, `demo_ready`, or `bridge_needed` as setup posture only. |
| `memory_trust` | Adopt into LIMA AI OS planning vocabulary | Source, confidence, verification, redaction, and pending-approval labels without memory storage. |
| `agent_identity` | Adopt into LIMA AI OS planning vocabulary | Owner, purpose, scopes, allowed tools, expiration, risk tier, and kill switch metadata without wiring agents. |
| `scheduled_work_posture` | Adapt for Arc Bot / LIMA Office with stricter defaults | Planned or awaiting-approval state only; no worker, queue, daemon, thread, subprocess, or hidden background job. |
| `external_write_posture` | Adapt for Arc Bot / LIMA Office with stricter defaults | External sends, calendar writes, file writes, and service writes are blocked or approval-postured by default. |
| `secret_use_posture` | Adapt for Arc Bot / LIMA Office with stricter defaults | Secret use is blocked, redacted, PIN-required, or breakglass-required planning metadata only. |
| `admin_action_posture` | Adapt for Arc Bot / LIMA Office with stricter defaults | Admin actions are blocked, PIN-required, or breakglass-required planning metadata only. |
| `physical_world_posture` | Defer until future integration planning | Robotics and physical-world requests are blocked, replay-only, simulation-only, or deferred; no hardware path. |
| Sparkbot workstation affordances | Keep as Sparkbot-only product behavior | Personal workstation shell, browser, live terminal, code execution, model-stack controls, and broad owner-local actions are not Arc defaults. |
| Runtime authority from labels | Reject from LIMA runtime safety model | Planning labels must never grant execution, approval, dispatch, persistence, adapter, Sparkbot, robotics, or physical-world authority. |

## Hard Invariants

Every Arc Bot planning artifact must preserve:

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

## Continue

Continue only to Phase 40.3 Arc Bot candidate preview fixture plan.
