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

`GuardianDecision.decision_id` is mandatory for consequential execution. It is the audit identity that links typed intent to model calls, tools, drivers, terminal/PTY commands, files, browser/network actions, admin actions, payments, robot actions, and Spine/Audit events.

Examples in prose:

- A model request enters the Harness. Guardian classifies the request for cost, policy, and allowed model route before the Harness calls a model provider.
- A tool call is planned by the Harness. Guardian classifies it as allow, deny, approval required, or route to another path.
- A robot motion command is represented as a driver command. Guardian classifies it before the driver can execute it.

### GuardianDecision

Fields:

- `decision_id`
- `request_id`
- `intent_id`
- `input_id`
- `actor_id`
- `shell_id`
- `action_type`
- `target_ref`
- `risk_class`
- `status` / outcome
- `approval_level`
- `allowed_tool_packs`
- `constraints`
- `evidence_refs`
- `policy_version`
- `created_at`
- `expires_at`
- `decided_at`
- `decided_by`
- `reason`
- `metadata`

Rules:

- A `decision_id` must be globally unique.
- A `decision_id` must be recorded before consequential execution.
- A `decision_id` must be carried by downstream Harness, Tool, Driver, Terminal, Robot, Spine, and Audit events.
- A `decision_id` must not be reused for unrelated actions.
- Denied, escalated, expired, revoked, and superseded decisions are still audit records.
- High/critical decisions require stronger evidence and approval metadata.

### GuardianDecisionStatus

Statuses:

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

### ConsequentialActionRequest

Fields:

- `request_id`
- `intent_id`
- `input_id`
- `actor_id`
- `shell_id`
- `action_type`
- `target_ref`
- `requested_tool_pack`
- `risk_class`
- `typed_args`
- `evidence_refs`
- `metadata`

Decision rules:

- Intent Compiler does not decide.
- Guardian decides.
- Harness/Driver/Tool execution requires `GuardianDecision`.
- Spine/Audit records the outcome.
- No consequential execution may proceed without `decision_id`.

Consequential actions include model calls with user/project context, tool calls, driver commands, terminal/PTY commands, file operations, browser/network actions, external communications, private data access, state changes, admin actions, payments, deployments, robot/physical-world actions, and any operation requiring approvals, auth, vault, breakglass, or elevated permissions.

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

Harness may plan a tool call. It may only execute consequential model/tool calls when supplied with a `GuardianDecision.decision_id`. Planning and execution must remain separated so raw chat, voice transcripts, or model-generated tool plans cannot execute directly.

## Spine

Spine is the task/event/process ledger. It appends audit events, creates task records, updates task state, and retrieves lineage.

Spine records what happened. Guardian decides whether externally actionable work may happen.

### AuditEventType

Event types:

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

### AuditStatus

Statuses:

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

### AuditLineageRecord

Fields:

- `lineage_id`
- `root_event_id`
- `latest_event_id`
- `input_id`
- `intent_id`
- `decision_id`
- `approval_id`
- `policy_decision_id`
- `exposure_id`
- `execution_id`
- `actor_id`
- `shell_id`
- `risk_class`
- `status`
- `created_at`
- `updated_at`
- `closed_at`
- `metadata`

### SpineEvent

Fields:

- `event_id`
- `lineage_id`
- `event_type`
- `status`
- `timestamp` / `created_at`
- `actor_id`
- `shell_id`
- `input_id`
- `intent_id`
- `decision_id`
- `approval_id`
- `policy_decision_id`
- `exposure_id`
- `execution_id`
- `parent_event_id`
- `root_event_id`
- `action_type`
- `target_ref`
- `tool_pack`
- `selected_tools`
- `risk_class`
- `approval_level`
- `policy_version`
- `evidence_refs`
- `result_ref`
- `error_ref`
- `metadata`

### SpineAuditEvent

Fields:

- `event_id`
- `lineage_id`
- `event_type`
- `status`
- `timestamp`
- `actor_id`
- `shell_id`
- `input_id`
- `intent_id`
- `decision_id`
- `approval_id`
- `policy_decision_id`
- `exposure_id`
- `execution_id`
- `parent_event_id`
- `root_event_id`
- `action_type`
- `target_ref`
- `tool_pack`
- `selected_tools`
- `risk_class`
- `approval_level`
- `policy_version`
- `evidence_refs`
- `result_ref`
- `error_ref`
- `metadata`

Rules:

- Events do not execute actions.
- Events do not approve actions.
- Events record what happened or what was requested.
- Downstream execution events must carry `decision_id`.
- `approval_id` is required where policy requires approval.
- Denied, blocked, expired, revoked, superseded, and failed events are still audit records.
- Secrets are referenced, not stored raw.

## Driver

Drivers expose capabilities, dry-run previews, telemetry expectations, and execution calls.

Driver execution requires a scoped `GuardianDecision.decision_id`. Terminal/PTY and robot driver actions are critical risk. For Robo-OS, real hardware motion is never a default path.

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

Tool packs group tools by capability and risk area. Tool exposure is deny-by-default: shells, actors, intents, and Guardian decisions narrow which tools can reach the Harness.

