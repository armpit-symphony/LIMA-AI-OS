# Roadmap

LIMA Runtime is SparkPit Labs' trust-gated automation and robotics runtime. Sparkbot is the R&D shell and parity source. Arc / LIMA AI Office becomes the office shell. Robo-OS becomes the robotics driver layer. SparkPit becomes the web, community, and research shell.

## Near-Term Milestones

### M0: Phase 0 Contracts

- Land docs, contracts, and package skeleton.
- Validate imports.
- Review architecture decisions before implementation extraction.

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
