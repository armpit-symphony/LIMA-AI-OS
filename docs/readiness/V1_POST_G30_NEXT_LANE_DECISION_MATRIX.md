# V1 Post-G30 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g30`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G30. The current chain is capability-open and authority-gated, but still candidate-only. V1-G30 adds deterministic fake-runtime consumer call evidence metadata for Sparkbot and Arc-Bot-shell; it does not approve fake call execution, live consumer imports/calls, shell wiring, live provider/model calls, connector authority, browser/network authority, physical-world authority, consumer repository mutation, or product readiness.

## Recommendation

Recommended next lane: `V1-G31 fake-runtime consumer repository test preview approval request`.

Reason: fake-runtime call evidence now exists in LIMA. The next safe step is a request-only gate for previewing consumer repository test files that would exercise the fake-runtime evidence boundary without editing consumer repos yet, calling live runtimes, using providers/models, reading secrets, using network/connectors, touching physical-world systems, or claiming product readiness.

Recommended order:

1. Fake-runtime consumer repository test preview approval request
2. Fake-runtime consumer repository test preview implementation only after exact approval
3. Fake-runtime consumer repository test preview audit
4. Consumer repository test edit approval request
5. Consumer repository test edit and import-smoke audit
6. Live consumer import/call lane only after fake-runtime repository test audit and separate approval
7. Live provider/model call dispatch lane only after credential policy proof
8. Connector authority lane
9. Browser/network authority lane
10. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fake-runtime consumer repository test preview approval request | Creates an exact gate for previewing consumer test files without editing consumer repos. | High. | V1-G30 audit, authority-chain audit, readiness rollup. | Dedicated V1-G31 approval request. | LIMA docs/tests/fixtures request files only; no preview implementation. | Stop on consumer repo edits, live calls, runtime wiring, provider/model calls, secrets, connectors, browser/network, product-readiness claims. | Approval-request fixture tests, no-consumer-edit tests, fake-runtime boundary metadata tests. | Yes. It is the next needed evidence gate. |
| Fake-runtime consumer repository test preview implementation | Adds deterministic LIMA-side preview metadata for future Sparkbot and Arc-Bot-shell test files. | High. | Approved V1-G31 request, G30 fake-runtime call evidence. | Dedicated implementation approval recorded from V1-G31. | LIMA docs/tests/fixtures only, unless a future gate explicitly approves more. | Stop on consumer file edits, live runtime calls, adapter symbol execution, secrets, provider/model calls, connectors, browser/network, product-readiness claims. | Preview fixture tests, rollback tests, no-live-call tests, no-consumer-mutation tests. | Later. It requires V1-G31 approval first. |
| Consumer repository test edit lane | Adds actual consumer repo tests from the approved preview. | Critical. | Approved preview and audit, exact consumer file map. | Dedicated consumer repo edit approval. | Consumer test/fixture files only, plus LIMA intake docs/tests if approved. | Stop on runtime source edits, shell wiring, live calls, provider/model calls, secrets, connectors, browser/network, physical-world behavior. | Consumer focused import-smoke tests, LIMA intake tests, diff checks in all repos. | Later. Preview should come first. |
| Live consumer import/call lane | Executes live imports/calls from consumer shells into LIMA. | Critical. | Fake-runtime repository test audit, final API/export decision, Guardian boundary, approval boundary, provider/model route boundary, runtime threat model. | Dedicated live import/call approval. | Consumer adapters, LIMA runtime boundary docs/tests, fake-runtime tests first. | Stop on bypassing Guardian, missing audit, secrets, provider/model calls, connectors, browser/network, physical-world, product-readiness claims. | Fake-runtime tests, denied path tests, audit-link tests, no-network/no-secret tests, then live tests only if approved. | Later. Live calls remain higher risk. |
| Live provider/model call dispatch lane | Enables actual model selection and fallback under Guardian and Harness control. | Critical. | V1-G20 metadata, credential policy, Vault boundary, audit persistence, live-call threat model. | Dedicated live dispatch approval request. | Harness provider boundary, Guardian route gate, Vault references, docs/tests/fixtures. | Stop on raw credentials, unscoped provider access, external sends, missing audit, consumer wiring bypass, product-readiness claims. | No-secret tests, fake-provider tests, denied route tests, fallback policy tests, audit-link tests, no live network by default. | Later. Consumer call authority should be clearer first. |
| Connector authority lane | Opens path toward governed business systems and office workflows. | High. | Consumer proof intake, connector capability profiles, tenant scope, approval policy, audit retention, approval evidence capture. | Dedicated connector authority approval request. | Contracts/docs first; future connector adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration. | Static connector authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is higher than fake-runtime evidence. |
| Browser/network authority lane | Enables controlled research, web workflows, and network automation. | High. | URL/network policy, shell/harness guiderails, approval policy, audit evidence, credential policy, consumer proof. | Dedicated browser/network approval request. | Browser/network contracts, Guardian docs/tests. | Stop on live browsing/network calls, external sends, credential use, unscoped access. | Blocked live-call tests, scoped metadata tests, approval requirement tests, audit-link tests. | Later. Needs separate threat model and approval lane. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g31-fake-runtime-consumer-repo-test-preview-approval-request`.

Do not start fake-runtime consumer repository test preview implementation, consumer repository edits, live consumer imports/calls, live provider/model calls, credential handling, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
