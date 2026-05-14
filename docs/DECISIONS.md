# Architecture Decisions

Current phase and branch guidance lives in `docs/CURRENT_PROJECT_STATE.md`. Read that file before using older decisions to infer implementation sequencing.

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

## ADR-0047: Fixture Harness Expansion Requires Coverage Review

Status: Accepted

Decision: Before expanding the non-production adapter fixture harness, LIMA must review current fixture/harness coverage and identify gaps.

Rationale: Fixture harnesses can create false confidence if important Sparkbot surfaces are missing or undercovered.

Consequences:

- production adapter remains blocked
- fixture gaps must be documented
- Phase 2.2 scope is based on coverage review
- MCP/robot fixtures remain non-executing

## ADR-0048: Fixture Coverage Expansion Reduces False Confidence

Status: Accepted

Decision: LIMA will expand synthetic fixture coverage for undercovered Sparkbot surfaces before considering any production adapter work.

Rationale: A fixture harness can create false confidence if frontend, Workstation, SparkBud, auth/session, or model-routing contexts are missing.

Consequences:

- production adapter remains blocked
- expanded fixtures are synthetic mirrors
- unsupported categories may be explicitly non-executing
- references and routing metadata remain passive

## ADR-0049: Fixture Regression Requires Coverage Readiness Review

Status: Accepted

Decision: Before adding a fixture regression harness, LIMA must review fixture coverage and explicitly document unsupported or non-executing categories.

Rationale: A regression harness can create false confidence if unsupported categories pass silently or if robot/MCP/model-routing fixtures are mistaken for execution readiness.

Consequences:

- production adapter remains blocked
- unsupported/non-executing categories must be explicit
- fixture regression remains non-production
- no Sparkbot imports or execution

## ADR-0050: Fixture Regression Harness Is Non-production

Status: Accepted

Decision: LIMA may include a fixture regression harness for synthetic Sparkbot payload fixtures, but it must not become production runtime.

Rationale: Regression testing reduces drift risk, but production adapter safety is still unproven.

Consequences:

- fixture harness remains under tests/helpers or clearly non-production namespace
- unsupported categories must be explicit
- no Sparkbot imports
- no execution
- production adapter remains blocked

## ADR-0051: Fixture Regression Must Gate Future Adapter Expansion

Status: Accepted

Decision: The fixture regression harness must become a required safety gate before future adapter expansion.

Rationale: Adapter work is high-risk because it is the path toward production wiring. Regression tests over LIMA-owned fixtures reduce drift and shortcut risk.

Consequences:

- future adapter work must pass fixture regression
- production adapter remains blocked
- fixture regression remains non-production
- no Sparkbot imports or execution are allowed

## ADR-0052: Fixture Regression Is Required for Adapter-Adjacent Changes

Status: Accepted

Decision: Future adapter-adjacent changes must pass fixture regression and adapter boundary tests before merge.

Rationale: Adapter work is the path toward production wiring. Fixture regression reduces drift, shortcut, and safety-regression risk.

Consequences:

- fixture regression becomes a standing gate
- production adapter remains blocked
- manual review still required for drift and new fixture categories
- regression harness remains non-production

## ADR-0053: Phase 2 Continues With Reviewable Fixture Regression Artifacts

Status: Accepted

Decision: Phase 2 should continue by making fixture regression results easier to review before any adapter-adjacent expansion.

Rationale: The regression harness is useful only if humans can easily inspect what passed, what was unsupported, and what safety statuses were produced.

Consequences:

- production adapter remains blocked
- report artifacts are not audit persistence
- fixture regression remains non-production
- no Sparkbot imports or execution are allowed

## ADR-0054: Fixture Regression Reports Are Review Artifacts, Not Audit Persistence

Status: Accepted

Decision: LIMA may generate fixture regression report artifacts for human review, but these reports are not audit persistence or production telemetry.

Rationale: Readable reports improve review quality without changing runtime behavior.

Consequences:

- reports are test/review artifacts only
- production adapter remains blocked
- no runtime persistence is introduced
- audit persistence remains a future reviewed phase

## ADR-0055: Regression Report Must Include Gate Context Before Adapter Expansion

Status: Accepted

Decision: Fixture regression reports must include enough review context before they are used as a standing adapter-adjacent safety artifact.

Rationale: A readable report without commit, drift, boundary, and gate verdict context can create false confidence.

Consequences:

- production adapter remains blocked
- next work hardens report fields
- report remains non-production and non-persistent
- report is not audit evidence

## ADR-0056: Regression Report Gate Status Does Not Authorize Production

Status: Accepted

Decision: Fixture regression reports may include `gate_status` and review context, but report gate status does not authorize production adapter work.

Rationale: A pass/fail report improves reviewability but must not be confused with Guardian evidence, audit persistence, or production authorization.

Consequences:

- production adapter remains blocked
- report context is review-only
- manual review remains required
- report artifacts are not audit persistence

## ADR-0057: Regression Gate Requires Final Consolidated Adapter Safety Policy

Status: Accepted

Decision: Before further adapter-adjacent work, LIMA will consolidate fixture regression, adapter boundaries, drift checks, and report gate requirements into one final adapter safety gate.

Rationale: The safety rules now exist across several docs and tests. A consolidated gate reduces confusion and prevents production wiring creep.

Consequences:

- production adapter remains blocked
- next work finalizes adapter safety gate documentation
- fixture regression remains non-production
- report `gate_status` remains non-authorizing
- manual review remains required

## ADR-0058: Adapter Safety Gate Is the Standing Review Gate

Status: Accepted

Decision: LIMA will use `docs/ADAPTER_SAFETY_GATE.md` as the standing safety gate for adapter-adjacent work.

Rationale: Adapter safety rules were spread across many phase docs. A consolidated gate reduces confusion and prevents production wiring creep.

Consequences:

- adapter-adjacent PRs must satisfy the gate
- production adapter remains blocked
- manual review remains required
- future production adapter discussion requires explicit readiness review

## ADR-0059: Adapter Safety Gate Is Ready as Standing Gate

Status: Accepted

Decision: `docs/ADAPTER_SAFETY_GATE.md` is ready to serve as the standing review gate for adapter-adjacent work.

Rationale: The gate consolidates checks, tests, Sparkbot freshness, forbidden imports/behaviors, manual review rules, PR blockers, and production adapter NO-GO status.

Consequences:

- adapter safety gate work may pause
- production adapter remains blocked
- future adapter-adjacent PRs must satisfy the gate
- next work may move to the next non-production kernel boundary

## ADR-0060: IntentEnvelope Test Design Requires Explicit Typed Metadata

Status: Accepted

Decision: LIMA may design test-only IntentEnvelope fixtures using explicit typed metadata, but must not infer intent from raw natural language.

Rationale: The IntentEnvelope boundary is safety-critical. Hidden inference would recreate raw chat-to-tool shortcuts.

Consequences:

- adapter remains HumanInput-only
- future IntentEnvelope test fixtures must use explicit metadata
- no real IntentCompiler yet
- no natural-language inference
- no execution or GuardianDecision creation

## ADR-0061: IntentEnvelope Fixtures Use Explicit Metadata Only

Status: Accepted

Decision: LIMA may add IntentEnvelope test fixtures using explicit typed metadata, but `raw_text` must not be parsed or interpreted to infer intent.

Rationale: IntentEnvelope is a safety-critical boundary. Hidden natural-language inference would recreate raw chat-to-tool shortcuts.

Consequences:

- fixtures are synthetic
- explicit metadata required for expected IntentEnvelope shape
- no real IntentCompiler yet
- no model calls
- no execution
- GuardianDecision remains mandatory later

## ADR-0062: IntentEnvelope Fixture Harness Requires Readiness Review

Status: Accepted

Decision: Before creating a test-only IntentEnvelope fixture harness, LIMA must review fixture coverage and confirm `raw_text` remains inert.

Rationale: IntentEnvelope sits between HumanInput and GuardianDecision. A test harness must not become hidden intent inference.

Consequences:

- real IntentCompiler remains blocked
- natural-language inference remains blocked
- fixture harness must use explicit typed metadata only
- IntentEnvelope remains non-authorizing
- GuardianDecision remains mandatory later

## ADR-0063: IntentEnvelope Fixture Harness Does Not Infer Intent

Status: Accepted

Decision: LIMA may include a test-only IntentEnvelope fixture harness, but it must validate explicit metadata only and must not parse `raw_text` or infer intent.

Rationale: A fixture harness can harden the IntentEnvelope boundary without creating a hidden compiler or raw chat-to-tool shortcut.

Consequences:

- no real IntentCompiler
- no natural-language inference
- no execution
- no GuardianDecision creation
- IntentEnvelope remains non-authorizing

## ADR-0064: IntentEnvelope Harness Requires Standing Safety Gate

Status: Accepted

Decision: Before further IntentEnvelope-adjacent work, LIMA will define a standing safety gate for explicit metadata, `raw_text` inertness, and no-real-compiler rules.

Rationale: IntentEnvelope is a critical boundary between HumanInput and GuardianDecision. A test harness helps, but future work needs a consolidated gate.

