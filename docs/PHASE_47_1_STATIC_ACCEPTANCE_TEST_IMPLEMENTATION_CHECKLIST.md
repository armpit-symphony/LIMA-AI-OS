# Phase 47.1 Static Acceptance-Test Implementation Checklist

Phase 47.1 opens a docs/tests/fixtures-only static checklist lane for future typed bridge acceptance-test implementation planning.

This phase does not implement runtime bridge behavior. This phase does not create or activate a runtime test harness. This phase does not add actual or executable runtime bridge acceptance tests. This phase does not modify `lima/` or `tests/support/` behavior.

## Mission

Define the exact static checklist for a future separately approved acceptance-test implementation lane, while preserving fail-closed boundaries.

## Required Shared Sequence

Future acceptance-test fixtures and docs must use this order:

1. `ConsumerRequest`
2. `TypedIntentEnvelope` or `TaskIntent`
3. `CandidatePreview`
4. `RuntimeStateSnapshot`

## Required Contract Metadata In The Sequence

The sequence must carry these required refs/fields:

- `consumer_profile` (structured profile from request onward)
- `embodiment_profile` (required on every `CandidatePreview`, including `text_only`)
- `approval_posture` (descriptive only)
- `evidence_ref` (reference-only evidence pointer)

## Guardian Ownership Boundary

- LIMA describes approval posture only.
- Guardian or a future policy membrane owns real approval state.
- Sparkbot Shell and other consumers display posture; they do not grant authority.
- Adapter calls are future-gated and remain inactive in this lane.

## Static Implementation Checklist (Future Lane Definition Only)

- [ ] Preserve docs/tests/fixtures-only scope.
- [ ] Keep `preview_only=true`, `non_authoritative=true`, `safe_by_default=true`.
- [ ] Keep `execution_allowed=false`, `dispatch_allowed=false`, `persistence_allowed=false`.
- [ ] Keep `approval_granted=false`, `guardian_decision_created=false`.
- [ ] Keep `runtime_active=false`, `runtime_test_harness_active=false`.
- [ ] Keep `model_provider_calls_allowed=false`, `connector_calls_allowed=false`.
- [ ] Keep `adapter_calls_allowed=false`, `tool_calls_allowed=false`, `driver_calls_allowed=false`.
- [ ] Keep `side_effects_permitted=false`, `audit_storage_written=false`.
- [ ] Keep `human_input_bridge_active=false`, `live_adapter_active=false`.
- [ ] Keep `robotics_allowed=false`, `physical_world_allowed=false`.
- [ ] Ensure every future fixture includes structured `consumer_profile`.
- [ ] Ensure every future `CandidatePreview` includes `embodiment_profile`.
- [ ] Ensure typed bridge acceptance fixtures remain non-authoritative demo shapes.
- [ ] Ensure no `lima/` or `tests/support/` changes.
- [ ] Ensure no runtime bridge behavior, dispatch, execution, persistence, or side effects.

## Runtime Ladder Vocabulary

Allowed as vocabulary:

- `preview_only`
- `explain_plan`
- `approval_required`
- `approved_not_dispatched`
- `dispatch_ready`
- `executing`
- `completed`
- `audited`
- `blocked`
- `deferred`

Mock-safe active states in current lanes:

- `preview_only`
- `explain_plan`
- `blocked`
- `deferred`

## Forbidden In Phase 47 Lane

- runtime implementation
- runtime test harness creation or activation
- executable acceptance tests
- GuardianDecision creation
- approval enforcement
- execution/dispatch/persistence
- model/tool/driver/adapter calls
- Sparkbot/Arc live wiring
- robotics/IoT/drone/humanoid physical action
- shell/browser/network/file mutation
- external calls

## Recommended Next Lane

Phase 47.2 should remain docs/tests/fixtures-only and perform static checklist readiness review.
