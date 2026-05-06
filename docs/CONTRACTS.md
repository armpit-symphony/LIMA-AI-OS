# Public Contracts

LIMA Runtime contracts define the kernel boundary before implementation is extracted from Sparkbot.

## Contract Rules

- Guardian is mandatory.
- Public Harness APIs must not execute tools without Guardian classification and approval state.
- Externally actionable operations use drivers or tool packs and pass through Guardian.
- MCP is the driver/tool/plugin boundary, not the mandatory internal kernel bus.
- Raw secrets must not be stored in general events; contracts use secret references.
- Shells declare allowed tool packs and permissions.
- Phase 0 contracts are intentionally small.

## Guardian

Guardian classifies and records decisions for model calls, tool calls, driver commands, privileged operations, and approval-requiring actions.

Examples in prose:

- A model request enters the Harness. Guardian classifies the request for cost, policy, and allowed model route before the Harness calls a model provider.
- A tool call is planned by the Harness. Guardian classifies it as allow, deny, approval required, or route to another path.
- A robot motion command is represented as a driver command. Guardian classifies it before the driver can execute it.

## Harness

Harness owns model routing, fallback, tool catalogue filtering, prompt cache, telemetry, and friendly errors.

Harness may plan a tool call. It may only execute a guarded tool call when supplied with a Guardian decision or approval token.

## Spine

Spine is the task/event/process ledger. It appends audit events, creates task records, updates task state, and retrieves lineage.

Spine records what happened. Guardian decides whether externally actionable work may happen.

## Driver

Drivers expose capabilities, dry-run previews, telemetry expectations, and execution calls.

Driver execution requires Guardian approval. For Robo-OS, real hardware motion is never a default path.

## Storage

Storage provides one persistence interface over SQLite, Postgres, Memory/Vault backends, and future stores.

`put_secret_ref` stores references or vault handles. It does not store raw secrets.

## Shell

Shells are user-facing or environment-facing surfaces. Sparkbot, Arc / LIMA AI Office, SparkPit web, and Robo shells are shells.

Shells declare:

- allowed tool packs
- permissions
- operator identity model
- runtime capabilities they intend to use

## ToolPack

Tool packs group tools by capability and risk area.

Required pack model:

- `packs/comms`
- `packs/robo`
- `packs/system`
- `packs/browser`
- `packs/files`
- `packs/memory`
- `packs/admin`

Shells declare allowed packs. The Harness scopes the available tool catalogue from those packs. The model does not receive every available tool by default.

## Approval

Approval contracts represent pending, approved, denied, expired, and routed decisions. Approval state must be auditable and tied to a Guardian decision.

## AuditEvent

Audit events are immutable evidence of runtime decisions and actions. They should contain safe metadata, actor identity, source shell, risk posture, and correlation IDs.

## ModelCall

Model call events record request metadata, selected route, cost/token posture, and result metadata. They must not leak raw secrets.

## ToolCall

Tool call events record planned action, tool identity, arguments metadata, Guardian decision, execution result metadata, and audit correlation.

Tool arguments containing sensitive material must be redacted or represented as vault references in audit surfaces.
