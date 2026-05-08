# Architecture Decisions

## ADR-0001: Extract, Do Not Greenfield

Status: Accepted

Sparkbot is the battle-tested source of truth. LIMA Runtime will be extracted from Sparkbot behavior with parity checks instead of rebuilt from a blank slate.

Consequence: Phase 0 creates contracts and docs only. Runtime behavior waits until contract review and extraction planning.

## ADR-0002: Guardian Is Mandatory Trust Boundary

Status: Accepted

Guardian is the syscall gate for every external action, tool execution, privileged operation, model call, robotics action, file/network/browser action, and approval-requiring operation.

Consequence: Guardian cannot be optional. Public Harness APIs cannot directly execute tools without Guardian classification and approval state.

## ADR-0003: MCP Is Driver/Tool/Plugin Boundary

Status: Accepted

MCP is used for external tools, drivers, Robo-OS, browser/filesystem/network adapters, plugins, and shell/runtime boundaries where useful.

Consequence: Internal Guardian, Harness, Spine, Storage, and policy contracts may use direct Python Protocols/ABCs. The internal kernel is not forced through MCP.

## ADR-0004: One Persistence Interface, Multiple Backends

Status: Accepted

Runtime persistence uses one contract with multiple backends: SQLite for local/desktop, Postgres for hosted, Memory/Vault backends, and future stores.

Consequence: Contracts store secret references, not raw secrets.

## ADR-0005: Tool-Pack Scoping Is Required

Status: Accepted

Shells declare allowed tool packs such as comms, robo, system, browser, files, memory, and admin.

Consequence: The Harness scopes tool catalogues per shell and request context. The model is not handed every available tool by default.

## ADR-0006: Sparkbot Remains The Parity Source

Status: Accepted

Sparkbot stays the current product shell and source of truth until LIMA Runtime parity is proven.

Consequence: Any extracted Guardian, Harness, Spine, driver, shell, or persistence behavior must be checked against Sparkbot behavior before Sparkbot is placed on top of LIMA Runtime.

## ADR-0007: Natural Language Is The Human Control Plane

Status: Accepted

Decision: LIMA Runtime treats natural language as a first-class OS primitive and human control plane. Text, voice, console, and future thought/BCI-style inputs enter through an Intent Compiler and become typed `IntentEnvelope` records before Guardian evaluates them.

Rationale: LIMA is built for human-controlled AI infrastructure. Humans need to command, understand, approve, and audit AI systems in natural language. Raw language is ambiguous and unsafe as an execution format, especially for robots, files, network access, admin functions, payments, and physical-world actions.

Consequences:

- Raw language cannot directly execute tools or drivers.
- All consequential commands require typed intent.
- Ambiguous intent requires clarification.
- High-risk intent requires Guardian approval.
- Voice is normalized into the same contract as text.
- Future thought/BCI input is confirm-only and never direct execution.
- Every action is traceable: `HumanInput -> IntentEnvelope -> GuardianDecision -> Action/Event`.

## ADR-0008: Intent Compiler Cannot Execute

Status: Accepted

Decision: The Intent Compiler is a translation and clarification boundary only. It cannot execute tools, call drivers, perform file/network/browser/admin/payment/robot actions, or approve its own output.

Rationale: Natural language is ambiguous. LIMA must preserve human control and Guardian review before consequential execution.

Consequences:

- `IntentCompilerProtocol` remains non-executing.
- Execution belongs behind Guardian-approved Harness/Driver/Tool paths.
- Ambiguity creates `ClarificationRequest`.
- Low-confidence intent cannot proceed to execution.
- High/critical-risk intent requires Guardian escalation and explicit approval.
- Future BCI/thought input remains confirm-only.

## ADR-0009: Inventory Sparkbot Entrypoints Before Extraction

Status: Accepted

Decision: Before extracting Guardian, Harness, Spine, or tool execution paths, LIMA Runtime will inventory Sparkbot's current entrypoints and map them to the contracts-first architecture.

Rationale: Sparkbot is the spec, but not every implementation shortcut should become part of the kernel. Inventory protects LIMA from inheriting raw chat-to-tool shortcuts, unclear side-effect paths, or shell-specific code as runtime primitives.

Consequences:

- Extraction is blocked until entrypoints are reviewed.
- Sparkbot parity means preserving user-facing behavior, not preserving unsafe internal shortcuts.
- Each entrypoint must map to `HumanInput`, `IntentEnvelope`, `GuardianDecision`, Harness, Driver, Spine, ToolPack, Shell, or be marked out-of-scope.
- High-risk areas such as terminal, files, network, admin, and future robot actions require explicit Guardian coverage.

## ADR-0010: GuardianDecision IDs Are Required For Consequential Execution

Status: Accepted

Decision: Every consequential LIMA Runtime action must be linked to a `GuardianDecision.decision_id` before execution.

Rationale: LIMA must preserve human control, auditability, and safety across model calls, tools, drivers, terminal, files, network, browser, admin, payments, and robots.

Consequences:

- Raw language cannot execute directly.
- Intent Compiler cannot approve or execute.
- Harness/Tool/Driver execution requires `decision_id`.
- Terminal/PTY and robot actions are critical risk.
- Denied, escalated, expired, revoked, and superseded decisions are still audit records.
- Sparkbot parity must adapt current behavior to decision-gated execution.

## ADR-0011: Tool Exposure Is Deny-by-Default and Pack-Scoped

