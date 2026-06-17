# V1 Post-G29 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g29`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G29. The current chain is capability-open and authority-gated, but still candidate-only. V1-G29 adds fake-runtime/no-network planning metadata for Sparkbot and Arc-Bot-shell; it does not approve fake-runtime call execution, live consumer imports/calls, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G30 fake-runtime consumer call evidence approval request`.

Reason: planning metadata now exists. The next safe step is a request-only gate for deterministic fake-runtime call evidence that can validate call boundaries without live providers, secrets, network, connectors, physical-world behavior, or product-readiness claims.

Recommended order:

1. Fake-runtime consumer call evidence approval request
2. Fake-runtime consumer call evidence implementation only after exact approval
3. Fake-runtime call evidence audit
4. Fake-runtime consumer repository test preview approval request
5. Fake-runtime consumer repository test preview and audit
6. Live consumer import/call lane only after fake-runtime call audit and separate approval
7. Live provider/model call dispatch lane only after credential policy proof
8. Connector authority lane
9. Browser/network authority lane
10. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fake-runtime consumer call evidence approval request | Creates an exact gate for deterministic fake-runtime call evidence without live calls. | High. | V1-G29 audit, authority-chain audit, readiness rollup. | Dedicated V1-G30 approval request. | LIMA docs/tests/fixtures request files only; no call implementation. | Stop on live calls, consumer repo edits, runtime wiring, provider/model calls, secrets, connectors, browser/network, product-readiness claims. | Approval-request fixture tests, fake-runtime boundary metadata tests, no-live-call tests. | Yes. It is the next needed evidence gate. |
| Fake-runtime consumer call evidence implementation | Adds deterministic fake-runtime call evidence for Sparkbot and Arc-Bot-shell. | Critical. | Approved V1-G30 request, G29 planning metadata. | Dedicated implementation approval recorded from V1-G30. | LIMA docs/tests/fixtures and possibly test-only fake-runtime helper if approved. | Stop on actual live calls, consumer source edits, shell wiring, secrets, provider/model calls, connectors, browser/network, product-readiness claims. | Fake-runtime evidence tests, denied-path metadata tests, consumer evidence link tests. | Later. It requires V1-G30 approval first. |
| Fake-runtime consumer repository test preview | Plans consumer-repo test files for fake-runtime call evidence without editing consumer repos yet. | High. | V1-G30 audit. | Dedicated preview approval request. | LIMA docs/tests/fixtures only; consumer patch previews only if approved. | Stop on consumer file edits, live calls, provider/model calls, secrets, connectors, browser/network. | Preview fixture tests, rollback tests, no-live-call tests. | Later. LIMA-side evidence should come first. |
| Live consumer import/call lane | Executes live imports/calls from consumer shells into LIMA. | Critical. | Fake-runtime call audit, final API/export decision, Guardian boundary, approval boundary, provider/model route boundary, runtime threat model. | Dedicated live import/call approval. | Consumer adapters, LIMA runtime boundary docs/tests, fake-runtime tests first. | Stop on bypassing Guardian, missing audit, secrets, provider/model calls, connectors, browser/network, physical-world, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests, then live tests only if approved. | Later. Live calls remain higher risk. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer call authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than fake-runtime evidence. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g30-fake-runtime-consumer-call-evidence-approval-request`.

Do not start fake-runtime consumer call evidence implementation, consumer repository test previews, live consumer imports/calls, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
