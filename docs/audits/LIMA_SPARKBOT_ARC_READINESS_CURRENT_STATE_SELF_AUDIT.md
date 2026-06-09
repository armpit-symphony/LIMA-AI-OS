# LIMA Sparkbot / Arc Readiness Current State Self-Audit

## Branch

`audit-lima-sparkbot-arc-readiness-current-state`

## Base Commit

`b0357cdb5d50fdc5fcdaffcb167fb55e19327cfe`

## Audit Verdict

PASS for LIMA-local current-state clarity.

NOT READY for Sparkbot product integration, Arc Bot product integration, public Sparkbot release use, live shell wiring,
model calls, tool execution, connector access, persistence, live discovery, Robo-OS access, device control, robotics,
drones, or physical-world behavior.

This audit records where LIMA AI OS stands as a future Sparkbot and Arc Bot dependency. It does not implement runtime
behavior and does not approve product use.

## Intention And Goal

LIMA AI OS is intended to become Spark Pit Labs' Guardian-gated AI runtime/kernel underneath Sparkbot, Arc Bot, LIMA
Office, LIMA-Robo-OS, custom office bots, and future device/robot/drone shells.

The target shape is:

- shells submit already-normalized intent/task metadata
- LIMA classifies and capability-gates requests
- Guardian is the syscall boundary for model calls, tool calls, connector access, storage, external sends, devices, and
  physical-world behavior
- HumanInput approval is required before consequential work
- every important action produces redacted audit evidence

Current operating doctrine remains:

- Contracts first.
- Guardian always.
- Sparkbot is the spec.
- Extract, do not rewrite.
- Robo-OS is a gated driver.
- LIMA Runtime is the kernel.

## Current Source-Backed Capability

Current package status:

- `pyproject.toml` declares package name `lima-runtime`, version `0.0.1`, Python `>=3.11`, and package discovery
  `lima*`.
- `import lima` works for package import proof.
- top-level `lima.__all__` remains `["contracts"]`.
- `from lima import LimaKernel` is not a supported proof-stage import.
- `from lima.kernel import LimaKernel` is supported.

Current proof-stage `lima.kernel` exports include:

- `LimaKernel`
- `CapabilityProfile`
- `KernelRequest`
- `ExecutionResult`
- `KernelEvent`
- `GuardianStubDecision`
- `SimulatedDiscoveryAdapter`
- additional dry-run candidate helpers documented in `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`

Current callable runtime surfaces:

- `LimaKernel.evaluate(...)`
- `LimaKernel.preview_guardian_lifecycle(...)`
- `SimulatedDiscoveryAdapter.simulate(...)`
- candidate preview/status/intake helpers under `lima.kernel`
- runtime state inspection that reports absence of live dependencies

Current behavior is deliberately narrow:

- accepts already-normalized metadata only
- does not parse raw natural language
- returns dry-run results
- proposes safe planning/drafting/text-preview metadata
- blocks unknown actions and approval-bypass wording
- blocks disabled capabilities
- blocks or marks consequential capability requests as approval-required metadata only
- classifies connection/discovery intent without scanning, discovering, connecting, pairing, or using credentials
- returns deterministic synthetic simulated discovery surfaces only through explicit simulated adapter use
- emits redacted in-memory/result-local event metadata only
- previews Guardian request lifecycle metadata without creating real `IntentEnvelope` or `GuardianDecision` authority

## Current Workstream

The current workstream is readiness for consumer-owned dry-run proof by Sparkbot and Arc Bot teams.

Completed LIMA-local readiness materials include:

- minimal non-executing `LimaKernel`
- runtime invariant hardening
- connection/discovery intent classification
- simulated discovery adapter and explicit kernel simulated-discovery wiring
- local package/example shell proof materials
- proof-stage public API manifest
- Sparkbot/Arc normalized request metadata contract and fixtures
- shell-owned translator boundary materials
- Sparkbot-owned and Arc-owned integration boundary designs
- proof handoff package, delivery note, intake templates, redaction checklist, receipt ledger, acceptance gate, and
  compatibility-freeze review materials
- Guardian lifecycle preview method and method-level public API metadata classification
- consumer proof delivery status record

Latest delivery status remains:

`operator_request_prepared_waiting_for_manual_delivery_or_consumer_packets`

No LIMA-local evidence currently proves manual delivery occurred. No Sparkbot proof packet or Arc Bot proof packet has
been received in this repository.

