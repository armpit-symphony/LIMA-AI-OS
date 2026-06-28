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

## Current Safety Status

**Candidate-only, non-production safety work. No live/executing runtime behavior is approved.**

This repository currently contains:

- Architecture documents
- Extraction plan
- Public contract definitions
- Package skeleton
- Import-only tests
- Narrow non-executing candidate, preview, status-normalization, and read-only runtime-state helpers

It does not contain migrated Sparkbot runtime behavior, live tool execution, production deployment wiring, credentials, real model calls, or robotics control paths.

## Current V1 Status

LIMA remains `CANDIDATE_ONLY`.

Current post-approval update: `Approve-V1-G61` is recorded and the bounded V1-G61 runtime vendor SDK import execution proof is complete as local test-scoped evidence. The proof imports only the approved `openai` module in tests, records sanitized version evidence `2.43.0`, and does not edit `lima/`, dependency manifests, lockfiles, Sparkbot, Arc-Bot-shell, provider clients, endpoint resolution, network egress, credentials, fallback, consumer production integration, product readiness, or final public API freeze. The latest V1 final readiness audit execution is recorded in `docs/audits/V1_FINAL_READINESS_AUDIT.md` with verdict `BLOCKED_RELEASE_CANDIDATE_CHECKLIST_AND_CUTOVER_AUTHORITY_NOT_SATISFIED`. Current consumer smoke and LIMA validation evidence pass, the release-candidate checklist is satisfied for first-consumer harness testing, and exactly one valid cutover operator choice remains required before any branch, tag, cutover, or readiness claim.

Post-reconciliation update: `docs/audits/V1_FINAL_READINESS_RECONCILIATION_AUDIT.md` records verdict `PASS_CANDIDATE_READY_FOR_FIRST_CONSUMER_HARNESS_TESTING_CUTOVER_AUTHORIZATION_REQUIRED`. This resolves the circular final-readiness/checklist blocker for first-consumer harness testing only. `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md` is prepared with status `AWAITING_EXPLICIT_CUTOVER_OPERATOR_DECISION`; it does not authorize release-candidate branch creation, tag creation, cutover, V1.0.0 completion, product readiness, production readiness, or consumer production integration.

The V1 target is to make LIMA usable first by `Sparkbot_shell`, public `Sparkbot`, and `Arc-Bot-shell`. The V1 runtime authority chain is audited through `V1-G56`; completed implementation evidence is refreshed through `V1-G60`; request-stage readiness is refreshed through the post-G61 request readiness refresh; and the V1-G61 runtime vendor SDK import execution proof approval request is prepared for operator decision.

The V1-G61 request gate is independently audited in `docs/audits/V1_G61_RUNTIME_VENDOR_SDK_IMPORT_EXECUTION_PROOF_APPROVAL_REQUEST_AUDIT.md`, with the current request-only readiness refresh recorded in `docs/readiness/V1_POST_G61_REQUEST_READINESS_REFRESH.md`. The preapproval runtime-tree guard is recorded in `docs/audits/V1_G61_PREAPPROVAL_RUNTIME_TREE_GUARD_AUDIT.md` and checks that no runtime vendor SDK import or provider client construction appears in `lima/` before exact approval. These artifacts preserve the operator-decision blocker and do not approve implementation.

The V1-G61 operator decision packet status audit is recorded in `docs/audits/V1_G61_OPERATOR_DECISION_PACKET_STATUS_AUDIT.md`. It proves `Approve-V1-G61` is recorded for bounded local import-proof evidence only and does not create release-candidate, cutover, product-readiness, or production-readiness authority.

The current gate consistency audit is recorded in `docs/audits/V1_CURRENT_GATE_CONSISTENCY_AUDIT.md`. It checks the current-facing README, project-state, readiness, and audit artifacts for alignment on the active V1-G61 operator-decision gate and rejects stale public Sparkbot publication or V1-G57 active-blocker language.

The current local harness handoff for Sparkbot and Arc-Bot-shell is recorded in `docs/readiness/V1_CANDIDATE_TEST_HANDOFF_MANIFEST.md`, with the shortest safe local smoke command path captured in `docs/readiness/V1_CANDIDATE_HARNESS_QUICKSTART.md`, current quickstart execution evidence captured in `docs/audits/V1_CANDIDATE_HARNESS_QUICKSTART_EXECUTION_AUDIT.md`, harness usability criteria captured in `docs/readiness/V1_CONSUMER_HARNESS_USABILITY_MATRIX.md`, consumer checkpoint coordination captured in `docs/readiness/V1_CONSUMER_CHECKPOINT_MANIFEST.md`, current validation refresh evidence captured in `docs/audits/V1_CURRENT_CANDIDATE_VALIDATION_REFRESH_AUDIT.md`, post-validation readiness-change freshness captured in `docs/audits/V1_POST_VALIDATION_READINESS_CHANGE_FRESHNESS_AUDIT.md`, the current Arc-Bot-shell drift exclusion audit captured in `docs/audits/V1_ARC_BOT_SHELL_LOCAL_DRIFT_EXCLUSION_AUDIT.md`, the V1.0.0 release-candidate bar captured in `docs/readiness/V1_RELEASE_CANDIDATE_ACCEPTANCE_CHECKLIST.md`, the blocked future cutover path captured in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_RUNBOOK.md`, the final readiness audit template captured in `docs/readiness/V1_FINAL_READINESS_AUDIT_TEMPLATE.md`, the historical final readiness audit execution captured in `docs/audits/V1_FINAL_READINESS_AUDIT.md`, the final readiness reconciliation captured in `docs/audits/V1_FINAL_READINESS_RECONCILIATION_AUDIT.md`, the active cutover blocker summarized in `docs/readiness/V1_FINAL_BLOCKER_REGISTER.md`, the operator handoff action captured in `docs/readiness/V1_OPERATOR_UNBLOCK_ACTION_PACKET.md`, and the saved candidate branch map captured in `docs/readiness/V1_FINAL_CANDIDATE_BRANCH_INDEX.md`. These artifacts keep the consumer smoke path testable with fake in-process executors and sanitized fixtures while preserving the cutover authorization blocker after the bounded V1-G61 proof. Arc-Bot-shell smoke evidence is current compatibility evidence only. Arc-Bot-shell clean-checkpoint proof is recorded in `docs/audits/V1_ARC_BOT_SHELL_CLEAN_CHECKPOINT_PROOF.md` at clean pushed commit `99a4ba4955f13626c2176a2c44592000029a16c3`; it is release-gate input evidence only and does not authorize release-candidate acceptance, branch, tag, cutover, product readiness, or production readiness.

The current validation refresh records focused current-gate/release-readiness validation as passing with 153 tests and the full LIMA suite passing with 5350 tests. A later 2026-06-21 LIMA-only validation supplement in the same audit records 37 focused G61 guard/operator/freshness tests, 147 focused V1 readiness regression tests, full LIMA suite validation with 5359 tests, diff hygiene, and protected runtime/dependency/support path status as clean; it does not claim Sparkbot or Arc-Bot-shell checkpoints were rerun. The latest 2026-06-21 LIMA readiness freshness supplement in the same validation refresh records 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, full LIMA suite validation with 5361 tests, diff hygiene, and protected runtime/dependency/support path status as clean; it also does not claim Sparkbot or Arc-Bot-shell checkpoints were rerun or create release, cutover, final-readiness, or G61 implementation authority. The latest 2026-06-21 handoff freshness supplement in the same validation refresh records 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, full LIMA suite validation with 5362 and 5364 tests, diff hygiene, and protected runtime/dependency/support path status as clean; it also does not claim Sparkbot or Arc-Bot-shell checkpoints were rerun or create release, cutover, final-readiness, Arc clean-checkpoint, consumer production integration, or G61 implementation authority. The candidate harness quickstart execution audit now records same-turn consumer smoke refresh evidence with public Sparkbot, accessible Sparkbot, and Arc-Bot-shell each passing 8 tests, plus post-refresh LIMA validation passing 17 focused quickstart/handoff tests, 108 broader V1 harness/readiness tests, and 5360 full-suite tests. The post-validation readiness-change freshness audit records that later readiness docs, fixtures, or tests require same-turn focused, full-suite, and diff-check evidence before they can support any future final-readiness pass. It records current same-turn full-suite freshness evidence passing 5359 tests after release/cutover freshness checks, latest quickstart post-refresh full-suite evidence passing 5360 tests, latest final blocker/index refresh evidence passing 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests, latest post-G61 request readiness-refresh supplement evidence passing 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests, and latest quickstart artifact refresh evidence passing 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests. The release-candidate checklist, cutover runbook, and final readiness audit template all require current validation refresh evidence, post-validation freshness evidence, and recorded clean Arc-Bot-shell checkpoint proof before any future V1.0.0 release-candidate branch, tag, cutover, or readiness claim.

Current machine-checkable freshness evidence: latest final blocker/index refresh evidence passing 15 focused final blocker/index tests, 89 broader affected V1 readiness tests, and 5361 full-suite tests; latest post-G61 request readiness-refresh supplement evidence passing 8 focused post-G61 request-refresh tests, 117 broader G61/readiness tests, and 5362 full-suite tests; latest quickstart artifact refresh evidence passing 7 focused candidate harness quickstart tests, 64 adjacent harness/readiness tests, 133 broader G61/readiness tests, and 5364 full-suite tests.

The V1 consumer target state after Arc readiness integration is recorded in `docs/readiness/V1_CONSUMER_TARGET_STATE_AFTER_ARC_READINESS_INTEGRATION.md`. It accepts Arc-Bot-shell runtime gating readiness integration as consumer-side testing evidence and records the saved `Sparkbot_shell` preview state. The former public Sparkbot G56 GitHub 403 publication blocker is resolved in `docs/audits/V1_PUBLIC_SPARKBOT_G56_PUBLICATION_RESOLUTION_AUDIT.md`.

`V1-G60` is complete as approved dependency declaration and vendor provider SDK import-boundary evidence. It adds `openai>=1.0.0,<3.0.0` to `pyproject.toml` only. G60 is `CANDIDATE_ONLY`; it does not edit a lockfile, add runtime vendor SDK imports in `lima/`, prove installed runtime import execution, add LIMA-owned provider SDK clients, construct provider clients, resolve endpoints, perform DNS/HTTP/socket/network calls, perform direct provider egress, read secrets, access credential values, change provider configuration, execute fallback, wire consumer production runtime integration, or claim product readiness.

Traceability note: the V1-G57 provider execution hardening authorization approval request has since been implemented and audited as completed candidate-only evidence in the path from the G56 consumer smoke proof to the G60 dependency declaration.

The active next V1 lane is recording exactly one valid cutover operator choice in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md`, if the operator approves. Do not edit lockfiles, add runtime vendor SDK imports in `lima/`, add built-in provider SDK clients, construct provider clients, resolve provider endpoints, make LIMA-owned network calls, read secrets, access credential values, change provider configuration, execute fallback, wire consumer production runtime behavior, or claim V1/product/production readiness from the completed import proof.

