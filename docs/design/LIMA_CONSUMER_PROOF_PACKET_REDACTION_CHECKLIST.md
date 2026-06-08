# LIMA Consumer Proof Packet Redaction Checklist

## Checklist Status

This checklist is for human-reviewed redaction screening of future Sparkbot and Arc Bot consumer-owned dry-run proof packets before LIMA archives or audits them.

It is docs-only. It does not implement a redaction engine, parser, scanner, intake service, storage system, archive writer, database, queue, scheduler, worker, webhook, notification sender, model call, connector, adapter, shell wiring, runtime behavior, live discovery, connection attempt, device behavior, Robo-OS behavior, robotics, drones, or physical-world behavior.

It does not inspect consumer repositories. It does not modify Sparkbot repositories, Arc Bot repositories, public release repositories, `lima/`, `tests/support/`, `pyproject.toml`, package metadata, public exports, or consumer proof branches.

It does not approve production integration.

## Purpose

The redaction checklist gives LIMA reviewers a pre-audit gate for consumer-owned proof packets.

It exists to prevent:

- archiving unredacted consumer proof evidence
- auditing packets that contain sensitive raw payloads
- treating redaction attestations as runtime approval
- storing credentials, customer data, raw prompts, network identifiers, device identifiers, or physical-world evidence in this repo
- starting compatibility freeze work before both consumer packets pass redaction and proof audit

## Relationship To Existing Artifacts

Use this checklist before:

- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`

Use this checklist with:

- `docs/REDACTION_PRIVACY_CONTRACT.md`
- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`

This checklist does not replace the proof packet review checklist. It only decides whether supplied evidence is safe enough to archive and audit.

## Entry Conditions

Do not begin redaction review unless:

- the user has supplied a proof packet or proof packet location
- the packet is described as Sparkbot-owned or Arc Bot-owned proof evidence
- the packet is intended for dry-run dependency proof only
- the packet is not a request to modify a consumer repo
- the packet is not a request to fetch, clone, scan, or inspect a consumer repo without explicit approval
- the packet is not a request to run runtime behavior, model calls, tool calls, connectors, storage, schedulers, live discovery, Robo-OS, devices, robots, drones, or physical-world behavior

If entry conditions fail, stop and use:

`docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`

## Required Redaction Attestation Fields

Every submitted packet should include a human-written redaction attestation with:

- `consumer_repo`
- `consumer_branch`
- `consumer_team_owner`
- `proof_packet_location`
- `redaction_reviewer`
- `redaction_review_date`
- `redaction_scope`
- `redaction_status`
- `redacted_evidence_refs`
- `withheld_sensitive_evidence_summary`
- `known_sensitive_categories_removed`
- `known_sensitive_categories_remaining`
- `redaction_limitations`
- `safe_to_archive`
- `safe_to_audit`
- `production_readiness`

If this attestation is missing, classify the packet as:

`needs_redaction_before_review`

## Allowed Redaction Statuses

Allowed statuses:

- `redacted_safe_for_archive`
- `redacted_safe_for_audit`
- `needs_redaction_before_review`
- `blocked_unredacted_sensitive_evidence`
- `needs_missing_redaction_attestation`
- `needs_human_redaction_review`

Required production readiness value:

`not_production_ready`

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
- `compatibility_frozen`

## Blocker Categories

If any blocker appears in supplied evidence, stop before archive or proof audit and classify as:

`blocked_unredacted_sensitive_evidence`

Blockers:

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
- raw IP addresses
- raw MAC addresses
- device serial numbers
- precise physical location
- robot command payloads
- drone command payloads
- physical-world actuator payloads
- production route payloads
- customer communications
- regulated HR, finance, legal, medical, identity, or customer-sensitive data

## Evidence That May Be Acceptable After Redaction

Acceptable proof evidence should use summaries, references, hashes, or inert examples instead of raw payloads.

Examples:

- redacted import transcript showing only allowed `lima.kernel` imports
- redacted package/version pin
- normalized metadata schema with fake or summarized values
- capability profile summary
- dry-run `ExecutionResult` summary
- non-execution invariant table
- simulated discovery evidence with synthetic-only surfaces
- forbidden surface attestation
- consumer-specific boundary attestation
- rollback or disable plan
- proof archive reference controlled by the consumer repo team

Evidence is not acceptable if the reviewer cannot tell whether it is synthetic, redacted, or inert.

Uncertain evidence must be classified as:

`needs_human_redaction_review`

