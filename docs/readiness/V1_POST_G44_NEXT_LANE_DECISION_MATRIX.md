# V1 Post-G44 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g44`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G44. The current chain is capability-open and authority-gated, but still candidate-only. V1-G44 adds a non-executing live provider/model call authority metadata/preflight validator; it does not export that validator through frozen `lima.harness.__all__`, execute live provider/model calls, make network calls, access credential values, execute fallback, approve connector/browser/network authority, approve physical-world authority, or claim product readiness.

## Recommendation

Recommended next lane: `V1-G45 runtime export cleanup/public API refresh approval request`.

Reason: G44 preserved the V1-G22 frozen public API surface. Before Sparkbot, Arc-Bot-shell, or other consumers can rely on the new validator through the frozen `lima.harness.__all__` surface, LIMA needs an exact request-only gate for export cleanup and public API fixture refresh.

Recommended order:

1. Runtime export cleanup/public API refresh approval request for G44 validator
2. Runtime export cleanup/public API refresh implementation only after exact approval
3. Export cleanup audit and readiness update
4. Live provider/model call execution approval request
5. Network provider egress and credential value access authority lanes
6. Connector/browser/network authority lane
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Runtime export cleanup/public API refresh request | Creates the exact gate for exposing the G44 validator through frozen public imports. | Medium. | V1-G44 implementation, G44 audit, authority-chain audit, readiness rollup, G22 API freeze, G28 export cleanup precedent. | Dedicated V1-G45 approval request. | LIMA request docs/tests/fixtures only; no implementation in the request. | Stop on live calls, network calls, credential access, runtime behavior changes beyond exports, consumer repo edits, product-readiness claims. | Approval-request fixture tests, file-map tests, frozen API boundary tests. | Yes. It is needed before consumer-facing import reliance. |
| Runtime export cleanup/public API refresh implementation | Adds the G44 validator to `lima.harness.__all__` and refreshes the frozen API fixture if approved. | Medium. | Approved V1-G45 request. | Dedicated implementation approval recorded from V1-G45. | `lima/harness/__init__.py`, V1-G22 freeze fixture, docs/tests/fixtures for G45 if approved. | Stop on symbol rename/removal, runtime behavior changes, live provider calls, network calls, credential access, consumer edits. | G22 frozen API tests, G44 tests, import tests, full suite. | Later. It requires V1-G45 approval first. |
| Live provider/model call execution request | Opens the decision gate for actual model service connectivity. | Critical. | G44 authority metadata/preflight, export cleanup if consumers need frozen imports, credential policy, network egress policy, audit policy. | Dedicated live execution approval request. | Request docs/tests/fixtures first; no live call implementation in request. | Stop on live calls before approval, raw credentials, raw prompts, unscoped network calls, fallback execution, product readiness. | Request fixture tests, no-authority-escalation tests, credential/network boundary tests. | Later. Export cleanup should come first for stable imports. |
| Network provider egress and credential value access authority | Separates the two riskiest execution prerequisites from model execution. | Critical. | Live call authority metadata, secret policy, provider egress policy, redaction policy. | Dedicated authority requests. | Contracts/docs/tests first; runtime only after approval. | Stop on credential values, provider tokens, unscoped network calls, missing audit, missing approval. | No-secret-leak tests, denied-egress tests, audit-link tests. | Later. This should be explicit and narrow. |
| Fallback execution lane | Opens controlled failover behavior after live provider execution exists. | High. | Live provider/model execution, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede live execution authority. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than export cleanup. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g45-runtime-export-cleanup-public-api-refresh-approval-request`.

Do not start export cleanup, live provider/model call execution, credential handling, secret lookup, network calls, provider configuration edits, fallback execution, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
