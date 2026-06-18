# V1 Post-G40 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g40`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G40. The current chain is capability-open and authority-gated, but still candidate-only. V1-G40 adds exact metadata-only shell wiring design evidence; it does not approve consumer integration implementation, shell runtime wiring implementation, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G41 consumer integration implementation approval request`.

Reason: Sparkbot and Arc-Bot-shell now have static candidate integration evidence, import-smoke evidence, and shell boundary design maps. The next safe step is a request-only gate for bounded consumer integration implementation evidence. That request must not itself approve shell runtime wiring implementation, provider/model dispatch, secrets, connectors/browser/network, physical-world systems, or product readiness unless the approval request explicitly includes those authorities.

Recommended order:

1. Consumer integration implementation approval request
2. Consumer integration implementation only after exact approval
3. Consumer integration implementation audit and readiness update
4. Shell wiring implementation request only after candidate integration evidence
5. Live provider/model call dispatch lane only after credential policy proof
6. Connector authority lane
7. Browser/network authority lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer integration implementation approval request | Creates an exact gate for bounded implementation evidence after static import-smoke and shell boundary design evidence. | Critical. | V1-G40 implementation, G40 audit, authority-chain audit, readiness rollup. | Dedicated V1-G41 approval request. | LIMA request docs/tests/fixtures only; no implementation in the request. | Stop on implementation outside approved future files, shell runtime wiring, provider/model calls, secrets, connectors, browser/network, physical-world behavior, product-readiness claims. | Approval-request fixture tests, file-map tests, no-authority-escalation tests. | Yes. It is the next needed implementation gate request. |
| Consumer integration implementation | Adds only the exact bounded implementation evidence authorized by a future approval. | Critical. | Approved V1-G41 request, G40 design evidence, G40 audit, authority-chain audit. | Dedicated implementation approval recorded from V1-G41. | Exact LIMA docs/tests/fixtures and exact consumer static tests/fixtures if approved. | Stop on shell runtime wiring implementation, provider/model calls, secrets, connectors, browser/network, physical-world behavior, product readiness. | Static/fake-runtime integration tests, no-live-call tests, rollback tests, evidence-link tests. | Later. It requires V1-G41 approval first. |
| Shell wiring implementation approval request | Creates an exact future gate for runtime shell wiring after bounded integration evidence. | Critical. | Shell boundary design evidence, consumer integration implementation evidence, rollback plan, threat model review. | Dedicated shell wiring implementation approval request. | Request docs/tests/fixtures only. | Stop on runtime wiring implementation, live provider/model dispatch, connector/browser/network behavior, secrets, physical-world behavior, product readiness. | Approval-request tests, boundary tests, no-runtime-call tests. | Later. Candidate integration implementation should be proven first. |
| Shell wiring implementation | Wires approved shells only through Guardian-gated boundaries. | Critical. | Approved shell wiring implementation request, consumer integration evidence, credential policy, audit persistence. | Dedicated shell wiring implementation approval. | Exact shell adapter/contract files and tests only if approved. | Stop on bypassing Guardian, direct provider dispatch, unapproved file mutation, connector/browser/network behavior, physical-world behavior, product-readiness claims. | Guarded route tests, denied direct-path tests, audit-link tests, no-network/no-secret tests. | Later. It is higher risk than the next request-only gate. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer integration and shell wiring authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than integration evidence. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g41-consumer-integration-implementation-approval-request`.

Do not start consumer integration implementation, shell wiring implementation, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
