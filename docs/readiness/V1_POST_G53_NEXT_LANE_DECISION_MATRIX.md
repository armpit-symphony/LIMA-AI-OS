# V1 Post-G53 Next Lane Decision Matrix

Date: 2026-06-18
Branch: `docs-v1-readiness-rollup-through-g53`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G53. The current chain is capability-open and authority-gated, but still candidate-only. V1-G53 defines metadata-only authority records for future built-in provider SDK authority, endpoint-resolution authority, provider network-egress authority, and credential-reference authority. It does not add fake SDK harness evidence, built-in provider SDK clients, endpoint resolution execution, network egress execution, secret lookup, credential value access, provider token/API key access, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, or product readiness.

## Recommendation

Recommended next lane: `V1-G54 fake SDK/fake-egress harness approval request`.

Reason: the G53 authority metadata exists, but no SDK-shaped or egress-shaped harness has proven that future provider paths can remain no-secret, no-network, no-real-endpoint, no-token, no-credential-value, and fail-closed. Before any real provider SDK, endpoint, or network behavior is considered, LIMA should ask for a request-only gate for bounded fake SDK or fake-egress harness evidence.

Recommended order:

1. Fake SDK/fake-egress harness approval request
2. Fake SDK/fake-egress harness evidence only after exact approval
3. Real provider SDK/egress approval request only after fake harness evidence is audited
4. Real provider SDK/egress implementation only after a later exact implementation approval
5. Fallback execution approval request
6. Connector/browser/network authority lane
7. Consumer production runtime integration lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model
9. Product-readiness lane only after runtime, security, field operations, support, rollback, and incident evidence exist

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fake SDK/fake-egress harness request | Asks whether LIMA should prepare bounded fake evidence for SDK-shaped and egress-shaped provider paths without real SDK clients, endpoints, credentials, or network calls. | High. | V1-G48 hardening, V1-G51 wrapper, V1-G52 consumer fake-executor proof, V1-G53 authority metadata. | Dedicated V1-G54 approval request. | LIMA request docs/tests/fixtures only. | Stop on real SDK clients, endpoint execution, network calls, direct provider egress, secret lookup, credential values, provider tokens, fallback, connectors, product claims. | Approval-request fixture tests, forbidden behavior assertions, prior evidence-ref checks. | Yes, as request-only gate. |
| Fake SDK/fake-egress harness evidence | Proves SDK-shaped or egress-shaped boundaries with fake in-process components only. | High. | Approved V1-G54 request. | Dedicated implementation approval from V1-G54. | Likely LIMA docs/tests/fixtures and possibly test-only helper files only if the approval explicitly names them. | Stop on real SDK dependencies, live endpoints, DNS/HTTP/socket calls, credential value access, provider token access, fallback, raw content persistence. | Fake SDK deny/allow tests, no-network tests, no-secret tests, no-endpoint tests, audit-link tests, full suite. | Later. It requires explicit approval first. |
| Real provider SDK/egress approval request | Asks whether to open the first governed real provider SDK/network path. | Critical. | G53 authority metadata, audited fake harness evidence, provider scope, timeout/cost/failure/redaction policies. | Dedicated real provider SDK/egress approval request. | Request docs/tests/fixtures only. | Stop on implementation, ambient secrets, unscoped endpoints, missing cost/timeout policy, fallback bypass, raw persistence. | Approval-request static tests and authority-chain checks. | Not yet. Fake harness proof should come first. |
| Real provider SDK/egress implementation | Adds first governed real provider path. | Critical. | Approved real provider request, fake harness audit, credential-reference policy, network policy, provider/model scope, rollback plan. | Dedicated implementation approval. | Exact LIMA provider/harness runtime files only after approval. | Stop on ambient secret lookup, broad SDK access, unscoped endpoints, missing timeout/cost bounds, fallback bypass, raw data persistence. | SDK fake tests, denied secret tests, egress boundary tests, full suite, focused consumer tests. | Not yet. |
| Fallback execution lane | Opens controlled failover behavior after first governed provider path is constrained. | High. | Governed provider execution path, credential/network hardening, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede first governed provider path. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider execution. |
| Consumer production runtime integration lane | Wires Sparkbot or Arc-Bot-shell production runtime/source paths to LIMA-owned calls. | Critical. | Provider authority boundaries, no-secret/no-network proof, approval/audit evidence, rollback plan per consumer. | Dedicated consumer production integration approval request. | Exact consumer runtime/source files plus LIMA evidence only after approval. | Stop on unbounded imports, route wiring without Guardian, raw prompt persistence, network/provider calls outside approved path, production claims. | Consumer focused tests, import/call tests, rollback tests, full relevant suites. | Later. Test evidence exists, but production integration is not approved. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |
| Product readiness lane | Converts candidate runtime evidence into release readiness only after operational controls exist. | Critical. | Runtime audits, security model, deployment/runbook evidence, rollback, support, observability, incident handling, consumer integration proof. | Dedicated product-readiness approval request. | Readiness docs/tests/checklists first; no production claims before approval. | Stop on unresolved security gaps, missing rollback, missing support/ops model, untested provider/network/connector boundaries. | Readiness checklist tests, runbook validation, security evidence checks. | Not yet. Current status remains candidate-only. |

## Decision

Proceed next to `prepare-v1-g54-fake-sdk-egress-harness-approval-request`.

Do not start fake SDK harness implementation, fake egress harness implementation, real provider SDK integration, credential handling, secret lookup, direct network calls, endpoint resolution execution, provider configuration edits, fallback execution, actual runtime file mutation execution, consumer production runtime integration, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
