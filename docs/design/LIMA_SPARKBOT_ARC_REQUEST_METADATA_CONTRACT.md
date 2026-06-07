# LIMA Sparkbot and Arc Request Metadata Contract

## Purpose

This document defines the first normalized request metadata contract for future Sparkbot and Arc Bot consumers of LIMA Runtime.

The goal is to make the next cross-team review concrete:

- what Sparkbot or Arc must normalize before calling LIMA
- what LIMA may accept as a `KernelRequest`
- what LIMA must reject or treat as out of scope
- what remains dry-run and non-executing
- what cannot be wired into public Sparkbot or Arc Bot yet

This branch is design-only. It does not implement request translation, shell wiring, HumanInput ingestion, IntentEnvelope creation, Guardian enforcement, provider/model calls, tool execution, storage, persistence, live adapters, connector access, browser/file/network mutation, scheduler/background work, Robo-OS access, device control, robotics, drones, or physical-world behavior.

## Product Context

LIMA is being prepared as the Guardian-gated runtime/kernel under:

- public Sparkbot
- Arc Bot / LIMA Office
- future office automation shells
- LIMA Guardian services
- LIMA-Robo-OS and physical-world drivers later

The current repo has a minimal non-executing `LimaKernel`, explicit simulated discovery wiring, and a local package/example-shell proof. The next product-readiness question is whether Sparkbot and Arc can agree on a stable normalized metadata shape before either repo attempts integration.

This contract is dependency-readiness work, not integration work.

## Core Rule

Sparkbot and Arc must not send raw chat text, raw prompts, provider payloads, tool payloads, connector payloads, credentials, or live command bodies into LIMA for execution.

The first supported consumer shape is:

```text
shell-normalized metadata in
capability profile in
dry-run ExecutionResult out
```

LIMA remains non-executing until later branches explicitly approve more runtime behavior.

## Future Consumer Boundary

Future Sparkbot and Arc callers may eventually provide:

- shell identity
- actor identity
- session identity
- tenant/workspace references
- already-normalized intent metadata
- capability profile
- source surface metadata
- optional context references
- optional synthetic/simulated discovery metadata

Future Sparkbot and Arc callers must not provide:

- raw chat text as executable intent
- raw prompt text
- raw provider request/response payloads
- raw tool arguments
- raw connector records
- secrets, tokens, headers, cookies, credentials, or pairing codes
- unsafe command payloads
- live network/device scan dumps
- device serial numbers or physical location details
- robot/drone command payloads

## Proposed Request Envelope

This is a design shape only. It is not implemented in this branch.

```python
SparkbotArcNormalizedRequest = {
    "schema_version": "0.1",
    "request_id": "shell-generated-id",
    "shell": {
        "shell_id": "sparkbot-workstation" | "arc-bot",
        "shell_type": "sparkbot" | "arc",
        "shell_version": "consumer-owned-version",
        "surface": "desktop" | "web" | "office_worker" | "service",
    },
    "actor": {
        "actor_id": "redacted-or-stable-actor-ref",
        "actor_type": "human" | "service" | "supervisor",
        "role_refs": ("owner", "operator"),
    },
    "session": {
        "session_id": "redacted-session-ref",
        "tenant_ref": "redacted-tenant-ref",
        "workspace_ref": "redacted-workspace-ref",
        "conversation_ref": "redacted-conversation-ref",
    },
    "normalized_intent": {
        "action_category": "planning",
        "requested_capability": None,
        "task_type": "office_task_preview",
        "risk_class": "low",
        "summary": "redacted shell-normalized summary",
        "input_origin": "humaninput_normalized_by_shell",
        "execution_mode": "dry_run",
    },
    "capability_profile": {
        "profile_id": "sparkbot-default-deny",
        "allowed_tool_packs": (),
        "model_calls": False,
        "external_send": False,
        "file_write": False,
        "process_execute": False,
        "browser_control": False,
        "device_control": False,
        "robotics_actuation": False,
        "drone_actuation": False,
    },
    "source_surface": {
        "surface": "sparkbot_workstation",
        "privacy_class": "redacted",
        "contains_raw_prompt": False,
        "contains_secret": False,
        "contains_unsafe_payload": False,
    },
    "context_refs": {
        "memory_refs": (),
        "task_refs": (),
        "document_refs": (),
        "connector_refs": (),
    },
}
```

