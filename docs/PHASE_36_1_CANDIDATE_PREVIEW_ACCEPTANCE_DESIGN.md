# Phase 36.1 Candidate Preview Acceptance Design

Phase 36.1 defines the acceptance design for the approved candidate preview helper before implementation.

This phase adds no runtime code. It does not modify `lima/`, does not modify `tests/support/`, and does not change runtime behavior.

## Required Preview Shape

The future preview output must be inspectable plain metadata with explicit safe flags:

- `preview_type`
- `preview_state`
- `status_reason`
- `input_present`
- `normalized_status`
- `non_authoritative`
- `read_only`
- `local_only`
- `deterministic`
- `safe_by_default`
- `execution_allowed`
- `side_effects_allowed`
- `approval_granted`
- `dispatch_allowed`
- `persistence_allowed`
- `phase_5_humaninput_runtime_bridge_gated`
- `humaninput_bridge_active`
- `sparkbot_wiring_active`
- `live_adapter_active`
- `external_calls_allowed`
- `robotics_allowed`
- `physical_world_allowed`
- `blocked_claims`
- `warnings`

## Required Input Coverage

Acceptance tests must cover:

- benign caller-provided input
- missing input
- malformed input
- unknown status values
- suspicious values
- nested suspicious metadata
- bypass wording such as Phil, operator, admin, trusted, urgent, override, approve, approved, and emergency
- shell/browser/network/file mutation claims
- robotics and physical-world claims
- external service and background-work claims

## Required Safety Outcomes

Every preview must remain non-authoritative, read-only, local-only, deterministic, non-executing, side-effect free, approval-free, dispatch-free, persistence-free, bridge-inactive, adapter-inactive, Sparkbot-inactive, external-call-free, robotics-free, and physical-world-free.

Unknown, malformed, suspicious, nested, or bypass-worded input must produce a blocked, invalid, or needs-review preview. Benign input may produce a proposed preview, but it must still remain non-authoritative and non-executing.

## Static Boundary Checks

Phase 36.2 tests must scan the new module for forbidden imports and behavior. The module must not import or reference shell, browser, network, database, filesystem mutation, subprocess, threading, queue, daemon, Sparkbot, HumanInput bridge, live adapter, IntentCompiler, GuardianDecision, robotics, or physical-world integration surfaces.

## Continue

Continue only to Phase 36.2 candidate preview runtime implementation.
