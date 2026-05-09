# Phase 1.5 Policy/Risk Fake Evaluator

## Purpose

Define a fake, in-memory policy/risk evaluator for contract tests.

It converts `PolicyEvaluationContext` into `PolicyDecision` without enforcing real policy or authorizing execution.

## Non-Goals

- no real policy enforcement
- no production authorization
- no Guardian enforcement
- no approval enforcement
- no tool execution
- no model calls
- no driver calls
- no Sparkbot integration
- no Guardian Suite implementation copied

## Fake Evaluator Rules

- unknown packs/tools deny by default
- deny rules deny
- low-risk allow rules may allow
- confirmation/review/operator PIN/breakglass rules do not auto-allow
- high/critical packs do not auto-allow
- terminal/admin/deploy/payments/robo/secrets remain blocked by default

These are deterministic test rules only. They are not production policy.

## PolicyDecision Safety

`PolicyDecision` is policy guidance only.

It does not replace `GuardianDecision`.

It does not authorize execution by itself.

A future execution path still requires `GuardianDecision.decision_id` and approval metadata where policy requires it.

## Future Path

Future real policy evaluator remains blocked until:

- Guardian enforcement design
- approval enforcement design
- audit lineage emission
- redaction/privacy implementation
- Sparkbot adapter review
- tool-pack runtime enforcement design
