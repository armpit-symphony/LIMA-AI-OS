# LIMA Consumer Proof Results Audit Template

## Template Status

This template is for LIMA-side human-reviewed audits of future Sparkbot and Arc Bot consumer-owned dry-run proof packets.

It does not create proof packets, audit missing proof packets, modify Sparkbot repositories, modify Arc Bot repositories, modify `lima/`, change package metadata, create runtime behavior, wire shells, automate intake, call models, execute tools, access connectors, persist events, run schedulers, use browser/file/process/network APIs, perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

It does not approve production integration.

## 1. Audit Identity

- Audit branch:
- Base commit:
- LIMA reviewer:
- Review date:
- Consumer repo:
- Consumer branch:
- Consumer team owner:
- Proof packet location:
- LIMA commit or version reviewed:
- Package name:
- Package version:

Expected consumer-owned proof branches:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot: `arc-lima-dry-run-boundary-proof`

The LIMA repo lane must not create, edit, or push those branches.

## 2. Reference Artifacts

Check the packet against:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`

## 3. Required Proof Evidence

The proof packet must include:

- `consumer_repo`
- `consumer_branch`
- `consumer_team_owner`
- `lima_repository_url`
- `lima_commit_or_package_version`
- `package_name`
- `package_version`
- `public_imports_used`
- `proof_archive_location`
- `import_method`
- `normalized_metadata_evidence`
- `capability_profile_evidence`
- `kernel_call_evidence`
- `dry_run_result_evidence`
- `simulated_discovery_evidence`
- `non_execution_invariant_evidence`
- `forbidden_surface_attestation`
- `redaction_attestation`
- `rollback_or_disable_plan`
- `final_proof_verdict`

Missing evidence must be classified as `needs_missing_evidence`.

## 4. Public API Import Review

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

## 5. Kernel Call Review

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

## 6. Optional Simulated Discovery Review

If `SimulatedDiscoveryAdapter` is used, the proof packet must show:

- explicit adapter usage
- `dry_run is True`
- `simulated_only is True`
- synthetic surfaces only
- inert surfaces only
- surfaces are not connectable
- surfaces are not controllable
- live discovery executed is False
- scan occurred is False
- connection attempted is False
- pairing attempted is False
- credentials used is False
- device control executed is False
- physical-world behavior occurred is False

If live discovery, scanning, connection, pairing, credential use, device access, Robo-OS access, robotics, drones, or physical-world behavior appear, classify as `blocked_by_runtime_boundary`.

## 7. Non-Execution Invariant Review

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

## 8. Redaction Review

Classify as `needs_redaction_before_review` if evidence includes:

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

## 9. Consumer-Specific Evidence

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

## 10. Audit Status

Allowed audit statuses:

- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

Forbidden audit statuses:

- `approved_for_production`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_live_discovery`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_physical_world`

The only passing status is `pass_for_dry_run_dependency_proof`.

That status does not mean production readiness.

## 11. Audit Output

Future completed audit report should include:

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

## 12. Next Branch Rules

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

## 13. Forbidden Surface Confirmation

This template does not authorize:

- modifying `lima/`
- modifying `pyproject.toml`
- modifying public Sparkbot repository files
- modifying Arc Bot repository files
- consumer integration implementation
- route wiring
- raw natural-language ingestion
- runtime `IntentEnvelope` creation
- live HumanInput bridge
- real Guardian decision authority
- approval enforcement
- provider/model calls
- tool execution
- connector access
- storage or persistence
- event spine persistence
- scheduler or background workers
- queues, daemons, subprocesses, or threads
- external sends
- browser actions
- file mutation
- process execution
- network actions
- live discovery
- scanning
- connection attempts
- pairing
- credential use or storage
- sockets
- OS network APIs
- Bluetooth or BLE APIs
- USB or serial APIs
- MQTT, Matter, or mDNS APIs
- IoT adapters
- Robo-OS adapters
- Sparkbot wiring
- Arc Bot wiring
- device control
- robotics
- drones
- physical-world behavior

## 14. Final Audit Verdict

- Audit status:
- Missing evidence:
- Boundary findings:
- Redaction findings:
- Consumer-specific findings:
- Recommended next branch:
- Production readiness: `not_production_ready`
