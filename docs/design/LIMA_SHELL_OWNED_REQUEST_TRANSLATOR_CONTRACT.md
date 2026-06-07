# LIMA Shell-Owned Request Translator Contract

## Purpose

This document defines the future shell-owned request translator contract for Sparkbot and Arc Bot consumers of LIMA Runtime.

The core rule:

```text
Shells own raw input.
Shells normalize and redact.
LIMA receives already-normalized metadata.
LIMA does not parse raw user text.
LIMA does not execute translated requests.
```

This branch is design-only. It does not implement translator code, modify `lima/`, touch public Sparkbot, touch Arc Bot repositories, ingest HumanInput, create runtime `IntentEnvelope` records, create real `GuardianDecision` authority, enforce approvals, call models/providers, execute tools, access connectors, persist data, use browser/file/network APIs, start background work, wire Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

## Product Context

The previous LIMA lanes proved:

- a minimal non-executing `LimaKernel`
- explicit simulated discovery wiring
- local package/example-shell dependency proof
- Sparkbot/Arc normalized request metadata contract
- synthetic Sparkbot/Arc fixtures that map into current `KernelRequest`

The next missing boundary is ownership:

- Sparkbot and Arc must own translation from their local user/session/application context into normalized metadata.
- LIMA must not become a raw chat parser or shell-specific adapter.
- The first shared contract should define translator inputs, outputs, redaction, rejection behavior, and future acceptance tests without implementing runtime translation.

## Ownership Boundary

Shell-owned translator means:

- Sparkbot owns Sparkbot UI/session/task context parsing.
- Arc Bot owns Arc office workflow/session/task context parsing.
- LIMA owns kernel evaluation, capability gates, Guardian boundaries, dry-run result shape, and future syscall-style policy enforcement.

LIMA must not import Sparkbot or Arc internals.

Sparkbot and Arc must not expect LIMA to ingest:

- raw chat text
- raw prompt text
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- headers
- cookies
- tokens
- unsafe command bodies
- live device/network scan dumps
- robot/drone command payloads

## Translator Contract Goals

A future shell-owned translator should:

- accept shell-local input already available inside that shell
- classify or map shell-local concepts into normalized metadata
- redact raw content before LIMA sees it
- produce a default-deny capability profile
- produce source surface metadata
- produce context refs without dereferencing them in LIMA
- identify expected dry-run state only for tests
- preserve tenant/session/actor boundaries
- fail closed on missing, ambiguous, unsafe, or privileged inputs

The translator must not:

- call models
- call providers
- execute tools
- access connectors
- mutate files
- open browsers
- send messages
- persist LIMA events
- create runtime tasks
- create real `IntentEnvelope` records
- create real `GuardianDecision` records
- enforce approvals
- use credentials
- scan networks/devices
- connect or pair
- access Robo-OS
- control physical systems

## Proposed Translator Input Shape

This is a future design shape only.

```python
ShellTranslatorInput = {
    "schema_version": "0.1",
    "translator_id": "sparkbot-local-translator" | "arc-local-translator",
    "shell": {
        "shell_id": "sparkbot-workstation" | "arc-office-worker",
        "shell_type": "sparkbot" | "arc",
        "shell_version": "consumer-owned-version",
        "surface": "desktop" | "web" | "office_worker" | "service",
    },
    "actor": {
        "actor_id": "shell-owned-redacted-ref",
        "actor_type": "human" | "service" | "supervisor",
        "role_refs": ("operator",),
    },
    "session": {
        "session_id": "shell-owned-redacted-ref",
        "tenant_ref": "redacted-tenant-ref",
        "workspace_ref": "redacted-workspace-ref",
        "conversation_ref": "redacted-conversation-ref",
    },
    "shell_task": {
        "task_ref": "redacted-task-ref",
        "task_kind": "planning_preview",
        "requested_surface": "draft" | "preview" | "simulated_discovery",
        "risk_hint": "low" | "consequential" | "physical_world",
    },
    "raw_input_state": {
        "raw_text_present": True,
        "raw_text_forwarded": False,
        "attachments_present": False,
        "connector_payload_present": False,
        "credential_material_present": False,
        "unsafe_payload_present": False,
    },
}
```

