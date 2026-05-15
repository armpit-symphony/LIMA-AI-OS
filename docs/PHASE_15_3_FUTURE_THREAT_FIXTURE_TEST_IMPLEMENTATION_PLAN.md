# Phase 15.3 Future Threat Fixture Test Implementation Plan

Phase 15.3 proposes the future threat fixture acceptance-test implementation package without implementing it.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not implement actual future threat fixture tests, does not add the future threat fixtures, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Proposed Future Test File

Future test-only implementation may create:

- `tests/test_acceptance_threat_fixtures.py`

This file is proposed for a later explicitly approved phase only.

## Proposed Future Fixture Files

Future test-only implementation may create synthetic fixtures named:

- `tests/fixtures/runtime_extraction/acceptance_malformed_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_unknown_status_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_stale_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_replayed_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_approval_bypass_wording_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_shell_command_attempt_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_browser_network_attempt_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_file_mutation_attempt_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_robotics_physical_world_attempt_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_sparkbot_integration_attempt_candidate.json`
- `tests/fixtures/runtime_extraction/acceptance_humaninput_bridge_attempt_candidate.json`

These files are proposed for a later explicitly approved phase only.

## Proposed Future Threat Fixture Tests

- `test_malformed_candidate_fixture_remains_invalid_or_blocked`
- `test_unknown_status_fixture_remains_invalid_blocked_or_needs_review`
- `test_stale_candidate_fixture_remains_non_executable`
- `test_replayed_candidate_fixture_remains_non_executable`
- `test_approval_bypass_wording_fixture_does_not_authorize`
- `test_shell_command_attempt_fixture_remains_non_executing`
- `test_browser_network_attempt_fixture_remains_non_executing`
- `test_file_mutation_attempt_fixture_remains_non_mutating`
- `test_robotics_physical_world_attempt_fixture_remains_blocked`
- `test_sparkbot_integration_attempt_fixture_remains_unwired`
- `test_humaninput_bridge_attempt_fixture_remains_gated`

## Future Fixture Content Requirements

Future fixtures must remain synthetic, inert, non-runtime, and side-effect-free. They must not include credentials, private hostnames, deploy configs, live shell commands for execution, live network targets, real file mutation targets, robot/device actuation instructions, approval tokens, audit persistence records, or any claim that the fixture is authorization.

## Readiness Decision

The Phase 14.3 threat fixture designs are ready to be proposed for a later test-only implementation lane, but they are not implemented in Phase 15.3.
