# LIMA Consumer Proof Ledger Package Readiness Gate

## Gate Status

This document designs a docs-only readiness gate for the LIMA-local consumer proof ledger package before Sparkbot and Arc Bot teams are asked to return dry-run proof packets.

It does not create, send, receive, archive, redact, or audit proof packets. It does not update the receipt ledger. It does not send responses. It does not start compatibility freeze. It does not inspect, fetch, clone, scan, modify, or push to Sparkbot, Arc Bot, LIMA Office, public Sparkbot, or consumer proof branches.

It does not modify `lima/`, `tests/`, `tests/support/`, `pyproject.toml`, package metadata, public exports, provider/model surfaces, adapters, storage, shell wiring, browser/file/process/network behavior, live discovery, connection attempts, pairing, credential use, Robo-OS, devices, robotics, drones, or physical-world systems.

It does not approve product or production integration.

## Purpose

The gate answers one narrow question:

Can the current LIMA-local consumer proof package be considered ready for operator handoff to Sparkbot and Arc Bot teams as a proof-only, dry-run dependency packet request?

The only passing answer is:

`ready_for_operator_handoff_request_only`

That means:

- LIMA can tell the operator what to ask Sparkbot and Arc Bot teams to produce.
- Sparkbot and Arc Bot proof packets are still missing.
- LIMA has not accepted any proof archive.
- LIMA has not audited consumer proof results.
- LIMA has not frozen compatibility.
- LIMA has not approved Sparkbot or Arc Bot dependency use.
- LIMA has not approved product or production use.

## Source Artifacts

This gate is derived from:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_STATUS_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_RECEIPT_RESPONSE_EXAMPLES.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/design/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW.md`
- `docs/design/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_INTAKE_LEDGER_CLOSEOUT_STATIC_TESTS.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`

If this gate conflicts with a source artifact, the stricter source artifact controls.

## Current Gate Verdict

`ready_for_operator_handoff_request_only`

Current state:

| Area | Gate State | Meaning |
| --- | --- | --- |
| LIMA proof package | `prepared_for_handoff_request` | local package docs and guardrails exist |
| Sparkbot proof packet | `not_received` | Sparkbot team has not supplied packet |
| Arc Bot proof packet | `not_received` | Arc Bot / LIMA Office team has not supplied packet |
| Sparkbot redaction review | `not_started` | cannot start until packet exists |
| Arc Bot redaction review | `not_started` | cannot start until packet exists |
| Sparkbot proof audit | `not_started` | cannot start until redacted packet exists |
| Arc Bot proof audit | `not_started` | cannot start until redacted packet exists |
| Compatibility freeze | `blocked` | both proof audits must pass first |
| Product readiness | `not_production_ready` | live/product lanes remain blocked |

## Gate Inputs

Allowed gate inputs are LIMA-local documentation and audit artifacts only:

- public API manifest
- handoff package
- handoff artifact
- delivery note
- dry-run proof delivery brief
- archive template
- intake response template
- proof results audit template
- status package
- readiness closeout
- readiness closeout package
- receipt ledger
- packet review checklist
- redaction checklist
- acceptance gate
- compatibility freeze input matrix
- compatibility freeze review
- intake ledger closeout
- ledger update gate closeout
- static-test implementation audits
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

## Required Package Artifacts

The gate can pass only if these documents exist and remain source-referenced:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_STATUS_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_CLOSEOUT_PACKAGE.md`
- `docs/design/LIMA_CONSUMER_PROOF_READINESS_STATUS_ROLLUP.md`
- `docs/design/LIMA_CONSUMER_PROOF_ACCEPTANCE_GATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_RECEIPT_RESPONSE_EXAMPLES.md`
- `docs/design/LIMA_DRY_RUN_CONSUMER_COMPATIBILITY_FREEZE_INPUT_MATRIX.md`
- `docs/design/LIMA_CONSUMER_PROOF_COMPATIBILITY_FREEZE_REVIEW.md`
- `docs/design/LIMA_SPARKBOT_ARC_PROOF_PACKET_INTAKE_LEDGER_CLOSEOUT.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT.md`

