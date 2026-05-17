# Phase 41.0 Arc Bot Candidate Preview Hardening Charter

Phase 41.0 opens a docs/tests/fixtures-only hardening lane for the existing read-only `candidate_preview` helper using Arc Bot / LIMA Office-shaped task fixtures.

This phase does not modify `lima/`, `tests/support/`, Sparkbot, Arc Bot implementation, HumanInput bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, shell/browser/network/file mutation, robotics, physical-world behavior, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Scope

Phase 41 may add:

- Arc Bot-shaped synthetic fixtures under `tests/fixtures/runtime_extraction/phase_41_*.json`
- regression tests under `tests/test_phase_41_*.py`
- Phase 41 docs and state/roadmap documentation

Phase 41 must not add runtime implementation or modify `candidate_preview.py`.

## Hardening Targets

Phase 41 should prove that Arc Bot-shaped task requests remain non-authoritative, preview-only, read-only, non-executing, side-effect-free, and safe by default:

- draft-only email
- external email send
- calendar write
- file mutation
- low-confidence memory fact
- connector missing secret/setup
- agent identity with `kill_switch=true`
- scheduled task requiring approval
- admin action requiring block/PIN/breakglass
- robotics or physical-world request
- Sparkbot-only workstation behavior
- strict-security default posture
- explain-plan-only risky request

## Invariants

Every test must preserve:

- `execution_allowed=false`
- `side_effects_allowed=false`
- `approval_granted=false`
- `dispatch_allowed=false`
- `persistence_allowed=false`
- `humaninput_bridge_active=false`
- `sparkbot_wiring_active=false`
- `live_adapter_active=false`
- `external_calls_allowed=false`
- `robotics_allowed=false`
- `physical_world_allowed=false`
- `non_authoritative=true`
- `safe_by_default=true`

The fixture/test interpretation of preview-only is `preview_type="candidate_preview"`.
