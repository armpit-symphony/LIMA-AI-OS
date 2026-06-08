# LIMA Sparkbot / Arc Dry-Run Proof Delivery Brief

## Brief Status

This is the current operator-facing delivery brief for Sparkbot and Arc Bot repo teams.

It is docs-only. It does not create proof packets, receive proof packets, update the receipt ledger, archive evidence, audit proof results, inspect consumer repositories, modify consumer repositories, create consumer branches, implement intake automation, implement storage, implement runtime behavior, wire shells, call models, execute tools, access connectors, run schedulers, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve production integration.

## Current LIMA Commit To Reference

Use this LIMA commit as the current proof-stage reference unless a later audited branch supersedes it:

`58ecd442d82f0c15cedb650b60aaed7835b0a9e1`

That commit is the independent audit of the Sparkbot / Arc dry-run boundary proof design.

## Current Verdict

`ready_for_consumer_owned_dry_run_proof_handoff_only`

LIMA is ready to hand proof instructions to Sparkbot and Arc Bot repo teams.

LIMA is not ready for:

- Sparkbot product integration
- Arc Bot product integration
- public Sparkbot release wiring
- dry-run compatibility freeze
- live HumanInput bridge
- raw natural-language execution
- runtime `IntentEnvelope` creation
- real Guardian decision authority
- approval enforcement
- provider/model calls
- tool execution
- connector access
- storage/persistence
- scheduler/background work
- live discovery
- connection attempts
- pairing
- credential use
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## What Changed Recently

The latest LIMA-local readiness work added:

- Guardian lifecycle preview public API metadata:
  - `LimaKernel.preview_guardian_lifecycle(...)` is documented as `method_level_dry_run_candidate`.
  - It is reachable only through proof-public `LimaKernel`.
  - Its result dataclasses are not public imports.
  - It is preview metadata only, not Guardian authority.
- Sparkbot / Arc dry-run boundary proof design and audit:
  - consumer proof branches remain repo-team owned
  - LIMA does not touch public Sparkbot or Arc repositories
  - proof is normalized metadata in and dry-run result out
  - optional simulated discovery remains explicit, synthetic, inert, and dry-run only

## Allowed Proof-Stage Imports

Consumer proof branches may use only:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Optional method-level dry-run candidate:

- `LimaKernel.preview_guardian_lifecycle(...)`

Consumer proof branches must not import lifecycle preview result dataclasses as public API.

Consumer proof branches must not import:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Sparkbot Team Instruction

```text
Please create `sparkbot-lima-dry-run-boundary-proof` in the Sparkbot repo.

Use LIMA commit `58ecd442d82f0c15cedb650b60aaed7835b0a9e1` or a later audited LIMA commit supplied by the operator.

Use only proof-stage LIMA imports. Build redacted already-normalized Sparkbot intent metadata locally. Call `LimaKernel.evaluate(...)` with dry-run metadata. Optionally pass `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata. Optionally call `LimaKernel.preview_guardian_lifecycle(...)` as non-authoritative preview metadata only.

Return a redacted proof packet using the LIMA proof archive template.

Do not wire public routes. Do not send raw chat text, prompts, connector payloads, provider payloads, tool arguments, credentials, headers, cookies, tokens, memory records, task payloads, browser/file/process/network payloads, live scan dumps, device identifiers, Robo-OS payloads, robot payloads, drone payloads, or physical-world command payloads to LIMA.

Do not call models, tools, connectors, storage, schedulers, external sends, browser/file/process/network surfaces, devices, Robo-OS, robots, drones, or physical-world systems through LIMA.
```

## Arc Bot Team Instruction

```text
Please create `arc-lima-dry-run-boundary-proof` in the Arc Bot / LIMA Office repo.

Use LIMA commit `58ecd442d82f0c15cedb650b60aaed7835b0a9e1` or a later audited LIMA commit supplied by the operator.

Use only proof-stage LIMA imports. Build redacted already-normalized Arc office-task metadata locally. Call `LimaKernel.evaluate(...)` with dry-run metadata. Optionally pass `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata. Optionally call `LimaKernel.preview_guardian_lifecycle(...)` as non-authoritative preview metadata only.

Return a redacted proof packet using the LIMA proof archive template.

Do not wire production office workflows. Do not send raw office-task text, customer records, customer files, form contents, connector payloads, provider payloads, tool arguments, credentials, headers, cookies, tokens, storage records, scheduler payloads, browser/file/process/network payloads, live scan dumps, device identifiers, office-system adapter payloads, Robo-OS payloads, robot payloads, drone payloads, or physical-world command payloads to LIMA.

Do not call models, tools, connectors, storage, schedulers, external sends, browser/file/process/network surfaces, office-system adapters, devices, Robo-OS, robots, drones, or physical-world systems through LIMA.
```

## Required Proof Packet Evidence

Each repo team must return:

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

That verdict does not mean production readiness.

## Required Non-Execution Evidence

Every proof result must show:

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

## LIMA Reviewer Flow After Packets Arrive

1. Confirm packet source and consumer-owned branch.
2. Run redaction review before archiving.
3. Do not archive unredacted evidence.
4. Use `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.
5. Audit Sparkbot and Arc packets separately.
6. Do not start compatibility freeze until both audits pass as `pass_for_dry_run_dependency_proof`.

## Source Artifacts

Use these LIMA-local references:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/design/LIMA_SPARKBOT_ARC_DRY_RUN_BOUNDARY_PROOF.md`
- `docs/audits/LIMA_SPARKBOT_ARC_DRY_RUN_BOUNDARY_PROOF_DESIGN_AUDIT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`

If this brief conflicts with a source artifact, the source artifact controls.

## Recommended Next Branch

If consumer proof packets are supplied:

`audit-consumer-owned-proof-results`

If LIMA continues locally without packets:

`audit-lima-sparkbot-arc-dry-run-proof-delivery-brief`
