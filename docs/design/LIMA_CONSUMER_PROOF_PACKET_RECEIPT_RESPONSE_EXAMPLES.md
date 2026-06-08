# LIMA Consumer Proof Packet Receipt Response Examples

## Example Status

This document provides synthetic, docs-only examples for future human-written LIMA-side receipt and response packets when Sparkbot or Arc Bot repo teams supply consumer-owned dry-run proof evidence.

It does not record real proof packets. It does not archive proof evidence. It does not update the receipt ledger. It does not audit proof results. It does not implement an intake service, parser, scanner, redaction engine, storage system, archive writer, webhook, bot, queue, scheduler, worker, notification sender, model call, connector, adapter, shell wiring, runtime behavior, live discovery, connection attempt, device behavior, Robo-OS behavior, robotics, drones, or physical-world behavior.

It does not inspect or modify Sparkbot repositories, Arc Bot repositories, public release repositories, `lima/`, `tests/support/`, `pyproject.toml`, package metadata, public exports, or consumer proof branches.

It does not approve production integration.

## Purpose

These examples show how LIMA reviewers should write consistent receipt and response records without implying that proof packets have already been received.

They exist to reduce ambiguity when future consumer teams provide:

- clean dry-run proof packets
- packets missing redaction evidence
- packets with missing non-execution evidence
- packets with forbidden runtime behavior
- packets with forbidden production or live-readiness claims
- question-only packets

## Source Artifacts

Use these examples with:

- `docs/templates/LIMA_CONSUMER_PROOF_INTAKE_RESPONSE_TEMPLATE.md`
- `docs/design/LIMA_CONSUMER_PROOF_RECEIPT_LEDGER.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REDACTION_CHECKLIST.md`
- `docs/design/LIMA_CONSUMER_PROOF_PACKET_REVIEW_CHECKLIST.md`
- `docs/templates/LIMA_CONSUMER_PROOF_RESULTS_AUDIT_TEMPLATE.md`

These examples must not override those artifacts.

## Global Rules

Every example response must preserve:

- `production_readiness: not_production_ready`
- no consumer repo modification
- no proof branch creation or push by LIMA
- no automated intake
- no repository fetch, clone, scan, or inspection without explicit approval
- no raw prompt, chat, office-task, customer, connector, provider, tool, credential, scan, device, location, robot, drone, or physical-world evidence
- no model calls
- no tool execution
- no connector access
- no storage or persistence implementation
- no scheduler or background work
- no browser/file/process/network actions
- no live discovery
- no connection attempts
- no pairing
- no credential use
- no Robo-OS invocation
- no device, robot, drone, or physical-world control

## Example 1: Sparkbot Clean Dry-Run Proof Receipt

Use only when a Sparkbot repo team supplies a redacted proof packet that appears archive-safe and dry-run-only.

```yaml
response_id: lima-consumer-proof-response-sparkbot-example-clean
consumer_repo: Sparkbot
consumer_branch: sparkbot-lima-dry-run-boundary-proof
lima_reviewer: lima-runtime-team
response_status: accepted_for_archive
summary: Sparkbot proof packet accepted as redacted dry-run evidence only; proof audit still required.
accepted_evidence_refs:
  - sparkbot-repo-team-redacted-proof-report-ref
missing_evidence: []
redaction_findings: []
boundary_findings: []
forbidden_claim_findings: []
recommended_next_branch: audit-consumer-owned-proof-results
production_readiness: not_production_ready
reviewer_notes:
  - This example does not represent an actual received packet.
  - Compatibility freeze remains blocked until both Sparkbot and Arc proof audits pass.
```

Ledger update example:

```yaml
receipt_id: sparkbot-proof-packet-received-example
received_date: example-date
received_by: lima-runtime-team
consumer_repo: Sparkbot
consumer_branch: sparkbot-lima-dry-run-boundary-proof
consumer_team_owner: sparkbot-repo-team
packet_location: sparkbot-repo-team-redacted-proof-report-ref
packet_kind: dry_run_dependency_proof
lima_commit_or_package_version: exact-lima-commit-or-version-from-packet
package_name: lima-ai-os
package_version: exact-package-version-from-packet
redaction_status: redacted
intake_status: accepted_for_archive
audit_status: ready_for_lima_side_audit
accepted_evidence_refs:
  - sparkbot-repo-team-redacted-proof-report-ref
missing_evidence: []
boundary_findings: []
forbidden_claim_findings: []
recommended_next_branch: audit-consumer-owned-proof-results
production_readiness: not_production_ready
reviewer_notes: Example only; not a real Sparkbot receipt.
```

