# LIMA-AI-OS

LIMA-AI-OS is the Phase 0 home for the **LIMA Runtime / LIMA Kernel**: a Guardian-gated agent and robotics runtime extracted from Sparkbot.

This is not a greenfield rewrite. Sparkbot is the battle-tested source of truth. LIMA-AI-OS starts with architecture, contracts, and package boundaries so SparkPit Labs can extract the runtime safely, preserve Sparkbot parity, and put every externally actionable operation behind Guardian.

Company context: [SparkPit Labs](https://sparkpitlabs.com).

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