Raw text presence may be recorded as boolean metadata, but raw text must not be forwarded to LIMA.

## Proposed Translator Output Shape

The translator output should match the existing Sparkbot/Arc normalized request metadata contract:

```python
ShellTranslatorOutput = {
    "schema_version": "0.1",
    "translator_id": "sparkbot-local-translator",
    "translation_state": "translated" | "blocked" | "needs_clarification",
    "blocked_reason": None,
    "redaction_summary": {
        "raw_text_forwarded": False,
        "attachments_forwarded": False,
        "connector_payload_forwarded": False,
        "credential_material_forwarded": False,
    },
    "normalized_request": {
        "request_id": "shell-generated-id",
        "shell": {},
        "actor": {},
        "session": {},
        "normalized_intent": {},
        "capability_profile": {},
        "source_surface": {},
        "context_refs": {},
    },
}
```

Only `normalized_request` is eligible to map into `KernelRequest`.

If `translation_state` is not `translated`, LIMA should not be called by that shell path.

## Required Translator Output Fields

Future translator output must include:

- `schema_version`
- `translator_id`
- `translation_state`
- `redaction_summary.raw_text_forwarded`
- `redaction_summary.attachments_forwarded`
- `redaction_summary.connector_payload_forwarded`
- `redaction_summary.credential_material_forwarded`
- `normalized_request.request_id`
- `normalized_request.shell.shell_id`
- `normalized_request.shell.shell_type`
- `normalized_request.actor.actor_id`
- `normalized_request.actor.actor_type`
- `normalized_request.session.session_id`
- `normalized_request.normalized_intent.action_category`
- `normalized_request.normalized_intent.risk_class`
- `normalized_request.normalized_intent.execution_mode`
- `normalized_request.capability_profile.profile_id`
- `normalized_request.source_surface.surface`
- `normalized_request.source_surface.privacy_class`

Missing required fields should block in a later implementation.

## Translation States

Allowed future states:

- `translated`
- `blocked`
- `needs_clarification`

`translated` means the shell produced normalized metadata and redacted raw inputs.

`blocked` means the shell detected unsafe, privileged, unsupported, raw, credentialed, physical-world, or malformed input and must not call LIMA for execution.

`needs_clarification` means the shell needs more human input before producing normalized metadata.

None of these states authorize execution.

## Fail-Closed Rules

The translator must block when:

- raw text would need to be forwarded to LIMA
- raw prompt would need to be forwarded to LIMA
- raw attachments would need to be forwarded to LIMA
- raw connector payload would need to be forwarded to LIMA
- credential material is present
- unsafe command payload is present
- live connector access is required
- live network/device scan is requested
- connection, pairing, or credential use is requested
- model call is requested
- external send is requested without a later approved approval path
- file write is requested
- browser control is requested
- process execution is requested
- scheduler/background work is requested
- device control is requested
- robot/drone/physical-world behavior is requested
- tenant/session/actor metadata is missing
- capability profile is missing or non-default-deny
- source surface cannot be identified

## Redaction Contract

Translator output must not contain:

- raw user text
- raw prompts
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- passwords
- tokens
- API keys
- headers
- cookies
- credential refs unless a later credential-ref contract approves them
- pairing codes
- unsafe command payloads
- raw scan dumps
- raw IP/MAC/Bluetooth addresses
- device serial numbers
- precise physical location
- robot/drone command payloads

Translator output may contain:

- redacted summaries
- boolean presence flags
- stable redacted refs
- synthetic fixture refs
- tenant/workspace/session refs after shell-side redaction

## Capability Profile Contract

Translator output must default all consequential capabilities to false:

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

Discovery capabilities may be enabled only for dry-run metadata classification or explicit simulated adapter paths.

## Mapping to `KernelRequest`

After successful translation, shell-owned code may map `normalized_request` to `KernelRequest`:

