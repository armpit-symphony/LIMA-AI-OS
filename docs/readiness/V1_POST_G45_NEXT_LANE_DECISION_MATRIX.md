# V1 Post-G45 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g45`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G45. The current chain is capability-open and authority-gated, but still candidate-only. V1-G45 exposes the existing V1-G44 live provider/model call authority metadata validator through the frozen candidate `lima.harness.__all__` surface; it does not execute live provider/model calls, make network calls, access credential values, execute fallback, approve connector/browser/network authority, approve physical-world authority, or claim product readiness.

## Recommendation

Recommended next lane: `V1-G46 live provider/model call execution approval request`.

Reason: The non-executing authority validator is now publicly importable through `lima.harness`. The next step should be a request-only gate deciding whether LIMA may implement the first bounded live provider/model call execution slice. The request must not execute live calls by itself and must explicitly handle network egress, credential value access, redaction, audit evidence, fallback prohibition, rollback, and stop conditions.

Recommended order:

1. Live provider/model call execution approval request
2. Live provider/model call execution implementation only after exact approval
3. Network provider egress and credential value access authority boundaries if not included in the approved G46 slice
4. Execution audit and readiness update
5. Fallback execution approval request
6. Connector/browser/network authority lane
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Live provider/model call execution request | Opens the exact decision gate for first real model service connectivity. | Critical. | V1-G20 routing authority, V1-G43 dispatch evidence, V1-G44 live call authority metadata, V1-G45 public export refresh, credential/network/redaction/audit policies. | Dedicated V1-G46 approval request. | LIMA request docs/tests/fixtures only; no live calls in the request. | Stop on live calls before approval, raw credentials, raw prompts, unscoped network calls, fallback execution, consumer repo edits, product-readiness claims. | Approval-request fixture tests, no-authority-escalation tests, credential/network boundary tests, public harness import tests. | Yes. It is the next necessary gate before any live execution work. |
| Live provider/model call execution implementation | Implements the first bounded execution slice only if G46 is approved. | Critical. | Approved V1-G46 request, exact provider/model scope, network egress approval, credential reference/value rules, redaction and audit rules. | Dedicated implementation approval recorded from V1-G46. | To be defined by G46; likely LIMA harness runtime plus docs/tests/fixtures only. | Stop on unscoped egress, raw secrets or prompts, fallback, connector/browser behavior, consumer repo edits, missing Guardian/audit linkage. | Fake and guarded live-call tests as approved, denied-path tests, no-secret-emission tests, full suite. | Later. It requires explicit approval first. |
| Network provider egress and credential value access authority | Separates the two riskiest execution prerequisites from model execution if they are not approved together. | Critical. | Provider boundary metadata, vault reference policy, network policy, redaction policy, audit retention. | Dedicated authority requests or explicit inclusion in G46. | Contracts/docs/tests first; runtime only after approval. | Stop on raw credential values, provider tokens, unscoped network calls, missing audit, missing approval. | No-secret-leak tests, denied-egress tests, audit-link tests. | Possibly next if G46 chooses to split live execution from egress/credential access. |
| Fallback execution lane | Opens controlled failover behavior after first live provider execution exists. | High. | Live provider/model execution, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede first live execution authority. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider/model execution. |
| Consumer repo execution expansion | Moves from static consumer import/smoke evidence toward live consumer runtime calls. | High. | Stable public LIMA imports, approved execution boundary, Sparkbot and Arc shell expectations. | Dedicated consumer execution approval request. | Request docs/tests/fixtures first; consumer repos only after explicit approval. | Stop on unapproved consumer edits, live services, secrets, external sends, browser/network actions, product-readiness claims. | Consumer fixture tests, import/call tests, no live service tests unless approved. | Later. First LIMA execution authority should be defined before consumer runtime expansion. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g46-live-provider-model-call-execution-approval-request`.

Do not start live provider/model call execution, credential handling, secret lookup, network calls, provider configuration edits, fallback execution, actual runtime file mutation execution, connector, browser/network, physical-world, consumer runtime expansion, or product-readiness work until their own approval gates exist.
