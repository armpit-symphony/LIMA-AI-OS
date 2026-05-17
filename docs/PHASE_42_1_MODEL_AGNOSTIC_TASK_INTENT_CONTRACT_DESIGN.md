# Phase 42.1 Model-Agnostic Task Intent Contract Design

Phase 42.1 defines universal LIMA AI OS planning contracts for model-agnostic input, task/intent description, candidate action preview, approval posture, embodiment/profile metadata, and telemetry/evidence vocabulary.

This phase is docs/tests/fixtures-only. It does not create runtime schemas, runtime modules, adapters, approval enforcement, execution, dispatch, persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Universal Input Contract

The universal input contract describes caller-provided request metadata:

- `input_id`
- `source_profile`
- `model_provider_hint`
- `model_identity_hint`
- `input_modality`
- `operator_context`
- `raw_request_summary`
- `attachments_descriptor`
- `trust_context`
- `redaction_posture`

Model/provider hints are descriptive only. Unknown models and providers must remain safe.

## Universal Task / Intent Contract

The universal task/intent contract describes what the caller appears to ask for:

- `task_id`
- `intent_summary`
- `consumer_profile`
- `embodiment_profile`
- `action_class`
- `risk_tier`
- `run_state`
- `requested_outcome`
- `constraints`
- `non_goals`

Intent classification cannot grant authority.

## Universal Candidate Action Preview Contract

The candidate action preview contract describes possible action-shaped output without action:

- `candidate_id`
- `preview_type`
- `preview_state`
- `action_class`
- `approval_posture`
- `dry_run_posture`
- `blocked_reasons`
- `warnings`
- `evidence_refs`
- `rollback_notes`

Preview output must remain `preview_only=true`, `non_authoritative=true`, and `safe_by_default=true`.

## Universal Approval-Posture Description Contract

LIMA may describe approval posture, but Guardian or a future policy membrane owns real approval state.

Allowed approval posture vocabulary:

- `not_required`
- `confirmation_required`
- `pin_required`
- `breakglass_required`
- `blocked`
- `policy_membrane_required`

LIMA cannot grant approval in this phase.

## Universal Telemetry / Evidence Vocabulary

Telemetry and evidence are descriptive references only:

- `policy_decision_ref`
- `run_timeline_ref`
- `audit_hash_ref`
- `redacted_args_ref`
- `evidence_ref`
- `simulation_ref`
- `connector_health_ref`

No audit persistence is implemented.

## Universal Embodiment / Profile Contract

Profiles describe consumer or embodiment posture:

- `profile_id`
- `profile_kind`
- `allowed_action_classes`
- `forbidden_action_classes`
- `adapter_boundary`
- `guardian_boundary`
- `approval_posture_defaults`
- `emergency_stop_posture`

Profile vocabulary cannot grant runtime authority.
