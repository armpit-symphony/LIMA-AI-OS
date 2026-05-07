# Guardian Decision Contract

## Purpose

`GuardianDecision` is the mandatory authorization, denial, escalation, or policy classification record that links human intent to consequential execution.

It is not optional. It is not advisory. It is the execution gate.

No consequential execution may proceed without `GuardianDecision.decision_id`.

## Decision Chain

```text
HumanInput.input_id
  -> IntentEnvelope.intent_id
  -> GuardianDecision.decision_id
  -> ModelCallEvent / ToolCallEvent / DriverEvent / TerminalEvent / SpineEvent
```

Every consequential action must be traceable through this chain.

## Consequential Action Definition

A consequential action is anything that may:

- call a model with user/project context
- execute a tool
- call a driver
- touch filesystem
- use browser or network
- send external communication
- access private data
- change state
- modify/delete files
- run terminal/PTY/shell commands
- administer systems
- spend money
- deploy production changes
- move robot hardware
- affect the physical world
- require approvals, auth, vault, breakglass, or elevated permissions

## Decision Outcomes

Decision outcomes are represented by `GuardianDecisionStatus`:

- `approved`
- `denied`
- `needs_clarification`
- `needs_human_confirmation`
- `needs_operator_pin`
- `needs_breakglass`
- `escalated`
- `expired`
- `revoked`
- `superseded`

Denied, escalated, expired, revoked, and superseded decisions are still audit records. They are not execution credentials.

## Decision Scope

A `GuardianDecision` must be scoped to:

- `actor_id`
- `shell_id`
- `input_id`
- `intent_id`
- `action_type`
- `target_ref`
- `allowed_tool_packs`
- `risk_class`
- `approval_level`
- expiry
- constraints
- `policy_version`

It must not be reused for unrelated actions. A decision for a read-only model summary cannot authorize file writes, terminal commands, browser clicks, robot motion, payments, admin changes, or external communication.

## Decision ID Rules

- `decision_id` must be globally unique.
- `decision_id` must be carried by every downstream event.
- `decision_id` must be recorded before execution.
- `decision_id` must be immutable after issuance.
- `decision_id` may expire.
- `decision_id` may be revoked.
- Denied decisions must still be auditable.
- High/critical decisions require stronger evidence and approval metadata.

## Approval Token vs Decision ID

- `decision_id` is the audit identity.
- `approval_token`, if later implemented, is the execution credential.
- Phase 0.7 defines the contract only, not token issuance logic.
- A decision can exist without an approval token, especially denied, escalated, expired, revoked, or superseded decisions.

## Risk Handling

`LOW`: read-only / informational. May be auto-approved by policy later.

`MEDIUM`: limited side effects. May require confirmation depending on shell policy.

`HIGH`: files, network, external communications, privileged data, expensive model/tool use. Requires Guardian review or explicit confirmation.

`CRITICAL`: terminal/PTY, production systems, payments, credential/security changes, robot/physical-world actions, destructive operations. Requires explicit human approval, operator PIN, or breakglass depending on policy.

## Carry-Forward Risks From Sparkbot Inventory

- `stream_chat_with_tools()` couples raw chat, model planning, Guardian policy, and tool execution too closely for direct extraction.
- Voice transcripts need `HumanInput` plus transcript confidence before Guardian decision.
- Terminal/PTY must be critical-risk and require `IntentEnvelope + GuardianDecision`.
- Robotics bridge must not parse natural language directly into robot MCP execution.
- Tool catalogue needs shell/tool-pack scoping.

## Harness / Tool / Driver Requirements

- Harness cannot execute consequential model/tool calls without `decision_id`.
- Tool execution must carry `decision_id`.
- Driver execution must carry `decision_id`.
- Terminal/PTY execution must carry `decision_id` and critical risk class.
- Robot driver execution must carry `decision_id`, dry-run metadata if available, and critical risk approval.
- File/network/browser/admin/payment actions must carry `decision_id`.

## Spine / Audit Requirements

Every downstream event must include:

- `decision_id`
- `intent_id` if available
- `input_id` if available
- `actor_id`
- `shell_id`
- `action_type`
- `target_ref`
- `risk_class`
- result/status
- timestamp
- evidence refs when applicable

## Acceptance Criteria

- `GuardianDecision` contract exists.
- `GuardianDecisionStatus` enum exists.
- `ConsequentialActionRequest` contract exists.
- Downstream event docs require `decision_id`.
- Harness/Driver docs require `decision_id` for consequential execution.
- Terminal/PTY and robot actions are critical-risk in docs.
- No runtime implementation exists.
- No Sparkbot code copied.
- Tests validate imports and contract shape only.
