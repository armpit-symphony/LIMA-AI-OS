# Phase 12.1 Next Direction Options: Runtime / Sparkbot / Robo-OS / Pause

Phase 12.1 compares the safe next lanes after the Phase 11 candidate status runtime slice.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Options Reviewed

### Option A: Pause And Preserve

Preserve the current Phase 11 runtime state and avoid new implementation until the product direction is clearer.

### Option B: Future Narrow Runtime Slice Design

Design a later non-executing kernel slice, but do not implement it in Phase 12.

### Option C: Sparkbot Integration Boundary Planning

Plan how Sparkbot could eventually consume LIMA Runtime contracts as a shell, without imports, wiring, or production integration.

### Option D: Robo-OS / Physical-World Boundary Planning

Plan the physical-world boundary as Guardian-gated driver integration, simulation-first and approval-blocked by default.

### Option E: Threat Model / Security Test Strengthening

Strengthen threat models and static/security test design before any more runtime work.

## Directional Finding

Phase 12 should continue with threat-model and safety-gap review before recommending a next lane. Sparkbot and Robo-OS planning are important, but they should not begin as integration work until their boundaries have been threat-modeled against the Phase 11 kernel slice.

## Next Step

Phase 12.2 should review threat-model and safety gaps across runtime, Sparkbot, Robo-OS, and pause options.
