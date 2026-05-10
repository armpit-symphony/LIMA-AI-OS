# Phase 1.19 Adapter Fixture Tests with Fake AuthContext

## Purpose

Add test-only fixtures proving Sparkbot HumanInput adapter payloads can carry identity/session/trust/autonomy references as passive metadata.

This phase does not implement live auth, session lookup, trusted device enforcement, or autonomy enforcement.

## What This Proves

- HumanInput payload metadata can carry actor/session/trust refs.
- AuthContext and trust contract IDs can be represented in tests.
- Adapter still returns HumanInput only.
- References remain passive.
- No authority is inferred.

## What This Does Not Prove

- verified identity
- verified session
- trusted device enforcement
- owner autonomy enforcement
- PIN verification
- face/voice recognition
- BCI/thought interpretation
- production adapter safety
- model/tool execution safety

## Fixture Rules

- fake AuthContext only
- fake TrustedDeviceContext only
- fake IdentityConfidence only
- fake OwnerAutonomyContext only
- no live lookup
- no enforcement
- no production use

## References Are Not Authority

`actor_ref`, `session_ref`, `trusted_context_ref`, `autonomy_notes`, privacy metadata, and fake AuthContext/trust objects do not authorize execution.

GuardianDecision remains mandatory later.

## Acceptance Criteria

- fixture tests exist
- adapter remains HumanInput-only
- no Sparkbot imports
- no live auth/session/trust/autonomy behavior
- no model/tool execution
- no GuardianDecision/ApprovalMetadata/PolicyDecision creation
- tests pass
