# V1 Post-G26 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g26`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G26. The current chain is capability-open and authority-gated, but still candidate-only. V1-G26 adds static Sparkbot and Arc-Bot-shell proof edits; it does not approve live consumer imports/calls, shell wiring, runtime export cleanup, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G27 first consumer frozen API import-smoke approval request`.

Reason: static consumer proof edits are now present in both target repositories. The next safe test-oriented step is a narrowly scoped import-smoke gate proving that consumer tests can import the frozen LIMA public API surface without calling runtime behavior.

Recommended order:

1. First consumer frozen API import-smoke approval request
2. Consumer import-smoke implementation only after exact approval
3. Consumer import-smoke audit
4. Runtime export cleanup only after import-smoke evidence is stable
5. Live consumer import/call lane only after import-smoke audit and a separate runtime call approval
6. Live provider/model call dispatch lane only after credential policy proof
7. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
8. Connector authority lane
9. Browser/network authority lane
10. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| First consumer frozen API import-smoke approval request | Creates an exact gate for consumer tests to import frozen LIMA APIs without runtime calls. | High. | V1-G22, V1-G24, V1-G25, V1-G26, authority-chain audit. | Dedicated V1-G27 approval request. | LIMA docs/tests/fixtures request files only; no consumer edits in the request branch. | Stop on live runtime calls, consumer runtime imports beyond test-only LIMA API import, provider/model calls, secrets, connectors, browser/network, product-readiness claims. | Approval-request fixture tests, no live-call tests, frozen API reference tests. | Yes. It is the next needed proof before live integration. |
| Consumer import-smoke implementation | Adds exact test-only imports of frozen LIMA API surfaces in Sparkbot and Arc-Bot-shell. | Critical. | Approved V1-G27 request, clean consumer repo status, exact file scope, rollback plan. | Dedicated implementation approval recorded from V1-G27. | Consumer tests/fixtures plus LIMA intake docs/tests/fixtures. | Stop on runtime wiring, app source changes, provider/model calls, connectors, secrets, external sends, product-readiness claims. | Consumer focused tests, LIMA focused tests, no-network/no-secret checks, full LIMA suite. | Later. It requires V1-G27 approval first. |
| Runtime export cleanup lane | Removes or reshapes candidate exports after consumer import-smoke evidence is stable. | High. | V1-G22, V1-G27 audit, export diff, rollback plan, consumer notice plan. | Dedicated cleanup approval. | Export files, docs/tests/fixtures, compatibility tests. | Stop on unapproved symbol removal, consumer breakage, hidden runtime behavior, live calls, product-readiness claims. | Export-diff tests, import tests, compatibility fixtures, rollback tests. | Later. Cleanup should wait until consumer import-smoke evidence exists. |
| Live consumer import/call lane | Executes live imports/calls from consumer shells into LIMA. | Critical. | Consumer import-smoke audit, final API freeze, Guardian boundary, approval boundary, provider/model route boundary, runtime threat model. | Dedicated live import/call approval. | Consumer adapters, LIMA runtime boundary docs/tests, fake-runtime tests first. | Stop on bypassing Guardian, missing audit, secrets, provider/model calls, connectors, browser/network, physical-world, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests. | Later. Live calls are higher risk than import-smoke tests. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer import-smoke proof should land first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than import-smoke testing. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g27-first-consumer-frozen-api-import-smoke-approval-request`.

Do not start consumer import-smoke implementation, runtime export cleanup, live consumer imports/calls, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
