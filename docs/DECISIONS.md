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

## ADR-0018: Phase 1 Starts With Decoupling Audit, Not Runtime Execution

Status: Accepted

Decision: Phase 1 will begin with Guardian Suite decoupling audit and import-boundary work, not Harness/tool execution, terminal, Robo-OS physical action, or production runtime migration.

Rationale: The safest extraction path is to remove coupling and prove boundaries before moving behavior. Sparkbot remains the spec, but unsafe shortcuts are not kernel primitives.

Consequences:

- Phase 1 PR #1 is non-executing decoupling/audit work.
- Harness extraction remains deferred.
- Terminal/PTY and robot physical action remain blocked.
- Guardian Suite coupling is the first risk to reduce.
- Runtime enforcement comes after contracts and import seams are stable.

## ADR-0019: Guardian Extraction Starts With Import Boundary Decoupling

Status: Accepted

Decision: Phase 1 starts by auditing and blocking Sparkbot `app.crud` / `app.models` / `app.services` coupling before migrating Guardian runtime behavior.

Rationale: Guardian is the trust boundary. It cannot become a reusable LIMA kernel module while depending on Sparkbot-specific backend internals.

Consequences:

- First Phase 1 work is audit/import-boundary only.
- Runtime enforcement remains deferred.
- Production Sparkbot remains untouched.
- Guardian modules must depend on LIMA contracts, not Sparkbot app modules.

## ADR-0020: Vault/Auth Extraction Starts With Non-Executing Interfaces

Status: Accepted

Decision: LIMA Runtime will define Vault/Auth interfaces before extracting any live Sparkbot or Guardian Suite vault/auth behavior.

Rationale: Vault/Auth are security-critical. LIMA must first define contracts that prevent raw secret exposure and remove Sparkbot backend coupling before runtime behavior is moved.

Consequences:

- no raw secret values in contracts
- live auth and PIN verification remain deferred
- live vault persistence/decryption remains deferred
- breakglass remains metadata-only in this phase
- future providers must be explicit adapters

## ADR-0021: Vault/Auth Providers Must Pass Boundary Tests Before Adapter Work

Status: Accepted

Decision: Before LIMA adds Vault/Auth provider adapters, provider-boundary tests must block Sparkbot imports, raw secret fields, live auth methods, decryption methods, and breakglass bypass methods.

Rationale: Vault/Auth are security-critical. Tests must preserve the seam created in Phase 1.1 before adapter code appears.

Consequences:

- future providers must depend on LIMA contracts
- raw secret fields remain forbidden
- live behavior remains deferred
- adapters require explicit review
- boundary tests become part of the safety gate

## ADR-0022: Vault/Auth Fake Providers Are Test-Only

Status: Accepted

Decision: LIMA Runtime may include fake in-memory Auth/Vault/Breakglass providers for contract validation, but they must not read real secrets, verify PINs, enforce breakglass, touch databases, or import Sparkbot internals.

Rationale: Fake providers allow safe tests and future adapter shape without moving production security behavior.

Consequences:

- test-only provider behavior is allowed
- real adapter work remains blocked
- live auth/vault/breakglass remains deferred
- no raw secret values may be introduced
- provider-boundary tests must pass

## ADR-0023: Guardian Decision Fake Evaluator Is Test-Only

Status: Accepted

Decision: LIMA may include a fake in-memory Guardian decision evaluator for contract tests, but it must not execute actions or serve as production enforcement.

Rationale: Contract tests need a safe way to produce `GuardianDecision` records before real Guardian enforcement exists.

Consequences:

- fake decisions are test artifacts only
- no real action is authorized by the fake evaluator
- critical actions should not auto-approve by default
- real enforcement remains deferred
- future adapters must not rely on fake evaluator in production

## ADR-0024: Policy/Risk Fake Evaluator Is Test-Only

Status: Accepted

Decision: LIMA may include a fake in-memory policy/risk evaluator for contract tests, but it must not authorize real execution or serve as production policy enforcement.

Rationale: Contract tests need a safe way to produce `PolicyDecision` records before real policy enforcement exists.

Consequences:

- fake policy decisions are test artifacts only
- unknown packs/tools deny by default
- high/critical packs do not auto-allow
- real policy enforcement remains deferred
- `PolicyDecision` does not replace `GuardianDecision`
- future adapters must not rely on fake evaluator in production

