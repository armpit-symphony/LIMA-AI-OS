# LIMA Runtime Architecture

LIMA-AI-OS is the contracts-first home for **LIMA Runtime / LIMA Kernel**, a Guardian-gated runtime extracted from Sparkbot. Sparkbot remains the spec until parity tests prove otherwise.

## Layer Diagram

```text
                    +----------------------------------------------+
                    | Human Control Surface                        |
                    | Text, voice, console, gesture, future BCI    |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Intent Compiler                             |
                    | normalize, clarify, typed intent, risk      |
                    | confidence, evidence requirements           |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Shells                                       |
                    | Sparkbot, Arc, SparkPit web, Robo shells     |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Guardian Control Plane                       |
                    | policy, auth, vault, budgets, approvals      |
                    | audit, breakglass, syscall gate              |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Tool-Pack Scope                             |
                    | deny-by-default packs, shortlist tools      |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Model Plane                                  |
                    | reasoning, planning, model routing           |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Driver Plane                                 |
                    | deterministic tools, Robo-OS, files, browser |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Spine / Event Ledger                         |
                    | process/task/event ledger, schedules, audit  |
                    +----------------------+-----------------------+
                                           |
                    +----------------------v-----------------------+
                    | Persistence                                  |
                    | SQLite, Postgres, Memory/Vault backends      |
                    +----------------------------------------------+
```

The diagram is logical, not a mandate that every internal call must be a network hop. The internal kernel may use direct Python contracts. Externally actionable operations still pass through Guardian.

## Layers

### Human Control Surface

Human control surfaces are the places where operators express intent: text, voice, mobile/operator consoles, gesture/manual controls, and future thought/BCI-style inputs.

These surfaces are not execution APIs. They produce human input records that must be normalized, clarified, typed, classified for risk, and routed to Guardian before any consequential action can occur.

Future thought/BCI signals are future-facing only. They can produce uncertain, low-confidence intent candidates, but they cannot directly execute tools, files, network actions, browser actions, payments, admin actions, or physical-world actions.

### Intent Compiler

The Intent Compiler is the boundary between human language and governed runtime action. It normalizes natural language, detects ambiguity, asks clarifying questions, produces typed `IntentEnvelope` records, assigns confidence, assigns risk class, attaches evidence requirements, and routes intent to Guardian.

The Intent Compiler does not execute actions and does not approve actions. It prepares structured intent for Guardian.

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

### Model Plane

The Model Plane owns model routing, fallback, prompt assembly, tool catalogue filtering, tool-pack scoping, prompt cache, telemetry, and friendly errors.

The Model Plane may reason and plan, but it cannot execute deterministic tools through a public API unless Guardian has approved, denied, or routed the action.

### Driver Plane

The Driver Plane contains deterministic execution surfaces: Robo-OS, filesystem, browser, network, MCP servers, hardware devices, robot drivers, and other tool packs. MCP belongs here as the tool, driver, and plugin boundary.

Robo-OS is a Guardian-gated driver/runtime integration, not a competing brain.

### Persistence

Persistence is one interface with multiple backends: SQLite for local/desktop, Postgres for hosted, Memory/Vault backends for governed recall and secret references, and future pluggable stores.

Contracts must never require raw secrets to be stored in general event payloads.

## Guardian Invariant

Guardian is the syscall gate.

Every external action, tool execution, privileged operation, model call, robotics/physical-world action, file/network/browser action, and approval-requiring operation must pass through Guardian.

No public Harness API should directly execute tools without Guardian classification, approval, denial, or routing.

Every consequential action must carry a scoped `GuardianDecision.decision_id` before execution. The `decision_id` is the audit identity that links typed intent to Harness, Tool, Driver, Terminal, Robot, Spine, and Audit events.

## Tool-Pack Scoping

Tool-pack scoping sits between `GuardianDecision` and Harness tool exposure:

```text
GuardianDecision -> ToolPackScope -> Harness Tool Shortlist -> Tool Execution -> Spine/Audit
```

Tool exposure is deny-by-default. Shells declare allowed packs, actor/session policy narrows them, intent proposes needed packs, and Guardian constrains the final allowed packs. The Harness receives a selected shortlist, not the full catalogue.

No shell receives every tool by default. Terminal, admin, robot, payment, deployment, filesystem, browser, and network packs require explicit risk and approval policy before exposure.

## Natural Language as an OS Primitive

Natural language is the primary human control protocol for LIMA. Text, voice, console commands, gestures, and future thought/BCI-style inputs are human control surfaces that enter the runtime as `HumanInput` records.

Natural language is not allowed to bypass Guardian. Raw natural language must never directly execute tools or drivers. All consequential commands must become `IntentEnvelope` records before execution is even considered.

Every `IntentEnvelope` must be traceable to a Guardian decision and audit events:

```text
HumanInput -> IntentEnvelope -> GuardianDecision.decision_id -> Action/Event
```

Voice transcripts are treated the same as text commands after transcription and normalization. Future thought/BCI signals are treated as uncertain intent candidates and require explicit confirmation, Guardian review, and approval. There is no direct actuation from thought input.

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