Existing V1 candidate slices remain non-production evidence only. The completed G60 dependency declaration does not authorize runtime import execution, built-in SDK clients, LIMA-owned network, credential, connector, browser, file, device, robotics, physical-world behavior, final API freeze, or production use.

The V1.0.0 release-candidate acceptance checklist is satisfied for first-consumer harness testing; the cutover runbook remains blocked by explicit operator authorization. Do not create a V1.0.0 release-candidate branch, release tag, cutover claim, or readiness claim until `Approve-V1-RC-Cutover` is recorded in `docs/readiness/V1_RELEASE_CANDIDATE_CUTOVER_AUTHORIZATION_PACKET.md` and the runbook confirms checklist/reconciliation evidence remains current.

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

Phase 8.0 opens a no-code Implementation Design Review lane. It converts the Phase 7 charter into a design package for a future non-executing kernel intake-to-candidate coordinator, but does not approve runtime implementation or modify `lima/`, `tests/support/`, Sparkbot wiring, execution, approval enforcement, audit persistence, or physical-world behavior.

Phase 8.1 adds a docs/tests/fixtures-only Exact Runtime File-Touch Map. It identifies future-eligible contract files and proposed new kernel files for a later explicitly approved first runtime slice, while keeping every `lima/` and `tests/support/` file untouched.

Phase 8.2 adds docs/tests/fixtures-only Runtime Acceptance Test Design. It defines future required test families, negative cases, limited positive cases, and validation expectations before any runtime slice can be approved.

Phase 8.3 adds docs/tests/fixtures-only Rollback / Audit Proof Plan. It defines future revertibility, forbidden-path review, audit-proof evidence, success criteria, and failure criteria before any runtime code can be approved.

Phase 8.4 closes the no-code Phase 8 implementation design review lane at a runtime implementation approval gate. It defines the exact future approval question for a narrow Phase 9 non-executing kernel intake-to-candidate coordinator and keeps runtime implementation blocked until Phil explicitly approves that scope.

Phase 8.5 archives Phase 8 as no-code implementation design review work. It confirms Phase 8.0 through Phase 8.4 added docs, fixtures, static tests, and roadmap/state updates only, preserves the exact Phase 9 approval question, and keeps runtime code gated pending explicit Phil approval.

Phase 9.0 confirms the Phase 8.1 eligible runtime file-touch map before runtime implementation work begins. It is docs/tests/fixtures only and allows the lane to continue to Phase 9.1 acceptance test scaffolding without modifying `lima/`.

Phase 9.1 scaffolds the acceptance-test obligations for the first Phase 9 runtime slice. It remains docs/tests/fixtures only and does not modify `lima/`; the next approved step is the narrow non-executing kernel intake-to-candidate coordinator implementation.

Phase 9.2 adds that narrow coordinator under `lima/kernel/`. It is pure, in-process, non-executing, accepts only synthetic already-normalized intake metadata, and returns candidate metadata with execution, side effects, approval authority, IntentEnvelope creation, and GuardianDecision creation all disabled.

Phase 9.3 reviews the coordinator as ready only for Phase 9.4 audit/archive closeout or further non-runtime review. It does not approve runtime expansion.

Phase 9.4 archives Phase 9 as the first narrow runtime slice lane. The only runtime files added in Phase 9 are `lima/kernel/__init__.py` and `lima/kernel/intake_candidate.py`; the slice remains non-executing candidate metadata only and Phase 10 requires explicit Phil approval.

Phase 9.5 archives the completed first runtime slice after a dedicated Phase 9.0-9.4 audit. It preserves the acceptable Phase 8.1 test-update warning and keeps Phase 10 gated.

Phase 10.0 opens the no-code next-runtime-slice design lane with a post-Phase-9 review. It records what the first runtime slice proved, what it did not prove, and keeps Phase 11 runtime implementation unapproved.

Phase 10.1 evaluates candidate validation, status normalization, lifecycle metadata, intake error taxonomy, provenance hardening, and stopping with no further runtime work. It recommends a future candidate validation plus status normalization slice for Phase 11 consideration only, with implementation still unapproved.

Phase 10.2 maps the exact future file-touch surface for that possible Phase 11 slice. It names only `lima/kernel/intake_candidate.py`, `lima/kernel/__init__.py`, and a possible new `lima/kernel/candidate_status.py` as future-eligible, while keeping all runtime implementation unapproved.

Phase 10.3 defines the future acceptance tests, rollback plan, and audit proof required before that possible Phase 11 slice can be implemented. It remains docs/tests/fixtures only and keeps runtime expansion unapproved.

