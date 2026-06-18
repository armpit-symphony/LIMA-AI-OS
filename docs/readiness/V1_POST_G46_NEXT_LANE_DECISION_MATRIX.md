# V1 Post-G46 Next Lane Decision Matrix

Date: 2026-06-17
Branch: `docs-v1-readiness-rollup-through-g46`
API status: `CANDIDATE_ONLY`

This matrix compares candidate authority lanes after V1-G46. The current chain is capability-open and authority-gated, but still candidate-only. V1-G46 adds a bounded LIMA harness execution wrapper that invokes only a caller-injected provider executor after authority, approval, audit, redaction, and boundary checks pass. It does not add built-in provider SDK clients, direct network clients, ambient secret lookup, credential value access, fallback execution, connector/browser/network authority, physical-world authority, or product readiness.

## Recommendation

Recommended next lane: `V1-G47 consumer fake-executor provider/model call smoke approval request`.

Reason: Sparkbot and Arc-Bot-shell can now test the public G46 harness wrapper with fake executors. That is the smallest consumer-facing validation step that exercises the new public API without live provider credentials, real network calls, connector behavior, production runtime calls, or product-readiness claims.

Recommended order:

1. Consumer fake-executor provider/model call smoke approval request
2. Consumer fake-executor tests only after exact approval
3. LIMA audit and readiness update
4. Provider credential/network hardening request
5. Built-in provider SDK integration request, if still needed
6. Fallback execution approval request
7. Connector/browser/network authority lane
8. Physical-world/device/robot/drone/IoT authority lane after a dedicated safety model

## Matrix

| Lane | Product Value | Risk Level | Prerequisites | Required Approvals | Likely File Scope | Stop Conditions | Tests Required | Should It Come Next? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Consumer fake-executor provider/model call smoke request | Verifies Sparkbot and Arc can import and call the G46 public wrapper with fake executors. | Medium. | V1-G46 implementation, G46 audit, authority-chain audit, readiness rollup, stable `lima.harness` exports. | Dedicated V1-G47 approval request. | LIMA request docs/tests/fixtures only; no consumer edits in the request. | Stop on consumer edits before approval, live provider calls, network calls, credentials, connector behavior, product-readiness claims. | Approval-request fixture tests, public export boundary tests, no-authority-escalation tests. | Yes. It gives consumer-facing proof without live services. |
| Consumer fake-executor provider/model call smoke implementation | Adds focused Sparkbot and Arc tests/fixtures that import the G46 wrapper and call it with fake executors. | Medium. | Approved V1-G47 request. | Dedicated implementation approval recorded from V1-G47. | Consumer test/fixture files plus LIMA evidence docs/tests/fixtures if approved. | Stop on production runtime calls, provider credentials, real network calls, secrets, connector/browser behavior, product-readiness claims. | Sparkbot fake-executor smoke tests, Arc fake-executor smoke tests, LIMA evidence tests, full relevant suites. | Later. It requires explicit approval first. |
| Provider credential/network hardening request | Defines how real credentials and provider egress would be authorized later. | Critical. | V1-G46 wrapper, secret policy, provider egress policy, redaction policy, audit retention. | Dedicated authority request. | Contracts/docs/tests first; runtime only after approval. | Stop on raw credential values, provider tokens, unscoped network calls, missing audit, missing approval. | No-secret-leak tests, denied-egress tests, audit-link tests. | Later. Consumer fake-executor proof should come first. |
| Built-in provider SDK integration | Adds first direct SDK-backed provider adapter if the injected executor boundary is not enough. | Critical. | Credential/network hardening, provider-specific scope, timeout/cost policy, audit policy. | Dedicated provider SDK approval request. | LIMA harness/provider adapter docs/tests/runtime only after approval. | Stop on ambient secrets, broad SDK access, missing timeout/cost bounds, fallback bypass, raw data persistence. | SDK fake tests, denied secret tests, egress boundary tests, full suite. | Later. Do not add SDK code before credential/network hardening. |
| Fallback execution lane | Opens controlled failover behavior after first execution path is stable. | High. | Live execution wrapper, fallback policy, cost/risk policy, audit evidence. | Dedicated fallback execution approval request. | LIMA contracts/docs/tests first; runtime only after approval. | Stop on silent fallback, unapproved provider expansion, secret lookup bypass, cost-policy bypass, missing audit link. | Fallback deny/allow tests, same-gate inheritance tests, audit-link tests. | Later. Fallback should not precede consumer fake-executor proof. |
| Connector/browser/network authority lane | Opens governed business systems, browser, and network workflows. | High. | URL/network policy, connector capability profiles, tenant scope, approval policy, audit retention. | Dedicated connector/browser/network approval request. | Contracts/docs first; future adapters only after approval. | Stop on live connector calls, credentials, external sends, customer record mutation, consumer integration bypass. | Static authority tests, tenant/scope tests, no live call tests, approval/audit linkage tests. | Later. Connector risk is broader than provider/model execution. |
| Physical-world/device/robot/drone/IoT authority lane | Establishes safety boundary for physical-world systems. | Critical. | Dedicated hazard model, emergency stop, simulator/dry-run, field safety policy, operator approval, rollback/stop semantics. | Dedicated physical-world authority/safety approval request. | Contracts/docs/threat model first; no drivers or live hardware until later approval. | Stop on live discovery, scanning, pairing, credentials, device commands, robot movement, safety-critical behavior. | Static threat tests first; later simulator-only tests; no live hardware tests without approval. | Not soon. Physical-world behavior requires a dedicated safety model. |

## Decision

Proceed next to `prepare-v1-g47-consumer-fake-executor-provider-model-call-smoke-approval-request`.

Do not start consumer repository edits, built-in provider SDK integration, credential handling, secret lookup, direct network calls, provider configuration edits, fallback execution, actual runtime file mutation execution, connector, browser/network, physical-world, or product-readiness work until their own approval gates exist.
