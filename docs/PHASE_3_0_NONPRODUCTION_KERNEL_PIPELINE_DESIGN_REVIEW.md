# Phase 3.0 Non-production Kernel Pipeline Design Review

## Purpose

Design a future non-production end-to-end kernel fixture pipeline.

This review does not implement the pipeline.
This review does not create runtime behavior.
This review does not authorize production integration.

## Phase 2 Baseline

Phase 2 completed non-production fixtures, harnesses, report artifacts, and standing gates for the major kernel boundaries:

- Adapter / HumanInput fixture harness and regression report helpers.
- IntentEnvelope fixtures and fixture harness.
- Guardian request fixtures and fixture harness.
- Fake GuardianDecision fixtures and fixture harness.
- Adapter Safety Gate exists.
- IntentEnvelope Safety Gate exists.
- Guardian Request Safety Gate exists.
- Fake GuardianDecision Safety Gate exists.

Production integration remains blocked.
Real IntentCompiler remains blocked.
Real GuardianDecision remains blocked.
Enforcement, approval, execution, and audit persistence remain blocked.

## Tag / Milestone Check

Expected Phase 2.35 tag:

- `phase-2.35-phase-two-final-readiness-review`

Actual Phase 2.35 tag found:

- `phase-2.35-phase-two-final-readiness-review`

Tag status: expected tag found; no warning.

## Proposed Non-production Pipeline

Proposed future test-only design path:

```text
Sparkbot-shaped fixture / HumanInput fixture
  -> HumanInput
  -> IntentEnvelope fixture shape
  -> Guardian request fixture shape
  -> fake GuardianDecision fixture shape
  -> fake approval/spine/lineage/report artifacts
```

This is a proposed design path only.

The path may describe how existing LIMA-owned fixtures relate across stages. It must not become a runtime pipeline, production adapter, real compiler, real GuardianDecision, approval mechanism, enforcement path, execution path, audit writer, model caller, or tool caller.

## Boundary Responsibilities

| Boundary | Input | Output | Allowed in Phase 3 design | Still blocked |
| --- | --- | --- | --- | --- |
| Adapter / HumanInput | LIMA-owned Sparkbot-shaped payload fixture or HumanInput fixture | `HumanInput` shape and fixture regression report status | Describe fixture-to-HumanInput relationship and cite adapter safety gate | Sparkbot imports, live routes/WebSocket, production adapter, `stream_chat_with_tools`, `execute_tool`, model/tool execution, terminal/PTY, Robo-OS physical action, live auth/session/trust/autonomy enforcement |
| IntentEnvelope | `HumanInput` reference plus explicit typed metadata fixture | IntentEnvelope fixture shape | Map explicit metadata fields and keep `raw_text` inert | Real IntentCompiler, natural-language inference, `raw_text` parsing, model calls, tool execution, GuardianDecision creation |
| Guardian request | IntentEnvelope fixture reference plus explicit request fixture | Guardian request fixture shape | Describe request-only shape and requested tool-pack metadata | Real GuardianDecision, approval, enforcement, granted/allowed tool packs, ApprovalMetadata recording, execution, audit persistence |
| Fake GuardianDecision | Guardian request fixture reference plus fake decision fixture | Fake GuardianDecision fixture shape | Describe test-only statuses and fake decision report shape | Real GuardianDecision, production authorization, policy enforcement, approval enforcement, action approval, execution |
| Fake approval metadata | Reference-only fake approval field or fixture note | Fake approval reference for review artifacts | Describe as reference-only test metadata | ApprovalMetadata recording, approval verification, approval enforcement, action approval |
| Fake Spine/Audit lineage | Fixture lineage IDs and fake pipeline/report metadata | In-memory fake lineage or report artifact | Describe lineage relationship and review-only artifacts | Audit persistence, runtime state, production telemetry, Guardian evidence, redaction runtime |
| Regression/report artifact | Fixture harness results | In-memory report or review-only markdown/dict artifact | Describe expected non-production report relationships | Audit persistence, production authorization, runtime state, production telemetry, file/DB/network side effects |