## Example 2: Arc Bot Clean Dry-Run Proof Receipt

Use only when an Arc Bot / LIMA AI Office repo team supplies a redacted proof packet that appears archive-safe and dry-run-only.

```yaml
response_id: lima-consumer-proof-response-arc-example-clean
consumer_repo: Arc Bot / LIMA AI Office
consumer_branch: arc-lima-dry-run-boundary-proof
lima_reviewer: lima-runtime-team
response_status: accepted_for_archive
summary: Arc proof packet accepted as redacted dry-run evidence only; proof audit still required.
accepted_evidence_refs:
  - arc-repo-team-redacted-proof-report-ref
missing_evidence: []
redaction_findings: []
boundary_findings: []
forbidden_claim_findings: []
recommended_next_branch: audit-consumer-owned-proof-results
production_readiness: not_production_ready
reviewer_notes:
  - This example does not represent an actual received packet.
  - Compatibility freeze remains blocked until both Sparkbot and Arc proof audits pass.
```

Ledger update example:

```yaml
receipt_id: arc-proof-packet-received-example
received_date: example-date
received_by: lima-runtime-team
consumer_repo: Arc Bot / LIMA AI Office
consumer_branch: arc-lima-dry-run-boundary-proof
consumer_team_owner: arc-repo-team
packet_location: arc-repo-team-redacted-proof-report-ref
packet_kind: dry_run_dependency_proof
lima_commit_or_package_version: exact-lima-commit-or-version-from-packet
package_name: lima-ai-os
package_version: exact-package-version-from-packet
redaction_status: redacted
intake_status: accepted_for_archive
audit_status: ready_for_lima_side_audit
accepted_evidence_refs:
  - arc-repo-team-redacted-proof-report-ref
missing_evidence: []
boundary_findings: []
forbidden_claim_findings: []
recommended_next_branch: audit-consumer-owned-proof-results
production_readiness: not_production_ready
reviewer_notes: Example only; not a real Arc Bot receipt.
```

## Example 3: Redaction Missing

Use when a packet lacks redaction attestation or includes unclear evidence.

```yaml
response_id: lima-consumer-proof-response-example-redaction-missing
consumer_repo: Sparkbot or Arc Bot / LIMA AI Office
consumer_branch: expected-consumer-owned-proof-branch
lima_reviewer: lima-runtime-team
response_status: needs_redaction_before_review
summary: Proof packet cannot be archived or audited until redaction evidence is supplied.
accepted_evidence_refs: []
missing_evidence:
  - redaction_attestation
redaction_findings:
  - redaction status is missing or unclear
boundary_findings: []
forbidden_claim_findings: []
recommended_next_branch: revise-consumer-proof-evidence
production_readiness: not_production_ready
reviewer_notes:
  - Do not archive unredacted evidence.
  - Do not begin proof audit.
```

Ledger update example:

```yaml
redaction_status: needs_redaction_before_review
intake_status: needs_missing_evidence
audit_status: needs_redaction_before_review
accepted_evidence_refs: []
missing_evidence:
  - redaction attestation
recommended_next_branch: revise-consumer-proof-evidence
production_readiness: not_production_ready
```

## Example 4: Missing Non-Execution Evidence

Use when redaction appears acceptable but the packet does not prove dry-run/non-execution invariants.

```yaml
response_id: lima-consumer-proof-response-example-missing-non-execution
consumer_repo: Sparkbot or Arc Bot / LIMA AI Office
consumer_branch: expected-consumer-owned-proof-branch
lima_reviewer: lima-runtime-team
response_status: needs_missing_evidence
summary: Proof packet lacks required non-execution invariant evidence.
accepted_evidence_refs:
  - redacted-proof-report-ref
missing_evidence:
  - executable is False
  - execution_allowed is False
  - side_effects_allowed is False
  - dispatch_allowed is False
  - persistence_allowed is False
  - dry_run is True
  - model_calls_executed is False
  - live_discovery_executed is False
  - connection_attempted is False
  - device_control_executed is False
  - physical_world_executed is False
redaction_findings: []
boundary_findings:
  - missing_non_execution_invariants
forbidden_claim_findings: []
recommended_next_branch: revise-consumer-proof-evidence
production_readiness: not_production_ready
reviewer_notes:
  - Missing evidence is not a runtime approval.
  - Do not proceed to compatibility freeze.
```

## Example 5: Forbidden Runtime Boundary

