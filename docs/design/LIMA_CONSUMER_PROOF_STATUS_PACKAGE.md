# LIMA Consumer Proof Status Package

## Package Status

This document is a docs-only status package for Sparkbot and Arc Bot repo teams.

It tells consumer repo teams what LIMA evidence is ready to hand off, what proof packet evidence LIMA needs next, and what LIMA reviewers may do after packets arrive.

It does not replace the handoff artifact, delivery note, archive template, intake response template, proof packet review checklist, redaction checklist, receipt ledger, readiness status rollup, public API manifest, compatibility freeze input matrix, or proof results audit template.

It does not create proof packets, receive proof packets, update the receipt ledger, archive evidence, audit proof results, inspect consumer repositories, modify consumer repositories, create consumer branches, implement intake automation, implement storage, implement runtime behavior, wire shells, call models, execute tools, access connectors, run schedulers, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve production integration.

## Current Package Verdict

`waiting_for_consumer_proof_packets`

LIMA has local proof guidance ready, but Sparkbot and Arc Bot are not proven consumers yet.

Current blockers:

- Sparkbot proof packet has not been received.
- Arc Bot proof packet has not been received.
- Sparkbot proof audit has not started.
- Arc Bot proof audit has not started.
- Compatibility freeze is blocked.
- Product use is blocked.

## Package Audience

This package is for:

- Sparkbot repo team
- Arc Bot / LIMA AI Office repo team
- LIMA reviewer
- Spark Pit Labs internal archive owner

This package is not:

- a public release note
- a production-readiness claim
- a Sparkbot integration claim
- an Arc Bot integration claim
- a compatibility freeze
- a runtime implementation plan
- a live discovery or device-readiness claim

## Source Artifacts Included By Reference

Consumer teams should use:

- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_RECEIPT_RESPONSE_EXAMPLES.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`

If this package conflicts with a source artifact, the source artifact controls.

## What LIMA Can Hand Off Now

LIMA can hand off proof-only guidance for consumer-owned dry-run branches.

Ready handoff materials:

- proof-stage public API manifest
- consumer proof handoff artifact
- consumer proof delivery note
- consumer proof archive template
- consumer proof intake response template
- consumer proof results audit template
- proof packet review checklist
- proof packet redaction checklist
- receipt ledger design
- receipt/response examples
- readiness status rollup
- static tests guarding receipt ledger, redaction checklist, receipt/response examples, and readiness rollup

These materials help Sparkbot and Arc Bot teams create proof packets. They do not prove Sparkbot or Arc Bot can use LIMA.

## What Sparkbot Team Must Send

Sparkbot team owns branch:

`sparkbot-lima-dry-run-boundary-proof`

Expected Sparkbot proof packet fields:

- `consumer_repo: sparkbot`
- `consumer_branch: sparkbot-lima-dry-run-boundary-proof`
- `consumer_team_owner`
- `lima_repository_url`
- `lima_commit_or_package_version`
- `package_name`
- `package_version`
- `import_method`
- `public_imports_used`
- `proof_archive_location`
- `normalized_metadata_evidence`
- `capability_profile_evidence`
- `kernel_call_evidence`
- `dry_run_result_evidence`
- `simulated_discovery_evidence`, if used
- `non_execution_invariant_evidence`
- `forbidden_surface_attestation`
- `redaction_attestation`
- `rollback_or_disable_plan`
- `final_proof_verdict`

Sparkbot-specific evidence must show:

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
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## What Arc Bot Team Must Send

Arc Bot / LIMA AI Office team owns branch:

`arc-lima-dry-run-boundary-proof`

Expected Arc proof packet fields:

- `consumer_repo: arc_bot`
- `consumer_branch: arc-lima-dry-run-boundary-proof`
- `consumer_team_owner`
- `lima_repository_url`
- `lima_commit_or_package_version`
- `package_name`
- `package_version`
- `import_method`
- `public_imports_used`
- `proof_archive_location`
- `normalized_metadata_evidence`
- `capability_profile_evidence`
- `kernel_call_evidence`
- `dry_run_result_evidence`
- `simulated_discovery_evidence`, if used
- `non_execution_invariant_evidence`
- `forbidden_surface_attestation`
- `redaction_attestation`
- `rollback_or_disable_plan`
- `final_proof_verdict`

Arc-specific evidence must show:

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
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Allowed Proof-Stage Imports

Consumer proof branches may use proof-public imports from `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Consumer proof branches must not use `dry_run_candidate` imports without explicit LIMA-side follow-up review.

Consumer proof branches must not import:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Required Proof Shape

Consumer proof branches must stop at:

```text
consumer-owned branch
redacted already-normalized metadata in
default-deny CapabilityProfile
explicit LimaKernel.evaluate(...) dry-run call
optional explicit SimulatedDiscoveryAdapter for synthetic preview only
dry-run ExecutionResult out
redacted proof packet
repo-team-owned proof report
```

