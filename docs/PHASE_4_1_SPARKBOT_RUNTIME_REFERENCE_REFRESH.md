# Phase 4.1 Sparkbot Runtime Reference Refresh

Phase 4.1 refreshes Sparkbot runtime reference knowledge for extraction planning.

It is read-only reference work. It does not copy Sparkbot code, import Sparkbot modules, wire live Sparkbot routes, move behavior into LIMA, execute tools, call models, enforce approvals, persist audit events, or touch physical-world systems.

## Reference Snapshot

Local Sparkbot reference inspected:

- path: `C:/Users/limap/Sparkbot`
- branch: `main`
- commit: `27bd7dd8ce9e164c6068a13b1855ccc62c7bbe7c`
- local status: dirty because two untracked proposal scripts are present
- Sparkbot files modified by this phase: none

The local Sparkbot checkout is useful as prototype/spec material, but it is not treated as clean source-of-truth code for copying. Any later extraction must re-check a reviewed Sparkbot commit before behavior moves.

## Reviewed Surfaces

Phase 4.1 reviewed Sparkbot only enough to ground future boundary selection:

- chat routing and room WebSocket surfaces in `backend/app/api/routes/chat/websocket.py`
- voice transcription path in `backend/app/api/routes/chat/voice.py`
- tool-aware chat/model loop in `backend/app/api/routes/chat/llm.py`
- tool catalogue and dispatcher in `backend/app/api/routes/chat/tools.py`
- Guardian policy decision surface in `backend/app/services/guardian/policy.py`
- Guardian suite entrypoint in `backend/app/services/guardian/suite.py`
- dashboard approval execution surface in `backend/app/api/routes/chat/dashboard.py`
- breakglass, vault, and task Guardian routes in `backend/app/api/routes/chat/guardian.py`
- MCP registry explain-plan and approval routes in `backend/app/api/routes/chat/mcp.py`
- robotics bridge route and service in `backend/app/api/routes/chat/robotics.py` and `backend/app/services/lima_robotics_bridge.py`
- terminal route and PTY manager in `backend/app/api/routes/terminal.py` and `backend/app/services/terminal_service.py`
- Workstation, Command Center, Spine, terminal, and station frontend surfaces

## Runtime Boundary Observations

Sparkbot currently concentrates several future LIMA kernel concerns inside shell/application code.

The tool-aware chat path combines model routing, tool shortlist selection, Guardian policy decisions, pending approvals, guarded execution, output guardrails, verifier notes, audit logging, and memory updates. LIMA should not extract this as one kernel primitive. Future work should split planning, tool exposure, decisioning, approval, execution, and lineage.

Voice input is useful reference because it normalizes audio into text and then enters the same tool-aware chat path. Future LIMA input work should preserve text/voice convergence while adding explicit `HumanInput` identity, transcript confidence, typed intent, and Guardian decision boundaries before consequential execution.

The tool dispatcher is broad and includes read-only tools, write-capable tools, browser/network/file/comms surfaces, terminal send, scheduled Guardian tasks, vault operations, dynamic skills, and robotics commands. LIMA must keep deny-by-default tool-pack scoping before any catalogue or dispatcher extraction.

Guardian policy and dashboard approval paths show useful reference behavior, but they are still coupled to Sparkbot users, rooms, pending approval storage, audit logging, and execution helpers. LIMA should extract contracts and decoupling seams before moving real policy/enforcement behavior.

MCP explain-plan routes are a safer reference than direct execution routes because they already represent dry-run planning and approval state without executing the tool. They remain application-specific and still need LIMA-owned contracts before extraction.

The terminal surface is high risk. The route is feature-gated and local-user scoped, but the PTY manager writes raw input to a live shell and does not enforce command-level policy. Terminal/PTY extraction remains blocked until critical-risk decision, approval, lineage, and redaction gates exist.

The robotics bridge is high risk. It has dry-run and approval-required metadata, but it also contains execution paths for some commands and an emergency-stop path. Robot, drone, IoT, and physical-world action remain blocked until later driver-plane contracts, simulation/dry-run policy, approval metadata, emergency-stop doctrine, and physical safety gates are complete.

Frontend Workstation, Command Center, Spine, and station surfaces are useful shell reference material. They should inform future shell adapter contracts, but they are not kernel code.

## Candidate Boundary Direction

The safest next milestone is Phase 4.2 Runtime Boundary Candidate Selection.

Recommended candidate for first detailed selection:

- HumanInput intake boundary for chat and voice, described as non-executing adapter contracts and fixture metadata.

This is preferable because it can be represented without tool execution, model calls, terminal access, Sparkbot wiring, or physical-world action.

Deferred candidates:

- model harness and tool-aware loop extraction
- broad tool catalogue/dispatcher extraction
- real Guardian policy/enforcement extraction
- dashboard approval execution extraction
- terminal/PTY extraction
- robotics command execution extraction
- production Sparkbot adapter wiring
- LIMA AI Office, ARC Bot, or custom bot implementation

## Phase 4.1 GO

Phase 4.1 may add:

- this reference refresh document
- static reference fixture metadata
- static tests that verify the reference refresh boundary
- small project tracking updates

## Phase 4.1 NO-GO

Phase 4.1 must not add:

- runtime behavior
- executable pipeline
- test-only composition harness
- Sparkbot import, wiring, route import, or code copy
- model calls
- tool execution
- terminal or PTY execution
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

GO for Phase 4.2 Runtime Boundary Candidate Selection.

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
