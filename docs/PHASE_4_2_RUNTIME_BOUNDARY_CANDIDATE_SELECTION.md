# Phase 4.2 Runtime Boundary Candidate Selection

Phase 4.2 selects the first runtime boundary candidate to carry into a safety gate.

It is selection work only. It does not add runtime behavior, create adapters, import Sparkbot, wire routes, call models, execute tools, enforce approvals, persist audit events, or control physical-world systems.

## Source Basis

Phase 4.2 uses the Phase 4.1 Sparkbot Runtime Reference Refresh as its source basis.

Relevant Phase 4.1 finding:

- Sparkbot chat and voice converge into a shared tool-aware path.
- The tool-aware path is too coupled to extract first because it mixes model routing, tool exposure, Guardian policy, approval, execution, audit, verifier, and memory concerns.
- Terminal/PTY and robotics surfaces are critical-risk and must stay deferred.
- Frontend shell surfaces are useful reference material, not kernel code.

## Selected Candidate

Selected first candidate:

`humaninput_intake_boundary_for_chat_and_voice`

Candidate type:

`non_executing_boundary_candidate`

Target for next phase:

Phase 4.3 Boundary Extraction Safety Gate.

## Candidate Scope

This candidate should define how future Sparkbot text and voice shell inputs become LIMA-owned `HumanInput` records before any intent compilation or Guardian decision work.

The candidate may describe:

- text input source metadata
- voice transcript source metadata
- shell/session/actor reference metadata
- channel, room, or conversation reference metadata
- transcript confidence and normalization metadata
- privacy/redaction/reference requirements for raw user content
- attachment and file reference metadata
- owner-autonomy context references
- downstream handoff requirements into IntentEnvelope and GuardianDecision boundaries

The candidate must stay non-executing. It must not parse natural language into action, select tools, call models, execute commands, write to terminal/PTY, call robotics, approve actions, enforce policy, or persist audit data.

## Why This Candidate First

HumanInput intake is the safest first Phase 4 candidate because it can be represented as contracts, fixtures, and tests without crossing into execution.

It preserves the Sparkbot reference shape that text and voice eventually feed the same work path, while preventing raw language from becoming the execution primitive. It also creates a clean place to attach identity, trust context, transcript confidence, privacy class, and lineage references before the Intent Compiler and Guardian boundaries are revisited.

## Deferred Boundaries

The following boundaries remain deferred:

- model harness and tool-aware loop extraction
- broad tool catalogue/dispatcher extraction
- real Guardian policy or enforcement extraction
- dashboard approval execution extraction
- MCP execution handoff
- terminal/PTY extraction
- robotics command execution
- production Sparkbot adapter wiring
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot, drone, IoT, or physical-world control

## Required Phase 4.3 Safety Gate

Phase 4.3 should be a safety gate for this selected candidate, not extraction implementation.

The gate should require:

- no Sparkbot imports, wiring, route imports, or code copy
- no runtime behavior
- no model calls
- no tool execution
- no terminal/PTY execution
- no robotics command execution
- no real IntentCompiler
- no real GuardianDecision
- no approval enforcement
- no policy enforcement
- no adaptive trust enforcement
- no audit persistence
- synthetic or redacted fixture material only
- explicit privacy and redaction rules for raw text and transcripts
- actor/session/trust fields as references, not live lookup
- import-boundary tests preventing Sparkbot runtime dependencies
- clear proof that HumanInput intake cannot execute or approve anything

## Phase 4.2 GO

Phase 4.2 may add:

- this candidate selection document
- static candidate-selection fixture metadata
- static tests
- project tracking updates

## Phase 4.2 NO-GO

Phase 4.2 must not add:

- runtime behavior
- executable pipeline
- test-only composition harness
- Sparkbot import, wiring, route import, or code copy
- model calls
- tool execution
- terminal or PTY execution
- robotics command execution
- real IntentCompiler
- real GuardianDecision
- approval enforcement
- policy enforcement
- adaptive trust enforcement
- audit persistence
- LIMA AI Office implementation
- ARC Bot implementation
- custom bot implementation
- robot control
- drone control
- IoT control
- physical-world action
- production shell implementation

## Decision

GO for Phase 4.3 Boundary Extraction Safety Gate for `humaninput_intake_boundary_for_chat_and_voice`.

NO-GO for runtime extraction implementation.

NO-GO for Sparkbot integration.

NO-GO for product shell implementation.

NO-GO for physical-world action.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
