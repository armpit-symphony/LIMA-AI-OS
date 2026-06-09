# LIMA Consumer Proof Operator Delivery Request

## Branch

`operator-deliver-lima-consumer-proof-request`

## Source Audit Tip

Use this LIMA commit as the current audited proof-stage reference unless a later audited branch supersedes it:

`6159dbc45e080c61d995f6be99669041ef3b373f`

That commit is the independent audit of the consumer proof operator-delivery static tests.

## Delivery Status

`manual_operator_delivery_request_only`

This file is a LIMA-local operator delivery request. It is intended for the operator to manually archive and deliver to
the Sparkbot and Arc Bot / LIMA Office repo teams.

This branch does not send this request, create proof packets, receive proof packets, archive proof packets, audit proof
packets, update ledgers, persist state, start compatibility freeze, inspect consumer repositories, create consumer
branches, modify consumer repositories, modify `lima/`, modify `tests/support/`, change package metadata, change public
exports, wire shells, call models, execute tools, access connectors, use storage, run schedulers, perform
browser/file/process/network actions, perform live discovery, connect, pair, use credentials, invoke Robo-OS, control
devices, control robots, control drones, or touch physical-world systems.

This request does not approve Sparkbot dependency use, Arc Bot dependency use, product readiness, production readiness,
or public Sparkbot release readiness.

## Required Delivery Boundary

Include this boundary with the manual request:

```text
This is a proof-only LIMA handoff package.
Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads,
provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads
to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, devices, Robo-OS,
or physical-world systems.
The first proof is normalized metadata in and dry-run ExecutionResult out.
```

## Artifacts To Manually Deliver

Deliver these LIMA-local artifacts by operator-controlled manual means only:

- `docs/public_api/LIMA_PUBLIC_API_MANIFEST.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_OPERATOR_DELIVERY_REQUEST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_LEDGER_PACKAGE_READINESS_GATE_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_OPERATOR_DELIVERY_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`

Do not deliver raw proof packet contents, raw chat text, raw office-task text, customer records, connector payloads,
provider payloads, tool arguments, credentials, headers, cookies, tokens, passwords, pairing codes, live scan dumps,
private SSIDs, raw Bluetooth identifiers, raw IP or MAC addresses, device serial numbers, precise physical location,
robot command payloads, drone command payloads, or physical-world actuator payloads.

## Sparkbot Team Request

Manually send this request to the Sparkbot repo team:

```text
Please create `sparkbot-lima-dry-run-boundary-proof` in the Sparkbot repo.

Use LIMA commit `6159dbc45e080c61d995f6be99669041ef3b373f` or a later audited LIMA commit supplied by the operator.
Use only proof-stage LIMA imports.
Build redacted already-normalized Sparkbot intent metadata locally.
Call `LimaKernel.evaluate(...)` with a default-deny capability profile.
Optionally pass `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata.
Optionally call `LimaKernel.preview_guardian_lifecycle(...)` as non-authoritative preview metadata only.

Return a redacted proof packet using `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`.

Do not wire public routes, mutate Sparkbot tasks/messages, invoke Sparkbot connectors/tools/providers/memory/storage/
schedulers, send raw chat text or prompts to LIMA, call models, execute tools, access storage, run browser/file/process/
network actions, perform live discovery, connect, pair, use credentials, invoke Robo-OS, control devices, control robots,
control drones, or touch physical-world systems through LIMA.
```

## Arc Bot / LIMA Office Team Request

Manually send this request to the Arc Bot / LIMA Office repo team:

```text
Please create `arc-lima-dry-run-boundary-proof` in the Arc Bot / LIMA Office repo.

Use LIMA commit `6159dbc45e080c61d995f6be99669041ef3b373f` or a later audited LIMA commit supplied by the operator.
Use only proof-stage LIMA imports.
Build redacted already-normalized Arc office-task metadata locally.
Call `LimaKernel.evaluate(...)` with a default-deny capability profile.
Optionally pass `SimulatedDiscoveryAdapter` only for explicit synthetic preview metadata.
Optionally call `LimaKernel.preview_guardian_lifecycle(...)` as non-authoritative preview metadata only.

Return a redacted proof packet using `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`.

Do not wire production office routes, mutate Arc tasks/projects/notes/forms/records/customer files, trigger schedulers
or background workers, invoke Arc connectors/tools/providers/memory/storage/office-system adapters, send raw office-task
text or customer records to LIMA, call models, execute tools, access storage, run browser/file/process/network actions,
perform live discovery, connect, pair, use credentials, invoke Robo-OS, control devices, control robots, control drones,
or touch physical-world systems through LIMA.
```

## Required Returned Evidence

Each consumer team should return a redacted proof packet containing:

- consumer repo
- consumer branch
- consumer team owner
- exact LIMA repository URL
- exact LIMA commit, tag, package version, or import method
- public imports used
- redacted already-normalized metadata evidence
- default-deny capability profile evidence
- explicit `LimaKernel.evaluate(...)` dry-run call evidence
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

## Required Non-Execution Invariants

Every returned proof packet must include evidence that:

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

Missing evidence remains `needs_missing_evidence`.

Contradictory execution evidence remains `blocked_by_runtime_boundary`.

## Delivery Controls

The operator delivery request preserves:

- consumer branches are repo-team owned
- LIMA repo does not create or inspect consumer branches
- proof packets are not accepted in this branch
- returned proof must be redacted before archive or audit
- proof archive and proof audit happen only in later approved branches
- Sparkbot and Arc packets are audited separately
- compatibility freeze starts only after both proof audits pass
- production readiness remains blocked

## After Manual Delivery

If the operator manually delivers the request and no consumer packet is supplied:

- LIMA remains waiting
- no compatibility freeze may start
- no product-readiness claim may be made

If Sparkbot or Arc Bot supplies a packet:

- do not process it in this branch
- start `audit-consumer-owned-proof-results`
- check redaction before archive or audit
- audit Sparkbot and Arc packets separately

## Source Artifacts

This request is derived from:

- `docs/design/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE_OPERATOR_DELIVERY.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_PACKAGE.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/handoffs/LIMA_CONSUMER_PROOF_DELIVERY_NOTE.md`
- `docs/handoffs/LIMA_SPARKBOT_ARC_DRY_RUN_PROOF_DELIVERY_BRIEF.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/audits/LIMA_CONSUMER_PROOF_OPERATOR_DELIVERY_STATIC_TESTS_IMPLEMENTATION_INDEPENDENT_AUDIT.md`

If this request conflicts with a source artifact, the stricter source artifact controls.

## Recommended Next Branch

If this operator request is accepted and no proof packet has been supplied:

`audit-lima-consumer-proof-operator-delivery-request`

If Sparkbot or Arc Bot proof packets are supplied first:

`audit-consumer-owned-proof-results`
