# Owner Autonomy & Safety Policy

## Purpose

Define how LIMA supports owner-defined autonomy without constant PIN prompts.

LIMA should let the owner decide what the bot can do, what needs confirmation, what needs PIN/breakglass, and what is never allowed.

This policy is for future office bots, automation agents, robots, humanoid helpers, and worker robots.

## Core Principle

The bot should not ask for approval for everything.

The bot should act freely inside owner-approved boundaries and escalate only when risk, uncertainty, law, safety, privacy, or policy requires it.

Approval does not mean asking every time. Approval means owner-defined policy, trusted context, known device/session, identity confidence, risk class, capability boundary, and escalation only when needed.

The bot should "just know" only because the owner configured autonomy rules and Guardian can verify the situation.

## Owner Command Center

Future LIMA shells should expose an Owner Command Center where the owner configures autonomy and safety posture before behavior-bearing automation, adapters, tools, or robot work is enabled.

The Command Center should configure:

- autonomy level
- trusted devices
- trusted sessions
- identity methods
- voice/facial confirmation modes
- PIN/breakglass requirements
- capability permissions
- robot safety modes
- external communication rules
- deletion/destructive-action rules
- vault/secret rules
- payment/spend rules
- admin/deploy rules

The Command Center is policy setup. It does not bypass Guardian, execute actions, expose secrets, or wire production adapters.

## Autonomy Levels

### MANUAL

The bot mostly asks before action.

Use when the owner wants maximum review, during early setup, during uncertain contexts, or when a shell is untrusted.

### ASSISTED

The bot drafts and plans freely but asks before side effects.

Use for writing, planning, search preparation, schedule proposals, and other low-side-effect work where execution should remain owner-confirmed.

### TRUSTED

The bot can perform common owner-approved actions.

Use when the owner has configured specific capability rules for routine actions such as reading calendar data, creating requested events, updating safe notes, or running approved workflows.

### AUTONOMOUS_WITH_LIMITS

The bot can act within configured domains and budgets.

Use for scoped automation with clear limits, such as pre-approved communications, bounded spending, known recurring tasks, approved files, selected tool packs, and expiration windows.

### ROBOT_SAFE_AUTONOMY

The bot or robot can perform physical actions only within a safety envelope.

Use when physical-world activity is limited by concrete constraints such as geofencing, speed/force limits, sensor confidence, emergency stop, safe tools, supervised spaces, and Guardian-reviewed capability rules.

### LOCKED_DOWN

Critical systems require PIN/breakglass.

Use for vault access, destructive operations, terminal/PTY, production deploys, system administration, high-value payments, safety-critical robot work, suspicious contexts, or incident response.

## Capability Rule Matrix

Owner autonomy policy should define action-level rules for each capability category. Future contracts may represent this as capability rules tied to shell, actor, trusted context, risk class, safety mode, and Guardian decision.

Action categories:

- read information
- draft content
- create plans
- schedule/calendar
- send messages/email
- file create/edit/delete
- browser/network action
- memory read/write
- vault/secret access
- payment/spend
- admin/system change
- production deploy
- terminal/PTY
- robot movement/manipulation
- robot sensor access
- physical-world action
- legal/regulated action

For each category, future rules can be:

- always allowed
- allowed if owner requested
- allowed with verbal yes/no
- allowed only from trusted device/session
- allowed with face/voice confirmation
- requires PIN
- requires breakglass
- never allowed

Default posture is deny or escalate for unknown capability, unknown tool, unknown device/session, unknown actor, unsafe robot context, unclear target, or ambiguous owner intent.

## Default Safety Examples

Read calendar:

- allowed

Create calendar event:

- allowed if owner requested

Send email:

- allowed if owner explicitly requested recipient/content
- otherwise confirmation required

Delete files:

- PIN required

Access raw vault secret:

- PIN or breakglass required

Payments:

- confirmation or PIN depending amount

Production deploy:

- PIN or operator approval

Terminal/PTY:

- critical risk, PIN/breakglass depending scope

Robot movement near people:

- safety envelope plus confirmation or stronger approval

Unknown device requesting critical action:

- denied or strong re-verification

## Trusted Device / Session Policy

Trusted devices may reduce approval friction but never bypass safety or law.

Track:

- device_id
- owner account
- session_id
- location confidence
- recent unlock/auth
- biometric confidence if available
- anomaly score
- expiration

Rules:

- unknown devices cannot approve critical actions
- trusted devices can approve low/medium actions depending owner policy
- critical actions require stronger verification
- device trust expires or can be revoked
- suspicious context escalates

