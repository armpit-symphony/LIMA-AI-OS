# LIMA Consumer Proof Delivery Note

## Subject

LIMA dry-run proof package for Sparkbot and Arc Bot teams

## Delivery Status

LIMA has reached consumer-owned dry-run proof handoff readiness only.

This is not production integration approval. LIMA is not production-ready for Sparkbot or Arc Bot integration.

The first proof is normalized metadata in and dry-run `ExecutionResult` out.

## Audience

This note is for:

- Sparkbot repo team
- Arc Bot / LIMA AI Office repo team
- Spark Pit Labs internal archive owner

This is not a public release note, marketing statement, product-readiness claim, or integration announcement.

## LIMA Proof Package

Use these LIMA-local artifacts:

- `docs/handoffs/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT.md`
- `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`
- `tests/fixtures/consumer_proof_archive_template/consumer_proof_archive_template.json`
- `docs/audits/LIMA_CONSUMER_PROOF_HANDOFF_ARTIFACT_AUDIT.md`
- `docs/audits/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE_IMPLEMENTATION_FINAL_AUDIT.md`

Package validation evidence:

- `python -m compileall lima`
- `python -m pytest -q tests/test_lima_consumer_proof_archive_template.py -p no:cacheprovider`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`

## Consumer-Owned Branches

Sparkbot branch:

`sparkbot-lima-dry-run-boundary-proof`

Arc Bot branch:

`arc-lima-dry-run-boundary-proof`

These branches must be created and owned by their repo teams. They are not owned by the LIMA repo lane.

## Proof Shape

The allowed proof shape is:

```text
consumer-owned branch
already-normalized redacted metadata in
default-deny capability profile
LimaKernel.evaluate(...) dry-run call
optional explicit SimulatedDiscoveryAdapter for synthetic preview only
dry-run ExecutionResult out
archive proof packet
stop at repo-team audit
```

## Allowed Consumer-Team Actions

Each repo team may:

1. Create its consumer-owned dry-run proof branch.
2. Import or install the current LIMA dependency candidate.
3. Record the exact LIMA commit, tag, package version, or import method.
4. Build redacted already-normalized intent or office-task metadata locally.
5. Build a default-deny capability profile.
6. Call `LimaKernel.evaluate(...)` in dry-run mode.
7. Optionally pass an explicit `SimulatedDiscoveryAdapter` only for synthetic preview metadata.
8. Archive the dry-run `ExecutionResult`.
9. Fill out `docs/templates/LIMA_CONSUMER_PROOF_ARCHIVE_TEMPLATE.md`.
10. Prove no raw prompt, chat, office task, customer data, credential, connector payload, provider payload, tool argument, live scan dump, device identifier, physical location, or robot/drone payload entered LIMA.
11. Prove no production route, model call, tool call, connector access, storage write, scheduler run, external send, browser/file/process/network action, device action, Robo-OS access, robot/drone action, or physical-world action occurred.
12. Stop at proof report and repo-team audit.

## Required Warning

```text
This is a proof-only handoff.
Do not wire production routes.
Do not send raw prompts, raw chat, raw office-task text, customer records, credentials, connector payloads, provider payloads, tool arguments, live scan dumps, device identifiers, physical location, or robot/drone payloads to LIMA.
Do not expect LIMA to call models, tools, connectors, storage, schedulers, external sends, devices, Robo-OS, or physical-world systems.
The first proof is normalized metadata in and dry-run ExecutionResult out.
```

## Required Non-Execution Invariants

Every archived proof result must preserve:

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

## Must Not Claim

This delivery note does not claim:

- LIMA is production-ready
- Sparkbot is integrated with LIMA
- Arc Bot is integrated with LIMA
- LIMA can process raw chat or raw office-task text
- LIMA can create runtime `IntentEnvelope` records
- LIMA can create real Guardian decisions
- LIMA can enforce approval
- LIMA can route model/provider calls
- LIMA can execute tools
- LIMA can access connectors
- LIMA can persist events
- LIMA can schedule work
- LIMA can discover or connect to networks/devices
- LIMA can pair devices
- LIMA can use credentials
- LIMA can control devices, robots, drones, or physical-world systems

## Must Not Do

This delivery note does not authorize LIMA or consumer teams to:

- touch public Sparkbot repository files from this LIMA lane
- touch Arc Bot repository files from this LIMA lane
- modify `lima/`
- modify `tests/support/`
- implement consumer integration
- add route wiring
- add model/provider calls
- add tool execution
- add connector access
- add storage/persistence
- add event spine persistence
- add scheduler/background work
- add browser/file/process/network actions
- add live discovery
- add scanning
- add connection attempts
- add pairing
- add credential use or storage
- add sockets
- add Bluetooth/BLE APIs
- add USB/serial APIs
- add MQTT/Matter/mDNS APIs
- add Robo-OS access
- add device/robot/drone/physical-world behavior

## Remaining Product Blockers

Sparkbot and Arc Bot remain blocked from production LIMA use until later approved branches complete:

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

## Delivery Verdict

Ready to deliver as proof-only guidance.

Not ready for production integration.
