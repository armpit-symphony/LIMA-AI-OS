# Tool-Pack Risk Policy

## Purpose

This policy defines default risk classes and approval expectations for each LIMA tool pack.

It does not implement enforcement. It does not execute tools. It does not replace `GuardianDecision`. It gives future Guardian and Harness extraction a clear policy target before any runtime enforcement exists.

`GuardianDecision` still gates execution. A policy decision can narrow or block exposure, but it cannot authorize execution by itself.

## Core Rule

Tool packs are deny-by-default.

A pack may be exposed only when:

- the shell allows it
- the actor/session allows it
- the `IntentEnvelope` supports it
- `GuardianDecision` allows it
- pack risk policy allows it
- approval requirements are satisfied
- the selected tool shortlist is auditable

## Policy Chain

```text
HumanInput
  -> IntentEnvelope
  -> GuardianDecision
  -> ToolPackScope
  -> ToolPackRiskPolicy
  -> Harness selected_tools
  -> Approved execution
  -> Spine/Audit event
```

Policy evaluation is a guardrail in the chain. It is not an execution surface.

## Risk Classes

LOW:

- read-only
- informational
- reversible
- no external side effect
- no private data mutation

MEDIUM:

- local drafts
- internal state changes
- non-public planning
- limited memory writes
- low-impact scheduling/draft actions

HIGH:

- external messages
- file modification
- network/API calls
- browser actions with side effects
- private data access
- calendar changes
- admin reads
- expensive model/tool usage

CRITICAL:

- terminal/PTY/shell
- deploys
- payments
- secret/vault access
- credential/security changes
- admin writes
- destructive file operations
- robot movement/manipulation
- physical-world actions
- production changes
- irreversible actions

## Approval Levels

NONE:

- only for low-risk read-only actions when policy allows

CONFIRM:

- explicit human confirmation required

GUARDIAN_REVIEW:

- Guardian policy review required before action

OPERATOR_PIN:

- operator PIN required for privileged/high-risk action

BREAKGLASS:

- emergency/critical override with strict audit and expiry

DENIED:

- blocked by default

## Default Pack Policy Table

| Pack | Default risk | Default exposure | Required approval | Allowed by default for shells | Denied by default for shells | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| core | LOW | Minimal read/status primitives only | NONE or GUARDIAN_REVIEW depending on shell/context | Sparkbot, Arc, SparkPit, Robo-OS | None, subject to shell policy | Still audit consequential use. |
| model | LOW to HIGH depending on context, cost, and data | Scoped model calls only | `decision_id` for model calls with user/project context; GUARDIAN_REVIEW for expensive/private-data calls | Sparkbot, Arc, SparkPit, Robo-OS planning contexts | Untrusted shells without model allowance | Expensive or private-data model calls are HIGH. |
| memory | Read LOW/MEDIUM; write HIGH | Read-only memory may be scoped; writes require decision | GUARDIAN_REVIEW for writes; CONFIRM for sensitive writes/deletes | Sparkbot, Arc where memory is enabled | Public/anonymous shells | Sensitive memory requires review. |
| files | Read MEDIUM/HIGH; write/delete HIGH/CRITICAL | Denied unless shell and decision allow | GUARDIAN_REVIEW or CONFIRM for writes; OPERATOR_PIN/BREAKGLASS for destructive operations | Sparkbot, Arc with file scope | SparkPit web local files, Robo-OS by default | Destructive file ops are CRITICAL. |
| browser | Read/research MEDIUM; authenticated/side-effect actions HIGH/CRITICAL | Read-only browsing may be scoped; side effects denied by default | CONFIRM or GUARDIAN_REVIEW for side effects; OPERATOR_PIN for critical authenticated actions | Sparkbot, Arc, research shells | Robo-OS and public web shells by default | Browser reads and clicks/forms are separate risk classes. |
| network | Outbound HTTP/API HIGH unless clearly read-only | Unknown external calls denied | GUARDIAN_REVIEW for external API calls; CONFIRM for data submission | Sparkbot, Arc, SparkPit research when scoped | Robo-OS by default except declared telemetry endpoints | Unknown destinations stay denied. |
| comms | Drafts MEDIUM; sends HIGH | Draft-only by default where allowed; sends denied until approved | CONFIRM and/or GUARDIAN_REVIEW for external sends | Sparkbot, Arc draft-style flows | Robo-OS, broad web shells unless role-scoped | External send requires confirmation/review. |
| calendar | Read MEDIUM; create/update/delete HIGH | Reads may be scoped; writes denied until approved | CONFIRM or GUARDIAN_REVIEW for changes/invites | Sparkbot, Arc | SparkPit web and Robo-OS unless explicitly enabled | External invites are HIGH. |
| meeting | Internal meeting flow MEDIUM | Scoped internal flow only | Follows target pack risk when meeting action triggers tools | Sparkbot, Arc | Public shells unless meeting-scoped | Scheduled/tool-triggering meeting work inherits target pack risk. |
| terminal | CRITICAL | Denied by default | OPERATOR_PIN or BREAKGLASS depending policy | None by default; Sparkbot operator shell only after explicit decision | Arc, SparkPit web, Robo-OS, future robots by default | Raw shell/PTY is never a default model tool. |
| system | HIGH/CRITICAL | Denied except scoped diagnostics | GUARDIAN_REVIEW for reads; OPERATOR_PIN/BREAKGLASS for service/runtime controls | Sparkbot operator shell for read-only diagnostics | Arc, SparkPit web, Robo-OS unless explicitly scoped | Service controls are critical if they affect runtime/prod. |
| admin | Admin read HIGH; admin write CRITICAL | Denied by default | OPERATOR_PIN or BREAKGLASS for writes; GUARDIAN_REVIEW for reads | None by default; role/policy only | All non-admin shells | Vault/breakglass/user-policy surfaces are not ordinary tools. |
| deploy | CRITICAL | Denied by default | Explicit approval plus OPERATOR_PIN or BREAKGLASS | None by default | All shells by default | Production-affecting deploys are critical. |
| payments | CRITICAL | Denied by default | Explicit confirmation plus GUARDIAN_REVIEW and role policy | None by default | All shells by default | Payment tools remain denied until dedicated contracts exist. |
| robo | Movement/manipulation CRITICAL; command planning may be HIGH | Sensor-free planning only unless scoped; motion denied by default | CONFIRM/GUARDIAN_REVIEW for planning; OPERATOR_PIN or BREAKGLASS for physical action | Robo-OS planning shell when explicitly enabled | SparkPit web, Arc, Sparkbot unless explicitly enabled | Physical-world action requires approval and dry-run/simulation when available. |
| sensors | MEDIUM/HIGH depending privacy | Read-only telemetry may be scoped | GUARDIAN_REVIEW for camera/mic/location/private telemetry | Robo-OS sensor read, Sparkbot voice where enabled | Public shells by default | Camera, mic, location, and private telemetry need review. |
| research | LOW/MEDIUM for read-only; HIGH if private data/network/browser/publishing involved | Scoped read-only research only | GUARDIAN_REVIEW for private data or external publishing | Sparkbot, Arc, SparkPit research | Robo-OS by default | Action-level policy applies when research uses other packs. |
| moderation | MEDIUM/HIGH; CRITICAL for admin-impacting moderation | Role-gated only | GUARDIAN_REVIEW; OPERATOR_PIN for critical admin effects | SparkPit web by role | Sparkbot, Arc, Robo-OS by default | Community moderation must stay role-scoped. |
| unknown | CRITICAL by default | Denied by default | Classification required before approval | None | All shells | Unknown packs/tools require classification before exposure. |