## Required Gates

The following standing gates must remain active for any future Phase 3 work:

- `docs/ADAPTER_SAFETY_GATE.md`
  - must remain active
  - must pass relevant tests
  - must block production creep
- `docs/INTENTENVELOPE_SAFETY_GATE.md`
  - must remain active
  - must pass relevant tests
  - must block production creep
- `docs/GUARDIAN_REQUEST_SAFETY_GATE.md`
  - must remain active
  - must pass relevant tests
  - must block production creep
- `docs/FAKE_GUARDIANDECISION_SAFETY_GATE.md`
  - must remain active
  - must pass relevant tests
  - must block production creep

## Test-only Composition Rules

Future non-production composition may use LIMA-owned fixtures only.
Future non-production composition may use test helpers only.
Future non-production composition may produce in-memory reports only.

Future non-production composition may not:

- write audit persistence
- call models
- execute tools
- import Sparkbot
- wire live routes
- create real GuardianDecision
- enforce policy or approval
- approve action

## Proposed Phase 3.1

Recommended next branch:

`phase-3-1-nonproduction-kernel-pipeline-fixture-map`

Purpose:

Create a docs/tests-only mapping plan that maps existing fixtures across pipeline stages:

- Sparkbot payload fixtures
- IntentEnvelope fixtures
- Guardian request fixtures
- fake GuardianDecision fixtures

Allowed:

- mapping doc
- fixture relationship table
- no runtime behavior
- no pipeline implementation
- no execution

## Phase 3.1 Allowed Scope

Allowed:

- docs-only or tests-only fixture map
- fixture ID relationship plan
- expected stage compatibility matrix
- no runtime pipeline
- no production integration
- no real compiler/decision/enforcement

## Still Blocked

- production Sparkbot integration
- live route/WebSocket adapter
- `stream_chat_with_tools`
- `execute_tool`
- real IntentCompiler
- natural-language inference
- real GuardianDecision
- Guardian enforcement
- policy enforcement
- approval enforcement
- ApprovalMetadata recording
- action approval
- tool execution
- model calls
- audit persistence
- redaction runtime
- terminal/PTY
- Robo-OS physical action
- live auth/session/trust/autonomy enforcement

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| Phase 3 mistaken for production | Critical | Phase 2.35 scopes Phase 3.0 as non-production design/review only | Repeat production NO-GO in Phase 3 docs and PR review |
| fixture pipeline mistaken for runtime | High | Phase 2 gates state fixtures and harnesses are not runtime authority | Keep Phase 3.1 to fixture mapping, not pipeline implementation |
| fake GuardianDecision mistaken for authorization | Critical | Fake GuardianDecision gate states fake decisions are test-only and non-authorizing | Require fake GuardianDecision gate review before related changes |
| report artifacts mistaken for audit persistence | High | Adapter gate states reports are not audit persistence, telemetry, evidence, authorization, or runtime state | Keep all report artifacts review-only and in-memory unless a future explicit audit phase approves persistence |
| safety gates forgotten | High | Four standing safety gates were established in Phase 2 | List applicable gates in each Phase 3 PR |
| helper code starts executing | Critical | Existing harness tests scan for forbidden imports, names, and side-effect paths | Keep Phase 3.1 docs/tests-only and extend scans only if helper scope changes |
| Sparkbot integration pressure | High | Adapter safety gate keeps production Sparkbot wiring NO-GO | Keep Sparkbot imports and live routes blocked |
| real compiler/decision/enforcement started too early | Critical | IntentEnvelope, Guardian request, and fake GuardianDecision gates block real compiler and enforcement behavior | Require explicit future readiness review before any real compiler, decision, or enforcement work |
| fixture mismatch across stages | Medium | Phase 2 fixtures validate each boundary independently | Use Phase 3.1 fixture map to identify relationships and compatibility gaps without composing runtime behavior |

## Final Decision

GO for Phase 3.1 Non-production Kernel Pipeline Fixture Map.

NO-GO for production integration, real IntentCompiler, real GuardianDecision, enforcement, approval, execution, or audit persistence.
