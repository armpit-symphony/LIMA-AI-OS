# V1 Post-G32 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g32`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G32. The current chain is capability-open and authority-gated, but still candidate-only. V1-G32 adds exact consumer test/fixture files for Sparkbot and Arc-Bot-shell; it does not approve adapter execution, fake call execution, live consumer imports/calls, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G33 consumer fake-runtime import/call smoke approval request`.

Reason: consumer-side test files now exist. The next safe step is a request-only gate for recording fake-runtime import/call smoke evidence without live runtimes, providers/models, secrets, network/connectors, physical-world systems, runtime/source edits, or product-readiness claims.

Recommended order:

1. Consumer fake-runtime import/call smoke approval request
2. Consumer fake-runtime import/call smoke implementation only after exact approval
3. Consumer fake-runtime import/call smoke audit and LIMA intake
4. Live consumer import/call lane only after fake-runtime smoke audit and separate approval
5. Live provider/model call dispatch lane only after credential policy proof
6. Connector authority lane
7. Browser/network authority lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer fake-runtime import/call smoke approval request | Creates an exact gate for recording fake-runtime smoke evidence after consumer tests exist. | Critical. | V1-G32 audit, authority-chain audit, readiness rollup. | Dedicated V1-G33 approval request. | LIMA request docs/tests/fixtures only; no smoke implementation. | Stop on live runtime calls, adapter execution, runtime source edits, provider/model calls, secrets, connectors, browser/network, product-readiness claims. | Approval-request fixture tests, file-map tests, no-live-call tests. | Yes. It is the next needed evidence gate. |
| Consumer fake-runtime import/call smoke implementation | Records fake-runtime/no-network smoke evidence for Sparkbot and Arc-Bot-shell test paths. | Critical. | Approved V1-G33 request, G32 consumer tests. | Dedicated implementation approval recorded from V1-G33. | LIMA docs/tests/fixtures and exact consumer test metadata if approved. | Stop on live runtime calls, runtime source edits, adapter symbol execution beyond approved test-only import checks, provider/model calls, secrets, connectors, browser/network, physical-world behavior. | Focused smoke evidence tests, consumer focused tests, rollback tests, diff checks in all repos. | Later. It requires V1-G33 approval first. |
| Live consumer import/call lane | Executes live imports/calls from consumer shells into LIMA. | Critical. | Fake-runtime smoke audit, final API/export decision, Guardian boundary, approval boundary, provider/model route boundary, runtime threat model. | Dedicated live import/call approval. | Consumer adapters, LIMA runtime boundary docs/tests, fake-runtime tests first. | Stop on bypassing Guardian, missing audit, secrets, provider/model calls, connectors, browser/network, physical-world, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests, then live tests only if approved. | Later. Live calls remain higher risk. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer call authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than fake-runtime evidence. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g33-consumer-fake-runtime-import-call-smoke-approval-request`.

Do not start consumer fake-runtime import/call smoke implementation, live consumer imports/calls, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
