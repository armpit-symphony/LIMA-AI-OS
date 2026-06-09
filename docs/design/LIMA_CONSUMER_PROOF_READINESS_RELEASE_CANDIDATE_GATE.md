# LIMA Consumer Proof Readiness Release Candidate Gate

## Design Status

This document defines a LIMA-local release-candidate gate for Sparkbot and Arc Bot dry-run consumer proof readiness.

It is design-only. It does not create a release, tag a package, bump a version, start a compatibility freeze, receive
proof packets, archive evidence, audit proof packets, inspect consumer repositories, modify consumer repositories,
modify `lima/`, modify `tests/support/`, modify `pyproject.toml`, change package metadata, change public exports,
implement runtime behavior, wire shells, call models, execute tools, access connectors, persist data, run schedulers,
perform live discovery, connect to devices, invoke Robo-OS, control devices, control robots, control drones, or touch
physical-world systems.

It does not approve product or production integration.

## Purpose

The release-candidate gate answers one narrow question:

Can the current LIMA-local proof package be treated as a release candidate for requesting and receiving Sparkbot and Arc
Bot consumer-owned dry-run proof packets?

The only passing verdict is:

`ready_for_consumer_proof_request_release_candidate_only`

That means:

- LIMA-local contracts, docs, public API metadata, handoff materials, proof templates, proof gates, compatibility-freeze
  blockers, and static tests are ready enough to request redacted consumer-owned dry-run proof packets.
- Sparkbot and Arc Bot packets are still missing unless separately supplied by those teams.
- LIMA has not accepted, archived, or audited consumer proof packets in this branch.
- LIMA has not frozen compatibility.
- LIMA has not approved Sparkbot or Arc dependency use.
- LIMA has not approved product or production use.

## Current Gate Verdict

`ready_for_consumer_proof_request_release_candidate_only`

Current state:

| Area | Gate State | Meaning |
| --- | --- | --- |
| LIMA-local proof package | `release_candidate_for_proof_request` | docs and static guardrails are sufficient to request proof packets |
| Sparkbot proof packet | `not_received` | Sparkbot team has not supplied a redacted packet |
| Arc Bot proof packet | `not_received` | Arc Bot / LIMA Office team has not supplied a redacted packet |
| Sparkbot redaction review | `not_started` | cannot start until packet exists |
| Arc Bot redaction review | `not_started` | cannot start until packet exists |
| Sparkbot proof audit | `not_started` | cannot start until redacted packet exists |
| Arc Bot proof audit | `not_started` | cannot start until redacted packet exists |
| Public API compatibility freeze | `not_ready_for_freeze` | both proof audits must pass first |
| Product readiness | `not_production_ready` | live/product lanes remain blocked |

## Source Artifacts

This release-candidate gate is derived from:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `tests/fixtures/public_api/lima_public_api_manifest.json`
- `docs/design/LIMA_CONSUMER_PROOF_STATUS_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW.md`
- `docs/design/LIMA_CONSUMER_PROOF_PUBLIC_API_COMPATIBILITY_FREEZE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_PUBLIC_API_COMPATIBILITY_FREEZE_STATIC_TESTS_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_PUBLIC_API_COMPATIBILITY_FREEZE_AUDIT.md`
- `docs/audits/LIMA_GUARDIAN_DECISION_AUTHORITY_PUBLIC_API_METADATA_AUDIT.md`

If this gate conflicts with any source artifact, the stricter source artifact controls.

## Gate Inputs

Allowed gate inputs are LIMA-local documentation, metadata, fixtures, tests, and audits only:

- public API manifest and fixture metadata
- proof package docs
- proof handoff docs
- proof archive/intake/results audit templates
- proof acceptance gate docs/tests/audits
- proof ledger package docs/tests/audits
- public API compatibility-freeze docs/tests/audits
- validation output from this branch

Forbidden gate inputs:

- raw consumer proof packets
- raw chat text
- raw office-task text
- customer records
- raw attachments
- connector payloads
- provider payloads
- tool arguments
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
- raw BLE identifiers
- raw IP addresses
- raw MAC addresses
- device serial numbers
- precise physical location
- robot command payloads
- drone command payloads
- physical-world actuator payloads
- live webhooks
- production route payloads
- automated event streams

## Gate Pass Criteria

The gate may pass as `ready_for_consumer_proof_request_release_candidate_only` only when:

- proof-public imports are documented and tested
- method-level dry-run candidates are documented as optional and non-authoritative
- consumer-owned Sparkbot and Arc proof branches are named
- handoff package and delivery materials exist
- proof archive template exists
- proof intake response template exists
- proof results audit template exists
- acceptance gate exists
- readiness closeout package exists
- ledger package readiness gate exists
- public API compatibility-freeze design exists
- public API compatibility-freeze static tests are audited
- Sparkbot proof packet remains `not_received`
- Arc Bot proof packet remains `not_received`
- Sparkbot proof audit remains `not_started`
- Arc Bot proof audit remains `not_started`
- compatibility freeze remains `not_ready_for_freeze`
- product readiness remains `not_production_ready`
- redaction blockers are listed
- non-execution invariants are listed
- Sparkbot-specific evidence requirements are listed
- Arc-specific evidence requirements are listed
- forbidden imports are listed
- forbidden product/live/runtime claims are listed
- forbidden package actions are listed
- validation commands pass on the branch

