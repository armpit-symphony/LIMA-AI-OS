# Phase 2.0 Non-production Adapter Fixture Harness

## Purpose

Create a non-production harness that proves LIMA-owned Sparkbot payload fixtures can flow through the safe adapter and fake pipeline path.

This phase does not implement production Sparkbot wiring, live routes, model calls, tool execution, driver calls, persistence, redaction runtime, or real Guardian/policy/approval enforcement.

## Pipeline

```text
payload fixture
  -> SparkbotHumanInputAdapter
  -> HumanInput
  -> HumanInputFakePipelineBridge
  -> FakeGuardianPipeline
  -> fake lineage
```

The harness uses only LIMA-owned synthetic fixture dictionaries and existing fake components.

## Non-Goals

- no production Sparkbot wiring
- no Sparkbot imports
- no live routes
- no `stream_chat_with_tools`
- no `execute_tool`
- no model calls
- no tool execution
- no terminal/PTY
- no Robo-OS physical action
- no audit persistence
- no redaction runtime
- no real enforcement
- no autonomy enforcement

## Fixture Rules

- fixtures are LIMA-owned mirrors
- fixtures are synthetic
- fixtures are not authority
- drift metadata must exist
- dirty Sparkbot worktrees are not source of truth
- production adapter remains blocked

## Harness Rules

- test-only
- in-memory only
- no external services
- no DB/storage
- no env vars
- no secrets
- no raw sensitive data persistence
- no natural-language intent inference
- critical/unknown requests must not auto-approve

The harness may carry fixture metadata into `HumanInput` and into the fake pipeline. It must not infer real intent from natural language or turn fixture content into production authorization.

## MCP / Robot Fixture Handling

MCP approval and robot request fixtures are non-executing.

Robot fixtures are safety-critical.

The harness may prove they become `HumanInput` and fake pipeline records, but must not perform physical-world action or treat the result as production authorization.

MCP fixtures may become fake `tool_call` records for boundary validation only. They do not call tools, approve runs, or open an execution path.

## Acceptance Criteria

- harness module exists
- fixture tests run fixture -> `HumanInput` -> fake pipeline
- adapter remains `HumanInput`-only
- bridge remains separate
- fake pipeline only
- no Sparkbot imports
- no model/tool/driver execution
- no persistence
- critical/unknown requests do not auto-approve
- tests pass