Consequences:

- real IntentCompiler remains blocked
- natural-language inference remains blocked
- fixture harness remains test-only
- IntentEnvelope remains non-authorizing
- GuardianDecision remains mandatory later

## ADR-0065: IntentEnvelope Safety Gate Is the Standing Review Gate

Status: Accepted

Decision: LIMA will use `docs/INTENTENVELOPE_SAFETY_GATE.md` as the standing safety gate for IntentEnvelope-adjacent work.

Rationale: IntentEnvelope is the boundary between HumanInput and GuardianDecision. A consolidated gate prevents hidden natural-language inference and premature compiler/execution behavior.

Consequences:

- real IntentCompiler remains blocked
- `raw_text` remains inert
- explicit metadata required for tests
- IntentEnvelope remains non-authorizing
- manual review required for future compiler work

## ADR-0066: IntentEnvelope Safety Gate Is Ready as Standing Gate

Status: Accepted

Decision: `docs/INTENTENVELOPE_SAFETY_GATE.md` is ready to serve as the standing review gate for IntentEnvelope-adjacent work.

Rationale: The gate consolidates `raw_text` inertness, explicit metadata, fixture rules, forbidden behaviors, PR blockers, manual review, and real IntentCompiler exit criteria.

Consequences:

- IntentEnvelope safety-gate work may pause
- real IntentCompiler remains blocked
- natural-language inference remains blocked
- next work may move to Guardian request test design
- IntentEnvelope remains non-authorizing

## ADR-0067: Guardian Request Is Not GuardianDecision

Status: Accepted

Decision: LIMA may design test-only Guardian request shapes, but a Guardian request must not be treated as GuardianDecision or authorization.

Rationale: The Guardian boundary is safety-critical. A request for decision is not a decision, approval, enforcement, or execution.

Consequences:

- no GuardianDecision creation yet
- no enforcement
- no approval
- no execution
- requested tool packs are requests only
- autonomy and approval refs remain passive/descriptive

## ADR-0068: Guardian Request Fixtures Are Not Decisions

Status: Accepted

Decision: LIMA may add Guardian request test fixtures, but Guardian requests must not be treated as GuardianDecision, approval, enforcement, or execution.

Rationale: The request-to-decision boundary is safety-critical. A request describes what should be reviewed; it does not authorize action.

Consequences:

- no GuardianDecision creation yet
- no approval
- no policy enforcement
- no execution
- requested tool packs remain requests only
- approval refs remain descriptive

## ADR-0069: Guardian Request Fixture Harness Requires Readiness Review

Status: Accepted

Decision: Before creating a test-only Guardian request fixture harness, LIMA must review fixture coverage and confirm Guardian request remains non-authorizing.

Rationale: Guardian request sits directly before GuardianDecision. A test harness must not create hidden approval, enforcement, or execution behavior.

Consequences:

- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- fixture harness must validate request shape only

## ADR-0070: Guardian Request Fixture Harness Does Not Decide

Status: Accepted

Decision: LIMA may include a test-only Guardian request fixture harness, but it must not create GuardianDecision, enforce policy, approve actions, execute tools, or persist audit records.

Rationale: A fixture harness can harden the Guardian request boundary without turning requests into decisions.

Consequences:

- Guardian request remains non-authorizing
- requested tool packs remain requests only
- approval refs remain descriptive
- no real Guardian enforcement
- no execution

## ADR-0071: Guardian Request Harness Requires Standing Safety Gate

Status: Accepted

Decision: Before further Guardian-request-adjacent work, LIMA will define a standing safety gate for Guardian request fixtures and harnesses.

Rationale: Guardian request sits directly before GuardianDecision. A harness helps validate fixture shape, but future work needs a consolidated gate to prevent requests from becoming hidden decisions or approvals.

Consequences:

- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- audit persistence remains blocked
- Guardian request fixture harness remains test-only

## ADR-0076: Fake GuardianDecision Fixture Harness Requires Readiness Review

Decision:

Before creating a test-only fake GuardianDecision fixture harness, LIMA must review fixture coverage and confirm fake GuardianDecision remains non-authorizing.

Rationale:

Fake GuardianDecision sits at the most sensitive boundary so far. A harness must not convert fake decisions into hidden production authorization.

Consequences:

- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- audit persistence remains blocked
- fixture harness must validate fake decision shape only

## ADR-0077: Fake GuardianDecision Fixture Harness Does Not Authorize

Decision:

LIMA may include a test-only fake GuardianDecision fixture harness, but it must not create real GuardianDecision, enforce policy, approve actions, execute tools, or persist audit records.

Rationale:

A fixture harness can harden fake decision shape validation without turning fake decisions into production authorization.

Consequences:

- fake GuardianDecision remains test-only
- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- audit persistence remains blocked

## ADR-0078: Fake GuardianDecision Harness Requires Standing Safety Gate

Decision:

Before further fake GuardianDecision-adjacent work, LIMA will define a standing safety gate for fake GuardianDecision fixtures and harnesses.

Rationale:

Fake GuardianDecision is the closest test artifact to production authorization. A harness helps validate fixture shape, but future work needs a consolidated gate to prevent fake decisions from becoming hidden authorization.

Consequences:

- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- audit persistence remains blocked
- fake GuardianDecision fixture harness remains test-only

## ADR-0079: Fake GuardianDecision Safety Gate Is the Standing Review Gate

Decision:

LIMA will use `docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md` as the standing safety gate for fake GuardianDecision-adjacent work.

Rationale:

Fake GuardianDecision is the closest current test artifact to production authorization. A consolidated gate prevents fake decisions from becoming hidden real decisions, approvals, enforcement, execution, or audit persistence.

Consequences:

- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- audit persistence remains blocked
- manual review is required for future real GuardianDecision work

## ADR-0080: Fake GuardianDecision Safety Gate Is Ready as Standing Gate

Decision:

`docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md` is ready to serve as the standing review gate for fake GuardianDecision-adjacent work.

Rationale:

The gate consolidates fake-vs-real decision rules, non-authorization rules, test-only status rules, fixture/harness rules, forbidden behaviors, PR blockers, manual review, and real GuardianDecision exit criteria.

Consequences:

- fake GuardianDecision safety-gate work may pause
- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- audit persistence remains blocked
- next work may move to Phase 2 final readiness review

## ADR-0081: Phase 3 Starts With Non-production Kernel Pipeline Design

Decision:

Phase 3 may begin only as non-production kernel pipeline design, not production integration.

Rationale:

Phase 2 established fixtures, harnesses, reports, and safety gates for the major kernel boundaries. The next safe step is designing an end-to-end non-production fixture pipeline while keeping real runtime behavior blocked.

Consequences:

- Phase 3.0 is design/review only
- production Sparkbot integration remains blocked
- real IntentCompiler remains blocked
- real GuardianDecision/enforcement remains blocked
- execution and audit persistence remain blocked
- safety gates remain required

## ADR-0082: Phase 3 Begins With Non-production Kernel Pipeline Design

Decision:

Phase 3 begins with design-only non-production kernel pipeline work, not production integration.

Rationale:

Phase 2 established fixtures, harnesses, reports, and safety gates for each boundary. The next safe step is designing how those boundaries compose without creating runtime behavior.

Consequences:

- Phase 3.0 is design/review only
- production integration remains blocked
- real IntentCompiler remains blocked
- real GuardianDecision remains blocked
- enforcement/approval/execution/audit persistence remain blocked
- standing gates remain mandatory

## ADR-0083: Kernel Pipeline Fixture Map Is Not Runtime

Decision:

LIMA may map fixture families across kernel pipeline stages, but the map is not an executable pipeline or runtime behavior.

Rationale:

Mapping fixture families helps prepare safe non-production composition without creating hidden runtime behavior.

Consequences:

- no data transformation yet
- no execution
- no audit persistence
- no production integration
- safety gates remain mandatory

## ADR-0084: Fixture Map Requires Readiness Review Before Relationship Metadata

Decision:

Before adding fixture relationship metadata, LIMA must review the non-production kernel pipeline fixture map.

Rationale:

Relationship metadata could be mistaken for runtime wiring unless the map is explicitly reviewed as non-executable.

Consequences:

- fixture relationship metadata remains metadata only
- no runtime pipeline
- no data transformation
- no production integration
- safety gates remain mandatory

## ADR-0085: Kernel Pipeline Relationship Metadata Is Not Runtime Wiring

Decision:

LIMA may add relationship metadata connecting fixture families across kernel pipeline stages, but this metadata must not be treated as runtime wiring or executable pipeline behavior.

Rationale:

Relationship metadata helps prepare safe non-production composition while preventing hidden runtime behavior.

Consequences:

- metadata is non-runtime
- no data transformation
- no execution
- no production integration
- safety gates remain mandatory

## ADR-0086: Relationship Metadata Requires Readiness Review Before Artifact Work

Decision:

Before future report/map artifact work or any later test-only composition harness, LIMA must review Phase 3.3 relationship metadata for clarity, safety, completeness, and non-runtime status.

Rationale:

