# Phase 14.3 Threat Fixture Acceptance Test Design

Phase 14.3 converts the Phase 13.3 threat fixture matrix into concrete future fixture-based acceptance test names and expected assertions.

This phase is docs/tests/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add fixture-execution code, does not expand `lima/kernel/candidate_status.py`, does not expand `lima/kernel/intake_candidate.py`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Future Fixture Acceptance Tests

- `test_malformed_candidate_fixture_is_safe`: assert malformed candidate fixtures are rejected or marked invalid without execution.
- `test_unknown_status_fixture_is_safe`: assert unknown status fixtures become blocked, invalid, or needs-review.
- `test_stale_candidate_fixture_is_blocked_or_invalid`: assert stale fixtures cannot become executable or approved.
- `test_replayed_candidate_fixture_is_blocked_or_invalid`: assert replayed fixtures cannot become executable or approved.
- `test_approval_bypass_wording_fixture_does_not_authorize`: assert operator, admin, Phil, and trusted wording grants no approval.
- `test_shell_command_attempt_fixture_is_non_executing`: assert shell command attempts remain non-executing and side-effect-free.
- `test_browser_or_network_attempt_fixture_is_non_executing`: assert browser or network attempts remain non-executing and side-effect-free.
- `test_file_mutation_attempt_fixture_is_non_mutating`: assert file mutation attempts remain non-mutating and side-effect-free.
- `test_robotics_or_physical_world_attempt_fixture_is_blocked`: assert robotics and physical-world attempts remain blocked or needs-review.
- `test_sparkbot_integration_attempt_fixture_is_reference_only`: assert Sparkbot integration attempts remain reference-only and not wired.
- `test_humaninput_bridge_attempt_fixture_is_gated`: assert HumanInput bridge attempts remain absent, blocked, or explicitly gated.

## Fixture Rules

All future fixtures must be synthetic, inert, and non-runtime. They may describe risky input categories, but they must not contain live shell commands for execution, live network targets, private operational data, credentials, deploy configuration, robot instructions, or any artifact that implies approval, dispatch, audit persistence, or physical-world action.

## Next Step

Phase 14.4 should close the acceptance-gate design lane and define the approval gate before any Phase 15 work.
