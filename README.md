# LIMA-AI-OS

LIMA-AI-OS is the Phase 0 home for the **LIMA Runtime / LIMA Kernel**: a Guardian-gated agent and robotics runtime extracted from Sparkbot.

This is not a greenfield rewrite. Sparkbot is the battle-tested source of truth. LIMA-AI-OS starts with architecture, contracts, and package boundaries so SparkPit Labs can extract the runtime safely, preserve Sparkbot parity, and put every externally actionable operation behind Guardian.

Company context: [SparkPit Labs](https://sparkpitlabs.com).

## Current Project State

Read `AGENTS.md` and `docs/CURRENT_PROJECT_STATE.md` before acting on roadmap or extraction-plan work. `docs/CURRENT_PROJECT_STATE.md` carries the current phase, latest approved main commit/tag, next intended branch, standing blocked items, and validation policy for Codex/operator workflows.

## Product North Star

LIMA-AI-OS is the trust-governed natural-language operating runtime/kernel for SparkPit Labs. Its long-term job is to let humans safely command AI models, assistant bots, office-worker bots, automation systems, IoT devices, drones, robots, and future humanoid systems through explicit Guardian-controlled trust boundaries.

Sparkbot is the open-source hobby/R&D shell and reference/publicity model. LIMA AI Office, ARC Bot, custom office-worker bots, and physical-world driver consumers are future product shells or runtime consumers. They are not implementation scope unless an explicit future phase approves them.

## What This Repo Is

LIMA Runtime is the trust-gated operating layer that should eventually sit underneath:

- Sparkbot Desktop / Workstation
- LIMA Guardian Suite
- LIMA Robo-OS
- Arc / LIMA AI Office
- SparkPit web systems
- office automation bots
- humanoid robots
- worker robots
- future agentic and robotic operating systems

The long-term vision can be called an AI OS. The engineering surface is more concrete: runtime, kernel, contracts, trust gate, model harness, spine, drivers, shells, tool packs, and persistence interface.

## Phase 0 Status

**Phase 0 only. No runtime implementation yet.**

This repository currently contains:

- Architecture documents
- Extraction plan
- Public contract definitions
- Package skeleton
- Import-only tests

It does not contain migrated Sparkbot runtime behavior, live tool execution, production deployment wiring, credentials, real model calls, or robotics control paths.

## Core Invariant

Every external action, tool execution, privileged operation, model call, robotics or physical-world action, file/network/browser action, and approval-requiring operation must pass through Guardian.

**Guardian is the syscall gate.**

No public Harness API should directly execute tools without Guardian classification, approval, denial, or routing. Every consequential execution path must carry a `GuardianDecision.decision_id` before execution and into downstream audit events.

## Natural Language Control Plane

Natural language is not just UI. It is the human control plane for LIMA Runtime.

LIMA is controlled through human-understandable language because humans need to command, understand, approve, and audit AI systems. Text and voice are first-class control surfaces. Operator consoles, mobile shells, gesture/manual controls, and future thought/BCI-style inputs are also human control surfaces, but they must compile into typed, governed intent before anything consequential executes.

Raw natural language never directly executes tools, files, network actions, browser actions, admin actions, payments, model calls, or robot/physical-world actions. Commands become typed `IntentEnvelope` records with confidence, risk class, evidence requirements, approval requirements, and tool-pack scope before Guardian evaluates them.

Guardian gates every meaningful action. LIMA exists to make AI systems and robots controllable by humans, not merely autonomous.

Future thought/BCI input is documented as a research-facing, confirmation-only surface. It may produce low-confidence intent candidates, but it must never directly actuate tools, systems, payments, admin functions, or physical-world drivers. Explicit confirmation and Guardian approval are mandatory.

## Tool-Pack Scoping

LIMA Runtime uses deny-by-default tool-pack scoping so each shell receives only the tools it is allowed to use. Sparkbot, Arc / LIMA AI Office, SparkPit web, Robo-OS, and future robot shells must declare allowed packs; Guardian decisions constrain which packs can reach the Harness shortlist.

No shell receives every tool by default. Consequential tool exposure and execution must carry `GuardianDecision.decision_id`.

Phase 0.9 inventories Sparkbot tools into deny-by-default packs before extraction. Sparkbot behavior remains the parity source, but broad full-catalogue exposure must not become a LIMA Runtime primitive.

Phase 0.10 defines default risk and approval policy for tool packs.

Phase 0.11 defines approval metadata for high/critical-risk actions, including breakglass and scheduled/autonomous inheritance.

Phase 0.12 defines end-to-end Spine/Audit lineage from human input to result.

Phase 0.13 defines redaction/privacy contracts so audit lineage can be useful without leaking secrets or private data.

Phase 0.14 maps Sparkbot, Guardian Suite, and Robo-OS surfaces to LIMA Runtime boundaries before extraction.

Phase 0.15 completes the extraction readiness review and identifies Phase 1.0 as Guardian Suite decoupling audit/import-boundary work.

Phase 1.0 audits Guardian Suite coupling and protects `lima.guardian` from Sparkbot backend imports.

Phase 1.1 defines non-executing Vault/Auth interfaces to decouple Guardian from Sparkbot internals without moving live secret/auth behavior.

Phase 1.2 adds provider-boundary tests to keep Vault/Auth seams free of Sparkbot internals and live secret/auth behavior.

Phase 1.3 adds test-only fake Auth/Vault/Breakglass providers with no real secret/auth behavior.

Phase 1.4 adds a fake in-memory Guardian decision evaluator for contract tests only; it does not enforce real policy or execute actions.

Phase 1.5 adds a fake in-memory policy/risk evaluator for contract tests only; it does not enforce real policy or authorize execution.

Phase 1.6 adds a fake in-memory ApprovalMetadata recorder for contract tests only; it does not enforce approval, verify PINs, open breakglass, or authorize execution.

Phase 1.7 adds a fake in-memory Spine/Audit recorder for contract tests only; it does not persist audit data or store raw sensitive content.

Phase 1.8 adds a fake in-memory Guardian pipeline proving contracts fit together without real enforcement, execution, persistence, or Sparkbot integration.

Phase 1.9 reviews the fake Guardian pipeline and permits adapter-design planning only, not production integration.

Phase 1.10 designs how Sparkbot input surfaces become LIMA HumanInput records without preserving raw chat-to-tool shortcuts.

Phase 1.11 defines describe-only HumanInput adapter contracts for future Sparkbot input mapping.

Phase 1.12A defines owner-controlled autonomy so bots can act freely inside configured boundaries while escalating high-risk actions.

Phase 1.12 reviews readiness for a non-production Sparkbot HumanInput adapter skeleton using neutral payloads and passive owner-autonomy metadata only.

Phase 1.13 adds a non-production Sparkbot HumanInput adapter skeleton using neutral payloads only.

Phase 1.14 reviews readiness to compose HumanInput with the fake Guardian pipeline while keeping the adapter boundary separate and non-production.

Phase 1.15 adds a test-only HumanInput-to-fake-pipeline bridge while keeping the Sparkbot adapter HumanInput-only.

Phase 1.16 reviews Phase 1 progress and routes next work toward identity/session/trust-context mapping before any real adapter implementation.

Phase 1.17 reviews identity/session/trust context mapping before any real Sparkbot adapter implementation.

Phase 1.18 adds trust-context contracts while keeping identity/session/trust/autonomy enforcement blocked.

Phase 1.19 adds test-only adapter fixtures with fake AuthContext/trust metadata while keeping references passive.

Phase 1.20 reviews real Sparkbot adapter readiness and keeps production wiring blocked pending payload/identity/trust stability.

Phase 1.21 adds synthetic Sparkbot payload fixture mirrors for adapter tests without importing Sparkbot.

Phase 1.22 defines payload drift checks so LIMA fixtures are reviewed against Sparkbot origin/main before adapter work.

Phase 1.23 hardens adapter boundaries so adapters remain isolated from Sparkbot runtime and execution paths.

Phase 1.24 reviews adapter safety and recommends Phase 2.0 as a non-production adapter fixture harness.

Phase 2.0 starts with a non-production fixture harness that validates fixture -> HumanInput -> fake pipeline flow without Sparkbot imports or execution.

Phase 2.1 reviews non-production fixture harness coverage and keeps production adapter wiring blocked.

Phase 2.2 expands synthetic Sparkbot fixture coverage for frontend, Workstation, SparkBud, auth/session, and model-routing contexts.

Phase 2.3 reviews expanded fixture harness coverage and keeps production adapter wiring blocked.

Phase 2.4 adds a non-production fixture regression harness for LIMA-owned Sparkbot payload fixtures.

Phase 2.5 reviews the fixture regression harness as a future adapter safety gate.

Phase 2.6 documents fixture regression as a standing safety gate for adapter-adjacent work.

Phase 2.7 reviews Phase 2 progress and recommends fixture regression report artifacts as the next safe step.

Phase 2.8 adds test-only fixture regression report helpers for human review; reports are not audit persistence.

Phase 2.9 reviews fixture regression report readiness and keeps production adapter wiring blocked.

Phase 2.10 hardens fixture regression reports with review gate fields while keeping reports non-production and non-persistent.

Phase 2.11 reviews regression gate readiness and recommends a final consolidated adapter safety gate.

Phase 2.12 finalizes `docs/ADAPTER_SAFETY_GATE.md` as the standing safety gate for adapter-adjacent work.

Phase 2.13 reviews the finalized adapter safety gate and recommends the next non-production kernel boundary.

Phase 2.14 reviews IntentEnvelope test design and keeps natural-language inference blocked.

Phase 2.15 adds synthetic IntentEnvelope fixtures using explicit typed metadata only; raw text is not parsed.

Phase 2.16 reviews IntentEnvelope fixture readiness before any test-only harness.

Phase 2.17 adds a test-only IntentEnvelope fixture harness that validates explicit typed metadata without parsing raw text.

Phase 2.18 reviews the IntentEnvelope fixture harness and recommends a standing safety gate for future IntentEnvelope work.

Phase 2.19 finalizes `docs/INTENTENVELOPE_SAFETY_GATE.md` as the standing safety gate for IntentEnvelope-adjacent work.

Phase 2.20 reviews the IntentEnvelope safety gate and recommends Guardian request test design as the next non-production kernel boundary.

Phase 2.21 reviews test-only Guardian request design and keeps GuardianDecision/enforcement blocked.

Phase 2.22 adds synthetic Guardian request fixtures and keeps GuardianDecision/enforcement blocked.

Phase 2.23 reviews Guardian request fixture readiness before any test-only harness.

Phase 2.24 adds a test-only Guardian request fixture harness and keeps GuardianDecision/enforcement blocked.

Phase 2.25 reviews the Guardian request fixture harness and recommends a standing safety gate for future Guardian request work.

Phase 2.26 finalizes `docs/GUARDIAN_REQUEST_SAFETY_GATE.md` as the standing safety gate for Guardian-request-adjacent work.

Phase 2.27 reviews the Guardian request safety gate and recommends fake GuardianDecision test design as the next non-production kernel boundary.

Phase 2.28 designs fake GuardianDecision test shapes while keeping real GuardianDecision and enforcement blocked.

Phase 2.29 adds fake GuardianDecision test fixtures while keeping real GuardianDecision and enforcement blocked.

Phase 2.30 reviews fake GuardianDecision fixture readiness before any test-only harness.

Phase 2.31 adds a test-only fake GuardianDecision fixture harness and keeps real GuardianDecision/enforcement blocked.

Phase 2.32 reviews the fake GuardianDecision fixture harness and recommends a standing safety gate for future fake GuardianDecision work.

Phase 2.33 finalizes `docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md` as the standing safety gate for fake GuardianDecision-adjacent work.

Phase 2.34 reviews the fake GuardianDecision safety gate and recommends Phase 2 final readiness review.

Phase 2.35 performs the final Phase 2 readiness review and recommends Phase 3.0 as non-production kernel pipeline design.

Phase 3.0 begins non-production kernel pipeline design while keeping production integration and runtime behavior blocked.

Phase 3.1 maps fixture families across the non-production kernel pipeline while keeping runtime behavior blocked.

Phase 3.2 reviews the non-production kernel pipeline fixture map before adding relationship metadata.

Phase 3.3 added non-runtime relationship metadata across kernel fixture families and is tagged as `phase-3.3-nonproduction-kernel-pipeline-relationship-metadata`.

Phase 3.4 reviewed the Phase 3.3 relationship metadata for readiness before future non-production report/map artifact work and is tagged as `phase-3.4-nonproduction-kernel-pipeline-relationship-metadata-readiness-review`.

Phase 3.5 added non-runtime LIMA Product Family and Adaptive Trust Doctrine docs, tests, and fixtures and is tagged as `phase-3.5-lima-product-family-adaptive-trust-doctrine`. It does not implement Sparkbot, ARC Bot, custom bots, robot control, adaptive trust enforcement, approval, execution, audit persistence, or runtime behavior.

Phase 3.6 added a static, non-runtime report/map artifact for the current fixture path and is tagged as `phase-3.6-nonproduction-kernel-pipeline-report-map-artifact`. It does not implement a report generator, pipeline, test-only harness, Sparkbot, ARC Bot, custom bots, robot control, adaptive trust enforcement, approval, execution, audit persistence, or runtime behavior.

Phase 3.7 adds Pipeline Composition Safety Gate Docs. It is docs/tests/fixtures only and defines preconditions, blockers, and future test-only harness conditions before any later readiness review. It does not add a pipeline, harness, runtime composition, approval, execution, enforcement, audit persistence, Sparkbot wiring, product shell implementation, or physical-world action. The next likely phase after Phase 3.7 is Phase 3.8, Pipeline Composition Safety Gate Readiness Review.

Phase 3.8 reviews the Pipeline Composition Safety Gate and keeps harness work blocked. It is docs/tests/fixtures only and recommends Phase 3 final readiness review before any Phase 4 planning.

Phase 3.9 is the final Phase 3 readiness review. It closes Phase 3 as non-runtime kernel pipeline safety work and recommends Phase 4.0 Runtime Extraction Readiness Planning only. It does not approve Phase 4 implementation, Sparkbot integration, product shell implementation, approval, execution, audit persistence, robot control, or physical-world action.

Phase 4.0 starts Runtime Extraction Readiness Planning. It is planning only and recommends Phase 4.1 Sparkbot Runtime Reference Refresh as the next read-only step. It does not move runtime behavior, import Sparkbot, wire routes, call models, execute tools, enforce approvals, persist audit events, implement product shells, or control physical-world systems.

Phase 4.1 refreshes Sparkbot runtime reference knowledge from the local Sparkbot checkout as read-only spec material. It identifies HumanInput intake for chat and voice as the safest Phase 4.2 candidate-selection direction and keeps runtime extraction, Sparkbot wiring, tool execution, terminal/PTY, robotics, product shells, approval enforcement, execution, audit persistence, and physical-world action blocked.

Phase 4.2 selects the non-executing HumanInput intake boundary for chat and voice as the first runtime boundary candidate to carry into a Phase 4.3 safety gate. It does not implement adapters, import Sparkbot, wire routes, parse natural language into action, call models, expose tools, execute commands, enforce policy, persist audit events, or control physical-world systems.

Phase 4.3 defines the Boundary Extraction Safety Gate for the selected HumanInput intake boundary. It permits only a future Phase 4.4 fixture/contract extension if explicitly approved and keeps adapters, runtime extraction, Sparkbot wiring, live lookup, model/tool/terminal/robotics behavior, approval enforcement, audit persistence, product shells, and physical-world action blocked.

Phase 4.4 extends synthetic HumanInput intake fixture/contract metadata for text and voice. The fixtures carry reference-only source, actor, session, trust, privacy, lineage, and handoff metadata and prove they cannot imply authorization, approval, execution, trust lookup, Sparkbot integration, or production runtime behavior.

Phase 4.5 reviews the HumanInput intake boundary as conditionally ready only for a future explicitly approved narrow non-production proposal. It keeps runtime extraction, Sparkbot integration, live adapter code, model/tool/terminal/robotics behavior, approval/enforcement/execution/audit persistence, product shells, and physical-world action blocked.

Phase 4.6 adds a non-production HumanInput adapter proposal as docs/tests/fixtures only. It describes how a future shell intake adapter could convert selected shell input context into the Phase 4.4 HumanInput fixture/contract shape, but it is not an adapter, not executable, not Sparkbot integration, not authorization, not approval, not execution, not audit persistence, and not a trust lookup.

Phase 4.7 reviews the Phase 4.6 proposal as ready only for future HumanInput Adapter Safety Gate Docs. It keeps live adapter code, Sparkbot wiring, runtime behavior, model/tool/terminal/robotics behavior, live trust lookup, real IntentCompiler, real GuardianDecision, approval/enforcement/execution/audit persistence, product shells, and physical-world action blocked.

Phase 4.8 adds HumanInput Adapter Safety Gate Docs. It requires any future HumanInput adapter to return HumanInput only and keeps live adapter code, Sparkbot imports/wiring, runtime behavior, real IntentCompiler, real GuardianDecision, approval/enforcement/execution/audit persistence, model/tool/terminal/robot behavior, live lookup, and physical-world action blocked.

Phase 4.9 reviews HumanInput adapter implementation readiness as docs/tests/fixtures only. It finds the boundary ready only for a future explicitly approved test-only HumanInput adapter harness proposal, while keeping live adapter code, production Sparkbot integration, runtime wiring, real IntentCompiler, real GuardianDecision, approval/enforcement/execution/audit persistence, model/tool/terminal/robot behavior, live lookup, and physical-world action blocked.

Phase 4.10 proposes a future test-only HumanInput adapter harness as docs/tests/fixtures only. It describes synthetic inputs, expected HumanInput fixture shape, safety boundaries, and validation requirements, but does not implement harness code, adapter code, runtime behavior, Sparkbot integration, approval/enforcement/execution/audit persistence, or physical-world action.

Phase 4.11 reviews the Phase 4.10 test-only harness proposal as clear enough for future safety gate documentation only. It keeps harness code, live adapter code, runtime behavior, Sparkbot integration, live lookup, model/tool/terminal/robot behavior, approval/enforcement/execution/audit persistence, and physical-world action blocked.

Phase 4.12 adds Test-only HumanInput Adapter Harness Safety Gate Docs. It states that any future test-only harness is not runtime, not Sparkbot integration, cannot call models/tools/terminal/robots, cannot approve/enforce/execute/audit, cannot perform live lookup, and cannot imply production adapter readiness.

Phase 4.13 reviews the full Phase 4 HumanInput boundary lane as docs/tests/fixtures only. It finds the lane ready only for a future explicitly approved test-only HumanInput adapter harness implementation phase or further non-runtime review, while keeping live adapter code, production Sparkbot integration, runtime wiring, real IntentCompiler, real GuardianDecision, approval/enforcement/execution/audit persistence, live lookup, model/tool/terminal/robot behavior, and physical-world action blocked.

Phase 4.14 adds a deterministic test-only HumanInput adapter harness under `tests/support/`. It validates synthetic Phase 4.4 fixture records and converts them into HumanInput-shaped test dictionaries only, while rejecting live/runtime/prod markers and keeping runtime code, Sparkbot integration, IntentEnvelope, GuardianDecision, approval, enforcement, execution, audit persistence, live lookup, and physical-world action blocked.

Phase 4.15 reviews the Phase 4.14 test-only harness as constrained, deterministic, synthetic-only, and non-runtime. It recommends Phase 4.16 HumanInput boundary lane closeout review only, not live adapter code, runtime wiring, Sparkbot integration, approval/enforcement/execution/audit persistence, or physical-world action.

Phase 4.16 closes the HumanInput boundary lane as complete enough to stop Phase 4 HumanInput work and propose the next explicitly approved lane, likely HumanInput to IntentEnvelope boundary planning. It does not approve next-lane implementation, live adapter code, runtime wiring, Sparkbot integration, approval/enforcement/execution/audit persistence, or physical-world action.

Phase 4.17 opens HumanInput to IntentEnvelope boundary planning as docs/tests/fixtures only. It aligns the next lane with the standing IntentEnvelope safety gate and keeps schema implementation, bridge code, real IntentCompiler, GuardianDecision, model/tool execution, Sparkbot wiring, approval/enforcement/execution/audit persistence, and physical-world action blocked.

Phase 4.18 proposes a static HumanInput to IntentEnvelope boundary schema/contract as docs/tests/fixtures only. It identifies HumanInput references, explicit typed intent metadata, and safety markers for future review, but does not create IntentEnvelope records, implement a bridge, implement IntentCompiler behavior, or approve runtime wiring.

Phase 4.19 reviews the HumanInput to IntentEnvelope boundary schema/contract proposal as docs/tests/fixtures only. It finds the proposal ready for Phase 4.20 Phase 5 gate / implementation readiness closeout, while keeping bridge code, real IntentCompiler behavior, real GuardianDecision behavior, runtime wiring, approval/enforcement/execution/audit persistence, Sparkbot integration, and physical-world action blocked.

Phase 4.20 closes the HumanInput to IntentEnvelope non-runtime planning lane at a Phase 5 gate. It confirms Phase 5 requires an explicit operator scope decision before any runtime behavior, test-only bridge code, live adapter code, real IntentCompiler behavior, real GuardianDecision behavior, approval/enforcement/execution/audit persistence, Sparkbot integration, or physical-world action.

Phase 5.0 opens Phase 5 as non-runtime planning only. It records the HumanInput to IntentEnvelope boundary charter, treats HumanInput as an operator-originated request envelope rather than an execution command, and keeps implementation, bridge code, runtime wiring, live adapter code, real IntentCompiler behavior, real GuardianDecision behavior, approval enforcement, audit persistence, Sparkbot integration, and physical-world action blocked.

Phase 5.1 proposes the HumanInput to IntentEnvelope contract as static non-runtime metadata. It defines preserved request fields and descriptive candidate states, but does not create IntentEnvelope records, implement bridge code, run IntentCompiler behavior, enforce approvals, execute actions, persist audit, or add runtime wiring.

Phase 5.2 proposes a future test-only HumanInput to IntentEnvelope bridge harness as docs/tests/fixtures only. It describes required synthetic inputs, future output constraints, and fail-closed conditions, but does not implement bridge code, create IntentEnvelope records, call models/tools, execute actions, persist audit, or add runtime wiring.

Phase 5.3 reviews the test-only bridge harness proposal as docs/tests/fixtures only and stops at an implementation gate. It finds the proposal ready only for an explicit operator implementation-scope decision, while keeping bridge code, runtime wiring, live adapter code, real IntentCompiler behavior, real GuardianDecision behavior, approval enforcement, execution, audit persistence, Sparkbot integration, and physical-world action blocked.

Phase 5.4 adds a deterministic test-only HumanInput to IntentEnvelope bridge helper under `tests/support/`. It converts synthetic HumanInput-shaped dictionaries into non-executable IntentEnvelope-candidate-shaped test dictionaries only, while keeping `lima/` runtime code, live adapter behavior, Sparkbot wiring, real IntentCompiler behavior, real GuardianDecision behavior, approval enforcement, execution, audit persistence, and physical-world action blocked.

Phase 5.5 reviews the Phase 5.4 helper as docs/tests/fixtures only. It confirms the helper remains test-only, must not be reused as runtime classifier logic, and keeps Phase 5.6, live runtime implementation, helper expansion, `lima/` changes, Sparkbot wiring, real IntentCompiler behavior, real GuardianDecision behavior, approval enforcement, execution, audit persistence, and physical-world action gated.

Phase 5.6 adds a docs/tests/fixtures-only HumanInput Runtime Bridge Safety Gate / Next-Scope Decision Record. It requires explicit Phil approval before any future live/runtime bridge and requires runtime design before implementation, while keeping the Phase 5.4 helper test-only and keeping Phase 5.7 gated.

Phase 5.7 adds a docs/tests/fixtures-only HumanInput Runtime Bridge Design Proposal. It documents allowed/rejected inputs, provenance, non-executable candidates, approval-required semantics, risk metadata, trust/autonomy boundaries, and blocked behavior without implementing a runtime bridge or changing helper behavior.

Phase 5.8 adds a docs/tests/fixtures-only HumanInput Runtime Bridge Threat Model. It documents injection, impersonation, trust bypass, accidental execution, side-effect escalation, audit gaps, approval confusion, helper misuse, malformed input, replay, and ambiguity threats while keeping live/runtime implementation blocked.

Phase 5.9 adds a docs/tests/fixtures-only HumanInput Runtime Bridge Boundary Validation Matrix. It makes low-risk, side-effecting, bypass, ambiguous, empty, malformed, and replay/stale categories machine-checkable while keeping every output non-executable and keeping runtime implementation blocked.

Phase 5.10 closes the HumanInput runtime bridge design lane with a docs/tests/fixtures-only implementation gate / closeout review. It records what was designed, what remains unimplemented, what runtime implementation would require, and that live/runtime implementation still requires explicit Phil approval.

Phase 5.11 archives the completed Phase 5 HumanInput bridge design lane as docs/tests/fixtures-only planning/specification work. It confirms Phase 5.0 through Phase 5.10 are complete, the Phase 5.4 helper remains test-only, no live/runtime bridge exists, and future runtime work requires new explicit Phil approval.

Phase 6.0 starts broader LIMA OS roadmap planning as docs/tests/fixtures only. It reorients from the archived Phase 5 bridge lane toward kernel lifecycle planning and keeps runtime bridge implementation, `lima/` changes, Sparkbot wiring, execution, approval enforcement, audit persistence, and physical-world action blocked.

Phase 6.1 adds docs/tests/fixtures-only LIMA Kernel Lifecycle Planning. It maps shell intake, boundary normalization, IntentEnvelope candidate formation, Guardian review, GuardianDecision record, spine/audit/memory handoff, and blocked driver handoff without implementing runtime behavior.

Phase 6.2 adds docs/tests/fixtures-only IntentEnvelope and GuardianDecision Lifecycle Boundary Mapping. It keeps IntentEnvelope candidates non-executable and separates descriptive candidate metadata from future GuardianDecision authority without implementing runtime behavior.

Phase 6.3 adds docs/tests/fixtures-only Approval / Audit / Memory Boundary Planning. It keeps approval states descriptive, audit/spine metadata as lineage planning, and memory references reference-only without adding enforcement, persistence, memory IO, or runtime behavior.

Phase 6.4 closes the current broader LIMA OS roadmap planning lane with a docs/tests/fixtures-only roadmap gate. It lists next-scope options and keeps Phase 7, runtime bridge implementation, `lima/` changes, helper behavior changes, Sparkbot wiring, execution, approval enforcement, audit persistence, memory IO, and physical-world action blocked until Phil explicitly selects a new scope.

Phase 6.5 archives Phase 6 as completed roadmap/planning work. It confirms Phase 6.0 through Phase 6.4 added docs, fixtures, static tests, and roadmap/state updates only, while keeping Phase 5 runtime bridge work and all future runtime lanes gated pending explicit Phil approval.

Phase 7.0 opens a no-code Kernel Runtime Implementation Charter lane. It defines the smallest future runtime slice that could be considered later, but it does not approve runtime implementation or modify `lima/`, `tests/support/`, Sparkbot wiring, execution, approval enforcement, audit persistence, or physical-world behavior.

Phase 7.1 adds a docs/tests/fixtures-only First Runtime Slice Eligibility Map. It names future-eligible contract files and forbidden execution surfaces for a later explicitly approved slice, while keeping all `lima/` and `tests/support/` files untouched.

Phase 7.2 adds docs/tests/fixtures-only Kernel Runtime Safety Preconditions. It defines required tests, rollback expectations, audit proof, input/output shape constraints, and safety gates that must be satisfied before any future runtime code can be approved.

Phase 7.3 adds a docs/tests/fixtures-only Runtime Implementation Test Plan. It defines future test families, required negative cases, limited positive cases, and validation commands without implementing runtime behavior.

Phase 7.4 closes the no-code Phase 7 charter lane at an implementation decision gate. It keeps runtime implementation, `lima/` changes, `tests/support/` changes, Sparkbot wiring, live adapters, execution, approval enforcement, audit persistence, and physical-world behavior blocked until Phil explicitly chooses the next step.

Phase 7.5 archives Phase 7 as a no-code kernel runtime charter lane. It confirms Phase 7.0 through Phase 7.4 added docs, fixtures, static tests, and roadmap/state updates only, while keeping Phase 5 runtime bridge work and all future runtime code gated pending explicit Phil approval.

## Runtime Shape

LIMA Runtime is organized around these layers:

- Human Control Surface: text, voice, console, gesture, future BCI
- Intent Compiler: normalization, clarification, typed intent, confidence, risk class, evidence requirements
- Shells: Sparkbot, Arc / LIMA AI Office, SparkPit web, Robo shell, future robot shells
- System Services: skills, comms, voice, office automation, tasks/projects
- Spine: task/event/process ledger, schedulers, audit, lineage
- Guardian: policy, auth, vault, token/cost control, verifier, approvals, breakglass
- Model Harness: model routing, tool catalogue, tool-pack scoping, prompt cache, telemetry
- IO Drivers: Robo-OS, filesystem, browser, network, MCP servers, devices
- Persistence: one interface over SQLite, Postgres, Memory/Vault backends, future stores

## Roadmap

### Phase 0: Runtime Contracts

Current phase. Define the architecture, contracts, package skeleton, and import validation only.

Acceptance line:

- README, architecture, extraction plan, contracts, reference notes, roadmap, and ADRs exist.
- Python contract stubs import and compile.
- No Sparkbot implementation code is migrated.
- No live tools, model calls, production deploys, credentials, or robotics execution paths are wired.

### Phase 1: Guardian Extraction Readiness

Decouple Guardian from Sparkbot application imports and route-level assumptions while preserving Sparkbot behavior.

Focus:

- policy
- auth
- vault references
- token and cost control
- verifier
- approvals
- breakglass
- memory/memo policy
- audit decisions

Sparkbot remains the parity source.

### Phase 2: Model Harness Extraction

Extract model routing, fallback, tool catalogue, tool-pack scoping, prompt cache, telemetry, and friendly error handling.

Non-negotiable: the Harness may plan tool calls, but no public Harness API may execute tools without a Guardian decision or approval token.

### Phase 3: Spine Extraction

Extract the process/task/event ledger, schedulers, recurring jobs, audit writer, autonomous loop metadata, and project/task lineage.

Spine records lineage. Guardian gates action.

### Phase 4: Sparkbot On LIMA Runtime

Run Sparkbot as the first production shell on top of LIMA Runtime contracts.

Acceptance line:

- Sparkbot operator UX remains intact.
- Guardian decisions match existing behavior.
- Tool calls, approvals, memory events, model calls, and Spine events pass parity tests.

### Phase 5: Robo-OS Driver Integration

Integrate LIMA Robo-OS as a Guardian-gated IO driver/runtime layer.

Rules:

- dry-run and simulation first
- capabilities declared before use
- telemetry required for physical-world actions
- medium/high/unknown robot commands require Guardian approval
- real hardware motion is blocked by default until approval and audit flows are proven

Robo-OS is a gated driver, not a competing brain.

### Phase 6: Office, Web, And Robot Shells

Bring Arc / LIMA AI Office, SparkPit web systems, office automation bots, humanoid shells, worker robot shells, and future agentic operating environments onto the shared runtime.

Each shell declares allowed tool packs and permissions. No shell receives every tool by default.

## Reference Docs

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [docs/EXTRACTION_PLAN.md](docs/EXTRACTION_PLAN.md)
- [docs/CONTRACTS.md](docs/CONTRACTS.md)
- [docs/INTENT_COMPILER_BOUNDARY.md](docs/INTENT_COMPILER_BOUNDARY.md)
- [docs/SPARKBOT_ENTRYPOINT_INVENTORY.md](docs/SPARKBOT_ENTRYPOINT_INVENTORY.md)
- [docs/SPARKBOT_TOOL_PACK_INVENTORY.md](docs/SPARKBOT_TOOL_PACK_INVENTORY.md)
- [docs/GUARDIAN_DECISION_CONTRACT.md](docs/GUARDIAN_DECISION_CONTRACT.md)
- [docs/APPROVAL_METADATA_CONTRACT.md](docs/APPROVAL_METADATA_CONTRACT.md)
- [docs/SPINE_AUDIT_LINEAGE_CONTRACT.md](docs/SPINE_AUDIT_LINEAGE_CONTRACT.md)
- [docs/REDACTION_PRIVACY_CONTRACT.md](docs/REDACTION_PRIVACY_CONTRACT.md)
- [docs/RUNTIME_BOUNDARY_MAP.md](docs/RUNTIME_BOUNDARY_MAP.md)
- [docs/EXTRACTION_READINESS_REVIEW.md](docs/EXTRACTION_READINESS_REVIEW.md)
- [docs/PHASE_1_0_GUARDIAN_SUITE_DECOUPLING_AUDIT.md](docs/PHASE_1_0_GUARDIAN_SUITE_DECOUPLING_AUDIT.md)
- [docs/PHASE_1_1_VAULT_AUTH_INTERFACE_SKELETON.md](docs/PHASE_1_1_VAULT_AUTH_INTERFACE_SKELETON.md)
- [docs/PHASE_1_2_VAULT_AUTH_PROVIDER_BOUNDARY_TESTS.md](docs/PHASE_1_2_VAULT_AUTH_PROVIDER_BOUNDARY_TESTS.md)
- [docs/PHASE_1_3_VAULT_AUTH_FAKE_PROVIDERS.md](docs/PHASE_1_3_VAULT_AUTH_FAKE_PROVIDERS.md)
- [docs/PHASE_1_4_GUARDIAN_DECISION_FAKE_EVALUATOR.md](docs/PHASE_1_4_GUARDIAN_DECISION_FAKE_EVALUATOR.md)
- [docs/PHASE_1_5_POLICY_RISK_FAKE_EVALUATOR.md](docs/PHASE_1_5_POLICY_RISK_FAKE_EVALUATOR.md)
- [docs/PHASE_1_6_APPROVAL_FAKE_RECORDER.md](docs/PHASE_1_6_APPROVAL_FAKE_RECORDER.md)
- [docs/PHASE_1_7_SPINE_AUDIT_FAKE_RECORDER.md](docs/PHASE_1_7_SPINE_AUDIT_FAKE_RECORDER.md)
- [docs/PHASE_1_8_GUARDIAN_FAKE_PIPELINE.md](docs/PHASE_1_8_GUARDIAN_FAKE_PIPELINE.md)
- [docs/PHASE_1_9_FAKE_PIPELINE_READINESS_REVIEW.md](docs/PHASE_1_9_FAKE_PIPELINE_READINESS_REVIEW.md)
- [docs/PHASE_1_10_SPARKBOT_HUMANINPUT_ADAPTER_DESIGN.md](docs/PHASE_1_10_SPARKBOT_HUMANINPUT_ADAPTER_DESIGN.md)
- [docs/PHASE_1_11_HUMANINPUT_ADAPTER_CONTRACT.md](docs/PHASE_1_11_HUMANINPUT_ADAPTER_CONTRACT.md)
- [docs/OWNER_AUTONOMY_SAFETY_POLICY.md](docs/OWNER_AUTONOMY_SAFETY_POLICY.md)
- [docs/PHASE_1_12_SPARKBOT_ADAPTER_READINESS_REVIEW.md](docs/PHASE_1_12_SPARKBOT_ADAPTER_READINESS_REVIEW.md)
- [docs/PHASE_1_13_SPARKBOT_HUMANINPUT_ADAPTER_SKELETON.md](docs/PHASE_1_13_SPARKBOT_HUMANINPUT_ADAPTER_SKELETON.md)
- [docs/PHASE_1_14_HUMANINPUT_ADAPTER_READINESS_REVIEW.md](docs/PHASE_1_14_HUMANINPUT_ADAPTER_READINESS_REVIEW.md)
- [docs/PHASE_1_15_HUMANINPUT_FAKE_PIPELINE_BRIDGE.md](docs/PHASE_1_15_HUMANINPUT_FAKE_PIPELINE_BRIDGE.md)
- [docs/PHASE_1_16_PHASE_ONE_READINESS_REVIEW.md](docs/PHASE_1_16_PHASE_ONE_READINESS_REVIEW.md)
- [docs/PHASE_1_17_IDENTITY_SESSION_TRUST_CONTEXT_REVIEW.md](docs/PHASE_1_17_IDENTITY_SESSION_TRUST_CONTEXT_REVIEW.md)
- [docs/PHASE_1_18_AUTHCONTEXT_TRUST_CONTRACT_EXTENSION.md](docs/PHASE_1_18_AUTHCONTEXT_TRUST_CONTRACT_EXTENSION.md)
- [docs/PHASE_1_19_ADAPTER_FIXTURE_TESTS_WITH_FAKE_AUTHCONTEXT.md](docs/PHASE_1_19_ADAPTER_FIXTURE_TESTS_WITH_FAKE_AUTHCONTEXT.md)
- [docs/PHASE_1_20_REAL_ADAPTER_READINESS_REVIEW.md](docs/PHASE_1_20_REAL_ADAPTER_READINESS_REVIEW.md)
- [docs/PHASE_1_21_SPARKBOT_PAYLOAD_FIXTURE_MIRROR.md](docs/PHASE_1_21_SPARKBOT_PAYLOAD_FIXTURE_MIRROR.md)
- [docs/PHASE_1_22_PAYLOAD_DRIFT_CHECK_CONTRACT.md](docs/PHASE_1_22_PAYLOAD_DRIFT_CHECK_CONTRACT.md)
- [docs/PHASE_1_23_ADAPTER_BOUNDARY_HARDENING.md](docs/PHASE_1_23_ADAPTER_BOUNDARY_HARDENING.md)
- [docs/PHASE_1_24_PHASE_ONE_ADAPTER_SAFETY_REVIEW.md](docs/PHASE_1_24_PHASE_ONE_ADAPTER_SAFETY_REVIEW.md)
- [docs/PHASE_2_0_NONPRODUCTION_ADAPTER_FIXTURE_HARNESS.md](docs/PHASE_2_0_NONPRODUCTION_ADAPTER_FIXTURE_HARNESS.md)
- [docs/PHASE_2_1_FIXTURE_HARNESS_COVERAGE_REVIEW.md](docs/PHASE_2_1_FIXTURE_HARNESS_COVERAGE_REVIEW.md)
- [docs/PHASE_2_2_FIXTURE_COVERAGE_EXPANSION.md](docs/PHASE_2_2_FIXTURE_COVERAGE_EXPANSION.md)
- [docs/PHASE_2_3_HARNESS_COVERAGE_READINESS_REVIEW.md](docs/PHASE_2_3_HARNESS_COVERAGE_READINESS_REVIEW.md)
- [docs/PHASE_2_4_FIXTURE_REGRESSION_HARNESS.md](docs/PHASE_2_4_FIXTURE_REGRESSION_HARNESS.md)
- [docs/PHASE_2_5_FIXTURE_REGRESSION_READINESS_REVIEW.md](docs/PHASE_2_5_FIXTURE_REGRESSION_READINESS_REVIEW.md)
- [docs/PHASE_2_6_FIXTURE_REGRESSION_CI_GATE_DOCS.md](docs/PHASE_2_6_FIXTURE_REGRESSION_CI_GATE_DOCS.md)
- [docs/PHASE_2_7_PHASE_TWO_READINESS_REVIEW.md](docs/PHASE_2_7_PHASE_TWO_READINESS_REVIEW.md)
- [docs/PHASE_2_8_FIXTURE_REGRESSION_REPORT_ARTIFACT.md](docs/PHASE_2_8_FIXTURE_REGRESSION_REPORT_ARTIFACT.md)
- [docs/PHASE_2_9_REGRESSION_REPORT_READINESS_REVIEW.md](docs/PHASE_2_9_REGRESSION_REPORT_READINESS_REVIEW.md)
- [docs/PHASE_2_10_REGRESSION_REPORT_GATE_HARDENING.md](docs/PHASE_2_10_REGRESSION_REPORT_GATE_HARDENING.md)
- [docs/PHASE_2_11_REGRESSION_GATE_READINESS_REVIEW.md](docs/PHASE_2_11_REGRESSION_GATE_READINESS_REVIEW.md)
- [docs/ADAPTER_SAFETY_GATE.md](docs/ADAPTER_SAFETY_GATE.md)
- [docs/PHASE_2_12_ADAPTER_SAFETY_GATE_FINALIZATION.md](docs/PHASE_2_12_ADAPTER_SAFETY_GATE_FINALIZATION.md)
- [docs/PHASE_2_13_ADAPTER_SAFETY_GATE_READINESS_REVIEW.md](docs/PHASE_2_13_ADAPTER_SAFETY_GATE_READINESS_REVIEW.md)
- [docs/PHASE_2_14_INTENT_ENVELOPE_TEST_DESIGN_REVIEW.md](docs/PHASE_2_14_INTENT_ENVELOPE_TEST_DESIGN_REVIEW.md)
- [docs/PHASE_2_15_INTENT_ENVELOPE_TEST_FIXTURES.md](docs/PHASE_2_15_INTENT_ENVELOPE_TEST_FIXTURES.md)
- [docs/PHASE_2_16_INTENTENVELOPE_FIXTURE_READINESS_REVIEW.md](docs/PHASE_2_16_INTENTENVELOPE_FIXTURE_READINESS_REVIEW.md)
- [docs/KERNEL_PIPELINE_REPORT_MAP_ARTIFACT.md](docs/KERNEL_PIPELINE_REPORT_MAP_ARTIFACT.md)
- [docs/PHASE_3_6_NONPRODUCTION_KERNEL_PIPELINE_REPORT_MAP_ARTIFACT.md](docs/PHASE_3_6_NONPRODUCTION_KERNEL_PIPELINE_REPORT_MAP_ARTIFACT.md)
- [docs/INTENTENVELOPE_SAFETY_GATE.md](docs/INTENTENVELOPE_SAFETY_GATE.md)
- [docs/TOOL_PACK_SCOPING.md](docs/TOOL_PACK_SCOPING.md)
- [docs/TOOL_PACK_RISK_POLICY.md](docs/TOOL_PACK_RISK_POLICY.md)
- [docs/REFERENCE_REPOS.md](docs/REFERENCE_REPOS.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/DECISIONS.md](docs/DECISIONS.md)

## Extraction Rules

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.

Do not migrate implementation code until contracts are reviewed and accepted.