Phase 10.4 closes the Phase 10 no-code design lane at a runtime expansion approval gate. It preserves the exact Phase 11 approval question for a narrow candidate validation/status normalization slice and keeps Phase 11 blocked until Phil explicitly approves it.

Phase 10.5 archives Phase 10 as a completed no-code next-runtime-slice design lane. It confirms no `lima/` changes, no `candidate_status.py`, no runtime behavior, and keeps Phase 11 gated pending explicit Phil approval.

Phase 11.0 opens the approved Phase 11 runtime slice lane with a docs/tests/fixtures-only preflight audit. It confirms the Phase 10.2 eligible runtime files are explicit and that `lima/kernel/candidate_status.py` is still absent before implementation.

Phase 11.1 scaffolds the candidate status and validation acceptance-test obligations for Phase 11.2 and Phase 11.3. It remains docs/tests/fixtures only and adds no runtime behavior.

Phase 11.2 implements candidate status normalization under `lima/kernel/candidate_status.py` and safe exports in `lima/kernel/__init__.py`. It remains pure, in-process, non-executing, and authority-free.

Phase 11.3 implements candidate validation in the same approved kernel-local scope. It fail-closes malformed or authority-bearing candidate metadata while preserving non-executing guarantees and the Phase 5 runtime bridge gate.

Phase 11.4 reviews the Phase 11 runtime slice after status normalization and validation. It is docs/tests/fixtures only, confirms no new runtime behavior, and keeps Phase 11.5 as archive-only before any Phase 12 decision.

Phase 11.5 archives Phase 11 as a completed narrow runtime slice. It confirms only `lima/kernel/candidate_status.py` and `lima/kernel/__init__.py` were touched as runtime files, preserves the non-executing guarantees, and gates Phase 12 pending explicit Phil approval.

Phase 12.0 opens a docs/tests/fixtures-only planning lane after the Phase 11 runtime slice. It reviews the completed candidate status work and compares safe next directions without modifying runtime code.

Phase 12.1 compares pause, future runtime design, Sparkbot boundary planning, Robo-OS boundary planning, and threat-model strengthening. It recommends continuing to threat-model and safety-gap review before any next lane is selected.

Phase 12.2 reviews threat-model and safety gaps across runtime expansion, Sparkbot boundary planning, Robo-OS physical-world planning, and pause options. It recommends a machine-checkable next-lane recommendation matrix before any implementation.

Phase 12.3 records the next-lane recommendation matrix. It recommends a docs/tests/fixtures-only threat-model-derived test planning lane as the safest next step and defers runtime, Sparkbot, and Robo-OS work.

Phase 12.4 closes Phase 12 at a decision gate. It preserves the Phase 13 approval question for a docs/tests/fixtures-only threat-model-derived test planning lane and stops before any runtime or integration work.

Phase 13.0 opens the approved threat-model-derived test planning lane. It converts Phase 12.2 threats into planned static checks, contract checks, fixture requirements, and future acceptance gates without runtime changes.

Phase 13.1 defines future static forbidden-pattern test requirements for imports, calls, boundary names, and behavior claims that could imply execution, approval, persistence, Sparkbot wiring, live adapters, or physical-world action.

Phase 13.2 defines future runtime contract test requirements for non-executing candidate invariants: execution and side-effect flags remain false, approval never becomes approved, provenance is preserved, and malformed/unknown/stale/replayed inputs remain safe.

Phase 13.3 defines future synthetic threat fixture families for malformed, unknown, stale/replayed, approval-bypass, shell/network/browser/file/robotics, Sparkbot, and HumanInput bridge attempts.

Phase 13.4 closes Phase 13 at a future acceptance gate. It recommends Phase 14 as docs/tests/fixtures-only acceptance-gate test design and stops before any runtime or integration work.

Phase 14.0 opens the approved acceptance-gate test design lane. It converts Phase 13 requirements into concrete future test names and expected assertions without implementing tests or touching runtime code.

Phase 14.1 designs future static forbidden-pattern tests for forbidden imports, calls, side-effect patterns, boundary names, and authority claims while adding no scanner implementation.

Phase 14.2 designs future runtime contract tests for non-executing candidate invariants: execution and side-effect flags remain false, approval never becomes approved, provenance is preserved, and malformed/unknown/stale/replayed inputs remain safe.

Phase 14.3 designs future fixture-based acceptance tests for malformed candidates, unknown statuses, stale/replayed candidates, approval-bypass wording, shell/network/browser/file/robotics attempts, Sparkbot integration attempts, and HumanInput bridge attempts.

Phase 14.4 closes Phase 14 at a Phase 15 decision gate. It preserves the future acceptance-gate requirements and recommends a docs/tests/fixtures-only Phase 15 proposal/readiness lane before any test implementation, runtime, or integration work.

Phase 15.0 opens the approved acceptance-gate implementation proposal/readiness lane. It reviews Phase 14 and defines future proposal outputs without implementing acceptance tests.

Phase 15.1 proposes the future static forbidden-pattern test implementation package, including file names, test names, assertions, and scanner constraints, without adding scanners or tests.

Phase 15.2 proposes the future runtime contract acceptance-test implementation package for candidate invariants without adding tests or touching runtime code.

Phase 15.3 proposes the future threat fixture acceptance-test implementation package and synthetic fixture names without adding those fixtures or tests.

Phase 15.4 closes Phase 15 at a Phase 16 decision gate. It marks the proposed package ready only for a later explicitly approved test-only implementation lane and keeps runtime, `lima/`, `tests/support`, Sparkbot, HumanInput bridge, live adapter, execution, dispatch, persistence, and physical-world work blocked.

Phase 16.0 opens the approved test-only acceptance-gate implementation lane while keeping runtime, `lima/`, and `tests/support` changes blocked.

Phase 16.1 adds static forbidden-pattern acceptance tests against the existing non-executing kernel candidate files.

Phase 16.2 adds runtime contract acceptance tests against existing non-executing candidate APIs, proving execution and side-effect flags remain false, approval never becomes approved, provenance is preserved, and unsafe inputs fail closed.

Phase 16.3 adds synthetic threat fixture acceptance tests for malformed, unknown, stale/replayed, approval-bypass, shell/network/browser/file/robotics, Sparkbot, and HumanInput bridge attempts.

Phase 16.4 reviews the test-only acceptance implementation as ready for archive/closeout.

Phase 16.5 archives Phase 16 as a completed test-only acceptance-gate lane and stops before Phase 17 or any runtime expansion.

Phase 17.0 opens the acceptance-gate audit/archive and next-lane decision phase. It audits Phase 16.0 through Phase 16.5 as test-only work and keeps runtime, `lima/`, `tests/support`, Sparkbot, HumanInput bridge, live adapter, execution, dispatch, persistence, and physical-world work blocked.

Phase 17.1 reviews Phase 16 acceptance-test coverage and records that the tests strengthen the gate while remaining limited to static, contract, and synthetic fixture coverage.

Phase 17.2 reviews remaining safety gaps before any next lane, including narrow future file coverage, non-enforcing approval semantics, synthetic-only fixture limits, and continued blocking of Sparkbot, HumanInput bridge, live adapter, audit persistence, and physical-world work.

Phase 17.3 compares Phase 18 options and recommends test-only regression hardening as the safest active next lane before runtime expansion.

Phase 17.4 archives Phase 17 as a completed acceptance-gate audit/archive lane and preserves the Phase 18 approval question for a test-only regression hardening lane.

Phase 18.0 opens the approved test-only regression hardening lane for existing non-executing candidate APIs and acceptance-gate boundaries. It keeps runtime, `lima/`, `tests/support`, Sparkbot, HumanInput bridge, live adapter, execution, dispatch, persistence, and physical-world work blocked.

