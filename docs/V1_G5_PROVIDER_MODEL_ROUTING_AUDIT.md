# V1-G5 Provider/Model Routing Audit

## Audit Verdict

Verdict: `accept_static_provider_model_routing_contract_only`.

`V1-G5` satisfies the static request to define provider/model routing contract and acceptance-test design evidence. It is insufficient for runtime routing, live provider calls, or V1 product readiness.

## Audit Questions

Did V1-G5 define provider/model route families?

- Yes. The contract covers primary, backup/fallback, heavy-hitter, agent override, Workstation/model-seat, local endpoint, Codex subscription, and provider-readiness/self-inspection route families.

Did V1-G5 provide required route metadata?

- Yes. The contract requires route, shell, actor/session, intent, decision, provider/model, role, family, data sensitivity, prompt context, tool-pack, secret-ref, budget, latency, fallback, audit evidence, and policy metadata.

Did V1-G5 require Guardian gating?

- Yes. Future routing requires a scoped `GuardianDecision` for consequential model calls.

Did V1-G5 require shell and tool-pack scoping?

- Yes. The route must be allowed by shell policy and `GuardianDecision.allowed_tool_packs`.

Did V1-G5 protect provider secrets?

- Yes. Raw provider keys, OAuth tokens, CLI auth contents, and endpoint credentials are forbidden in route metadata. The contract uses secret refs or explicit no-key local provider posture.

Did V1-G5 constrain fallback routing?

- Yes. Fallback candidates must satisfy the same gates as the primary route.

Did V1-G5 provide machine-readable fixture evidence?

- Yes. `tests/fixtures/runtime_extraction/v1_g5_provider_model_routing_contract.json` summarizes the static contract and lists all case fixtures.

Did V1-G5 avoid runtime provider/model calls?

- Yes. All fixtures keep model/provider call flags false.

Did V1-G5 avoid `lima/`, `tests/support`, and runtime export changes?

- Yes.

Did V1-G5 avoid importing or copying Sparkbot code?

- Yes. Sparkbot is used as read-only behavior reference only.

## Accepted Evidence

- Static provider/model route families.
- Static route metadata requirements.
- Static Guardian, shell, tool-pack, secret, budget, privacy, and audit gates.
- Static fallback inheritance requirement.
- Static safe route-shape evidence.
- Static fail-closed evidence for private data, expensive model, unknown provider, missing secret ref, tool-scope mismatch, shell-disallowed provider, and forged route decision.

## Rejected / Non-Accepted Claims

- runtime provider/model routing
- model calls
- provider SDK/API/CLI/local endpoint calls
- live Token Guardian routing
- provider readiness checks
- secret lookup
- fallback execution
- runtime `GuardianDecision`
- approval enforcement
- audit persistence
- shell runtime wiring
- haptic device behavior
- production readiness
- V1 product readiness

## Remaining Gaps

- no haptic intent metadata contract
- no first-shell integration proof
- no audit persistence
- no runtime routing implementation
- no shell runtime wiring
- no production behavior

## Next Recommendation

Move to `V1-G6`: haptic intent metadata as shell-contract metadata only.
