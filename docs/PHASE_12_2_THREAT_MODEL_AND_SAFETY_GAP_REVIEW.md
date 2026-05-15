# Phase 12.2 Threat Model and Safety Gap Review

Phase 12.2 reviews safety gaps before the project selects a next lane after Phase 11.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Threats Reviewed

- candidate status normalization mistaken for approval
- candidate validation mistaken for GuardianDecision behavior
- HumanInput runtime bridge pressure before the Phase 5 gate is reopened
- Sparkbot integration being treated as imports or wiring instead of boundary planning
- Robo-OS planning drifting into driver behavior or physical-world action
- operator, admin, Phil, or trusted wording being treated as permission
- shell, browser, network, file mutation, robotics, or external-service escalation
- audit persistence being implied before an approved persistence lane
- static tests being mistaken for complete runtime security proof

## Safety Gaps

- no runtime threat-model test plan exists for future Phase 13+ work
- no Sparkbot shell-boundary plan has been threat-modeled yet
- no Robo-OS / physical-world simulation boundary has been threat-modeled yet
- no approved runtime expansion exists beyond candidate status normalization and validation
- Phase 5 HumanInput runtime bridge remains gated

## Finding

The safest immediate next phase is a recommendation matrix that compares pause, threat-model-derived test planning, Sparkbot boundary planning, Robo-OS boundary planning, and future runtime design as separate lanes.

## Next Step

Phase 12.3 should produce a machine-checkable next-lane recommendation matrix.