## ADR-0025: Approval Fake Recorder Is Test-Only

Status: Accepted

Decision: LIMA may include a fake in-memory `ApprovalMetadata` recorder for contract tests, but it must not enforce approval, verify PINs, open breakglass, issue approval tokens, or authorize execution.

Rationale: Contract tests need a safe way to record `ApprovalMetadata` before real approval enforcement exists.

Consequences:

- fake approvals are test artifacts only
- `ApprovalMetadata` remains evidence, not execution
- approval does not replace `GuardianDecision`
- real approval enforcement remains deferred
- future adapters must not rely on fake recorder in production

## ADR-0026: Spine/Audit Fake Recorder Is Test-Only

Status: Accepted

Decision: LIMA may include a fake in-memory Spine/Audit recorder for contract tests, but it must not persist data, store raw sensitive content, or execute actions.

Rationale: Contract tests need a safe way to record lineage events before real Spine storage and audit persistence exist.

Consequences:

- fake audit events are test artifacts only
- no real persistence is added
- no raw secrets or sensitive data are stored
- real audit persistence remains deferred
- future adapters must not rely on fake recorder in production

## ADR-0027: Guardian Fake Pipeline Is Test-Only

Status: Accepted

Decision: LIMA may include a fake in-memory Guardian pipeline for contract tests, but it must not enforce policy, authorize execution, execute actions, or serve as production runtime behavior.

Rationale: The contracts need an end-to-end integration proof before real enforcement or adapters are designed.

Consequences:

- fake pipeline results are test artifacts only
- no real execution is authorized
- critical actions do not auto-approve
- real runtime pipeline remains deferred
- future Sparkbot adapters must not rely on fake pipeline in production

## ADR-0028: Fake Pipeline Enables Adapter Design, Not Runtime Integration

Status: Accepted

Decision: The fake Guardian pipeline allows LIMA to begin adapter-design work, but it does not authorize production runtime integration or real enforcement.

Rationale: The fake pipeline proves contract composition but does not prove runtime safety. Adapter design can proceed only as docs/contracts/tests.

Consequences:

- Phase 1.10 may design Sparkbot `HumanInput` adapter boundaries
- production Sparkbot wiring remains blocked
- tool execution remains blocked
- real Guardian/policy/approval enforcement remains blocked
- audit persistence and redaction runtime remain blocked

## ADR-0029: Sparkbot Inputs Must Adapt to HumanInput Before Execution

Status: Accepted

Decision: Sparkbot input surfaces must be adapted into LIMA `HumanInput` records before any `IntentEnvelope`, `GuardianDecision`, tool planning, or execution path.

Rationale: Sparkbot is the spec, but raw chat-to-tool shortcuts are not kernel primitives. LIMA needs a clean input boundary before any runtime behavior is extracted.

Consequences:

- chat, voice, meeting, Workstation, SparkBud, and operator inputs map to `HumanInput`
- production adapter wiring remains blocked
- `stream_chat_with_tools` is not a direct extraction target
- tool/model execution remains blocked
- privacy/redaction defaults are required before persistence

## ADR-0030: HumanInput Adapter Contracts Are Describe-Only

Status: Accepted

Decision: LIMA will define describe-only `HumanInput` adapter contracts before implementing any Sparkbot adapter.

Rationale: Sparkbot input must become `HumanInput` before `IntentEnvelope`, `GuardianDecision`, planning, or execution. Describe-only contracts let LIMA define the boundary without touching live Sparkbot behavior.

Consequences:

- no live adapter implementation yet
- no Sparkbot route wiring
- raw chat-to-tool shortcuts remain blocked
- future adapters must target `HumanInput` first
- tests block execution-style adapter methods

## ADR-0032: Owner-Defined Autonomy Replaces Constant Approval Prompts

Status: Accepted

Decision: LIMA will use owner-defined autonomy profiles and capability rules instead of asking for approval on every action.

Rationale: Future AI assistants, office bots, and humanoid/worker robots must act naturally inside owner-approved boundaries. Constant PIN prompts would make the system unusable. Safety is preserved through risk classes, trusted identity, device/session policy, approval metadata, breakglass, Guardian decisions, and audit lineage.

Consequences:

- owner config controls autonomy level
- low-risk owner-approved actions can proceed without repeated prompts
- high/critical actions escalate based on policy
- vault/secrets/destructive actions remain strongly protected
- robot actions require safety constitution and safety modes
- law/human safety override owner command
- Guardian remains mandatory