Phase 3.3 has landed and is tagged as `phase-3.3-nonproduction-kernel-pipeline-relationship-metadata`. Relationship metadata can look like pipeline wiring if it is not explicitly reviewed. The readiness review preserves the boundary that scenario groups, stage references, and compatibility notes are descriptive fixture metadata only.

Consequences:

- Phase 3.4 is docs/tests/fixtures only
- relationship metadata remains non-runtime
- report/map artifact work may be considered after readiness review
- executable pipeline work remains blocked
- composition harness work remains blocked
- production Sparkbot integration remains blocked
- real IntentCompiler and real GuardianDecision remain blocked
- enforcement, approval, execution, and audit persistence remain blocked
- the next likely phase is Phase 3.5, LIMA Product Family and Adaptive Trust Doctrine
- product-family and adaptive-trust doctrine is deferred and not implemented in Phase 3.4

## ADR-0087: Product Family And Adaptive Trust Doctrine Is Non-runtime

Decision:

LIMA may document product-family, adaptive trust, breakglass evolution, and human-safety doctrine as non-runtime reference material before returning to pipeline report/map artifact work.

Rationale:

Phase 3.4 identified product-family and adaptive-trust doctrine as deferred strategic context. Capturing that context helps keep LIMA AI OS positioned as the trust-governed runtime underneath shells while preventing product doctrine from becoming hidden implementation.

Consequences:

- Phase 3.5 is docs/tests/fixtures only
- LIMA AI OS is documented as the governed runtime/kernel
- Sparkbot remains reference-only and is not imported or wired
- ARC Bot remains future commercial shell doctrine only
- custom business/private-sector bots remain future shell doctrine only
- Robo/automation consumers remain future driver-plane doctrine only
- adaptive trust gates remain doctrine only
- breakglass behavior is unchanged
- human-safety doctrine is non-runtime and non-executable
- runtime trust gate engine, approvals, enforcement, execution, audit persistence, robot control, and production wiring remain blocked

## ADR-0088: Kernel Pipeline Report Map Artifact Is Not Runtime Wiring

Decision:

LIMA may add a static non-runtime report/map artifact for the current non-production kernel pipeline fixture path, but the artifact must not be treated as a pipeline, execution order, compatibility proof, authorization, policy enforcement, approval, execution, audit persistence, or production wiring.

Rationale:

Phase 3.3 relationship metadata and Phase 3.4 readiness findings are useful review material, and Phase 3.5 doctrine gives product-family context. A static report/map artifact helps reviewers understand those sources before any future composition safety gate, while keeping runtime behavior blocked.

Consequences:

- Phase 3.6 is docs/tests/fixtures only
- no report generator is added
- no executable pipeline is added
- no test-only composition harness is added
- production Sparkbot integration remains blocked
- Sparkbot remains reference-only and is not imported or wired
- ARC Bot and custom bots remain doctrine/reference only
- Robo and automation consumers remain doctrine/reference only
- real IntentCompiler remains blocked
- real GuardianDecision remains blocked
- adaptive trust enforcement remains blocked
- approval, enforcement, execution, and audit persistence remain blocked
- next likely work is Phase 3.7 Pipeline Composition Safety Gate Docs

## ADR-0089: Pipeline Composition Safety Gate Must Precede Harness Work

Status: Accepted

Decision:

LIMA will add a non-runtime pipeline composition safety gate before any future test-only composition harness can be proposed.

Rationale:

Phase 3.6 made the current fixture path easier to review, but report/map artifacts can be mistaken for executable order or compatibility proof. A standing safety gate preserves the boundary that fixture families, stage maps, relationship metadata, readiness findings, and doctrine references remain descriptive until a later readiness review explicitly approves any test-only harness design.

Consequences:

- Phase 3.7 is docs/tests/fixtures only
- the safety gate is not a pipeline
- the safety gate is not a harness
- test-only composition harness work remains blocked
- runtime composition remains blocked
- production Sparkbot integration remains blocked
- Sparkbot remains reference-only and is not imported or wired
- real IntentCompiler remains blocked
- real GuardianDecision remains blocked
- approval, enforcement, execution, and audit persistence remain blocked
- LIMA AI Office, ARC Bot, custom bots, robots, drones, IoT, and physical-world action remain blocked
- next likely work is Phase 3.8 Pipeline Composition Safety Gate Readiness Review

## ADR-0090: Pipeline Composition Safety Gate Is Ready For Final Phase 3 Review

Status: Accepted

Decision:

The Phase 3.7 Pipeline Composition Safety Gate is clear enough to stand as the review gate for future pipeline-composition-adjacent work. Phase 3.8 may route the project to a final Phase 3 readiness review.

Rationale:

The safety gate clearly states that it is not a pipeline, not a harness, not authorization, not approval, not enforcement, not execution, not audit persistence, and not production wiring. It also keeps future harness work behind a separate explicit design review.

Consequences:

- Phase 3.8 is docs/tests/fixtures only
- test-only composition harness work remains unapproved
- Phase 3 final readiness review becomes the next safe step
- Phase 4 planning remains blocked until final Phase 3 readiness review lands
- production Sparkbot integration remains blocked
- product shells and physical-world control remain blocked
- approval, enforcement, execution, and audit persistence remain blocked

## ADR-0091: Phase 3 Completes As Non-runtime Kernel Pipeline Safety Work

Status: Accepted

Decision:

Phase 3 may close as non-runtime kernel pipeline safety work and route the project to Phase 4.0 Runtime Extraction Readiness Planning only.

Rationale:

Phase 3 mapped fixture families, reviewed relationship metadata, added product-family and adaptive-trust doctrine, created a static report/map artifact, established a pipeline composition safety gate, and reviewed that gate. This is enough to plan the next runtime-extraction readiness sequence, but not enough to move behavior.

Consequences:

- Phase 3.9 is docs/tests/fixtures only
- Phase 4.0 may begin as planning/review only
- no Phase 4 runtime implementation is approved
- test-only composition harness work remains separately gated
- production Sparkbot integration remains blocked
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- product shell implementation remains blocked
- robot, drone, IoT, and physical-world action remain blocked

## ADR-0092: Phase 4 Starts With Runtime Extraction Readiness Planning

Status: Accepted

Decision:

Phase 4 begins with runtime extraction readiness planning only. The first recommended boundary is a read-only Sparkbot Runtime Reference Refresh.

Rationale:

Phase 3 closed the non-production kernel pipeline safety work, but it did not prove runtime compatibility or authorize behavior movement. Before extracting anything, LIMA must refresh Sparkbot reference knowledge, choose a narrow boundary, and define the contract, fixture, test, and safety gates required for that boundary.

Consequences:

- Phase 4.0 is docs/tests/fixtures only
- no runtime behavior is moved
- Sparkbot remains the spec but is not imported or wired
- local Sparkbot inspection is deferred to Phase 4.1 and remains read-only
- Phase 4.1 becomes Sparkbot Runtime Reference Refresh
- real IntentCompiler and GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- product shells and physical-world control remain blocked

## ADR-0093: Sparkbot Reference Refresh Selects HumanInput Candidate Direction

Status: Accepted

Decision:

Phase 4.1 refreshes Sparkbot runtime reference knowledge as read-only planning material and recommends HumanInput intake for chat and voice as the first boundary candidate to evaluate in Phase 4.2.

Rationale:

Sparkbot shows text and voice paths converging into a tool-aware chat loop that also handles model routing, tool selection, Guardian policy, approvals, guarded execution, audit, verifier, and memory concerns. That loop is too coupled and too action-capable to extract first. A HumanInput intake boundary can preserve the text/voice reference shape while staying non-executing and forcing typed intent plus Guardian decision gates before consequential behavior.

Consequences:

- Phase 4.1 is docs/tests/fixtures only
- Sparkbot remains read-only reference/spec material
- no Sparkbot code is copied, imported, or wired
- Phase 4.2 should select and bound a non-executing HumanInput intake candidate
- tool-aware loop, tool dispatcher, terminal/PTY, robotics, approval execution, and product shells remain deferred
- runtime extraction implementation remains blocked
- approval, enforcement, execution, and audit persistence remain blocked
- physical-world control remains blocked

## ADR-0094: HumanInput Intake Is The First Phase 4 Boundary Candidate

Status: Accepted

Decision:

Phase 4.2 selects HumanInput intake for chat and voice as the first runtime boundary candidate to carry into Phase 4.3 Boundary Extraction Safety Gate.

Rationale:

HumanInput intake can preserve Sparkbot's text/voice convergence while staying non-executing. It is safer than extracting the model harness, tool-aware loop, tool dispatcher, terminal/PTY surface, robotics bridge, dashboard approval execution, or real Guardian enforcement because it can be bounded as source metadata, transcript metadata, actor/session references, privacy references, and downstream handoff requirements.

Consequences:

- Phase 4.2 is docs/tests/fixtures only
- selected candidate is for safety-gate review, not extraction implementation
- HumanInput intake cannot parse action, select tools, call models, approve, enforce policy, persist audit data, touch terminal/PTY, or touch robotics
- Phase 4.3 should define safety gates for this selected candidate
- Sparkbot remains read-only reference/spec material
- runtime extraction implementation remains blocked
- approval, enforcement, execution, and audit persistence remain blocked
- physical-world control remains blocked