Phase 18.1 adds candidate API regression tests against existing non-executing APIs, proving candidates remain non-executable, authority-free, provenance-preserving, and safe for malformed, unknown, stale/replayed, dangerous wording, and raw HumanInput-like inputs.

Phase 18.2 adds synthetic acceptance-boundary regression fixtures for approval-bypass wording, shell/browser/network/file/robotics attempts, Sparkbot integration attempts, HumanInput runtime bridge attempts, stale/replayed candidates, malformed candidates, and unknown statuses.

Phase 18.3 adds forbidden integration regression tests that scan existing candidate runtime files for forbidden imports, calls, side-effect patterns, and integration wiring names without adding runtime enforcement.

Phase 18.4 reviews the regression hardening package as ready for archive while still not ready for runtime implementation, `lima/`, `tests/support`, Sparkbot, HumanInput bridge, live adapter, execution, dispatch, persistence, or physical-world work.

Phase 18.5 archives Phase 18 as a completed test-only regression hardening lane and preserves the Phase 19 approval question for a docs/tests/fixtures-only audit/archive and next-lane decision phase.

Phase 19.0 opens the acceptance-gate audit/archive lane for the Phase 18 regression hardening package, while keeping runtime, `lima/`, `tests/support`, Sparkbot, HumanInput bridge, live adapter, execution, dispatch, persistence, and physical-world work blocked.

Phase 19.1 reviews Phase 18 regression coverage and records that the coverage is meaningful but still test-only; it does not create runtime enforcement or approve Phase 20.

Phase 19.2 records remaining regression gaps after Phase 18: static checks are not runtime monitors, fixtures are synthetic, future integration behavior still needs separate design, and direct runtime expansion remains blocked.

Phase 19.3 evaluates the approved Phase 20 options and recommends a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice, without approving Phase 20 implementation.

Phase 19.4 archives Phase 19 as complete and preserves the exact Phase 20 approval question. Phase 20 remains unapproved and runtime expansion remains blocked.

Phase 20.0 opens Phase 20 as a docs/tests/fixtures-only no-code design lane for the next narrow runtime slice, using Phase 18 regression coverage and Phase 19 audit findings without modifying runtime code.

Phase 20.1 compares next-slice options and recommends candidate provenance hardening as the only future runtime slice to carry forward, without approving Phase 21 or implementation.

