# LIMA Kernel Plugin Contract Design

## Purpose

This document defines the first plug-and-play LIMA Kernel contract for future shell consumers such as Sparkbot, Arc Bot, SparkPit web shells, LIMA-Robo-OS, and future bot/robot/drone shells.

This is design only. It does not implement `LimaKernel`, runtime services, provider calls, storage, Guardian enforcement, HumanInput bridging, adapters, Sparkbot wiring, Arc Bot wiring, Robo-OS wiring, tool execution, driver execution, schedulers, workers, file/browser/network actions, robotics, drone actuation, device control, or physical-world behavior.

The intended implementation direction is a later separately approved minimal non-executing runtime branch.

## Non-Goals

- No product runtime behavior.
- No model calls or provider registry implementation.
- No storage, database, durable event log, or persistence.
- No real GuardianDecision creation.
- No approval enforcement.
- No HumanInput runtime bridge.
- No shell wiring for Sparkbot, Arc Bot, Robo-OS, or any product shell.
- No adapters, tools, drivers, schedulers, background workers, external sends, file/browser/network actions, robotics, drones, devices, or physical-world behavior.

## Top-Level Shell-Facing Entry Point

Proposed object:

- `LimaKernel`

Proposed role:

- A shell-facing app object that accepts already-normalized task or intent metadata.
- A coordination boundary, not an executor.
- A fail-closed dry-run evaluator that returns an `ExecutionResult` with no side effects.

Proposed initialization shape:

```python
# PSEUDO-CODE ONLY. Not implemented.
kernel = LimaKernel(
    kernel_id="lima-local-dev",
    shell_manifest=shell_manifest,
    guardian=fail_closed_guardian_stub,
    event_sink=in_memory_redacted_event_sink,
    provider_registry=None,
    storage=None,
    humaninput_bridge=None,
    driver_registry=None,
    clock=clock,
)
```

Dependency injection points:

- `shell_manifest`: declares shell identity, default packs, denied packs, and permissions.
- `guardian`: future Guardian policy boundary. First implementation must be a fail-closed stub only.
- `event_sink`: future redacted in-memory event collector. No durable persistence in first implementation.
- `provider_registry`: future model/provider registry. Must be `None` or inert in the first implementation.
- `storage`: future persistence interface. Must be `None` in the first implementation.
- `humaninput_bridge`: future HumanInput-to-normalized-intent bridge. Must be `None` in the first implementation.
- `driver_registry`: future tool/driver registry. Must be `None` in the first implementation.
- `clock`: deterministic timestamp provider for testability.

Shell ID / actor / session handling:

- `shell_id` identifies the calling shell, such as `sparkbot`, `arc-office`, `sparkpit-web`, or `robo-shell`.
- `actor_id` identifies the human or system actor making the request.
- `session_id` is optional and references the current shell session.
- The kernel must treat these as metadata only in the first implementation.
- The kernel must not perform live auth lookup, trust lookup, session lookup, or product-shell lookup.

## Kernel Input Contract

Proposed object:

- `KernelRequest`

Required fields:

- `request_id`: caller-provided unique request reference.
- `shell_id`: shell identity.
- `actor_id`: actor identity reference.
- `session_id`: optional session reference.
- `normalized_intent`: already-normalized intent or task metadata.
- `capability_profile`: requested capability booleans and constraints.
- `source_surface`: source surface metadata.
- `metadata`: optional bounded non-authoritative metadata.

`normalized_intent` shape:

- `intent_id`: optional existing intent reference.
- `task_type`: normalized task type, such as `preview_text`, `draft`, `plan`, `connector_read`, `external_send`, `file_write`, `device_control`, or `unknown`.
- `summary`: redacted human-readable task summary.
- `risk_class`: `low`, `medium`, `high`, `critical`, or `unknown`.
- `requested_action`: normalized action label.
- `target_ref`: optional reference-only target, not raw credentials or raw content.
- `typed_args_ref`: optional reference to typed args stored outside the kernel request.
- `approval_hint`: optional caller hint; never authority.

Capability and context fields:

- `capability_profile`: the requested capability profile described below.
- `actor_context`: actor metadata references only; no raw credentials, tokens, or secrets.
- `shell_context`: shell metadata references only.
- `session_context`: session metadata references only.
- `memory_refs`: optional reference-only memory/context handles.
- `source_surface`: source channel, product surface, input type, fixture/test marker, and privacy class.

Rules:

- The first implementation must reject raw HumanInput payloads.
- The first implementation must reject raw natural language as execution authority.
- The first implementation must accept already-normalized metadata only.
- Caller-provided approval claims must never authorize execution.
- Unknown or missing risk/capability data must fail closed.

