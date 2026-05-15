# Phase 16.3 Threat Fixture Acceptance Tests

Phase 16.3 implements synthetic threat fixture acceptance tests.

This phase is tests/docs/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Fixture Scope

Phase 16.3 adds one synthetic fixture matrix:

- `tests/fixtures/runtime_extraction/phase_16_3_threat_fixture_acceptance_cases.json`

The fixture cases are synthetic labels only. They do not contain credentials, private hostnames, deploy configs, live shell commands, live network targets, real file paths, robot/device actuation instructions, approval tokens, or audit persistence records.

## Implemented Acceptance Checks

- malformed candidate metadata remains invalid or blocked
- unknown status remains invalid, blocked, or needs-review
- stale candidate remains non-executable
- replayed candidate remains non-executable
- approval-bypass wording does not authorize
- shell attempts remain non-executing
- browser/network attempts remain non-executing
- file mutation attempts remain non-mutating
- robotics/physical-world attempts remain blocked or review-required
- Sparkbot integration attempts remain unwired
- HumanInput bridge attempts remain gated or rejected
