# V1 Post-G54 Next Lane Decision Matrix

Date: 2026-06-18
Branch: `docs-v1-readiness-rollup-through-g54`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G54. The current chain is capability-open and authority-gated, but still candidate-only. V1-G54 proves that SDK-shaped and egress-shaped provider boundaries can be modeled with deterministic test-module-local fake components while remaining no-secret, no-network, no-real-endpoint, no-token, no-credential-value, and fail-closed.

## Recommendation

Recommended next lane: `V1-G55 real provider SDK/network egress approval request`.

Reason: the G53 authority metadata and G54 fake harness evidence exist, but no real provider SDK/network path is approved. The next safe step is not implementation. It is a request-only gate asking whether LIMA should define a tightly scoped real provider SDK/network egress lane with explicit authority, credential-reference, endpoint, timeout, cost, redaction, denial, rollback, and stop-condition metadata.

Recommended order:

1. Real provider SDK/network egress approval request
2. Real provider SDK/network egress implementation only after exact approval
3. Consumer fake/live integration proof against the approved path
4. Fallback execution approval request only after the first governed provider path is constrained
5. Connector/browser/network authority lane
6. Consumer production runtime integration lane
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model
8. Product-readiness lane only after runtime, security, field operations, support, rollback, and incident evidence exist

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Real provider SDK/network egress approval request | Asks whether LIMA should open the first tightly scoped real provider SDK/network path after fake harness proof. | Critical. | V1-G48 hardening, V1-G51 wrapper, V1-G52 consumer fake-executor proof, V1-G53 authority metadata, audited V1-G54 fake harness evidence. | Dedicated V1-G55 approval request. | LIMA request docs/tests/fixtures only. | Stop on implementation, real SDK clients, endpoint execution, DNS/HTTP/socket/network calls, direct provider egress, secret lookup, credential values, provider tokens, fallback, connectors, product claims. | Approval-request fixture tests, forbidden behavior assertions, prior evidence-ref checks, authority-chain checks. | Yes, as request-only gate. |
| Real provider SDK/network egress implementation | Adds first governed real provider path. | Critical. | Approved V1-G55 request, fake harness audit, credential-reference policy, network policy, provider/model scope, rollback plan. | Dedicated implementation approval. | Exact LIMA provider/harness runtime files only after approval. | Stop on ambient secret lookup, broad SDK access, unscoped endpoints, missing timeout/cost bounds, fallback bypass, raw data persistence. | SDK fake tests, denied secret tests, egress boundary tests, full suite, focused consumer tests. | Later. It requires explicit approval first. |
| Consumer fake/live integration proof | Proves Sparkbot and Arc-Bot-shell can call the governed provider path through approved public APIs without bypass. | Critical. | Approved provider implementation, frozen public API update if needed, consumer branch approval, rollback plan. | Dedicated consumer integration approval request. | Exact consumer docs/tests/source files plus LIMA evidence only after approval. | Stop on unbounded imports, direct provider access, raw prompt persistence, missing Guardian/audit linkage, production claims. | Consumer import/call tests, LIMA focused tests, rollback tests. | Later. |
| Fallback execution lane | Opens controlled failover behavior after first governed provider path is constrained. | High. | Governed provider execution path, credential/network hardening, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede first governed provider path. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider execution. |
| Consumer production runtime integration lane | Wires Sparkbot or Arc-Bot-shell production runtime/source paths to LIMA-owned calls. | Critical. | Provider authority boundaries, no-secret/no-network proof, approval/audit evidence, rollback plan per consumer. | Dedicated consumer production integration approval request. | Exact consumer runtime/source files plus LIMA evidence only after approval. | Stop on unbounded imports, route wiring without Guardian, raw prompt persistence, network/provider calls outside approved path, production claims. | Consumer focused tests, import/call tests, rollback tests, full relevant suites. | Later. Test evidence exists, but production integration is not approved. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |
| Product readiness lane | Converts candidate runtime evidence into release readiness only after operational controls exist. | Critical. | Runtime audits, security model, deployment/runbook evidence, rollback, support, observability, incident handling, consumer integration proof. | Dedicated product-readiness approval request. | Readiness docs/tests/checklists first; no production claims before approval. | Stop on unresolved security gaps, missing rollback, missing support/ops model, untested provider/network/connector boundaries. | Readiness checklist tests, runbook validation, security evidence checks. | Not yet. Current status remains candidate-only. |

## Decision

Proceed next to `prepare-v1-g55-real-provider-sdk-network-egress-approval-request`.

Do not start real provider SDK integration, credential handling, secret lookup, direct network calls, endpoint resolution execution, provider configuration edits, fallback execution, actual runtime file mutation execution, consumer production runtime integration, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