## What LIMA Cannot Do Yet

LIMA cannot currently:

- ingest live HumanInput
- parse raw chat or raw office-task text into runtime intent
- create runtime `IntentEnvelope` authority
- create real `GuardianDecision` authority
- enforce approvals
- route or call models
- execute tools
- read or write connectors
- read or write memory or task state
- persist events or storage
- run schedulers, queues, workers, daemons, subprocesses, or threads
- open browsers, mutate files, execute processes, or call networks
- discover live devices or networks
- connect, pair, scan, or use credentials
- wire Sparkbot, Arc Bot, or Robo-OS
- control devices, robots, drones, or physical-world systems

These are product blockers, not defects in the current dry-run slice.

## Sparkbot Readiness

Sparkbot status:

`waiting_for_consumer_owned_dry_run_proof_packet`

The required Sparkbot proof branch remains:

`sparkbot-lima-dry-run-boundary-proof`

That branch must be owned by the Sparkbot repo team. This LIMA lane must not create, edit, inspect, fetch, clone, scan,
or push the public Sparkbot repository or any Sparkbot proof branch without explicit approval.

Sparkbot must prove:

- exact LIMA commit/package reference
- proof-stage imports only
- redacted already-normalized Sparkbot metadata
- default-deny capability profile
- explicit dry-run `LimaKernel.evaluate(...)` call
- optional explicit synthetic `SimulatedDiscoveryAdapter` use only
- optional `LimaKernel.preview_guardian_lifecycle(...)` preview only
- no raw chat text sent to LIMA
- no public Sparkbot production route wired
- no Sparkbot model/tool/connector/memory/storage/scheduler/external-send/browser/file/process/network/device/Robo-OS
  behavior invoked through LIMA
- complete non-execution invariant evidence

## Arc Bot Readiness

Arc Bot status:

`waiting_for_consumer_owned_dry_run_proof_packet`

The required Arc Bot / LIMA Office proof branch remains:

`arc-lima-dry-run-boundary-proof`

That branch must be owned by the Arc Bot / LIMA Office repo team. This LIMA lane must not create, edit, inspect, fetch,
clone, scan, or push Arc Bot proof branches without explicit approval.

Arc Bot must prove:

- exact LIMA commit/package reference
- proof-stage imports only
- redacted already-normalized office-task metadata
- default-deny capability profile
- explicit dry-run `LimaKernel.evaluate(...)` call
- optional explicit synthetic `SimulatedDiscoveryAdapter` use only
- optional `LimaKernel.preview_guardian_lifecycle(...)` preview only
- no raw office-task text, customer records, connector payloads, credentials, or provider/tool payloads sent to LIMA
- no Arc production route wired
- no Arc task/project/note/form/record/customer file, connector, tool, provider, memory, storage, scheduler,
  external-send, browser/file/process/network/device/Robo-OS behavior invoked through LIMA
- complete non-execution invariant evidence

## Required Non-Execution Invariants

Any accepted current proof must preserve:

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

Missing or contradictory invariant evidence blocks proof acceptance.

## Roadmap To Sparkbot And Arc Product Use

Phase 1: Consumer-owned dry-run proof.

- Sparkbot team produces a redacted proof packet.
- Arc Bot / LIMA Office team produces a redacted proof packet.
- LIMA audits each packet using the existing proof-results audit template.
- Outcome may only be `pass_for_dry_run_dependency_proof`, not product readiness.

Phase 2: Dry-run compatibility freeze.

- Start only after both proof audits pass.
- Freeze proof-public imports and dry-run result invariants for consumer proof use.
- Do not approve live integration.

Phase 3: Real Guardian decision authority contract.

- Design real Guardian request/decision authority boundaries.
- Keep decision creation separate from approval enforcement.
- Require fail-closed semantics and redacted events.
- No model/tool/connector execution yet.

Phase 4: Approval-required and HumanInput approval flow.

- Design and then implement approval request, operator response, denial, timeout, and revocation handling.
- No execution until approval enforcement is separately implemented and audited.

Phase 5: Runtime `IntentEnvelope` creation.

- Add governed runtime creation from already-normalized shell metadata.
- Raw chat and raw office-task text still stay outside LIMA until a live HumanInput bridge is separately approved.

Phase 6: Event/spine and storage foundation.