## Sparkbot-Specific Redaction Checks

Sparkbot proof packets must not include:

- raw chat text
- raw user message bodies
- raw assistant outputs
- raw task descriptions
- raw tool arguments
- connector payloads
- provider payloads
- memory contents
- storage records
- scheduler payloads
- production route payloads
- public Sparkbot customer or user data

Acceptable Sparkbot evidence should be redacted to show:

- allowed import shape
- dry-run kernel call shape
- non-execution result shape
- absence of Sparkbot route wiring
- absence of Sparkbot task/message mutation
- absence of Sparkbot connector, tool, provider, memory, storage, and scheduler invocation

## Arc Bot-Specific Redaction Checks

Arc Bot / LIMA AI Office proof packets must not include:

- raw office-task text
- customer records
- customer communications
- customer files
- form contents
- project notes
- finance, HR, legal, medical, identity, or regulated business data
- connector payloads
- provider payloads
- tool arguments
- storage records
- scheduler payloads
- office-system adapter payloads
- production route payloads

Acceptable Arc evidence should be redacted to show:

- allowed import shape
- dry-run kernel call shape
- non-execution result shape
- absence of Arc route wiring
- absence of task, project, note, form, record, or customer file mutation
- absence of Arc connector, tool, provider, memory, storage, scheduler, and office-system adapter invocation

## Connection, Device, And Physical-World Redaction Checks

Proof packets must not include:

- raw WiFi SSIDs marked private or sensitive
- raw Bluetooth MAC addresses
- raw BLE identifiers
- raw IP addresses
- raw MAC addresses
- raw LAN scan results
- USB or serial device serial numbers
- MQTT, Matter, or mDNS raw discovery dumps
- pairing codes
- credentials or credential references that identify real secrets
- precise physical location
- robot command payloads
- drone command payloads
- device control payloads
- live scan dumps
- live connection evidence

Acceptable evidence may say only that:

- live discovery executed is False
- scan occurred is False
- connection attempted is False
- pairing attempted is False
- credentials used is False
- session opened is False
- device control executed is False
- physical-world behavior occurred is False
- simulated surfaces were synthetic and inert

## Decision Flow

1. Confirm the packet is a consumer-owned dry-run proof packet.
2. Confirm no reviewer action would touch consumer repos or run live behavior.
3. Check that redaction attestation exists.
4. Check for blocker categories.
5. Check Sparkbot-specific or Arc-specific sensitive evidence.
6. Check connection/device/physical-world sensitive evidence.
7. If blockers appear, stop and do not archive.
8. If evidence is uncertain, request human redaction review.
9. If evidence is redacted and safe, allow archive reference.
10. Only after redaction passes, continue to proof packet review and audit.

## Output Classification

Allowed outputs:

- `redacted_safe_for_archive`
- `redacted_safe_for_audit`
- `needs_redaction_before_review`
- `blocked_unredacted_sensitive_evidence`
- `needs_missing_redaction_attestation`
- `needs_human_redaction_review`

Forbidden outputs:

- `pass_for_production`
- `approved_for_live_integration`
- `approved_for_model_calls`
- `approved_for_tool_execution`
- `approved_for_connector_access`
- `approved_for_live_discovery`
- `approved_for_device_control`
- `approved_for_robo_os`
- `approved_for_physical_world`
- `compatibility_frozen`

## Reviewer Boundaries

Reviewers must not:

- modify consumer repos
- create or push consumer proof branches
- fetch, clone, scan, or inspect consumer repos without explicit approval
- automate proof intake
- run a redaction scanner
- archive unredacted evidence
- store raw evidence in this repo
- call models
- execute tools
- access connectors
- persist events
- run schedulers
- perform browser/file/process/network actions
- perform live discovery
- connect to devices
- pair devices
- use credentials
- invoke Robo-OS
- control devices, robots, drones, or physical-world systems

## Compatibility Freeze Boundary

Passing redaction does not mean:

- proof packet audit passed
- compatibility freeze is ready
- public Sparkbot integration is ready
- Arc Bot integration is ready
- production readiness exists
- live integration is approved

Compatibility freeze remains blocked until both Sparkbot and Arc packets pass redaction, both pass proof audit, and the compatibility freeze branch is separately designed and audited.

## Recommended Next Branch

If this checklist is accepted:

`audit-lima-consumer-proof-packet-redaction-checklist`

If proof packets are supplied first:

`audit-consumer-owned-proof-results`