## Public API Boundary

Consumer dry-run proof branches may use only proof-public imports from `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Optional method-level dry-run candidates:

- `LimaKernel.preview_guardian_lifecycle(...)`
- `LimaKernel.preview_guardian_decision_authority(...)`

Consumer proof branches must not use:

- `from lima import LimaKernel`
- unreviewed `dry_run_candidate` imports
- standalone preview result dataclass imports
- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Required Proof Shape

The release-candidate request may ask only for:

```text
consumer-owned branch
redacted already-normalized metadata in
default-deny CapabilityProfile
explicit LimaKernel.evaluate(...) dry-run call
optional explicit SimulatedDiscoveryAdapter for synthetic preview only
optional LimaKernel.preview_guardian_lifecycle(...) as non-authoritative metadata only
optional LimaKernel.preview_guardian_decision_authority(...) as non-authoritative metadata only
dry-run ExecutionResult out
redacted proof packet
repo-team-owned proof report
LIMA-side proof audit later
```

The request must not ask consumer teams to wire production routes, call models, execute tools, invoke connectors, write
storage, schedule work, open browsers, mutate files, spawn processes, access networks, discover live devices, connect,
pair, use credentials, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

## Required Non-Execution Invariants

Every requested proof packet must include evidence that:

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

Contradictory invariant evidence must be treated as:

`blocked_by_runtime_boundary`

## Consumer Branch Ownership

Sparkbot team should own:

`sparkbot-lima-dry-run-boundary-proof`

Arc Bot / LIMA Office team should own:

`arc-lima-dry-run-boundary-proof`

The LIMA repo team must not create, edit, push, fetch, clone, scan, inspect, or validate those branches unless the user
supplies explicit approved proof artifacts or explicitly approves read-only reference review.

## Sparkbot Proof Requirements

Sparkbot proof must remain missing until the Sparkbot repo team supplies redacted evidence that:

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
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Arc Bot Proof Requirements

Arc Bot / LIMA Office proof must remain missing until the Arc Bot / LIMA Office repo team supplies redacted evidence that:

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
- any simulated discovery preview was explicit, synthetic, inert, and dry-run only

## Redaction Gate

Consumer proof packets must not include:

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

If any appear, the packet must be classified as:

`needs_redaction_before_review`

Do not archive unredacted evidence.

## Gate Fail Conditions

The gate must fail if any source artifact or branch attempts to:

- claim Sparkbot readiness
- claim Arc Bot readiness
- claim public Sparkbot readiness
- claim product readiness
- claim production readiness
- claim compatibility freeze
- claim live integration readiness
- claim model-call readiness
- claim tool-execution readiness
- claim connector readiness
- claim storage readiness
- claim scheduler readiness
- claim live-discovery readiness
- claim connection readiness
- claim pairing readiness
- claim credential-use readiness
- claim Robo-OS readiness
- claim device-control readiness
- claim robotics readiness
- claim drone readiness
- claim physical-world readiness
- receive proof packets
- archive proof packets
- audit proof packets
- send responses
- persist a ledger
- create consumer branches
- inspect consumer repositories
- modify consumer repositories
- modify `lima/`
- add runtime behavior
- wire shells
- call models
- execute tools
- invoke connectors
- write storage
- run schedulers or background workers
- perform browser/file/process/network actions
- perform live discovery
- connect
- pair
- use credentials
- invoke Robo-OS
- control devices, robots, drones, or physical-world systems

## Manual Next-Step Decision

If this gate passes and no proof packets are supplied:

- operator may deliver the proof-only request package to Sparkbot and Arc Bot teams outside this branch
- LIMA repo remains waiting for consumer-owned packets
- no LIMA compatibility freeze may start
- no product readiness claim may be made

If Sparkbot or Arc Bot supplies a packet:

- do not process it in this branch
- start `audit-consumer-owned-proof-results`
- check redaction before archive or audit
- audit Sparkbot and Arc packets separately

If the gate needs machine-checkable coverage:

- a later branch may add static fixture/test coverage only

## Forbidden Release-Candidate Claims

This gate must not be described as:

- production-ready
- Sparkbot integrated
- Arc Bot integrated
- public Sparkbot ready
- compatibility frozen
- live integration approved
- model-call ready
- tool-execution ready
- connector-ready
- storage-ready
- scheduler-ready
- live-discovery ready
- connection-ready
- pairing-ready
- credential-use ready
- Robo-OS ready
- device-control ready
- robotics-ready
- drone-ready
- physical-world ready

## Forbidden Release-Candidate Actions

This gate must not trigger:

- consumer repository edits
- public Sparkbot repository changes
- Arc Bot repository changes
- creation or pushing of consumer proof branches by LIMA
- fetching, cloning, scanning, or inspecting consumer repositories without explicit approval
- automated proof intake
- proof archive crawling
- redaction scanning
- raw evidence storage
- receipt ledger persistence
- event spine persistence
- runtime behavior expansion
- live HumanInput bridge
- runtime `IntentEnvelope` creation
- real Guardian decision authority
- approval enforcement
- provider/model routing
- model calls
- tool execution
- connector access
- storage/persistence
- scheduler/background workers
- browser/file/process/network actions
- live discovery
- connection attempts
- pairing
- credential use or storage
- sockets
- OS network APIs
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

`audit-lima-consumer-proof-readiness-release-candidate-gate`
