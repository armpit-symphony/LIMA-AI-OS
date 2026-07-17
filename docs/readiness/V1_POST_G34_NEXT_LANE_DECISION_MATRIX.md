# V1 Post-G34 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g34`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G34. The current chain is capability-open and authority-gated, but still candidate-only. V1-G34 adds exact focused consumer tests that call only approved LIMA adapter validators with sanitized metadata; it does not approve consumer integration, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G35 consumer integration compatibility review approval request`.

Reason: Sparkbot and Arc-Bot-shell now prove local adapter-validator call compatibility. The next safe step is a request-only gate for deciding whether to perform a bounded consumer integration compatibility review. That request must not itself wire shells, dispatch providers/models, access secrets, use connectors/browser/network, touch physical-world systems, or claim product readiness.

Recommended order:

1. Consumer integration compatibility review approval request
2. Consumer integration compatibility review implementation only after exact approval
3. Consumer integration compatibility review audit and readiness update
4. Bounded consumer integration design gate only after compatibility review
5. Live provider/model call dispatch lane only after credential policy proof
6. Connector authority lane
7. Browser/network authority lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer integration compatibility review approval request | Creates an exact gate for reviewing whether V1-G34 proof is enough to propose a bounded consumer integration lane. | Critical. | V1-G34 audit, authority-chain audit, readiness rollup. | Dedicated V1-G35 approval request. | LIMA request docs/tests/fixtures only; no integration implementation. | Stop on shell wiring, runtime/source edits, provider/model calls, secrets, connectors, browser/network, physical-world behavior, product-readiness claims. | Approval-request fixture tests, file-map tests, no-authority-escalation tests. | Yes. It is the next needed review gate. |
| Consumer integration compatibility review implementation | Reviews evidence and produces compatibility metadata, gap list, and next-lane recommendations. | Critical. | Approved V1-G35 request, G34 audit, authority-chain audit. | Dedicated implementation approval recorded from V1-G35. | LIMA docs/tests/fixtures only unless otherwise approved. | Stop on consumer repo edits, shell wiring, provider/model calls, secrets, connectors, browser/network, physical-world behavior, product-readiness claims. | Focused compatibility review tests, evidence-link tests, blocked-authority tests. | Later. It requires V1-G35 approval first. |
| Bounded consumer integration design gate | Proposes exact future shell/runtime integration file map after compatibility review. | Critical. | Compatibility review audit, threat model, rollback plan. | Dedicated design approval request. | Docs/tests/fixtures first; future consumer files only if approved. | Stop on runtime wiring, live provider/model calls, secrets, connectors, browser/network, product readiness. | Design fixture tests, boundary tests, rollback tests. | Later. It depends on compatibility review. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer integration authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than compatibility review. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g35-consumer-integration-compatibility-review-approval-request`.

Do not start consumer integration, shell wiring, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
