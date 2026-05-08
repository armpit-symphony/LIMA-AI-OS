# Approval Metadata Contract

## Purpose

`ApprovalMetadata` records the human/operator authorization details required for high/critical-risk LIMA actions.

It does not execute actions. It does not replace `GuardianDecision`. It does not replace policy. It is evidence attached to a `GuardianDecision`.

## Core Rule

A critical action may only proceed when all required items exist:

```text
HumanInput
  -> IntentEnvelope
  -> GuardianDecision.decision_id
  -> ApprovalMetadata, when policy requires it
  -> ToolPackRiskPolicy satisfied
  -> approved Harness / Tool / Driver / Terminal / Robot execution
  -> Spine / Audit event
```

Approval metadata proves the authorization context. It does not authorize execution by itself.

## Approval Identity

Approval metadata records:

- `approval_id`
- `decision_id`
- `input_id`
- `intent_id`
- `actor_id`
- `shell_id`
- `approved_by`
- `approval_level`
- `approval_method`
- `status`
- `risk_class`
- `action_type`
- `target_ref`
- `tool_pack`
- `selected_tools`
- `constraints`
- `evidence_refs`
- `policy_version`
- `created_at`
- `expires_at`
- `revoked_at`
- `superseded_by`
- `reason`
- `metadata`

## Approval Levels

NONE:

- no explicit approval required

CONFIRM:

- explicit user confirmation

GUARDIAN_REVIEW:

- Guardian policy review and recorded decision

OPERATOR_PIN:

- operator PIN / privileged local confirmation

BREAKGLASS:

- emergency privileged override with short expiry and heavy audit

DENIED:

- approval denied / blocked

## Approval Methods

Approval methods:

- `chat_confirmation`
- `voice_confirmation`
- `ui_button`
- `operator_pin`
- `hardware_key`
- `signed_token`
- `breakglass`
- `delegated_admin`
- `policy_auto_approval`
- `external_system`
- `unknown`

Future voice/thought/BCI confirmation must be treated carefully. Thought/BCI cannot directly approve critical execution. It can only suggest candidate intent or candidate confirmation requiring explicit secondary confirmation.

## Approval Scope

Approval must be scoped to:

- `decision_id`
- `actor_id`
- `shell_id`
- `action_type`
- `target_ref`
- `tool_pack`
- `selected_tools`
- `risk_class`
- `constraints`
- expiry
- `policy_version`

Approval cannot be reused for unrelated actions.

## Expiry and Revocation

- approvals can expire
- approvals can be revoked
- approvals can be superseded
- expired/revoked approvals cannot authorize execution
- expired/revoked/superseded approvals remain auditable
- scheduled/autonomous execution must renew approval if expired or scope changed

## Constraints

Examples:

- max executions
- allowed time window
- target path prefix
- target host
- max spend
- allowed robot zone
- dry-run required
- require second approval
- read-only
- no destructive actions
- no external send
- no production deploy

## Critical Pack Approval Requirements

terminal:

- OPERATOR_PIN or BREAKGLASS depending command/scope

admin:

- GUARDIAN_REVIEW for reads, OPERATOR_PIN/BREAKGLASS for writes

deploy:

- OPERATOR_PIN or BREAKGLASS; production deploys require explicit confirmation

payments:

- explicit confirmation and Guardian review; high-value payments require stronger approval

secrets/vault:

- OPERATOR_PIN or breakglass depending sensitivity

robo:

- physical-world movement/manipulation requires explicit confirmation, dry-run/simulation where available, and critical approval

filesystem:

- destructive operations require explicit confirmation or stronger

network/browser:

- side-effect/authenticated actions require confirmation/review

comms:

- external send requires confirmation/review

## Breakglass Rules

Breakglass approvals:

- are critical
- must be short-lived
- must require reason
- must record actor and approver
- must record scope
- must record expiry
- must produce audit events
- must never be silent
- must not become a general-purpose approval bypass

## Scheduled / Autonomous Approval Inheritance

Scheduled/autonomous actions must carry:

- original `decision_id`
- `approval_id` when required
- inherited scope
- expiry
- `policy_version`
- renewal requirement

If approval is expired, revoked, or scope changed, execution must request a new `GuardianDecision` and approval.

## Audit Requirements

`ApprovalMetadata.approval_id` must appear in Spine/Audit events when policy requires approval.

Approval audit events must record:

- `approval_id`
- `decision_id`
- `input_id` if available
- `intent_id` if available
- `actor_id`
- `shell_id`
- `approval_level`
- `approval_method`
- `approved_by`
- `risk_class`
- `action_type`
- `target_ref`
- `tool_pack`
- `selected_tools`
- `constraints`
- `evidence_refs`
- `created_at`
- `expires_at`
- `revoked_at`
- result/status
- `policy_version`

## Acceptance Criteria

- `ApprovalMetadata` contract exists.
- `ApprovalLevel`/`ApprovalMethod`/`ApprovalStatus` are documented or represented.
- Approval metadata attaches to `GuardianDecision.decision_id`.
- Approval does not replace `GuardianDecision`.
- Critical packs have approval guidance.
- Breakglass rules are explicit.
- Scheduled/autonomous approval inheritance is documented.
- No runtime implementation exists.
- No Sparkbot code copied.
- Tests validate import/contract shape only.
