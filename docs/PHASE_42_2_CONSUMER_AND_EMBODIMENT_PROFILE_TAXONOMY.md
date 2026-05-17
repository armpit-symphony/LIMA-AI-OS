# Phase 42.2 Consumer And Embodiment Profile Taxonomy

Phase 42.2 defines consumer, embodiment, action, and adapter-boundary planning taxonomy for LIMA AI OS.

This taxonomy is universal OS vocabulary. It does not make Arc Bot the center, wire Sparkbot, implement Arc Bot, create adapters, call hardware, mutate files, call networks, execute commands, enforce approvals, dispatch, persist, or change runtime behavior.

## Consumer Profiles

Consumer profiles describe the type of shell, bot, agent, controller, or future embodiment consuming LIMA AI OS contracts:

- `arc_bot_lima_office`
- `sparkbot_public`
- `generic_chatbot`
- `automation_agent`
- `office_agent`
- `coding_agent`
- `research_agent`
- `robot_controller`
- `drone_controller`
- `humanoid_controller`
- `iot_controller`

Arc Bot / LIMA Office is one guarded office-agent profile. Sparkbot Public is an open-source showcase shell and reference profile. Neither grants default runtime authority.

## Embodiment / Action Profiles

Embodiment profiles describe the action surface a consumer may request:

- `text_only`
- `office_workflow`
- `browser`
- `shell`
- `file_system`
- `network_api`
- `database`
- `scheduled_background_work`
- `iot_device`
- `mobile_robot`
- `drone`
- `humanoid`
- `physical_world_actuator`
- `emergency_stop`

Robotics, drones, humanoids, IoT, and physical-world actuators are core long-term LIMA AI OS vision surfaces, but in this lane they remain planning vocabulary with blocked or deferred posture.

## Universal Action Classes

LIMA AI OS planning vocabulary includes:

- `read`
- `internal_write`
- `external_write`
- `execute`
- `admin`
- `secret_use`
- `scheduled_work`
- `robot_motion`
- `physical_world_action`
- `iot_device_action`
- `human_proximity_action`
- `emergency_stop`

## Adapter Boundary Taxonomy

Adapter boundaries describe where future integrations would sit, not what exists now:

- `no_adapter`
- `planning_only`
- `mock_fixture`
- `contract_preview`
- `guardian_gated_adapter_required`
- `private_product_adapter`
- `paid_embodiment_unlock_required`
- `blocked_without_explicit_approval`

Profile vocabulary cannot grant runtime authority. Guardian or a future policy membrane must own real approval state.
