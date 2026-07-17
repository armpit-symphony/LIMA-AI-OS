# V1 Post-G55 Next Lane Decision Matrix

Date: 2026-06-19
Branch: `audit-v1-g55-real-provider-sdk-network-egress`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G55. The current chain is capability-open and authority-gated, but still candidate-only. V1-G55 proves a bounded LIMA-owned wrapper that validates authority-chain metadata and calls only a caller-injected provider SDK/network executor.

## Recommendation

Recommended next lane: `V1-G56 consumer fake-executor provider SDK/network egress smoke approval request`.

Reason: the G55 wrapper is public candidate API. Before credential value access, fallback, connector/browser/network authority, or consumer production runtime integration, the next safest proof is a request-only gate for first-shell consumers to import and call the G55 wrapper with fake in-process provider SDK/network executors only.

Recommended order:

1. Consumer fake-executor provider SDK/network egress smoke approval request.
2. Consumer fake-executor provider SDK/network egress smoke implementation only after exact approval.
3. Credential value access approval request only after fake consumer compatibility is audited.
4. Fallback execution approval request only after the first governed provider path remains constrained.
5. Connector/browser/network authority lane.
6. Consumer production runtime integration lane.
7. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model.
8. Product-readiness lane only after runtime, security, field operations, support, rollback, and incident evidence exist.

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer fake-executor provider SDK/network egress smoke approval request | Asks whether Sparkbot and Arc-Bot-shell should prove import/call compatibility with the V1-G55 wrapper using fake injected SDK/network executors only. | High. | Audited V1-G55 wrapper, V1-G54 fake SDK/fake-egress evidence, V1-G53 authority metadata, V1-G52 consumer fake-executor precedent. | Dedicated V1-G56 approval request. | LIMA request docs/tests/fixtures only. | Stop on consumer repo edits, live provider credentials, built-in SDK clients, endpoint execution, DNS/HTTP/socket/network calls, direct provider egress, secret lookup, credential values, provider tokens, fallback, connectors, product claims. | Approval-request fixture tests, forbidden behavior assertions, prior evidence-ref checks, public API import expectations. | Yes, as request-only gate. |
| Consumer fake-executor provider SDK/network egress smoke implementation | Proves first-shell consumers can import and call the G55 wrapper without bypassing its caller-injected executor boundary. | High. | Approved V1-G56 request, audited G55 wrapper, rollback plan per consumer. | Dedicated implementation approval from V1-G56. | Exact consumer test/source files plus LIMA evidence only if approval names them. | Stop on real provider calls, credentials, network, direct SDK clients, raw prompt persistence, production wiring, Guardian bypass, product claims. | Consumer import/call tests, LIMA focused tests, rollback checks, no-network/no-secret assertions. | Later. It requires explicit approval first. |
| Credential value access approval request | Asks whether any provider credential value may be presented to caller-owned executor boundaries under controlled policy. | Critical. | Audited fake consumer compatibility, credential-reference policy, redaction/audit policy, vault ownership model. | Dedicated credential value access approval request. | Request docs/tests/fixtures first. | Stop on ambient secret lookup, provider token persistence, broad vault access, missing audit refs, endpoint/network broadening, fallback bypass. | Credential-deny tests, redaction tests, audit-link tests, policy reference checks. | Later. Consumer fake proof should come first. |
| Fallback execution lane | Opens controlled failover behavior after the provider path and credential policy are constrained. | High. | Governed provider execution path, credential/network hardening, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede fake consumer proof. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider execution. |
| Consumer production runtime integration lane | Wires Sparkbot or Arc-Bot-shell production runtime/source paths to LIMA-owned calls. | Critical. | Provider authority boundaries, no-secret/no-network proof, approval/audit evidence, rollback plan per consumer. | Dedicated consumer production integration approval request. | Exact consumer runtime/source files plus LIMA evidence only after approval. | Stop on unbounded imports, route wiring without Guardian, raw prompt persistence, network/provider calls outside approved path, production claims. | Consumer focused tests, import/call tests, rollback tests, full relevant suites. | Later. Test evidence exists, but production integration is not approved. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |
| Product readiness lane | Converts candidate runtime evidence into release readiness only after operational controls exist. | Critical. | Runtime audits, security model, deployment/runbook evidence, rollback, support, observability, incident handling, consumer integration proof. | Dedicated product-readiness approval request. | Readiness docs/tests/checklists first; no production claims before approval. | Stop on unresolved security gaps, missing rollback, missing support/ops model, untested provider/network/connector boundaries. | Readiness checklist tests, runbook validation, security evidence checks. | Not yet. Current status remains candidate-only. |

## Decision

Proceed next to `prepare-v1-g56-consumer-fake-executor-provider-sdk-network-egress-smoke-approval-request`.

Do not start consumer fake-executor smoke implementation, credential handling, secret lookup, direct network calls, endpoint resolution execution, provider configuration edits, fallback execution, actual runtime file mutation execution, consumer production runtime integration, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
