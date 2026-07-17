# V1 Post-G39 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g39`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G39. The current chain is capability-open and authority-gated, but still candidate-only. V1-G39 adds exact static consumer integration import-smoke evidence; it does not approve consumer integration, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G40 shell wiring design approval request`.

Reason: Sparkbot and Arc-Bot-shell now have static candidate integration and import-smoke evidence. The next safe step is a request-only gate for a shell wiring design artifact that maps future shell integration boundaries without implementing runtime wiring. That request must not itself approve shell wiring implementation, provider/model dispatch, secrets, connectors/browser/network, physical-world systems, consumer integration implementation, or product readiness.

Recommended order:

1. Shell wiring design approval request
2. Shell wiring design implementation only after exact approval
3. Shell wiring design audit and readiness update
4. Consumer integration implementation gate only after design evidence
5. Live provider/model call dispatch lane only after credential policy proof
6. Connector authority lane
7. Browser/network authority lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Shell wiring design approval request | Creates an exact gate for a static design that maps future Sparkbot and Arc-Bot-shell wiring boundaries. | Critical. | V1-G39 implementation, G39 audit, authority-chain audit, readiness rollup. | Dedicated V1-G40 approval request. | LIMA request docs/tests/fixtures only; no design implementation in the request. | Stop on shell wiring implementation, consumer integration implementation, provider/model calls, secrets, connectors, browser/network, physical-world behavior, product-readiness claims. | Approval-request fixture tests, file-map tests, no-authority-escalation tests. | Yes. It is the next needed design gate. |
| Shell wiring design implementation | Documents shell boundary maps and future integration seams without runtime wiring. | Critical. | Approved V1-G40 request, G39 audit, authority-chain audit. | Dedicated implementation approval recorded from V1-G40. | LIMA docs/tests/fixtures if approved. | Stop on runtime module execution, shell wiring implementation, provider/model calls, network, secrets, physical-world behavior, product readiness. | Static design tests, boundary tests, no-live-call tests, rollback tests. | Later. It requires V1-G40 approval first. |
| Consumer integration implementation gate | Introduces bounded implementation only after design evidence and exact approval. | Critical. | Import-smoke evidence, shell wiring design, threat model, rollback plan. | Dedicated consumer integration implementation approval request. | Exact implementation files only after approval; likely consumer tests plus LIMA evidence first. | Stop on shell wiring implementation, provider/model calls, secrets, connectors, browser/network, physical-world behavior. | Static and fake-runtime tests first; no live provider/network by default. | Later. Design evidence should come first. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer integration authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than shell design evidence. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g40-shell-wiring-design-approval-request`.

Do not start shell wiring design, shell wiring implementation, consumer integration implementation, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