Use when supplied evidence shows LIMA was used for live behavior, execution, hidden dispatch, model calls, connectors, storage, live discovery, device access, Robo-OS, or physical-world behavior.

```yaml
response_id: lima-consumer-proof-response-example-runtime-blocked
consumer_repo: Sparkbot or Arc Bot / LIMA AI Office
consumer_branch: expected-consumer-owned-proof-branch
lima_reviewer: lima-runtime-team
response_status: blocked_by_runtime_boundary
summary: Proof packet indicates behavior outside the dry-run LIMA boundary.
accepted_evidence_refs: []
missing_evidence: []
redaction_findings: []
boundary_findings:
  - forbidden_runtime_claim
  - execution_or_live_surface_evidence_present
forbidden_claim_findings: []
recommended_next_branch: design-lima-runtime-blocker-resolution
production_readiness: not_production_ready
reviewer_notes:
  - Do not archive as passing dry-run proof.
  - Do not continue compatibility freeze.
  - Do not implement workaround behavior in LIMA.
```

## Example 6: Forbidden Production Claim

Use when a packet claims production readiness, live integration readiness, model-call readiness, tool-execution readiness, connector readiness, live discovery readiness, device-control readiness, Robo-OS readiness, physical-world readiness, or compatibility freeze.

```yaml
response_id: lima-consumer-proof-response-example-claim-blocked
consumer_repo: Sparkbot or Arc Bot / LIMA AI Office
consumer_branch: expected-consumer-owned-proof-branch
lima_reviewer: lima-runtime-team
response_status: blocked_by_claim_boundary
summary: Proof packet uses forbidden production or live-readiness claims.
accepted_evidence_refs: []
missing_evidence: []
redaction_findings: []
boundary_findings: []
forbidden_claim_findings:
  - forbidden_production_or_live_claim
recommended_next_branch: audit-production-readiness-blockers
production_readiness: not_production_ready
reviewer_notes:
  - Request corrected dry-run-only proof packet language.
  - Passing dry-run dependency proof is not production readiness.
```

## Example 7: Question-Only Packet

Use when a consumer team asks a design/API question without submitting proof evidence.

```yaml
response_id: lima-consumer-proof-response-example-question-only
consumer_repo: Sparkbot or Arc Bot / LIMA AI Office
consumer_branch: expected-consumer-owned-proof-branch-or-not_applicable
lima_reviewer: lima-runtime-team
response_status: requires_followup_design
summary: Consumer team submitted a question, not a proof packet.
accepted_evidence_refs: []
missing_evidence:
  - consumer-owned proof packet
redaction_findings: []
boundary_findings:
  - requires_lima_design_followup
forbidden_claim_findings: []
recommended_next_branch: design-lima-consumer-proof-question-response
production_readiness: not_production_ready
reviewer_notes:
  - Do not update proof packet audit status as passed.
  - Do not start compatibility freeze.
```

## Example 8: Consumer Repo Boundary Blocked

Use when the request asks LIMA reviewers to modify, push, fetch, clone, scan, or inspect a consumer repo without explicit approval.

```yaml
response_id: lima-consumer-proof-response-example-consumer-boundary-blocked
consumer_repo: Sparkbot or Arc Bot / LIMA AI Office
consumer_branch: expected-consumer-owned-proof-branch
lima_reviewer: lima-runtime-team
response_status: blocked_by_consumer_repo_boundary
summary: Request crosses the consumer repo ownership boundary.
accepted_evidence_refs: []
missing_evidence: []
redaction_findings: []
boundary_findings:
  - consumer_repo_boundary_unclear
forbidden_claim_findings: []
recommended_next_branch: revise-consumer-proof-evidence
production_readiness: not_production_ready
reviewer_notes:
  - LIMA reviewers must not modify or push consumer proof branches.
  - Consumer repo teams own proof packets.
```

## Forbidden Example Interpretations

These examples must not be interpreted as:

- real packet receipts
- real proof audits
- proof archive records
- automated intake templates
- storage schema
- database schema
- event spine schema
- parser input
- redaction engine input
- model prompt input
- product readiness approval
- compatibility freeze approval
- authorization to touch Sparkbot or Arc repos
- authorization to run LIMA runtime behavior
- authorization to call models, tools, connectors, storage, schedulers, browser/file/process/network APIs, live discovery, Robo-OS, devices, robots, drones, or physical-world systems

## Recommended Next Branch

If this examples design is accepted:

`audit-lima-consumer-proof-packet-receipt-response-examples`

If proof packets are supplied first:

`audit-consumer-owned-proof-results`
