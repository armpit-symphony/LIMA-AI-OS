# LIMA Sparkbot / Arc Dry-Run Boundary Proof

## Purpose

This document defines the next LIMA-local design gate for proving future Sparkbot and Arc Bot dependency use without touching either consumer repository.

The boundary proof is not product integration. It is a repo-team-owned dry-run exercise showing that Sparkbot and Arc Bot can import the current LIMA proof-stage API, construct redacted already-normalized metadata locally, call non-executing kernel surfaces, and return evidence that all Guardian-safe invariants remain intact.

This design exists so Spark Pit Labs can move toward Sparkbot and Arc Bot readiness without allowing runtime sprawl.

## Scope

Allowed in this LIMA branch:

- document the expected Sparkbot proof branch shape
- document the expected Arc Bot proof branch shape
- define the proof packet evidence LIMA needs back
- define LIMA-side acceptance and rejection criteria
- preserve the current public API manifest boundary
- preserve dry-run-only Guardian lifecycle preview classification
- preserve explicit simulated discovery adapter use as optional and synthetic only

Forbidden in this LIMA branch:

- modifying the public Sparkbot repo
- modifying Arc Bot / LIMA Office repo code
- modifying `lima/`
- modifying package metadata
- adding tests/support helper behavior
- adding runtime behavior
- adding shell wiring
- ingesting raw chat or raw office-task text
- creating runtime `IntentEnvelope` records
- creating real `GuardianDecision` authority
- enforcing approval
- calling models
- executing tools
- accessing connectors
- reading or writing memory, task state, files, databases, or storage
- opening sockets
- using browser, process, network, Bluetooth, USB, serial, MQTT, Matter, or mDNS APIs
- live discovery, scanning, connecting, pairing, or credential use
- Sparkbot, Arc Bot, or Robo-OS wiring
- scheduler, queue, worker, daemon, subprocess, or thread behavior
- device, robot, drone, or physical-world control

## Current LIMA Dependency Surface

Consumer proof branches may use only proof-stage public imports documented in `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

`LimaKernel.preview_guardian_lifecycle(...)` is allowed only as a method-level dry-run candidate reachable through `LimaKernel`. Its result dataclasses are not approved public imports.

Consumer proof branches must not import:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Expected Consumer Branches

Sparkbot team-owned branch:

`sparkbot-lima-dry-run-boundary-proof`

Arc Bot / LIMA Office team-owned branch:

`arc-lima-dry-run-boundary-proof`

The LIMA repo team must not create, edit, or push those branches. The LIMA team may provide this design, archive-ready notes, and review criteria for the repo teams to use.

## Sparkbot Proof Shape

Sparkbot should prove only:

1. Sparkbot can pin or reference the exact LIMA commit or proof package used.
2. Sparkbot can import proof-stage LIMA symbols.
3. Sparkbot can build redacted already-normalized intent metadata locally.
4. No raw chat text, raw prompt, connector payload, tool argument, credential, header, cookie, token, memory record, task payload, browser payload, file content, terminal command, network payload, device identifier, Robo-OS payload, robot payload, drone payload, or physical-world command is sent to LIMA.
5. Sparkbot can call `LimaKernel.evaluate(...)` explicitly with `dry_run=True`.
6. Sparkbot can optionally pass an explicit `SimulatedDiscoveryAdapter` only for synthetic simulated discovery metadata.
7. Sparkbot can optionally call `LimaKernel.preview_guardian_lifecycle(...)` as dry-run preview metadata only.
8. Sparkbot can capture a redacted proof packet with all non-execution invariants.
9. Sparkbot can prove no public production route, task flow, model route, connector route, tool route, memory write, storage write, scheduler, external send, browser action, file action, process action, network action, device action, Robo-OS action, robot action, drone action, or physical-world action was wired through LIMA.

Sparkbot must not claim production readiness from this proof.

## Arc Bot Proof Shape

Arc Bot / LIMA Office should prove only:

1. Arc can pin or reference the exact LIMA commit or proof package used.
2. Arc can import proof-stage LIMA symbols.
3. Arc can build redacted already-normalized office-task metadata locally.
4. No raw office-task text, customer record, customer file, connector payload, provider payload, tool argument, credential, header, cookie, token, form payload, payment payload, legal payload, HR payload, medical payload, browser payload, file content, network payload, device identifier, Robo-OS payload, robot payload, drone payload, or physical-world command is sent to LIMA.
5. Arc can call `LimaKernel.evaluate(...)` explicitly with `dry_run=True`.
6. Arc can optionally pass an explicit `SimulatedDiscoveryAdapter` only for synthetic simulated discovery metadata.
7. Arc can optionally call `LimaKernel.preview_guardian_lifecycle(...)` as dry-run preview metadata only.
8. Arc can capture a redacted proof packet with all non-execution invariants.
9. Arc can prove no production route, customer workflow, project mutation, note mutation, form submission, connector route, tool route, model route, memory write, storage write, scheduler, external send, browser action, file action, process action, network action, office-system adapter, device action, Robo-OS action, robot action, drone action, or physical-world action was wired through LIMA.

Arc must not claim production readiness from this proof.

## Required Proof Packet Evidence

Each repo-team proof packet must include:

- consumer repo
- consumer branch
- consumer team owner
- LIMA repository URL
- exact LIMA commit or package version
- package name and package version
- import method
- public imports used
- redacted already-normalized metadata evidence
- capability profile evidence
- `LimaKernel.evaluate(...)` call evidence
- optional `SimulatedDiscoveryAdapter` evidence if used
- optional `LimaKernel.preview_guardian_lifecycle(...)` evidence if used
- dry-run `ExecutionResult` sample
- full non-execution invariant evidence
- redaction attestation
- forbidden surface attestation
- rollback or disable plan
- repo-team proof verdict

Allowed proof verdict:

`pass_for_dry_run_dependency_proof`

Allowed non-pass verdicts:

- `needs_redaction`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_missing_evidence`
- `question_only`