## ADR-0095: HumanInput Intake Needs A Safety Gate Before Fixture Extension

Status: Accepted

Decision:

Phase 4.3 defines a Boundary Extraction Safety Gate for the selected HumanInput intake boundary. The gate permits only a future fixture/contract extension if explicitly approved; it does not approve adapters, runtime extraction, Sparkbot wiring, or behavior movement.

Rationale:

HumanInput intake is the safest first boundary candidate, but even input records can become unsafe if they perform live lookup, preserve raw private content, parse language into action, or create shortcuts around IntentEnvelope and GuardianDecision. The safety gate requires synthetic or redacted fixture material, reference-only identity/trust fields, no Sparkbot imports, and no execution-capable behavior.

Consequences:

- Phase 4.3 is docs/tests/fixtures only
- Phase 4.4 may proceed only as fixture/contract extension if explicitly approved
- HumanInput intake remains before IntentEnvelope and GuardianDecision
- live auth/session/trust lookup remains blocked
- runtime extraction implementation remains blocked
- approval, enforcement, execution, and audit persistence remain blocked
- physical-world control remains blocked

## ADR-0096: HumanInput Intake Fixtures Are Synthetic And Non-Authorizing

Status: Accepted

Decision:

Phase 4.4 extends synthetic HumanInput intake fixture/contract metadata for the selected chat and voice boundary. The fixtures are inert, reference-only, and cannot imply authorization, approval, execution, trust lookup, Sparkbot integration, or production runtime behavior.

Rationale:

HumanInput intake needs concrete text and voice fixture shapes before readiness can be reviewed, but the fixture shape must not become a hidden adapter or authority surface. The metadata therefore carries only synthetic content references, actor/session/trust references, privacy classes, lineage seeds, and handoff requirements toward future IntentEnvelope and GuardianDecision boundaries.

Consequences:

- Phase 4.4 is docs/tests/fixtures only
- no files under `lima/` are modified
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- fixture records are synthetic and non-runtime
- HumanInput intake cannot parse, approve, enforce, execute, persist audit data, or perform live lookup
- Phase 4.5 may review boundary readiness
- runtime extraction implementation remains blocked
- physical-world control remains blocked

## ADR-0097: HumanInput Intake Boundary Is Conditionally Ready For An Explicit Future Proposal

Status: Accepted

Decision:

Phase 4.5 reviews the selected HumanInput intake boundary and finds it conditionally ready only for a future explicitly approved narrow non-production proposal. It does not approve runtime extraction implementation, Sparkbot integration, live adapter code, or behavior movement.

Rationale:

Phase 4.1 through Phase 4.4 established the reference basis, selected the HumanInput intake boundary, defined the safety gate, and added hardened synthetic text and voice fixture metadata. That is enough to support a future proposal discussion, but not enough to move behavior into runtime code.

Consequences:

- Phase 4.5 is docs/tests/fixtures only
- HumanInput intake remains non-authorizing input
- IntentEnvelope remains the next semantic boundary
- GuardianDecision remains required before consequential behavior
- any next narrow non-production extraction or adapter proposal requires explicit operator approval
- runtime extraction implementation remains blocked
- approval, enforcement, execution, and audit persistence remain blocked
- physical-world control remains blocked

## ADR-0098: HumanInput Adapter Proposal Is Not A HumanInput Adapter

Status: Accepted

Decision:

Phase 4.6 may add a non-production HumanInput adapter proposal as docs/tests/fixtures only. The proposal may describe how a future shell intake adapter could convert selected shell input context into the Phase 4.4 HumanInput fixture/contract shape, but it is not a HumanInput adapter and does not approve live adapter code.

Rationale:

Phase 4.5 found the HumanInput intake boundary conditionally ready for an explicitly approved narrow non-production proposal. A proposal gives the project a reviewable shape for future adapter design while keeping HumanInput as non-authorizing input before IntentEnvelope and GuardianDecision.

Consequences:

- Phase 4.6 is docs/tests/fixtures only
- no files under `lima/` are modified
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- no live auth/session/trust lookup is added
- the proposal cannot authorize, approve, enforce, execute, persist audit data, or perform physical-world action
- real IntentCompiler and real GuardianDecision remain blocked
- any next narrow non-production phase requires explicit operator approval

## ADR-0099: HumanInput Adapter Proposal Readiness Review Allows Safety Gate Docs Only

Status: Accepted

Decision:

Phase 4.7 may review the Phase 4.6 HumanInput adapter proposal as docs/tests/fixtures only and may recommend HumanInput Adapter Safety Gate Docs as the next non-runtime step. The readiness review is not a HumanInput adapter and does not approve live adapter code.

Rationale:

Phase 4.6 created a proposal shape, but a safety gate should exist before any future adapter implementation can be discussed. The readiness review confirms that source references, passive trust/autonomy metadata, transcript confidence, privacy fields, lineage seeds, and IntentEnvelope/GuardianDecision handoffs remain descriptive and non-executable.

Consequences:

- Phase 4.7 is docs/tests/fixtures only
- no files under `lima/` are modified
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- no live auth/session/trust lookup is added
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 4.8 may proceed only as HumanInput Adapter Safety Gate Docs

## ADR-0100: HumanInput Adapter Safety Gate Requires HumanInput-only Output

Status: Accepted

Decision:

Phase 4.8 establishes the HumanInput Adapter Safety Gate as docs/tests/fixtures only. Any future HumanInput adapter must return HumanInput only and must stop before IntentEnvelope, GuardianDecision, model/tool/terminal/robot behavior, approval, enforcement, execution, and audit persistence.

Rationale:

The HumanInput boundary is the first safe intake boundary, but adapter work can easily become runtime wiring if it performs live lookup, imports Sparkbot, creates semantic intent, or reaches toward action. A standing safety gate keeps future adapter work narrow and reviewable before any code phase is approved.

Consequences:

- Phase 4.8 is docs/tests/fixtures only
- no files under `lima/` are modified
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- no live auth/session/trust lookup is added
- adapter output must remain HumanInput only
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- any next narrow non-production phase requires explicit operator approval

## ADR-0101: HumanInput Adapter Implementation Readiness Is Test-only Harness Proposal Readiness Only

Status: Accepted

Decision:

Phase 4.9 may review whether the HumanInput adapter boundary is ready for a future explicitly approved test-only adapter harness proposal. It does not approve adapter implementation, live adapter code, test-only harness code, runtime wiring, Sparkbot integration, or behavior movement.

Rationale:

Phase 4.4 through Phase 4.8 created the fixture contract, readiness reviews, proposal, and safety gate needed to discuss a narrow test-only harness proposal. That readiness is not the same as runtime implementation readiness. The project still needs explicit approval before any harness code or adapter code exists.

Consequences:

- Phase 4.9 is docs/tests/fixtures only
- no files under `lima/` are modified
- no live adapter code is added
- no test-only adapter harness code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- no live auth/session/trust lookup is added
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- any next narrow non-production phase requires explicit operator approval

## ADR-0102: Test-only HumanInput Adapter Harness Proposal Is Not Harness Code

Status: Accepted

Decision:

Phase 4.10 may propose a future test-only HumanInput adapter harness as docs/tests/fixtures only. It does not approve harness code, live adapter code, runtime wiring, Sparkbot integration, or behavior movement.

Rationale:

Phase 4.9 found the HumanInput boundary ready to discuss a future test-only harness proposal. The proposal must describe purpose, synthetic inputs, expected HumanInput fixture shape, safety boundaries, and validation requirements before any code exists.

Consequences:

- Phase 4.10 is docs/tests/fixtures only
- no files under `lima/` are modified
- no harness code is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked

## ADR-0103: Test-only Harness Proposal Readiness Allows Safety Gate Docs Only

Status: Accepted

Decision:

Phase 4.11 may review the Phase 4.10 test-only HumanInput adapter harness proposal as docs/tests/fixtures only. It may recommend safety gate documentation, but it does not approve harness code, adapter code, Sparkbot integration, or runtime behavior.

Rationale:

The proposal is clear enough to gate, but a standing safety gate must exist before any future harness implementation can be considered. The readiness review keeps the next step documentation-only.

Consequences:

- Phase 4.11 is docs/tests/fixtures only
- no files under `lima/` are modified
- no harness code is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- approval, enforcement, execution, and audit persistence remain blocked

## ADR-0104: Test-only Harness Safety Gate Does Not Prove Production Readiness

Status: Accepted

Decision:

Phase 4.12 may define the Test-only HumanInput Adapter Harness Safety Gate as docs/tests/fixtures only. The gate states that a future test-only harness is not runtime, not Sparkbot integration, cannot call models/tools/terminal/robots, cannot approve/enforce/execute/audit, cannot perform live lookup, and cannot imply production adapter readiness.

Rationale:

Even a test-only harness can be mistaken for adapter implementation readiness. A dedicated safety gate preserves the distinction between static fixture validation and runtime adapter safety.

