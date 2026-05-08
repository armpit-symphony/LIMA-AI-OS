# Spine / Audit Lineage Contract

## Purpose

Define the required lineage model for LIMA Runtime.

Spine and Audit Lineage record the full chain from human control surface to result.

This contract does not implement storage. This contract does not execute actions. This contract does not approve actions. This contract defines the traceability requirements for future Spine extraction.

## Core Lineage Chain

```text
HumanInput.input_id
  -> IntentEnvelope.intent_id
  -> GuardianDecision.decision_id
  -> ApprovalMetadata.approval_id when required
  -> ToolExposureDecision.exposure_id when tools are exposed
  -> ModelCallEvent / ToolCallEvent / DriverEvent / TerminalEvent / RobotEvent
  -> ResultEvent
  -> SpineEvent / AuditLineageRecord
```

Every consequential action must carry enough IDs to reconstruct this chain.

## Required IDs

input_id:

- source human/operator input

intent_id:

- typed normalized intent

decision_id:

- Guardian decision identity and execution gate

approval_id:

- human/operator approval evidence when required

policy_decision_id:

- policy/risk decision reference when available

exposure_id:

- tool exposure decision reference

execution_id:

- concrete execution attempt

result_id:

- execution result

spine_event_id:

- canonical ledger event

lineage_id:

- end-to-end chain identifier

## Event Categories

- `human_input`
- `intent_compiled`
- `clarification_requested`
- `guardian_decision`
- `approval_recorded`
- `policy_evaluated`
- `tool_exposure_decided`
- `model_call_planned`
- `model_call_completed`
- `tool_call_planned`
- `tool_call_completed`
- `driver_command_planned`
- `driver_command_completed`
- `terminal_command_planned`
- `terminal_command_completed`
- `robot_action_planned`
- `robot_action_completed`
- `task_created`
- `task_updated`
- `scheduled_action_requested`
- `scheduled_action_executed`
- `result_recorded`
- `audit_warning`
- `audit_error`
- `lineage_closed`

## Audit Status

- `received`
- `planned`
- `approved`
- `denied`
- `escalated`
- `needs_confirmation`
- `needs_approval`
- `executing`
- `succeeded`
- `failed`
- `canceled`
- `expired`
- `revoked`
- `superseded`
- `blocked`
- `unknown`

## Required Event Fields

Every audit/spine event should carry:

- `event_id`
- `lineage_id`
- `event_type`
- `status`
- `timestamp`
- `actor_id`
- `shell_id`
- `input_id` when available
- `intent_id` when available
- `decision_id` when available
- `approval_id` when available
- `policy_decision_id` when available
- `exposure_id` when available
- `execution_id` when available
- `parent_event_id` when available
- `root_event_id` when available
- `action_type` when available
- `target_ref` when available
- `tool_pack` when available
- `selected_tools` when available
- `risk_class`
- `approval_level` when available
- `policy_version` when available
- `evidence_refs`
- `result_ref` when available
- `error_ref` when available
- `metadata`

## Parent / Root Event Rules

- every event after the first should reference a `parent_event_id` when possible
- every event should reference `root_event_id` when possible
- `lineage_id` ties the chain together
- retries create new `execution_id` but keep `lineage_id`
- superseded actions reference prior event/decision/approval where possible
- denied actions still emit audit events
- blocked actions still emit audit events
- failed actions still emit audit events

## Scheduled / Autonomous Lineage

Scheduled/autonomous actions must preserve:

- original `lineage_id` if continuing the same approved chain
- original `input_id` and `intent_id` when applicable
- original `decision_id` if still valid
- renewed `decision_id` if expired/out of scope
- `approval_id` if required and still valid
- renewed `approval_id` if expired/out of scope
- `parent_event_id` linking the scheduled execution to the scheduled request

## Critical Action Lineage

Critical actions must include stronger lineage requirements.

For:

- terminal/PTY
- admin writes
- deploy
- payments
- secrets/vault
- destructive file operations
- credential/security changes
- robot movement/manipulation
- physical-world actions

Require:

- `decision_id`
- `approval_id` when policy requires
- `risk_class` critical
- selected tools or command refs
- `target_ref`
- constraints
- `evidence_refs`
- result/status
- audit event even if denied/blocked

## Privacy / Redaction

- audit events should avoid raw secrets
- raw transcripts may be stored by reference instead of inline
- sensitive content should use `content_ref` / `evidence_ref`
- vault secrets must never be written into audit events
- future persistence must support redaction classes
- operator-facing audit can show summaries while retaining secure evidence refs

## Sparkbot Extraction Notes

- `stream_chat_with_tools()` must emit or adapt to lineage events before extraction
- voice transcript path must preserve `input_id` and transcript confidence
- terminal/PTY path must create critical lineage events
- robotics bridge must produce typed intent, `decision_id`, approval metadata, and robot action events
- dynamic skills must produce exposure and execution events with selected tools

## Acceptance Criteria

- Spine/Audit Lineage doc exists.
- Event chain is defined from `HumanInput` to Result.
- `AuditLineageRecord` or equivalent contract exists.
- `SpineEvent` contract includes `lineage_id` and parent/root event references.
- Critical action lineage requirements are documented.
- Scheduled/autonomous lineage inheritance is documented.
- Privacy/redaction guidance exists.
- No runtime storage implementation exists.
- No Sparkbot code copied.
- Tests validate import/contract shape only.
