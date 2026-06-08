# LIMA Consumer Proof Compatibility Freeze Review

## Design Status

This document defines the LIMA-side review gate that must run before any future dry-run consumer compatibility freeze branch may start for Sparkbot and Arc Bot.

It is design-only. It does not start a compatibility freeze, accept proof packets, archive evidence, update ledgers, audit real proof results, inspect consumer repositories, modify consumer repositories, create consumer branches, modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports, implement intake automation, implement storage, implement runtime behavior, wire shells, call models, execute tools, access connectors, run schedulers, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve production integration.

## Purpose

The compatibility freeze review is a final human-reviewed stop between consumer proof audits and any future freeze design.

It answers one narrow question:

Can LIMA safely start a separate dry-run compatibility freeze design branch for the current proof-public API surface?

The answer must remain `blocked` unless both Sparkbot and Arc Bot proof packets exist, both pass redaction and LIMA-side proof audits, and no runtime, consumer, redaction, claim, or API-boundary blocker remains.

## Relationship To Existing Artifacts

This review depends on:

- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE_STATIC_TESTS_AUDIT.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- future Sparkbot proof audit report
- future Arc Bot proof audit report

If this review conflicts with any source artifact, the stricter artifact controls.

## Current Review Verdict

`freeze_review_blocked`

Reasons:

- Sparkbot consumer-owned dry-run proof packet has not been supplied in this LIMA branch.
- Arc Bot consumer-owned dry-run proof packet has not been supplied in this LIMA branch.
- Sparkbot LIMA-side proof audit does not exist.
- Arc Bot LIMA-side proof audit does not exist.
- No evidence proves both consumer proof audits passed as `pass_for_dry_run_dependency_proof`.
- Compatibility freeze must not start from LIMA-local readiness materials alone.

## Review Inputs

Required inputs before review may pass:

| Input ID | Required Evidence | Required Status |
| --- | --- | --- |
| `sparkbot_packet_acceptance` | Sparkbot packet passed the acceptance gate as safe enough to audit | `accepted_for_dry_run_proof_audit` |
| `arc_packet_acceptance` | Arc Bot packet passed the acceptance gate as safe enough to audit | `accepted_for_dry_run_proof_audit` |
| `sparkbot_proof_audit` | Sparkbot LIMA-side audit using proof results audit template | `pass_for_dry_run_dependency_proof` |
| `arc_proof_audit` | Arc Bot LIMA-side audit using proof results audit template | `pass_for_dry_run_dependency_proof` |
| `sparkbot_redaction` | Sparkbot packet redaction review | `passed_redaction_review` |
| `arc_redaction` | Arc Bot packet redaction review | `passed_redaction_review` |
| `public_api_manifest` | Current proof-public API manifest reviewed against both packets | `unchanged_or_reviewed` |
| `non_execution_invariants` | Both packet audits prove all current non-execution invariants | `verified` |
| `claim_boundary` | Neither packet claims production/live/model/tool/connector/device/Robo-OS/physical-world readiness | `verified` |
| `consumer_boundary` | Neither packet changes or wires consumer production routes through LIMA | `verified` |

If any input is missing, contradictory, stale, or unredacted, review status must remain `freeze_review_blocked`.

## Allowed Review Statuses

Allowed review statuses:

- `freeze_review_blocked`
- `needs_consumer_packet`
- `needs_redaction`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `blocked_by_public_api_drift`
- `ready_for_dry_run_freeze_design`

`ready_for_dry_run_freeze_design` means only that a separate freeze design branch may be proposed. It does not mean a freeze exists or that Sparkbot or Arc Bot can use LIMA in product.

## Forbidden Review Statuses

Forbidden review statuses:

- `compatibility_frozen`
- `ready_for_sparkbot`
- `ready_for_arc_bot`
- `ready_for_public_sparkbot`
- `ready_for_product_use`
- `production_ready`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_live_discovery`
- `approved_for_connection`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_physical_world`

## Public API Freeze Candidate Boundary

A future freeze review may consider only proof-public imports:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

The method-level dry-run candidate may be referenced only as a method on proof-public `LimaKernel`:

