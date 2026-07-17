# V1 Post-G33 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g33`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G33. The current chain is capability-open and authority-gated, but still candidate-only. V1-G33 adds metadata-only fake-runtime import/call smoke evidence for Sparkbot and Arc-Bot-shell; it does not approve adapter execution, fake call execution, live consumer imports/calls, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G34 live consumer import/call approval request`.

Reason: fake-runtime smoke evidence now exists. The next safe step is a request-only gate for deciding whether to authorize a narrowly scoped live consumer import/call test lane. That request must not itself implement live calls or grant provider/model, secret, connector, browser/network, physical-world, or product-readiness authority.

Recommended order:

1. Live consumer import/call approval request
2. Live consumer import/call implementation only after exact approval
3. Live consumer import/call audit and LIMA intake
4. Consumer integration compatibility review after live-call audit
5. Live provider/model call dispatch lane only after credential policy proof
6. Connector authority lane
7. Browser/network authority lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Live consumer import/call approval request | Creates an exact gate for deciding whether Sparkbot and Arc-Bot-shell may run live import/call tests against LIMA candidate adapters. | Critical. | V1-G33 audit, authority-chain audit, readiness rollup. | Dedicated V1-G34 approval request. | LIMA request docs/tests/fixtures only; no live implementation. | Stop on live runtime calls, adapter execution, runtime source edits, provider/model calls, secrets, connectors, browser/network, physical-world behavior, product-readiness claims. | Approval-request fixture tests, file-map tests, no-live-call tests, boundary tests. | Yes. It is the next needed authority gate. |
| Live consumer import/call implementation | Executes narrowly scoped live consumer import/call tests if approved. | Critical. | Approved V1-G34 request, G33 smoke audit, exact consumer test scope, rollback plan. | Dedicated implementation approval recorded from V1-G34. | Exact consumer tests and LIMA evidence files only if approved. | Stop on bypassing Guardian, missing audit, provider/model calls, secrets, connectors, browser/network, runtime/source edits outside scope, physical-world behavior, product-readiness claims. | Focused live import/call tests, denied path tests, audit-link tests, no-network/no-secret tests unless explicitly approved. | Later. It requires V1-G34 approval first. |
| Consumer integration compatibility review | Determines whether live import/call evidence is enough to unfreeze a limited consumer integration path. | Critical. | Live consumer import/call audit, G21 compatibility metadata, G22 API freeze, G23 import dry-run evidence. | Dedicated compatibility review approval. | LIMA docs/tests/fixtures and maybe consumer docs only if approved. | Stop on shell wiring, provider/model dispatch, connector/browser/network, physical-world behavior, product-readiness claims. | Compatibility fixture tests, regression tests, no-authority escalation tests. | Later. It depends on live-call evidence. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer call authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than live consumer import/call proof. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g34-live-consumer-import-call-approval-request`.

Do not start live consumer import/call implementation, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
