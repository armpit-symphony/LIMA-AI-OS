# V1 Post-G31 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g31`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G31. The current chain is capability-open and authority-gated, but still candidate-only. V1-G31 adds deterministic fake-runtime consumer repository test preview metadata for Sparkbot and Arc-Bot-shell; it does not approve consumer repository edits, consumer test creation, live consumer imports/calls, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G32 consumer repository test edit approval request`.

Reason: the previewed test paths and expected assertion categories now exist in LIMA metadata. The next safe step is a request-only gate for adding the exact consumer test/fixture files in Sparkbot and Arc-Bot-shell while still blocking runtime source edits, live runtimes, providers/models, secrets, network/connectors, physical-world systems, and product-readiness claims.

Recommended order:

1. Consumer repository test edit approval request
2. Consumer repository test edit implementation only after exact approval
3. Consumer repository test edit audit and LIMA intake
4. Consumer fake-runtime import/call smoke request
5. Live consumer import/call lane only after fake-runtime repository test audit and separate approval
6. Live provider/model call dispatch lane only after credential policy proof
7. Connector authority lane
8. Browser/network authority lane
9. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer repository test edit approval request | Creates an exact gate for adding the previewed consumer test/fixture files. | Critical. | V1-G31 audit, authority-chain audit, readiness rollup. | Dedicated V1-G32 approval request. | LIMA request docs/tests/fixtures only; no consumer edits yet. | Stop on actual consumer edits, runtime source edits, live calls, provider/model calls, secrets, connectors, browser/network, product-readiness claims. | Approval-request fixture tests, file-map tests, no-live-call tests. | Yes. It is the next needed evidence gate. |
| Consumer repository test edit implementation | Adds actual Sparkbot and Arc-Bot-shell test/fixture files from the approved preview. | Critical. | Approved V1-G32 request, G31 preview metadata. | Dedicated implementation approval recorded from V1-G32. | Exact consumer test/fixture files plus LIMA intake docs/tests if approved. | Stop on runtime source edits, shell wiring, live calls, adapter execution beyond import-smoke, provider/model calls, secrets, connectors, browser/network, physical-world behavior. | Consumer focused tests, LIMA intake tests, rollback tests, diff checks in all repos. | Later. It requires V1-G32 approval first. |
| Consumer fake-runtime import/call smoke lane | Runs or records fake-runtime consumer-side smoke behavior after test edits. | Critical. | Approved consumer test edits and audit. | Dedicated fake-runtime smoke approval. | Consumer tests and LIMA intake metadata, exact file map. | Stop on live runtime calls, provider/model calls, secrets, connectors, browser/network, runtime source edits, product-readiness claims. | Consumer smoke tests, LIMA evidence tests, no-live-call/no-secret tests. | Later. Test edits should come first. |
| Live consumer import/call lane | Executes live imports/calls from consumer shells into LIMA. | Critical. | Fake-runtime repository test audit, final API/export decision, Guardian boundary, approval boundary, provider/model route boundary, runtime threat model. | Dedicated live import/call approval. | Consumer adapters, LIMA runtime boundary docs/tests, fake-runtime tests first. | Stop on bypassing Guardian, missing audit, secrets, provider/model calls, connectors, browser/network, physical-world, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests, then live tests only if approved. | Later. Live calls remain higher risk. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer call authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than fake-runtime evidence. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g32-consumer-repository-test-edit-approval-request`.

Do not start consumer repository test edit implementation, live consumer imports/calls, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
