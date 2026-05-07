# Tool-Pack Scoping Contract

## Purpose

Tool-pack scoping prevents models and shells from receiving every available tool by default.

Tool exposure must be explicit, minimal, risk-aware, shell-aware, and Guardian-gated. The goal is to avoid the tool firehose problem found during Sparkbot entrypoint inventory while preserving Sparkbot behavior through governed runtime contracts.

## Core Rule

No shell receives all tools by default.

Tools are deny-by-default.

A tool may be exposed only when all are true:

- the shell declares the pack
- the actor/session is allowed to use the pack
- the `IntentEnvelope` proposes or permits the pack
- `GuardianDecision` allows the pack
- risk/approval policy allows the action
- the tool belongs to the selected shortlist for the current request

The required future chain is:

```text
HumanInput
  -> IntentCompiler
  -> IntentEnvelope
  -> GuardianDecision
  -> ToolPackScope
  -> Harness tool shortlist
  -> Approved tool execution
  -> Spine / Audit event
```

Tool exposure does not replace `GuardianDecision`. It narrows the tools available after Guardian has produced a scoped decision.

## Shells and Tool Packs

Future shells declare tool packs as part of their shell manifest. These examples are contract-level targets, not implementation wiring.

Sparkbot:

- chat
- memory
- files
- browser
- meeting
- terminal only with critical approval
- admin only with elevated approval

Arc / LIMA AI Office:

- comms
- calendar
- files
- browser
- memory
- office automation
- no terminal by default
- no robot by default

SparkPit web:

- community
- research
- messaging
- moderation/admin only by role
- no local filesystem/terminal by default

Robo-OS / robot shell:

- robo
- sensors
- device drivers
- local navigation
- no broad admin/payment/deploy tools by default
- physical-world actions are critical risk

Future humanoid / worker robot:

- robo
- sensors
- environment
- task execution
- explicit physical safety constraints
- critical risk for movement, manipulation, doors, vehicles, tools, or workplace hazards

## Starter Tool Packs

Starter packs:

- core
- memory
- files
- browser
- network
- comms
- calendar
- meeting
- terminal
- system
- admin
- deploy
- payments
- robo
- sensors
- model
- research
- moderation
- unknown

These are contract-level groups, not implementation packages yet.

## Risk Classes by Pack

LOW:

- core read-only
- informational
- local non-sensitive memory reads

MEDIUM:

- draft files
- local notes
- non-public planning
- limited browser research

HIGH:

- external messages
- file modification
- network calls
- private data access
- admin read access
- expensive model/tool usage
- calendar changes

CRITICAL:

- terminal/PTY
- system admin writes
- payments
- deploys
- secrets/vault access
- robot movement/manipulation
- physical-world actions
- destructive file operations
- credential/security changes

## Tool Exposure Pipeline

1. `ShellManifest` declares allowed packs.
2. Actor/session policy narrows packs.
3. `IntentEnvelope` proposes needed packs.
4. `GuardianDecision` allows, denies, or constrains packs.
5. Harness receives only the selected tool shortlist.
6. Tool execution must carry `GuardianDecision.decision_id`.
7. Spine/Audit records exposed packs, selected tools, and executed tools.

## Tool Shortlist

The Harness should receive a shortlist, not the whole catalogue.

Shortlist inputs:

- `shell_id`
- `actor_id`
- `intent_id`
- `decision_id`
- allowed tool packs
- `risk_class`
- `target_ref`
- current task/session context

## Forbidden Patterns

- giving every model call every tool
- exposing terminal/admin/robot/payment/deploy packs by default
- allowing model-generated tool calls to execute without `GuardianDecision`
- shell-side bypass of pack declarations
- runtime fallback to full catalogue
- using natural language alone as tool authorization
- reusing a `decision_id` to expand tool scope
- hiding tool exposure from audit

## Audit Requirements

Every tool exposure decision should be auditable.

Record:

- `shell_id`
- `actor_id`
- `intent_id`
- `decision_id`
- requested packs
- allowed packs
- denied packs
- selected tools
- `risk_class`
- `policy_version`
- timestamp

## Sparkbot Extraction Notes

Sparkbot's broad tool catalogue should not be extracted directly as a universal runtime catalogue.

Before Harness extraction:

- identify Sparkbot tool definitions
- group them into packs
- mark terminal/admin/file/network/browser tools with risk class
- prevent `stream_chat_with_tools()` from exposing all tools at once
- ensure tool execution requires `GuardianDecision.decision_id`

## Acceptance Criteria

- `ToolPackManifest` contract exists or is expanded.
- `ShellToolScope` or equivalent contract exists.
- `ToolExposureRequest` and `ToolExposureDecision` contracts exist.
- Harness docs require a scoped shortlist, not a full catalogue.
- Shells declare allowed packs.
- Pack exposure is deny-by-default.
- Critical packs require `GuardianDecision` and approval level.
- No runtime implementation exists.
- No Sparkbot code is copied.
- Tests validate imports and contract shape only.
