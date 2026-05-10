# Phase 2.15 IntentEnvelope Test Fixtures

## Purpose

Create synthetic fixtures for explicit typed intent metadata and expected IntentEnvelope shapes.

This phase does not implement real IntentCompiler.
This phase does not infer intent from natural language.
This phase does not authorize execution.

## Fixture Rule

IntentEnvelope fixtures must use explicit typed metadata.

`raw_text` may appear only as inert fixture text and must not be parsed.

## Fixture Categories

- `typed_intent_fixtures.json`: valid typed intent examples with complete explicit metadata and expected IntentEnvelope shapes.
- `invalid_missing_metadata_fixtures.json`: raw text with missing or incomplete explicit metadata where no IntentEnvelope should be created.
- `clarification_needed_fixtures.json`: partial explicit metadata that requires clarification before any complete envelope candidate exists.
- `safety_critical_intent_fixtures.json`: critical-risk robot, terminal, secret, payment, deploy, and admin examples that require later Guardian/policy/approval review.

## Explicit Metadata Fields

- `intent_type`
- `action_type`
- `risk_class`
- `target_ref`
- `typed_args`
- `evidence_refs`
- `requested_tool_packs`
- `approval_level`
- `privacy_class`
- `redaction_class`
- `lineage_id`
- `reason`
- `confidence`

## Non-Goals

- no real IntentCompiler
- no natural-language inference
- no model calls
- no hidden parser
- no tool execution
- no GuardianDecision creation
- no production wiring
- no Sparkbot imports

## IntentEnvelope Is Not Authorization

IntentEnvelope does not authorize action.

GuardianDecision remains mandatory before consequential behavior.

## Safety-Critical Intent Rules

Safety-critical fixtures must not imply approval.

Robot, terminal, secret, payment, deploy, admin, and destructive intents require later Guardian/policy/approval review.

## Acceptance Criteria

- fixture files exist
- fixtures are synthetic/no secrets
- explicit metadata exists for valid fixtures
- missing metadata fixtures do not imply envelope creation
- `raw_text` is never used as source of intent
- tests validate fixture shape
- no runtime behavior added
