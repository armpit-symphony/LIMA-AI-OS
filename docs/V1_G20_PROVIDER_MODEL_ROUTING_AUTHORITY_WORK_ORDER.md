# V1-G20 Provider Model Routing Authority Work Order

Date: 2026-06-16
Branch: `prepare-v1-g20-provider-model-routing-authority-approval-request`
API status: `CANDIDATE_ONLY`

Work order verdict: `ready_if_operator_approves_provider_model_routing_authority_slice`

This is a conditional work order only. It does not record operator approval, approve implementation, route providers/models, call model providers, read secrets, execute tools, touch consumer repos, import consumer code, wire consumers, or add runtime dispatch.

## Approval Dependency

V1-G20 implementation may start only after the operator explicitly approves:

`docs/V1_G20_PROVIDER_MODEL_ROUTING_AUTHORITY_APPROVAL_REQUEST.md`

Until that approval is recorded, allowed work remains docs/tests/fixtures-only decision-recording work.

## Implementation Sequence If Approved

1. Add `lima/harness/v1_provider_model_routing_authority.py`.
2. Add deterministic validators for sanitized provider/model routing authority metadata.
3. Require route id, route family, and route intent scope metadata.
4. Require request id or Guardian decision id linkage.
5. Require tenant, shell, actor, and session scope metadata.
6. Require provider id, model id, model role, and provider boundary metadata.
7. Require data sensitivity and prompt context class metadata without raw prompts.
8. Require requested and allowed tool-pack scope metadata.
9. Require credential reference metadata without secret lookup.
10. Require budget, cost, and latency metadata.
11. Require fallback chain metadata and same-gate inheritance.
12. Require approval evidence linkage when risk policy requires approval.
13. Require provider configuration reference metadata.
14. Require audit/evidence linkage metadata.
15. Require proof-not-authority confirmation.
16. Reject raw prompts, customer data, credentials, provider tokens, API keys, and secrets.
17. Keep live provider/model calls unimplemented.
18. Keep secret lookup unimplemented.
19. Keep execution authority unimplemented.
20. Keep consumer integration unimplemented.
21. Add candidate exports only in `lima/harness/__init__.py`.
22. Add V1-G20 docs/tests/fixtures.

## Required Validation If Approved

Run at minimum:

- focused V1-G20 tests
- `python -m compileall lima`
- `python -m pytest -q tests -p no:cacheprovider`
- `git diff --check`
- `git diff --cached --check`
- `git status --short --branch`

## Non-Negotiable Stop Conditions

Stop if implementation requires or accidentally adds:

- files outside the approved V1-G20 file map
- live provider/model calls
- model request dispatch
- fallback execution
- provider readiness network checks
- Token Guardian live routing
- secret lookup
- credential access or persistence
- raw prompt or raw customer data persistence
- tool execution
- action execution
- file mutation execution
- consumer repo edits
- consumer code imports
- consumer runtime calls
- consumer integration
- route metadata becoming broad runtime authority
- connector/browser/network/device/robotics/physical-world behavior
- scheduled task execution
- external sends
- final API freeze
- product-readiness or production-readiness claims

## Recommended Next Step

Record exactly one valid operator choice in the V1-G20 operator decision packet.

If approved, implement only the LIMA-side provider/model routing authority metadata slice on branch `v1-g20-provider-model-routing-authority`. Do not call model providers, read secrets, dispatch live requests, execute tools, or touch consumer repos.