Forbidden verdicts:

- `production_ready`
- `ready_for_live_integration`
- `ready_for_model_calls`
- `ready_for_tool_execution`
- `ready_for_connector_access`
- `ready_for_live_discovery`
- `ready_for_device_control`
- `ready_for_robo_os`
- `ready_for_physical_world`

## Required Non-Execution Invariants

Every accepted proof packet must show:

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

Missing invariant evidence means the packet is not accepted.

Any contradictory invariant means the packet is blocked.

## Optional Simulated Discovery Evidence

If used, the consumer proof must show:

- adapter is passed explicitly
- `dry_run=True`
- `simulated_only=True`
- discovery mode is `simulated`
- returned surfaces are synthetic
- returned surfaces are inert
- returned surfaces are not connectable
- returned surfaces are not controllable
- live discovery did not execute
- scanning did not execute
- connection did not execute
- pairing did not execute
- credential use did not occur
- session opening did not occur
- device control did not execute
- physical-world behavior did not execute

Any live discovery, scan, connection attempt, pairing attempt, credential use, device access, Robo-OS access, robotics, drones, or physical-world behavior blocks the proof.

## Optional Guardian Lifecycle Preview Evidence

If used, the consumer proof must show:

- method is called through `LimaKernel.preview_guardian_lifecycle(...)`
- request is already-normalized `KernelRequest` metadata or equivalent mapping
- output is treated as preview metadata only
- no lifecycle result dataclasses are imported as public API
- no runtime `IntentEnvelope` authority is created
- no real `GuardianDecision` authority is created
- approval is not enforced
- execution is not approved
- events are redacted and in-memory/result-local only

Any claim that lifecycle preview output is a real Guardian decision blocks the proof.

## LIMA-Side Review Result

LIMA may accept a consumer proof packet only as:

`pass_for_dry_run_dependency_proof`

That means:

- dry-run dependency shape is proven for the current LIMA commit or package version
- no production integration is approved
- no live runtime behavior is approved
- no public Sparkbot release integration is approved
- no Arc Bot product integration is approved

## Archive-Ready Note For Sparkbot Team

```text
Please run `sparkbot-lima-dry-run-boundary-proof` in the Sparkbot repo only.

Use the current LIMA proof-stage API as a dependency candidate. Build redacted already-normalized metadata locally, call `LimaKernel.evaluate(...)` with dry-run metadata, optionally pass `SimulatedDiscoveryAdapter` only for synthetic preview metadata, and optionally call `LimaKernel.preview_guardian_lifecycle(...)` as preview metadata only.

Return a redacted proof packet. Do not wire public routes, production chat flows, models, tools, connectors, memory, storage, schedulers, external sends, browser/file/process/network surfaces, devices, Robo-OS, robots, drones, or physical-world behavior through LIMA.
```

## Archive-Ready Note For Arc Bot Team

```text
Please run `arc-lima-dry-run-boundary-proof` in the Arc Bot / LIMA Office repo only.

Use the current LIMA proof-stage API as a dependency candidate. Build redacted already-normalized office-task metadata locally, call `LimaKernel.evaluate(...)` with dry-run metadata, optionally pass `SimulatedDiscoveryAdapter` only for synthetic preview metadata, and optionally call `LimaKernel.preview_guardian_lifecycle(...)` as preview metadata only.

Return a redacted proof packet. Do not wire production office workflows, customer records, models, tools, connectors, memory, storage, schedulers, external sends, browser/file/process/network surfaces, office-system adapters, devices, Robo-OS, robots, drones, or physical-world behavior through LIMA.
```

## Recommended Next Branch

`audit-lima-sparkbot-arc-dry-run-boundary-proof-design`

That branch should independently audit this design before any consumer-team proof packet is treated as acceptable evidence.
