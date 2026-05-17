# Phase 41.1 Arc Bot Candidate Preview Fixtures

Phase 41.1 adds synthetic Arc Bot / LIMA Office-shaped fixture cases for the existing `candidate_preview` helper.

The fixtures are caller-provided test data only. They do not implement Arc Bot, modify `candidate_preview.py`, modify `lima/`, modify `tests/support/`, wire Sparkbot, create HumanInput bridge behavior, create live adapters, enforce approvals, execute, dispatch, persist, mutate files, call external systems, create background work, or touch robotics or physical-world behavior.

## Fixture Set

The fixture corpus includes:

- `draft_email_no_send`
- `external_email_send_request`
- `calendar_write_request`
- `file_mutation_request`
- `low_confidence_memory_fact`
- `connector_missing_secret`
- `agent_identity_kill_switch`
- `scheduled_task_requires_approval`
- `admin_breakglass_request`
- `robotics_physical_world_request`
- `sparkbot_only_behavior_rejected`
- `strict_security_default_posture`
- `explain_plan_only_risky_request`

## Expected Preview States

Benign draft-only work may remain `proposed`. Strict-security routine review may remain `needs_review`. Missing setup and every risky external, mutation, background, admin, Sparkbot-only, robotics, or physical-world case must remain blocked or review-only and must never grant execution, approval, dispatch, persistence, bridge behavior, adapter behavior, external calls, robotics, or physical-world behavior.

## Continue

Continue only to Phase 41.2 runtime-state-free `candidate_preview` regression tests over these fixtures.
