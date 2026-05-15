# Phase 18.2 Acceptance Boundary Regression Fixtures

Phase 18.2 adds synthetic acceptance-boundary regression fixtures and fixture tests.

This phase is tests/docs/fixtures only. It does not modify `lima/`, does not modify `tests/support/`, does not change runtime behavior, does not add helper behavior, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not enforce approval, does not execute, does not dispatch, does not persist audit, and does not perform shell, browser, network, file mutation, robotics, or physical-world action.

## Fixture Purpose

The fixtures preserve synthetic examples for acceptance boundaries that must remain non-executing:

- approval-bypass wording
- shell attempt
- browser/network attempt
- file mutation attempt
- robotics/physical-world attempt
- Sparkbot integration attempt
- HumanInput runtime bridge attempt
- stale and replayed candidate signals
- malformed and unknown-status candidate signals

## Fixture Rules

The fixtures are synthetic, inert, non-runtime, side-effect-free, and not authorization. They must not contain credentials, private hostnames, deploy configs, live shell commands, live network targets, real file paths, robot/device actuation instructions, approval tokens, audit records, or external service targets.

## Boundary

Phase 18.2 fixture tests may exercise existing non-executing candidate APIs but must not modify runtime files.
