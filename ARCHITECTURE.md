# LIMA Runtime Architecture

LIMA-AI-OS is the contracts-first home for **LIMA Runtime / LIMA Kernel**, a Guardian-gated runtime extracted from Sparkbot. Sparkbot remains the spec until parity tests prove otherwise.

## Layer Diagram

```text
                    +----------------------------------------------+
                    | Shells                                       |
                    | Sparkbot, Arc, SparkPit web, Robo shells     |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | System Services                              |
                    | skills, comms, voice, office automation      |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Spine                                        |
                    | process/task/event ledger, schedules, audit  |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Guardian                                     |
                    | policy, auth, vault, verifier, approvals     |
                    | syscall gate for all external action         |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Model Harness                                |
                    | model routing, tools, tool packs, telemetry  |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | IO Drivers                                   |
                    | Robo-OS, filesystem, browser, network, MCP   |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Persistence                                  |
                    | SQLite, Postgres, Memory/Vault backends      |
                    +----------------------------------------------+
```

The diagram is logical, not a mandate that every internal call must be a network hop. The internal kernel may use direct Python contracts. Externally actionable operations still pass through Guardian.

## Layers

### Shells

Shells are user- or environment-facing surfaces. Examples include Sparkbot Desktop / Workstation, Arc / LIMA AI Office, the SparkPit web shell, robot runtimes on Jetson-class devices, and future humanoid or worker robot shells.

Shells declare allowed tool packs and permissions. They do not receive every tool by default.

### System Services

System services provide reusable runtime features such as skills, comms, voice loops, task/project services, and office automation. Services must call the Guardian boundary before requesting an external action.

### Spine

The Spine is the process, task, and event ledger. It records audit-grade events, scheduled work, recurring jobs, autonomous loops, task lineage, project lineage, and approval state.

Sparkbot already demonstrates this shape with a Guardian/Spine ledger, scheduler loops, pending approvals, meeting heartbeat, audit events, and project/task promotion. Phase 0 captures the contract boundary without migrating that implementation.

### Guardian

Guardian is the primary trust boundary. It owns policy, auth, vault references, token and cost control, verification, approvals, breakglass, and memory/memo policy.

Every model call, tool call, robotics action, file/network/browser action, and privileged operation must be classified by Guardian before execution.

### Model Harness

The Model Harness owns model routing, fallback, prompt assembly, tool catalogue filtering, tool-pack scoping, prompt cache, telemetry, and friendly errors.

The Harness may plan a tool call, but it cannot execute one through a public API unless Guardian has approved, denied, or routed the action.

### IO Drivers

Drivers are boundaries to external systems: Robo-OS, filesystem, browser, network, MCP servers, hardware devices, and robot drivers. MCP belongs here as the tool, driver, and plugin boundary.

Robo-OS is a Guardian-gated driver/runtime integration, not a competing brain.

### Persistence

Persistence is one interface with multiple backends: SQLite for local/desktop, Postgres for hosted, Memory/Vault backends for governed recall and secret references, and future pluggable stores.

Contracts must never require raw secrets to be stored in general event payloads.

## Guardian Invariant

Guardian is the syscall gate.

Every external action, tool execution, privileged operation, model call, robotics/physical-world action, file/network/browser action, and approval-requiring operation must pass through Guardian.

No public Harness API should directly execute tools without Guardian classification, approval, denial, or routing.

## MCP Boundary Rule

Use MCP for:

- tools
- drivers
- Robo-OS
- browser/filesystem/network adapters
- external plugins
- shell/runtime boundaries where useful

Use direct Python contracts/ABCs for:

- Guardian core
- Harness core
- Spine ledger
- storage interface
- internal policy checks

Everything externally actionable goes through Guardian. MCP is the driver/tool/plugin boundary. The internal kernel may use direct contracts.

## Separation Rules

- Shells request capabilities; they do not own runtime policy.
- Services compose internal capabilities; they do not bypass Guardian.
- Guardian classifies and authorizes external action.
- Harness routes models and scopes tools; it does not execute unguarded tools.
- Drivers expose capabilities, dry runs, and execution surfaces; execution requires Guardian approval.
- Persistence stores events, state, and secret references through one interface.

## Extraction Principle

Sparkbot is the spec. Extract, do not rewrite.

LIMA-AI-OS Phase 0 creates the contracts and boundaries needed to extract Guardian, Harness, Spine, drivers, shells, tool packs, and persistence interfaces from Sparkbot with parity checks. It does not migrate production behavior.
