# Intent Compiler Boundary

## Purpose

The Intent Compiler converts human-understandable commands into structured, inspectable, Guardian-reviewable intent.

It does not execute actions. It does not approve actions. It does not call tools. It does not call drivers. It does not call models directly for execution. It does not bypass Guardian.

The boundary exists so raw text, voice, console input, gestures, and future thought/BCI-style input cannot become consequential runtime action until LIMA has produced typed intent and Guardian has decided what may happen next.

## Human Control Surfaces

Current and future human control surfaces include:

- `text`
- `voice`
- `console` / operator command
- `gesture` / manual control
- `future_bci`

Voice transcripts follow the same path as text. Console/operator commands and manual controls still produce `HumanInput` records before intent compilation.

Future BCI/thought input is research-facing only, low-confidence by default, confirmation-only, and never direct actuation. It can suggest candidate intent, but it cannot execute tools, drivers, files, network actions, browser actions, payments, admin changes, production actions, or robot/physical-world actions.

HumanInput from voice and future BCI/thought-adjacent sources must carry privacy/biometric handling metadata before persistence or audit emission.

## Intent Pipeline

1. Receive `HumanInput`.
2. Normalize language.
3. Detect ambiguity.
4. Request clarification if needed.
5. Build `IntentEnvelope`.
6. Assign confidence.
7. Assign `RiskClass`.
8. Attach required evidence.
9. Attach required approval level.
10. Propose allowed tool packs.
11. Send to Guardian.
12. Guardian approves, denies, escalates, or requires confirmation.
13. Only after `GuardianDecision` may Harness, Driver, or Tool planning proceed.

```text
HumanInput
  -> IntentCompiler
  -> IntentEnvelope
  -> GuardianDecision
  -> Harness / Tool / Driver plan
  -> Approved execution
  -> Spine / Audit event
```

## Boundary Rules

- Raw language cannot execute tools.
- Raw language cannot call drivers.
- Raw language cannot call filesystem, network, browser, admin, payment, or robot actions.
- Voice transcripts follow the same path as text.
- Ambiguity blocks execution until clarified.
- High-risk intent requires approval.
- Critical physical-world intent requires explicit human confirmation and Guardian approval.
- Thought/BCI input can only suggest candidate intent; it cannot execute.
- Confidence and risk thresholds are policy-owned, not compiler-owned.
- The Intent Compiler may prepare `required_evidence`, `required_approval_level`, and `proposed_tool_packs`; Guardian owns the decision.

## Intent Types

Starter contract-level intent categories:

- `ask_information`
- `create_plan`
- `draft_content`
- `schedule_task`
- `run_tool`
- `operate_file`
- `browse_web`
- `send_message`
- `control_robot`
- `administer_system`
- `approve_action`
- `deny_action`
- `unknown`

These are contract-level categories, not implementation. They describe how intent is represented for Guardian review and later Harness/Driver planning.

## Risk Classes

`LOW`: read-only, reversible, informational.

`MEDIUM`: limited side effects, local draft, non-public changes.

`HIGH`: external communication, file modification, network action, privileged data access, expensive model/tool use.

`CRITICAL`: physical-world robot action, payments, deletion, credential/security changes, production deploy, admin lockout risk, irreversible action.

## Clarification Rules

Clarification is required when:

- target is missing
- actor is unknown
- command is ambiguous
- action has side effects
- scope is too broad
- risk is high or critical
- confidence is below threshold
- user intent conflicts with policy
- tool pack is unavailable
- requested shell lacks permission

Clarification produces `ClarificationRequest`. A blocking clarification prevents submission to Guardian for consequential execution until revised human input produces a clearer `IntentEnvelope`.

## Audit Chain

Every consequential action must be traceable:

```text
HumanInput.input_id
  -> IntentEnvelope.intent_id
  -> GuardianDecision.decision_id
  -> ToolCallEvent / DriverEvent / ModelCallEvent
  -> SpineEvent
```

The audit chain is part of the runtime trust boundary. Intent compilation records what the human asked for. Guardian records what was allowed, denied, escalated, or routed. Harness, Tool, Driver, and Spine events record what was planned, executed, and observed.

## Sparkbot Adapter Boundary

Sparkbot chat and voice should later become adapters that emit `HumanInput` and receive clarification or approval requirements.

Sparkbot must not preserve raw chat-to-tool shortcuts when moving onto LIMA Runtime. Existing Sparkbot behavior remains the parity source, but the extracted runtime boundary must be:

```text
Sparkbot chat/voice -> HumanInput -> IntentEnvelope -> GuardianDecision
```

No Sparkbot migration happens in Phase 0.5. No Sparkbot implementation code is copied into LIMA-AI-OS during this boundary definition.

## Acceptance Criteria

- Intent Compiler contracts exist.
- Intent lifecycle docs exist.
- No execution logic exists.
- No Sparkbot code is copied.
- Tests only validate imports and contract instantiation.
- Guardian remains mandatory.
- Harness/Driver execution contracts reference `GuardianDecision` or approval token.
- Roadmap says Phase 0.5 must complete before Harness execution extraction.
