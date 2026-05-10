# IntentEnvelope Test Fixtures

These fixtures are synthetic review/test artifacts for Phase 2.15.

They describe explicit typed intent metadata and expected `IntentEnvelope` shapes for future tests. They do not implement a real IntentCompiler, natural-language inference, model calls, tool execution, GuardianDecision creation, production wiring, or Sparkbot integration.

Fixture rules:

- all fixture data is synthetic
- `raw_text` is inert fixture text only
- intent data must come from `explicit_metadata`
- missing or incomplete metadata must not imply `IntentEnvelope` creation
- `IntentEnvelope` is not authorization
- Guardian remains mandatory before consequential behavior
- owner autonomy metadata remains passive
- references are not authority

Fixture files:

- `typed_intent_fixtures.json`: complete explicit metadata with expected `IntentEnvelope` shapes
- `invalid_missing_metadata_fixtures.json`: raw text with missing/incomplete metadata where no envelope should be created
- `clarification_needed_fixtures.json`: partial explicit metadata requiring clarification
- `safety_critical_intent_fixtures.json`: critical-risk examples that require later Guardian/policy/approval review