Consequences:

- Phase 4.12 is docs/tests/fixtures only
- no files under `lima/` are modified
- no harness implementation is added
- no live adapter implementation is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 4.13 may summarize HumanInput boundary readiness as a final non-runtime review

## ADR-0105: Phase 4 HumanInput Boundary Readiness Is Not Runtime Readiness

Status: Accepted

Decision:

Phase 4.13 may review the full HumanInput boundary lane as docs/tests/fixtures only. It may conclude readiness only for a future explicitly approved test-only HumanInput adapter harness implementation phase or further non-runtime review.

Rationale:

The Phase 4.4 through Phase 4.12 lane now has synthetic HumanInput fixture metadata, adapter proposal docs, adapter safety gate docs, test-only harness proposal docs, and test-only harness safety gate docs. A final readiness review can summarize those artifacts without implementing any harness, adapter, or runtime behavior.

Consequences:

- Phase 4.13 is docs/tests/fixtures only
- no files under `lima/` are modified
- no harness implementation is added
- no live adapter implementation is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- physical-world action remains blocked

## ADR-0106: Test-only HumanInput Harness Stays Under Tests

Status: Accepted

Decision:

Phase 4.14 may implement a deterministic test-only HumanInput adapter harness under `tests/`. The harness may validate synthetic fixture records and produce HumanInput-shaped test dictionaries only.

Rationale:

Phase 4.13 found the HumanInput boundary lane ready for a future explicitly approved test-only harness implementation. The first implementation must prove fixture shape validation without moving code into `lima/`, importing Sparkbot, creating runtime adapter behavior, or producing downstream authority artifacts.

Consequences:

- Phase 4.14 test-only helper code stays under `tests/`
- no files under `lima/` are modified
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- no IntentEnvelope or GuardianDecision is produced
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 4.15 should review whether the harness stayed deterministic, synthetic-only, and non-runtime

## ADR-0107: Test-only HumanInput Harness Readiness Allows Closeout Review Only

Status: Accepted

Decision:

Phase 4.15 may review the Phase 4.14 harness as docs/tests/fixtures only. It may recommend Phase 4.16 HumanInput boundary lane closeout review, but it does not approve live adapter code, runtime wiring, Sparkbot integration, or any authority/execution behavior.

Rationale:

The Phase 4.14 harness stayed under `tests/`, converted only synthetic fixtures to HumanInput-shaped dictionaries, and rejected runtime/prod markers. A readiness review confirms the constraint before closing the HumanInput boundary lane.

Consequences:

- Phase 4.15 is docs/tests/fixtures only
- no files under `lima/` are modified
- no new harness behavior is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 4.16 may close out the HumanInput boundary lane

## ADR-0108: HumanInput Boundary Lane Closeout Stops Phase 4 HumanInput Work

Status: Accepted

Decision:

Phase 4.16 may close out the HumanInput boundary lane as docs/tests/fixtures only. It may recommend a future explicitly approved HumanInput to IntentEnvelope boundary planning lane, but it does not approve next-lane implementation or runtime behavior.

Rationale:

The HumanInput lane now has boundary selection, fixture contracts, safety gates, proposal reviews, test-only harness implementation, and readiness review. The safest next move is to stop this lane and require explicit approval before planning the HumanInput to IntentEnvelope boundary.

Consequences:

- Phase 4.16 is docs/tests/fixtures only
- no files under `lima/` are modified
- no new harness behavior is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- no runtime behavior is added
- HumanInput to IntentEnvelope implementation remains blocked
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- next lane requires explicit operator approval

## ADR-0109: HumanInput to IntentEnvelope Lane Starts With Planning

Status: Accepted

Decision:

Phase 4.17 may open HumanInput to IntentEnvelope boundary planning as docs/tests/fixtures only. It may recommend a later schema/contract proposal, but it does not approve schema implementation, bridge code, real IntentCompiler behavior, or runtime behavior.

Rationale:

Phase 4.16 closed the HumanInput lane and recommended HumanInput to IntentEnvelope planning. Existing IntentEnvelope safety gates require explicit typed metadata, inert raw text, and no hidden parser before any test-only bridge or compiler-adjacent work.

Consequences:

- Phase 4.17 is docs/tests/fixtures only
- no files under `lima/` are modified
- no bridge code is added
- no schema implementation is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 4.18 may propose a boundary schema/contract as metadata only

## ADR-0110: HumanInput to IntentEnvelope Schema Proposal Is Not A Bridge

Status: Accepted

Decision:

Phase 4.18 may propose a static HumanInput to IntentEnvelope boundary schema/contract as docs/tests/fixtures only. It may list HumanInput references, explicit typed intent metadata, and safety markers, but it does not create IntentEnvelope records or implement bridge code.

Rationale:

The IntentEnvelope safety gate requires explicit typed metadata and inert raw text before any test-only bridge discussion. A schema proposal gives the next readiness review a stable, reviewable target without introducing compiler behavior.

Consequences:

- Phase 4.18 is docs/tests/fixtures only
- no files under `lima/` are modified
- no bridge code is added
- no IntentEnvelope record is created
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 4.19 may review readiness of the proposal

## ADR-0111: HumanInput to IntentEnvelope Readiness Review Is Not Implementation Readiness

Status: Accepted

Decision:

Phase 4.19 may review the Phase 4.18 HumanInput to IntentEnvelope schema/contract proposal as docs/tests/fixtures only. It may decide whether the proposal is clear enough for a Phase 5 gate / implementation readiness closeout, but it does not approve bridge code, test-only bridge code, real IntentCompiler behavior, real GuardianDecision behavior, or runtime wiring.

Rationale:

The schema proposal is useful only if the project explicitly preserves the standing IntentEnvelope safety gate. A readiness review creates a final non-runtime check before any Phase 5 gate discussion and prevents a metadata proposal from becoming hidden implementation approval.

Consequences:

- Phase 4.19 is docs/tests/fixtures only
- no files under `lima/` are modified
- no bridge code or test-only bridge code is added
- no IntentEnvelope record is created
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 4.20 may close the Phase 4 lane at a Phase 5 gate

## ADR-0112: Phase 4.20 Must Stop At Phase 5 Gate

Status: Accepted

Decision:

Phase 4.20 may close the HumanInput to IntentEnvelope non-runtime planning lane at a Phase 5 gate as docs/tests/fixtures only. It must identify operator decisions needed before Phase 5 and must not approve runtime behavior, test-only bridge code, real IntentCompiler behavior, real GuardianDecision behavior, or production integration.

Rationale:

The HumanInput lane and the HumanInput to IntentEnvelope planning lane now have enough static contracts and reviews to expose the next real decision point. Moving past that point requires product and safety decisions about human flow, approval semantics, trust behavior, and whether Phase 5 starts as planning or implementation.

Consequences:

- Phase 4.20 is docs/tests/fixtures only
- no files under `lima/` are modified
- no bridge code or test-only bridge code is added
- no runtime behavior is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5 requires explicit operator approval

## ADR-0113: Phase 5 Gate Is Reached

Status: Accepted

Decision:

Phase 4.20 confirms the Phase 5 gate is reached. Phase 5 is not pre-approved and requires an explicit operator scope decision before further work.

Rationale:

The HumanInput boundary lane and HumanInput to IntentEnvelope planning lane are complete enough to expose the next real product and safety decisions. Continuing without a scope decision would risk turning non-runtime planning into implementation by momentum.

Consequences:

- stop at Phase 5 gate
- Phase 5 scope must be explicitly approved
- human UX flow must be decided before implementation
- approval semantics must be decided before implementation
- trust/autonomy handling must be decided before implementation
- runtime behavior remains blocked
- test-only bridge code remains blocked until explicitly approved
- files under `lima/` remain blocked unless explicitly approved

## ADR-0114: Phase 5 Starts As Non-runtime Planning

Status: Accepted

Decision:

Phase 5.0 opens Phase 5 as non-runtime planning only. HumanInput is treated as an operator-originated request envelope, not an execution command. The lane may plan and propose HumanInput to IntentEnvelope boundaries, but it does not approve implementation, bridge code, runtime wiring, or live behavior.

Rationale:

The Phase 4.20 gate identified the correct next work: planning the HumanInput to IntentEnvelope boundary while preserving Guardian-first execution discipline. Operator intent is important context, but it cannot bypass classification, approval semantics, or GuardianDecision boundaries.

Consequences:

- Phase 5.0 is docs/tests/fixtures only
- no files under `lima/` are modified
- no bridge code or test-only bridge code is added
- no runtime behavior is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- HumanInput is not execution permission
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.1 may propose a contract, not implement it

## ADR-0115: HumanInput To IntentEnvelope Contract Proposal Is Metadata Only

Status: Accepted

Decision:

Phase 5.1 may propose the HumanInput to IntentEnvelope contract as static metadata only. The contract may define source, operator intent, requested action, risk tier, approval state, candidate state, and not-executable-yet markers, but it does not create IntentEnvelope records or implement bridge code.

Rationale:

The Phase 5 charter makes operator intent high-priority context without making it permission. A contract proposal lets reviewers inspect the required fields before any test-only bridge harness proposal.

