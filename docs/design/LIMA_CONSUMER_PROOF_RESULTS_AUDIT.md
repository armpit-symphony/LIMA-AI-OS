# LIMA Consumer Proof Results Audit Design

## Purpose

This document designs the LIMA-side audit process for future Sparkbot and Arc Bot consumer-owned dry-run proof result packets.

The audit exists to decide whether repo-team proof packets demonstrate safe dependency-readiness for the current LIMA proof-stage public API.

This branch is design-only. It does not audit any real Sparkbot or Arc proof packet, modify consumer repositories, modify `lima/`, change package metadata, create runtime behavior, create shell wiring, ingest raw user data, automate intake, call models, execute tools, access connectors, persist events, run schedulers, use browser/file/process/network APIs, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

## Audit Inputs

Allowed future inputs:

- Sparkbot repo team proof archive packet
- Arc Bot / LIMA AI Office repo team proof archive packet
- LIMA public API manifest reference
- LIMA consumer proof archive template
- LIMA consumer proof intake response template
- human-written repo-team question or blocker summary
- human-written redaction issue summary

Forbidden future inputs:

- public Sparkbot source changes from this LIMA lane
- Arc Bot source changes from this LIMA lane
- live webhooks
- production route payloads
- raw chat exports
- raw office-task exports
- customer record dumps
- raw connector/provider/tool payloads
- credentials
- headers
- cookies
- tokens
- live scan dumps
- raw device identifiers
- precise physical location
- robot/drone command payloads

If a future proof packet contains forbidden input evidence, the LIMA audit must stop and classify the packet as `needs_redaction_before_review`.

## Required Reference Artifacts

Future proof-result audits must check the consumer packet against:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`

The proof packet must name the exact LIMA commit or package version it used.

## Expected Consumer Branches

Expected future consumer-owned proof branches:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot: `arc-lima-dry-run-boundary-proof`

The LIMA repo lane must not create, edit, or push those branches.

## Required Proof Evidence

Every consumer proof packet must include:

- consumer repo
- consumer branch
- consumer team owner
- LIMA repository URL
- LIMA commit or package version
- package name
- package version
- public imports used
- proof archive location
- import method
- normalized metadata evidence
- capability profile evidence
- kernel call evidence
- dry-run result evidence
- optional simulated discovery evidence if used
- non-execution invariant evidence
- forbidden surface attestation
- redaction attestation
- rollback or disable plan
- final proof verdict

## Public API Evidence Review

The proof packet must show that consumer code used only proof-stage imports.

Allowed proof-stage imports:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Imports requiring follow-up review:

- any `dry_run_candidate` import from `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`

Forbidden consumer imports:

- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

If forbidden consumer imports are present, classify as `blocked_by_consumer_repo_boundary`.

## Kernel Call Evidence Review

The proof packet must show:

- already-normalized metadata in
- no raw natural-language parser in LIMA
- `LimaKernel.evaluate(...)` called explicitly
- no hidden adapter dispatch
- no runtime `IntentEnvelope` creation
- no real `GuardianDecision` authority
- no approval enforcement
- redacted result evidence out

Allowed result states:

- `proposed`
- `approval_required`
- `blocked`

Any result state claiming execution must be classified as `blocked_by_runtime_boundary`.

## Optional Simulated Discovery Review

If the consumer proof uses `SimulatedDiscoveryAdapter`, it must show:

- adapter is passed explicitly
- `dry_run` is true
- `simulated_only` is true
- surfaces are synthetic
- surfaces are inert
- surfaces are not connectable
- surfaces are not controllable
- no live discovery occurred
- no scan occurred
- no connection attempt occurred
- no pairing occurred
- no credential use occurred
- no device control occurred
- no physical-world behavior occurred

If a proof packet includes live discovery, scanning, connection, pairing, credential use, device access, Robo-OS access, robotics, drones, or physical-world behavior, classify as `blocked_by_runtime_boundary`.

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

Missing invariant evidence must be classified as `needs_missing_evidence`.

Contradictory invariant evidence must be classified as `blocked_by_runtime_boundary`.

## Redaction Review

The audit must classify the proof packet as `needs_redaction_before_review` if it includes:

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

LIMA must not archive unredacted consumer evidence.

## Consumer-Specific Evidence Review

### Sparkbot

Sparkbot proof packet must show:

- no raw chat text was sent to LIMA
- no public Sparkbot production route was wired
- no Sparkbot task was created or mutated
- no Sparkbot message was sent or mutated
- no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA

### Arc Bot / LIMA AI Office

Arc proof packet must show:

- no raw office-task text was sent to LIMA
- no customer record payload was sent to LIMA
- no customer communication was sent
- no Arc production route was wired
- no Arc task, project, note, form, record, or customer file was created or mutated
- no Arc scheduler or background worker was triggered
- no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA

## Audit Statuses

Allowed LIMA-side proof-result audit statuses:

- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

Forbidden LIMA-side proof-result audit statuses:

- `approved_for_production`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_live_discovery`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_physical_world`

## Pass Criteria

The only passing result is:

`pass_for_dry_run_dependency_proof`

That status means only:

- the consumer proof packet is redacted
- the consumer proof packet references an exact LIMA commit or version
- consumer imports match the proof-stage public API manifest
- consumer metadata is already normalized
- the kernel call is dry-run only
- result evidence preserves all non-execution invariants
- no forbidden surfaces are present
- no production or live integration claims are made

It does not mean production readiness.

## Required Output Shape

Future audit report should include:

- branch
- base commit
- consumer repo
- consumer branch
- LIMA commit or version reviewed
- proof packet location
- public API import review
- package/version pin review
- normalized metadata review
- kernel call review
- simulated discovery review if applicable
- non-execution invariant review
- redaction review
- forbidden surface review
- consumer-specific findings
- missing evidence
- audit status
- validation result
- recommended next branch

## Next Branch Rules

If both Sparkbot and Arc proof packets pass:

- recommended next branch may be `design-lima-dry-run-consumer-compatibility-freeze`

If one packet passes and one is missing:

- recommended next branch should be `revise-consumer-proof-evidence`

If redaction is missing:

- response must be `needs_redaction_before_review`
- recommended next branch should be `revise-consumer-proof-evidence`

If forbidden runtime behavior appears:

- response must be `blocked_by_runtime_boundary`
- recommended next branch should be `design-lima-runtime-blocker-resolution`

If forbidden production claims appear:

- response must be `blocked_by_claim_boundary`
- recommended next branch should be `audit-production-readiness-blockers`

If consumer teams ask for an API addition:

- response should be `requires_lima_design_followup`
- recommended next branch should be `design-lima-consumer-api-gap-response`

## Later Implementation Branch

The next implementation-shaped branch may be:

`implement-lima-consumer-proof-results-audit-template`

That branch may only add:

- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `tests/fixtures/consumer_proof_results_audit/consumer_proof_results_audit.json`
- `tests/test_lima_consumer_proof_results_audit_template.py`
- `docs/audits/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE_IMPLEMENTATION_AUDIT.md`

It must not modify `lima/`, `pyproject.toml`, consumer repositories, runtime behavior, providers, tools, connectors, storage, schedulers, browser/file/process/network behavior, live discovery, device behavior, Robo-OS, robotics, drones, or physical-world systems.

## Recommended Next Branch

`audit-lima-consumer-proof-results-audit-design`

That branch should independently audit this design before any proof-results audit template is implemented.
