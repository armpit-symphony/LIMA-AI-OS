# LIMA Consumer Proof Archive Template

## Template Status

This template is for consumer-owned dry-run proof archives only.

It does not approve production integration, live routes, raw input ingestion, model calls, tool execution, connector access, storage, scheduler/background work, live discovery, network/device behavior, Robo-OS access, robotics, drones, or physical-world behavior.

## 1. Branch And Owner

- Consumer repo:
- Consumer branch:
- Consumer team owner:
- Proof date:
- Proof author:
- Reviewer:
- LIMA handoff artifact:
- LIMA handoff audit:

Expected branch names:

- Sparkbot: `sparkbot-lima-dry-run-boundary-proof`
- Arc Bot: `arc-lima-dry-run-boundary-proof`

## 2. LIMA Dependency Reference

- LIMA repo:
- LIMA commit:
- LIMA branch or tag:
- LIMA package version, if any:
- Import method:
- Public imports used:

Allowed proof-stage public imports:

- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import SimulatedDiscoveryAdapter`

No LIMA internals should be imported.

## 3. Consumer Proof Scope

- Proof goal:
- Proof is dry-run only: `true`
- Production routes touched: `false`
- Consumer state mutated: `false`
- External side effects observed: `false`
- Runtime claims made: `false`

The proof must claim only:

```text
This consumer repo can import the current LIMA dependency candidate and call the non-executing dry-run kernel surface with already-normalized redacted metadata, while preserving all non-execution invariants.
```

## 4. Input Evidence

- Normalized metadata builder or fixture:
- Source surface metadata:
- Shell ID redacted: `true`
- Actor ID redacted: `true`
- Session ID redacted: `true`
- Context refs only: `true`
- Raw input excluded: `true`
- Sensitive payloads excluded: `true`

Allowed input evidence:

- redacted shell identity
- redacted actor identity
- redacted session identity
- already-normalized intent metadata
- already-normalized office-task metadata
- default-deny capability profile
- source surface metadata
- context references only
- synthetic or simulated discovery metadata
- redacted approval-boundary hints

Forbidden input evidence:

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

## 5. Capability Profile Evidence

Expected default-deny capability values:

- `model_calls: false`
- `memory_write: false`
- `task_state_write: false`
- `connector_read: false`
- `connector_write: false`
- `external_send: false`
- `file_write: false`
- `process_execute: false`
- `browser_control: false`
- `device_control: false`
- `robotics_actuation: false`
- `drone_actuation: false`
- `scheduler_run: false`
- `connection_attempt: false`
- `device_pairing: false`
- `credential_use: false`
- `physical_world_actuation: false`

If any simulated-only discovery capability is enabled, explain why it remains synthetic, inert, dry-run only, and non-executing:

- Simulated discovery explanation:

## 6. Kernel Call Evidence

- Kernel entrypoint: `LimaKernel.evaluate`
- Request type:
- Evaluate called: `true`
- Dry run requested: `true`
- Raw language parser used: `false`
- HumanInput bridge used: `false`
- IntentEnvelope created: `false`
- Guardian authority created: `false`

Do not include raw prompts, customer records, credentials, or live connector payloads.

## 7. Optional Simulated Discovery Evidence

Complete this section only if `SimulatedDiscoveryAdapter` is explicitly used.

- Simulated adapter used:
- Simulated only:
- Dry run:
- Synthetic surfaces only:
- Live discovery executed: `false`
- Connection attempted: `false`
- Pairing attempted: `false`
- Credentials used: `false`
- Session opened: `false`
- Device control executed: `false`
- Physical world executed: `false`

The proof must not scan, discover, connect, pair, use credentials, open sockets, call OS network APIs, call Bluetooth/BLE APIs, call USB/serial APIs, call MQTT/Matter/mDNS APIs, or touch devices.

## 8. Dry-Run Result Evidence

- Result status:
- Guardian stub summary:
- Event refs:
- Redacted audit summary:
- ExecutionResult sample redacted:

Allowed result states:

- `proposed`
- `approval_required`
- `blocked`

Do not archive a result that claims execution, dispatch, persistence, approval enforcement, model calls, connector access, device access, or physical-world behavior occurred.

## 9. Non-Execution Invariant Checklist

Required values:

- `executable: false`
- `execution_allowed: false`
- `side_effects_allowed: false`
- `dispatch_allowed: false`
- `persistence_allowed: false`
- `dry_run: true`
- `model_calls_allowed: false`
- `model_calls_executed: false`
- `live_discovery_executed: false`
- `connection_attempted: false`
- `pairing_attempted: false`
- `credentials_used: false`
- `session_opened: false`
- `device_control_executed: false`
- `physical_world_allowed: false`
- `physical_world_executed: false`
- `guardian_decision_created: false`
- `approval_enforced: false`
- `humaninput_bridge_active: false`
- `sparkbot_wiring_active: false`
- `robo_os_wiring_active: false`
- `adapter_active: false`
- `tool_execution_allowed: false`
- `driver_execution_allowed: false`
- `scheduler_active: false`
- `external_calls_allowed: false`

## 10. Forbidden Surface Checklist

Confirm the proof did not touch:

- production route wiring
- raw natural-language execution
- raw prompt parsing in LIMA
- runtime `IntentEnvelope` creation
- live HumanInput bridge
- real Guardian decisions
- approval enforcement
- provider routing
- model calls
- tool execution
- connector reads or writes
- memory writes
- task state writes
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
- WiFi connection attempts
- Bluetooth or BLE connection attempts
- USB or serial connection attempts
- MQTT, Matter, or mDNS calls
- pairing
- credential use or storage
- device control
- Robo-OS access
- robotics
- drones
- physical-world behavior

## 11. Redaction And Sensitive-Data Checklist

Confirm no archive evidence contains:

- raw prompts
- raw chat text
- raw office-task text
- raw customer records
- raw connector records
- raw provider payloads
- raw tool arguments
- credentials
- headers
- cookies
- tokens
- passwords
- pairing codes
- private SSIDs
- raw Bluetooth MAC addresses
- raw IP or MAC addresses
- device serial numbers
- precise physical location
- robot or drone command payloads

If any item is present, the proof fails until redacted.

## 12. Consumer-Specific Evidence

### Sparkbot

- Proof no raw chat text was sent to LIMA:
- Proof no public Sparkbot production route was wired:
- Proof no Sparkbot task was created or mutated:
- Proof no Sparkbot message was sent or mutated:
- Proof no Sparkbot connector, tool, provider, memory, storage, or scheduler was invoked by LIMA:

### Arc Bot

- Proof no raw office-task text was sent to LIMA:
- Proof no customer record payload was sent to LIMA:
- Proof no customer communication was sent:
- Proof no Arc production route was wired:
- Proof no Arc task, project, note, form, record, or customer file was created or mutated:
- Proof no Arc scheduler or background worker was triggered:
- Proof no Arc connector, tool, provider, memory, storage, or office-system adapter was invoked by LIMA:

## 13. Rollback Or Disable Plan

- Proof branch disable step:
- Dependency revert step:
- Feature flag or import gate, if any:
- Owner to contact:
- Evidence archive location:

Rollback must not depend on live LIMA services because no live LIMA service is approved in this proof stage.

## 14. Open Blockers

Carry forward these current LIMA blockers:

- stable public API versioning policy
- stronger install/package verification if needed
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
- consumer-owned proof branch audit in each repo

## 15. Final Proof Verdict

Allowed verdicts:

- `pass_for_dry_run_proof_only`
- `needs_redaction`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_missing_evidence`

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
