# Phase 40.1 Arc Bot Guarded Task Consumer Boundary Review

Phase 40.1 defines the Arc Bot / LIMA AI Office consumer boundary as planning metadata only.

Sparkbot v1.6.80 remains reference evidence for current control vocabulary, not the direct future consumer to wire next. Arc Bot / LIMA AI Office is the primary guarded task-oriented office consumer for this boundary review. LIMA AI OS / runtime remains the safety substrate target.

This phase does not modify `lima/`, Sparkbot, `tests/support/`, runtime behavior, helper behavior, Sparkbot wiring, HumanInput runtime bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, audit persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Boundary Definition

Arc Bot is a guarded office-task consumer that should submit inspectable task candidates into LIMA AI OS / runtime safety concepts.

Arc Bot is not:

- a full personal workstation bot
- a shell/browser/live-terminal/code-execution surface
- a Sparkbot clone
- a HumanInput runtime bridge
- an approval executor
- a dispatch system
- an audit persistence system
- a robotics or physical-world controller

## Default Posture

Arc Bot defaults stricter than personal Sparkbot:

- external writes require approval posture
- secrets require blocked or breakglass-required posture
- admin actions require blocked or breakglass-required posture
- connector setup issues block execution-like interpretation
- scheduled work is planned/awaiting approval, not background execution
- physical-world and robotics requests are rejected or deferred
- Sparkbot-only workstation affordances are not inherited

## Consumer Boundary Fields

Arc Bot task candidates should be described with planning fields:

- `consumer_kind=arc_office`
- `task_intake`
- `task_classification`
- `office_workflow_context`
- `operator_approval_boundary`
- `explain_plan_required`
- `run_state`
- `audit_evidence_ref`
- `connector_health`
- `memory_trust`
- `agent_identity`
- `scheduled_work_posture`
- `external_write_posture`
- `secret_use_posture`
- `admin_action_posture`
- `physical_world_posture`

All fields are non-authoritative in this phase.

## Continue

Continue only to Phase 40.2 LIMA Office task/approval/audit vocabulary matrix.