## ADR-0033: First Sparkbot Adapter Uses Neutral Payloads and Passive Autonomy Metadata

Status: Accepted

Decision: The first Sparkbot HumanInput adapter skeleton must use neutral LIMA-owned payload dataclasses and may carry owner-autonomy context only as passive metadata.

Rationale: Neutral payloads preserve the HumanInput boundary and prevent Sparkbot runtime coupling, raw chat-to-tool shortcuts, route wiring, accidental production behavior, or premature autonomy enforcement.

Consequences:

- no Sparkbot imports in Phase 1.13
- no live route wiring
- adapter returns HumanInput only
- `stream_chat_with_tools` remains blocked
- autonomy enforcement remains blocked
- production adapter implementation remains deferred

## ADR-0034: Sparkbot HumanInput Adapter Skeleton Returns HumanInput Only

Status: Accepted

Decision: The first Sparkbot adapter skeleton may convert neutral payload dataclasses into HumanInput records only.

Rationale: This allows LIMA to test input-boundary shape without importing Sparkbot, wiring routes, or preserving raw chat-to-tool shortcuts.

Consequences:

- no production wiring
- no Sparkbot imports
- no IntentEnvelope creation
- no GuardianDecision creation
- no tool/model execution
- autonomy metadata remains passive
- future implementation still requires review

## ADR-0035: HumanInput Adapter and Fake Pipeline Bridge Must Remain Separate

Status: Accepted

Decision: The Sparkbot HumanInput adapter must stop at HumanInput. Any future test-only bridge from HumanInput to the fake Guardian pipeline must be a separate component.

Rationale: Keeping the adapter separate prevents raw chat-to-tool shortcuts, premature intent inference, production wiring creep, and fake pipeline misuse.

Consequences:

- adapter returns HumanInput only
- bridge may be test-only and separate
- adapter does not create IntentEnvelope, ConsequentialActionRequest, GuardianDecision, ApprovalMetadata, PolicyDecision, or SpineEvent
- production integration remains blocked

## ADR-0036: HumanInput-to-Fake-Pipeline Bridge Is Test-Only and Separate From Adapter

Status: Accepted

Decision: LIMA may include a test-only bridge from HumanInput to FakeGuardianPipeline, but the Sparkbot HumanInput adapter must remain separate and stop at HumanInput.

Rationale: This proves contract composition without turning the adapter into an intent parser, GuardianDecision creator, or production execution path.

Consequences:

- bridge may create test-only ConsequentialActionRequest from explicit metadata
- bridge must not infer intent from natural language
- adapter remains HumanInput-only
- production wiring remains blocked
- fake pipeline remains test-only

## ADR-0037: Identity and Trust Context Must Be Reviewed Before Real Adapter Work

Status: Accepted

Decision: LIMA will not begin production Sparkbot adapter implementation until identity, session, trusted-context, autonomy, and privacy mapping are reviewed.

Rationale: The current adapter skeleton uses neutral metadata. Real adapter work must not treat `actor_ref`, `session_ref`, `trusted_context_ref`, or `autonomy_notes` as verified authority.

Consequences:

- next phase is identity/session/trust mapping review
- production adapter remains blocked
- autonomy metadata remains passive
- actor/session metadata is not verified auth
- fake pipeline remains test-only

## ADR-0038: Actor and Trust References Are Passive Until Verified

Status: Accepted

Decision: `actor_ref`, `session_ref`, `trusted_context_ref`, `autonomy_notes`, and privacy metadata must remain passive metadata until mapped into explicit `AuthContext`, `TrustedDeviceContext`, `IdentityConfidence`, `OwnerAutonomyProfile`, and redaction/visibility enforcement.

Rationale: Real adapter work must not confuse references with authority. A string pointing to an actor, session, trusted device, or autonomy note is not proof of identity or permission.

Consequences:

- production adapter remains blocked
- next phase adds/extends contracts
- `actor_ref` does not equal verified identity
- `session_ref` does not equal verified session
- `trusted_context_ref` does not equal trusted device
- `autonomy_notes` do not enforce autonomy
- privacy metadata does not enforce redaction

## ADR-0039: Trust Context Contracts Do Not Confer Authority

Status: Accepted

