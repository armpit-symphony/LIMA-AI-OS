# Phase 42.0 LIMA Universal Runtime Contract Reframing Audit

Phase 42.0 reframes Phase 42 around LIMA AI OS as the universal runtime contract target.

This lane corrects the Phase 40/41 consumer emphasis without rewriting or discarding that work. Arc Bot / LIMA Office remains valid as an early guarded office-agent consumer profile, but it is not the center of LIMA AI OS. Sparkbot remains reference evidence and a public showcase shell, not the default runtime posture.

This phase is docs/tests/fixtures-only. It does not modify `lima/`, `tests/support/`, Sparkbot, runtime behavior, helper behavior, Sparkbot wiring, Arc Bot implementation, HumanInput bridge behavior, live adapters, approval enforcement, execution, dispatch, persistence, shell/browser/network/file mutation, robotics, physical-world action, external calls, background work, subprocesses, threads, queues, daemons, database writes, or hidden side effects.

## Universal Runtime Target

LIMA AI OS is the model-agnostic, consumer-agnostic, embodiment-agnostic reasoning operating system/runtime for:

- bots
- automation
- agents
- office workers
- coding agents
- research agents
- physical robots
- humanoids
- drones
- IoT devices
- future embodiments

LIMA AI OS should support future consumers through explicit profiles, contracts, and adapters. Profiles and contracts may describe posture, but they cannot grant runtime authority.

## Product Split

Phase 42 records the following product split:

- `lima_ai_os_runtime`: universal public runtime contract and safety substrate.
- `sparkbot_public`: open-source showcase shell and reference evidence for product/control vocabulary.
- `arc_bot_lima_office`: proprietary guarded worker-bot shell and office-agent consumer profile.
- `paid_lima_robotics_iot_unlock`: proprietary/paid path for robotics, IoT, embodied adapters, deployment-specific policy, and hardware unlocks.

## Public Versus Private Boundary

Public LIMA AI OS should include:

- model-agnostic contracts
- consumer/profile vocabulary
- safety invariants
- Guardian boundary descriptions
- preview-only fixtures and tests
- public showcase-compatible contract examples

Private/proprietary layers should include:

- Arc Bot product shell and business workflows
- paid robotics/IoT unlocks
- deployment-specific adapters
- hardware manifests and guarded drivers
- secrets, operator policies, customer connectors, and private integrations

## Sanitization Checklist

Before any repo split or public release, verify:

- no secrets, tokens, keys, customer data, private policies, hardware credentials, or deployment manifests
- no proprietary Arc Bot implementation
- no paid robotics/IoT unlock code
- no Sparkbot private workstation-specific code copied into LIMA
- no runtime behavior that executes, dispatches, persists, mutates, calls external systems, or touches hardware
- no Guardian bypass, approval grant, live adapter, HumanInput bridge behavior, or hidden side effect

## Hard Reframe

Arc Bot is one consumer profile. Sparkbot is reference evidence and an open-source showcase shell. LIMA AI OS is the universal runtime contract target.