### ToolPackName / ToolPackCategory

Starter categories:

- `core`
- `memory`
- `files`
- `browser`
- `network`
- `comms`
- `calendar`
- `meeting`
- `terminal`
- `system`
- `admin`
- `deploy`
- `payments`
- `robo`
- `sensors`
- `model`
- `research`
- `moderation`
- `unknown`

### ToolPackManifest

Fields:

- `pack_name`
- `description`
- `default_risk_class`
- `allowed_action_types`
- `requires_decision`
- `requires_approval_level`
- `tools`
- `constraints`
- `metadata`

### ShellToolScope

Fields:

- `shell_id`
- `actor_id` or `role_ref`
- `allowed_packs`
- `denied_packs`
- `default_packs`
- `critical_packs`
- `constraints`
- `policy_version`
- `metadata`

### ToolExposureRequest

Fields:

- `request_id`
- `shell_id`
- `actor_id`
- `intent_id`
- `decision_id`
- `requested_packs`
- `requested_tools`
- `risk_class`
- `context_refs`
- `metadata`

### ToolExposureDecision

Fields:

- `exposure_id`
- `request_id`
- `decision_id`
- `allowed_packs`
- `denied_packs`
- `selected_tools`
- `risk_class`
- `constraints`
- `reason`
- `policy_version`
- `created_at`
- `metadata`

Rules:

- ToolPack scoping does not execute tools.
- Tool exposure does not replace `GuardianDecision`.
- `decision_id` is required for consequential tool exposure.
- Tool execution still requires `GuardianDecision.decision_id`.
- Harness receives only `selected_tools`.
- Deny-by-default.

### PolicyExposure

Values:

- `allow`
- `deny`
- `require_confirmation`
- `require_guardian_review`
- `require_operator_pin`
- `require_breakglass`

These values describe policy exposure posture. They are not execution methods and do not replace `GuardianDecisionStatus`.

### ToolPackRiskRule

Fields:

- `pack_name`
- `default_risk_class`
- `read_risk_class`
- `write_risk_class`
- `destructive_risk_class`
- `default_exposure`
- `required_approval_level`
- `requires_decision`
- `requires_explicit_confirmation`
- `requires_operator_pin`
- `requires_breakglass`
- `requires_audit`
- `constraints`
- `metadata`

Rules:

- A risk rule is contract metadata, not enforcement logic.
- Risk is action-level for mixed packs such as files, browser, network, comms, calendar, memory, meeting, and robo.
- Terminal, admin, robot, payment, and deploy rules must default to critical risk.

### ToolPackRiskPolicy

Fields:

- `policy_id`
- `policy_version`
- `shell_id`
- `rules`
- `default_unknown_risk`
- `unknown_default_exposure`
- `created_at`
- `metadata`

Rules:

- Policy evaluation does not execute tools.
- Policy decision does not replace `GuardianDecision`.
- `GuardianDecision` still gates execution.
- Unknown packs/tools are denied by default.
- Dynamic tools require pack classification before exposure.

### PolicyEvaluationContext

Fields:

- `shell_id`
- `actor_id`
- `intent_id`
- `decision_id`
- `requested_pack`
- `requested_tool`
- `action_type`
- `risk_class`
- `metadata`

The context packages the inputs needed to evaluate risk policy after Guardian and tool-pack scoping have narrowed the request. It does not authorize execution by itself.

### PolicyDecision

Fields:

- `policy_decision_id`
- `policy_id`
- `decision_id`
- `allowed`
- `pack_name`
- `tool_name`
- `risk_class`
- `approval_level`
- `reason`
- `constraints`
- `metadata`

Rules:

- A policy decision is auditable policy evidence.
- A policy decision cannot expand `GuardianDecision.allowed_tool_packs`.
- A policy decision cannot add tools that are not in the Harness `selected_tools` shortlist.
- Denied policy decisions are still audit records.

### PolicyProtocol

Protocol surface:

- `describe_policy() -> ToolPackRiskPolicy`
- `evaluate(context: PolicyEvaluationContext) -> PolicyDecision`

Rules:

- `PolicyProtocol` has no execute method.
- `evaluate` produces policy evidence only.
- Execution remains behind `GuardianDecision` and later approved Harness, Tool, or Driver paths.

## Approval

Approval contracts represent pending, approved, denied, expired, and routed decisions. Approval state must be auditable and tied to a Guardian decision.

### ApprovalStatus

Statuses:

- `pending`
- `approved`
- `denied`
- `expired`
- `revoked`
- `superseded`

### ApprovalMethod

Methods:

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

### ApprovalMetadata

Fields:

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

### ApprovalScope

Fields:

- `decision_id`
- `actor_id`
- `shell_id`
- `action_type`
- `target_ref`
- `tool_pack`
- `selected_tools`
- `risk_class`
- `constraints`
- `expires_at`
- `policy_version`

### ApprovalProtocol

Methods:

- `describe_required_approval(scope) -> ApprovalMetadata | None`
- `record_approval(approval) -> None`

Rules:

- Approval protocol methods describe or record approval evidence.
- Approval protocol methods do not execute actions.
- Approval protocol methods do not enforce approval policy.

