# LIMA Consumer Proof Receipt Ledger

## Ledger Status

This document defines a future human-maintained, LIMA-local receipt ledger shape for Sparkbot and Arc Bot consumer-owned dry-run proof packets.

It is docs-only. It does not implement storage, persistence, an intake service, a database, a queue, a scheduler, a worker, a webhook, a parser, a bot, a notification sender, a model call, a connector, an adapter, shell wiring, runtime behavior, live discovery, connection attempts, device behavior, Robo-OS behavior, robotics, drones, or physical-world behavior.

It does not audit real consumer proof packets.

It does not modify Sparkbot repositories, Arc Bot repositories, public release repositories, `lima/`, `tests/support/`, `pyproject.toml`, package metadata, or public exports.

It does not approve production integration.

## Purpose

The receipt ledger gives LIMA reviewers a consistent manual record for whether consumer proof packets have been received, redaction-checked, accepted for audit, blocked, or still missing.

It exists to prevent:

- losing track of whether a Sparkbot or Arc packet was supplied
- mistaking a handoff package for a returned proof packet
- auditing missing proof packets
- starting a compatibility freeze before both packets pass
- using automated intake, storage, repository scanning, or live connectors

## Current Ledger Verdict

`no_consumer_packets_received`

Current packet states:

- Sparkbot packet: `not_received`
- Arc Bot packet: `not_received`
- Sparkbot audit: `not_started`
- Arc Bot audit: `not_started`
- Compatibility freeze: `blocked`

## Ledger Entry Shape

Each future receipt entry should be human-written and include:

- `receipt_id`
- `received_date`
- `received_by`
- `consumer_repo`
- `consumer_branch`
- `consumer_team_owner`
- `packet_location`
- `packet_kind`
- `lima_commit_or_package_version`
- `package_name`
- `package_version`
- `redaction_status`
- `intake_status`
- `audit_status`
- `accepted_evidence_refs`
- `missing_evidence`
- `boundary_findings`
- `forbidden_claim_findings`
- `recommended_next_branch`
- `production_readiness`
- `reviewer_notes`

This ledger shape must remain a document-only record until a separate storage design, threat model, and implementation approval exist.

## Allowed Receipt Status Values

Allowed `redaction_status` values:

- `not_checked`
- `redacted`
- `needs_redaction_before_review`
- `blocked_unredacted_sensitive_evidence`

Allowed `intake_status` values:

- `not_received`
- `received_for_redaction_check`
- `accepted_for_archive`
- `needs_missing_evidence`
- `blocked_by_claim_boundary`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`

Allowed `audit_status` values:

- `not_started`
- `ready_for_lima_side_audit`
- `pass_for_dry_run_dependency_proof`
- `needs_redaction_before_review`
- `needs_missing_evidence`
- `blocked_by_runtime_boundary`
- `blocked_by_consumer_repo_boundary`
- `blocked_by_claim_boundary`
- `requires_lima_design_followup`
- `requires_lima_audit_followup`
- `not_ready_for_implementation`

Required `production_readiness` value:

- `not_production_ready`

## Forbidden Receipt Status Values

Forbidden receipt, intake, or audit statuses:

- `production_ready`
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

## Initial Ledger Entries

### Sparkbot

```yaml
receipt_id: sparkbot-proof-packet-pending
received_date: not_received
received_by: not_assigned
consumer_repo: Sparkbot
consumer_branch: sparkbot-lima-dry-run-boundary-proof
consumer_team_owner: sparkbot-repo-team
packet_location: not_received
packet_kind: dry_run_dependency_proof
lima_commit_or_package_version: not_received
package_name: not_received
package_version: not_received
redaction_status: not_checked
intake_status: not_received
audit_status: not_started
accepted_evidence_refs: []
missing_evidence:
  - consumer-owned proof packet
  - redaction attestation
  - non-execution invariant evidence
  - Sparkbot-specific forbidden surface evidence
boundary_findings: []
forbidden_claim_findings: []
recommended_next_branch: audit-consumer-owned-proof-results after packet receipt
production_readiness: not_production_ready
reviewer_notes: LIMA has not received the Sparkbot proof packet.
```

### Arc Bot

```yaml
receipt_id: arc-proof-packet-pending
received_date: not_received
received_by: not_assigned
consumer_repo: Arc Bot / LIMA AI Office
consumer_branch: arc-lima-dry-run-boundary-proof
consumer_team_owner: arc-repo-team
packet_location: not_received
packet_kind: dry_run_dependency_proof
lima_commit_or_package_version: not_received
package_name: not_received
package_version: not_received
redaction_status: not_checked
intake_status: not_received
audit_status: not_started
accepted_evidence_refs: []
missing_evidence:
  - consumer-owned proof packet
  - redaction attestation
  - non-execution invariant evidence
  - Arc-specific forbidden surface evidence
boundary_findings: []
forbidden_claim_findings: []
recommended_next_branch: audit-consumer-owned-proof-results after packet receipt
production_readiness: not_production_ready
reviewer_notes: LIMA has not received the Arc Bot proof packet.
```

## Receipt Workflow

When the user supplies a consumer proof packet or packet location:

1. Confirm the consumer branch is expected.
2. Create or update a human-written ledger entry.
3. Check redaction before archiving.
4. If redaction fails, set `redaction_status: needs_redaction_before_review`.
5. If required fields are missing, set `intake_status: needs_missing_evidence`.
6. If forbidden claims appear, set `intake_status: blocked_by_claim_boundary`.
7. If intake is clean, set `intake_status: accepted_for_archive`.
8. Audit the packet using `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`.
9. Record audit status in the ledger entry.
10. Do not start compatibility freeze until both Sparkbot and Arc audit statuses are `pass_for_dry_run_dependency_proof`.

## Redaction Blockers

Do not archive or audit packet contents that include:

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

## Compatibility Freeze Rule

Compatibility freeze remains blocked unless:

- Sparkbot packet is received
- Arc Bot packet is received
- Sparkbot packet passes LIMA-side audit as `pass_for_dry_run_dependency_proof`
- Arc Bot packet passes LIMA-side audit as `pass_for_dry_run_dependency_proof`
- no redaction blockers remain
- no missing evidence blockers remain
- no forbidden import blockers remain
- no runtime boundary blockers remain
- no production/live-claim blockers remain

Current freeze status:

`blocked`

## Forbidden Ledger Behavior

This ledger must not become:

- automated intake
- durable storage implementation
- database table
- event spine
- queue
- scheduler
- background worker
- webhook receiver
- notification sender
- repo scanner
- proof archive crawler
- raw evidence archive
- model/tool/connector runner
- live discovery surface
- Robo-OS integration
- device/robot/drone control surface

## Forbidden Reviewer Actions

Reviewers must not:

- modify consumer repos
- create or push consumer proof branches
- fetch, clone, scan, or inspect consumer repos without explicit approval
- automate proof intake
- archive unredacted evidence
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

## Recommended Next Branch

If this ledger design is accepted:

`audit-lima-consumer-proof-receipt-ledger`

If proof packets are supplied first:

`audit-consumer-owned-proof-results`
