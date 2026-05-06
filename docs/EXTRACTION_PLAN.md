# Extraction Plan

LIMA Runtime is extracted from Sparkbot in phases. Phase 0 is contracts/docs/stubs only.

Do not migrate code until contracts are approved.

## Phase 0: Contracts, Docs, Stubs

Scope:

- Establish architecture documents.
- Define public contracts for Guardian, Harness, Spine, Driver, Storage, Shell, ToolPack, approvals, audit events, model calls, and tool calls.
- Create importable package skeleton.
- Add import-only validation.

Acceptance criteria:

- Repository imports cleanly.
- Contract modules compile on Python 3.11+.
- Docs state Guardian invariant and MCP boundary rule.
- No real execution paths exist.
- No Sparkbot implementation code is copied.
- No secrets or production deploys are touched.

## Phase 1: Decouple Guardian

Scope:

- Review recent Sparkbot Guardian improvements before extraction.
- Decouple Guardian modules from Sparkbot imports such as `app.crud`, `app.models`, route modules, and UI-specific assumptions.
- Preserve policy, auth, vault, verifier, approvals, breakglass, memory policy, token/cost control, and audit behavior behind contracts.

Acceptance criteria:

- Guardian core can import without Sparkbot application models.
- Sparkbot adapter remains explicit.
- Secret handling uses references, not raw secret event payloads.
- Existing Sparkbot Guardian tests are mapped to runtime parity tests.

## Phase 2: Extract Model Harness

Scope:

- Extract model routing/fallback, tool catalogue, prompt cache, telemetry, and friendly error handling.
- Enforce tool-pack scoping.
- Preserve Sparkbot model behavior through parity tests.

Acceptance criteria:

- Public Harness APIs cannot execute tools without a Guardian decision or approval token.
- Shells declare allowed tool packs.
- Model calls are auditable events.
- Sparkbot model routing behavior is covered by parity tests.

## Phase 3: Extract Spine

Scope:

- Extract the process/task/event ledger, scheduler contracts, recurring jobs, audit writer, autonomous loop metadata, and lineage interfaces.
- Keep storage backend behind the persistence interface.

Acceptance criteria:

- Spine can append events and retrieve lineage through contracts.
- Approval state is represented in the ledger.
- Storage backend is replaceable.
- Sparkbot task/project/approval ledger behavior has parity coverage.

## Phase 4: Put Sparkbot On LIMA Runtime

Scope:

- Run Sparkbot as a shell on top of LIMA Runtime.
- Replace direct internal runtime calls with contract-backed adapters.
- Keep Sparkbot product behavior unchanged.

Acceptance criteria:

- Sparkbot parity tests pass.
- Tool policy decisions, pending approvals, model calls, audit events, memory events, and Spine events match current behavior.
- Operators retain existing approval and breakglass controls.

## Phase 5: Integrate Robo-OS As Guardian-Gated Driver

Scope:

- Treat LIMA Robo-OS as a driver/runtime layer.
- Register robotics capabilities, telemetry requirements, dry runs, and approval requirements.
- Use MCP for robot/device tool boundaries.

Acceptance criteria:

- Simulation and dry-run commands can be planned without physical execution.
- Medium/high/unknown physical-world commands require Guardian approval.
- Real hardware motion is blocked by default until approval workflow and audit evidence are complete.
- Emergency stop remains available and audited.

## Phase 6: Arc, LIMA AI Office, And SparkPit Shells

Scope:

- Integrate Arc / LIMA AI Office, SparkPit web systems, office bots, automation agents, and future robot shells as LIMA Runtime consumers.
- Each shell declares tool packs and permissions.

Acceptance criteria:

- Shells consume shared runtime contracts.
- Shell-specific permissions are enforced by Guardian.
- Tool packs are scoped per shell.
- Runtime audit and lineage remain consistent across shells.

## Extraction Risks

- Sparkbot Guardian improvements are moving faster than earlier Guardian Suite extraction work.
- Existing Guardian Suite code shows useful module boundaries but still has Sparkbot app coupling.
- Robo-OS has real physical-world execution surfaces; integration must default to dry-run, simulation, and explicit Guardian approval.
- Tool catalogues can grow beyond safe model context; tool-pack scoping is required.
