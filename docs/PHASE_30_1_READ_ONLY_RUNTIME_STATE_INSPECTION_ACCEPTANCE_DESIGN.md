# Phase 30.1 Read-Only Runtime State Inspection Acceptance Design

Phase 30.1 defines acceptance and regression coverage for the approved Phase 30 read-only runtime state inspection slice before implementation.

This phase is acceptance design only. It does not implement runtime behavior, does not modify `lima/`, does not modify `tests/support/`, does not wire Sparkbot, does not add a HumanInput runtime bridge, does not add live adapters, does not change IntentCompiler or GuardianDecision runtime behavior, does not approve, execute, dispatch, persist audit, enforce approval, or add shell, browser, network, file mutation, robotics, external-service, background-worker, or physical-world behavior.

## Required Runtime Contract

The Phase 30.2 implementation must expose a pure read-only inspection API for caller-provided candidate-like state.

The API must:

- return deterministic output for identical input,
- return safe default output for missing input,
- return safe output for malformed input,
- return safe output for unknown status values,
- keep bypass wording from changing the safety outcome,
- mark output as non-authoritative,
- preserve `execution_allowed` as false,
- preserve `side_effects_allowed` as false,
- keep approval not approved,
- keep dispatch disallowed,
- keep persistence disallowed,
- keep Phase 5 HumanInput runtime bridge gated,
- expose no Sparkbot wiring/imports,
- expose no live adapter behavior,
- expose no shell/browser/network/file mutation behavior,
- expose no robotics or physical-world behavior,
- expose no background worker/thread/subprocess/queue/daemon behavior.

## Required Test Families

Phase 30.2 must include tests for:

- deterministic snapshots,
- missing input safe defaults,
- malformed input safe defaults,
- unknown status safe defaults,
- bypass wording resistance,
- non-execution invariants,
- non-authoritative advisory output,
- no mutation of caller-provided input,
- forbidden import and forbidden behavior absence,
- Phase 5 HumanInput runtime bridge remains gated.

## Required Synthetic Fixtures

Phase 30.2 fixtures should cover:

- valid non-executing candidate state,
- missing candidate state,
- malformed candidate state,
- unknown candidate status,
- bypass wording in candidate-like text,
- shell/browser/network/file/robotics/physical-world attempt metadata,
- Sparkbot integration attempt metadata,
- HumanInput bridge attempt metadata.

## Continue

Continue only to Phase 30.2 read-only runtime state inspection implementation.
