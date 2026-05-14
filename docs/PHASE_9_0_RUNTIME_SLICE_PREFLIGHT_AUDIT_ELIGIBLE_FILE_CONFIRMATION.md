# Phase 9.0 Runtime Slice Preflight Audit / Eligible File Confirmation

Phase 9.0 confirms the Phase 8.1 runtime file-touch map before any runtime implementation work begins. This phase is docs/tests/fixtures only and does not modify `lima/`.

This phase does not implement runtime behavior, does not modify `tests/support/`, does not change helper behavior, does not wire Sparkbot, does not add live adapters, does not implement HumanInput runtime bridge behavior, does not implement IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Preflight Finding

Phase 8.1 clearly lists the exact eligible runtime file surface for the narrow Phase 9 runtime slice.

## Eligible Existing Runtime Files

The following existing files are the only runtime files eligible for Phase 9.2 if the implementation needs them:

- `lima/contracts/boundary.py`
- `lima/contracts/intent.py`
- `lima/contracts/guardian.py`
- `lima/contracts/events.py`
- `lima/contracts/privacy.py`
- `lima/__init__.py`, only if a public export is required

## Eligible New Runtime Files

The following new files are eligible for the narrow Phase 9.2 coordinator implementation:

- `lima/kernel/__init__.py`
- `lima/kernel/intake_candidate.py`

## Phase 9.0 Decision

Phase 9.0 finds the file-touch map explicit enough to continue to Phase 9.1 acceptance test scaffolding.

Implementation remains blocked until the Phase 9.1 acceptance tests exist. Phase 9.2 must touch only the eligible runtime files and must stop if any forbidden surface is needed.

## Standing Forbidden Scope

- No `tests/support/` changes.
- No Sparkbot imports or wiring.
- No live adapter.
- No HumanInput runtime bridge.
- No IntentCompiler runtime behavior change unless explicitly justified within the eligible file map.
- No GuardianDecision runtime behavior change unless explicitly justified within the eligible file map.
- No approval enforcement.
- No execution.
- No audit persistence.
- No shell, browser, network, file mutation, robotics, or physical-world side effects.
- No external service calls.
- No background worker, daemon, queue, database write, or hidden side effect.

Contracts first.
Guardian always.
Sparkbot is the spec.
Extract, do not rewrite.
Robo-OS is a gated driver.
LIMA Runtime is the kernel.
