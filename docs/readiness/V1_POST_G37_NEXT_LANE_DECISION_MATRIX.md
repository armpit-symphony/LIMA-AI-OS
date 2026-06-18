# V1 Post-G37 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g37`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G37. The current chain is capability-open and authority-gated, but still candidate-only. V1-G37 adds metadata-only consumer integration patch-preview evidence; it does not approve consumer repository edits, consumer integration, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G38 consumer repository edit approval request`.

Reason: Sparkbot and Arc-Bot-shell now have sanitized patch-preview evidence for exact future consumer test/fixture files. The next safe step is a request-only gate for creating those files. That request must not itself approve consumer integration, shell wiring, provider/model dispatch, secrets, connectors/browser/network, physical-world systems, or product readiness.

Recommended order:

1. Consumer repository edit approval request
2. Consumer repository edit implementation only after exact approval
3. Consumer repository edit audit and readiness update
4. Consumer integration import-smoke gate only after consumer repository edit approval
5. Shell wiring design gate only after import-smoke evidence
6. Live provider/model call dispatch lane only after credential policy proof
7. Connector authority lane
8. Browser/network authority lane
9. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer repository edit approval request | Creates an exact gate for applying the previewed static consumer test/fixture edits. | Critical. | V1-G37 audit, authority-chain audit, readiness rollup. | Dedicated V1-G38 approval request. | LIMA request docs/tests/fixtures only; no edit implementation in the request. | Stop on consumer repo edits before approval, shell wiring, runtime/source edits outside exact scope, provider/model calls, secrets, connectors, browser/network, physical-world behavior, product-readiness claims. | Approval-request fixture tests, file-map tests, no-authority-escalation tests. | Yes. It is the next needed edit gate. |
| Consumer repository edit implementation | Creates exact static consumer test/fixture files previewed by V1-G37. | Critical. | Approved V1-G38 request, G37 audit, authority-chain audit. | Dedicated implementation approval recorded from V1-G38. | Exact consumer test/fixture files plus LIMA evidence docs/tests/fixtures. | Stop on unapproved files, runtime/source edits beyond exact scope, shell wiring, provider/model calls, secrets, connectors, browser/network, physical-world behavior, product-readiness claims. | Consumer focused tests, LIMA evidence tests, rollback tests. | Later. It requires V1-G38 approval first. |
| Consumer integration import-smoke gate | Confirms imported candidate consumer integration surfaces stay bounded and static. | Critical. | Approved consumer repo edit, exact import surface, no shell wiring. | Dedicated import-smoke approval request. | LIMA docs/tests/fixtures and exact consumer tests only if approved. | Stop on runtime module execution, shell wiring, provider/model calls, network, secrets, product readiness. | Static import-smoke tests, boundary tests, no-live-call tests. | Later. It depends on consumer repository edits. |
| Shell wiring design gate | Designs future shell wiring without implementing live shell behavior. | Critical. | Import-smoke evidence, threat model, rollback plan. | Dedicated shell wiring design approval request. | LIMA docs/tests/fixtures first. | Stop on shell runtime implementation, provider/model calls, secrets, connectors, browser/network, physical-world behavior. | Design fixture tests, authority-boundary tests. | Later. Integration evidence should come first. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer integration authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than repo edit. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g38-consumer-repository-edit-approval-request`.

Do not start consumer repository edits, consumer integration, shell wiring, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
