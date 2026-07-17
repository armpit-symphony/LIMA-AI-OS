# V1 Post-G28 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g28`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G28. The current chain is capability-open and authority-gated, but still candidate-only. V1-G28 completes the approved adapter export cleanup; it does not approve live consumer imports/calls, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G29 live consumer import/call planning approval request`.

Reason: Sparkbot and Arc-Bot-shell have import-smoke evidence, and the adapter export surface is cleaned up. The next safe step is a request-only planning gate for fake-runtime/no-network live consumer import/call boundaries before any live call implementation is considered.

Recommended order:

1. Live consumer import/call planning approval request
2. Live consumer import/call planning implementation only after exact approval
3. Planning audit
4. Fake-runtime consumer call implementation approval request
5. Fake-runtime consumer call implementation and audit
6. Live provider/model call dispatch lane only after credential policy proof
7. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
8. Connector authority lane
9. Browser/network authority lane
10. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Live consumer import/call planning approval request | Creates an exact gate to plan fake-runtime consumer call boundaries without live calls. | High. | V1-G27 audit, V1-G28 audit, authority-chain audit, readiness rollup. | Dedicated V1-G29 approval request. | LIMA docs/tests/fixtures request files only; no runtime call implementation. | Stop on live calls, consumer repo edits, runtime wiring, provider/model calls, secrets, connectors, browser/network, product-readiness claims. | Approval-request fixture tests, boundary metadata tests, no-live-call tests. | Yes. It is the next needed planning gate. |
| Live consumer import/call planning implementation | Records fake-runtime/no-network call boundary plans for Sparkbot and Arc-Bot-shell. | High. | Approved V1-G29 request, cleaned export surface, consumer smoke evidence. | Dedicated implementation approval recorded from V1-G29. | LIMA docs/tests/fixtures only unless separately approved. | Stop on actual live calls, consumer source edits, shell wiring, secrets, provider/model calls, connectors, browser/network, product-readiness claims. | Planning fixture tests, denied-path metadata tests, consumer evidence link tests. | Later. It requires V1-G29 approval first. |
| Fake-runtime consumer call implementation | Adds deterministic fake-runtime call tests without live provider/model, connector, or network behavior. | Critical. | Planning audit, Guardian boundary, approval boundary, provider/model route boundary. | Dedicated fake-runtime call approval. | Exact LIMA and consumer test files; no production wiring. | Stop on live runtime calls, bypassing Guardian, secrets, network, external sends, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests. | Later. Planning should come first. |
| Live consumer import/call lane | Executes live imports/calls from consumer shells into LIMA. | Critical. | Fake-runtime call audit, final API/export decision, Guardian boundary, approval boundary, provider/model route boundary, runtime threat model. | Dedicated live import/call approval. | Consumer adapters, LIMA runtime boundary docs/tests, fake-runtime tests first. | Stop on bypassing Guardian, missing audit, secrets, provider/model calls, connectors, browser/network, physical-world, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests, then live tests only if approved. | Later. Live calls remain higher risk. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer call authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than planning. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g29-live-consumer-import-call-planning-approval-request`.

Do not start live consumer import/call planning implementation, fake-runtime calls, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