Consequences:

- Phase 5.1 is docs/tests/fixtures only
- no files under `lima/` are modified
- no bridge code or test-only bridge code is added
- no runtime behavior is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.2 may propose a test-only bridge harness, not implement it

## ADR-0116: Test-only Bridge Harness Must Start As Proposal

Status: Accepted

Decision:

Phase 5.2 may propose a future test-only HumanInput to IntentEnvelope bridge harness as docs/tests/fixtures only. It must not implement harness code or create IntentEnvelope records.

Rationale:

Even test-only bridge code can create implementation momentum. A proposal phase lets the repo verify boundaries, inputs, outputs, failure modes, and blocked interpretations before any helper code is considered.

Consequences:

- Phase 5.2 is docs/tests/fixtures only
- no files under `lima/` are modified
- no bridge implementation or test-only bridge code is added
- no runtime behavior is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.3 may review readiness before any implementation gate

## ADR-0117: Bridge Harness Readiness Review Must Stop At Implementation Gate

Status: Accepted

Decision:

Phase 5.3 may review the Phase 5.2 proposal as docs/tests/fixtures only. If the proposal is ready, Phase 5.3 must stop at an implementation gate before any test-only bridge harness code.

Rationale:

The next step after a safe proposal is an implementation decision. That decision must be explicit because even test-only bridge code begins shaping behavior around HumanInput and IntentEnvelope candidates.

Consequences:

- Phase 5.3 is docs/tests/fixtures only
- no files under `lima/` are modified
- no bridge implementation or test-only bridge code is added
- no runtime behavior is added
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- any Phase 5.4 implementation scope requires explicit operator approval

## ADR-0118: Test-only Bridge Harness Implementation Stays Under Tests

Status: Accepted

Decision:

Phase 5.4 may implement a deterministic HumanInput to IntentEnvelope bridge helper only under `tests/support/`. The helper may convert synthetic HumanInput-shaped dictionaries into non-executable IntentEnvelope-candidate-shaped test dictionaries.

Rationale:

The operator approved a narrow test-only implementation scope after Phase 5.3. Keeping the helper under `tests/support/` lets LIMA validate boundary shape, conservative risk classification, provenance preservation, and fail-closed behavior without creating a runtime bridge.

Consequences:

- Phase 5.4 may add test-only helper code under `tests/support/`
- no files under `lima/` are modified
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- output candidates are non-executable test dictionaries only
- operator/admin/Phil/trusted wording does not bypass approval
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.5 or later requires explicit operator approval

## ADR-0119: Test-only Bridge Harness Readiness Review Blocks Runtime Reuse

Status: Accepted

Decision:

Phase 5.5 may review the Phase 5.4 helper as docs/tests/fixtures only. It must not change helper behavior. The Phase 5.4 helper's keyword risk classifier is test metadata only and must not be reused as runtime classifier logic.

Rationale:

The helper is useful for checking candidate shape and fail-closed behavior, but it is not an IntentCompiler and not a runtime bridge. A readiness review prevents test-only semantics from quietly becoming live runtime semantics.

Consequences:

- Phase 5.5 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- no live adapter code is added
- no Sparkbot code is copied, imported, or wired
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.6 or later requires explicit operator approval

## ADR-0120: Runtime Bridge Work Requires Safety Gate and Design First

Status: Accepted

Decision:

Phase 5.6 records that the Phase 5.4 helper remains test-only and that any future live/runtime HumanInput to IntentEnvelope bridge requires separate explicit Phil approval. Future runtime bridge work must begin with a runtime design proposal before implementation.

Rationale:

The test-only helper and readiness review are useful boundary scaffolding, but they are not sufficient to approve runtime behavior. A safety gate prevents test classifier semantics, operator wording, or candidate metadata from becoming execution permission.

Consequences:

- Phase 5.6 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime HumanInput to IntentEnvelope behavior remains blocked
- HumanInput remains intent context, not execution permission
- operator/admin/Phil/trusted wording cannot bypass approval
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.7 or later requires explicit operator approval

## ADR-0121: Runtime Bridge Design Proposal Remains Non-runtime

Status: Accepted

Decision:

Phase 5.7 documents the proposed shape of a future HumanInput to IntentEnvelope runtime bridge while keeping all implementation blocked. It defines allowed inputs, rejected inputs, provenance requirements, non-executable candidate requirements, approval-required semantics, risk-tier semantics, trust/autonomy rules, and blocked behavior.

Rationale:

The project needs a runtime bridge design before any implementation can be evaluated, but design language must not become implicit approval to wire runtime behavior.

Consequences:

- Phase 5.7 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime HumanInput to IntentEnvelope behavior remains blocked
- operator/admin/Phil/trusted wording cannot bypass approval
- real IntentCompiler and real GuardianDecision remain blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.8 may continue only as docs/tests/fixtures-only threat modeling

## ADR-0122: Runtime Bridge Threat Model Precedes Validation Matrix

Status: Accepted

Decision:

Phase 5.8 records a threat model for a future HumanInput to IntentEnvelope runtime bridge before any boundary validation matrix or implementation gate. It covers prompt injection, operator impersonation, trust bypass, accidental execution, side-effect escalation, audit gaps, approval confusion, helper classifier misuse, unsafe test-code reuse, malformed input, replayed input, and ambiguous commands.

Rationale:

The future bridge would sit near sensitive operator intent and eventual Guardian review. Threat modeling must preserve the distinction between candidate metadata and executable runtime behavior.

Consequences:

- Phase 5.8 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime HumanInput to IntentEnvelope behavior remains blocked
- future runtime work requires fresh design, semantic tests, and Guardian gate review
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.9 may continue only as docs/tests/fixtures-only boundary validation matrix work

## ADR-0123: Boundary Validation Matrix Keeps Candidate Outputs Non-executable

Status: Accepted

Decision:

Phase 5.9 records a validation matrix for a future HumanInput to IntentEnvelope runtime bridge design. Every matrix category remains non-executable, side-effecting categories require approval or are blocked, and empty, malformed, replayed, or stale requests are rejected or blocked.

Rationale:

A future bridge needs clear category expectations before implementation. Matrix rows make the boundary easier to audit without turning the matrix into a runtime classifier.

Consequences:

- Phase 5.9 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime HumanInput to IntentEnvelope behavior remains blocked
- the matrix is not a runtime schema or classifier implementation
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 5.10 may continue only as docs/tests/fixtures-only implementation gate / closeout review

## ADR-0124: Runtime Bridge Design Lane Stops at Implementation Gate

Status: Accepted

Decision:

Phase 5.10 closes the HumanInput runtime bridge design lane at an implementation gate. The lane designed the safety gate, future bridge shape, threat model, and validation matrix, but it does not approve live/runtime implementation.

Rationale:

The repository now has enough non-runtime design metadata to support an explicit operator decision. Proceeding further without a new scope would risk turning planning artifacts into implicit implementation approval.

Consequences:

- Phase 5.10 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime HumanInput to IntentEnvelope behavior remains blocked
- future runtime implementation requires separate explicit Phil approval
- future runtime implementation must define production boundaries, Guardian handoff, provenance validation, replay/staleness handling, malformed-input rejection, approval semantics, audit design, and semantic tests
- approval, enforcement, execution, and audit persistence remain blocked

## ADR-0125: Phase 5 HumanInput Bridge Design Lane Archived

Status: Accepted

Decision:

Phase 5.11 archives Phase 5.0 through Phase 5.10 as the completed HumanInput to IntentEnvelope design lane. Phase 5.7 through Phase 5.10 are archived as planning/specification only, and future runtime work requires new explicit Phil approval.

Rationale:

The design lane has reached a clean decision point. Archiving the lane prevents design metadata, fixtures, static tests, or the Phase 5.4 test-only helper from being mistaken for runtime approval.

Consequences:

- Phase 5.11 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime HumanInput to IntentEnvelope behavior remains blocked
- the Phase 5.4 helper remains test-only
- helper classifier runtime reuse remains unapproved
- approval, enforcement, execution, and audit persistence remain blocked
- the next step requires explicit operator scope selection

## ADR-0126: Phase 6 Starts With Kernel Lifecycle Planning

Status: Accepted

Decision:

Phase 6.0 reorients the roadmap after Phase 5 and selects broader LIMA Kernel lifecycle planning as the safest next architectural lane. Runtime bridge work remains blocked until kernel, IntentEnvelope, GuardianDecision, approval, audit/spine/memory, Sparkbot, and physical-world boundaries are clearer.

Rationale:

The Phase 5 HumanInput bridge design lane produced useful planning artifacts, but runtime bridge implementation still depends on broader kernel lifecycle decisions.

Consequences:

- Phase 6.0 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime bridge implementation remains blocked
- Phase 6.1 may continue only as docs/tests/fixtures-only LIMA Kernel Lifecycle Planning

## ADR-0127: Kernel Lifecycle Planning Precedes Runtime Boundaries

Status: Accepted

Decision:

Phase 6.1 records a planning-only LIMA Kernel lifecycle. The lifecycle runs from shell intake to boundary normalization, IntentEnvelope candidate formation, Guardian review, GuardianDecision record, spine/audit/memory handoff, and blocked driver handoff.

Rationale:

Runtime bridge work should not proceed until the kernel lifecycle is explicit enough to place future runtime behavior behind Guardian and persistence boundaries.

Consequences:

- Phase 6.1 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime behavior remains blocked
- Phase 6.2 may continue only as docs/tests/fixtures-only IntentEnvelope and GuardianDecision lifecycle boundary mapping

## ADR-0128: IntentEnvelope Candidates Are Not Guardian Decisions

Status: Accepted

Decision:

Phase 6.2 maps IntentEnvelope candidate and GuardianDecision lifecycle boundaries as planning metadata only. IntentEnvelope candidates may carry provenance, risk, confidence, approval-state, and review-readiness metadata, but they are not commands, authorization, approval, execution, audit persistence, or driver readiness. GuardianDecision remains the future authority boundary and is not implemented in this phase.

Rationale:

The kernel needs a clear boundary between intent candidate metadata and approval authority before any future runtime bridge or compiler path can be considered.

Consequences:

- Phase 6.2 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime behavior remains blocked
- real IntentCompiler behavior remains blocked
- real GuardianDecision behavior remains blocked
- approval, enforcement, execution, and audit persistence remain blocked
- Phase 6.3 may continue only as docs/tests/fixtures-only approval, audit, and memory boundary planning

## ADR-0129: Approval, Audit, And Memory References Are Planning Boundaries

Status: Accepted

Decision:

Phase 6.3 plans approval, audit/spine, and memory boundaries as metadata only. Approval states remain descriptive, audit/spine fields remain lineage planning, and memory fields remain reference-only. None of these references enforce approval, authorize execution, persist audit, append a ledger, read memory, or write memory.

Rationale:

Future runtime bridge work needs approval, evidence, retention, redaction, audit, and memory boundaries before any live behavior can be considered. Planning those boundaries now prevents future candidate metadata from being mistaken for authority or persistence.

Consequences:

- Phase 6.3 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- approval enforcement remains blocked
- audit persistence remains blocked
- memory IO remains blocked
- spine ledger writes remain blocked
- execution and physical-world action remain blocked
- Phase 6.4 may continue only as docs/tests/fixtures-only roadmap gate / next-lane closeout

## ADR-0130: Phase 6 Planning Lane Closes At A Roadmap Gate

Status: Accepted

Decision:

Phase 6.4 closes the broader LIMA OS roadmap planning lane as docs/tests/fixtures-only work. It records Phase 6.0 through Phase 6.3 as complete planning, summarizes what remains unimplemented, and requires explicit Phil next-scope selection before any Phase 6.5, Phase 7, runtime bridge, Sparkbot integration, Robo-OS integration, approval/enforcement/execution/audit, memory IO, or physical-world work.

Rationale:

The lane has clarified enough kernel, candidate, GuardianDecision, approval, audit/spine, memory, shell, and physical-world boundaries to stop cleanly without drifting into implementation.

Consequences:

- Phase 6.4 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- live/runtime bridge implementation remains blocked
- Sparkbot wiring remains blocked
- Robo-OS and physical-world behavior remain blocked
- approval, enforcement, execution, audit persistence, memory IO, and spine ledger writes remain blocked
- the next step requires explicit operator scope selection

## ADR-0131: Phase 6 Is Archived As Planning Only

Status: Accepted

Decision:

Phase 6.5 archives Phase 6.0 through Phase 6.4 as completed roadmap/planning work. The lane added docs, fixtures, static tests, and roadmap/state updates only. It did not add runtime behavior, `lima/` changes, `tests/support/` changes, Sparkbot wiring, live adapters, execution, approval enforcement, audit persistence, or physical-world behavior.

Rationale:

Archiving the lane creates a clean decision point before any future Phase 7, Sparkbot integration boundary planning, Robo-OS / physical-world boundary planning, or product roadmap lane.

Consequences:

- Phase 6.5 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- Phase 5 runtime bridge remains gated
- Phase 6 is archived as planning only
- future runtime work requires new explicit Phil approval
- the next step requires explicit operator scope selection

## ADR-0132: Phase 7 Starts As A No-Code Runtime Charter

Status: Accepted

Decision:

Phase 7.0 opens Phase 7 as a no-code kernel runtime implementation charter lane. The smallest future runtime slice that may be considered later is a non-executing kernel intake-to-candidate coordinator that accepts only typed explicit inputs and produces non-executable candidate metadata for Guardian review. Phase 7.0 does not approve implementation.

Rationale:

The repo needs a precise runtime charter before any `lima/` code can be touched. A no-code charter prevents planning language from turning into accidental runtime behavior.

Consequences:

- Phase 7.0 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- Phase 5 runtime bridge remains gated
- future runtime implementation still requires explicit Phil approval
- Phase 7.1 may continue only as docs/tests/fixtures-only first runtime slice eligibility mapping

## ADR-0133: Runtime File Eligibility Is Not Modification Approval

Status: Accepted

Decision:

Phase 7.1 maps future eligible files for the first possible runtime slice, but eligibility is not approval to modify files now. Future eligible files are limited to selected contract files and optional new kernel files if explicitly approved. Execution surfaces, adapters, IO, persistence, services, shells, spine, Guardian implementation paths, and `tests/support/**` remain forbidden for the first slice.

Rationale:

The repo needs a concrete file boundary before any runtime implementation decision. Naming eligible and forbidden files reduces ambiguity without touching runtime code.

Consequences:

- Phase 7.1 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- eligibility does not approve runtime implementation
- Phase 7.2 may continue only as docs/tests/fixtures-only kernel runtime safety preconditions

## ADR-0134: Runtime Preconditions Must Exist Before Runtime Code

Status: Accepted

Decision:

Phase 7.2 defines required tests, rollback expectations, audit proof requirements, input/output shape constraints, and safety gates before any future runtime implementation can be approved. These preconditions remain planning metadata only and do not approve code.

Rationale:

The first runtime slice must be reversible, tested, non-executing, and bounded before any `lima/` file is changed.

Consequences:

- Phase 7.2 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- future candidate output must remain non-executable
- approval enforcement, execution, audit persistence, and physical-world behavior remain blocked
- Phase 7.3 may continue only as docs/tests/fixtures-only runtime implementation test planning

## ADR-0135: Runtime Implementation Requires A Test Plan First

Status: Accepted

Decision:

Phase 7.3 defines the future runtime implementation test plan before any runtime implementation can be approved. The plan requires import-boundary, typed-input, fail-closed, natural-language rejection, non-executable output, approval-bypass rejection, GuardianDecision non-creation, Sparkbot coupling rejection, side-effect rejection, and rollback review tests.

Rationale:

The first runtime slice must have its proof obligations defined before implementation. Tests come before code.

Consequences:

- Phase 7.3 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- runtime implementation remains blocked
- Phase 7.4 may continue only as docs/tests/fixtures-only implementation decision gate / closeout

## ADR-0136: Phase 7 Stops At An Implementation Decision Gate

Status: Accepted

Decision:

Phase 7.4 closes the no-code kernel runtime implementation charter lane at an implementation decision gate. Phase 7 defined a possible future non-executing kernel intake-to-candidate coordinator, file eligibility, safety preconditions, and test-plan obligations, but did not approve runtime implementation.

Rationale:

The repo has enough no-code planning to ask for a deliberate implementation decision without drifting into `lima/` changes.

Consequences:

- Phase 7.4 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- Phase 5 runtime bridge remains gated
- future runtime work requires explicit Phil approval
- the next step requires explicit operator implementation decision

## ADR-0137: Phase 7 Is Archived As No-Code Charter Only

Status: Accepted

Decision:

Phase 7.5 archives Phase 7.0 through Phase 7.4 as a completed no-code kernel runtime implementation charter lane. The archive records that Phase 7 added docs, fixtures, static tests, and roadmap/state updates only.

Rationale:

Phase 7 has enough no-code charter, eligibility, safety-precondition, test-plan, and decision-gate material to preserve the lane before any Phase 8 design review or runtime slice decision.

Consequences:

- Phase 7.5 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- no runtime implementation is approved
- Phase 5 runtime bridge remains gated
- future runtime code requires explicit Phil approval
- the next step requires explicit operator next-scope decision

## ADR-0138: Phase 8 Starts As No-Code Implementation Design Review

Status: Accepted

Decision:

Phase 8.0 opens Phase 8 as a no-code implementation design review lane. The lane may convert the Phase 7 charter into a future implementation design package, but it may not implement runtime behavior or modify runtime files.

Rationale:

The repo needs an exact design package before any narrow runtime slice can be responsibly approved.

Consequences:

- Phase 8.0 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- Phase 5 runtime bridge remains gated
- the narrowest future runtime slice remains non-executing candidate metadata only
- Phase 8.1 may continue only as docs/tests/fixtures-only exact file-touch mapping

## ADR-0139: Runtime File-Touch Eligibility Is Exact And Future-Only

Status: Accepted

