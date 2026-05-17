# Phase 37.1 Candidate Preview Boundary Evidence Review

Phase 37.1 reviews evidence that the Phase 36 candidate preview helper stayed within its approved runtime boundary.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, `tests/support/`, or stale prior-phase tests.

## Evidence Reviewed

Phase 36 acceptance and regression tests prove:

- benign caller-provided input returns deterministic, inspectable, non-authoritative preview output
- missing input remains invalid and blocked
- malformed input remains invalid and blocked
- unknown values remain blocked and non-authoritative
- suspicious values remain blocked
- nested suspicious metadata remains blocked
- bypass wording does not grant authority
- explicit execution, approval, dispatch, and persistence flags are blocked
- the helper exports safely through `lima.kernel`
- forbidden imports and calls are absent

## Boundary Evidence

The candidate preview helper emits explicit inert flags:

- `non_authoritative = true`
- `read_only = true`
- `local_only = true`
- `deterministic = true`
- `safe_by_default = true`
- `execution_allowed = false`
- `side_effects_allowed = false`
- `approval_granted = false`
- `dispatch_allowed = false`
- `persistence_allowed = false`
- `phase_5_humaninput_runtime_bridge_gated = true`
- `humaninput_bridge_active = false`
- `sparkbot_wiring_active = false`
- `live_adapter_active = false`
- `external_calls_allowed = false`
- `robotics_allowed = false`
- `physical_world_allowed = false`

## Static Scan Evidence

The Phase 36 scan found no forbidden imports or calls for subprocesses, threads, queues, sockets, HTTP libraries, SQLite/database access, browsers, file opening, dynamic execution, Sparkbot imports, IntentCompiler calls, or GuardianDecision calls.

## Continue

Continue only to Phase 37.2 candidate preview regression and gap review.