- `normalized_request.request_id` -> `KernelRequest.request_id`
- `normalized_request.shell.shell_id` -> `KernelRequest.shell_id`
- `normalized_request.actor.actor_id` -> `KernelRequest.actor_id`
- `normalized_request.session.session_id` -> `KernelRequest.session_id`
- `normalized_request.normalized_intent` -> `KernelRequest.normalized_intent`
- `normalized_request.capability_profile` -> `KernelRequest.capability_profile`
- `normalized_request.actor` -> `KernelRequest.actor_context`
- `normalized_request.shell` -> `KernelRequest.shell_context`
- `normalized_request.session` -> `KernelRequest.session_context`
- `normalized_request.context_refs.memory_refs` -> `KernelRequest.memory_refs`
- `normalized_request.source_surface` -> `KernelRequest.source_surface`
- translator metadata -> `KernelRequest.metadata`

The mapping should remain test-only in the first implementation lane.

## Sparkbot Translator Boundary

Future Sparkbot-owned translator work must happen in a Sparkbot-owned branch after LIMA contract audit and handoff.

Until separately approved, Sparkbot must not:

- add LIMA calls to production routes
- send raw chat text to LIMA
- expect LIMA to call models
- expect LIMA to call tools
- expect LIMA to read connectors
- expect LIMA to persist task state
- expect LIMA to enforce approvals
- expect LIMA to send external messages

## Arc Translator Boundary

Future Arc-owned translator work must happen in an Arc-owned branch after LIMA contract audit and handoff.

Until separately approved, Arc must not:

- add LIMA calls to production office workflows
- send raw office interactions to LIMA
- expect LIMA to run schedules
- expect LIMA to update customer records
- expect LIMA to access connectors
- expect LIMA to control workstations, devices, robots, or drones
- expect LIMA to execute physical-world actions

## Example Pseudo-Flow

```text
Sparkbot receives a user request
Sparkbot local code identifies task kind
Sparkbot local code redacts raw user text
Sparkbot local code creates ShellTranslatorOutput
ShellTranslatorOutput.translation_state == translated
Shell maps normalized_request into KernelRequest
LimaKernel evaluates dry-run only
Sparkbot receives proposed/blocked/approval_required metadata
No model/tool/connector/file/browser/network/device action occurs
```

## Blocked Pseudo-Flows

The translator must block:

- raw prompt forwarding
- send this message now
- run this command
- open browser and submit form
- read live email connector
- write this file
- schedule this recurring job
- connect to WiFi or Bluetooth
- pair this device
- use this credential
- control this workstation
- control this robot or drone
- try every method
- bypass approval

## Future Implementation Branch

The next implementation-shaped branch may be:

`implement-lima-shell-owned-translator-fixtures`

That branch may only add:

- synthetic `ShellTranslatorInput` fixtures
- synthetic `ShellTranslatorOutput` fixtures
- tests that validate translated outputs can map into `KernelRequest`
- tests that blocked/needs-clarification outputs do not call `LimaKernel`
- tests that redaction flags remain safe
- an implementation audit report

That branch must not:

- implement production translator code
- modify `lima/` runtime behavior
- touch public Sparkbot
- touch Arc Bot repositories
- ingest live HumanInput
- parse raw natural language in LIMA
- create runtime `IntentEnvelope` records
- create real `GuardianDecision` records
- enforce approvals
- call models/providers
- execute tools
- access connectors
- persist events
- mutate files
- use browser/network APIs
- start subprocesses, threads, workers, or schedulers
- wire Robo-OS
- control devices, robots, drones, or physical-world systems

## Handoff Notes for Sparkbot and Arc Teams

Archive-ready message:

- LIMA is defining the translator boundary, not taking ownership of raw shell input.
- Sparkbot and Arc must own local normalization and redaction.
- LIMA should receive already-normalized metadata only.
- The first LIMA-side implementation should be synthetic translator fixtures and tests, not production translator code.
- Do not wire public Sparkbot or Arc production paths yet.

## Design Verdict

This design is ready for independent audit.

It does not approve translator implementation, Sparkbot integration, Arc Bot integration, live HumanInput, raw text parsing in LIMA, IntentEnvelope runtime creation, Guardian enforcement, provider/model calls, tool execution, persistence, connector behavior, live discovery, Robo-OS access, or physical-world behavior.