Decision:

Phase 8.1 defines the exact future file-touch map for a possible first runtime slice. Eligible files are future-only and may not be modified unless Phil explicitly approves runtime implementation later.

Rationale:

An exact file-touch map prevents a future narrow runtime slice from drifting into adapters, IO, persistence, services, shells, spine, Sparkbot wiring, or `tests/support/`.

Consequences:

- Phase 8.1 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- future implementation must stay inside the named eligible file set
- any need to touch a forbidden surface stops the work for Phil approval
- Phase 8.2 may continue only as docs/tests/fixtures-only acceptance test design

## ADR-0140: Runtime Acceptance Tests Must Be Designed Before Code

Status: Accepted

Decision:

Phase 8.2 defines future runtime acceptance test obligations before any runtime implementation can be approved. These obligations include import-boundary tests, typed-input tests, malformed-input rejection, non-executable output, authority-free output, approval-bypass rejection, GuardianDecision and IntentEnvelope non-creation, Sparkbot coupling rejection, and side-effect rejection.

Rationale:

The first runtime slice must be test-constrained before any code is written, otherwise a small coordinator could accidentally become a compiler, bridge, adapter, approval engine, or execution path.

Consequences:

- Phase 8.2 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- future positive tests are limited to non-executable candidate metadata
- runtime implementation remains blocked
- Phase 8.3 may continue only as docs/tests/fixtures-only rollback / audit proof planning

## ADR-0141: Runtime Rollback And Audit Proof Must Be Planned Before Code

Status: Accepted

Decision:

Phase 8.3 defines rollback and audit proof requirements before any future runtime implementation can be approved. Audit proof remains test evidence only until audit persistence is separately approved.

Rationale:

The first runtime slice must be independently revertible and prove non-executable candidate behavior without creating persistence or authority.

Consequences:

- Phase 8.3 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- future runtime code must be independently revertible
- future audit proof cannot imply audit persistence
- Phase 8.4 may continue only as docs/tests/fixtures-only runtime implementation approval gate / closeout

## ADR-0142: Phase 8 Stops At Runtime Implementation Approval Gate

Status: Accepted

Decision:

Phase 8.4 closes the no-code implementation design review lane at an explicit runtime implementation approval gate. Runtime code remains blocked unless Phil later approves the exact narrow Phase 9 implementation question.

Rationale:

Phase 8 has defined the design package, file-touch map, acceptance tests, rollback expectations, audit proof requirements, success criteria, and failure criteria needed for a deliberate runtime implementation decision.

Consequences:

- Phase 8.4 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- Phase 5 runtime bridge remains gated
- Phase 9 is not approved by this closeout
- future runtime implementation requires explicit Phil approval of the narrow non-executing coordinator scope

## ADR-0143: Phase 8 Is Archived As No-Code Design Review Only

Status: Accepted

Decision:

Phase 8.5 archives Phase 8.0 through Phase 8.4 as a completed no-code implementation design review lane. The archive preserves the exact Phase 9 approval question and records that no runtime implementation was approved.

Rationale:

Phase 8 produced the design charter, file-touch map, acceptance-test design, rollback/audit proof plan, and approval gate. Archiving the lane prevents the next phase from inheriting approval by implication.

Consequences:

- Phase 8.5 is docs/tests/fixtures only
- no helper behavior is changed
- no `tests/support/` files are modified
- no files under `lima/` are modified
- Phase 5 runtime bridge remains gated
- Phase 9 runtime implementation remains blocked
- future runtime code requires explicit Phil approval of the preserved narrow question

## ADR-0144: Phase 9 Starts With Eligible File Confirmation

Status: Accepted

Decision:

Phase 9.0 confirms the Phase 8.1 file-touch map before any runtime implementation work. The map is explicit enough to proceed to Phase 9.1 acceptance test scaffolding.

Rationale:

The first runtime slice must not begin by guessing file scope. Confirming the exact eligible files protects the lane from drifting into adapters, `tests/support/`, Sparkbot wiring, IntentCompiler behavior, GuardianDecision behavior, approval enforcement, execution, or side effects.

Consequences:

- Phase 9.0 is docs/tests/fixtures only
- no files under `lima/` are modified
- no `tests/support/` files are modified
- Phase 9.1 may continue only as acceptance test scaffolding
- Phase 9.2 must touch only the Phase 8.1 eligible runtime files
- any need for a forbidden file surface stops the lane for Phil approval

## ADR-0145: Phase 9 Runtime Tests Precede Runtime Code

Status: Accepted

Decision:

Phase 9.1 records the Phase 9.2 acceptance obligations before the first runtime slice is implemented. The obligations are machine-checkable and limited to non-executing candidate metadata behavior.

Rationale:

The first runtime slice must be constrained by tests before code is added. Acceptance scaffolding prevents the coordinator from expanding into a HumanInput bridge, IntentCompiler, GuardianDecision, approval engine, execution path, audit persistence path, live adapter, or Sparkbot integration.

Consequences:

- Phase 9.1 is docs/tests/fixtures only
- no files under `lima/` are modified
- no `tests/support/` files are modified
- Phase 9.2 may implement only the narrow non-executing coordinator
- candidate outputs must be non-executable, not approved, and side-effect-free
- approval, execution, persistence, driver handoff, and physical-world behavior remain blocked

## ADR-0146: The First Runtime Slice Is Candidate Metadata Only

Status: Accepted

Decision:

Phase 9.2 implements a pure non-executing kernel intake-to-candidate coordinator under `lima/kernel/`. It accepts only synthetic already-normalized intake metadata and returns authority-free candidate metadata.

Rationale:

The smallest safe runtime step is not a bridge, compiler, Guardian decision, approval engine, or execution path. A candidate-metadata coordinator lets the kernel start forming safe internal metadata while keeping every consequential boundary behind future Guardian review.

Consequences:

- only `lima/kernel/__init__.py` and `lima/kernel/intake_candidate.py` are added as runtime files
- no existing contract file changes are required
- no HumanInput runtime bridge is added
- no real IntentEnvelope or GuardianDecision behavior is added
- approval enforcement, execution, audit persistence, Sparkbot wiring, live adapters, and side effects remain blocked
- Phase 9.3 must review the slice before any further implementation

## ADR-0147: Phase 9 Runtime Slice Is Ready Only For Closeout

Status: Accepted

Decision:

Phase 9.3 reviews the Phase 9.2 coordinator as constrained enough for Phase 9.4 audit/archive closeout, but not for runtime expansion.

Rationale:

The first runtime slice met the narrow non-executing candidate-metadata boundary. The safe next step is to archive the lane and stop at a new decision gate rather than continue implementing adjacent runtime behavior by momentum.

Consequences:

- Phase 9.3 is docs/tests/fixtures only
- no runtime code is changed
- no files under `lima/` are modified by Phase 9.3
- the Phase 9.2 coordinator remains non-executing
- Phase 9.4 may archive the lane
- Phase 10, runtime expansion, HumanInput bridge behavior, Sparkbot wiring, approval enforcement, execution, audit persistence, and physical-world behavior remain unapproved

## ADR-0072: Guardian Request Safety Gate Is the Standing Review Gate

Status: Accepted

Decision: LIMA will use `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` as the standing safety gate for Guardian-request-adjacent work.

Rationale: Guardian request is the boundary directly before GuardianDecision. A consolidated gate prevents requests from becoming hidden decisions, approvals, enforcement, or execution.

Consequences:

- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- manual review is required for future GuardianDecision work

## ADR-0073: Guardian Request Safety Gate Is Ready as Standing Gate

Status: Accepted

Decision: `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` is ready to serve as the standing review gate for Guardian-request-adjacent work.

Rationale: The gate consolidates request-vs-decision, request-vs-approval, tool-pack request semantics, approval/autonomy reference rules, fixture rules, forbidden behaviors, PR blockers, manual review, and real GuardianDecision exit criteria.

Consequences:

- Guardian-request safety-gate work may pause
- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- next work may move to fake GuardianDecision test design

## ADR-0074: Fake GuardianDecision Is Not Production Authorization

Decision:

LIMA may design fake GuardianDecision test shapes, but fake GuardianDecision must not be treated as real GuardianDecision, approval, enforcement, or production authorization.

Rationale:

GuardianDecision is the safety-critical authorization boundary. Fake decisions are useful for tests, but must not create production authority.

Consequences:

- real GuardianDecision remains blocked
- fake decision statuses must be clearly test-only
- approval refs remain references only
- no enforcement
- no execution
- no audit persistence

## ADR-0075: Fake GuardianDecision Fixtures Are Not Production Authorization

Decision:

LIMA may add fake GuardianDecision test fixtures, but fake decisions must not be treated as real GuardianDecision, approval, enforcement, audit evidence, or production authorization.

Rationale:

GuardianDecision is the safety-critical authorization boundary. Fake decision fixtures are useful for testing shape and risk behavior, but must remain clearly non-production.

Consequences:

- fake statuses must be test-only
- real GuardianDecision remains blocked
- enforcement remains blocked
- approval remains blocked
- execution remains blocked
- audit persistence remains blocked
