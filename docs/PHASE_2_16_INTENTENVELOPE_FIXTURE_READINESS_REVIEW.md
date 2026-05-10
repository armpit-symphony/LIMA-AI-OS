# Phase 2.16 IntentEnvelope Fixture Readiness Review

## Purpose

Review whether the Phase 2.15 IntentEnvelope test fixtures are ready for a future test-only IntentEnvelope fixture harness.

This review does not implement real IntentCompiler.
This review does not parse natural language.
This review does not authorize execution.

## Current Fixture Inventory

| Fixture file | Fixture purpose | Expected status | Explicit metadata required? | `raw_text` inert? | Safety notes |
| --- | --- | --- | --- | --- | --- |
| `typed_intent_fixtures.json` | Complete synthetic examples for expected IntentEnvelope-like shapes | `compiled` | Yes | Yes | Includes low, medium, high, and critical examples; safety-critical entries remain non-authorizing |
| `invalid_missing_metadata_fixtures.json` | Missing or incomplete metadata cases that must not create an envelope | `invalid` / `unknown` / `clarification_needed` | Missing by design | Yes | No hidden parser, model call, heuristic interpretation, execution, or GuardianDecision |
| `clarification_needed_fixtures.json` | Partial metadata cases requiring clarification | `clarification_needed` | Partial by design | Yes | Missing target or unknown/low-confidence explicit metadata must not be filled from raw text |
| `safety_critical_intent_fixtures.json` | Critical robot, terminal, secret, payment, deploy, admin, and destructive examples | `compiled` as expected shape only | Yes | Yes | Requires later Guardian/policy/approval review; no authorization and no auto-approval |

## What The Fixtures Prove

- valid fixture examples contain explicit typed metadata
- expected IntentEnvelope shapes can be represented
- invalid/missing metadata cases are represented
- clarification_needed cases are represented
- safety-critical cases are represented
- `raw_text` is inert
- GuardianDecision is absent
- safety-critical examples require later Guardian/policy/approval review

## What The Fixtures Do Not Prove

- real IntentCompiler behavior
- natural-language inference
- model-based intent extraction
- production adapter behavior
- tool execution safety
- GuardianDecision safety
- policy/approval enforcement
- audit persistence
- redaction runtime

## Fixture Coverage Assessment

| Category | Covered? | Risk class | Gap | Recommendation |
| --- | --- | --- | --- | --- |
| low-risk informational intent | yes | low | No harness validates the shape yet | Use in Phase 2.17 harness happy-path checks |
| calendar/scheduling intent | yes | medium | No harness validates typed calendar references yet | Use as medium-risk typed metadata case |
| draft-only communication intent | yes | medium | No harness validates draft-only non-send semantics yet | Keep send behavior blocked; validate shape only |
| email-send intent requiring later approval | yes | high | No Guardian/policy/approval validation yet | Keep as expected shape only; require later Guardian review |
| terminal critical request | yes | critical | No terminal safety enforcement exists | Keep terminal execution blocked and validate no authorization |
| robot safety-critical request | yes | critical | No Robo-OS safety enforcement exists | Keep physical action blocked and require later Guardian review |
| secret access | yes | critical | No vault/redaction runtime exists | Keep secret references synthetic and non-authorizing |
| payment/deploy/admin/destructive action | yes | critical | No policy/approval enforcement exists | Keep as review-only and require later Guardian/policy/approval review |
| missing metadata | yes | unknown / invalid | No future result object exists yet | Future harness may report invalid/unknown only |
| clarification needed | yes | medium | No clarification object is created yet | Future harness may report clarification_needed only |
| raw_text-only no metadata | yes | unknown | No parser exists and none should be added | Preserve raw_text as inert fixture text only |

## Readiness Decision

GO for Phase 2.17 IntentEnvelope Fixture Harness.

NO-GO for real IntentCompiler, natural-language inference, model/tool execution, GuardianDecision creation, or production wiring.

## Recommended Next Branch

`phase-2-17-intentenvelope-fixture-harness`

Purpose:

Create a test-only harness that validates explicit typed metadata fixtures against expected IntentEnvelope-like shapes.

Allowed:

- test-only helper
- fixtures only
- no real IntentCompiler
- no natural-language inference
- no model calls
- no tool execution
- no GuardianDecision creation
- no production behavior

## Future Harness Rules

The Phase 2.17 harness may:

- load intent fixture files
- validate required explicit metadata
- compare expected_intent_envelope shape
- report invalid / clarification_needed / safety_critical status

The Phase 2.17 harness must not:

- parse `raw_text`
- infer intent
- call models
- create production IntentEnvelope behavior
- create GuardianDecision
- execute tools
- approve actions

## Still Blocked

- real IntentCompiler
- natural-language inference
- model calls
- tool execution
- GuardianDecision creation from adapter
- production Sparkbot wiring
- `stream_chat_with_tools`
- `execute_tool`
- terminal/PTY
- Robo-OS physical action
- live auth/session lookup
- trusted device/autonomy enforcement
- audit persistence
- redaction runtime
- real Guardian / policy / approval enforcement

## Risk Register

| Risk | Severity | Current mitigation | Next action |
| --- | --- | --- | --- |
| `raw_text` accidentally parsed as intent | High | Fixtures and tests state `raw_text` is inert | Phase 2.17 harness must never read `raw_text` as source of intent |
| `expected_intent_envelope` mistaken for production behavior | High | Fixture docs label expected shapes as test artifacts | Future harness must remain shape-only and non-production |
| fixture harness mistaken for real IntentCompiler | High | Phase 2.16 blocks real compiler work | Phase 2.17 docs/tests must say harness is not a compiler |
| IntentEnvelope mistaken for authorization | High | Docs state IntentEnvelope is not authorization | Keep GuardianDecision mandatory before consequential behavior |
| safety-critical fixture mistaken for approval | High | Safety fixtures require later Guardian/policy/approval review | Harness must report critical status without approval |
| owner autonomy metadata mistaken for approval | Medium | Existing docs keep autonomy metadata passive | Future fixture additions must keep autonomy references non-authorizing |
| references mistaken for authority | Medium | Fixture refs are synthetic and non-authorizing | Future harness must treat refs as metadata only |

## Final Decision

GO for Phase 2.17 IntentEnvelope Fixture Harness.

NO-GO for real IntentCompiler, natural-language inference, execution, or GuardianDecision creation.