## Mapping to Current `KernelRequest`

Future shell-owned translation may map:

- `request_id` to `KernelRequest.request_id`
- `shell.shell_id` to `KernelRequest.shell_id`
- `actor.actor_id` to `KernelRequest.actor_id`
- `session.session_id` to `KernelRequest.session_id`
- `normalized_intent` to `KernelRequest.normalized_intent`
- `capability_profile` to `KernelRequest.capability_profile`
- `actor` to `KernelRequest.actor_context`
- `shell` to `KernelRequest.shell_context`
- `session` to `KernelRequest.session_context`
- `context_refs.memory_refs` to `KernelRequest.memory_refs`
- `source_surface` to `KernelRequest.source_surface`
- schema and trace metadata to `KernelRequest.metadata`

This mapping must stay one-way and inert in the first implementation. It must not create real runtime `IntentEnvelope` records, real Guardian decisions, durable events, live task records, or shell-side effects.

## Required Metadata Fields

Future request contract fields:

- `schema_version`
- `request_id`
- `shell.shell_id`
- `shell.shell_type`
- `actor.actor_id`
- `actor.actor_type`
- `session.session_id`
- `normalized_intent.action_category`
- `normalized_intent.risk_class`
- `normalized_intent.execution_mode`
- `capability_profile.profile_id`
- `source_surface.surface`
- `source_surface.privacy_class`

Missing required fields should block in a later implementation.

## Allowed Initial Action Categories

Initial Sparkbot/Arc metadata contract may allow dry-run classification for:

- `informational`
- `planning`
- `drafting`
- `text_preview`
- simulated connection/discovery categories already recognized by `LimaKernel`

All other categories should remain blocked until explicitly designed and audited.

## Capability Profile Requirements

Sparkbot and Arc must provide a default-deny capability profile.

The following capabilities must default to `False`:

- `model_calls`
- `memory_write`
- `task_state_write`
- `connector_read`
- `connector_write`
- `external_send`
- `file_write`
- `process_execute`
- `browser_control`
- `device_control`
- `robotics_actuation`
- `drone_actuation`
- `scheduler_run`
- `connection_attempt`
- `device_pairing`
- `credential_use`
- `iot_control`
- `physical_world_actuation`

Discovery capabilities may be enabled only for dry-run metadata classification or explicit simulated adapter paths. Live discovery remains out of scope.

## Source Surface Metadata

Shells must identify where metadata came from without forwarding raw sensitive input.

Required fields:

- `surface`
- `privacy_class`
- `contains_raw_prompt`
- `contains_secret`
- `contains_unsafe_payload`

Recommended future fields:

- `redaction_policy_id`
- `retention_policy_id`
- `operator_visible`
- `customer_visible`
- `tenant_scoped`
- `source_channel`

The source surface must not contain raw message text, raw attachments, raw connector data, credentials, headers, or command payloads.

## Context Reference Rules

Context references are references only.

Allowed:

- redacted memory refs
- task refs
- document refs
- conversation refs
- connector refs that are not dereferenced by LIMA
- synthetic fixture refs

Forbidden:

- embedded document contents
- raw connector records
- raw emails/messages
- raw file contents
- raw credentials
- raw tokens
- raw provider payloads
- raw device/network scan results
- physical location details

LIMA must not dereference refs in this contract lane.

## Output Contract Expectations

For this lane, Sparkbot and Arc should expect only current dry-run `ExecutionResult` behavior:

- `state`: `proposed`, `approval_required`, or `blocked`
- `guardian_summary`: non-authoritative stub metadata
- `event_refs`: in-memory only
- `redacted_audit_summary`: safe summary
- `metadata`: redacted dry-run metadata

They must not expect:

- executed actions
- model output
- sent messages
- mutated files
- browser sessions
- connector reads or writes
- task persistence
- approval enforcement
- real GuardianDecision authority
- device/network access
- robot/drone behavior

## Non-Execution Invariants

Future Sparkbot/Arc contract tests must assert:

- `executable is False`
- `execution_allowed is False`
- `side_effects_allowed is False`
- `dispatch_allowed is False`
- `persistence_allowed is False`
- `dry_run is True`
- `model_calls_allowed is False`
- `model_calls_executed is False`
- `live_discovery_executed is False`
- `connection_attempted is False`
- `pairing_attempted is False`
- `credentials_used is False`
- `session_opened is False`
- `device_control_executed is False`
- `physical_world_allowed is False`
- `physical_world_executed is False`
- `guardian_decision_created is False`
- `approval_enforced is False`
- `humaninput_bridge_active is False`
- `sparkbot_wiring_active is False`
- `robo_os_wiring_active is False`
- `adapter_active is False`
- `tool_execution_allowed is False`
- `driver_execution_allowed is False`
- `scheduler_active is False`
- `external_calls_allowed is False`

## Sparkbot-Specific Notes

Sparkbot may eventually be the first public shell to depend on LIMA, but this design does not authorize touching the public Sparkbot repo.

Future Sparkbot branch work should only happen after this contract is audited. That future branch should compare Sparkbot's existing normalized action/task concepts against this contract and produce handoff notes before implementation.

Sparkbot must not use LIMA for:

- raw chat execution
- production route wiring
- model calls
- tool execution
- connector access
- message sending
- file/browser/network actions
- persistence
- approval enforcement

until separate implementation lanes approve those surfaces.

## Arc Bot-Specific Notes

Arc Bot / LIMA Office consumers should treat LIMA as a future kernel boundary, not as a live office automation engine yet.

Arc must not use LIMA for:

- live employee/customer workflow execution
- autonomous office actions
- external sends
- file mutation
- production connector reads/writes
- scheduled jobs
- workstation/device control
- Robo-OS access

until separate implementation lanes approve those surfaces.

## Future Pseudo-Flow

```text
Sparkbot or Arc shell receives user interaction
Shell normalizes intent metadata locally
Shell redacts raw input and sensitive payloads
Shell builds default-deny capability profile
Shell builds source surface metadata
Shell creates KernelRequest-shaped metadata
LimaKernel evaluates dry-run only
LIMA returns proposed, approval_required, or blocked
Shell displays or records redacted dry-run result
No model call, tool call, persistence, connector access, or external action occurs
```

## Blocked Pseudo-Flows

The following must block or remain out of scope:

- raw chat text sent directly to LIMA for execution
- Sparkbot asks LIMA to send a message
- Sparkbot asks LIMA to call a model
- Arc asks LIMA to update a customer record
- Arc asks LIMA to run a scheduled job
- either shell asks LIMA to read a live connector
- either shell asks LIMA to write a file
- either shell asks LIMA to open a browser
- either shell asks LIMA to connect to WiFi, Bluetooth, IoT, or LAN
- either shell asks LIMA to control a device, robot, or drone

## Future Implementation Branch

The next implementation-shaped branch after audit may be:

`implement-lima-sparkbot-arc-request-fixtures`

That branch may only add:

- synthetic Sparkbot-shaped normalized request fixtures
- synthetic Arc-shaped normalized request fixtures
- focused tests mapping those fixtures into existing `KernelRequest`
- dry-run result invariant checks
- an implementation audit report

That branch must not:

- touch the public Sparkbot repository
- touch Arc Bot repositories
- modify `lima/` runtime behavior unless separately approved
- create a live HumanInput bridge
- create IntentEnvelope runtime records
- create real GuardianDecision authority
- enforce approvals
- call models/providers
- execute tools
- access connectors
- persist events
- use storage
- mutate files
- use browser/network APIs
- start workers, schedulers, threads, or subprocesses
- wire Robo-OS
- control devices, robots, drones, or physical-world systems

## Handoff Notes for Sparkbot and Arc Teams

Archive-ready message:

- LIMA now has a local package/example-shell proof and a proposed normalized request metadata contract.
- The first supported consumer model is normalized metadata in, dry-run `ExecutionResult` out.
- Do not send raw chat text into LIMA for execution.
- Do not expect LIMA to call models, tools, connectors, storage, networks, browsers, files, devices, robots, or drones.
- Do not wire public Sparkbot or Arc production paths yet.
- The next useful review is to compare Sparkbot and Arc's existing normalized task/action shapes against this contract and identify gaps.

## Design Verdict

This design is ready for independent audit.

It does not approve Sparkbot integration, Arc Bot integration, live HumanInput, IntentEnvelope runtime creation, Guardian enforcement, provider/model calls, tool execution, persistence, live discovery, connector behavior, Robo-OS access, or physical-world behavior.