## Mixed Read/Write Pack Rules

Packs like files, browser, network, comms, calendar, memory, meeting, and robo have mixed read/write risks.

Risk is determined by the actual action, not only the pack name.

Examples:

- file read may be MEDIUM, file delete is CRITICAL
- email draft may be MEDIUM, email send is HIGH
- calendar read may be MEDIUM, invite send/update is HIGH
- robot sensor read may be MEDIUM/HIGH, movement is CRITICAL

## Dynamic Skill Policy

Dynamic skills are denied by default unless:

- declared in a `ToolPackManifest`
- assigned to a pack
- risk-classified
- shell-approved
- `GuardianDecision.allowed_tool_packs` permits the pack
- `selected_tools` includes the tool
- audit records the exposure

Sparkbot dynamic surfaces that must not become self-authorizing runtime tools include:

- `SPARKBOT_SKILLS_DIR`
- `_register_extra()`
- `execute_tool()` fallback names

Any new, moved, fallback, or unclassified dynamic skill remains `unknown` and denied by default until it has explicit pack and risk classification.

## Scheduled / Autonomous Execution Policy

Scheduled or autonomous execution must inherit:

- original `intent_id` if applicable
- `decision_id` or renewal `decision_id`
- allowed tool packs
- risk class
- approval constraints
- expiry
- actor/shell context
- audit lineage

Task Guardian scheduled execution must inherit the target tool pack and `decision_id`. If the decision is expired or scope does not match, a new `GuardianDecision` is required.

Autonomous loops, recurring jobs, reminders, meeting actions, and workflow runners must not expand tool scope by reusing an old decision outside its constraints.

## Shell-Specific Defaults

Sparkbot:

- default packs: core, model, memory, meeting
- optional with decision: files, browser, network, comms, calendar
- critical denied by default: terminal, admin, deploy, payments, robo

Arc / LIMA AI Office:

- default packs: core, model, memory, comms/calendar draft-style flows
- optional: files, browser, research
- denied by default: terminal, deploy, robo, payments

SparkPit web:

- default packs: core, model, research/community
- role-gated: moderation/admin
- denied by default: terminal, local files, deploy, robo

Robo-OS:

- default packs: core, sensors read
- optional: robo command planning
- critical: movement/manipulation
- denied by default: payments, deploy, broad admin

Future humanoid / worker robot:

- default packs: core, sensors, task context
- critical: movement, manipulation, doors, vehicles, tools, hazardous workplace actions
- physical safety constraints required

## Policy Audit Requirements

Every policy decision must eventually record:

- `policy_version`
- `shell_id`
- `actor_id`
- `input_id` if available
- `intent_id`
- `decision_id`
- requested pack
- allowed/denied pack
- selected tools
- risk class
- approval level
- reason
- timestamp

## Extraction Blockers

- no Harness extraction until pack risk policy is reviewed
- no tool execution extraction until mixed read/write pack rules exist
- no dynamic skill extraction until dynamic skills are pack-classified
- no scheduled/autonomous execution extraction until decision inheritance is defined
- no terminal/admin/robot/payment/deploy extraction until critical-risk policy is defined

## Acceptance Criteria

- Tool-pack risk policy doc exists.
- Every starter pack has default risk and approval guidance.
- Unknown tools are denied by default.
- Dynamic skills are denied by default unless classified.
- Mixed read/write pack rules are documented.
- Scheduled/autonomous execution inherits `decision_id` or requires renewal.
- No runtime implementation exists.
- No Sparkbot code copied.
- Tests validate contract shape only if contracts changed.