Phase 20.2 defines the exact future file-touch map for that candidate provenance slice: only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py` would be eligible in a later explicitly approved runtime phase.

Phase 20.3 defines future acceptance tests and rollback/audit proof for the candidate provenance slice, while still not implementing those tests or touching runtime code.

Phase 20.4 archives Phase 20 as a completed no-code design lane and preserves the exact Phase 21 approval question for a narrow candidate provenance hardening runtime slice. Phase 21 remains unapproved.

Phase 20.5 archives Phase 20 as a completed no-code design package before any Phase 21 runtime decision. It adds no runtime behavior and keeps Phase 21 gated.

Phase 21.0 opens the approved candidate provenance hardening runtime slice with preflight confirmation that only `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py` are eligible runtime files.

Phase 21.1 scaffolds deterministic candidate provenance acceptance tests and fixtures before runtime implementation. It changes no runtime code and keeps Phase 21.2 limited to the two approved runtime files.

Phase 21.2 implements the narrow candidate provenance hardening slice inside `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py` only. Runtime remains non-executing, side-effect-free, approval-free, and dispatch-free.

Phase 21.3 reviews the candidate provenance hardening slice as regression-only docs/tests/fixtures work. It adds no runtime changes and preserves the Phase 21.2 boundaries.

Phase 21.4 marks the candidate provenance hardening runtime slice ready for archive closeout. It adds no runtime changes and keeps Phase 22 gated.

Phase 21.5 archives Phase 21 as a completed narrow runtime slice. The only runtime files touched by the lane were `lima/kernel/intake_candidate.py` and `lima/kernel/candidate_status.py`; Phase 22 remains gated.

Phase 22.0 opens the approved docs/tests/fixtures-only no-code decision lane after Phase 21. It audits the provenance hardening slice and lists possible Phase 23 directions without implementing anything.

Phase 22.1 reviews candidate provenance coverage and identifies test-only gaps for nested provenance and static guardrails. It adds no runtime behavior.

Phase 22.2 reviews remaining safety gaps and finds they are best handled by test-only hardening before any future runtime expansion.

Phase 22.3 compares next-lane options and recommends Phase 23 as test-only hardening for provenance and candidate invariants.

Phase 22.4 closes the Phase 22 no-code decision lane and preserves the exact Phase 23 approval question. Phase 23 remains gated.

Phase 23.0 opens the approved test-only hardening lane for provenance and candidate invariants. It adds no runtime behavior and keeps `lima/` and `tests/support/` unchanged.

Phase 23.1 adds deterministic candidate provenance regression tests for valid, missing, malformed, stale, and replayed provenance behavior. It changes no runtime code.

Phase 23.2 adds synthetic suspicious provenance fixtures covering authority claims in values, keys, nested mappings, lists, and risky action metadata. It changes no runtime code.

Phase 23.3 adds explicit bypass-wording provenance tests covering Phil, operator, admin, trusted, urgent, override, approve, and emergency wording. It changes no runtime code.

Phase 23.4 reviews Phase 23.0 through Phase 23.3 as ready for archive/closeout. It changes no runtime code.

Phase 23.5 archives Phase 23 as a completed test-only hardening lane and preserves Phase 24 as a docs/tests/fixtures-only next-lane decision gate. It changes no runtime code.

Phase 24.0 opens the approved docs/tests/fixtures-only audit/archive and next-lane decision phase for the Phase 23 test-only hardening package. It changes no runtime code.

Phase 24.1 reviews Phase 23 provenance and candidate-invariant coverage as deterministic offline test protection. It changes no runtime code.

Phase 24.2 identifies remaining provenance and candidate-invariant gaps as planning inputs only. It changes no runtime code.

Phase 24.3 recommends Phase 25 as additional test-only hardening for a cross-API candidate invariant matrix. It changes no runtime code.

Phase 24.4 archives Phase 24 as a completed docs/tests/fixtures-only audit lane and preserves Phase 25 as an explicit test-only hardening gate. It changes no runtime code.

Phase 25.0 opens the approved test-only hardening lane for a cross-API candidate invariant matrix. It changes no runtime code.

Phase 25.1 adds synthetic matrix fixtures for existing candidate API invariant checks. It changes no runtime code.

Phase 25.2 adds deterministic cross-API non-execution invariant tests for existing candidate-facing APIs. It changes no runtime code.

Phase 25.3 adds deterministic provenance and status invariant tests across existing candidate-facing APIs. It changes no runtime code.

Phase 25.4 reviews the cross-API candidate invariant hardening package as ready for archive/closeout. It changes no runtime code.

Phase 25.5 archives Phase 25 as a completed test-only cross-API candidate invariant hardening lane and preserves Phase 26 as a docs/tests/fixtures-only audit/archive decision gate. It changes no runtime code.

Phase 26.0 opens the approved docs/tests/fixtures-only audit/archive and next-lane decision lane for the Phase 25 cross-API candidate invariant hardening package. It changes no runtime code.

Phase 26.1 reviews Phase 25 cross-API candidate invariant coverage across construction, status normalization, validation, and provenance hardening. It changes no runtime code.

Phase 26.2 records remaining cross-API candidate invariant gaps as planning inputs only. It changes no runtime code.

Phase 26.3 recommends Phase 27 as a docs/tests/fixtures-only preservation and roadmap decision lane to pause and preserve the current runtime/test state. It changes no runtime code.

Phase 26.4 archives Phase 26 as a completed docs/tests/fixtures-only audit/archive lane and preserves Phase 27 as an explicit preservation and roadmap decision gate. It changes no runtime code.

Phase 27.0 opens the approved docs/tests/fixtures-only preservation and roadmap decision lane after the Phase 26 archive. It changes no runtime code.

Phase 27.1 records the current known-good runtime/test state and preserves the constrained non-executing candidate APIs before any future expansion decision. It changes no runtime code.

Phase 27.2 reviews the gated runtime and integration boundaries that remain blocked after Phase 26. It changes no runtime code.

Phase 27.3 recommends Phase 28 as a docs/tests/fixtures-only preservation status review to continue pausing and preserving the current runtime/test state. It changes no runtime code.

Phase 27.4 archives Phase 27 as a completed docs/tests/fixtures-only preservation lane and preserves Phase 28 as an explicit preservation status review gate. It changes no runtime code.

Phase 28.0 opens the approved docs/tests/fixtures-only preservation status review and explicitly prevents an endless preservation loop by requiring a sharper Phase 29 decision gate. It changes no runtime code.

Phase 28.1 confirms the current runtime/test state remains stable and preserved, with no concrete immediate test-only hardening gap found. It changes no runtime code.

Phase 28.2 finds that continued pause is safe but no longer the sharpest default recommendation; Phase 29 should be a docs/tests/fixtures-only no-code design review for the next narrow runtime slice. It changes no runtime code.

Phase 28.3 recommends Phase 29 as a docs/tests/fixtures-only no-code design review for the next narrow runtime slice, not runtime implementation. It changes no runtime code.

Phase 28.4 archives Phase 28 as a completed preservation status review and preserves Phase 29 as an explicit docs/tests/fixtures-only no-code design review gate. It changes no runtime code.

Phase 29.0 opens the approved docs/tests/fixtures-only no-code design review for the next narrow runtime slice. It changes no runtime code.

Phase 29.1 recommends a future read-only runtime state inspection slice as the safest next narrow runtime candidate for detailed no-code boundary design. It changes no runtime code.

Phase 29.2 defines the no-code safety boundary for a future read-only runtime state inspection slice. It changes no runtime code.

Phase 29.3 defines future implementation eligibility criteria, acceptance-test expectations, rollback/audit proof, and the exact Phase 30 approval question for a possible read-only runtime state inspection slice. It changes no runtime code.

Phase 29.4 archives Phase 29 as a completed docs/tests/fixtures-only no-code design review and keeps Phase 30 blocked pending explicit Phil approval. It changes no runtime code.

Phase 30.0 opens the explicitly approved narrow runtime implementation lane by auditing Phase 29 and confirming the allowed runtime scope before runtime files are touched. It changes no runtime code.

Phase 30.1 defines acceptance and regression coverage for the approved read-only runtime state inspection slice before implementation. It changes no runtime code.

Phase 30.2 implements the approved read-only runtime state inspection slice in `lima/kernel/runtime_state.py` with a safe public export from `lima/kernel/__init__.py`. It remains local-only, non-authoritative, non-executing, read-only, and side-effect-free.

Phase 30.3 reviews the Phase 30.2 runtime state inspection boundary and confirms the slice remains deterministic, local-only, read-only, non-authoritative, non-executing, and side-effect-free. It changes no runtime code.

Phase 30.4 archives Phase 30 as the completed narrow read-only runtime state inspection slice and stops at the Phase 31 gate. It changes no runtime code.

Phase 31.0 opens the docs/tests/fixtures-only audit/archive lane for the completed Phase 30 runtime slice and records the Phase 30 audit result. It changes no runtime code.

Phase 31.1 records evidence that the Phase 30 runtime state inspection slice remains deterministic, local-only, read-only, non-authoritative, non-executing, and side-effect-free. It changes no runtime code.

Phase 31.2 reviews Phase 30 regression coverage and remaining gaps, finding no blocking safety regression and recommending Phase 32 not default to implementation. It changes no runtime code.

Phase 31.3 recommends Phase 32 as a docs/tests/fixtures-only design review for the next narrow runtime slice, not runtime implementation. It changes no runtime code.

Phase 31.4 archives Phase 31 as the completed docs/tests/fixtures-only audit/archive for the Phase 30 runtime slice and stops at the Phase 32 gate. It changes no runtime code.

Phase 32.0 opens the docs/tests/fixtures-only design review for the next narrow runtime slice and records the Phase 31 audit result. It changes no runtime code.

Phase 32.1 inventories candidate next lanes and recommends Phase 33 as test-only `runtime_state` hardening with nested suspicious metadata fixtures, not runtime implementation.

Phase 32.2 compares next-slice safety and scope and confirms that no immediate Phase 33 runtime implementation is recommended.

Phase 32.3 defines the Phase 33 eligibility and test plan matrix, preserving an exact test-only hardening approval question for Phil.

Phase 32.4 archives Phase 32 as a completed docs/tests/fixtures-only design review and stops at the Phase 33 test-only hardening approval gate.

Phase 33.0 opens the approved test-only hardening lane for the existing read-only `runtime_state` inspection slice and records the Phase 32 audit result.

Phase 33.1 adds synthetic nested suspicious metadata fixtures for `runtime_state` hardening without changing runtime code.

Phase 33.2 adds regression tests proving nested suspicious metadata remains deterministic, read-only, non-authoritative, non-executing, and side-effect free under the existing `runtime_state` API.

Phase 33.3 recommends Phase 34 as docs/tests/fixtures-only audit/archive for the Phase 33 hardening package, not runtime implementation.

Phase 33.4 archives Phase 33 as completed test-only `runtime_state` hardening and stops at the Phase 34 audit/archive approval gate.

Phase 34.0 opens the docs/tests/fixtures-only audit/archive lane for the completed Phase 33 hardening package and records the Phase 33 audit result.

Phase 34.1 reviews nested metadata coverage evidence and confirms Phase 33 hardening remained test-only and inert.

Phase 34.2 reviews runtime_state hardening gaps and finds no concrete gap, no runtime change need, and no immediate additional test-only hardening need.

Phase 34.3 recommends Phase 35 as docs/tests/fixtures-only no-code design review for a possible second narrow runtime slice, not implementation.

Phase 34.4 archives Phase 34 as completed docs/tests/fixtures-only audit/archive and stops at the Phase 35 no-code design review approval gate.

Phase 35.0 opens the docs/tests/fixtures-only no-code design review lane for a possible second narrow runtime slice and records the Phase 34 audit result.

Phase 35.1 inventories second runtime slice options and carries forward a future-only non-executing candidate preview helper as the leading design candidate, without implementation.

Phase 35.2 compares second-slice safety and scope and recommends the future candidate preview helper only for a later explicit Phase 36 approval question.

Phase 35.3 defines Phase 36 eligibility criteria, acceptance-test requirements, rollback/audit proof, stop conditions, and the exact future approval question for Phil.

Phase 35.4 archives Phase 35 as completed docs/tests/fixtures-only no-code design review and stops at the Phase 36 explicit approval gate.

Phase 36.0 opens the explicitly approved narrow candidate preview runtime implementation lane with a Phase 35 audit PASS and no runtime implementation yet.

Phase 36.1 defines candidate preview acceptance requirements and static boundary checks before implementation, with no runtime code added.

Phase 36.2 adds the approved `candidate_preview` runtime helper and safe kernel export. The helper is local-only, read-only, non-authoritative, non-executing, side-effect free, and accepts caller-provided data only.

Phase 36.3 reviews the candidate preview boundary and confirms Phase 36.2 changed only approved runtime files, with no additional runtime behavior.

Phase 36.4 archives Phase 36 as a completed narrow candidate preview runtime slice and stops at the Phase 37 audit/archive approval gate.

Phase 37.0 opens the docs/tests/fixtures-only audit/archive lane for the completed Phase 36 candidate preview runtime slice and records the Phase 36 audit result.

Phase 37.1 reviews candidate preview boundary evidence and confirms the Phase 36 helper remains non-authoritative, non-executing, bridge-inactive, adapter-inactive, and side-effect free.

Phase 37.2 reviews candidate preview regressions and gaps, finding no blocking gap and no immediate test-only hardening need.

Phase 37.3 recommends pausing and preserving the current runtime/test state after Phase 37.4 rather than starting another automatic lane.

Phase 37.4 archives Phase 37 as a completed docs/tests/fixtures-only candidate preview audit lane. It finds no remaining gap and recommends pausing and preserving the current runtime/test state with no Phase 38 approval question required by this closeout.

Phase 38.0 opens a docs/tests/fixtures-only Sparkbot v1.6.80 alignment intake lane after a Phase 37 audit PASS. Sparkbot is reviewed as read-only source material only; no Sparkbot wiring, LIMA runtime change, or integration behavior is approved.

Phase 38.1 records the Sparkbot v1.6.42-to-v1.6.80 concept delta and carries forward local-first, Command Center, owner-local, strict Security, policy simulation, persistent approval, agent identity, memory trust, Guardian Spine, MCP/Robo OS, and audit vocabulary as LIMA planning metadata only.

Phase 38.2 defines Sparkbot-shaped LIMA consumer boundary vocabulary for posture, action class, risk, approval posture, dry-run posture, run state, agent identity, memory trust, connector health, robotics posture, and audit surfaces while keeping every term non-authoritative and non-executing.

Phase 38.3 compares Sparkbot v1.6.80 concepts against current LIMA runtime slices and recommends Phase 39 as test-only `candidate_preview` hardening with Sparkbot-shaped fixtures, not implementation.

Phase 38.4 archives the Sparkbot alignment intake lane. It confirms no LIMA runtime files, Sparkbot files, or `tests/support/` files changed, and recommends Phase 39 as docs/tests/fixtures-only `candidate_preview` hardening with Sparkbot-shaped fixtures.

Phase 39.0 opens the test-only `candidate_preview` hardening lane for Sparkbot-shaped caller-provided fixtures. It does not approve runtime implementation or `lima/` changes.

Phase 39.1 adds inert Sparkbot-shaped caller-provided fixture data for owner-local reads, strict-security writes, breakglass/Vault, MCP explain-plan, Robo OS simulation, real hardware motion, kill-switch agent identity, and low-confidence memory write cases.

Phase 39.2 adds regression tests proving the existing `candidate_preview` helper keeps every Sparkbot-shaped fixture blocked, non-authoritative, non-executing, approval-free, dispatch-free, persistence-free, bridge-inactive, and side-effect free.

Phase 39.3 reviews the hardening result, finds no runtime gap, and recommends only Phase 39.4 archive/closeout followed by pause and preserve.

Phase 39.4 archives the Sparkbot-shaped `candidate_preview` hardening lane. It finds no remaining gap, no need for runtime changes, and recommends pausing and preserving the current runtime/test state.

Phase 40.0 clarifies that Sparkbot v1.6.80 is reference evidence for product/control vocabulary, not the direct future consumer to wire next. Arc Bot / LIMA AI Office is recorded as the primary guarded task-oriented office consumer for the next boundary-planning thread, with stricter defaults than Sparkbot's owner-local workstation posture.

Phase 40.1 defines Arc Bot / LIMA AI Office as a guarded task-oriented office consumer boundary over LIMA AI OS/runtime safety concepts, explicitly not a Sparkbot clone, workstation surface, HumanInput bridge, approval executor, dispatch system, or physical-world controller.

Phase 40.2 records the LIMA Office task, approval, audit, connector, memory-trust, scheduled-work, and physical-world vocabulary matrix. Sparkbot remains reference evidence only; Arc Bot / LIMA AI Office keeps stricter defaults and planning labels do not grant runtime authority.

Phase 40.3 defines the Arc Bot-shaped `candidate_preview` fixture plan for a future test-only hardening lane. The plan covers draft-only email, external send, calendar write, file mutation, low-confidence memory, connector setup, kill switch, scheduled work, admin breakglass, robotics, Sparkbot-only behavior, strict-security posture, and explain-plan-only cases without approving implementation.

Phase 40.4 archives Phase 40 as a completed Arc Bot / LIMA Office consumer boundary review. Sparkbot remains reference evidence only, Arc Bot / LIMA Office remains the primary guarded task consumer, and Phase 41 is recommended as docs/tests/fixtures-only Arc Bot-shaped `candidate_preview` hardening.

Phase 41.0 opens a docs/tests/fixtures-only test-hardening lane for the existing `candidate_preview` helper using Arc Bot / LIMA Office-shaped task fixtures. No runtime implementation or `lima/` changes are approved.

Phase 41.1 adds the Arc Bot-shaped synthetic fixture corpus for `candidate_preview` hardening, including safe draft-only work, external writes, connector setup, memory trust, scheduled work, admin posture, Sparkbot-only behavior, and robotics/physical-world cases.

Phase 41.2 adds regression tests proving the existing `candidate_preview` helper keeps Arc Bot-shaped office fixtures deterministic, non-authoritative, read-only, non-executing, approval-free, dispatch-free, persistence-free, bridge-inactive, adapter-inactive, Sparkbot-wiring inactive, external-call inactive, robotics inactive, and physical-world inactive.

Phase 41.3 reviews the Arc Bot-shaped hardening results and finds no concrete runtime gap. Existing conservative blocking of suspicious planning keys is accepted as safe, and Phase 41.4 is recommended as docs/tests/fixtures-only archive closeout.

Phase 41.4 archives the Arc Bot-shaped `candidate_preview` hardening lane. It confirms no runtime gap, no `lima/` changes, no `tests/support/` changes, and recommends a future docs/tests/fixtures-only no-code Arc Bot / LIMA Office consumer contract design review rather than implementation.

Phase 42.0 reframes the next lane around LIMA AI OS as the universal, model-agnostic, consumer-agnostic, embodiment-agnostic runtime contract target. Arc Bot / LIMA Office is preserved as an example guarded office-agent consumer profile, Sparkbot Public is framed as an open-source showcase shell and reference evidence, and paid/proprietary LIMA robotics/IoT unlocks are separated from the public contract surface.

Phase 42.1 defines universal model-agnostic planning contracts for input, task/intent, candidate action preview, approval posture description, telemetry/evidence references, and embodiment/profile metadata. These are docs/tests/fixtures-only contract descriptions, not runtime schemas or authority grants.

Phase 42.2 defines the universal consumer and embodiment profile taxonomy for LIMA AI OS, covering Arc Bot / LIMA Office, Sparkbot Public, generic chatbots, automation agents, coding/research agents, robot/drone/humanoid/IoT controllers, action classes, and adapter-boundary vocabulary. Robotics and IoT remain profile vocabulary only with no hardware calls.

Phase 42.3 records universal safety invariants and the Guardian boundary matrix. LIMA may describe approval posture, risk, evidence, simulation, and adapter requirements, but Guardian or a future policy membrane owns real approval state; LIMA cannot grant approval, execute, dispatch, persist, mutate, call adapters, or touch physical-world systems in this lane.

Phase 42.4 archives Phase 42 as a completed LIMA AI OS Universal Runtime Contract Design lane. The lane reframes Phase 42 away from Arc-centered planning, preserves Arc Bot as one example guarded office-agent profile, keeps Sparkbot Public as reference/showcase, separates public/private product surfaces, and recommends Phase 43 as docs/tests/fixtures-only Universal Contract Fixture Hardening.

Phase 43.0 opens the Universal Contract Fixture Hardening lane as a docs/tests/fixtures-only charter. It converts the Phase 42.4 recommendation into fixture-hardening scope for consumer profiles, embodiment/action profiles, and adversarial profile data while keeping runtime implementation, `lima/` changes, `tests/support/` changes, live adapters, approval enforcement, execution, dispatch, persistence, robotics, physical-world behavior, and hidden side effects blocked.

Phase 43.1 adds the inert universal contract profile fixture corpus. The cases cover safe consumer profiles, risky browser/shell/file/network/scheduled action profiles, IoT/drone/humanoid/robot/emergency-stop profiles, and adversarial profile data while preserving preview-only, non-authoritative, local-only, approval-free, non-executing, adapter-inactive, robotics-inactive, and physical-world-inactive boundaries.

Phase 43.2 adds regression tests over the Phase 43.1 universal profile fixtures using the existing `candidate_preview` helper. Risky, embodied, physical-world, and adversarial profile metadata stays blocked, while all preview outputs preserve deterministic, read-only, local-only, non-authoritative, non-executing, approval-free, dispatch-free, persistence-free, adapter-inactive, robotics-inactive, and physical-world-inactive flags.

Phase 43.3 reviews the Universal Contract Fixture Hardening lane and finds no concrete runtime gap. Conservative blocking is accepted as safe, and Phase 43.4 is recommended as docs/tests/fixtures-only archive closeout rather than runtime implementation.

Phase 43.4 archives Phase 43 as completed docs/tests/fixtures-only Universal Contract Fixture Hardening. It confirms no runtime gap, no `lima/` changes, no `tests/support/` changes, no Sparkbot wiring, no Arc Bot implementation, no live adapters, no approval enforcement, no execution, no dispatch, no persistence, no robotics, no physical-world behavior, and no hidden side effects. The next action is a merge/tag approval gate for the Phase 43 stack.

Phase 44.0 opens the typed IntentEnvelope / Guardian Request Bridge design charter as docs/tests/fixtures-only work. It defines the no-code path from HumanInput, shell, bot, or automation request metadata to a typed IntentEnvelope candidate and Guardian request, while keeping GuardianDecision creation, approval enforcement, execution, dispatch, persistence, model/tool/driver calls, adapters, robotics, physical-world behavior, and hidden side effects blocked.

Phase 44.1 adds the inert typed IntentEnvelope / Guardian request bridge fixture corpus as docs/tests/fixtures-only metadata. It locks source request metadata, typed intent candidate metadata, Guardian request metadata, and future GuardianDecision absent/pending/blocked states while preserving non-authoritative, non-executing, non-dispatching, non-persistent boundaries with no runtime implementation.

Phase 44.2 validates and gap-reviews the Phase 44.1 typed bridge fixture corpus as docs/tests/fixtures-only evidence work. It confirms source request metadata, typed IntentEnvelope candidate metadata, and Guardian request metadata coverage remains inert; Guardian request remains non-authoritative and not a GuardianDecision; no execution path exists; and no concrete runtime gap was found.

Phase 44.3 archives Phase 44.0 through Phase 44.2 as a completed no-code typed IntentEnvelope / Guardian request bridge lane. It confirms the design, fixture corpus, and validation/gap-review stack is complete as metadata-only work with no GuardianDecision authority, no execution path, and no runtime implementation recommendation.

Phase 45.0 opens a no-code typed bridge acceptance-test design lane. It defines the static test requirements that would be required before any future runtime bridge implementation could be considered, while keeping source request metadata, typed IntentEnvelope candidate metadata, Guardian request metadata, future GuardianDecision metadata, execution, dispatch, persistence, model/tool/driver calls, adapters, external calls, robotics, physical-world behavior, and hidden side effects unimplemented.

Phase 45.1 opens docs/tests/fixtures-only acceptance-test fixture matrix and scaffolding design for the future typed bridge slice. It maps positive and fail-closed case families into inert matrix metadata without creating runtime bridge behavior, test harness behavior, GuardianDecision records, approvals, execution, dispatch, persistence, adapter calls, model/tool/driver calls, external calls, or physical-world behavior.
Phase 45.2 opens docs/tests/fixtures-only acceptance-test matrix readiness review. It reviews whether Phase 45.1 fully maps Phase 45.0 required future test families while preserving non-authoritative, non-executing boundary states and recommends only docs/tests/fixtures-only continuation lanes.

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
## Phase 45.3 - Typed Bridge Acceptance Test Archive Closeout

Goal:

- Archive Phase 45.0 through Phase 45.2 as a completed docs/tests/fixtures-only acceptance-test design lane.
- Preserve non-runtime boundaries and recommend a non-runtime next lane.

Result:

- Phase 45.0 design, Phase 45.1 fixture matrix, and Phase 45.2 readiness review are archived.
- No SEV-1 or SEV-2 readiness gap was found.
- Runtime implementation remains blocked.

Status:

- complete
- tagged as `phase-45.3-typed-bridge-acceptance-test-archive-closeout`

## Phase 46.0 - Static Acceptance-Test Implementation-Plan Template

Goal:

- Define a docs/tests/fixtures-only static template for a future typed bridge acceptance-test implementation plan.
- Record what future tests must prove, which files may be eligible after separate approval, which files remain forbidden, and which validation/rollback gates are mandatory.
- Preserve Phil approval gates before actual acceptance-test implementation, runtime harness work, `lima/` changes, `tests/support/` changes, or runtime behavior.

Result:

- Phase 46.0 is static implementation-plan template work only.
- No runtime test harness is created.
- No executable runtime bridge acceptance tests are added.
- Runtime implementation remains blocked.

Status:

- complete
- tagged as `phase-46.0-static-acceptance-test-implementation-plan-template`

## Phase 46.1 - Static Acceptance-Test Dry-Run Plan

Goal:

- Use the Phase 46.0 static template to simulate a future typed bridge acceptance-test implementation phase as metadata only.
- Define dry-run cases, candidate-only file patterns, forbidden surfaces, stop conditions, rollback requirements, and blocked boundaries before any implementation.
- Keep runtime behavior, harness behavior, executable acceptance tests, and `lima/` or `tests/support/` changes blocked.

Result:

- Phase 46.1 is static dry-run planning metadata only.
- No runtime test harness is created.
- No actual or executable runtime bridge acceptance tests are added.
- Runtime implementation remains blocked.

Status:

- complete
- tagged as `phase-46.1-static-acceptance-test-dry-run-plan`

## Phase 46.2 - Static Acceptance-Test Dry-Run Readiness Review

Goal:

- Review whether the Phase 46.1 static dry-run plan is adequate before any future acceptance-test implementation planning continues.
- Confirm all required dry-run cases exist, required fields are complete, candidate patterns remain candidate-only, forbidden surfaces remain explicit, stop/rollback coverage fails closed, and boundary flags stay blocked.
- Preserve docs/tests/fixtures-only scope and keep runtime implementation blocked.

Result:

- Phase 46.2 is static dry-run readiness-review metadata only.
- No runtime test harness is created or activated.
- No actual or executable runtime bridge acceptance tests are added.
- Runtime implementation remains blocked.

Status:

- complete
- tagged as `phase-46.2-static-acceptance-test-dry-run-readiness-review`

## Phase 46.3 - Static Acceptance-Test Dry-Run Archive Closeout

Goal:

- Archive Phase 46.0 through Phase 46.2 as a completed docs/tests/fixtures-only static acceptance-test planning lane.
- Preserve non-runtime boundaries and recommend a non-runtime next lane.

Result:

- Phase 46.0 static implementation-plan template, Phase 46.1 static dry-run plan, and Phase 46.2 static readiness review are archived.
- No SEV-1 or SEV-2 readiness gap was found.
- Runtime implementation remains blocked.

Status:

- complete
- tagged as `phase-46.3-static-acceptance-test-dry-run-archive-closeout`

## Phase 47.0 - Static Acceptance-Test Implementation Preflight Review

Goal:

- Review whether the Phase 44, Phase 45, and Phase 46 planning stack is complete enough for a future separately approved concrete acceptance-test implementation checklist.
- Preserve blocked runtime and action boundaries while recording explicit future Phil approval gates.

Result:

- Phase 47.0 is docs/tests/fixtures-only static preflight-review metadata only.
- It does not create a runtime test harness.
- It does not create actual or executable runtime bridge acceptance tests.
- Runtime implementation remains blocked.

Status:

- complete
- tagged as `phase-47.0-static-acceptance-test-implementation-preflight-review`

## Phase 47.1 - Static Acceptance-Test Implementation Checklist

Goal:

- Convert the Phase 47.0 preflight decision into an exact docs/tests/fixtures-only static checklist for a future separately approved typed bridge acceptance-test implementation lane.
- Preserve fail-closed boundaries and explicit Phil approval gates before any runtime, harness, or executable acceptance-test behavior.

Result:

- Phase 47.1 is docs/tests/fixtures-only static checklist metadata only.
- It does not create or activate a runtime test harness.
- It does not create actual or executable runtime bridge acceptance tests.
- It does not modify `lima/` or `tests/support/`.
- Runtime implementation remains blocked.

Status:

- complete
- tagged as `phase-47.1-static-acceptance-test-implementation-checklist`

## Phase 47.2 - Static Acceptance-Test Checklist Readiness Review

Goal:

- Review whether the Phase 47.1 static acceptance-test implementation checklist is complete and safe for archive/closeout.
- Preserve fail-closed boundaries and explicit Phil approval gates before any runtime, harness, or executable acceptance-test behavior.

Result:

- Phase 47.2 is docs/tests/fixtures-only static checklist readiness-review metadata only.
- It does not create or activate a runtime test harness.
- It does not create actual or executable runtime bridge acceptance tests.
- It does not modify `lima/` or `tests/support/`.
- Runtime implementation remains blocked.

Status:

- complete
- tagged as `phase-47.2-static-acceptance-test-checklist-readiness-review`

## Phase 47.3 - Static Acceptance-Test Checklist Archive Closeout

Goal:

- Archive Phase 47.0 through Phase 47.2 as a completed docs/tests/fixtures-only static acceptance-test implementation preflight/checklist/readiness lane.
- Preserve fail-closed boundaries and explicit Phil approval gates before any runtime, harness, or executable acceptance-test behavior.

Result:

- Phase 47.0 preflight review, Phase 47.1 static checklist, and Phase 47.2 readiness review are archived.
- No SEV-1 or SEV-2 readiness gaps remain.
- Only optional SEV-3 cleanup notes remain.
- Runtime implementation is not recommended.
- Future runtime or harness implementation is not approved.
- Any future implementation lane requires separate explicit Phil approval.

Status:

- complete
- tagged as `phase-47.3-static-acceptance-test-checklist-archive-closeout`

## Phase 48.0 - Implementation Gate Decision Charter

Goal:

- Define the formal decision gate that must be passed before any future implementation lane can begin.
- Preserve that Phase 48.0 is docs/tests/fixtures-only and does not approve implementation.

Result:

- Phase 48.0 is docs/tests/fixtures-only implementation gate charter metadata.
- It defines what a later Phil approval must explicitly name: file scope, test/harness scope, runtime boundaries, rollback plan, audit requirements, and stop conditions.
- No runtime implementation, runtime harness, executable acceptance tests, `lima/` changes, or `tests/support/` changes are approved.

Status:

- complete
- tagged as `phase-48.0-implementation-gate-decision-charter`

## Phase 48.1 - Implementation Gate Readiness Review

Goal:

- Review whether the Phase 48.0 implementation gate decision charter is complete, internally consistent, and safe to govern future implementation decisions.
- Keep this lane docs/tests/fixtures-only and non-implementing.

Result:

- Phase 48.1 is docs/tests/fixtures-only implementation gate readiness metadata.
- It confirms approval requirements, stop conditions, file-scope requirements, and rollback requirements are explicit enough for a future decision gate.
- It confirms Sparkbot Shell public/open-source preview alignment may continue only as non-authoritative mock/display-only contract guidance.
- It does not approve runtime implementation, runtime harness creation, executable acceptance tests, `lima/` changes, `tests/support/` changes, or Sparkbot wiring/modification.

Status:

- complete
- tagged as `phase-48.1-implementation-gate-readiness-review`

## Phase 48.2 - Concrete Implementation Design Review

Goal:

- Design the first possible concrete implementation lane after Phase 48.1 without approving or implementing it.
- Keep this lane docs/tests/fixtures-only and preserve Sparkbot Shell alignment as mock/display-only preview guidance.

Result:

- Phase 48.2 is docs/tests/fixtures-only concrete implementation design-review metadata.
- It proposes `first_concrete_typed_bridge_acceptance_test_design` as a design-only future candidate lane.
- It records `docs/V1_PRODUCT_READINESS_TARGET.md` as product-direction evidence for first-shell V1 readiness: `Sparkbot_shell`, `Sparkbot`, and `Arc-Bot-shell`; future live approval, real `GuardianDecision`, provider/model routing, shell-owned haptic intent support, and operator approval for destructive edits/deletes.
- It records `docs/V1_READINESS_GAP_MATRIX.md` as the current V1 gap sequence.
- It adds `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_REQUEST.md` as the narrow Sparkbot_shell request for source-backed `thinking` / progress-state proof.
- It adds `docs/V1_G1_SPARKBOT_SHELL_THINKING_PROOF_INTAKE.md` as LIMA intake for Sparkbot_shell commit `36d697bf875a44dbafa41fc841ded86437917627`, accepting `thinking` as source-backed local shell evidence only.
- It adds `docs/V1_G2_TYPED_BRIDGE_ACCEPTANCE_PROOF.md` as the static V1-G2 typed bridge acceptance proof.
- It adds `docs/V1_G3_DESTRUCTIVE_EDIT_DELETE_OPERATOR_APPROVAL_CONTRACT.md` as the static V1-G3 destructive edit/delete operator-approval contract proof.
- It adds `docs/V1_G4_REAL_GUARDIAN_DECISION_LIVE_APPROVAL_PATH_GATE.md` as the static V1-G4 real `GuardianDecision` and live approval path design gate.
- It adds `docs/V1_G5_PROVIDER_MODEL_ROUTING_CONTRACT.md` as the static V1-G5 provider/model routing contract and acceptance-test design.
- It adds `docs/V1_G6_HAPTIC_INTENT_METADATA_CONTRACT.md` as the static V1-G6 haptic intent metadata contract and shell fixture proof.
- It adds `docs/V1_G7_FIRST_SHELL_INTEGRATION_PROOF_REQUEST.md` as the V1-G7 first-shell integration proof request gate.
- The next smallest safe V1 action is `V1-G7D`: request all three first-shell proof packets in parallel, then perform one LIMA intake audit per returned packet.
- V1-G2 proof fixtures and static tests are created under `tests/fixtures/runtime_extraction/` and `tests/`.
- V1-G3 contract fixtures and static tests are created under `tests/fixtures/runtime_extraction/` and `tests/`.
- V1-G4 design-gate fixtures and static tests are created under `tests/fixtures/runtime_extraction/` and `tests/`.
- V1-G5 routing contract fixtures and static tests are created under `tests/fixtures/runtime_extraction/` and `tests/`.
- V1-G6 haptic intent metadata fixtures and static tests are created under `tests/fixtures/runtime_extraction/` and `tests/`.
- V1-G7 request-gate fixture and static test are created under `tests/fixtures/runtime_extraction/` and `tests/`.
- Runtime implementation, runtime harness creation, `lima/` changes, `tests/support/` changes, and Sparkbot Shell changes remain unapproved.

Status:

- prepared on `phase-48-2-concrete-implementation-design-review`
- not merged or tagged
