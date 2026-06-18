# V1 Post-G43 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g43`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G43. The current chain is capability-open and authority-gated, but still candidate-only. V1-G43 adds deterministic fake-provider/no-secret/no-network provider/model dispatch evidence; it does not approve live provider/model calls, real model request dispatch execution, fallback execution, secret lookup, credential access, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G44 live provider/model call authority approval request`.

Reason: LIMA now has routing metadata and fake-provider dispatch evidence. The next safe step is not implementation by default; it is a request-only gate that asks whether the operator wants to authorize the next live-provider boundary. That request must explicitly cover network authority, credential access, secret lookup policy, redaction, audit evidence, rollback, and stop conditions.

Recommended order:

1. Live provider/model call authority approval request
2. Live provider/model call authority implementation only after exact approval
3. Live provider/model authority audit and readiness update
4. Fallback execution approval request, if needed
5. Connector/browser/network authority lane
6. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Live provider/model call authority approval request | Creates the exact decision gate for real provider/model connectivity after fake dispatch evidence. | Critical. | V1-G43 implementation, G43 audit, authority-chain audit, readiness rollup, G20 routing metadata. | Dedicated V1-G44 approval request. | LIMA request docs/tests/fixtures only; no implementation in the request. | Stop on live calls, credentials, secrets, network calls, provider config edits, external sends, fallback execution, connector/browser behavior, product-readiness claims. | Approval-request fixture tests, file-map tests, no-authority-escalation tests, credential/network boundary tests. | Yes. It is the next needed authority gate request. |
| Live provider/model call authority implementation | Adds only the exact bounded live-provider behavior authorized by a future approval. | Critical. | Approved V1-G44 request, credential policy, network boundary, provider configuration policy, audit persistence, redaction policy. | Dedicated implementation approval recorded from V1-G44. | Exact LIMA docs/tests/fixtures and narrowly approved runtime stubs or adapters only if the request approves them. | Stop on raw credentials, raw prompts, unredacted model responses, unscoped network calls, missing Guardian/audit path, fallback execution without approval, product readiness. | No-secret-leak tests, redaction tests, denied-provider tests, audit-link tests, bounded network policy tests. | Later. It requires V1-G44 approval first. |
| Fallback execution lane | Opens controlled failover behavior after live provider calls exist. | High. | Live provider/model call authority, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests, cost-boundary tests. | Later. Fallback should not precede live call authority. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Provider/model live-call boundary or a deliberate operator decision to prioritize connectors first, tenant scope, approval policy, audit retention. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later by default. Connector risk is higher than model-call request setup. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guardrails, approval policy, audit evidence, credential policy. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g44-live-provider-model-call-authority-approval-request`.

Do not start live provider/model call implementation, credential handling, secret lookup, network calls, provider configuration edits, fallback execution, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
