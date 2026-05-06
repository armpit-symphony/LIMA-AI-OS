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

No public Harness API should directly execute tools without Guardian classification, approval, denial, or routing.

## Runtime Shape

LIMA Runtime is organized around these layers:

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