Decision: `TrustedDeviceContext`, `IdentityConfidence`, `SessionContext`, and `OwnerAutonomyContext` are descriptive contracts only. They do not verify identity, authorize actions, enforce autonomy, or bypass Guardian.

Rationale: LIMA must distinguish references and confidence metadata from authority. Future adapters need structured fields, but execution authority still belongs to `GuardianDecision` and policy.

Consequences:

- references remain passive
- production adapter remains blocked
- live auth/trust/autonomy enforcement remains deferred
- Guardian remains mandatory

## ADR-0040: Adapter AuthContext Fixtures Are Passive Test Metadata

Status: Accepted

Decision: LIMA may use fake AuthContext/trust fixtures in adapter tests, but these references do not confer authority, verify identity, or enforce autonomy.

Rationale: Future adapters need to carry identity/session/trust references, but carrying a reference is not the same as verifying it.

Consequences:

- fixture tests are allowed
- adapter remains HumanInput-only
- live auth/trust enforcement remains blocked
- references are not authority

## ADR-0041: Real Sparkbot Adapter Requires Payload Stability and Verified Context

Status: Accepted

Decision: LIMA will not implement a production Sparkbot adapter until Sparkbot payload surfaces are stable/mirrored and identity/session/trust context handling is ready.

Rationale: Real adapter work would connect LIMA to live Sparkbot surfaces. Payload drift, identity ambiguity, trust-context ambiguity, and raw chat-to-tool shortcuts remain high-risk.

Consequences:

- production adapter remains blocked
- next work is fixture/boundary hardening
- no Sparkbot imports
- no route wiring
- no `stream_chat_with_tools`
- no model/tool execution

## ADR-0042: Sparkbot Payload Fixtures Are LIMA-Owned Mirrors

Status: Accepted

Decision: LIMA may maintain synthetic fixture mirrors of Sparkbot payload shapes, but must not import Sparkbot route/request objects for adapter tests.

Rationale: Fixture mirrors reduce payload drift risk while preserving LIMA's boundary from Sparkbot runtime internals.

Consequences:

- fixtures are synthetic
- no Sparkbot imports
- payload fixtures are not production contracts
- drift must be reviewed before real adapter work

## ADR-0043: Payload Fixture Drift Must Be Reviewed Against Sparkbot Origin

Status: Accepted

Decision: Before real Sparkbot adapter work, LIMA payload fixtures must be reviewed against Sparkbot origin/main or an explicit reviewed commit. Dirty local Sparkbot files are not a source of truth.

Rationale: Sparkbot moves quickly and local worktrees may contain uncommitted changes. LIMA needs stable fixture mirrors before adapter implementation.

Consequences:

- production adapter remains blocked
- fixture drift metadata is required
- dirty local Sparkbot state must be ignored or explicitly documented
- no Sparkbot imports are allowed

## ADR-0044: Adapter Modules Must Remain Runtime-Isolated Until Approved

Status: Accepted

Decision: LIMA adapter modules must not import Sparkbot runtime modules, route layers, model/tool execution, persistence, terminal, robot, or external service dependencies until a future approved phase.

Rationale: Adapters are the likely entry point for production wiring creep. Boundary tests protect the HumanInput-first architecture.

Consequences:

- adapter code remains isolated
- adapter methods remain non-executing
- production wiring remains blocked
- future adapter expansion requires explicit review

## ADR-0045: Phase 2 Starts With a Non-Production Fixture Harness

Status: Accepted

Decision: Phase 2 will begin with a non-production adapter fixture harness, not production Sparkbot wiring.

Rationale: Phase 1 proved adapter safety, fixture mirroring, drift metadata, and fake pipeline composition. It did not prove production runtime safety.

Consequences:

- production adapter remains blocked
- Phase 2 starts with LIMA-owned fixtures only
- no Sparkbot imports
- no model/tool execution
- no real enforcement
- no persistence

## ADR-0046: Phase 2 Starts With Non-production Fixture Harness

Status: Accepted

Decision: Phase 2 begins with a non-production fixture harness that runs LIMA-owned payload fixtures through the adapter and fake pipeline only.

Rationale: Phase 1 proved adapter safety and fake contract composition. The next safe step is end-to-end fixture validation without Sparkbot imports, production wiring, execution, or persistence.

Consequences:

- production adapter remains blocked
- fixtures remain synthetic mirrors
- fake pipeline remains non-production
- no model/tool execution
- no real enforcement
- no audit persistence