- `LimaKernel.preview_guardian_lifecycle(...)`

The freeze review must not promote `dry_run_candidate` imports, lifecycle preview result dataclasses, internal namespaces, or top-level runtime re-exports without a separate design and audit.

Forbidden consumer imports remain:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Non-Execution Review

Both proof audits must prove:

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

Missing evidence maps to `needs_missing_evidence`.

Contradictory evidence maps to `blocked_by_runtime_boundary`.

## Redaction Review

The freeze review must block if any input contains:

- raw prompts
- raw chat text
- raw office-task text
- raw customer records
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- API keys
- secrets
- headers
- cookies
- tokens
- passwords
- pairing codes
- unsafe command bodies
- live scan dumps
- private SSIDs
- raw Bluetooth MAC addresses
- raw BLE identifiers
- raw IP addresses
- raw MAC addresses
- device serial numbers
- precise physical location
- robot command payloads
- drone command payloads
- physical-world actuator payloads

Unredacted evidence must not be archived or used as freeze evidence.

## Sparkbot Freeze Review

Sparkbot side may count toward a future freeze only if its proof audit confirms:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector was invoked by LIMA
- no Sparkbot tool was invoked by LIMA
- no Sparkbot provider was invoked by LIMA
- no Sparkbot memory was invoked by LIMA
- no Sparkbot storage was invoked by LIMA
- no Sparkbot scheduler was invoked by LIMA
- no live terminal, browser, file, network, connector, model, scheduler, or external send behavior was introduced through LIMA

## Arc Bot Freeze Review

Arc Bot side may count toward a future freeze only if its proof audit confirms:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector was invoked by LIMA
- no Arc tool was invoked by LIMA
- no Arc provider was invoked by LIMA
- no Arc memory was invoked by LIMA
- no Arc storage was invoked by LIMA
- no office-system adapter was invoked by LIMA
- no live office connector, customer system, file, browser, process, network, scheduler, model, or external send behavior was introduced through LIMA

## Decision Table

| Condition | Review Status | Next Action |
| --- | --- | --- |
| Either packet is missing | `needs_consumer_packet` | Wait for consumer-owned packet |
| Either packet has redaction blockers | `needs_redaction` | Return to consumer team for redaction |
| Either proof audit is missing | `needs_missing_evidence` | Audit packet using proof results template |
| Either proof audit lacks pass status | `needs_missing_evidence` | Resolve audit findings first |
| Either proof audit reports runtime behavior | `blocked_by_runtime_boundary` | Do not start freeze |
| Either proof audit reports consumer repo boundary violation | `blocked_by_consumer_repo_boundary` | Do not start freeze |
| Either proof audit reports forbidden readiness claims | `blocked_by_claim_boundary` | Do not start freeze |
| Public API manifest changed after proof audits | `blocked_by_public_api_drift` | Re-audit against current API manifest |
| Both proof audits pass and all blockers are clear | `ready_for_dry_run_freeze_design` | Start separate freeze design branch |

## Future Freeze Design Boundary

If the freeze review reaches `ready_for_dry_run_freeze_design`, the next branch may only design a static compatibility freeze for the proof-public dry-run API surface.

That future design may define:

- frozen proof-public import list
- frozen non-execution invariants
- frozen package/version evidence requirements
- consumer packet audit references
- rollback criteria
- API drift handling
- next review cadence

That future design must not implement runtime behavior or approve product use.

## Reviewer Forbidden Actions

Reviewers must not:

- modify consumer repositories
- create or push consumer proof branches
- fetch, clone, scan, or inspect consumer repositories without explicit approval
- automate proof intake
- archive unredacted evidence
- run redaction scanners
- persist proof packet contents
- call models
- execute tools
- access connectors
- run schedulers
- perform browser/file/process/network actions
- perform live discovery
- connect to devices
- pair devices
- use credentials
- invoke Robo-OS
- control devices, robots, drones, or physical-world systems

## Recommended Next Branch

If this design is accepted:

`audit-lima-consumer-proof-compatibility-freeze-review`

If Sparkbot and Arc proof packets are supplied first:

`audit-consumer-owned-proof-results`
