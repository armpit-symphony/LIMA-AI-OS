# Phase 1.7 Spine/Audit Fake Recorder

## Purpose

Define a fake, in-memory Spine/Audit recorder for contract tests.

It records audit lineage contract objects without real persistence, storage, redaction implementation, enforcement, or execution.

## Non-Goals

- no real Spine storage
- no audit persistence
- no DB/storage
- no redaction runtime
- no Guardian enforcement
- no policy enforcement
- no approval enforcement
- no tool execution
- no model calls
- no driver calls
- no Sparkbot integration
- no Guardian Suite implementation copied

## Fake Recorder Rules

- in-memory only
- contract objects only
- no external services
- no env vars
- no DB/storage
- no file writes
- no raw secrets
- no raw prompts/transcripts/tool outputs/terminal output/sensor data
- no production use

## Lineage Safety

The fake recorder can store:

- lineage_id
- event_id
- decision_id
- approval_id
- policy_decision_id
- exposure_id
- execution_id
- redacted_summary
- content_refs
- evidence_refs
- privacy/redaction metadata

It must not store:

- raw secrets
- raw credentials
- raw vault values
- raw private prompts
- raw terminal output
- raw robot sensor data
- raw BCI/thought-adjacent data

## Scheduled / Autonomous Safety

The fake recorder may record scheduled/autonomous lineage metadata, but it does not execute scheduled work and does not renew decisions/approvals.

## Future Path

Future real Spine/audit persistence remains blocked until:

- storage design
- redaction implementation
- audit view filtering
- secret scanning
- retention enforcement
- Sparkbot adapter emission review
- Guardian/policy/approval enforcement review
