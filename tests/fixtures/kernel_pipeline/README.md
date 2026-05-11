# Kernel Pipeline Fixture Relationship Metadata

This directory contains Phase 3.3 non-runtime relationship metadata for proposed kernel pipeline fixture families.

The metadata is review material only. It is not runtime wiring, does not transform fixture data, does not authorize actions, and does not persist audit data.

Current files:

- `pipeline_relationships.json`: reference-only relationships across existing Sparkbot-shaped payload, IntentEnvelope, Guardian request, fake GuardianDecision, and report placeholder stages.

Rules:

- every relationship must set `non_runtime` to `true`
- `scenario_id` is a grouping label, not sequence control
- `previous_stage_ref` and `next_stage_ref` are references only
- `compatible_with` is a fixture-map statement only
- `expected_posture` is a review/status hint only
- no runtime code may consume this metadata in Phase 3.3
