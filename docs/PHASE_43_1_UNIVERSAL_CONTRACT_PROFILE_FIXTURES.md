# Phase 43.1 Universal Contract Profile Fixtures

Phase 43.1 adds inert universal contract profile fixture data for the Phase 43 Universal Contract Fixture Hardening lane.

The fixtures are caller-provided metadata only. They do not implement profile handling, modify `lima/`, modify `tests/support/`, wire Sparkbot, implement Arc Bot, create HumanInput bridge behavior, create live adapters, enforce approvals, execute, dispatch, persist, mutate files, call external systems, create background work, or touch robotics, hardware, or physical-world behavior.

## Fixture Set

The fixture corpus includes:

- `arc_bot_office_task_profile`
- `sparkbot_reference_profile`
- `generic_automation_agent_profile`
- `coding_agent_profile`
- `research_agent_profile`
- `browser_action_profile`
- `shell_action_profile`
- `file_mutation_profile`
- `network_api_action_profile`
- `scheduled_background_work_profile`
- `iot_device_action_profile`
- `drone_action_profile`
- `humanoid_action_profile`
- `robot_motion_profile`
- `emergency_stop_profile`
- `malicious_consumer_profile_trying_to_grant_approval`
- `malicious_embodiment_profile_trying_to_allow_execution`
- `malformed_profile_data`
- `unknown_model_provider_data`
- `nested_bypass_wording`

## Expected Posture

Safe read-only planning profiles may remain `proposed` or `needs_review`. Browser, shell, file, network/API, scheduled/background, IoT, drone, humanoid, robot motion, emergency stop, malformed, unknown-provider, and adversarial bypass cases must remain blocked or review-only and must never grant approval, execution, dispatch, persistence, adapter activity, external calls, robotics, or physical-world behavior.

## Boundary

These fixtures make no runtime claim. They exist so later tests can prove universal profile metadata remains preview-only, non-authoritative, deterministic, local-only, approval-free, non-executing, side-effect free, adapter-inactive, robotics-inactive, and physical-world inactive.

## Continue

Continue only to Phase 43.2 docs/tests/fixtures-only universal contract profile regression tests over this fixture corpus. No runtime implementation is approved.