## Kernel Output Contract

Proposed object:

- `ExecutionResult`

Required fields:

- `request_id`
- `kernel_id`
- `shell_id`
- `actor_id`
- `session_id`
- `state`: `blocked`, `proposed`, or `approval_required`
- `dry_run`: always `True` in the first implementation.
- `executed`: always `False`.
- `execution_claims`: always empty.
- `guardian_summary`: summary of the fail-closed Guardian stub outcome.
- `event_refs`: references to in-memory redacted events emitted during evaluation.
- `redacted_audit_summary`: short sanitized summary.
- `blocked_reason`: required for `blocked`.
- `approval_reason`: required for `approval_required`.
- `warnings`: bounded warning codes.
- `metadata`: bounded non-authoritative metadata.

State meanings:

- `proposed`: text-only preview or planning metadata may be shown to a shell. It does not authorize execution.
- `approval_required`: consequential intent was detected and must stop before approval/enforcement work exists.
- `blocked`: unknown, dangerous, unsupported, or unsafe input was denied fail-closed.

No execution claims:

- The result must not claim that any model call, tool call, file mutation, connector operation, send, browser action, process execution, scheduled run, device control, robot actuation, drone actuation, or persistence occurred.

## Capability Profile Contract

Proposed object:

- `CapabilityProfile`

Required boolean fields:

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

Required metadata:

- `profile_id`
- `profile_version`
- `allowed_tool_packs`
- `denied_tool_packs`
- `approval_required_capabilities`
- `source`

First implementation rule:

- Any capability set to `True` other than a text-only preview capability must produce `approval_required` or `blocked`.
- `process_execute`, `device_control`, `robotics_actuation`, `drone_actuation`, and unknown capabilities must default to `blocked`.
- `external_send`, `connector_write`, `file_write`, `memory_write`, `task_state_write`, `browser_control`, and `scheduler_run` must default to `approval_required` or `blocked` until explicit Guardian enforcement exists.

Capability decision table:

| Capability | First implementation state |
| --- | --- |
| `model_calls` | `approval_required` unless explicitly handled as no-call preview metadata |
| `memory_write` | `approval_required` |
| `task_state_write` | `approval_required` |
| `connector_read` | `approval_required` |
| `connector_write` | `approval_required` |
| `external_send` | `approval_required` |
| `file_write` | `approval_required` |
| `process_execute` | `blocked` |
| `browser_control` | `approval_required` |
| `device_control` | `blocked` |
| `robotics_actuation` | `blocked` |
| `drone_actuation` | `blocked` |
| `scheduler_run` | `approval_required` |

## Fail-Closed Guardian Stub Contract

Proposed object:

- `GuardianStub`

Allowed first behavior:

- Allow text-only preview metadata as `proposed`.
- Mark consequential action as `approval_required`.
- Deny unknown, dangerous, unsupported, or physical-world action as `blocked`.

Explicit boundaries:

- No real `GuardianDecision` creation unless separately scoped later.
- No approval enforcement.
- No PIN verification.
- No breakglass handling.
- No auth/vault/trust lookup.
- No policy persistence.
- No execution authorization.

Guardian summary shape:

- `guardian_state`: `proposed`, `approval_required`, or `blocked`.
- `decision_ref`: `None` in the first implementation.
- `policy_stub`: stable stub name and version.
- `reason_code`: deterministic reason code.
- `capabilities_reviewed`: reviewed capability names.
- `constraints`: fail-closed constraints applied.

## Event Contract

Proposed object:

- `KernelEvent`

Required fields:

- `event_id`
- `request_id`
- `kernel_id`
- `shell_id`
- `actor_id`
- `session_id`
- `event_type`
- `created_at`
- `state`
- `reason_code`
- `redacted_summary`
- `privacy_class`
- `contains_secret`: always `False`
- `contains_raw_prompt`: always `False`
- `contains_unsafe_payload`: always `False`
- `metadata`

Allowed event types:

- `kernel.request_received`
- `kernel.capability_profile_reviewed`
- `kernel.guardian_stub_evaluated`
- `kernel.result_returned`

Storage rule:

- First implementation may emit redacted in-memory events only.
- No durable persistence.
- No database writes.
- No file writes.
- No background event flush.

Forbidden event content:

- raw prompts
- raw provider payloads
- secrets
- headers
- tokens
- unsafe command payloads
- credentials
- raw tool arguments/results
- raw terminal output
- raw browser/network payloads
- raw sensor payloads
- robot/device command payloads

## Provider/Model Boundary

Future plug-in point:

- `provider_registry`

Contract role:

- A future model/provider registry may be injected into `LimaKernel` after Guardian and capability policy are implemented.
- It must sit behind Guardian classification and tool-pack scoping.
- It must emit redacted model-call events and never expose every tool by default.

Current design boundary:

- Do not implement provider adapters.
- Do not call models.
- Do not route providers.
- Do not build prompts.
- Do not expose provider credentials.
- Do not store provider payloads.

## HumanInput Boundary

Future plug-in point:

- `humaninput_bridge`

Contract role:

- A future bridge may convert validated `HumanInput` records into normalized intent/task metadata.
- The bridge must not treat raw text, voice, console, gesture, or future BCI input as execution authority.
- It must produce typed metadata for Guardian review.

Current design boundary:

- Do not implement a live bridge.
- Do not parse natural language.
- Do not compile intent.
- Do not connect Sparkbot, Arc Bot, or any shell.
- Do not create GuardianDecision records from HumanInput.

## Robo-OS / Physical-World Boundary

Future plug-in point:

- `driver_registry`
- `robo_os_adapter`

Contract role:

- LIMA-Robo-OS must remain a Guardian-gated driver/runtime integration.
- Physical-world actions must require typed intent, dry-run/simulation where possible, explicit approval, safety constraints, emergency-stop semantics, telemetry evidence, and audit lineage.

Future required semantics:

- dry-run or simulation before execution where available
- operator approval for physical-world action
- scoped Guardian decision before execution
- emergency-stop path that is auditable and safety-prioritized
- no model-direct robot command path
- no drone/device actuation from raw natural language

Current design boundary:

- Do not implement Robo-OS adapters.
- Do not expose robot, drone, device, sensor, or hardware commands.
- Do not create physical-world execution paths.
- Do not wire MCP robot tools.
- Do not call drivers.

## Example Pseudo-Usage

The following examples are pseudo-code only. They are not executable runtime claims.

Sparkbot-style shell:

```python
# PSEUDO-CODE ONLY. Not implemented.
kernel = LimaKernel(
    kernel_id="lima-sparkbot-local",
    shell_manifest=ShellManifest(
        shell_id="sparkbot",
        allowed_tool_packs=("core", "model", "memory"),
        denied_tool_packs=("terminal", "deploy", "payments", "robo"),
    ),
    guardian=GuardianStub(mode="fail_closed"),
    event_sink=InMemoryRedactedEventSink(),
)

result = kernel.evaluate(
    KernelRequest(
        request_id="req-001",
        shell_id="sparkbot",
        actor_id="actor-ref",
        session_id="session-ref",
        normalized_intent={
            "task_type": "draft",
            "summary": "Draft a customer reply.",
            "risk_class": "low",
            "requested_action": "text_preview",
        },
        capability_profile=CapabilityProfile.text_preview_only(),
        source_surface={"surface": "chat", "privacy_class": "private"},
    )
)
assert result.dry_run is True
assert result.executed is False
```

Arc Bot-style shell:

```python
# PSEUDO-CODE ONLY. Not implemented.
kernel = LimaKernel(
    kernel_id="lima-arc-office",
    shell_manifest=ShellManifest(
        shell_id="arc-office",
        allowed_tool_packs=("core", "model", "comms", "calendar"),
        denied_tool_packs=("terminal", "deploy", "payments", "robo"),
    ),
    guardian=GuardianStub(mode="fail_closed"),
    event_sink=InMemoryRedactedEventSink(),
)

result = kernel.evaluate(normalized_office_task)
# external_send=True would return approval_required, not send anything.
```

Robo shell:

```python
# PSEUDO-CODE ONLY. Not implemented.
kernel = LimaKernel(
    kernel_id="lima-robo-shell",
    shell_manifest=ShellManifest(
        shell_id="robo-shell",
        allowed_tool_packs=("core",),
        denied_tool_packs=("robo", "terminal", "browser", "network"),
    ),
    guardian=GuardianStub(mode="fail_closed"),
    event_sink=InMemoryRedactedEventSink(),
)

result = kernel.evaluate(robotics_task_metadata)
# robotics_actuation=True would return blocked in the first implementation.
```

## Minimal Later Implementation Scope

If separately approved, the first implementation branch may add only:

- a top-level `LimaKernel` or equivalent app object
- request/result/capability/event dataclasses
- fail-closed Guardian stub
- redacted in-memory event sink
- deterministic tests for proposed, approval-required, and blocked outcomes

It must not add provider calls, storage, persistence, real Guardian enforcement, approval enforcement, HumanInput bridging, Sparkbot wiring, Arc Bot wiring, Robo-OS wiring, adapters, tool execution, driver execution, schedulers, background work, external sends, file/browser/network actions, robotics, drones, devices, or physical-world behavior.
