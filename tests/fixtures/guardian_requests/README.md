# Guardian Request Test Fixtures

These fixtures are synthetic review/test artifacts for Phase 2.22.

They describe explicit IntentEnvelope-like inputs and expected Guardian request shapes for future tests. They do not create GuardianDecision, enforce policy, approve actions, execute tools, persist audit data, call models, implement real IntentCompiler, infer intent from natural language, wire Sparkbot, or call production systems.

Fixture rules:

- all fixture data is synthetic
- no secrets or real user data are allowed
- Guardian request is not GuardianDecision
- Guardian request is not approval
- `requested_tool_packs` are requests only
- `autonomy_context_ref` is passive only
- `approval_requirement_ref` is descriptive only
- privacy/redaction metadata is not enforcement
- no ApprovalMetadata is created
- no audit persistence is created
- no execution occurs

Fixture files:

- `valid_guardian_request_fixtures.json`: complete explicit request metadata with expected Guardian request shapes
- `invalid_guardian_request_fixtures.json`: incomplete or malformed request metadata where no accepted request should be produced
- `safety_critical_guardian_request_fixtures.json`: critical-risk examples requiring later Guardian/policy/approval review
- `approval_required_guardian_request_fixtures.json`: approval-required examples where approval refs remain descriptive only