Status: Accepted

Decision: LIMA Runtime will expose tools through explicit tool packs scoped by shell, actor/session, intent, risk class, and `GuardianDecision`. No shell or model call receives the full catalogue by default.

Rationale: Broad tool exposure creates safety, cost, privacy, and reliability risks. Sparkbot's current broad tool-aware path must be adapted into scoped packs before extraction.

Consequences:

- Shells declare allowed packs.
- `GuardianDecision` constrains `allowed_tool_packs`.
- Harness receives a tool shortlist.
- Critical packs require explicit approval.
- Tool exposure is auditable.
- Sparkbot parity must preserve behavior without preserving full-catalogue exposure.

## ADR-0012: Sparkbot Tools Must Be Inventoried Into Packs Before Harness Extraction

Status: Accepted

Decision: Before extracting Sparkbot's Harness or tool catalogue into LIMA Runtime, current Sparkbot tool surfaces must be inventoried and grouped into deny-by-default tool packs.

Rationale: Sparkbot is the spec, but broad full-catalogue exposure must not become a LIMA Runtime primitive. Tool-pack inventory allows LIMA to preserve Sparkbot behavior while enforcing scoped, auditable, `GuardianDecision`-constrained tool exposure.

Consequences:

- Harness extraction is blocked until Sparkbot tool surfaces are classified.
- Unknown tools remain denied by default.
- Critical packs require explicit approval policy.
- Sparkbot parity means behavior parity through scoped packs, not full firehose exposure.

## ADR-0013: Tool-Pack Risk Policy Is Required Before Tool Enforcement

Status: Accepted

Decision: LIMA Runtime requires a default risk and approval policy for tool packs before Harness/tool catalogue extraction or runtime enforcement.

Rationale: Tool-pack names alone are not enough. Many packs mix read/write/destructive behavior. Sparkbot's dynamic skills and scheduled actions can expand capability surface unless each tool pack has risk and approval policy.

Consequences:

- Unknown tools are denied by default.
- Dynamic skills require classification.
- Mixed read/write tools are risked by action.
- Scheduled/autonomous execution must inherit or renew `decision_id`.
- Critical packs require explicit approval metadata.
- Harness extraction remains blocked until policy is reviewed.

## ADR-0014: Approval Metadata Is Required for High and Critical Actions

Status: Accepted

Decision: High and critical LIMA actions must carry scoped approval metadata when policy requires explicit approval.

Rationale: `GuardianDecision` establishes the policy decision, but high/critical execution also needs auditable proof of human/operator approval, method, scope, expiry, and constraints.

Consequences:

- Approval does not replace `GuardianDecision`.
- Approval metadata is scoped to decision/action/target/tool pack.
- Expired/revoked approvals cannot authorize execution.
- Breakglass is short-lived and heavily audited.
- Thought/BCI cannot directly approve critical execution.
- Scheduled/autonomous actions must inherit or renew approval.

## ADR-0015: Every Consequential Action Requires Audit Lineage

Status: Accepted

Decision: Every consequential LIMA Runtime action must be traceable through a Spine/Audit lineage chain linking human input, typed intent, Guardian decision, approval metadata, policy/tool exposure, execution, and result.

Rationale: LIMA is intended for human-controlled AI infrastructure. Traceability is required for trust, debugging, safety, compliance, replay, and future autonomous operation.

Consequences:

- `lineage_id` is required for consequential chains.
- Downstream execution events carry `decision_id`.
- `approval_id` is recorded when required.
- Denied, blocked, expired, revoked, superseded, and failed actions are auditable.
- Scheduled/autonomous work must preserve or renew lineage.
- Secrets are referenced, not stored raw.
- Extraction remains blocked until lineage contract is reviewed.

## ADR-0016: Audit Lineage Must Use Redaction and References for Sensitive Data

Status: Accepted

Decision: LIMA Runtime audit/spine events must classify sensitive data and use references, summaries, hashes, masks, or secret refs instead of storing raw sensitive content.

Rationale: LIMA is intended for human-controlled AI infrastructure across office agents, automation, and robots. Auditability must not leak secrets, private data, transcripts, sensor data, or future biometric/thought-adjacent data.

Consequences:

- Raw secrets are never written to audit events.
- Sensitive content uses `content_ref`, `evidence_ref`, `secret_ref`, `transcript_ref`, or equivalent references.
- BCI/thought-adjacent data is biometric and never direct approval/control.
- Robot sensor data requires safety/privacy defaults.
- Extraction remains blocked until privacy/redaction is reviewed.

## ADR-0017: Runtime Boundaries Must Be Mapped Before Extraction

Status: Accepted

Decision: Before extracting runtime code from Sparkbot, LIMA Guardian Suite, or LIMA Robo-OS, each candidate surface must be classified against the LIMA Runtime boundary model.

Rationale: Sparkbot is the spec, but not every implementation detail is a kernel primitive. Boundary mapping prevents shell code, unsafe shortcuts, full-catalogue exposure, direct terminal execution, raw robot commands, or private data leakage from becoming part of LIMA Runtime.

Consequences:

- Phase 1 extraction is blocked until boundary mapping is reviewed.
- Unsafe shortcuts are marked do-not-extract-yet.
- Guardian Suite coupling must be resolved before extraction.
- Robo-OS is treated as a Guardian-gated driver integration.
- Future adapters preserve behavior without preserving unsafe internals.