The gate should reference these latest local guardrails:

- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_AUDIT.md`
- `tests/fixtures/consumer_proof_ledger_update_closeout/consumer_proof_ledger_update_closeout.json`
- `tests/test_lima_consumer_proof_ledger_update_closeout_static.py`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_IMPLEMENTATION_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_UPDATE_CLOSEOUT_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`

## Required Public Proof Imports

The gate must preserve the proof-public import list:

- `import lima`
- `from lima.kernel import LimaKernel`
- `from lima.kernel import CapabilityProfile`
- `from lima.kernel import KernelRequest`
- `from lima.kernel import ExecutionResult`
- `from lima.kernel import KernelEvent`
- `from lima.kernel import GuardianStubDecision`
- `from lima.kernel import SimulatedDiscoveryAdapter`

Optional proof-stage method:

- `LimaKernel.preview_guardian_lifecycle(...)`

Forbidden consumer proof imports:

- `from lima import LimaKernel`
- unreviewed `dry_run_candidate` imports
- standalone lifecycle preview result dataclass imports
- `lima.io.*`
- `lima.persistence.*`
- `lima.harness.*`
- `lima.guardian.*`
- `lima.spine.*`
- `lima.services.*`
- `lima.shells.*`
- `lima.adapters.*`

## Required Consumer Branch Requests

Sparkbot team should own:

`sparkbot-lima-dry-run-boundary-proof`

Arc Bot / LIMA Office team should own:

`arc-lima-dry-run-boundary-proof`

The LIMA repo team must not create, edit, push, fetch, clone, scan, inspect, or validate those branches unless the user supplies explicit approved proof artifacts or explicitly approves read-only reference review.

## Required Proof Shape

The handoff request must ask for:

```text
consumer-owned branch
redacted already-normalized metadata in
default-deny CapabilityProfile
explicit LimaKernel.evaluate(...) dry-run call
optional explicit SimulatedDiscoveryAdapter for synthetic preview only
optional LimaKernel.preview_guardian_lifecycle(...) as non-authoritative metadata only
dry-run ExecutionResult out
redacted proof packet
repo-team-owned proof report
LIMA-side proof audit later
```

The request must not ask consumer teams to wire production routes, call models, execute tools, invoke connectors, write storage, schedule work, open browsers, mutate files, spawn processes, access networks, discover live devices, connect, pair, use credentials, invoke Robo-OS, control devices, control robots, control drones, or touch physical-world systems.

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

## Gate Pass Criteria

The gate may pass as `ready_for_operator_handoff_request_only` only when:

- required package artifacts are listed and exist
- proof-public imports are listed
- consumer-owned branches are identified
- handoff request wording is proof-only
- Sparkbot proof packet remains `not_received`
- Arc Bot proof packet remains `not_received`
- Sparkbot proof audit remains `not_started`
- Arc Bot proof audit remains `not_started`
- compatibility freeze remains `blocked`
- product readiness remains `not_production_ready`
- redaction blockers are listed
- non-execution invariants are listed
- Sparkbot-specific evidence requirements are listed
- Arc-specific evidence requirements are listed
- forbidden imports are listed
- forbidden package claims are listed
- forbidden package actions are listed
- validation commands pass on the branch

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

If the gate passes and no proof packets are supplied:

- operator may deliver the proof-only request package to Sparkbot and Arc Bot teams outside this branch
- LIMA repo remains waiting for consumer-owned packets
- no LIMA compatibility freeze may start

If Sparkbot or Arc Bot supplies a packet:

- do not process it in this branch
- start `audit-consumer-owned-proof-results`
- check redaction before archive or audit
- audit Sparkbot and Arc packets separately

If the package needs machine-checkable coverage:

- next branch should design fixture-backed static tests for this gate

## Forbidden Package Claims

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

## Forbidden Package Actions

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

If this design is accepted:

`audit-lima-consumer-proof-ledger-package-readiness-gate`

If Sparkbot or Arc Bot proof packets are supplied first:

`audit-consumer-owned-proof-results`
