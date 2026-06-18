# V1 Post-G52 Next Lane Decision Matrix

Date: 2026-06-18
Branch: `docs-v1-readiness-rollup-through-g52`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G52. The current chain is capability-open and authority-gated, but still candidate-only. V1-G52 proves Sparkbot and Arc-Bot-shell can import and call the V1-G51 public wrapper with fake in-process provider executors only. It does not add built-in provider SDK clients, credential access, endpoint resolution, direct network egress, fallback execution, connector/browser/network authority, physical-world authority, consumer production runtime integration, or product readiness.

## Recommendation

Recommended next lane: `V1-G53 provider SDK/network/credential authority approval request`.

Reason: the G51 wrapper exists, and G52 proves both first consumers can exercise that wrapper through fake in-process executors. The next safety-critical boundary is whether LIMA should open any built-in provider SDK, provider endpoint resolution, credential-reference, or provider network-egress authority. That must start as a request-only gate with exact file scope, tests, rollback plan, and stop conditions before any implementation.

Recommended order:

1. Provider SDK/network/credential authority approval request
2. Provider SDK/network/credential authority design metadata only after exact approval
3. Bounded fake-SDK or fake-egress harness evidence before real egress
4. Real provider SDK/egress implementation only after a later exact implementation approval
5. Fallback execution approval request
6. Connector/browser/network authority lane
7. Consumer production runtime integration lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model
9. Product-readiness lane only after runtime, security, field operations, and rollback evidence exist

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Provider SDK/network/credential authority request | Asks whether LIMA should prepare the first authority gate for built-in provider SDK clients, endpoint scope, credential references, and provider egress. | Critical. | V1-G48 hardening, V1-G51 wrapper, V1-G52 consumer fake-executor proof. | Dedicated V1-G53 approval request. | LIMA request docs/tests/fixtures only. | Stop on SDK code, endpoint resolution, network calls, secret lookup, credential values, provider tokens, fallback, connectors, product claims. | Approval-request fixture tests, forbidden behavior assertions, evidence-ref checks. | Yes, as request-only gate. |
| Provider SDK/network/credential authority design metadata | Defines scoped metadata for a future SDK/egress slice without implementing SDK or network behavior. | Critical. | Approved V1-G53 request. | Dedicated implementation approval from V1-G53. | LIMA docs/tests/fixtures only unless the approval explicitly names runtime files. | Stop on live SDK clients, real endpoint resolution, network calls, credential value access, raw data persistence. | Static authority metadata tests, denied/allowed boundary fixture tests. | Later. It requires explicit approval first. |
| Fake-SDK or fake-egress harness evidence | Proves SDK/egress-shaped boundaries without using real providers, real endpoints, or credentials. | High. | SDK/network/credential authority metadata. | Separate fake-harness approval request. | Tests/fixtures plus docs; no real provider SDK by default. | Stop on real network egress, real secrets, live provider calls, endpoint lookup, fallback, raw content persistence. | Fake SDK deny/allow tests, no-network tests, no-secret tests. | Later. Useful before any real SDK implementation. |
| Real provider SDK/egress implementation | Adds first governed real provider path. | Critical. | Approved authority metadata, fake harness evidence, explicit provider scope, timeout/cost policy, audit policy, credential reference policy. | Dedicated real provider implementation approval request. | Exact LIMA provider/harness runtime files only after approval. | Stop on ambient secrets, broad SDK access, unscoped endpoints, missing timeout/cost bounds, fallback bypass, raw data persistence. | SDK fake tests, denied secret tests, egress boundary tests, full suite, focused consumer tests. | Not yet. It should not come before request/design/fake-harness evidence. |
| Fallback execution lane | Opens controlled failover behavior after first governed provider path is constrained. | High. | Governed provider execution path, credential/network hardening, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede first governed provider authority. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider execution. |
| Consumer production runtime integration lane | Wires Sparkbot or Arc-Bot-shell production runtime/source paths to LIMA-owned calls. | Critical. | Provider authority boundaries, no-secret/no-network proof, approval/audit evidence, rollback plan per consumer. | Dedicated consumer production integration approval request. | Exact consumer runtime/source files plus LIMA evidence only after approval. | Stop on unbounded imports, route wiring without Guardian, raw prompt persistence, network/provider calls outside approved path, production claims. | Consumer focused tests, import/call tests, rollback tests, full relevant suites. | Later. Test evidence exists, but production integration is not approved. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |
| Product readiness lane | Converts candidate runtime evidence into release readiness only after operational controls exist. | Critical. | Runtime audits, security model, deployment/runbook evidence, rollback, support, observability, incident handling, consumer integration proof. | Dedicated product-readiness approval request. | Readiness docs/tests/checklists first; no production claims before approval. | Stop on unresolved security gaps, missing rollback, missing support/ops model, untested provider/network/connector boundaries. | Readiness checklist tests, runbook validation, security evidence checks. | Not yet. Current status remains candidate-only. |

## Decision

Proceed next to `prepare-v1-g53-provider-sdk-network-credential-authority-approval-request`.

Do not start built-in provider SDK integration, credential handling, secret lookup, direct network calls, endpoint resolution, provider configuration edits, fallback execution, actual runtime file mutation execution, consumer production runtime integration, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