Trusted context is evidence for Guardian, not a bypass around Guardian. A trusted device cannot make unsafe, illegal, destructive, or out-of-policy work safe by itself.

## Identity Confidence

Future identity signals may include:

- known device
- login session
- voice recognition
- facial recognition
- operator PIN
- hardware key
- location/context
- behavior pattern
- future biometric/BCI signal

Identity confidence is combined with action risk and owner policy. It is not a standalone permission.

BCI/thought-adjacent signals are biometric and confirm-only. They cannot directly approve execution, directly control tools/drivers/robots, or bypass Guardian.

## Verbal Approval

Future voice approval rules:

- verbal yes/no may approve only actions allowed by owner policy
- high/critical actions may require secondary verification
- voice approval requires confidence threshold
- voice approval should be recorded as ApprovalMetadata
- voice approval cannot expose secrets or bypass Guardian
- voice approval from unknown context should escalate

Verbal approval is a confirmation method, not a universal authorization method. It must be scoped to a specific action, target, risk class, decision, and expiration window.

## Breakglass Configuration

The owner can configure what requires breakglass.

Breakglass is for exceptional or critical cases.

Rules:

- short-lived
- scoped
- reason required
- heavily audited
- revocable
- not a general bypass
- never silent

Breakglass does not remove Guardian. Breakglass creates explicit, high-friction evidence for Guardian-reviewed critical work.

## Vault and Personal Data

Vault is always high security.

Raw secrets are never stored in audit events.

Raw secret access requires strong approval.

Personal data is private/confidential by default.

The owner can grant autonomy to use references without exposing raw secrets.

Vault references, secret handles, summaries, and redacted evidence should be preferred over raw secret reveal. Personal data access should carry privacy class, redaction class, visibility class, retention class, and lineage.

## External Communication

No email/message is sent unless:

- owner explicitly requested it, or
- owner configured a pre-approved workflow, or
- confirmation/approval is satisfied.

Drafting is lower risk.

Sending is higher risk.

Recipient, content, channel, account, attachment, timing, and audience should be part of the capability boundary. Ambiguous recipients, sensitive content, unknown accounts, or unusual destinations should escalate.

## Destructive Actions

Deletion/destructive actions require PIN or stronger approval by default.

Includes:

- file delete
- database delete
- account removal
- secret deletion
- memory wipe
- production destructive operation
- robot action that can damage property

Destructive action approval should be scoped to target, action type, time, actor, shell, and rollback/recovery evidence where available.

## Robot / Humanoid Safety Constitution

LIMA Safety Constitution principles:

1. Human safety comes first.
2. The robot/bot obeys the human owner unless that conflicts with human safety, law, or configured safety policy.
3. The robot/bot protects its own existence as long as that does not conflict with human safety or owner commands.

These are philosophical safety principles. Implementation requires concrete policies, sensor checks, geofencing, speed/force limits, emergency stop, confidence thresholds, and audit.

Owner authority does not override human safety, law, or configured safety policy.

## Robot Safety Modes

### OBSERVE

Sensors only.

### ASSIST

Suggestions and planning only.

### LOW_RISK_ACTION

Simple physical actions in safe environment.

### HOUSEHOLD_HELPER

Owner-approved household tasks with safety envelope.

### WORKER_ROBOT

Workplace tasks with role/geofence/tool safety.

### HUMANOID_HELPER

High trust but still safety bounded.

### EMERGENCY_STOP

Stop all physical action.

Emergency stop must remain available even when other autonomy rules are locked down, expired, denied, or under review.

## Law and Policy

The bot may not obey owner commands that violate law, human safety, or configured safety policy.

Owner authority does not override human safety.

Guardian must be able to deny or escalate requests even when the owner requested the action.

## Guardian Relationship

Owner autonomy does not remove Guardian.

Guardian uses:

- owner autonomy profile
- risk class
- identity confidence
- trusted device/session
- ApprovalMetadata
- policy rules
- safety constitution
- audit lineage

Owner-defined autonomy is one input to Guardian. It narrows what can proceed without repeated prompts, but all consequential execution remains Guardian-gated and auditable.

## Acceptance Criteria

- owner autonomy policy doc exists
- autonomy levels are defined
- capability rule matrix exists
- trusted device/session policy exists
- verbal approval policy exists
- breakglass configuration exists
- vault/personal data protection is explicit
- destructive actions default to PIN/strong approval
- robot safety constitution exists
- robot safety modes exist
- law/human safety override owner command
- no runtime behavior added
