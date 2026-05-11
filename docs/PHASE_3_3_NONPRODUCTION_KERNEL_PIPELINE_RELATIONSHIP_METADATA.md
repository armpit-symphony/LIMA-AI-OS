# Phase 3.3 Non-production Kernel Pipeline Relationship Metadata

## Purpose

Add explicit relationship metadata across fixture families for the proposed non-production kernel pipeline.

This phase does not implement a runtime pipeline.
This phase does not transform data.
This phase does not create executable behavior.
This phase does not authorize production integration.

## Relationship Metadata Rule

Relationship metadata is not runtime wiring.

It does not:

- execute stages
- transform fixture data
- validate runtime compatibility
- authorize actions
- persist audit data
- imply production integration

The metadata exists for review and fixture-family mapping only. `scenario_id` groups related fixture shapes; it does not imply execution order. Stage references point to fixture metadata relationships only; they do not imply a live pipeline. `compatible_with` is a fixture-map statement only and does not prove runtime compatibility.

## Metadata Fields

- `relationship_id`: stable identifier for this metadata row
- `scenario_id`: scenario grouping label, not sequence control
- `scenario_name`: human-readable scenario label
- `pipeline_stage`: fixture stage represented by this row
- `current_fixture_ref`: fixture file and fixture id reference, or `null` when no current fixture exists
- `previous_stage_ref`: previous relationship reference, or `null`; reference only
- `next_stage_ref`: next relationship reference, or `null`; reference only
- `compatible_with`: related fixture or relationship references; fixture-map statement only
- `expected_posture`: review/status hint only
- `safety_gate_refs`: standing safety gate docs relevant to the row
- `non_runtime`: must be `true`
- `notes`: review notes and gap explanations

## Scenario Groups

- `low_risk_informational`
- `calendar_scheduling`
- `draft_only_communication`
- `email_send_requires_approval`
- `terminal_critical`
- `robot_safety_critical`
- `secret_access`
- `payment_deploy_admin_destructive`
- `invalid_missing_metadata`
- `clarification_needed`
- `blocked_unsafe_request`
- `expired_revoked_superseded_fake_decision`

## Safety Gate References

- `docs/ADAPTER_SAFETY_GATE.md`
- `docs/INTENTENVELOPE_SAFETY_GATE.md`
- `docs/GUARDIAN_REQUEST_SAFETY_GATE.md`
- `docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md`

## Known Gaps

- fake approval metadata fixtures are placeholders only if not present
- fake spine/audit lineage fixtures are placeholders only if not present
- report artifact placeholder is not runtime output
- stage compatibility is not code-verified
- fixture IDs may need future standardization

## Acceptance Criteria

- relationship metadata file exists
- relationship metadata is valid JSON
- every relationship has `non_runtime` true
- safety gate refs are present
- no runtime behavior added
- tests validate metadata shape
- tests pass