### ApprovalAuditEvent

Fields extend `AuditEvent` with:

- `approval_id`
- `approval_level`
- `approval_method`
- `status`
- `risk_class`
- `action_type`
- `target_ref`
- `tool_pack`
- `selected_tools`
- `policy_version`

Rules:

- Approval metadata does not execute actions.
- Approval metadata does not replace `GuardianDecision`.
- Approval must be scoped.
- Approval can expire/revoke/supersede.
- Critical actions require explicit approval metadata when policy says so.
- Thought/BCI cannot directly approve critical actions.

## Redaction / Privacy

Redaction and privacy contracts classify what audit/spine events may store directly, summarize, reference, retain, or hide from views. Redaction does not authorize execution.

### PrivacyClass

Classes:

- `public`
- `internal`
- `private`
- `confidential`
- `secret`
- `restricted`
- `safety_critical`
- `biometric`
- `unknown`

### RedactionClass

Classes:

- `none`
- `summary_only`
- `reference_only`
- `hash_only`
- `masked`
- `secret_ref_only`
- `drop`
- `operator_only`
- `breakglass_only`

### RetentionClass

Classes:

- `ephemeral`
- `short`
- `standard`
- `extended`
- `legal_hold`
- `do_not_store`

### VisibilityClass

Classes:

- `public_view`
- `operator_view`
- `admin_view`
- `security_view`
- `breakglass_view`
- `system_only`
- `no_view`

### DataReference

Fields:

- `ref_id`
- `ref_type`
- `uri`
- `privacy_class`
- `redaction_class`
- `retention_class`
- `visibility_class`
- `content_hash`
- `created_at`
- `expires_at`
- `metadata`

### RedactionMetadata

Fields:

- `privacy_class`
- `redaction_class`
- `retention_class`
- `visibility_class`
- `content_refs`
- `evidence_refs`
- `secret_refs`
- `redacted_summary`
- `contains_secret`
- `contains_biometric`
- `contains_safety_critical`
- `data_subject_ref`
- `retention_expires_at`
- `metadata`

### PrivacyProtocol

Protocol surface:

- `describe_reference(ref) -> RedactionMetadata`

Rules:

- References do not expose raw content.
- `secret_ref` never contains raw secret.
- Redaction does not authorize execution.
- Events may carry refs/summaries, not raw sensitive content.
- Raw secrets are never written to audit events.

## Runtime Boundary Map

Runtime boundary contracts classify inspected Sparkbot, Guardian Suite, and Robo-OS surfaces before extraction. Boundary mapping does not migrate code, execute tools, or authorize extraction.

### BoundaryClassification

Classes:

- `shell_adapter`
- `human_input_adapter`
- `intent_boundary`
- `guardian_contract`
- `harness_contract`
- `tool_pack_candidate`
- `policy_candidate`
- `approval_candidate`
- `spine_audit_candidate`
- `privacy_redaction_candidate`
- `driver_candidate`
- `system_service`
- `persistence_candidate`
- `do_not_extract_yet`
- `deprecated_or_unsafe_shortcut`
- `unknown`

### ExtractionStatus

Statuses:

- `ready_for_adapter_design`
- `needs_contract_review`
- `needs_pack_classification`
- `needs_privacy_review`
- `needs_decision_gate`
- `needs_approval_metadata`
- `needs_lineage_mapping`
- `do_not_extract_yet`
- `unknown`

### RuntimeBoundaryRecord

Fields:

- `source_repo`
- `source_path`
- `surface_name`
- `current_role`
- `classification`
- `future_lima_location`
- `required_contracts`
- `risk_level`
- `extraction_status`
- `notes`
- `metadata`

### BoundaryMapProtocol

Protocol surface:

- `list_records() -> Sequence[RuntimeBoundaryRecord]`

Rules:

- Boundary records do not extract implementation.
- Boundary records do not authorize execution.
- Unsafe shortcuts are marked do-not-extract-yet.
- Sparkbot parity means preserving behavior, not unsafe internal shortcuts.
- Robo-OS is classified as a Guardian-gated driver/runtime integration.

## AuditEvent

Audit events are immutable evidence of runtime decisions and actions. They should contain safe metadata, actor identity, source shell, risk posture, correlation IDs, and `decision_id` for consequential execution.

Audit events that participate in a consequential chain should also carry `lineage_id`, parent/root event references when available, and result/error references. `AuditLineageRecord` tracks the latest known state of the chain without executing or approving any action.

Audit and Spine events may carry:

- `privacy_class`
- `redaction_class`
- `retention_class`
- `visibility_class`
- `content_refs`
- `secret_refs`
- `redacted_summary`
- `contains_secret`
- `contains_biometric`
- `contains_safety_critical`
- `data_subject_ref`
- `retention_expires_at`

## ModelCall

Model call events record request metadata, selected route, cost/token posture, result metadata, and `decision_id` for consequential model calls. They must not leak raw secrets.

## ToolCall

Tool call events record planned action, tool identity, arguments metadata, Guardian decision, execution result metadata, and audit correlation.

Tool arguments containing sensitive material must be redacted or represented as vault references in audit surfaces.