- Start with redacted in-memory event spine behavior.
- Add durable persistence only after a storage contract, redaction policy, rollback plan, and audit pass.

Phase 7: Provider/model boundary.

- Design provider registry and routing as Guardian-gated.
- Add model calls only after capability checks, token/cost controls, audit events, fallback policy, and no-secret logging
  are reviewed.

Phase 8: Tool, connector, and shell execution boundaries.

- Design tool packs and connector read/write boundaries.
- Keep Sparkbot and Arc shell wiring repo-owned.
- Require Guardian approval for write/execute/external-send surfaces.

Phase 9: Sparkbot dry-run integration, then gated live integration.

- Sparkbot consumes frozen dry-run API first.
- Production public Sparkbot release wiring requires a separate Sparkbot-owned branch and LIMA-side audit.

Phase 10: Arc Bot / LIMA Office dry-run integration, then gated office workflows.

- Arc consumes frozen dry-run API first.
- Customer data, office connectors, sends, form submissions, and scheduled work require Guardian and HumanInput approval
  design before live behavior.

Phase 11: Robo-OS / physical-world readiness.

- Design Robo-OS as a gated driver plane, not a competing brain.
- Require dry-run/simulation, Guardian classification, HumanInput approval, emergency stop semantics, telemetry, and
  explicit operator controls before any physical-world behavior.

## Current Blockers To End Goal

- manual operator delivery confirmation is not recorded in LIMA
- Sparkbot proof packet is missing
- Arc Bot proof packet is missing
- proof redaction reviews are not started
- proof results audits are not started
- dry-run consumer compatibility freeze is blocked
- real Guardian decision authority is not implemented
- approval enforcement is not implemented
- live HumanInput bridge is not implemented
- runtime `IntentEnvelope` creation is not implemented
- provider/model routing is not implemented
- tool and connector execution boundaries are not implemented
- storage/event-spine persistence is not implemented
- Sparkbot and Arc integration remain consumer-repo-owned and unproven

## Archive-Ready Team Notes

Sparkbot team note:

```text
LIMA is ready only for a Sparkbot-owned dry-run dependency proof packet.

Use branch sparkbot-lima-dry-run-boundary-proof in the Sparkbot repo. Use proof-stage LIMA imports, redacted
already-normalized Sparkbot metadata, default-deny capabilities, explicit LimaKernel.evaluate(...) dry-run calls, and
optional explicit synthetic SimulatedDiscoveryAdapter / Guardian lifecycle preview evidence only.

Do not wire public routes, raw chat, models, tools, connectors, memory, storage, schedulers, external sends,
browser/file/process/network behavior, devices, Robo-OS, robots, drones, or physical-world behavior through LIMA.
```

Arc Bot / LIMA Office team note:

```text
LIMA is ready only for an Arc-owned dry-run dependency proof packet.

Use branch arc-lima-dry-run-boundary-proof in the Arc Bot / LIMA Office repo. Use proof-stage LIMA imports, redacted
already-normalized office-task metadata, default-deny capabilities, explicit LimaKernel.evaluate(...) dry-run calls, and
optional explicit synthetic SimulatedDiscoveryAdapter / Guardian lifecycle preview evidence only.

Do not wire production office workflows, raw office-task text, customer records, models, tools, connectors, memory,
storage, schedulers, external sends, browser/file/process/network behavior, devices, Robo-OS, robots, drones, or
physical-world behavior through LIMA.
```

## Validation Run

PASS.

Commands run:

- `python -m compileall lima` - passed
- `python -m pytest -q tests/test_lima_consumer_proof_intake_ledger_closeout_static.py -p no:cacheprovider` - passed, 19 tests
- `python -m pytest -q tests -p no:cacheprovider` - passed, 2848 tests
- `git diff --check` - passed
- `git status --short --branch` - showed only the intended audit report before commit

## Recommended Next Branch

If the operator confirms manual delivery and no proof packets are supplied:

`record-lima-consumer-proof-manual-delivery-confirmation`

If Sparkbot or Arc proof packets are supplied:

`audit-consumer-owned-proof-results`

If LIMA continues internally before proof packets arrive:

`design-lima-guardian-decision-authority-contract`

That internal branch should be design-only and must not implement real `GuardianDecision` authority, approval
enforcement, model calls, tool execution, connector access, storage, shell wiring, live discovery, Robo-OS, devices,
robotics, drones, or physical-world behavior.
