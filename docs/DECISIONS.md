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
