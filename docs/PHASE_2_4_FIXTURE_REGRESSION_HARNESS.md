# Phase 2.4 Fixture Regression Harness

## Purpose

Create a non-production regression harness for LIMA-owned Sparkbot payload fixtures.

This proves fixtures can be repeatedly checked against the safe adapter/fake-pipeline path without production wiring.

## Regression Path

```text
fixture file
  -> fixture loader
  -> AdapterFixtureHarness
  -> SparkbotHumanInputAdapter
  -> HumanInput
  -> HumanInputFakePipelineBridge
  -> FakeGuardianPipeline
  -> fake lineage
  -> FixtureRegressionReport
```

## Non-Goals

- no Sparkbot imports
- no production route wiring
- no model/tool execution
- no terminal/PTY
- no Robo-OS physical action
- no live auth/session lookup
- no trust/autonomy enforcement
- no persistence
- no real enforcement

## Unsupported / Non-executing Categories

Unsupported categories must be explicit.

They may not pass silently.

MCP, robot, and unknown categories remain non-executing. Compatible MCP and robot fixtures may flow through the fake pipeline only to prove non-approval posture; that does not imply execution readiness.

## Safety Checks

- critical and unknown paths do not auto-approve
- model-routing metadata does not call models
- auth/session refs are not authority
- autonomy metadata is passive
- fixtures are synthetic and contain no secrets
- fake lineage is in memory only and is not audit persistence

## Acceptance Criteria

- regression helper exists
- regression tests load all fixtures
- compatible fixtures run through safe harness
- unsupported categories explicit
- no failed results
- no Sparkbot imports
- no execution/persistence
- critical/unknown paths do not auto-approve