LIMA must not create the consumer branch.

LIMA must not push consumer proof code.

LIMA must not fetch, clone, scan, or inspect consumer repositories without explicit approval.

## Required Non-Execution Invariants

Every proof packet must include evidence that:

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

Missing invariant evidence means the packet is not ready for proof acceptance.

Contradictory invariant evidence must be treated as a runtime boundary blocker.

## Redaction Gate

Consumer proof packets must be redacted before LIMA-side archive or audit.

Packets must not include:

- raw prompts
- raw chat text
- raw office-task text
- raw customer records
- raw attachments
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- headers
- cookies
- tokens
- passwords
- pairing codes
- unsafe command bodies
- live scan dumps
- private SSIDs
- raw Bluetooth MAC addresses
- raw IP or MAC addresses
- device serial numbers
- precise physical location
- robot or drone command payloads

If any appear, response status must be:

`needs_redaction_before_review`

## LIMA Reviewer Intake Flow

After a consumer proof packet is supplied, a LIMA reviewer should:

1. Confirm the packet source and consumer-owned branch.
2. Confirm the packet is dry-run proof only.
3. Run the redaction gate before archive or detailed audit.
4. Check package/version/import evidence.
5. Check normalized metadata and capability profile evidence.
6. Check explicit `LimaKernel.evaluate(...)` dry-run result evidence.
7. Check optional simulated discovery evidence, if present.
8. Check all non-execution invariants.
9. Check Sparkbot-specific or Arc-specific evidence.
10. Check forbidden claims.
11. Update receipt ledger manually only after redaction is acceptable.
12. Use `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md` for final LIMA-side audit.

This package does not automate intake, redaction, archive, ledger update, or audit.

## Response Status Rules

Allowed response statuses:

- `accepted_for_archive`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_claim_boundary`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `requires_followup_design`
- `requires_followup_audit`
- `not_ready_for_implementation`

Allowed proof audit statuses:

- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

Forbidden statuses:

- `approved_for_production`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_live_discovery`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_physical_world`
- `production_ready`
- `ready_for_live_integration`
- `ready_for_model_calls`
- `ready_for_tool_execution`
- `ready_for_connector_access`
- `ready_for_live_discovery`
- `ready_for_device_control`
- `ready_for_robo_os`
- `ready_for_physical_world`

The only passing proof audit status is:

`pass_for_dry_run_dependency_proof`

That status does not mean production readiness.

## Package Delivery Note

```text
Sparkbot and Arc Bot teams:

LIMA has local proof-only handoff guidance ready.

Please create your consumer-owned dry-run proof branch, import the proof-stage LIMA dependency candidate, call the non-executing dry-run kernel surface with redacted already-normalized metadata, and return a redacted proof packet using the archive template.

Do not wire production routes.
Do not send raw prompts, chat text, office-task text, customer records, credentials, connector payloads, provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads to LIMA.
Do not call models, tools, connectors, storage, schedulers, external sends, browsers, files, processes, networks, devices, Robo-OS, robots, drones, or physical-world systems through LIMA.

The first proof is normalized metadata in and dry-run ExecutionResult out.
```

## Current Product Blockers

Sparkbot and Arc Bot remain blocked from product use until later approved branches complete:

- both consumer proof packets received
- both packets pass redaction review
- both packets pass LIMA-side proof audit
- dry-run consumer compatibility freeze designed and audited
- stable public API versioning policy
- install/package verification strong enough for consumer use
- real Guardian request and decision lifecycle
- approval-required flow design
- approval enforcement implementation
- HumanInput bridge contract and implementation
- runtime `IntentEnvelope` creation contract and implementation
- provider/model boundary design and implementation
- tool execution boundary design and implementation
- connector boundary design and implementation
- scheduler/background-work boundary design and implementation
- event/spine persistence design
- storage interface implementation

## Forbidden Package Interpretations

This package must not be interpreted as approval for:

- Sparkbot product integration
- Arc Bot product integration
- public Sparkbot release integration
- production use
- compatibility freeze
- live HumanInput bridge
- raw natural-language execution
- runtime `IntentEnvelope` creation
- real Guardian decision authority
- approval enforcement
- provider/model calls
- tool execution
- connector access
- storage or persistence
- scheduler/background work
- browser/file/process/network actions
- live discovery
- scanning
- connection attempts
- pairing
- credential use or storage
- sockets
- Bluetooth/BLE APIs
- USB/serial APIs
- MQTT/Matter/mDNS APIs
- IoT adapters
- Robo-OS access
- device control
- robotics
- drones
- physical-world behavior

## Recommended Next Branch

If this package design is accepted:

`audit-lima-consumer-proof-status-package`

If Sparkbot or Arc Bot proof packets are supplied first:

`audit-consumer-owned-proof-results`
