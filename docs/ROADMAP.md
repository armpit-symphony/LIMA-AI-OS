# Roadmap

LIMA Runtime is SparkPit Labs' trust-gated automation and robotics runtime. Sparkbot is the R&D shell and parity source. Arc / LIMA AI Office becomes the office shell. Robo-OS becomes the robotics driver layer. SparkPit becomes the web, community, and research shell.

## Near-Term Milestones

### M0: Phase 0 Contracts

- Land docs, contracts, and package skeleton.
- Validate imports.
- Review architecture decisions before implementation extraction.

### M0.5: Intent Compiler Boundary

Goal: define how human language becomes governed action before Harness extraction.

Deliverables:

- `IntentEnvelope` contract.
- `HumanInput` contract.
- `ClarificationRequest` contract.
- `RiskClass` enum.
- `IntentCompilerProtocol`.
- Intent Compiler boundary doc.
- `IntentLifecycle` / intent status contract.
- `IntentStatus` enum.
- `IntentType` enum.
- `ApprovalLevel` enum.
- `EvidenceRequirement` contract.
- `IntentCompilationResult` contract.
- Clarification lifecycle.
- Confidence/risk thresholds as policy-owned, not compiler-owned.
- Sparkbot chat/voice adapter requirements.
- Approval UX requirements.
- Voice/text normalization rules.
- Future BCI safety constraints.
- Raw language execution prohibition.
- Future BCI confirmation-only rule.
- Audit trail linking raw human input -> typed intent -> Guardian decision -> action/result.

Acceptance criteria:

- No tool, model, driver, file, browser, network, admin, or robot action can execute from raw natural language.
- Raw chat/voice cannot directly execute tools in the architecture.
- Every consequential command has an `IntentEnvelope`.
- Ambiguous commands trigger clarification instead of execution.
- High-risk intent requires Guardian approval.
- `IntentCompilerProtocol` remains non-executing.
- `GuardianDecision` is required before consequential Harness/Driver/Tool execution.
- Phase 1 Harness extraction is blocked until this boundary is reviewed.
- Future thought/BCI input is documented as confirm-only, never direct execution.
- Sparkbot can later adapt its chat/voice commands into this contract without losing current behavior.

### M0.6: Sparkbot Entrypoint Inventory

Goal: inventory Sparkbot's current chat/voice/tool/model/Guardian/terminal/file/network/meeting entrypoints before extraction.

Deliverables:

- `docs/SPARKBOT_ENTRYPOINT_INVENTORY.md`.
- Mapping from current Sparkbot entrypoints to future LIMA contracts.
- Raw chat-to-tool shortcut risk notes.
- Guardian coverage notes.
- Tool-pack scoping notes.
- Extraction blockers list.

Acceptance criteria:

- No Sparkbot code is copied.
- No LIMA runtime implementation is added.
- Current entrypoints are mapped to `HumanInput`, `IntentEnvelope`, `GuardianDecision`, Harness, Driver, Spine, ToolPack, or Shell contracts.
- Potential raw chat-to-tool shortcuts are identified.
- Future Sparkbot adapter requirements are documented.
- Phase 1 extraction remains blocked until inventory is reviewed.

### M1: Guardian Extraction Readiness

- Map recent Sparkbot Guardian behavior.
- Identify direct app coupling.
- Define Sparkbot adapters.
- Build parity test list for policy, approvals, breakglass, vault references, verifier, token/cost control, memory policy, and audit.

### M2: Harness Extraction Readiness

- Map Sparkbot model routing, fallback, tool catalogue, prompt cache, and telemetry.
- Define tool-pack scoping rules.
- Ensure no public Harness API can execute unguarded tools.

### M3: Spine Extraction Readiness

- Map task/event/process ledger, pending approvals, project lineage, meeting heartbeat, recurring jobs, and audit writer.
- Define storage backend boundary.

### M4: Sparkbot On Runtime

- Run Sparkbot as a shell over LIMA Runtime contracts.
- Preserve operator UX and parity behavior.
- Keep Sparkbot as the proof shell until runtime parity is real.

### M5: Robo-OS Driver Integration

- Register robotics capabilities and telemetry requirements.
- Support dry runs and simulation first.
- Require Guardian approval for physical-world execution.
- Treat emergency stop as always available and audited.

### M6: Office And Web Shells

- Add Arc / LIMA AI Office shell contracts.
- Add SparkPit web shell contracts.
- Expand office bots and automation agents through scoped tool packs.

## Long-Term Vision

LIMA Runtime becomes the kernel for human-controlled AI infrastructure: office bots, automation agents, worker robots, humanoid robots, and AI-operated work environments.

The runtime is credible only if the trust boundary is real:

- Guardian gates action.
- Natural language compiles into typed, auditable intent.
- Spine records lineage.
- Harness scopes models and tools.
- Drivers expose capabilities without becoming brains.
- Shells remain consumers, not policy owners.

## Risks

- Extracting too early can fork behavior away from Sparkbot.
- Guardian Suite may lag Sparkbot and may preserve app coupling that should be removed.
- Robo-OS integration touches physical-world risk and must default to dry-run/simulation.
- Tool catalogues can become unsafe if shells do not declare tool packs.
- Persistence must avoid raw secret sprawl in audit/event payloads.

## Current Status

Phase 0 only. No runtime implementation yet.
