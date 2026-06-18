# V1 Post-G42 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g42`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G42. The current chain is capability-open and authority-gated, but still candidate-only. V1-G42 adds exact static shell wiring implementation evidence; it does not approve runtime shell wiring execution, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G43 provider/model dispatch approval request`.

Reason: Sparkbot and Arc-Bot-shell now have static shell wiring implementation evidence. The next safe step is a request-only gate for provider/model dispatch authority. That request should keep credentials, live network calls, connector authority, browser/network authority, physical-world systems, and product readiness out of scope unless the operator explicitly approves them.

Recommended order:

1. Provider/model dispatch approval request
2. Provider/model dispatch implementation only after exact approval
3. Provider/model dispatch audit and readiness update
4. Connector authority lane
5. Browser/network authority lane
6. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Provider/model dispatch approval request | Creates an exact gate for future model routing and dispatch authority after static shell wiring evidence. | Critical. | V1-G42 implementation, G42 audit, authority-chain audit, readiness rollup. | Dedicated V1-G43 approval request. | LIMA request docs/tests/fixtures only; no implementation in the request. | Stop on live calls, credentials, secrets, connector/browser/network behavior, external sends, physical-world behavior, product-readiness claims. | Approval-request fixture tests, file-map tests, no-authority-escalation tests. | Yes. It is the next needed authority gate request. |
| Provider/model dispatch implementation | Adds only the exact bounded model dispatch evidence authorized by a future approval. | Critical. | Approved V1-G43 request, V1-G20 routing metadata, credential policy, audit persistence. | Dedicated implementation approval recorded from V1-G43. | Exact LIMA docs/tests/fixtures and possibly fake-provider contract files if approved. | Stop on raw credentials, live network calls unless explicitly approved, direct shell bypass, missing Guardian/audit path, product readiness. | Fake-provider tests, denied-route tests, no-secret tests, fallback policy tests, audit-link tests. | Later. It requires V1-G43 approval first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Provider/model dispatch evidence, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than model-dispatch evidence. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g43-provider-model-dispatch-approval-request`.

Do not start provider/model dispatch implementation, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
