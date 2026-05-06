# Public Contracts

LIMA Runtime contracts define the kernel boundary before implementation is extracted from Sparkbot.

## Contract Rules

- Guardian is mandatory.
- Public Harness APIs must not execute tools without Guardian classification and approval state.
- Externally actionable operations use drivers or tool packs and pass through Guardian.
- MCP is the driver/tool/plugin boundary, not the mandatory internal kernel bus.
- Raw secrets must not be stored in general events; contracts use secret references.
- Shells declare allowed tool packs and permissions.
- Natural language, voice transcripts, console input, gestures, and future BCI signals compile into typed intent before consequential execution.
- Phase 0 contracts are intentionally small.

## Guardian

Guardian classifies and records decisions for model calls, tool calls, driver commands, privileged operations, and approval-requiring actions.

Examples in prose:

- A model request enters the Harness. Guardian classifies the request for cost, policy, and allowed model route before the Harness calls a model provider.
- A tool call is planned by the Harness. Guardian classifies it as allow, deny, approval required, or route to another path.
- A robot motion command is represented as a driver command. Guardian classifies it before the driver can execute it.

## HumanInput

Human input records capture the operator-facing control surface before intent is compiled.

Fields:

- `input_id`
- `source`: `text | voice | console | gesture | future_bci`
- `actor_id`
- `shell_id`
- `raw_content` or `transcript_ref`
- `timestamp`
- `locale`
- confidence metadata
- privacy/data class

Rules:

- Voice transcripts are normalized into the same contract as text commands.
- Future BCI input is future-facing only and can only produce low-confidence intent candidates requiring explicit confirmation.
- Human input records are evidence, not execution commands.

## IntentEnvelope

Intent envelopes are typed, auditable command candidates prepared for Guardian.

Fields:

- `intent_id`
- `source_input_id`
- `actor_id`
- `shell_id`
- `normalized_text`
- `intent_type`
- `typed_args`
- `confidence`
- `risk_class`
- `ambiguity_flags`
- `required_evidence`
- `required_approval_level`
- `proposed_tool_packs`
- `created_at`

Rules:

- Raw natural language must never directly execute tools or drivers.
- Every consequential command must have an `IntentEnvelope`.
- Every `IntentEnvelope` must be traceable to a `GuardianDecision` and audit events.
- High-risk intent requires Guardian approval before execution.

## Intent Lifecycle

Intent lifecycle states:

- `received`
- `normalized`
- `needs_clarification`
- `compiled`
- `submitted_to_guardian`
- `approved`
- `denied`
- `escalated`
- `expired`
- `superseded`

The intent lifecycle contract is represented by `IntentStatus`, which records where an intent sits in the control-plane pipeline. It is not an execution state machine. Execution remains behind Guardian-approved Harness, Tool, or Driver paths.

## IntentType

Starter contract-level categories:

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

These categories help Guardian and later planning surfaces inspect intent. They are not implementation dispatch hooks.

## ApprovalLevel

Approval levels:

- `none`
- `confirm`
- `guardian_review`
- `operator_pin`
- `breakglass`

The Intent Compiler may recommend a required approval level. Guardian owns the decision and escalation path.

## EvidenceRequirement

Evidence requirements describe information needed before Guardian can evaluate consequential intent.

Fields:

- `evidence_id`
- `kind`
- `description`
- `required`
- `metadata`

Confidence and risk thresholds are policy-owned, not compiler-owned. The compiler can attach evidence requirements; Guardian and policy decide whether evidence is sufficient.

## IntentCompilationResult

Compilation results package the output of one compilation attempt.

Fields:

- `input`
- `intent`
- `clarification`
- `status`
- `warnings`
- `metadata`

Results can contain an intent, a clarification request, or warnings. They do not contain execution output.

## ClarificationRequest

Clarification requests stop ambiguous commands before they become action.

Fields:

- `clarification_id`
- `intent_id`
- `question`
- `choices`
- `reason`
- `blocking`: `true | false`

## IntentCompilerProtocol

Protocol surface:

- `compile(input: HumanInput, context: SessionContext) -> IntentEnvelope`
- `clarify(intent: IntentEnvelope) -> ClarificationRequest | None`
- `revise(intent: IntentEnvelope, user_reply: HumanInput) -> IntentEnvelope`

Rules:

- The Intent Compiler does not execute actions.
- The Intent Compiler does not approve actions.
- The Intent Compiler only prepares structured intent for Guardian.
- Guardian owns approval, denial, escalation, and confirmation requirements.
- Harness and Driver APIs must require `GuardianDecision` or an approval token for consequential execution.

## Responsibility Split

- Intent Compiler creates intent.
- Guardian decides.
- Harness plans and completes model calls only after Guardian classification.
- Drivers execute only after Guardian approval.
- Spine records the chain.

## Harness

Harness owns model routing, fallback, tool catalogue filtering, prompt cache, telemetry, and friendly errors.

Harness may plan a tool call. It may only execute a guarded tool call when supplied with a Guardian decision or approval token.

## Spine

Spine is the task/event/process ledger. It appends audit events, creates task records, updates task state, and retrieves lineage.

Spine records what happened. Guardian decides whether externally actionable work may happen.

## Driver

Drivers expose capabilities, dry-run previews, telemetry expectations, and execution calls.

Driver execution requires Guardian approval. For Robo-OS, real hardware motion is never a default path.

## Storage

Storage provides one persistence interface over SQLite, Postgres, Memory/Vault backends, and future stores.

`put_secret_ref` stores references or vault handles. It does not store raw secrets.

## Shell

Shells are user-facing or environment-facing surfaces. Sparkbot, Arc / LIMA AI Office, SparkPit web, and Robo shells are shells.

Shells declare:

- allowed tool packs
- permissions
- operator identity model
- runtime capabilities they intend to use

## ToolPack

Tool packs group tools by capability and risk area.

Required pack model:

- `packs/comms`
- `packs/robo`
- `packs/system`
- `packs/browser`
- `packs/files`
- `packs/memory`
- `packs/admin`

Shells declare allowed packs. The Harness scopes the available tool catalogue from those packs. The model does not receive every available tool by default.

## Approval

Approval contracts represent pending, approved, denied, expired, and routed decisions. Approval state must be auditable and tied to a Guardian decision.

## AuditEvent

Audit events are immutable evidence of runtime decisions and actions. They should contain safe metadata, actor identity, source shell, risk posture, and correlation IDs.

## ModelCall

Model call events record request metadata, selected route, cost/token posture, and result metadata. They must not leak raw secrets.

## ToolCall

Tool call events record planned action, tool identity, arguments metadata, Guardian decision, execution result metadata, and audit correlation.

Tool arguments containing sensitive material must be redacted or represented as vault references in audit surfaces.
