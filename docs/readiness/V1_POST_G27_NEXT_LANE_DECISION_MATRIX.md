# V1 Post-G27 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g27`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G27. The current chain is capability-open and authority-gated, but still candidate-only. V1-G27 adds test-only Sparkbot and Arc-Bot-shell frozen API import-smoke evidence; it does not approve calls to imported symbols, live consumer imports/calls, shell wiring, runtime export cleanup, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G28 runtime export cleanup approval request`.

Reason: consumer import-smoke evidence now proves the frozen candidate symbols are importable. The next safe step is an exact request-only gate that asks whether runtime export cleanup may be implemented, with explicit compatibility, rollback, and stop conditions before any export file is touched.

Recommended order:

1. Runtime export cleanup approval request
2. Runtime export cleanup implementation only after exact approval
3. Runtime export cleanup audit
4. Live consumer import/call planning only after cleanup audit or explicit decision to defer cleanup
5. Live consumer import/call lane only after a separate runtime call approval
6. Live provider/model call dispatch lane only after credential policy proof
7. Actual guarded file mutation execution only after stronger approval/rollback/shell policy evidence
8. Connector authority lane
9. Browser/network authority lane
10. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Runtime export cleanup approval request | Creates an exact gate to stabilize the candidate public API surface before live consumer calls. | High. | V1-G22, V1-G27 audit, authority-chain audit, readiness rollup. | Dedicated V1-G28 approval request. | LIMA docs/tests/fixtures request files only; no runtime export edits in the request branch. | Stop on export edits, live runtime calls, provider/model calls, secrets, connectors, browser/network, product-readiness claims. | Approval-request fixture tests, export-map metadata tests, no-runtime-change tests. | Yes. It is the next needed gate before touching exports. |
| Runtime export cleanup implementation | Cleans up candidate public exports under exact compatibility and rollback constraints. | Critical. | Approved V1-G28 request, frozen API import-smoke evidence, export diff, consumer notice plan. | Dedicated implementation approval recorded from V1-G28. | Exact export files plus docs/tests/fixtures named by the request. | Stop on unapproved symbol removal, consumer breakage, hidden runtime behavior, live calls, product-readiness claims. | Export-diff tests, import tests, compatibility fixtures, rollback tests, consumer smoke tests. | Later. It requires V1-G28 approval first. |
| Live consumer import/call planning | Designs fake-runtime or no-network call boundaries before any live consumer call. | High. | V1-G27 audit and runtime export cleanup decision. | Dedicated planning approval request. | LIMA docs/tests/fixtures only; no consumer runtime wiring. | Stop on live calls, runtime wiring, provider/model calls, secrets, connectors, browser/network, product-readiness claims. | Planning fixture tests, denied-path metadata tests, no-live-call tests. | Later. Cleanup request should come first. |
| Live consumer import/call lane | Executes live imports/calls from consumer shells into LIMA. | Critical. | Consumer import-smoke audit, final API/export decision, Guardian boundary, approval boundary, provider/model route boundary, runtime threat model. | Dedicated live import/call approval. | Consumer adapters, LIMA runtime boundary docs/tests, fake-runtime tests first. | Stop on bypassing Guardian, missing audit, secrets, provider/model calls, connectors, browser/network, physical-world, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests. | Later. Live calls are higher risk than export cleanup. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer call authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than export cleanup. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g28-runtime-export-cleanup-approval-request`.

Do not start runtime export cleanup implementation, live consumer imports/calls, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
